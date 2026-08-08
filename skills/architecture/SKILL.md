---
name: "architecture"
description: "Design advanced Unity systems and features before implementation, including gameplay architecture, save/load, inventory, combat, AI, UI, scene flow, services, content pipelines, ECS/DOTS, and multiplayer. Use for large or cross-cutting features."
---

# Unity Architecture

Start from constraints: game type, target platforms, team size, content scale, save requirements, multiplayer topology, performance budget and installed packages.

## Design output
Define responsibilities, data ownership, runtime boundaries, public interfaces/events, serialization/persistence, scene/prefab boundaries, lifecycle, dependency flow, failure handling, test strategy, and migration plan.

Prefer simple architecture with explicit seams. Do not force a generic pattern (service locator, DI container, ECS, event bus, singleton, MVVM) without a concrete need.

## Multiplayer architecture
If networked, delegate detailed networking decisions to `multiplayer`. Explicitly separate local presentation, predicted/local input, authoritative game state, replicated state, backend/session state and persistence. Define what clients may request versus what they may decide.

Produce an implementation sequence that keeps the project compiling and testable after each major step.
