# Runtime diagnostics contract

Phase 6 uses explicit diagnostic adapters rather than traversing arbitrary private managed graphs.

## Evidence surfaces

- `RuntimeStateProbe`: identity, hierarchy path, transform, Rigidbody/Rigidbody2D, Animator layer/parameter state, bounded operations and lightweight runtime metrics.
- `IRuntimeStateDiagnostics`: FSM, behavior-tree, utility AI, planner, ability or gameplay state supplied by the owning system.
- `IRuntimeNetworkDiagnostics`: package-neutral object ID, owner, spawn and local-authority state plus provider-specific bounded values.
- `RuntimeOperationRegistry`: explicit task/coroutine/job/request lifecycle. Register at start and update on completion, failure or cancellation.
- `RuntimeDebuggerWindow`: read-only selected-object capture in Play Mode and JSON export under `Temp/UnityArchitectPro`.

## Safety and limitations

- Do not reflect arbitrary fields, enumerate managed graphs, reveal secrets, or execute property getters for diagnostics.
- Unity has no safe public API that lists every coroutine. Unregistered operations are **unknown**, not absent.
- A package adapter must match the installed provider/version. Do not infer ownership from component names.
- Bound output sizes and sampling rates. `FindObjectsOfType` is diagnostic-only and must not ship in a production hot path.
- Runtime changes are not persisted unless a separate, explicit Editor transaction writes serialized state.
- Remove templates after diagnosis unless the project intentionally adopts development-only instrumentation.
