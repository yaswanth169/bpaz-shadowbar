"use client"

import { Copy, Terminal } from "lucide-react"
import { cn } from "@/lib/utils"

interface TerminalBlockProps {
    command: string
    output?: string
    className?: string
}

export function TerminalBlock({ command, output, className }: TerminalBlockProps) {
    return (
        <div className={cn("overflow-hidden rounded-xl border border-white/10 bg-[#0B0E14] shadow-2xl", className)}>
            {/* Header */}
            <div className="flex items-center justify-between border-b border-white/5 bg-white/5 px-4 py-3">
                <div className="flex gap-2">
                    <div className="h-3 w-3 rounded-full bg-red-500/20" />
                    <div className="h-3 w-3 rounded-full bg-yellow-500/20" />
                    <div className="h-3 w-3 rounded-full bg-green-500/20" />
                </div>
                <div className="flex items-center gap-2 text-xs font-medium text-gray-500">
                    <Terminal className="h-3 w-3" />
                    bash
                </div>
                <Copy className="h-4 w-4 text-gray-500 hover:text-white cursor-pointer transition-colors" />
            </div>

            {/* Content */}
            <div className="p-4 font-mono text-sm">
                <div className="flex items-center gap-2">
                    <span className="text-green-500">$</span>
                    <span className="text-white">{command}</span>
                </div>
                {output && (
                    <div className="mt-2 text-gray-400 whitespace-pre-wrap">
                        {output}
                    </div>
                )}
            </div>
        </div>
    )
}
