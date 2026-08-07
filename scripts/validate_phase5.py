#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
errors = []
required = [
    "skills/live-editor/assets/UnityArchitectPro.Editor/LiveUnityInspector.cs",
    "skills/live-editor/assets/UnityArchitectPro.Editor/SerializedPropertyMutation.cs",
    "skills/live-editor/resources/live-inspector-contract.md",
    "skills/live-inspector/SKILL.md",
    "agents/unity-inspector-analyst.md",
    "tests/fixtures/live_inspector_report.json",
]
for relative in required:
    if not (ROOT / relative).is_file(): errors.append("missing " + relative)
try:
    fixture = json.loads((ROOT / "tests/fixtures/live_inspector_report.json").read_text())
    if fixture.get("schemaVersion") != 1: errors.append("fixture schemaVersion must be 1")
except Exception as exc: errors.append("fixture: " + str(exc))
for relative in required[:2]:
    source = (ROOT / relative).read_text()
    if source.count("#if UNITY_EDITOR") != 1 or source.count("#endif") != 1: errors.append(relative + " must be Editor guarded")
    if source.count("{") != source.count("}"): errors.append(relative + " has unbalanced braces")
if errors:
    raise SystemExit("\n".join("ERROR: " + error for error in errors))
print("Phase 5 validation: OK")
