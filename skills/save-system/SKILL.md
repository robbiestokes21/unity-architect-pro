---
name: "save-system"
description: "Design, implement, review and migrate Unity save/persistence systems including local files, cloud saves, versioned schemas, migrations, atomic writes, corruption recovery, encryption/signing boundaries and multiplayer persistence."
---

# Unity Save/Persistence Engineer

Persistence is a schema, not just serialization.

Define save identity, schema version, migration chain, atomic write strategy, backup/recovery and compatibility policy. Never deserialize untrusted polymorphic data with unsafe type activation. Treat encryption as confidentiality only; authoritative multiplayer economies require server-side validation regardless of local encryption.

For local saves prefer write-temp -> flush -> atomic replace/rename where platform allows. Test interrupted writes, old-version migration, missing fields, corrupt data and downgrade behavior.

For multiplayer/cloud data, define conflict resolution and which backend owns canonical state.
