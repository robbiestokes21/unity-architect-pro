---
name: impact-analysis
description: Determine what can break before changing a Unity script, assembly, scene, prefab, ScriptableObject, material, shader, Addressable asset or GUID-linked resource. Use for risky refactors, package migrations, renames, deletions, API changes, serialized-field changes, or any "what depends on this?" question.
---
# Unity Change Impact Analysis

Run project intelligence, then build the dependency graph with `--target`. Separate authoritative serialized/asmdef evidence from inferred Unity conventions and heuristic runtime/code signals. Inspect all direct dependents before changing serialization, APIs, GUIDs or assembly boundaries, then map the transitive blast radius and verification order.

Treat serialized field removal/rename, serialized type changes, script moves across assemblies/namespaces, `.meta` GUID changes, nested prefab changes and widely shared ScriptableObject schema changes as high risk.

Output the target, change type, direct dependents, transitive blast radius, evidence confidence, serialization/GUID hazards, assembly/API consumers, tests/builds/network topologies at risk, and migration order. Never say an asset is safe to delete solely because static reachability does not find it.
