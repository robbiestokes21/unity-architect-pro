---
name: "addressables"
description: "Design, implement, review and debug Unity Addressables usage including groups, labels, catalogs, remote content, content updates, dependency duplication, AsyncOperationHandle lifetime, scene loading and memory release."
---

# Unity Addressables Engineer

First verify `com.unity.addressables` is installed and its version.

## Core rules
- Every acquired handle needs an intentional owner and release path.
- Do not release a handle while consumers still depend on its asset/result.
- Distinguish asset lifetime from instantiated-object lifetime.
- Avoid hidden duplicate dependencies across bundles/groups.
- Treat remote catalog/content updates as a deployment/versioning system, not a file-loading trick.
- Make cancellation semantics explicit: stopping a caller does not automatically cancel underlying Addressables work.
- For scenes, define activation and unload ownership deliberately.

When diagnosing memory, correlate Addressables handles with Memory Profiler evidence rather than assuming `Release` immediately frees all memory.
