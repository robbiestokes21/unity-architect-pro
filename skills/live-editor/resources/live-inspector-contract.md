# Live Inspector contract

Phase 5 emits JSON evidence under `Temp/UnityArchitectPro/`; it never writes inspection output into `Assets/`.

## Coverage

- loaded-scene hierarchy, arbitrary components and visible `SerializedProperty` values
- prefab source and per-component property override counts
- cameras, layers, tags and sorting layers
- Input System action assets when the package is installed
- Animator controllers, layers and state machines
- NavMesh data and navigation project settings
- lights, lighting settings, volume profiles and volume components
- current render pipeline plus graphics, quality, physics/2D physics and other project settings

Package-owned types are discovered by asset type/name and inspected through `SerializedObject`; the template therefore has no hard dependency on Input System, AI Navigation, URP or HDRP assemblies.

## Mutation request

Create `Temp/UnityArchitectPro/property-mutation-request.json`, then run **Tools > Unity Architect Pro > Live Inspector > Apply Serialized Property Request**. Obtain `targetGlobalObjectId`, `propertyPath`, and exact `expectedValue` from a fresh inspection.

```json
{
  "schemaVersion": 1,
  "targetGlobalObjectId": "GlobalObjectId_V1-...",
  "propertyPath": "m_Enabled",
  "expectedValue": "True",
  "value": "false",
  "objectReferenceAssetPath": "",
  "allowProjectSettings": false
}
```

Safety properties: optimistic expected-value check, stable global object identity, one property per request, supported scalar/vector/reference types only, `m_Script`/arrays/managed references blocked, `Undo` recording, dirty-scene tracking, save, and read-back logging. Project settings are denied unless the request explicitly opts in. Review diffs and keep source control available before project-setting changes.
