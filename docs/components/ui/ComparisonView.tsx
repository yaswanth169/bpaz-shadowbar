"use client"

import { cn } from "@/lib/utils"

interface ComparisonViewProps {
    leftTitle: string
    rightTitle: string
    leftContent: React.ReactNode
    rightContent: React.ReactNode
}

export function ComparisonView({ leftTitle, rightTitle, leftContent, rightContent }: ComparisonViewProps) {
    return (
        <div className="grid gap-8 md:grid-cols-2">
            {/* Left Side (ShadowBar) */}
            <div className="relative group">
                <div className="absolute -inset-0.5 rounded-xl bg-gradient-to-r from-purple-500 to-pink-500 opacity-30 blur transition duration-1000 group-hover:opacity-50" />
                <div className="relative h-full rounded-xl bg-[#0B0E14] border border-white/10 p-6">
                    <div className="mb-4 flex items-center justify-between">
                        <h3 className="font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400">
                            {leftTitle}
                        </h3>
                        <span className="text-xs text-green-400 font-mono">8 lines</span>
                    </div>
                    {leftContent}
                </div>
            </div>

            {/* Right Side (Competitor) */}
            <div className="relative h-full rounded-xl bg-[#0B0E14] border border-white/5 p-6 opacity-80">
                <div className="mb-4 flex items-center justify-between">
                    <h3 className="font-bold text-gray-400">
                        {rightTitle}
                    </h3>
                    <span className="text-xs text-gray-600 font-mono">30+ lines</span>
                </div>
                {rightContent}
            </div>
        </div>
    )
}
