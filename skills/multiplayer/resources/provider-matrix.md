# Provider Selection Matrix

Use this as a decision aid, not a ranking. Verify current package/provider capabilities in official documentation before making a final recommendation.

| Stack | Strong fit | Key cautions |
|---|---|---|
| Unity Netcode for GameObjects (NGO) | GameObject/MonoBehaviour projects, small-to-medium sessions, Unity-first workflows, integration with Unity MPS | Design authority carefully; validate package-version RPC/API differences; not the same scaling/prediction model as NfE |
| Unity Netcode for Entities (NfE) | DOTS/ECS, high-performance server-authoritative simulation, prediction/lag compensation, larger/complex realtime games | Requires DOTS architecture and specialist knowledge; do not mix with NGO in one project as if interchangeable |
| Unity Multiplayer Services (MPS) | Unity-hosted session/lobby/relay/matchmaker workflows, especially with NGO/NfE | Backend/session SDK, not a substitute for gameplay netcode; service costs/limits/auth requirements apply |
| Photon Fusion | Realtime action/co-op/competitive games wanting mature hosted networking and prediction/topology options | Cloud/vendor model and API/version differences; do not generate PUN APIs in Fusion code |
| Photon Quantum | Deterministic simulation/competitive designs where its deterministic architecture is desired | Architectural commitment; gameplay must fit deterministic simulation model |
| Photon PUN | Existing/legacy Photon projects and simpler room/RPC patterns | Do not choose by default for a new advanced project when Fusion/other options better match requirements |
| Mirror | Open-source GameObject networking, dedicated/host architectures, broad transport ecosystem | You own hosting/backend choices; confirm current authority/serialization APIs |
| FishNet | Feature-rich open-source Unity netcode with prediction/observers/multiple transports | Verify installed version because APIs/features evolve; backend/session layer is separate |
| Steamworks / Facepunch | Steam identity, lobbies, invites, networking sockets for Steam-distributed games | Steam ecosystem/platform constraints; often paired with a gameplay netcode rather than replacing all netcode concerns |
| Epic Online Services (EOS) | Cross-platform identity/social/lobbies/sessions/P2P/connectivity services | EOS is often a service/connectivity layer; gameplay replication may still need a netcode framework |
| PlayFab | Backend, identity, matchmaking, economy, telemetry, Multiplayer Servers | Gameplay replication is separate; secure server-side service usage and title/player auth correctly |
| Custom authoritative server | Full control, custom scale/security/protocol, non-Unity server tech | Highest engineering/ops cost; protocol/versioning/observability/deployment are your responsibility |

## Selection questions
1. Is the simulation GameObject-based, DOTS, or deterministic?
2. How many concurrent players per match/world?
3. Is cheating resistance important enough to require dedicated authority?
4. Is client-host acceptable? Is host migration required?
5. Need cross-play identities/friends/invites?
6. Need relay/NAT traversal?
7. Need managed matchmaking or dedicated-server allocation?
8. Target platforms and certification restrictions?
9. Can the team operate servers/backend infrastructure?
10. Existing provider/package investment and migration cost?
