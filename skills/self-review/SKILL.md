---
name: "self-review"
description: "Run Unity Architect Pro's completion gate after implementing a meaningful change. Compile, inspect diagnostics, review architecture/performance/security impact, run targeted tests, validate Editor/runtime state, and build when required before declaring work done."
---

# Unity Completion Gate

Use this after implementation, not as ceremony before work.

## Gate order
1. **Scope check** — inspect the diff and confirm only intended behavior changed.
2. **Compilation** — Unity compile succeeds; no unexplained new warnings.
3. **Static review** — lifecycle, serialization, null/destroyed-object semantics, async/threading, allocations and API-version correctness.
4. **Specialist review** — multiplayer/security, Addressables, DOTS, shaders, UI, save migration as applicable.
5. **Targeted tests** — smallest reliable tests first.
6. **Runtime/Editor validation** — use `live-editor`/`hierarchy-inspector`; add `console-diagnostics`, `visual-verification`, or `profiler-capture` evidence when applicable.
7. **Build validation** — required for platform-sensitive, IL2CPP, dedicated server, package, stripping or release-affecting work.
8. **Diff re-read** — ensure generated/temp files, secrets and accidental asset churn are absent.

## Definition of Done
A feature is complete only when all applicable gates pass or remaining gates are explicitly reported as unverified with a reason.

Read `resources/definition-of-done.md` for the default checklist and adapt it to project-local requirements.

## Release-grade additions
Before a release or migration, include `asset-integrity`. For online services/servers include `observability` and the production topology subset of `multiplayer-harness`. For package/version changes include `package-manager`/`migration-engineer` verification.

## Durable memory write-back
After applicable gates pass, invoke `project-memory` for material discoveries: bug root cause/regression test, accepted architecture changes, important feature lifecycle events, networking decisions and measured performance changes. Do not write memory before validation, and do not record routine implementation noise.
