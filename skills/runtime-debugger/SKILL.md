---
name: "runtime-debugger"
description: "Diagnose a running Unity game by inspecting live state, lifecycle, physics, animation, AI, tasks/coroutines, network ownership and runtime logs through available Editor/player instrumentation. Use for bugs that only reproduce in Play Mode or builds."
---
# Runtime Debugger

Prefer observation over speculative edits.

Inspect relevant live state: transforms/physics, active/enabled state, Animator parameters/state, AI/FSM/behavior-tree state, coroutines/tasks, scene lifetime, pooled objects, network ownership/spawn state/RPC flow, frame timing and exceptions.

If direct runtime introspection is unavailable, generate a temporary narrowly-scoped probe, run it, capture structured output, then remove it after verification. Do not ship debug probes unless the user explicitly wants instrumentation.

## Phase 6 workflow

1. Establish project/editor identity, compilation state, Play Mode state, reproduction window and selected runtime instance.
2. Capture logs and a pre-change snapshot. Use stable scene/hierarchy identity plus instance ID; instance IDs alone are session-local.
3. Use `IRuntimeStateDiagnostics` for FSM/AI/gameplay state and `IRuntimeNetworkDiagnostics` for provider-aware ownership/spawn/authority evidence.
4. Instrument relevant tasks, coroutines, jobs or requests with `RuntimeOperationRegistry`. Do not claim no coroutine exists merely because it was not registered.
5. Compare state across the failure transition and correlate frame/time with Console evidence and profiler metrics.
6. Make the smallest justified fix, reproduce, capture a post-change snapshot and remove temporary probes.

## Bundled templates

`assets/RuntimeDiagnosticsContracts.cs`, `RuntimeStateProbe.cs`, and `assets/UnityArchitectPro.Editor/RuntimeDebuggerWindow.cs` provide package-neutral runtime instrumentation and selected-object JSON export. Read `resources/runtime-diagnostics-contract.md` before adapting them. Verify Unity/C# compatibility and keep Editor code in an Editor-only assembly.

Runtime metrics are diagnostic signals, not profiler replacements. Route detailed CPU/GPU/GC analysis to `profiler-capture`, exceptions to `console-diagnostics`, networking behavior to `multiplayer`, and persisted scene/prefab inspection to `live-inspector`.
