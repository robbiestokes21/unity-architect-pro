---
name: project-memory
description: Maintain durable Unity engineering memory: verified project facts, architecture decisions, bug/fix history, feature history, relationships, networking choices, and performance baselines. Use before/after substantial work so future Claude sessions inherit evidence-backed context without trusting stale guesses.
---
# Project Memory

Treat memory as **versioned engineering evidence**, not a transcript and not a substitute for source code.

## Store
Use `.claude/unity/project.db` through `${CLAUDE_SKILL_DIR}/scripts/memory_db.py` for structured records and `.claude/unity/decisions/ADR-*.md` for human-readable architectural decisions.

Record only durable information that will materially improve future engineering work:
- verified project facts and conventions
- accepted/superseded architecture decisions
- networking authority/topology/provider decisions
- bugs with root cause, fix, and regression test
- important feature events and migrations
- performance baselines/regressions with scenario/build target
- relationships between systems/packages/assets when useful

## Evidence hierarchy
1. current project files and Unity/package manifests
2. current Editor/runtime/build/test evidence
3. accepted project documentation/ADR
4. structured project memory
5. inferred patterns

Higher levels always override lower levels. When memory disagrees with current files, refresh or stale the memory record.

## Confidence and expiry
- `1.0`: explicit project setting, manifest, accepted ADR, or directly verified runtime/build result
- `0.8-0.95`: repeated source-code evidence or strongly corroborated convention
- `0.5-0.79`: useful inference that requires re-checking before risky work
- below `0.5`: normally do not persist

Give volatile facts a TTL. Package/API versions, temporary hosting topology, experimental flags and benchmark results may become stale faster than architectural intent.

## Write-back protocol
After a meaningful change passes applicable `self-review` gates:
1. record only facts that were actually verified
2. add/update the feature-history event
3. if a bug was fixed, capture root cause + regression test
4. if architecture changed, write/update an ADR and corresponding decision record
5. if measured performance changed materially, store the new sample
6. run `memory-review` when the change supersedes earlier knowledge

Do **not** write memory merely because code was generated. Validation must come first.

## Security/privacy rules
Never store:
- credentials, tokens, API keys, private keys or connection strings containing secrets
- personal information
- raw conversations or prompts
- unredacted production logs containing sensitive identifiers

The helper rejects common credential patterns, but that is defense-in-depth, not permission to pass secrets to it.

## CLI examples
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/memory_db.py put-fact networking provider FishNet \
  --source Packages/manifest.json --confidence 1.0

python3 ${CLAUDE_SKILL_DIR}/scripts/memory_db.py add-decision ADR-004 \
  "Server authority" "Server validates combat outcomes" \
  "Prevents clients from authoring damage/economy state" \
  --source .claude/unity/decisions/ADR-004-server-authority.md

python3 ${CLAUDE_SKILL_DIR}/scripts/memory_db.py search "server authority"
python3 ${CLAUDE_SKILL_DIR}/scripts/memory_db.py review --stale-days 90
```

Read `resources/memory-policy.md` before bulk writes or migrations.
