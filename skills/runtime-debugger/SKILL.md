---
name: runtime-debugger
description: Diagnose a running Unity game by inspecting live state, lifecycle, physics, animation, AI, tasks/coroutines, network ownership and runtime logs through available Editor/player instrumentation. Use for bugs that only reproduce in Play Mode or builds.
---
# Runtime Debugger

Prefer observation over speculative edits.

Inspect relevant live state: transforms/physics, active/enabled state, Animator parameters/state, AI/FSM/behavior-tree state, coroutines/tasks, scene lifetime, pooled objects, network ownership/spawn state/RPC flow, frame timing and exceptions.

If direct runtime introspection is unavailable, generate a temporary narrowly-scoped probe, run it, capture structured output, then remove it after verification. Do not ship debug probes unless the user explicitly wants instrumentation.
