# Changelog

## 2.0.0-alpha.10.1 — Unity MCP integration

- Added plugin/project and marketplace-ready loopback HTTP configuration for the optional CoplayDev MCP for Unity bridge, plus VS Code and stdio examples.
- Added the `mcp-unity` skill with resource-first discovery, explicit multi-instance selection, serialized mutation, compilation/Console checks and evidence-based verification.
- Added installation, approval, troubleshooting and security guidance; the external Unity package remains pinned, reviewed and opt-in rather than vendored or silently installed.
- Added MCP configuration validation and routed master/live-editor behavior through the shared connection contract before Phase 11.

## 2.0.0-alpha.10 — Phases 9–10: Visual QA and Performance AI

- Added gameplay-checkpoint camera capture, reviewed readable baselines, ignore masks, configurable pixel tolerances, current images, heatmaps and structured visual verdicts.
- Added explicit UI clipping/overlap and missing material/shader audit hooks without optional UI package dependencies.
- Added representative warmup/measurement windows and p50/p95/p99 budgets for frame time, CPU, GPU, GC, memory and project-defined metrics.
- Added baseline regression comparison, schemas, fixtures, validation, user instructions and independent visual/performance result markers.
- Published Phase 11 Security AI and Phases 12–18 follow-on scope in the roadmap.

## 2.0.0-alpha.9 — Phase 8: Gameplay Testing

- Added versioned, deterministic gameplay scenarios with project-owned action/assertion adapters and a package-neutral transform smoke adapter.
- Added bounded execution, seeded runs, per-step state evidence, JSON results, failure screenshots and guaranteed cleanup.
- Added an Editor validator, schemas, example/fixture, gameplay QA agent, static tests and Phase 7 marker interoperability.

## 2.0.0-alpha.8 — Phase 7: Multiplayer Laboratory

- Added scenario-driven dedicated server/client orchestration with dependency readiness, late join, expected stop and restart/reconnect actions.
- Added reviewed external fault-controller hooks with mandatory teardown support, argv-only execution and bounded process artifacts.
- Added provider/project adapter rendering, scenario/result schemas, structured generation/timing/failure evidence and a specialist lab operator.
- Added a real multi-process fixture covering dedicated-server readiness, delayed client join and client restart/reconnect.

## 2.0.0-alpha.7 — Phase 6: Runtime Debugger

- Expanded runtime diagnostics from a periodic transform log into structured object, physics, Animator, FSM/AI, network ownership, operation and runtime-metric snapshots.
- Added package-neutral `IRuntimeStateDiagnostics` and `IRuntimeNetworkDiagnostics` adapters plus a bounded task/coroutine/job/request lifecycle registry.
- Added a Play Mode selected-object debugger window, JSON/JSONL evidence, safety/limitations contract, specialist agent, fixtures and validation.
- Fixed CI frontmatter validation to accept conservative valid YAML plain scalars such as `model: inherit`.

## 2.0.0-alpha.6 — Phase 5: Live Unity Inspector

- Added full loaded-scene hierarchy and arbitrary visible `SerializedProperty` inspection with bounded JSON evidence output.
- Added prefab source/override analysis plus cameras, tags/layers/sorting layers, Input System, Animator state machines, NavMesh/navigation, lighting, render-pipeline, physics, volumes and project-settings coverage.
- Added optimistic, Undo-backed single-property mutation with stable global IDs, expected-value checks, an explicit safe-type allowlist, project-settings opt-in, save and read-back verification.
- Added the `live-inspector` skill, inspector specialist agent, capability contract, fixtures, static validation, release metadata and documentation.

## 2.0.0-alpha.5 — Phase 4: Persistent Project Memory

- Rebuilt project memory as a versioned SQLite engineering knowledge store with facts, ADR decisions, incidents/root causes, feature history, relationships and performance samples.
- Added confidence, TTL/expiry, stale/superseded state, full-text search, review reports and a credential-pattern safety guard.
- Added `memory-review`, durable-memory policy, and a `project-memory-curator` specialist agent.
- Added automatic write-back guidance after validated work and tests for search, incidents, decisions, performance history, exports and secret rejection.

## 2.0.0-alpha.4 — Phase 3: Autonomous Project Intelligence

- Rebuilt dependency scanning as an evidence-backed project graph engine.
- Added reverse/transitive impact analysis, `.asmdef` cycles, serialized GUID integrity, JSON/DOT export, conservative unused-asset candidates, and optional code heuristics.
- Added `impact-analysis`, evidence-model documentation, a project-intelligence analyst agent, and automated fixture tests.

## 2.0.0-alpha.3

- Added project-memory SQLite helper and durable engineering-memory rules.
- Added dependency/impact graph, runtime debugger, gameplay tester and visual AI skills.
- Added performance/security engineering, build-farm and release-manager layers.
- Added documentation engine, safe refactoring, game design, world building and project-learning skills.
- Added GitHub Actions validation/release packaging, issue/PR templates and contributor/security documentation.
- Removed generated Python cache files from distributable packages.

- Added live Editor intelligence and semantic capability handshake.
- Added hierarchy/serialized-state inspection, Console/log diagnostics and screenshot-based visual verification.
- Added profiler-capture workflow with baseline/budget comparison.
- Added provider-neutral multi-client/server process harness and stable result schema.
- Added gameplay AI, input, asset integrity, package management, migration and observability skills.
- Added live-editor, visual-QA, profiler, asset-integrity and release specialist agents.
- Added filesystem asset integrity scanner, log parser and extended project facts scripts.
- Extended master routing, testing and self-review gates to consume runtime evidence.

## 2.0.0-alpha.1

- Added `project-intelligence` with a local Unity project indexer.
- Added durable `.claude/unity/` architecture-memory conventions and ADR support.
- Added `unity-doctor` whole-project health audits.
- Added `self-review` Definition-of-Done completion gate.
- Added `build-doctor`, `addressables`, `ui-engineer`, `dots`, `shaders`, `save-system`, and `release-engineering` skills.
- Expanded multiplayer into specialist security, performance, prediction, dedicated-server and topology/fault-testing agents.
- Added network budget and adverse-condition test-matrix resources.
- Updated master routing and performance/testing workflows to use the new specialist system.
