# Durable Memory Policy

## Good memory
A record is worth persisting when all are true:
1. likely useful in a later session
2. backed by evidence or an explicit accepted decision
3. materially changes implementation, validation, migration, performance or operations
4. safe to keep in the repository

## Record classes
- **Fact**: current verifiable state. May expire or become stale.
- **Decision**: intentional choice with rationale and consequences. Preserve history; supersede, don't erase.
- **Incident**: reproducible failure/bug with root cause, resolution and ideally a regression test.
- **Performance sample**: measurement tied to scenario/build target/source/commit when possible.
- **Feature event**: durable lifecycle event such as introduced, migrated, deprecated, removed, shipped.
- **Relationship**: meaningful connection between systems, packages, assets or services.

## Avoid memory pollution
Do not store every file touched, every test run, obvious language facts, transient TODOs, speculative design brainstorms, or information trivially re-read from one nearby file unless indexing it provides clear cross-session value.

## Conflicts
Never resolve conflicts by silently overwriting history. Prefer:
- fact: refresh active value; stale/supersede old record when the distinction matters
- decision: new ADR supersedes old ADR
- incident: retain the original fingerprint and append/update verified resolution
- performance: append samples rather than replacing measurements

## Review cadence
Run memory review after migrations, package upgrades, networking changes, release cutovers, major refactors, and whenever project files contradict remembered context.
