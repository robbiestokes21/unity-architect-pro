---
name: "project-intelligence"
description: "Build and refresh a durable technical profile of a Unity project before substantial implementation. Detect Unity version, installed packages, render/input/network stacks, target settings, asmdefs, scenes, tests, architecture signals, build targets and project conventions. Use at the start of unfamiliar or large Unity work and whenever project structure materially changes."
---

# Unity Project Intelligence

Create evidence before assumptions. The goal is a small, durable project model that other skills can consume.

## Discover
Read, when present:
- `ProjectSettings/ProjectVersion.txt`
- `Packages/manifest.json` and `Packages/packages-lock.json`
- `ProjectSettings/ProjectSettings.asset`, `EditorBuildSettings.asset`, `GraphicsSettings.asset`, `QualitySettings.asset`, `TagManager.asset`
- all relevant `.asmdef` / `.asmref` files
- `.editorconfig`, analyzer settings and repository instructions
- representative runtime, Editor and test folders

Run `${CLAUDE_SKILL_DIR}/scripts/index_unity_project.py <project-root>` when shell execution is available. For substantial projects or risky changes also generate `.claude/unity/generated/project-graph.json` with the `dependency-graph` skill. Treat generated output as an index, not a substitute for reading relevant code.

## Produce/refresh project memory
With permission to modify the repository, maintain `.claude/unity/`:
- `project-profile.md` — versions, packages, pipelines, platforms, tests, networking and high-level systems
- `architecture.md` — current system boundaries and dependencies
- `networking.md` — only when networking exists
- `conventions.md` — namespaces, naming, serialization and code patterns actually observed
- `performance-budgets.md` — only when budgets are known or established
- `decisions/` — Architecture Decision Records for durable choices
- `generated/project-index.json` — generated machine-readable index; safe to refresh

Do not overwrite hand-written architectural decisions with guesses. Mark inferred facts clearly.

## Stack detection
Detect independently:
- render pipeline: Built-in / URP / HDRP / custom
- input: legacy / Input System / both
- async: coroutines / Tasks / UniTask / custom
- assets: Resources / Addressables / AssetBundles / custom
- gameplay architecture: GameObject/OOP / DOTS / hybrid
- multiplayer layers: netcode, transport, session/backend, hosting, auth
- testing: Unity Test Framework assemblies, custom runners, CI test commands

## Change impact
Before a large edit, identify:
1. assemblies affected
2. serialized assets/scenes/prefabs potentially affected
3. runtime/editor boundary
4. tests that should prove the change
5. build targets at risk
6. multiplayer compatibility/authority impact

## Rules
- Never infer package API version from memory when lockfile evidence exists.
- Never rewrite `.claude/unity/*` merely to make it prettier; preserve useful project history.
- Prefer incremental refreshes after the first index.
- If generated index and source files disagree, source files win.

## Memory integration
Before substantial work, query `project-memory` for architecture/networking/incident history relevant to the affected systems, but re-verify volatile facts against current files. After an index refresh, do not bulk-copy the entire index into memory; persist only durable facts that materially improve future decisions.
