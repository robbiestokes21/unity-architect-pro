---
name: "gameplay-ai"
description: "Architect and implement Unity gameplay AI: finite/hierarchical state machines, behavior trees, utility AI, perception, navigation, steering, combat decisions, spawning, LOD, and multiplayer authority. Use for NPC/enemy/companion AI systems."
---
# Gameplay AI Engineering

Pick architecture from behavior complexity and scale rather than preference. Keep sensing, decision, action and presentation separable enough to test.

For many agents, budget perception queries, path requests, physics and animation work; stagger or schedule expensive work instead of running every decision every frame. Use pooling for frequently spawned agents and explicit cancellation when agents despawn or scenes unload.

Navigation must account for the project's actual navigation stack/package/version. Do not invent NavMesh APIs. For networked AI, canonical decisions belong on the authoritative simulation; replicate compact intent/state needed for presentation rather than running competing decision systems on every client.

Tests should cover deterministic decision inputs where possible, blocked/unreachable navigation, target loss, interruption, death/despawn and multiplayer late-join state reconstruction.
