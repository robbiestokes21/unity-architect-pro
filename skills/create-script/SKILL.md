---
name: "create-script"
description: "Create or modify production-quality Unity C# scripts, MonoBehaviours, ScriptableObjects, custom inspectors, editor tooling, ECS systems/components, utilities, and package code. Use whenever writing Unity C#."
---

# Advanced Unity C# Generation

## Inspect first
Determine Unity version, assembly, namespace, neighboring patterns and relevant package versions. Search for an existing type with the same responsibility before creating a new one.

## Choose the correct Unity construct
- `MonoBehaviour`: scene/prefab lifecycle behavior
- `ScriptableObject`: reusable/configurable serialized data or authoring assets
- plain C# type: domain logic that does not require Unity lifecycle/serialization
- Editor type under an Editor assembly/folder: tooling only
- ECS component/system/aspect: only when the project uses Entities/DOTS

Do not turn every class into a MonoBehaviour.

## Code rules
- Match project formatting and language level.
- Prefer private serialized fields or auto-properties according to project conventions; avoid public mutable fields as API by default.
- Validate inspector configuration early and emit actionable errors where appropriate.
- Cache component references used repeatedly; do not call expensive lookups every frame.
- Avoid LINQ, closures, boxing and temporary collections in proven hot loops unless acceptable for context.
- Avoid `async void` except event-style boundaries. Carry `CancellationToken` when lifetime cancellation matters.
- Do not call UnityEngine APIs from arbitrary worker threads.
- Treat `UnityEngine.Object` null semantics correctly.
- Subscribe/unsubscribe symmetrically to events; define who owns the subscription lifetime.
- Avoid string-based Invoke/coroutine APIs when typed alternatives exist.
- Use `TryGetComponent` where appropriate.
- Do not use `Resources` as a default architecture choice; follow existing Addressables/asset-loading strategy.
- Preserve serialized names with `FormerlySerializedAs` when refactoring serialized fields when appropriate.

## Lifecycle selection
Use the smallest lifecycle surface needed. Do not create empty `Start`/`Update`. Put physics mutation in fixed-step logic when required. Distinguish initialization order from enable/disable lifetime.

## Editor scripts
For scene/prefab mutation use Undo-aware APIs where interactive, mark/save dirty state intentionally, and use `AssetDatabase`/`PrefabUtility`/`EditorSceneManager` safely. Never put Editor APIs in runtime assemblies.

## Output/implementation workflow
1. Inspect dependencies and call sites.
2. Design public API and ownership.
3. Implement the minimal complete change.
4. Compile.
5. Fix diagnostics introduced by the change.
6. Add/update targeted tests when behavior is non-trivial.
7. Re-read the diff for serialized compatibility, lifecycle leaks, allocations, and concurrency issues.
