#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
errors = []
required = [
    "skills/runtime-debugger/assets/RuntimeDiagnosticsContracts.cs",
    "skills/runtime-debugger/assets/RuntimeStateProbe.cs",
    "skills/runtime-debugger/assets/UnityArchitectPro.Editor/RuntimeDebuggerWindow.cs",
    "skills/runtime-debugger/resources/runtime-diagnostics-contract.md",
    "agents/runtime-debugger-analyst.md",
    "tests/fixtures/runtime_diagnostics_snapshot.json",
]
for relative in required:
    if not (ROOT / relative).is_file(): errors.append("missing " + relative)
try:
    fixture = json.loads((ROOT / "tests/fixtures/runtime_diagnostics_snapshot.json").read_text())
    if fixture.get("schemaVersion") != 1: errors.append("runtime fixture schemaVersion must be 1")
except Exception as exc: errors.append("runtime fixture: " + str(exc))
for relative in required[:3]:
    source = (ROOT / relative).read_text()
    if source.count("{") != source.count("}"): errors.append(relative + " has unbalanced braces")
if errors: raise SystemExit("\n".join("ERROR: " + error for error in errors))
print("Phase 6 validation: OK")
