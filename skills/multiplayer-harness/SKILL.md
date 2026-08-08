---
name: "multiplayer-harness"
description: "Build and run repeatable Unity multiplayer test harnesses with multiple clients/servers, local player instances, headless builds, network-condition simulation, structured logs, readiness checks, teardown, and result aggregation. Use for real end-to-end network verification."
---
# Multiplayer Harness

The goal is repeatable production-like evidence, not just "Host worked in Editor".

## Phase 7 laboratory

Use `scripts/multiplayer_lab.py` with a versioned scenario matching `resources/scenario-schema.json`. It supports dependency-ordered startup, delayed late join, expected stop, restart/reconnect, explicit external fault-controller actions, readiness/completion/failure regex evidence, per-generation logs, bounded tails, deterministic variables and guaranteed reverse-order teardown.

Use `scripts/provider_adapter.py` and `resources/provider-adapter-contract.md` to render verified project/provider launch descriptors. The included standalone descriptor is a template contract, not a claim that every networking package accepts the same command-line flags.

## Topology adapters
Select the safest supported adapter for the installed stack:
- Unity Multiplayer Play Mode for small local Editor/player scenarios when installed;
- provider-specific multi-instance tooling when available;
- standalone client + dedicated server processes;
- thin clients for Netcode for Entities where appropriate;
- custom process orchestration for third-party frameworks.

Never assume Multiplayer Play Mode exists. Detect package/version first.

## Harness contract
Each process receives an explicit role, player identity/test token, endpoint/session input, test scenario ID, log path, timeout and deterministic seed where practical. Server exposes readiness; clients expose connected/ready/test-complete signals. Teardown must terminate orphan processes.

## Fault scenarios
Support a matrix chosen from latency, jitter, packet loss, reordering when provider supports it, disconnect/reconnect, late join, server stop, host loss, scene transition, duplicate request, invalid authority request, session expiration and allocation failure.

## Results
Aggregate topology, build hashes/versions, network conditions, pass/fail, connection timings, disconnect reason, assertion failures, server tick metrics, bandwidth and artifact paths. Use `resources/harness-result-schema.json` as the stable output shape.

Schema version 2 also records actions, process generations, readiness/completion timings, failures and artifact directories. A scenario passes only after all scheduled actions run, required processes become ready, and every required completion marker is observed.

Do not ship test tokens, cheats or fault-injection defaults in production configurations.

## Server container template
`assets/docker/Dockerfile.unity-server.template` is a starting point for Linux Dedicated Server containers. Adapt executable name, ports, native libraries, health/readiness and provider allocation arguments; never assume one hosting provider's contract.
