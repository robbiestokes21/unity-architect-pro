# Scenario matrix
Minimum release-significant coverage should include a production topology happy path, one remote client, late join/state reconstruction, disconnect cleanup, reconnect if supported, scene/match transition, and at least one degraded-network profile for timing-sensitive gameplay. Add hostile/invalid requests for authoritative competitive/economy features. Scale/load tests are separate from correctness tests.

Phase 7 scenarios express late join with delayed `start`, reconnect with `restart`, and verified network shaping with paired `fault_on`/`fault_off` actions. See `fault-injection.md` for baseline, regional, degraded and hostile-mobile profiles. A fault profile without tool/application verification is inconclusive.
