---
name: "live-editor"
description: "Operate a connected Unity Editor as a live engineering surface: inspect hierarchy/components, read Console state, enter/exit Play Mode, invoke safe editor actions, capture Game View evidence, and verify changes. Use when the task depends on the actual running Editor rather than source files alone."
---

# Live Unity Editor Intelligence

Treat the Editor as stateful infrastructure. Never assume the open scene, Play Mode state, selected object, compile state, or domain state.

When the bridge is MCP, load `mcp-unity` and follow `../../mcp/README.md`. Discover live resources/tools and select the intended Editor instance before this skill's capability handshake.

## Capability handshake
Before acting, discover the available Editor bridge and map only capabilities that really exist:
- project/editor identity and Unity version
- compilation state and diagnostics
- hierarchy/scene inspection
- component/SerializedProperty inspection
- Editor method execution
- Play Mode control
- Console/log retrieval
- Game/Scene view screenshots
- test execution
- profiler capture/metrics

If a capability is absent, route to a safe fallback: temporary Editor script, Unity batchmode, log parser, or explicit unverified status. Never invent MCP tool names.

## Transaction protocol
For every mutation:
1. snapshot enough pre-state to detect accidental churn;
2. ensure compilation is clean;
3. leave Play Mode when asset mutation requires it;
4. perform one logical mutation at a time;
5. save explicitly;
6. wait for refresh/domain reload if triggered;
7. inspect the resulting object/component/asset;
8. run a focused behavior check;
9. remove temporary automation.

Do not parallelize state-changing Editor calls.

## Hierarchy intelligence
For scene/prefab tasks, inspect hierarchy paths, active state, prefab instance status, sibling order, components and serialized references. Prefer stable object identification by scene path + hierarchy path + component type; do not rely on display names alone when duplicates exist.

## Runtime intelligence
In Play Mode, distinguish runtime instances from persisted assets. Capture relevant runtime state before stopping Play Mode. Never claim a runtime change persisted unless the underlying serialized asset was intentionally saved through an Editor workflow.

Route deep live-state diagnosis to `runtime-debugger`, including explicit FSM/AI adapters, network ownership adapters, registered task/coroutine lifecycles and bounded runtime metrics. The live-editor skill owns the Editor session; runtime-debugger owns diagnostic evidence.

## Evidence
A live-editor claim should be backed by at least one of: inspected property value, hierarchy result, clean Console slice, screenshot, passing test, profiler metric, or build/run result. Route screenshots to `visual-verification`, logs to `console-diagnostics`, and performance evidence to `profiler-capture`.

## Bundled Unity-side templates
`assets/UnityArchitectPro.Editor/` contains optional Editor utilities for hierarchy snapshots and Game View capture. Treat them as templates: verify the project's Unity/C# compatibility, copy into an Editor-only assembly, run, collect evidence, then remove them unless the project intentionally adopts the tooling.

Phase 5 also includes `LiveUnityInspector.cs` and `SerializedPropertyMutation.cs`. Use `resources/live-inspector-contract.md` as the stable evidence/mutation contract. Prefer read-only full reports or targeted selection inspection; mutate one property only after capturing its stable global object ID, property path, and exact expected value. Package-specific surfaces remain optional and are discovered through assets/serialized state.
