---
name: observability
description: Add production-grade Unity client/server observability: structured logs, crash/error context, metrics, traces, session/build identifiers, network diagnostics, privacy-conscious telemetry, and health/readiness signals.
---
# Unity Observability

Design observability around questions operators need to answer. Use structured events with stable names/fields rather than parsing prose logs where possible.

For multiplayer/dedicated servers include build/version, region/allocation/session ID, process role, connected player count, tick health, disconnect reasons and graceful-shutdown state. Never log auth tokens, secrets, full payment data or unnecessary personal data.

Keep high-cardinality labels bounded. Add sampling/rate limits for noisy events. Client telemetry must respect platform/privacy requirements and project consent policy.

Health/readiness are distinct: health means process is alive; readiness means it can accept/join the intended workload.
