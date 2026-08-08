---
name: "refactoring-engine"
description: "Perform safe cross-file Unity refactors with serialization, scene/prefab, asmdef and package awareness. Use for splitting god classes, renaming serialized members/types, moving assemblies, introducing interfaces, or replacing architecture without breaking assets."
---
# Refactoring Engine

Before changing code, determine serialized and asset blast radius. Preserve serialized data with supported migration attributes/patterns where possible, update references atomically, compile after structural steps, and run affected tests/build checks.

Prefer staged refactors: characterization tests → seam creation → migration → removal → asset integrity scan → completion gate.
