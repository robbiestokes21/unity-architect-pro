---
name: "debug-fix"
description: "Diagnose and fix Unity bugs, compile errors, exceptions, broken editor behavior, regressions, desyncs, race conditions, and test failures using evidence-driven reproduction and verification."
---

# Unity Debugging and Fixing

## Workflow
1. Capture the exact symptom, stack trace/log, platform, scene/state and reproduction path.
2. Inspect recent/relevant code and configuration.
3. Classify: compile, serialization, lifetime, logic, physics, async/threading, package/API mismatch, asset/import, platform, multiplayer, performance-induced, or editor tooling.
4. Form a falsifiable hypothesis.
5. Reproduce with the smallest useful test/log/instrumentation.
6. Fix the root cause, not the visible exception only.
7. Recompile and rerun the reproduction.
8. Run nearby regression tests.

## Unity log discipline
Read the first causal error, not just cascaded errors. A missing script/assembly/package error can generate dozens of secondary exceptions.

## Common traps
- domain reload/static state
- execution order assumptions
- callbacks after object destruction
- scene reference lost after unload
- package version/API mismatch
- serialization changes breaking prefab/scene data
- race between async operation and lifetime cancellation
- non-main-thread Unity API access
- network code working as host but failing as remote client

For multiplayer bugs, load `multiplayer`; reproduce with at least host + remote client when possible, and test latency/loss when timing-sensitive.
