import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Sidebar } from "@/components/layout/Sidebar";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "ShadowBar Documentation",
  description: "The Barclays Internal AI agent framework.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-[#0B0E14] text-white`}
      >
        <Sidebar />
        <main className="pl-[280px] min-h-screen">
          <div className="mx-auto max-w-5xl px-8 py-12">
            {children}
          </div>
        </main>
      </body>
    </html>
  );
}
