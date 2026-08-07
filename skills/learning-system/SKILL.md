---
name: learning-system
description: Infer and maintain project-specific Unity conventions from repeated verified patterns—folder structure, naming, DI, async, pooling, networking and preferred packages—without overriding explicit project rules. Use to adapt Claude behavior to a codebase over time.
---
# Project Learning System

Learn only from repeated, verified repository patterns or explicit decisions. Record learned conventions with confidence and evidence in project memory. Explicit documentation and current code policy outrank inferred preferences.

Never infer secrets or personal information. Do not turn one-off implementations into global conventions without corroborating evidence.

Use `project-memory` facts for learned conventions. Store evidence paths, conservative confidence, and an expiry when the pattern is likely to change. Promote an inferred convention only after repeated corroboration or explicit project documentation. Use `memory-review` to retire conventions that no longer match the codebase.
