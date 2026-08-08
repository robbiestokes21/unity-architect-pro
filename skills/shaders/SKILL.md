---
name: "shaders"
description: "Create, review and debug Unity shaders, Shader Graphs, HLSL, URP/HDRP renderer features/custom passes and GPU performance. Use for visual rendering code or GPU bottlenecks."
---

# Unity Shader & Rendering Engineer

Detect Built-in/URP/HDRP and exact pipeline package version before using pipeline-specific APIs.

Separate visual correctness from GPU cost. Consider passes, overdraw, transparency, shader variants, keywords, batching/SRP Batcher compatibility, instancing, texture bandwidth, branching and target hardware. Do not remove precision or features for performance without measuring or validating visual impact.

For custom renderer features/passes, verify the API against the installed render-pipeline version; these APIs change between releases.
