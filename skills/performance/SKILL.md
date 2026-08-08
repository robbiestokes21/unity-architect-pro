---
name: "performance"
description: "Analyze and improve Unity CPU, GPU, memory, GC, loading, physics, rendering, asset, mobile, and multiplayer/network performance. Use for profiling, stutter, frame-time, bandwidth, allocation, or scale problems."
---

# Unity Performance Engineering

Measure before optimizing. Identify target platform and frame/network budget.

## Evidence sources
Use Unity Profiler, Profile Analyzer, Memory Profiler, Frame Debugger/RenderDoc where appropriate, network profiler/statistics, build/player profiling, and controlled benchmarks.

## CPU/GC
Look for per-frame allocations, repeated component/object searches, reflection, LINQ/closures in hot code, Instantiate/Destroy churn, expensive UI/layout rebuilds, physics queries, main-thread asset work, and over-frequent network serialization.

## GPU
Check draw calls/batches, overdraw, shader cost/variants, shadows, texture bandwidth, post-processing, resolution and platform-specific bottlenecks. Do not call a CPU optimization a GPU fix.

## Multiplayer
Budget tick rate, snapshot/state size, RPC/event frequency, interest management, relevancy, compression/quantization, reliable backlog, prediction cost, server simulation cost and connection count. Preserve correctness/anti-cheat boundaries while optimizing bandwidth.

Provide baseline, suspected bottleneck, change, measured result and tradeoff whenever measurement is available.

## Budgets before optimization
For substantial performance work, establish a target budget before changing architecture: CPU frame/tick time, GPU frame time, GC allocation/frame, memory, load/scene transition time, draw/batch cost as appropriate, and for multiplayer bytes/sec plus server tick cost. Use platform-specific measurements when the target hardware materially differs from the Editor.
