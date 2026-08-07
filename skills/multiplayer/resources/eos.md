# Epic Online Services (EOS)

Identify the Unity binding/package and enabled EOS interfaces: Auth/Connect, Lobbies, Sessions, P2P, RTC, etc. Use official Epic documentation for exact SDK version.

EOS session/lobby/connectivity services do not by themselves define your gameplay replication architecture. Determine which netcode owns simulation and how EOS product user IDs map to game identities.

Keep client credentials appropriate for distribution and never embed server/private secrets. Handle login expiration, reconnect, lobby/session teardown and cross-platform account mapping deliberately.
