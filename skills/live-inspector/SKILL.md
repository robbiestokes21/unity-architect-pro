---
name: live-inspector
description: Inspect a real Unity Editor's loaded hierarchy, arbitrary serialized components/properties, prefab overrides, cameras, input, animation, navigation, lighting/rendering/physics and project settings; safely modify one serialized property with optimistic verification. Use for Phase 5 Inspector work.
---

# Live Unity Inspector

Use after `live-editor` capability discovery and before scene/prefab/project-setting edits. Prefer the connected bridge when it exposes equivalent semantic capabilities; otherwise install the templates from `skills/live-editor/assets/UnityArchitectPro.Editor/` into an Editor-only assembly after checking Unity compatibility.

## Inspection workflow

1. Confirm target project, Unity version, compile state, active scene and Play Mode state.
2. Capture a full report for cross-system audits or inspect the current selection for a bounded question.
3. Treat runtime instances and persisted assets separately.
4. For optional packages (Input System, AI Navigation, URP/HDRP volumes), report absence instead of assuming installation.
5. Keep reports in `Temp/UnityArchitectPro`; never commit project content or sensitive values merely to provide evidence.

## Mutation workflow

Mutation is opt-in and single-property. Capture a fresh global object ID, property path and formatted value. Review prefab/project-setting blast radius. Create the request described by `../live-editor/resources/live-inspector-contract.md`, run it serially outside Play Mode when persistence requires, inspect the read-back value and diff, then run focused tests. Never bypass the allowed property types, expected-value guard, `m_Script` block, project-settings opt-in or Undo recording.

Use `hierarchy-inspector` for wiring analysis, `editor-control` for transactional state changes, `input-engineer` for behavior, `gameplay-ai` for navigation behavior, `shaders` for pipeline behavior, and `testing`/`self-review` for completion evidence.
