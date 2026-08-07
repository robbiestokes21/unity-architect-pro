---
name: docs-research
description: Research Unity APIs/packages using official version-matched documentation first. Use whenever API behavior, package compatibility, deprecations, installation, multiplayer APIs, render/input packages, or Unity-version differences matter.
---

# Unity Documentation Research

## Source priority
1. Installed package metadata/docs in the project (`Packages`, package cache if accessible)
2. Official Unity Manual / Scripting API for the exact editor stream
3. Official Unity package documentation on docs.unity3d.com or docs.unity.com
4. Official package repositories/samples
5. Third-party provider official docs/repositories
6. Community sources only for gaps, and label them as such

Do not use random tutorials to establish API truth when official docs exist.

## Version matching
Read `ProjectVersion.txt`, `manifest.json`, and lockfile first when available. Distinguish:
- Unity Editor version
- package version
- service SDK version
- transport version
- pre-release vs released package

Never copy current docs into an older project without checking compatibility. Never replace a working legacy API solely because newer docs deprecate it unless migration is requested or required.

## Research output
State the project/version context, authoritative source, relevant API behavior, compatibility/deprecation note, and the exact implementation consequence. If evidence conflicts, explain the conflict rather than guessing.

## Multiplayer documentation
For Unity Gaming Services, prefer the current Multiplayer Services SDK for new work when compatible, while recognizing existing projects may intentionally use legacy standalone Lobby/Relay/Matchmaker packages. For Photon, Mirror, FishNet, Steam/Facepunch, EOS, PlayFab or other providers, use their official version-matched docs and do not mix concepts/API names across providers.
