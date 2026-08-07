# Photon

Identify whether the project uses Fusion, Quantum, or PUN before writing code. They are separate products with different programming models.

## Fusion
Inspect installed Fusion version and topology (Host/Server/Shared/etc.). Use Fusion's tick/state authority/input authority model, network object lifecycle, RPC/state synchronization and prediction mechanisms. Never substitute PUN `PhotonView`/PunRPC patterns.

## Quantum
Treat deterministic simulation as the architecture boundary. Avoid non-deterministic Unity runtime state as canonical gameplay simulation. Presentation should consume deterministic game state rather than own it.

## PUN
Use only PUN APIs/patterns in PUN projects. Preserve room/player property semantics and ownership rules. For new projects, do not recommend PUN automatically without comparing current Photon offerings and project needs.

For all Photon products, verify APIs against official Photon docs for the installed major/minor version.
