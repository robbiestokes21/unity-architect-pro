# Changelog

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
