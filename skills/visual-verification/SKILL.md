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
