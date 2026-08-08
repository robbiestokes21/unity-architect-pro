---
name: "gameplay-tester"
description: "Design and run end-to-end Unity gameplay QA flows such as movement, combat, inventory, crafting, quests, vehicles, respawn and UI interactions. Use when validating whether a feature actually works as a player experiences it."
---
# Gameplay Tester

Convert requirements into observable player journeys and invariants. Prefer deterministic test hooks and Unity Test Framework where feasible; use live Editor/input automation only where it adds coverage.

Validate success paths, cancellation, invalid input, scene transitions, save/load, pause/focus, controller/keyboard differences, repeated actions, and multiplayer remote-client behavior where relevant. Record reproduction steps and evidence for every failure.

## Phase 8 workflow

1. Describe the journey with `resources/gameplay-scenario-schema.json`.
2. Implement narrow project adapters using `assets/GameplayTestContracts.cs`; use the supplied transform adapter only for smoke coverage.
3. Validate scenarios with `scripts/validate_gameplay_scenario.py`.
4. Run `GameplayScenarioRunner` in a development/test build and consume its bounded ready, complete, or failed markers.
5. Retain result JSON, state/assertion values, logs, seed, build identity, and failure screenshot. Never infer a pass from process exit alone.
6. Reset adapters and temporary input/state after success, failure, or timeout.

For multiplayer journeys, let Phase 7 own the processes and fault conditions. Identify the acting peer and assert authority-visible outcomes. Keep adapters in test/development assemblies, prefer observable public test seams, and exclude credentials, personal data, save contents, and session tokens from evidence.
