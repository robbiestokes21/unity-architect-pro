---
name: "profiler-capture"
description: "Capture and interpret Unity runtime performance evidence using Profiler, ProfilerRecorder, frame timing, memory data, network profiler, or structured instrumentation. Use when optimizing or validating performance budgets."
---
# Profiler Capture and Performance Evidence

Do not optimize from intuition alone. Establish target device/build/topology and budgets first.

## Capture hierarchy
Prefer the most representative available source:
1. development/player build on target hardware;
2. dedicated server/headless build for server budgets;
3. Editor only for early diagnosis, with Editor overhead clearly noted.

Collect only relevant counters to minimize measurement perturbation. Useful domains include main/render thread time, GC allocations/collections, batches/draw calls, physics, jobs, memory, loading, network messages/bytes and server tick duration.

Use Unity Profiler/ProfilerRecorder APIs when compatible with the project's version, provider-native network profilers where applicable, and project instrumentation for domain-specific counters.

## Comparison protocol
Capture baseline -> make one optimization class -> capture again under the same scenario -> compare median/p95/p99 where timing variability matters. Do not claim improvement from a single noisy frame.

Route multiplayer bandwidth/tick findings to `network-performance-analyzer`. Route memory ownership/leaks involving Addressables to `addressables`.

## Runtime probe template
`assets/RuntimePerformanceProbe.cs` demonstrates a development-only `ProfilerRecorder` probe. Counter names/availability vary by Unity version and platform; verify them before installing. Do not ship diagnostic logging by accident.
