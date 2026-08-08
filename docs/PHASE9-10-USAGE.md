# Using Phase 9 Visual QA and Phase 10 Performance AI

These skills are quality gates for repeatable gameplay journeys. They are templates installed into a Unity project's development/test assemblies; they do not claim to operate a player build until the project has connected and run them.

## Visual QA

1. Create a stable Phase 8 gameplay scenario and choose step IDs as visual checkpoints.
2. Add `VisualQaContracts.cs`, `VisualQaRunner.cs`, and optionally `VisualLayoutAudit.cs` to a development-only test assembly.
3. Add `VisualQaRunner` to the test scene. For each resolution/camera/checkpoint case, assign an explicitly reviewed readable baseline texture.
4. If animation, particles, time, player names, or other dynamic pixels must be excluded, assign a same-size readable mask; pixels with nonzero alpha are ignored.
5. Set a per-channel tolerance and maximum mismatched-pixel ratio appropriate to that platform and render pipeline.
6. Run the gameplay scenario in the intended player/build. Archive the current image, heatmap, JSON result, logs, build identity, quality level, render pipeline, GPU/driver where relevant, and scenario seed.

Do not reuse baselines across incompatible resolution, aspect ratio, quality level, render pipeline, platform, color space, or intentionally different content. A human must review and approve baseline changes.

## Performance AI

1. Define budgets per target device/platform, quality level, topology and scenario before profiling.
2. Add `PerformanceBudgetContracts.cs` and `PerformanceBudgetProbe.cs` to a development-only test assembly and configure warmup plus a sufficiently representative measurement window.
3. Use a player build on target hardware where possible. Editor evidence is useful for diagnosis but includes Editor overhead.
4. Use `IPerformanceMetricSource` for loading duration, network traffic, server tick, gameplay counts, or provider-specific metrics.
5. Archive the structured result and raw Profiler capture when deeper diagnosis is required.
6. Compare like-for-like reports:

```bash
python skills/profiler-capture/scripts/compare_performance_reports.py approved-baseline.json current.json --maximum-regression-percent 10 --out comparison.json
```

Unavailable counters must be reported as unavailable and investigated; a zero reading is not automatically proof of good performance. An absolute budget and a relative regression gate answer different questions, so require both where appropriate.

## Suggested prompts

- `Use visual-verification to add reviewed baseline checks for the HUD at 16:9, 16:10, and ultrawide checkpoints. Do not update baselines.`
- `Use visual-ai to explain the largest heatmap regions and separate intended dynamic content from likely regressions.`
- `Use profiler-capture to measure the combat-wave Phase 8 scenario after 120 warmup frames for 900 frames in a Windows player.`
- `Use performance-engineer to rank the failed budgets and propose the next narrow profiler captures without changing production code yet.`
