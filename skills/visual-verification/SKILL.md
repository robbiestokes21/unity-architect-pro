---
name: "visual-verification"
description: "Verify Unity Game View, UI, scene composition, rendering, cameras, animations, and visual regressions using screenshots or captured frames. Use when correctness is visible rather than fully provable from code/tests."
---
# Visual Verification

Visual evidence supplements tests; it does not replace state assertions for logic.

## Workflow
1. define observable acceptance criteria before capture;
2. establish deterministic scene/state, resolution, aspect ratio, quality level and camera;
3. capture Game View or player frame using the available Editor/player bridge;
4. compare against acceptance criteria or an approved baseline when one exists;
5. report concrete visible differences, not aesthetic guesses;
6. retain artifacts only when the project workflow expects them.

Check UI clipping/overlap, anchors/safe areas, missing materials/shaders, lighting/camera framing, z-order, text overflow, animation pose, loading/error states and multiplayer per-client differences.

For baseline testing, tolerate explicitly defined dynamic regions/tolerances. Never silently approve a changed baseline just to make a test pass.

## Phase 9 setup and use

Use `assets/VisualQaRunner.cs` and `VisualQaContracts.cs` in a development-only test scene. Configure cases with a stable camera, checkpoint ID, capture dimensions, readable baseline, optional readable ignore mask, channel tolerance and maximum mismatch ratio. Nonzero mask alpha excludes a pixel from comparison. Phase 8 `StepCompleted` events trigger matching cases; `CaptureCase` supports explicit capture.

Results are written under `Application.persistentDataPath/UnityArchitectPro/VisualQa` as current PNG, heatmap PNG and JSON. Treat dimension/readability errors as failures. Use `VisualLayoutAudit` only with deliberate reference lists: automated overlap checks across an entire UI create false positives for intentional stacking.

Example request: `Use visual-verification to verify the inventory-open checkpoint at 1920x1080 and report clipping, missing materials, pixel mismatch, and the heatmap without changing the baseline.`
