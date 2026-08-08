---
name: "mcp-unity"
description: "Connect Unity Architect Pro to a live Unity Editor through MCP, discover actual resources/tools, select the correct Editor instance, perform serialized safe operations, and verify compilation, Console, scene, test, screenshot, profiler, and build evidence."
---

# Unity MCP Integration

Use this skill when a task requires the actual Unity Editor through Model Context Protocol. The recommended configuration targets the optional CoplayDev MCP for Unity bridge, but behavior is capability-based so provider names are never treated as guaranteed tool names.

## Required handshake

1. Confirm the MCP server is connected and enumerate its current tools/resources.
2. Read editor state and project identity, including Unity version, compilation/domain-reload status, Play Mode, active scene, and blocking reasons when exposed.
3. If more than one Editor is available, list instances and select the intended project explicitly.
4. Map the requested work to observed capabilities. If a capability is absent, use a reviewed Editor script, batchmode/CLI, or mark it unverified.

## Safe operation loop

For reads, prefer resources and bounded/paginated queries. For mutations, capture pre-state, confirm the Editor is ready, perform one logical state-changing operation, wait for completion or reload, read state back, inspect Console errors, and run the smallest relevant verification. Batch independent reads; do not parallelize state-changing Editor operations.

After creating or editing scripts, wait for compilation to finish before attaching components or running tests. After scene/prefab/project-setting changes, save explicitly and verify the serialized result. Runtime state is not persisted asset state. Never claim success from an accepted tool call alone.

## Routing

- hierarchy and components: `live-inspector` / `hierarchy-inspector`
- runtime object, AI, ownership and operations: `runtime-debugger`
- gameplay journeys: `gameplay-tester`
- screenshots and baselines: `visual-verification`
- profiling and budgets: `profiler-capture`
- tests: `testing`
- builds: `build-doctor` / `release-engineering`

## Setup and security

Read `../../mcp/README.md`. The committed endpoint is loopback-only HTTP. Project-scoped MCP servers require user review because MCP tools can modify project and Editor state. Do not insert secrets into `.mcp.json`, expose an unauthenticated bridge beyond localhost, assume a provider/package is installed, or bypass Unity Undo/save/compilation safeguards.

Example request: `Use mcp-unity to connect to my open Unity project, confirm the instance and clean compilation state, inspect the active scene, then run the Phase 8 gameplay scenario and collect Phase 9 visual plus Phase 10 performance evidence.`
