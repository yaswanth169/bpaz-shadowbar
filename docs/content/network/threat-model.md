# Threat Model

ShadowBar is designed with a "Defense in Depth" approach.

## Trust Boundaries

1.  **The Agent**: Untrusted code. Can be hallucinating or compromised.
2.  **The Framework**: Trusted code. Enforces policy.
3.  **The Network**: Hostile environment. All traffic must be encrypted and authorized.

## Mitigations

*   **Prompt Injection**: Mitigated by separating system prompts and user input.
*   **Data Exfiltration**: Mitigated by the `Trust` allowlist for network hosts.
*   **Unauthorized Action**: Mitigated by `shell_approval` and explicit tool permissions.
