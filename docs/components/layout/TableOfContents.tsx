"use client"

import { cn } from "@/lib/utils"

interface ToCItem {
    title: string
    href: string
    level: number
}

const items: ToCItem[] = [
    { title: "Introduction", href: "#introduction", level: 1 },
    { title: "Key Features", href: "#key-features", level: 2 },
    { title: "Installation", href: "#installation", level: 2 },
    { title: "Quick Start", href: "#quick-start", level: 2 },
]

export function TableOfContents() {
    return (
        <div className="hidden xl:block fixed right-0 top-0 h-screen w-64 border-l border-white/5 p-6">
            <h5 className="mb-4 text-sm font-semibold text-gray-400 uppercase tracking-wider">
                On This Page
            </h5>
            <ul className="space-y-3 text-sm">
                {items.map((item) => (
                    <li key={item.href} style={{ paddingLeft: (item.level - 1) * 12 }}>
                        <a
                            href={item.href}
                            className="text-gray-500 hover:text-white transition-colors block"
                        >
                            {item.title}
                        </a>
                    </li>
                ))}
            </ul>
        </div>
    )
}
