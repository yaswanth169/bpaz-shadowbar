import { getDocBySlug } from "@/lib/docs"
import { MDXRemote } from "next-mdx-remote/rsc"
import { TerminalBlock } from "@/components/ui/TerminalBlock"
import { Step } from "@/components/ui/StepGuide"
import { ComparisonView } from "@/components/ui/ComparisonView"

const components = {
    TerminalBlock,
    Step,
    ComparisonView,
    h1: (props: any) => <h1 className="text-4xl font-bold tracking-tight mb-6" {...props} />,
    h2: (props: any) => <h2 className="text-2xl font-bold mt-10 mb-4 border-b border-white/10 pb-2" {...props} />,
    h3: (props: any) => <h3 className="text-xl font-bold mt-8 mb-3" {...props} />,
    p: (props: any) => <p className="leading-7 text-gray-300 mb-4" {...props} />,
    ul: (props: any) => <ul className="list-disc list-inside mb-4 space-y-2 text-gray-300" {...props} />,
    li: (props: any) => <li className="ml-4" {...props} />,
    code: (props: any) => <code className="bg-white/10 rounded px-1.5 py-0.5 text-sm font-mono text-purple-300" {...props} />,
    pre: (props: any) => (
        <div className="my-6 overflow-hidden rounded-xl border border-white/10 bg-[#0B0E14]">
            <div className="flex items-center gap-2 border-b border-white/5 bg-white/5 px-4 py-2">
                <div className="flex gap-1.5">
                    <div className="h-2.5 w-2.5 rounded-full bg-red-500/20" />
                    <div className="h-2.5 w-2.5 rounded-full bg-yellow-500/20" />
                    <div className="h-2.5 w-2.5 rounded-full bg-green-500/20" />
                </div>
            </div>
            <pre className="p-4 overflow-x-auto text-sm" {...props} />
        </div>
    ),
}

export default async function DocPage({ params }: { params: { slug: string[] } }) {
    const { slug } = await params
    try {
        const { content, meta } = getDocBySlug(slug)

        return (
            <article className="prose prose-invert max-w-none">
                <MDXRemote source={content} components={components} />
            </article>
        )
    } catch (error) {
        return (
            <div className="flex h-[50vh] flex-col items-center justify-center text-center">
                <h1 className="text-4xl font-bold text-gray-800 dark:text-gray-200">404</h1>
                <p className="mt-4 text-gray-500">Document not found.</p>
            </div>
        )
    }
}
