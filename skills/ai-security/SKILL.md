---
name: ai-security
description: Review Unity client/server gameplay and backend integration for trust-boundary vulnerabilities, RPC abuse, authority mistakes, replay/duplication exploits, insecure persistence and sensitive-data exposure. Use for multiplayer, economy, inventory, trading, progression and authentication systems.
---
# Unity Security Engineering

Model trust boundaries first. Assume the client is hostile for competitive/economic state.

Review input vs outcome authority, RPC validation/rate limits, ownership, identity/session binding, replay/idempotency, item/currency transactions, save/cloud tampering, secrets in builds/logs, and server-side validation. Provide severity, exploit preconditions, impact, evidence and remediation. Do not provide cheat implementation instructions.
