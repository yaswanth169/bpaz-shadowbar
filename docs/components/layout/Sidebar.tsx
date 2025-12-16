"use client"

import * as React from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { Search, Copy, Bot } from "lucide-react"
import { cn } from "@/lib/utils"
import { navItems } from "@/lib/navigation"
import { SearchDialog } from "@/components/ui/SearchDialog"

export function Sidebar() {
    const pathname = usePathname()
    const [open, setOpen] = React.useState(false)

    React.useEffect(() => {
        const down = (e: KeyboardEvent) => {
            if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
                e.preventDefault()
                setOpen((open) => !open)
            }
        }
        document.addEventListener("keydown", down)
        return () => document.removeEventListener("keydown", down)
    }, [])

    return (
        <>
            <aside className="fixed left-0 top-0 z-40 h-screen w-[280px] border-r border-white/5 bg-[#0B0E14] text-white">
                <div className="flex h-full flex-col">
                    {/* Header */}
                    <div className="flex h-16 items-center border-b border-white/5 px-6">
                        <Link href="/" className="flex items-center gap-2 font-bold text-xl tracking-tight hover:opacity-80 transition-opacity">
                            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-purple-500 to-pink-500">
                                <Bot className="h-5 w-5 text-white" />
                            </div>
                            ShadowBar
                        </Link>
                    </div>

                    {/* Search & Actions */}
                    <div className="p-4 space-y-4">
                        <button
                            onClick={() => setOpen(true)}
                            className="flex w-full items-center gap-2 rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-sm text-gray-400 hover:border-white/20 hover:text-white transition-colors"
                        >
                            <Search className="h-4 w-4" />
                            <span>Search docs...</span>
                            <kbd className="ml-auto text-xs bg-white/10 px-1.5 rounded">⌘K</kbd>
                        </button>

                        <button className="group relative flex w-full items-center justify-center gap-2 rounded-lg bg-gradient-to-r from-purple-500/10 to-pink-500/10 border border-purple-500/20 px-3 py-2 text-sm font-medium text-purple-400 hover:text-white hover:border-purple-500/50 transition-all overflow-hidden">
                            <div className="absolute inset-0 bg-gradient-to-r from-purple-500/20 to-pink-500/20 opacity-0 group-hover:opacity-100 transition-opacity" />
                            <Copy className="h-4 w-4 relative z-10" />
                            <span className="relative z-10">Copy All Docs</span>
                        </button>
                    </div>

                    {/* Navigation */}
                    <div className="flex-1 overflow-y-auto px-4 py-2 scrollbar-thin scrollbar-thumb-white/10 scrollbar-track-transparent">
                        {navItems.map((section, i) => (
                            <div key={i} className="mb-8">
                                <h4 className="mb-2 px-2 text-xs font-semibold uppercase tracking-wider text-gray-500">
                                    {section.title}
                                </h4>
                                <div className="space-y-1">
                                    {section.items.map((item) => {
                                        const isActive = pathname === item.href
                                        return (
                                            <Link
                                                key={item.href}
                                                href={item.href}
                                                className={cn(
                                                    "group flex items-center gap-3 rounded-lg px-2 py-1.5 text-sm transition-all",
                                                    isActive
                                                        ? "bg-gradient-to-r from-purple-500/10 to-transparent text-white border-l-2 border-purple-500"
                                                        : "text-gray-400 hover:bg-white/5 hover:text-white border-l-2 border-transparent"
                                                )}
                                            >
                                                <item.icon className={cn("h-4 w-4", isActive ? "text-purple-400" : "text-gray-500 group-hover:text-gray-300")} />
                                                {item.title}
                                            </Link>
                                        )
                                    })}
                                </div>
                            </div>
                        ))}
                    </div>

                    {/* Footer */}
                    <div className="border-t border-white/5 p-4">
                        <div className="flex items-center justify-between text-xs text-gray-500">
                            <span>v1.0.0</span>
                            <div className="flex flex-col items-end gap-0.5">
                                <div className="flex items-center gap-2">
                                    <div className="h-2 w-2 rounded-full bg-green-500" />
                                    <span>Barclays Internal</span>
                                </div>
                                <span className="text-[10px] text-gray-600">
                                    Built by Platform Engineering · Team BPAZ
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </aside>
            <SearchDialog open={open} onOpenChange={setOpen} />
        </>
    )
}
