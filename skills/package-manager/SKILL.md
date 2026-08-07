---
name: package-manager
description: Safely analyze and change Unity Package Manager dependencies, scoped registries, Git/local packages, lockfiles, package migrations, and compatibility. Use when adding/upgrading/removing Unity or third-party packages.
---
# Package Management

Read both `Packages/manifest.json` and `packages-lock.json`. Identify direct vs transitive dependencies and source type before modification.

For upgrades, check Unity editor compatibility, package release/migration notes and related packages before editing the manifest. Make one dependency family change at a time when practical, refresh/resolve, compile, then test. Do not hand-edit the lockfile to force versions unless the package workflow explicitly requires it.

Never silently replace a Git/local/scoped-registry dependency with a registry package. Preserve embedded package modifications intentionally.

For multiplayer packages, invoke `multiplayer` and `docs-research` because backend/netcode migrations can change behavior, not just APIs.
