import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Next.js legt sonst beim Start eine web/AGENTS.md an; Regeln für Agenten stehen nur in der AGENTS.md im Repo-Root.
  agentRules: false,
  cacheComponents: true,
  partialPrefetching: true,
};

export default nextConfig;
