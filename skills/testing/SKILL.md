---
name: testing
description: Design, write, run and interpret Unity EditMode, PlayMode, integration, scene, build/player, and multiplayer tests. Use whenever verifying Unity behavior or adding regression coverage.
---

# Unity Testing

Choose the cheapest layer that can reliably prove the behavior.

## Test layers
- pure C# unit tests for domain logic
- EditMode tests for editor tooling/assets and fast Unity-object behavior where valid
- PlayMode tests for lifecycle, frames, coroutines, scenes, physics and runtime components
- player/build tests for stripping, platform defines, IL2CPP/runtime-only behavior
- multiplayer integration tests for authority/replication/session behavior

## Rules
Tests must have a meaningful failure signal. Avoid sleep-based timing when a deterministic condition can be awaited. Clean up created scenes/assets/network sessions. Keep tests independent of execution order.

## Multiplayer test matrix
When applicable test: host + client, dedicated server + clients, late join, disconnect, reconnect, ownership transfer, invalid client input, packet delay/loss/jitter, scene transition, spawn/despawn and session teardown. Adapt to provider capabilities rather than assuming all stacks support host migration or dedicated servers.

When Unity Editor test tooling is available, run stateful operations serially and wait for compilation/domain reload before tests.

## Network condition testing
For multiplayer features, read the multiplayer skill's `resources/network-test-matrix.md`. Prefer provider-native network simulation when it exists; otherwise isolate simulation in test/dev-only transport wrappers. Never ship artificial latency/loss code enabled by default.

Record topology and conditions with results so a passing localhost test is not mistaken for WAN validation.

## End-to-end multiplayer harness
For release-significant online behavior, route to `multiplayer-harness`. Prefer Multiplayer Play Mode when installed for small local scenarios; use standalone/headless process orchestration for production topology, provider-independent verification, or larger matrices. A localhost host-only pass is insufficient evidence for authoritative remote-client behavior.

## Visual and performance tests
Route visible acceptance criteria to `visual-verification` and budget assertions/measurements to `profiler-capture`. Keep correctness and performance verdicts separate.
