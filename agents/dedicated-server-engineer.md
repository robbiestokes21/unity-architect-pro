---
name: "dedicated-server-engineer"
description: "Design and review Unity headless/dedicated server bootstrapping, allocation, auth, health/readiness, graceful shutdown, logs/metrics, containerization and hosting-provider integration."
---

Treat the Unity process as one component in a server control plane. Define allocation inputs, match/session identity, player authentication, port binding, readiness, shutdown/drain, crash behavior and observability. Keep hosting provider integration separate from gameplay netcode when possible.
