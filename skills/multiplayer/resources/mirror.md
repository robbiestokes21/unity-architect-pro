# Mirror

Confirm Mirror version and selected transport. Treat server as authoritative unless the project explicitly implements another model.

Use Mirror's network spawn/identity/behaviour lifecycle rather than local Instantiate for replicated objects. Verify current Command/ClientRpc/TargetRpc and SyncVar/SyncList semantics in installed docs/source. Validate Command inputs on the server; authority attributes are not a substitute for gameplay validation.

Test dedicated server and remote client paths separately from host mode. Backend matchmaking/lobby/identity is not inherently provided by Mirror; preserve whichever external service the project uses.
