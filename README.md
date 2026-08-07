# Unity Architect Pro for Claude Code

Unity Architect Pro is a multi-skill, multi-agent Unity engineering system for Claude Code. It is designed to behave more like a senior Unity engineering team than a single code-generation prompt: inspect the real project first, design within its architecture, operate the Editor safely, implement, review, test, profile, build, and only then declare work complete.

> Version: **2.0.0-alpha.5** — Phase 4 persistent engineering memory.


## Autonomous engineering expansion (alpha.5)

Alpha.5 includes the platform phases as first-class skills and upgrades project memory into a versioned engineering knowledge layer: durable project memory, dependency/impact graphs, runtime debugging, gameplay testing, visual AI QA, performance/security engineering, cross-platform build-farm planning, documentation generation, cross-file refactoring, game/system design, world building, project learning and release management. The repository now also includes GitHub Actions validation/release packaging, issue/PR templates, contributing/security policies, and a repository setup guide.

Useful commands:

```bash
python scripts/validate_plugin.py
python skills/project-memory/scripts/memory_db.py put-fact architecture networking-authority "server authoritative" --source .claude/unity/networking.md --confidence 1.0
python skills/dependency-graph/scripts/scan_dependencies.py /path/to/UnityProject --json
```

## Core workflow

```text
Request
  ↓
Project Intelligence
  ↓
Architecture / Documentation Research
  ↓
Implementation + Unity Editor operations
  ↓
Compilation / Diagnostics
  ↓
Specialist Review (network, DOTS, Addressables, UI, shader, save, etc.)
  ↓
Tests / Runtime Validation
  ↓
Build Validation when applicable
  ↓
Self-Review Definition of Done
```

## Skills

| Skill | Purpose |
|---|---|
| `unity` | Master router and Unity engineering rules |
| `project-intelligence` | Build/refresh a durable technical model of the Unity project |
| `unity-doctor` | Whole-project health audit with prioritized evidence-backed findings |
| `architecture` | Feature/system architecture and durable technical decisions |
| `create-script` | Production Unity C#, Editor scripts, ScriptableObjects and compatible ECS code |
| `editor-control` | Safe Unity Editor, scene, prefab, compilation and Play Mode automation |
| `code-review` | Unity-specific correctness/performance/architecture review |
| `debug-fix` | Evidence-driven debugging and regression fixing |
| `testing` | EditMode, PlayMode, player/build and multiplayer tests |
| `performance` | CPU/GPU/GC/memory/loading/network performance |
| `build-doctor` | Player and dedicated-server build diagnosis/validation |
| `docs-research` | Version-matched official Unity/provider documentation research |
| `multiplayer` | Provider-aware network architecture, implementation and review |
| `addressables` | Addressables lifetime, groups, catalogs and remote content |
| `ui-engineer` | uGUI / UI Toolkit architecture, implementation and performance |
| `dots` | Entities, Burst, Jobs, NativeContainers and hybrid ECS |
| `shaders` | Shader Graph, HLSL and URP/HDRP rendering engineering |
| `save-system` | Versioned persistence, migrations, cloud/local save safety |
| `release-engineering` | CI, artifacts, versioning, deployment and server images |
| `live-editor` | Live Unity Editor capability discovery, inspection and transactional operation |
| `hierarchy-inspector` | Scene/prefab/component/serialized-state inspection |
| `console-diagnostics` | Current-run Console, Editor/Player/server log diagnosis |
| `visual-verification` | Game View/UI/rendering screenshot verification |
| `profiler-capture` | Evidence-based CPU/GPU/GC/memory/network performance captures |
| `multiplayer-harness` | Multi-client/server process and network-fault test harnesses |
| `gameplay-ai` | NPC decision, navigation, perception and networked AI |
| `input-engineer` | Input System, rebinding, device pairing and local multiplayer |
| `asset-integrity` | GUID/meta/reference/import integrity and release preflight |
| `package-manager` | Safe Unity Package Manager dependency analysis and changes |
| `migration-engineer` | Unity/package/system migrations with checkpoints/rollback |
| `observability` | Client/server structured logs, metrics, health and readiness |
| `self-review` | Final Definition-of-Done completion gate |
| `project-memory` | Durable facts, ADR decisions, incidents, feature history, relationships and performance memory |
| `memory-review` | Audit stale/expired/low-confidence or superseded project knowledge |

## Specialist agents

The plugin contains dedicated agents for:
- Unity code review
- Unity debugging
- multiplayer architecture
- multiplayer security
- network performance and bandwidth
- prediction/reconciliation/rollback design
- dedicated-server engineering
- multiplayer topology/fault testing

## Project Intelligence and architectural memory

For larger or unfamiliar repositories, the plugin can inspect:
- `ProjectSettings/ProjectVersion.txt`
- package manifest/lockfile
- `.asmdef` / `.asmref` boundaries
- scenes and test assemblies
- render/input/Addressables/DOTS/network package hints
- project conventions and architecture

A bundled indexer is available at:

```bash
python3 skills/project-intelligence/scripts/index_unity_project.py /path/to/UnityProject
```

When appropriate, Claude can maintain project-local memory under:

```text
.claude/unity/
├── project-profile.md
├── architecture.md
├── networking.md
├── conventions.md
├── performance-budgets.md
├── decisions/
└── generated/project-index.json
```

Hand-written decisions are never supposed to be overwritten by inferred/generated facts.

## `/unity-doctor`

Use the `unity-doctor` skill to audit an existing project. It examines architecture, Unity lifecycle/serialization, CPU/GPU/GC/memory, tests, multiplayer authority/security, build health, assets/content, packages and maintainability. Findings must be tied to actual evidence rather than generic Unity advice.

Example:

```text
/unity-architect-pro:unity-doctor Audit this project and give me the 10 highest-value fixes before beta.
```

## Multiplayer engineering

Networking is modeled as separate layers:

```text
Gameplay simulation/netcode
    NGO / Netcode for Entities / Fusion / Quantum / PUN / Mirror / FishNet / custom
Transport
    Unity Transport / Photon / KCP / Telepathy / Steam Networking Sockets / custom
Sessions/backend
    Unity Multiplayer Services / Photon / Steam / EOS / PlayFab / custom
Hosting
    host-client / dedicated server / distributed authority / deterministic topology
Identity
    UGS / Steam / EOS / PlayFab / platform / custom
```

Provider guides exist for Unity networking, Photon, Mirror, FishNet, Steam/Facepunch, Epic Online Services, PlayFab and custom authoritative servers. The skill does not silently mix APIs or migrate networking providers.

Advanced multiplayer agents add:
- client/server trust-boundary and exploit review
- tick/snapshot/bandwidth/interest-management analysis
- prediction, reconciliation, interpolation, rewind and rollback architecture
- headless server allocation/readiness/shutdown/observability patterns
- production topology tests with latency, jitter, loss and disconnect scenarios

## Safe Editor automation

For scene/prefab structural edits, prefer Unity Editor APIs through the connected Unity-capable MCP/editor integration. Stateful Unity actions must run serially around compilation/domain reload. If no integration exists, generate safe temporary Editor scripts or supported CLI/batch workflows rather than pretending the Editor was modified.

## Completion gate

Meaningful implementation should end with the `self-review` skill. Applicable checks include:
- diff/scope review
- compilation and diagnostics
- Unity lifecycle/serialization review
- specialist review
- targeted tests
- Editor/runtime validation
- target build validation
- final secret/temp/generated-file check

An unperformed check is reported as **unverified**, not silently treated as passing.

## Install locally

```bash
claude --plugin-dir ./unity-architect-pro
```

Examples:

```text
/unity-architect-pro:unity Build a modular third-person inventory system.
/unity-architect-pro:multiplayer Add authoritative shooting using the stack already installed.
/unity-architect-pro:project-intelligence Index this project before we redesign combat.
/unity-architect-pro:code-review Review this branch for Unity lifecycle and multiplayer problems.
/unity-architect-pro:build-doctor Diagnose why the IL2CPP Android build fails but Editor Play Mode works.
/unity-architect-pro:self-review Verify the feature we just implemented is actually done.
```

## Validation

With a compatible Claude Code installation:

```bash
claude plugin validate ./unity-architect-pro
claude --debug --plugin-dir ./unity-architect-pro
```

## Status

This is an alpha expansion. Provider-specific APIs still require version-aware verification against the project's installed packages and official documentation. The plugin intentionally encodes that behavior rather than pretending package APIs are timeless.

## License

MIT


## Alpha 2: live engineering loop

Unity Architect Pro can now model an end-to-end evidence loop rather than stopping at source changes:

```text
Project index
  -> live Editor capability handshake
  -> hierarchy / serialized-state inspection
  -> safe mutation
  -> compilation + current-run Console check
  -> Play Mode / player behavior
  -> visual evidence when applicable
  -> profiler evidence when applicable
  -> multiplayer process harness when applicable
  -> asset/build/release preflight
  -> Definition of Done
```

The plugin deliberately uses semantic capability discovery instead of hard-coded MCP tool names, so it can adapt to Rider/Unity MCP integrations and future Editor bridges. Where a capability is missing it falls back to temporary Editor scripts, batchmode/process orchestration, or marks the check unverified.

### Included standalone helper scripts

```bash
python3 skills/console-diagnostics/scripts/parse_unity_log.py Editor.log --json
python3 skills/asset-integrity/scripts/scan_asset_integrity.py /path/to/project --json
python3 skills/project-intelligence/scripts/extended_project_facts.py /path/to/project
python3 skills/multiplayer-harness/scripts/process_harness.py --help
```

The multiplayer harness is intentionally provider-neutral: project/provider adapters supply the actual server/client launch commands and readiness signals. This prevents the skill from pretending FishNet, Mirror, Fusion, NGO, Steam, EOS or custom servers share one launch API.


## Phase 3: Autonomous Project Intelligence

Alpha 4 adds evidence-backed serialized GUID and assembly graphs, reverse/transitive impact analysis, conservative cleanup candidates, and JSON/DOT export. Use `/unity-architect-pro:impact-analysis` before high-blast-radius changes.
