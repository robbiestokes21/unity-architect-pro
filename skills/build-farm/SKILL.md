---
name: "build-farm"
description: "Plan and validate a Unity build matrix for Windows, Linux, macOS, Android, iOS, WebGL and Dedicated Server, including Mono/IL2CPP, architecture, stripping and platform-specific failures. Use for CI matrices or cross-platform shipping readiness."
---
# Build Farm

Treat target-platform builds as independent products. Detect supported targets and project requirements before generating a matrix.

Validate compile, player build, scripting backend, architecture, stripping/AOT, Addressables/content, native plugins, symbols, server subtarget, build size and smoke-launch where executable in the environment. Never claim an iOS/macOS build was validated on an unsupported host.
