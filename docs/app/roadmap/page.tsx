"use client";

import React from "react";
import { Rocket, Shield, Brain, Boxes } from "lucide-react";

type Category = "Core" | "Trust" | "AI" | "Platform";

interface RoadmapItem {
  id: string;
  title: string;
  description: string;
  category: Category;
  when: string;
  progress: number; // 0–100
}

const items: RoadmapItem[] = [
  // Core
  {
    id: "core-launch",
    title: "ShadowBar v1.0.0 Launch",
    description: "Anthropic-only agent framework with tools, plugins, and docs for Barclays.",
    category: "Core",
    when: "Q4 2025",
    progress: 100,
  },
  {
    id: "core-browser",
    title: "Browser Tool",
    description: "Stateful browser automation via the Browser tool wrapping Playwright.",
    category: "Core",
    when: "Q4 2025",
    progress: 100,
  },
  {
    id: "core-network",
    title: "Relay Server & connect()",
    description: "Serve agents over WebSockets and call them from other processes and machines.",
    category: "Core",
    when: "Q1 2026",
    progress: 40,
  },
  // Trust
  {
    id: "trust-layer",
    title: "Trust Layer (Host Allow-list)",
    description: "Restrict outbound network access using the Trust parameter.",
    category: "Trust",
    when: "Q4 2025",
    progress: 100,
  },
  {
    id: "trust-audit",
    title: "Audit Logs & Session Exports",
    description: "Structured logs of prompts, tools, and network calls for review.",
    category: "Trust",
    when: "Q2 2026",
    progress: 20,
  },
  // AI
  {
    id: "ai-anthropic",
    title: "Anthropic Claude 4.5 Integration",
    description: "First-class support for claude-sonnet-4-5 and related models.",
    category: "AI",
    when: "Q4 2025",
    progress: 100,
  },
  {
    id: "ai-eval",
    title: "Evaluation Patterns",
    description: "Helpers and examples for testing agents end to end in tested-files/.",
    category: "AI",
    when: "Q2 2026",
    progress: 10,
  },
  // Platform
  {
    id: "platform-templates",
    title: "Template & Example Library",
    description: "Curated sb create templates and docs examples for common Barclays use cases.",
    category: "Platform",
    when: "Q2–Q3 2026",
    progress: 5,
  },
  {
    id: "platform-tooling",
    title: "IDE & Observability Integration",
    description: "Quality-of-life tooling: editor helpers and hooks into Barclays logging/metrics.",
    category: "Platform",
    when: "2026+",
    progress: 0,
  },
];

export default function RoadmapPage() {
  const completed = items.filter((i) => i.progress === 100).length;
  const inProgress = items.filter((i) => i.progress > 0 && i.progress < 100).length;
  const planned = items.filter((i) => i.progress === 0).length;

  const byCategory = items.reduce<Record<Category, RoadmapItem[]>>(
    (acc, item) => {
      acc[item.category].push(item);
      return acc;
    },
    { Core: [], Trust: [], AI: [], Platform: [] }
  );

  return (
    <div className="space-y-10">
      {/* Header */}
      <section className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-to-br from-purple-500 to-pink-500 shadow-lg">
            <Rocket className="h-5 w-5 text-white" />
          </div>
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Roadmap</h1>
            <p className="text-sm text-gray-400">
              Track ShadowBar&apos;s journey from the v1.0.0 internal launch to future platform features.
            </p>
          </div>
        </div>
        <span className="inline-flex items-center gap-2 rounded-full border border-emerald-500/40 bg-emerald-500/10 px-3 py-1 text-xs font-semibold text-emerald-300">
          v1.0.0
          <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
          Barclays Internal
        </span>
      </section>

      {/* Core Features */}
      <section className="mt-6 space-y-4">
        <div className="flex items-center gap-2 text-sm font-semibold text-gray-200">
          <Rocket className="h-4 w-4 text-purple-400" />
          <span>Core Features</span>
        </div>
        {byCategory.Core.map((item) => (
          <RoadmapCard key={item.id} item={item} />
        ))}
      </section>

      {/* Trust Features */}
      <section className="mt-10 space-y-4">
        <div className="flex items-center gap-2 text-sm font-semibold text-gray-200">
          <Shield className="h-4 w-4 text-purple-400" />
          <span>Trust Features</span>
        </div>
        {byCategory.Trust.map((item) => (
          <RoadmapCard key={item.id} item={item} />
        ))}
      </section>

      {/* AI Features */}
      <section className="mt-10 space-y-4">
        <div className="flex items-center gap-2 text-sm font-semibold text-gray-200">
          <Brain className="h-4 w-4 text-purple-400" />
          <span>AI Features</span>
        </div>
        {byCategory.AI.map((item) => (
          <RoadmapCard key={item.id} item={item} />
        ))}
      </section>

      {/* Platform Features */}
      <section className="mt-10 space-y-4">
        <div className="flex items-center gap-2 text-sm font-semibold text-gray-200">
          <Boxes className="h-4 w-4 text-purple-400" />
          <span>Platform Features</span>
        </div>
        {byCategory.Platform.map((item) => (
          <RoadmapCard key={item.id} item={item} />
        ))}
      </section>

      {/* Summary footer */}
      <section className="mt-4 flex flex-wrap items-center gap-6 rounded-2xl border border-white/5 bg-white/5 px-4 py-3 text-xs text-gray-300">
        <div className="flex items-baseline gap-2">
          <span className="text-lg font-semibold text-emerald-300">{completed}</span>
          <span>Completed</span>
        </div>
        <div className="flex items-baseline gap-2">
          <span className="text-lg font-semibold text-amber-300">{inProgress}</span>
          <span>In Progress</span>
        </div>
        <div className="flex items-baseline gap-2">
          <span className="text-lg font-semibold text-gray-300">{planned}</span>
          <span>Planned</span>
        </div>
      </section>
    </div>
  );
}

function RoadmapCard({ item }: { item: RoadmapItem }) {
  const statusLabel =
    item.progress === 100 ? "Complete" : item.progress === 0 ? "Planned" : "In Progress";

  return (
    <article className="relative overflow-hidden rounded-2xl border border-white/10 bg-[#0B0E14] px-5 py-4 shadow-[0_0_0_1px_rgba(255,255,255,0.02)]">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-sm font-semibold text-gray-100">{item.title}</h2>
          <p className="mt-1 text-xs text-gray-400">{item.description}</p>
        </div>
        <div className="flex flex-col items-end gap-1 text-right text-[11px]">
          <span className="text-gray-400">{item.when}</span>
          <span
            className={
              statusLabel === "Complete"
                ? "font-semibold text-emerald-300"
                : statusLabel === "In Progress"
                ? "font-semibold text-amber-300"
                : "font-semibold text-gray-300"
            }
          >
            {statusLabel}
          </span>
        </div>
      </div>
      <div className="mt-3 space-y-1">
        <span className="text-[10px] uppercase tracking-wide text-gray-500">Progress</span>
        <div className="h-1.5 w-full rounded-full bg-white/5">
          <div
            className="h-1.5 rounded-full bg-emerald-400"
            style={{ width: `${item.progress}%` }}
          />
        </div>
      </div>
    </article>
  );
}


