# Custom Authoritative Server

Document the protocol before implementation: message IDs/schema, versioning, framing, reliability/order guarantees, authentication, connection handshake, tick/time sync, snapshot strategy, compression, limits and error handling.

Use server authority for canonical state. Treat every client message as untrusted input. Bound message sizes/counts and validate enum/range/ownership/state transitions. Include protocol-version negotiation and backward-compatibility policy.

Plan observability: connection IDs, match/session IDs, structured logs, metrics, tick time, queue depth, bandwidth, disconnect reason and tracing. Define deployment, graceful shutdown, persistence and rolling compatibility.
