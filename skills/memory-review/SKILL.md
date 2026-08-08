---
name: "memory-review"
description: "Audit Unity Architect Pro project memory for expired, aging, low-confidence, contradictory, superseded, or unresolved engineering knowledge. Use after migrations, package/network changes, large refactors, releases, or whenever remembered context may be stale."
---
# Memory Review

Audit `.claude/unity/project.db` against current source-of-truth project files.

## Workflow
1. Run `project-intelligence` first when project structure/package versions may have changed.
2. Execute the memory review report:
   ```bash
   python3 ../project-memory/scripts/memory_db.py review --stale-days 90
   ```
3. For every expired/aging/low-confidence fact that matters to current work, verify it against source files or runtime/build evidence.
4. Refresh verified facts; mark expired facts stale when no longer trustworthy.
5. Preserve superseded decisions and incidents for historical reasoning.
6. Search for the domain currently being changed and check for contradictory records.
7. Report unresolved memory conflicts rather than choosing whichever record is convenient.

## Never
- delete historical ADRs just because a new one exists
- promote inference confidence without new evidence
- refresh timestamps merely to make a review report clean
- let memory override a current manifest, source file, Unity setting, test, build, or profiler result
