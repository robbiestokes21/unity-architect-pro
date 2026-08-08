#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "skills/runtime-debugger"
fixture = json.loads((ROOT / "tests/fixtures/runtime_diagnostics_snapshot.json").read_text())
assert fixture["schemaVersion"] == 1
assert {"stateDiagnostics", "networkDiagnostics", "operations", "metrics"} <= fixture.keys()

contracts = (BASE / "assets/RuntimeDiagnosticsContracts.cs").read_text()
probe = (BASE / "assets/RuntimeStateProbe.cs").read_text()
window = (BASE / "assets/UnityArchitectPro.Editor/RuntimeDebuggerWindow.cs").read_text()
for token in ["IRuntimeStateDiagnostics", "IRuntimeNetworkDiagnostics", "RuntimeOperationRegistry", "Begin", "Complete", "Fail", "Cancel"]: assert token in contracts, token
for token in ["Rigidbody2D", "Animator", "RuntimeOperationRegistry.Snapshot", "Profiler.GetMonoUsedSizeLong", "Application.persistentDataPath", "JsonUtility.ToJson"]: assert token in probe, token
for token in ["EditorApplication.isPlaying", "Selection.activeGameObject", "Temp", "RuntimeStateProbe"]: assert token in window, token
for source in (contracts, probe, window): assert source.count("{") == source.count("}"), "unbalanced braces"
assert window.count("#if UNITY_EDITOR") == window.count("#endif") == 1
print("runtime debugger tests: OK")
