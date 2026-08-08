---
name: "visual-ai"
description: "Perform screenshot-based Unity visual QA for UI layout, missing assets, materials, lighting, camera/rendering regressions and cross-resolution differences. Use after visual changes or when tests require image judgment."
---
# Visual AI QA

Compare current captures against explicit acceptance criteria or approved baselines. Check resolution/aspect ratio, safe areas, clipping, overlap, missing text/materials, camera composition, lighting/shadow anomalies and render-pipeline regressions.

Do not call a screenshot correct just because capture succeeded. Separate deterministic pixel/baseline checks from semantic visual judgment.

Use Phase 9 `visual-verification` artifacts as evidence. Explain important heatmap regions and layout findings, distinguish intended animation/dynamic content from regressions, and request explicit review before any baseline update.
