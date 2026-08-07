---
name: editor-control
description: Safely operate or automate the Unity Editor: compile, enter/exit Play Mode, run editor methods, create/edit scenes and prefabs, add/configure components, inspect logs, refresh assets, and validate saved state. Use whenever a task changes Editor-managed assets or requires running Unity.
---

# Unity Editor Control

## Capability discovery
First identify which Unity integration is actually available (MCP server, Rider integration, Unity-specific MCP, CLI/batchmode, or none). Use only tools that are present. Never fabricate a tool name. Read `resources/editor-integration.md` when configuring or mapping editor capabilities.

## Serial execution rule
Do not run state-changing Editor operations concurrently. Compilation, domain reload, Play Mode transitions, asset refresh, tests, scene/prefab saves and editor-method execution can invalidate one another.

## Safe order of operations
1. Confirm project/editor target.
2. If code changed, allow/trigger refresh and wait for compilation.
3. Check compile errors before invoking dependent editor code.
4. Ensure Play Mode state is appropriate.
5. Execute one mutation/validation step.
6. Save scene/prefab/assets explicitly.
7. Validate resulting hierarchy/component values or diff.
8. Clean temporary editor automation scripts when no longer needed.

## Scenes/prefabs
Prefer Unity Editor APIs over hand-editing `.unity` and `.prefab` YAML for structural changes. YAML editing is reserved for narrow, understood text-level operations where GUID/fileID semantics are known and the user explicitly accepts the risk.

Use:
- `EditorSceneManager` for scene open/create/save
- `PrefabUtility.LoadPrefabContents` -> modify -> `SaveAsPrefabAsset` -> `UnloadPrefabContents` for prefab contents
- `Undo`/`ObjectFactory` for interactive-friendly editor changes
- `SerializedObject`/`SerializedProperty` for serialized inspector changes when appropriate

Preserve prefab overrides intentionally. Do not accidentally apply or revert overrides.

## Temporary automation
When direct editor mutation tools do not exist, create a temporary Editor script with a deterministic public static entry point. Make the action idempotent when practical, log clear success/failure, save all touched assets, run it through the available integration, verify the result, then remove the temporary script and its generated metadata if appropriate.

## Play Mode
Never modify project assets assuming Play Mode persistence. Know whether Enter Play Mode Options/domain reload are enabled before relying on static initialization behavior.

## Failure behavior
If compilation fails, stop editor execution and diagnose the compilation error first. If an editor action partially succeeds, inspect saved state before retrying so the second attempt does not duplicate objects/assets.

## Advanced routing
Use `live-editor` for connected live inspection/operation, `hierarchy-inspector` for serialized wiring, `console-diagnostics` for current-run errors, `visual-verification` for screenshots, and `profiler-capture` for runtime evidence. The Editor-control skill owns mutation safety; those skills own specialized evidence.
