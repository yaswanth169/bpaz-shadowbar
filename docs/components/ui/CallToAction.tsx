import Link from "next/link"

export function CallToAction() {
    return (
        <div className="mt-24 flex flex-col items-center justify-center text-center">
            <h3 className="text-2xl font-bold text-white">Ready to build?</h3>
            <div className="mt-8 flex gap-4">
                <Link
                    href="/getting-started/quick-start"
                    className="rounded-full bg-purple-600 px-6 py-2.5 font-semibold text-white transition-colors hover:bg-purple-500"
                >
                    Get Started
                </Link>
                <Link
                    href="https://gitlab.barclays.internal/shadowbar/shadowbar"
                    className="rounded-full border border-white/10 bg-white/5 px-6 py-2.5 font-semibold text-white transition-colors hover:bg-white/10"
                >
                    View on GitLab
                </Link>
            </div>
        </div>
    )
}
