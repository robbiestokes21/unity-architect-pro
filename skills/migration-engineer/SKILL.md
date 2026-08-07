---
name: migration-engineer
description: Plan and execute safe Unity migrations across editor versions, render/input/networking packages, serialization schemas, APIs, prefabs/scenes, and assembly boundaries with checkpoints and rollback strategy.
---
# Unity Migration Engineering

Migrations are staged compatibility projects, not search-and-replace exercises.

## Plan
Inventory current/target Unity and package versions, deprecated/removed APIs, serialized data risks, package compatibility, build targets and third-party plugins. Define rollback point and migration checkpoints.

## Execute
Prefer incremental upgrades across unsupported gaps when vendor guidance requires it. Preserve serialized data using supported migration attributes/tools, open and resave assets only when necessary, and isolate mechanical API migrations from behavior changes.

At each checkpoint: resolve packages -> compile -> targeted tests -> scene/prefab integrity -> representative build. For networking migrations, validate wire/state semantics, ownership and session behavior; do not assume API-equivalent means protocol-equivalent.
