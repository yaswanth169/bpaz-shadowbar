"use client"

import { cn } from "@/lib/utils"

interface StepProps {
    number: number
    title: string
    children: React.ReactNode
    isLast?: boolean
}

export function Step({ number, title, children, isLast }: StepProps) {
    return (
        <div className="relative pl-12 pb-12">
            {/* Line */}
            {!isLast && (
                <div className="absolute left-[19px] top-12 bottom-0 w-0.5 bg-gradient-to-b from-purple-500/50 to-transparent" />
            )}

            {/* Badge */}
            <div className="absolute left-0 top-0 flex h-10 w-10 items-center justify-center rounded-full border border-purple-500/30 bg-purple-500/10 text-lg font-bold text-purple-400 shadow-[0_0_15px_rgba(168,85,247,0.2)]">
                {number}
            </div>

            {/* Content */}
            <div>
                <h3 className="mb-4 text-xl font-bold text-white">{title}</h3>
                <div className="text-gray-400">
                    {children}
                </div>
            </div>
        </div>
    )
}
