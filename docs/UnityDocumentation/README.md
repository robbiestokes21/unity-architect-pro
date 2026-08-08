# Optional local Unity 6.5 documentation

Unity Architect Pro can use an extracted local copy of the Unity 6.5 Manual and Scripting Reference when online documentation is unavailable or local research is requested.

## Install

1. Download `UnityDocumentation.zip` from the matching GitHub release asset. Git clones require Git LFS to retrieve the archive itself.
2. Verify its SHA-256: `8204FCFC9A34253065F571F8A077DF36F1E4657F4A6DB20207FC5C0706F3000D`.
3. Extract it so `docs/UnityDocumentation/Documentation/en/Manual/UnityManual.html` exists.

The extracted `Documentation/` directory is intentionally ignored by Git. Do not add it with `git add -f`.

This archive targets Unity **6.5 / 6000.5**. Use it only for a compatible editor stream. Installed package documentation remains the higher priority for package-specific APIs.

Unity owns the documentation and trademarks. The archive is not covered by Unity Architect Pro's MIT license. Read [NOTICE.md](NOTICE.md) and the included `Documentation/en/Manual/TermsOfUse.html`.
