# PlayFab

Separate PlayFab backend concerns (identity, data/economy, matchmaking, telemetry, Multiplayer Servers) from realtime gameplay replication.

Never expose title secret keys or server-only credentials in the Unity client. Use player/entity tokens and server/cloud functions according to official security guidance. For Multiplayer Servers, define build allocation, readiness/health, shutdown and match backfill/teardown behavior.

If PlayFab Matchmaking selects a server/session, clearly hand off connection information to the actual game transport/netcode layer.
