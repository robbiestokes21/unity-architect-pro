---
name: "hierarchy-inspector"
description: "Inspect and reason about Unity scenes, prefabs, GameObjects, components, serialized references, prefab overrides, missing scripts, and dependency wiring. Use before risky scene/prefab edits or when diagnosing broken Inspector wiring."
---
# Hierarchy and Serialized-State Inspector

Inspect before editing. Build a concise tree containing hierarchy path, active state, layer/tag when relevant, component types, important serialized references, prefab source/override status, and missing-script/null-reference findings.

## Checks
- duplicate or ambiguous object names used by automation/tests
- Missing Mono Script components
- required component dependencies
- null serialized references that are expected to be assigned
- prefab overrides that would be unintentionally lost
- scene-only references embedded in reusable prefabs
- inactive parents masking active children
- DontDestroyOnLoad/persistent-object duplication risks
- cameras, EventSystems, AudioListeners and other uniqueness-sensitive components
- NetworkObject/network identity ownership or prefab registration where applicable

Prefer `SerializedObject`/`SerializedProperty` or the connected Editor's equivalent over reflection for serialized data. Do not traverse arbitrary managed graphs that can execute user code.

For Phase 5 coverage, route to `live-inspector` for cameras, project tags/layers/sorting layers, Input System action assets, Animator controller state machines, NavMesh data/settings, lights/lighting settings, volume profiles/components, render pipeline, physics and project settings. Record prefab source plus property modification counts before any mutation.

For large scenes, inspect targeted subtrees first and summarize counts instead of dumping the entire hierarchy into context.
