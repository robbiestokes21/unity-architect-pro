# Multiplayer Network Test Matrix

Select only scenarios relevant to the shipped topology/provider, but never validate network gameplay with host mode alone.

## Topology
- 1 dedicated server + 1 remote client
- 1 dedicated server + N clients at intended match size
- host + remote client(s), if host mode ships
- late join into active gameplay
- reconnect after transient transport loss, if supported
- ownership transfer, if supported

## Network conditions
Test provider-supported simulation around expected regions/players:
- baseline LAN/local
- 50–100 ms RTT
- 150–250 ms RTT for degraded-but-supported conditions
- jitter
- 1–5% packet loss where appropriate
- burst loss
- reordering/duplication only if the transport/provider can simulate them meaningfully
- bandwidth cap for mobile/poor connections when relevant

## Failure scenarios
- client disconnect during spawn/scene transition
- server shutdown/crash
- session allocation timeout
- relay/session/matchmaking failure
- authentication expiry or rejected token
- duplicate/replayed gameplay request
- stale/out-of-order input
- reconnect with stale local state

## Assertions
Measure state convergence, prediction corrections, hard snaps, message/RPC rejection, orphan cleanup, session cleanup, bytes/sec/player, server CPU/frame/tick budget and reliable queue pressure.
