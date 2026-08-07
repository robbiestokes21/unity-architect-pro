# Dependency graph evidence model

**Authoritative:** GUID references physically present in text-serialized Unity assets, explicit `.asmdef` references, and GUID ownership from `.meta` files.

**Inferred:** default Assembly-CSharp membership and runtime-root classification from Unity conventions.

**Heuristic:** namespace imports, text/path signals, and static reachability cleanup candidates.

Static graphing can miss `Resources.Load` strings, Addressables keys/labels and remote catalogs, AssetBundles, reflection/type-name strings, JSON/config-driven paths, DI registration, mods/plugins, platform-specific code, generated code, and runtime downloads. Use live Editor/runtime inspection and tests when these mechanisms exist.
