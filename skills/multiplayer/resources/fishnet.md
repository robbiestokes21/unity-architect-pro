# FishNet

Confirm FishNet version, transport, prediction usage, observer configuration and topology before implementation. APIs evolve, so consult official FishNet docs/source for exact attributes/method names.

Respect FishNet's server/client/network object lifecycle. Use the framework's spawn/despawn, ownership, RPC, SyncType, prediction and observer mechanisms instead of custom parallel replication unless deliberately required.

Server-side validation remains mandatory for sensitive gameplay. Test remote owner, non-owner observer and server behavior; host-only testing is insufficient.
