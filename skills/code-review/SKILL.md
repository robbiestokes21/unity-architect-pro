---
name: code-review
description: Perform senior-level Unity C# code review for correctness, lifecycle, serialization, architecture, performance, concurrency, tests, editor/runtime boundaries, security/trust boundaries, and multiplayer behavior. Use for reviews, PRs, refactors, or quality audits.
---

# Unity Code Review

Review the actual code and surrounding call sites. Prioritize defects over stylistic preferences.

## Severity order
1. correctness/data loss/crashes
2. multiplayer authority/security/desync
3. Unity lifetime/domain reload/serialization breakage
4. concurrency/async cancellation/thread-affinity problems
5. memory/GC/performance in meaningful hot paths
6. maintainability/testability/API design
7. style only when project standards require it

## Unity-specific checks
- destroyed-object/null behavior
- event subscription leaks and duplicated registration after enable/reload
- coroutine/async lifetime after object destruction
- scene unload/additive loading assumptions
- ScriptableObject mutable shared state
- static state across domain reload-disabled workflows
- serialized field rename/type compatibility
- prefab/scene references and runtime-instantiated object ownership
- `Update`/`FixedUpdate` misuse
- component lookup/allocation in hot loops
- accidental Editor API dependency in runtime assembly
- Addressables/asset handle release symmetry
- pooling reset correctness

## Multiplayer review
Load the `multiplayer` skill when network code is present. Verify authority, input validation, RPC direction, ownership, replication frequency, unreliable/reliable channel choice, prediction/reconciliation, late join, host migration (if supported), disconnect cleanup, reconnect semantics, and exploit surfaces.

## Output
Give findings with file/line where possible, severity, why it matters, concrete fix, and verification suggestion. Do not pad the review with compliments or low-value nits. If no meaningful defects are found, say so and list residual risks/test gaps.
