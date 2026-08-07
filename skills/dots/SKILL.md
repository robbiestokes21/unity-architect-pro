---
name: dots
description: Design, implement, review and optimize Unity DOTS/Entities/Burst/Jobs code. Use for ECS worlds, systems, bakers, components, jobs, NativeContainers, Burst, Netcode for Entities and hybrid GameObject/ECS projects.
---

# Unity DOTS Engineer

Verify installed Entities/Burst/Collections/Netcode package versions first.

Prefer data-oriented design based on access patterns, not ECS for its own sake. Track world/system lifetime, structural changes, command buffers, allocator lifetime, safety handles and sync points. Burst-compatible hot paths must avoid managed allocations/references.

For jobs, reason about read/write dependencies explicitly. Do not defeat parallelism with unnecessary `Complete()` calls. For Entities Graphics or Netcode for Entities, load matching specialist guidance and version-aware docs.

Hybrid projects need an explicit boundary between authoring/GameObject presentation and ECS simulation.
