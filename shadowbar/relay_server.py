"""
ShadowBar Relay Server
A WebSocket-based message broker for agent-to-agent communication.

Run: uvicorn shadowbar.relay_server:app --host 0.0.0.0 --port 8000

This is a minimal relay server implementation for internal Barclays use.
For production deployment, consider:
- Adding Redis for persistent agent storage
- Adding authentication middleware
- Adding rate limiting
- Deploying behind a reverse proxy
"""

import asyncio
import json
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass, field

try:
    from fastapi import FastAPI, WebSocket, WebSocketDisconnect
    from nacl.signing import VerifyKey
    from nacl.exceptions import BadSignatureError
except ImportError:
    raise ImportError(
        "ShadowBar Relay Server requires additional dependencies.\n"
        "Install with: pip install fastapi uvicorn pynacl"
    )

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("shadowbar-relay")

app = FastAPI(title="ShadowBar Relay Server")


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class RegisteredAgent:
    """Represents a registered agent in the relay."""
    address: str                          # Ed25519 public key (0x...)
    summary: str                          # Description of capabilities
    endpoints: list                       # Connection endpoints
    websocket: WebSocket                  # Active WebSocket connection
    last_announce: float = field(default_factory=time.time)
    last_heartbeat: float = field(default_factory=time.time)


# In-memory agent registry
# Key: agent address (0x...), Value: RegisteredAgent
agents: Dict[str, RegisteredAgent] = {}

# Pending INPUT messages waiting for response
# Key: input_id, Value: {"websocket": WebSocket, "timestamp": float}
pending_inputs: Dict[str, Dict] = {}


# ============================================================================
# SIGNATURE VERIFICATION
# ============================================================================

def verify_signature(message: Dict[str, Any]) -> bool:
    """
    Verify Ed25519 signature on ANNOUNCE message.
    
    The signature is created by:
    1. Removing 'signature' field from message
    2. JSON serializing with sort_keys=True
    3. Signing with Ed25519 private key
    """
    try:
        # Extract signature and address
        signature_hex = message.get("signature", "")
        address = message.get("address", "")
        
        if not signature_hex or not address:
            return False
        
        # Remove 0x prefix if present
        if signature_hex.startswith("0x"):
            signature_hex = signature_hex[2:]
        if address.startswith("0x"):
            public_key_hex = address[2:]
        else:
            public_key_hex = address
        
        # Create message without signature for verification
        message_to_verify = {k: v for k, v in message.items() if k != "signature"}
        message_bytes = json.dumps(message_to_verify, sort_keys=True).encode('utf-8')
        
        # Convert hex to bytes
        signature_bytes = bytes.fromhex(signature_hex)
        public_key_bytes = bytes.fromhex(public_key_hex)
        
        # Verify using PyNaCl
        verify_key = VerifyKey(public_key_bytes)
        verify_key.verify(message_bytes, signature_bytes)
        
        return True
        
    except (BadSignatureError, ValueError, Exception) as e:
        logger.warning(f"Signature verification failed: {e}")
        return False


# ============================================================================
# WEBSOCKET ENDPOINTS
# ============================================================================

@app.websocket("/ws/announce")
async def announce_endpoint(websocket: WebSocket):
    """
    Endpoint for agents to register and receive tasks.
    
    Protocol:
    1. Agent sends ANNOUNCE message
    2. Server stores agent in registry
    3. Server forwards INPUT messages to agent
    4. Agent sends OUTPUT messages back
    """
    await websocket.accept()
    agent_address = None
    
    try:
        while True:
            # Receive message from agent
            data = await websocket.receive_text()
            message = json.loads(data)
            msg_type = message.get("type")
            
            if msg_type == "ANNOUNCE":
                # Verify signature
                if not verify_signature(message):
                    await websocket.send_json({
                        "type": "ERROR",
                        "error": "Invalid signature"
                    })
                    continue
                
                # Register agent
                agent_address = message["address"]
                agents[agent_address] = RegisteredAgent(
                    address=agent_address,
                    summary=message.get("summary", ""),
                    endpoints=message.get("endpoints", []),
                    websocket=websocket,
                    last_announce=time.time()
                )
                
                logger.info(f"✓ Agent registered: {agent_address[:16]}...")
                
            elif msg_type == "OUTPUT":
                # Agent is responding to an INPUT
                input_id = message.get("input_id")
                
                if input_id in pending_inputs:
                    # Forward response to waiting client
                    client_ws = pending_inputs[input_id]["websocket"]
                    try:
                        await client_ws.send_json(message)
                        logger.info(f"✓ Forwarded OUTPUT for {input_id[:8]}...")
                    except Exception as e:
                        logger.warning(f"Failed to forward OUTPUT: {e}")
                    finally:
                        del pending_inputs[input_id]
                        
            elif msg_type == "HEARTBEAT":
                # Update last seen time
                if agent_address and agent_address in agents:
                    agents[agent_address].last_heartbeat = time.time()
                    
    except WebSocketDisconnect:
        logger.info(f"Agent disconnected: {agent_address[:16] if agent_address else 'unknown'}...")
    except Exception as e:
        logger.error(f"Error in announce endpoint: {e}")
    finally:
        # Remove agent from registry
        if agent_address and agent_address in agents:
            del agents[agent_address]
            logger.info(f"✗ Agent removed: {agent_address[:16]}...")


@app.websocket("/ws/input")
async def input_endpoint(websocket: WebSocket):
    """
    Endpoint for clients to send tasks to agents.
    
    Protocol:
    1. Client sends INPUT message with target agent address
    2. Server routes to agent via their WebSocket
    3. Server waits for OUTPUT from agent
    4. Server forwards OUTPUT to client
    """
    await websocket.accept()
    
    try:
        # Receive INPUT request
        data = await websocket.receive_text()
        message = json.loads(data)
        
        if message.get("type") != "INPUT":
            await websocket.send_json({
                "type": "ERROR",
                "error": "Expected INPUT message"
            })
            return
        
        # Extract fields
        input_id = message.get("input_id")
        target_address = message.get("to")
        prompt = message.get("prompt")
        
        if not all([input_id, target_address, prompt]):
            await websocket.send_json({
                "type": "ERROR",
                "error": "Missing required fields: input_id, to, prompt"
            })
            return
        
        # Check if target agent is online
        if target_address not in agents:
            await websocket.send_json({
                "type": "ERROR",
                "error": f"Agent not found or offline: {target_address[:16]}..."
            })
            return
        
        # Get agent's WebSocket
        agent = agents[target_address]
        
        # Store pending request
        pending_inputs[input_id] = {
            "websocket": websocket,
            "timestamp": time.time()
        }
        
        # Forward INPUT to agent
        try:
            await agent.websocket.send_json({
                "type": "INPUT",
                "input_id": input_id,
                "prompt": prompt,
                "from_address": message.get("from", "unknown")
            })
            logger.info(f"→ Forwarded INPUT {input_id[:8]}... to {target_address[:16]}...")
        except Exception as e:
            del pending_inputs[input_id]
            await websocket.send_json({
                "type": "ERROR",
                "error": f"Failed to reach agent: {e}"
            })
            return
        
        # Wait for response (with timeout)
        timeout = 300  # 5 minutes
        start_time = time.time()
        
        while input_id in pending_inputs:
            if time.time() - start_time > timeout:
                del pending_inputs[input_id]
                await websocket.send_json({
                    "type": "ERROR",
                    "error": "Request timed out"
                })
                return
            await asyncio.sleep(0.1)
        
        # Response was already sent by announce_endpoint
        
    except WebSocketDisconnect:
        logger.info("Client disconnected from /ws/input")
    except Exception as e:
        logger.error(f"Error in input endpoint: {e}")
        try:
            await websocket.send_json({
                "type": "ERROR",
                "error": str(e)
            })
        except:
            pass


@app.websocket("/ws/lookup")
async def lookup_endpoint(websocket: WebSocket):
    """
    Endpoint for discovering agents.
    
    Supports:
    - GET_AGENT: Get specific agent by address
    - FIND: Search agents by capability
    - LIST_ALL: List all online agents
    """
    await websocket.accept()
    
    try:
        data = await websocket.receive_text()
        message = json.loads(data)
        msg_type = message.get("type")
        
        if msg_type == "GET_AGENT":
            address = message.get("address")
            
            if address in agents:
                agent = agents[address]
                await websocket.send_json({
                    "type": "AGENT_INFO",
                    "agent": {
                        "address": agent.address,
                        "summary": agent.summary,
                        "endpoints": agent.endpoints,
                        "online": True,
                        "last_seen": agent.last_announce
                    }
                })
            else:
                await websocket.send_json({
                    "type": "AGENT_INFO",
                    "agent": None,
                    "error": "Agent not found or offline"
                })
                
        elif msg_type == "FIND":
            query = message.get("query", "").lower()
            
            # Simple substring matching (could use embeddings for semantic search)
            matching_agents = []
            for agent in agents.values():
                if query in agent.summary.lower():
                    matching_agents.append({
                        "address": agent.address,
                        "summary": agent.summary,
                        "endpoints": agent.endpoints,
                        "last_seen": agent.last_announce
                    })
            
            await websocket.send_json({
                "type": "AGENTS",
                "query": query,
                "agents": matching_agents[:10]  # Limit to 10 results
            })
            
        elif msg_type == "LIST_ALL":
            # List all online agents
            all_agents = [{
                "address": agent.address,
                "summary": agent.summary,
                "online": True
            } for agent in agents.values()]
            
            await websocket.send_json({
                "type": "AGENTS",
                "agents": all_agents
            })
            
    except WebSocketDisconnect:
        pass
    except Exception as e:
        logger.error(f"Error in lookup endpoint: {e}")


# ============================================================================
# HTTP ENDPOINTS (for monitoring)
# ============================================================================

@app.get("/")
async def root():
    """Health check and info."""
    return {
        "service": "ShadowBar Relay Server",
        "status": "running",
        "agents_online": len(agents),
        "pending_requests": len(pending_inputs)
    }


@app.get("/agents")
async def list_agents():
    """List all registered agents (for debugging)."""
    return {
        "count": len(agents),
        "agents": [
            {
                "address": agent.address[:20] + "...",
                "summary": agent.summary[:100] + "..." if len(agent.summary) > 100 else agent.summary,
                "last_seen": agent.last_announce
            }
            for agent in agents.values()
        ]
    }


# ============================================================================
# BACKGROUND TASKS
# ============================================================================

@app.on_event("startup")
async def startup():
    """Start background cleanup task."""
    asyncio.create_task(cleanup_stale_agents())
    logger.info("🚀 ShadowBar Relay Server started")


async def cleanup_stale_agents():
    """Remove agents that haven't sent heartbeat in 2 minutes."""
    while True:
        await asyncio.sleep(30)  # Check every 30 seconds
        
        now = time.time()
        stale_threshold = 120  # 2 minutes
        
        stale_addresses = [
            addr for addr, agent in agents.items()
            if now - agent.last_announce > stale_threshold
        ]
        
        for addr in stale_addresses:
            del agents[addr]
            logger.info(f"🧹 Cleaned up stale agent: {addr[:16]}...")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


