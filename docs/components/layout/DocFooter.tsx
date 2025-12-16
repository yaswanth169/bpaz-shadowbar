import { Github } from "lucide-react"
import Link from "next/link"

export function DocFooter() {
    return (
        <footer className="mt-24 border-t border-white/10 py-12">
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                    <div className="h-6 w-6 rounded-full bg-gradient-to-br from-purple-500 to-pink-500" />
                    <span className="font-bold text-gray-200">ShadowBar</span>
                    <span className="text-sm text-gray-500">© 2025 Barclays Internal</span>
                </div>
                <div className="flex gap-4">
                    <Link
                        href="https://gitlab.barclays.internal/shadowbar/shadowbar"
                        className="text-gray-500 hover:text-white transition-colors"
                    >
                        <Github className="h-5 w-5" />
                    </Link>
                </div>
            </div>
        </footer>
    )
}
