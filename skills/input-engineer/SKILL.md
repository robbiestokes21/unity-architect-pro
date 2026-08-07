---
name: input-engineer
description: Design, implement, migrate, and debug Unity input using the installed Input System or legacy input. Covers action maps, rebinding, devices, multiplayer local users, UI input, persistence, and generated wrappers.
---
# Unity Input Engineering

Detect whether `com.unity.inputsystem` is installed and whether the project uses generated C# wrappers, PlayerInput, InputUser, direct InputAction references, or legacy Input Manager. Do not mix approaches casually.

Define action semantics before bindings. Separate gameplay/UI maps where useful, handle device hot-plug, disable/unsubscribe correctly, and make rebind persistence versionable. Avoid reading input from authoritative server builds unless intentionally supporting server-side simulation/testing.

For local multiplayer, explicitly model user-device pairing. For online multiplayer, transmit sanitized gameplay intent, not raw device objects or client-authoritative results.
