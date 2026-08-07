---
name: console-diagnostics
description: Read, classify, deduplicate, and trace Unity Console/Editor.log/player/server logs. Use for compile errors, exceptions, warnings, domain reload problems, build failures, multiplayer disconnects, or runtime regressions.
---
# Console and Log Diagnostics

Always anchor analysis to a time/run boundary so stale errors are not mistaken for current failures.

## Order
1. determine log source: Editor Console, Editor.log, Player.log, server log, test log, build log;
2. isolate the current run/session using timestamps or lifecycle markers;
3. normalize duplicate stack traces and count frequency;
4. classify: compiler, managed exception, native crash, asset import, serialization, package, build pipeline, networking, test, performance warning;
5. identify the first actionable/root error rather than fixing cascades;
6. map stack frames back to project source and package version;
7. reproduce or verify after the fix.

Use `scripts/parse_unity_log.py` when a plain log file is available. Secrets/tokens in logs must be redacted in summaries.

Never treat `Debug.LogError` from an expected negative test as a product defect without checking test context.
