"use client"

import * as React from "react"
import { useRouter } from "next/navigation"
import { Search, X, ArrowRight, FileText, Hash } from "lucide-react"
import { navItems } from "@/lib/navigation"
import { cn } from "@/lib/utils"

interface SearchDialogProps {
    open: boolean
    onOpenChange: (open: boolean) => void
}

export function SearchDialog({ open, onOpenChange }: SearchDialogProps) {
    const router = useRouter()
    const [query, setQuery] = React.useState("")
    const [selectedIndex, setSelectedIndex] = React.useState(0)
    const inputRef = React.useRef<HTMLInputElement>(null)

    // Flatten items for search
    const allItems = React.useMemo(() => {
        return navItems.flatMap((section) =>
            section.items.map((item) => ({
                ...item,
                category: section.title,
            }))
        )
    }, [])

    // Filter items
    const filteredItems = React.useMemo(() => {
        if (!query) return []
        return allItems.filter((item) =>
            item.title.toLowerCase().includes(query.toLowerCase()) ||
            item.category.toLowerCase().includes(query.toLowerCase())
        )
    }, [query, allItems])

    // Reset selection when query changes
    React.useEffect(() => {
        setSelectedIndex(0)
    }, [query])

    // Focus input when opened
    React.useEffect(() => {
        if (open) {
            setTimeout(() => inputRef.current?.focus(), 10)
        }
    }, [open])

    // Handle keyboard navigation
    React.useEffect(() => {
        const handleKeyDown = (e: KeyboardEvent) => {
            if (!open) return

            if (e.key === "ArrowDown") {
                e.preventDefault()
                setSelectedIndex((prev) => Math.min(prev + 1, filteredItems.length - 1))
            } else if (e.key === "ArrowUp") {
                e.preventDefault()
                setSelectedIndex((prev) => Math.max(prev - 1, 0))
            } else if (e.key === "Enter") {
                e.preventDefault()
                const item = filteredItems[selectedIndex]
                if (item) {
                    router.push(item.href)
                    onOpenChange(false)
                }
            } else if (e.key === "Escape") {
                onOpenChange(false)
            }
        }

        window.addEventListener("keydown", handleKeyDown)
        return () => window.removeEventListener("keydown", handleKeyDown)
    }, [open, filteredItems, selectedIndex, router, onOpenChange])

    if (!open) return null

    return (
        <div className="fixed inset-0 z-50 flex items-start justify-center bg-black/80 backdrop-blur-sm p-4 pt-[15vh]">
            <div className="w-full max-w-lg overflow-hidden rounded-xl border border-white/10 bg-[#0B0E14] shadow-2xl animate-in fade-in zoom-in-95 duration-200">
                <div className="flex items-center border-b border-white/5 px-4 py-3">
                    <Search className="mr-3 h-5 w-5 text-gray-400" />
                    <input
                        ref={inputRef}
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        placeholder="Search documentation..."
                        className="flex-1 bg-transparent text-sm text-white placeholder:text-gray-500 focus:outline-none"
                    />
                    <button
                        onClick={() => onOpenChange(false)}
                        className="rounded p-1 hover:bg-white/5 text-gray-400 hover:text-white"
                    >
                        <X className="h-4 w-4" />
                    </button>
                </div>

                <div className="max-h-[60vh] overflow-y-auto p-2">
                    {filteredItems.length === 0 ? (
                        <div className="py-10 text-center text-sm text-gray-500">
                            {query ? "No results found." : "Type to search..."}
                        </div>
                    ) : (
                        <div className="space-y-1">
                            {filteredItems.map((item, index) => (
                                <button
                                    key={item.href}
                                    onClick={() => {
                                        router.push(item.href)
                                        onOpenChange(false)
                                    }}
                                    className={cn(
                                        "flex w-full items-center gap-3 rounded-lg px-3 py-2 text-left text-sm transition-colors",
                                        index === selectedIndex
                                            ? "bg-purple-500/10 text-purple-400"
                                            : "text-gray-300 hover:bg-white/5 hover:text-white"
                                    )}
                                >
                                    <div className={cn(
                                        "flex h-8 w-8 items-center justify-center rounded-md border border-white/5 bg-white/5",
                                        index === selectedIndex && "border-purple-500/20 bg-purple-500/10"
                                    )}>
                                        <item.icon className="h-4 w-4" />
                                    </div>
                                    <div className="flex-1">
                                        <div className="font-medium">{item.title}</div>
                                        <div className="text-xs text-gray-500">{item.category}</div>
                                    </div>
                                    {index === selectedIndex && <ArrowRight className="h-4 w-4 opacity-50" />}
                                </button>
                            ))}
                        </div>
                    )}
                </div>

                <div className="border-t border-white/5 bg-white/5 px-4 py-2 text-xs text-gray-500 flex justify-between">
                    <span>Select <kbd className="font-sans bg-white/10 px-1 rounded">↵</kbd></span>
                    <span>Navigate <kbd className="font-sans bg-white/10 px-1 rounded">↑↓</kbd></span>
                    <span>Close <kbd className="font-sans bg-white/10 px-1 rounded">esc</kbd></span>
                </div>
            </div>
        </div>
    )
}
