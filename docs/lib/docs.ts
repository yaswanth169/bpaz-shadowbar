import fs from "fs"
import path from "path"
import matter from "gray-matter"

const contentDirectory = path.join(process.cwd(), "content")

export function getAllDocs() {
    // This is a simplified version. In a real app, you'd recursively walk the directory.
    // For now, we'll just return a list of known paths or implement a walker.
    // Given the structure is simple (concepts/, cli/, etc.), we can hardcode or walk.
    return []
}

export function getDocBySlug(slug: string[]) {
    const realSlug = slug.join("/")
    const fullPath = path.join(contentDirectory, `${realSlug}.md`)

    if (!fs.existsSync(fullPath)) {
        // Try index.md if it's a directory
        const indexPath = path.join(contentDirectory, realSlug, "index.md")
        if (fs.existsSync(indexPath)) {
            const fileContents = fs.readFileSync(indexPath, "utf8")
            const { data, content } = matter(fileContents)
            return { slug: realSlug, meta: data, content }
        }
        throw new Error(`Doc not found: ${realSlug}`)
    }

    const fileContents = fs.readFileSync(fullPath, "utf8")
    const { data, content } = matter(fileContents)

    return { slug: realSlug, meta: data, content }
}
