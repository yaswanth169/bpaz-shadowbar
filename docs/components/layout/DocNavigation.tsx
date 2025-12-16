"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { ArrowLeft, ArrowRight } from "lucide-react"
import { navItems } from "@/lib/navigation"

export function DocNavigation() {
    const pathname = usePathname()

    // Flatten the navigation items to find prev/next
    const flatItems = navItems.flatMap((section) => section.items)
    const currentIndex = flatItems.findIndex((item) => item.href === pathname)

    const prevItem = currentIndex > 0 ? flatItems[currentIndex - 1] : null
    const nextItem = currentIndex < flatItems.length - 1 ? flatItems[currentIndex + 1] : null

    return (
        <div className="mt-16 flex items-center justify-between border-t border-white/10 pt-8">
            {prevItem ? (
                <Link
                    href={prevItem.href}
                    className="group flex flex-col gap-1 rounded-lg border border-white/5 bg-white/5 px-6 py-4 transition-colors hover:border-white/10 hover:bg-white/10"
                >
                    <span className="flex items-center gap-2 text-xs text-gray-400 group-hover:text-gray-300">
                        <ArrowLeft className="h-3 w-3" /> Previous
                    </span>
                    <span className="font-medium text-purple-400 group-hover:text-purple-300">
                        {prevItem.title}
                    </span>
                </Link>
            ) : (
                <div />
            )}

            {nextItem ? (
                <Link
                    href={nextItem.href}
                    className="group flex flex-col items-end gap-1 rounded-lg border border-white/5 bg-white/5 px-6 py-4 transition-colors hover:border-white/10 hover:bg-white/10"
                >
                    <span className="flex items-center gap-2 text-xs text-gray-400 group-hover:text-gray-300">
                        Next <ArrowRight className="h-3 w-3" />
                    </span>
                    <span className="font-medium text-purple-400 group-hover:text-purple-300">
                        {nextItem.title}
                    </span>
                </Link>
            ) : (
                <div />
            )}
        </div>
    )
}
