#!/usr/bin/env python3
"""Generate a conservative Unity project index with no Unity dependency."""
from __future__ import annotations
import json, os, re, sys
from pathlib import Path

if len(sys.argv) != 2:
    print("usage: index_unity_project.py <unity-project-root>", file=sys.stderr); sys.exit(2)
root = Path(sys.argv[1]).resolve()
if not (root / "ProjectSettings" / "ProjectVersion.txt").exists():
    print("Not a Unity project: ProjectSettings/ProjectVersion.txt missing", file=sys.stderr); sys.exit(3)

def read_json(path: Path):
    try: return json.loads(path.read_text(encoding="utf-8"))
    except Exception: return None

pv = (root / "ProjectSettings" / "ProjectVersion.txt").read_text(encoding="utf-8", errors="replace")
m = re.search(r"m_EditorVersion:\s*(.+)", pv)
unity_version = m.group(1).strip() if m else "unknown"
manifest = read_json(root / "Packages" / "manifest.json") or {}
lock = read_json(root / "Packages" / "packages-lock.json") or {}
deps = manifest.get("dependencies", {}) if isinstance(manifest, dict) else {}

skip = {"Library", "Temp", "Logs", "Obj", "Build", "Builds", ".git", ".idea", ".vs"}
def walk_files(suffix):
    out=[]
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in skip]
        for f in fns:
            if f.endswith(suffix): out.append(str((Path(dp)/f).relative_to(root)).replace("\\","/"))
    return sorted(out)

asmdefs = []
for rel in walk_files(".asmdef"):
    data = read_json(root / rel)
    asmdefs.append({"path": rel, "name": data.get("name") if isinstance(data, dict) else None,
                    "references": data.get("references", []) if isinstance(data, dict) else []})

packages_lower = {k.lower(): v for k,v in deps.items()}
def has(*needles): return any(any(n in k for n in needles) for k in packages_lower)
network_hints=[]
for label, needles in {
    "Netcode for GameObjects": ("com.unity.netcode.gameobjects",),
    "Netcode for Entities": ("com.unity.netcode", "com.unity.entities"),
    "Unity Multiplayer Services": ("com.unity.services.multiplayer",),
    "Mirror": ("mirror",), "FishNet": ("fishnet",), "Photon": ("photon",),
    "Steamworks": ("steamworks", "facepunch"), "EOS": ("epic", "eos"), "PlayFab": ("playfab",)
}.items():
    if has(*needles): network_hints.append(label)

index = {
  "schema": 1,
  "unityVersion": unity_version,
  "packages": deps,
  "lockDependenciesPresent": bool(lock.get("dependencies")) if isinstance(lock, dict) else False,
  "assemblyDefinitions": asmdefs,
  "scenes": walk_files(".unity"),
  "prefabsCount": len(walk_files(".prefab")),
  "scriptCount": len(walk_files(".cs")),
  "testAssemblyHints": [a for a in asmdefs if a.get("name") and "test" in a["name"].lower()],
  "stackHints": {
    "urp": has("com.unity.render-pipelines.universal"),
    "hdrp": has("com.unity.render-pipelines.high-definition"),
    "inputSystem": has("com.unity.inputsystem"),
    "addressables": has("com.unity.addressables"),
    "entities": has("com.unity.entities"),
    "networking": network_hints,
  }
}
print(json.dumps(index, indent=2, sort_keys=True))
