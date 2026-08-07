# Default Unity Definition of Done

- Requested behavior implemented without unrelated scope expansion.
- Project compiles and no unexplained new warnings are introduced.
- Relevant EditMode/PlayMode/integration tests pass.
- Serialized data compatibility has been considered for renamed/changed fields and types.
- Scene/prefab references touched by the change are valid.
- No Editor-only API leaks into runtime/player assemblies.
- Hot-path allocations/performance regressions are considered and measured when material.
- Version-sensitive APIs are verified against installed versions.
- Multiplayer: authority, ownership, late join, disconnect and remote-client behavior are reviewed.
- Security: no client-trusted economy/damage/admin decisions and no embedded server secrets.
- Platform/build-sensitive changes receive an appropriate build.
- Temporary editor scripts, debug artifacts and accidental asset churn are removed.
- Documentation/ADR is updated when an architectural decision changed.
