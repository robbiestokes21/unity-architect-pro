# Network Budget Template

Do not invent universal numbers. Establish project-specific budgets and measure them.

Record:
- target players per match
- simulation tick rate
- snapshot/send rate
- expected RTT regions
- client upstream bytes/sec
- client downstream bytes/sec
- server aggregate ingress/egress
- maximum reliable messages/sec
- maximum replicated entities/observer
- acceptable prediction correction rate
- acceptable hard reconciliation rate
- server CPU time/tick
- memory/player and memory/match

Estimate a message as:
`payload bytes + framework/transport overhead`, multiplied by frequency and observer count.

The dangerous multiplier is often server egress: one player's update replicated to many observers.
