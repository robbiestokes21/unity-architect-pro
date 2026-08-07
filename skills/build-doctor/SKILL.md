---
name: build-doctor
description: Diagnose and validate Unity player and dedicated-server builds across target platforms, including scripting backend, stripping, conditional compilation, platform-only APIs, package/build pipeline issues, headless behavior and CI build failures.
---

# Unity Build Doctor

Establish the exact target, build profile/settings, scripting backend and CI/local invocation before diagnosing.

## Check layers
- C# compile vs player compile differences
- `#if` platform symbols and assembly constraints
- Mono vs IL2CPP, managed stripping/link.xml and reflection
- platform plugin import settings and native libraries
- scenes/build profiles and Addressables/content build dependencies
- headless/dedicated-server exclusions and graphics/audio assumptions
- file paths, permissions and case sensitivity
- build callbacks and custom build pipeline

Prefer reproducible command-line builds for CI problems. Preserve the first useful error; cascading errors are often noise.

For dedicated server builds, verify server bootstrap, no client-only UI/input dependency, graceful shutdown, logs, health/readiness behavior and server credential handling.
