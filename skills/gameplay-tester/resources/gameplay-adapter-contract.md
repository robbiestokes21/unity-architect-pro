# Gameplay adapter contract

Implement `IGameplayTestAdapter` in project test code for domain actions and assertions. Adapter IDs and operation kinds are stable scenario API: keep them explicit, validate parameters, and never silently treat an unsupported operation as success.

The runner owns deterministic ordering, seeded randomness, timeouts, evidence, final markers, and cleanup. Adapters own project behavior such as input injection, combat commands, inventory, quests, save/load, UI, or network-aware actions. Avoid reflection into private gameplay state when a production-safe test seam can expose the same observable outcome.

Adapters must restore temporary state in `ResetAdapter`, tolerate cleanup after partial failure, stay on Unity's main thread, and report actual observed values. Multiplayer scenarios should identify the acting peer and combine this runner with the Phase 7 laboratory. Secrets and player personal data must never appear in evidence.
