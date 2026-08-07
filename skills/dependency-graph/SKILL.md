---
name: dependency-graph
description: Build evidence-backed Unity dependency graphs across serialized GUIDs, scenes, prefabs, ScriptableObjects, materials, shaders, assemblies and optional code heuristics. Use for reverse-dependency queries, circular dependencies, missing references, architecture boundaries, likely-unused asset candidates, and "what breaks if I change this" analysis.
---
# Unity Dependency Graph

Build the graph before risky refactors, migrations or asset cleanup.

Run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/dependency-graph/scripts/scan_dependencies.py <project-root> --json`.
For reverse impact analysis add `--target Assets/Path/Thing.asset`. Optional outputs are `--write-json` and `--write-dot`; add `--code-heuristics` only when weak namespace-import signals help triage.

Graph layers include asset GUID ownership, serialized GUID edges, nested prefab/ScriptableObject links represented by serialization, explicit `.asmdef` references and cycles, script-to-assembly membership, enabled build-scene/runtime roots, Resources/StreamingAssets/Addressables configuration roots, and optional C# namespace-import heuristics.

Read `resources/evidence-model.md` before interpreting cleanup candidates. Always distinguish **authoritative**, **inferred**, and **heuristic** relationships. `unusedCandidates` are inspection candidates only and are never deletion authority.

Report direct dependents, transitive blast radius, cycles, missing GUIDs, fragile serialization edges, verification targets, and recommended change order. Never claim semantic C# dependencies from text or namespace scanning alone.
