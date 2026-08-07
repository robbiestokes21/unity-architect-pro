#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "skills/live-editor/assets/UnityArchitectPro.Editor"
REPORT = json.loads((ROOT / "tests/fixtures/live_inspector_report.json").read_text())

assert REPORT["schemaVersion"] == 1
assert {"hierarchy", "cameras", "animators", "lighting", "settings", "assets"} <= REPORT.keys()

inspector = (ASSETS / "LiveUnityInspector.cs").read_text()
mutation = (ASSETS / "SerializedPropertyMutation.cs").read_text()
for required in ["SerializedObject", "PrefabUtility.GetPropertyModifications", "modification.propertyPath", "PackageInfo.GetAllRegisteredPackages", "t:InputActionAsset", "AnimatorController", "t:NavMeshData", "t:VolumeProfile", "PhysicsManager.asset", "GraphicsSettings.currentRenderPipeline", "SortingLayer.layers"]:
    assert required in inspector, required
for required in ["expectedValue", "Undo.RecordObject", "ApplyModifiedProperties", "GlobalObjectId", "allowProjectSettings", "m_Script", "AssetDatabase.SaveAssets"]:
    assert required in mutation, required
for source in (inspector, mutation):
    assert source.count("#if UNITY_EDITOR") == source.count("#endif") == 1
    assert source.count("{") == source.count("}"), "unbalanced braces"
print("live inspector tests: OK")
