# Steamworks / Facepunch

First distinguish official Steamworks.NET, Facepunch.Steamworks, Steamworks SDK bindings, and any transport adapter in use. Do not mix their API types.

Steam lobbies are discovery/social/session coordination primitives, not automatically a complete gameplay replication layer. Determine whether gameplay packets use Steam Networking Sockets/P2P directly or a netcode transport adapter for NGO/Mirror/FishNet/etc.

Never trust lobby metadata as secure authoritative gameplay state. Validate identity and gameplay actions at the authoritative simulation layer. Handle invites, lobby leave, owner changes and connection teardown explicitly.
