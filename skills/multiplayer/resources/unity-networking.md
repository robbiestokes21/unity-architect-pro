# Unity Networking: NGO, Netcode for Entities, Multiplayer Services

## Netcode choice
Unity provides two distinct netcode frameworks. NGO targets GameObject/MonoBehaviour workflows; Netcode for Entities targets DOTS/ECS and server-authoritative predicted simulation. Do not combine them casually or generate APIs from one for the other.

## Multiplayer Services SDK
For new compatible UGS work, use `com.unity.services.multiplayer` as the primary session abstraction. It unifies Lobby, Relay and Matchmaker functionality. Existing projects using standalone packages may remain on them until migration is requested/tested.

MPS is a session/backend layer. Gameplay state still belongs to NGO/NfE/custom networking.

## NGO implementation rules
- Use `NetworkObject`/network-prefab lifecycle for replicated GameObjects.
- Put network-aware behavior in `NetworkBehaviour` when framework callbacks/state/RPCs are required.
- Verify installed NGO version before choosing RPC attributes/API forms.
- Durable state belongs in network variables/replicated state; transient intent/events belong in RPC/message flows.
- Validate server-side requests even when ownership restrictions exist.
- Test as a true remote client; host mode hides authority mistakes.

## Netcode for Entities rules
- Follow Ghost authoring/serialization and the package's tick/prediction model.
- Keep predicted and interpolated entities/components intentional.
- Use command/input streams and authoritative server simulation appropriately.
- Test thin clients and dedicated server behavior when applicable.
- Inspect package version because bootstrap/world-creation and integration behavior can differ across versions.

## MPS session rules
- Treat session membership and transport connection as related but distinct lifecycle state.
- Handle authentication initialization and service errors explicitly.
- Implement leave/delete/teardown and reconnect flows rather than only happy-path create/join.
- Respect underlying Lobby/Relay/Matchmaker limits and billing.
