---
name: "multiplayer"
description: "Architect, implement, review, debug, test, and optimize Unity multiplayer across Netcode for GameObjects, Netcode for Entities, Unity Multiplayer Services, Photon Fusion/PUN/Quantum, Mirror, FishNet, Steamworks/Facepunch, Epic Online Services, PlayFab, custom authoritative servers, and mixed backend/transport stacks. Use for any networked gameplay, sessions, matchmaking, lobbies, relay, dedicated servers, RPCs, prediction, replication, authority, or online services."
---

# Unity Multiplayer — Provider-Aware Engineering

Treat multiplayer as a distributed system, not "single-player code with RPCs".

## 1. Discover the actual stack before coding
Inspect `Packages/manifest.json`, lockfile, assemblies and networking code. Identify each layer separately:
- **simulation/netcode**: NGO, Netcode for Entities, Fusion, Quantum, PUN, Mirror, FishNet, custom
- **transport**: Unity Transport, Photon transport/cloud, KCP, Telepathy, Steam networking sockets, ENet/LiteNetLib/custom
- **session/backend**: Unity MPS/Lobby/Relay/Matchmaker, Photon rooms, EOS sessions/lobbies, Steam lobbies, PlayFab matchmaking/multiplayer servers, custom backend
- **hosting topology**: host/client, dedicated server, distributed authority, peer-to-peer, server-authoritative lockstep/deterministic
- **identity/auth**: UGS Authentication, Steam, EOS, PlayFab, platform identity, custom JWT/backend

Do not infer one layer from another. A project can use, for example, FishNet + Steam transport + custom matchmaking.

## 2. Provider selection
If the user has not chosen a stack, first derive requirements: player count, genre, tick rate, competitive vs co-op, authoritative security needs, host migration, cross-play, dedicated hosting, platform targets, expected concurrency, budget/vendor constraints, DOTS vs GameObjects, deterministic simulation, and migration constraints.

Read `resources/provider-matrix.md` before recommending a provider. Never claim one provider is universally "best".

## 3. Authority and trust model
For every networked feature explicitly define:
- authoritative owner of canonical state
- who may send intent/request
- validation performed before mutation
- replicated observers
- ownership transfer rules
- behavior for late join/reconnect/disconnect
- whether prediction is used and how reconciliation occurs

Remote clients must not directly decide damage, currency, inventory grants, match outcomes, cooldown completion, spawn authorization, or other security-sensitive canonical state in authoritative games.

## 4. State vs events
Use replicated/state variables for durable state that late joiners need. Use RPC/messages/events for transient actions. Do not model durable truth only as an RPC history.

Select reliability deliberately:
- reliable for infrequent must-arrive control/state transitions
- unreliable/sequenced for frequent replaceable updates
Avoid flooding reliable channels with high-frequency transform/input snapshots.

## 5. Tick and simulation
Know the simulation/tick model of the selected framework. Keep simulation deterministic enough for its prediction model. Avoid tying authoritative simulation directly to render frame rate. Timestamp/sequence data using the framework's network time/tick primitives rather than local wall clock where possible.

For predicted games separate:
- input collection
- input command serialization
- prediction
- authoritative simulation
- snapshots/state replication
- reconciliation
- interpolation/presentation

## 6. Spawning and ownership
Use the provider's network spawn lifecycle. Never instantiate a networked prefab locally on every peer and assume it becomes synchronized. Validate spawn requests server-side. Reset pooled network objects completely before reuse.

## 7. Scene changes
Use provider-supported network scene management or build an explicit scene synchronization protocol. Define how clients join during transitions and how persistent network objects are handled.

## 8. Sessions, lobbies, relay, matchmaking and hosting
Keep session/backend state distinct from gameplay replication. Joining a lobby/session does not necessarily mean the gameplay transport is connected.

For new Unity Gaming Services implementations, prefer the current Multiplayer Services SDK when compatible with the project. Do not automatically migrate older projects using standalone Lobby/Relay/Matchmaker packages. Unity documents the MPS SDK as the unified abstraction over those services and provides built-in integration with NGO and Netcode for Entities.

For non-Unity providers, use the provider's official current API. Never translate concepts by name alone (for example, a Photon Room, Steam Lobby, EOS Session and Unity MPS Session have different semantics).

## 9. Supported provider patterns
Read the matching resource before implementation:
- Unity NGO / Netcode for Entities / MPS: `resources/unity-networking.md`
- Photon Fusion / PUN / Quantum: `resources/photon.md`
- Mirror: `resources/mirror.md`
- FishNet: `resources/fishnet.md`
- Steamworks / Facepunch: `resources/steam.md`
- Epic Online Services: `resources/eos.md`
- PlayFab: `resources/playfab.md`
- custom dedicated/backend: `resources/custom-server.md`

If a package version is unknown or API details may have changed, invoke `docs-research` before generating provider-specific API calls.

## 10. Security review
Assume clients are hostile when the game has competitive or economic value. Validate rates, ranges, ownership, sequence/tick, state preconditions, permissions and replayability. Never trust a client-provided player ID/owner ID merely because it arrived over an authenticated connection.

Do not put backend/service secret keys in Unity clients. Server credentials belong in protected server/backend environments.

## 11. Testing
Use `testing` and cover the topology actually shipped. Minimum meaningful checks for a gameplay feature:
- remote client behavior (not only host)
- spawn/ownership
- late join or state reconstruction if relevant
- disconnect cleanup
- invalid/duplicate/out-of-order request handling when relevant
- simulated latency/loss for timing-sensitive features

## 12. Review checklist
Before declaring a multiplayer change complete, verify:
- no framework API mixing
- correct authority and RPC/message direction
- late join receives durable state
- ownership checks exist where required
- state serialization is bounded/version-compatible where needed
- disconnect/teardown unsubscribes and frees handles
- no client secrets
- bandwidth/tick cost is reasonable
- dedicated-server/headless compatibility if the project ships it
- host-only success has not been mistaken for client correctness

## 13. Advanced specialist routing
For substantial multiplayer work, delegate focused review/design to the matching agent when available:
- `network-security-reviewer` — adversarial authority/trust review
- `network-performance-analyzer` — bandwidth/tick/interest-management analysis
- `network-prediction-engineer` — prediction/reconciliation/rollback/interpolation
- `dedicated-server-engineer` — headless hosting/control-plane integration
- `multiplayer-test-agent` — topology and fault-condition verification

Before performance-sensitive work, read `resources/network-budgets.md`. Before a release-significant multiplayer change, read `resources/network-test-matrix.md` and construct the smallest matrix that represents production.
