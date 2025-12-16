import { Home, Zap, Terminal, Box, Layout, PenTool, Cpu, Mail, Globe, Bug, Shield, Link as LinkIcon } from "lucide-react"

export const navItems = [
    {
        title: "Getting Started",
        items: [
            { title: "Introduction", href: "/getting-started/introduction", icon: Home },
            { title: "Quick Start", href: "/getting-started/quick-start", icon: Zap },
            { title: "Philosophy", href: "/getting-started/philosophy", icon: Terminal },
        ],
    },
    {
        title: "Project",
        items: [
            { title: "Roadmap", href: "/roadmap", icon: Box },
        ],
    },
    {
        title: "Core Concepts",
        items: [
            { title: "Agent", href: "/core-concepts/agent", icon: Box },
            { title: "Tools", href: "/core-concepts/tools", icon: PenTool },
            { title: "Models", href: "/core-concepts/models", icon: Cpu },
            { title: "LLM Function", href: "/core-concepts/llm-function", icon: Zap },
            { title: "Event System", href: "/core-concepts/events", icon: Zap },
            { title: "Plugin System", href: "/core-concepts/plugins", icon: Box },
            { title: "Logging & Sessions", href: "/core-concepts/logging", icon: Terminal },
            { title: "Trust", href: "/core-concepts/trust", icon: Shield },
        ],
    },
    {
        title: "Useful Tools",
        items: [
            { title: "Shell", href: "/useful-tools/shell", icon: Terminal },
            { title: "Diff Writer", href: "/useful-tools/diff-writer", icon: PenTool },
            { title: "Memory", href: "/useful-tools/memory", icon: Cpu },
            { title: "Todo List", href: "/useful-tools/todo-list", icon: Layout },
            { title: "WebFetch", href: "/useful-tools/webfetch", icon: Globe },
            { title: "Browser", href: "/useful-tools/browser", icon: Globe },
            { title: "Outlook", href: "/useful-tools/outlook", icon: Mail },
            { title: "Calendar", href: "/useful-tools/calendar", icon: Layout },
        ],
    },
    {
        title: "Integrations",
        items: [
            { title: "Microsoft Integration", href: "/integrations/microsoft", icon: Mail },
            { title: "Google Integration", href: "/integrations/google", icon: Globe },
        ],
    },
    {
        title: "TUI",
        items: [
            { title: "Components", href: "/tui/components", icon: Layout },
            { title: "Input", href: "/tui/input", icon: Terminal },
        ],
    },
    {
        title: "Debug",
        items: [
            { title: "Interactive Debugging", href: "/debug/interactive", icon: Bug },
            { title: "@xray Decorator", href: "/debug/xray", icon: Zap },
            { title: "Logging", href: "/debug/logging", icon: Terminal },
            { title: "Browser Screenshots", href: "/debug/screenshots", icon: Globe },
        ],
    },
    {
        title: "Network",
        items: [
            { title: "Trust Parameter", href: "/network/trust", icon: Shield },
            { title: "Relay & Connect", href: "/network/relay-connect", icon: LinkIcon },
            { title: "CLI Reference", href: "/network/cli", icon: Terminal },
            { title: "Threat Model", href: "/network/threat-model", icon: Shield },
        ],
    },
    {
        title: "Examples",
        items: [
            { title: "Calculator", href: "/examples/calculator", icon: Box },
            { title: "Browser Automation", href: "/examples/browser-automation", icon: Globe },
            { title: "Web Research", href: "/examples/web-research", icon: Globe },
        ],
    },
    {
        title: "Connect",
        items: [
            { title: "Links", href: "/connect/links", icon: LinkIcon },
        ],
    },
]
