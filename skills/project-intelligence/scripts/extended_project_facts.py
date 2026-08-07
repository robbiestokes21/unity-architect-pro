#!/usr/bin/env python3
import json,re,argparse
from pathlib import Path
ap=argparse.ArgumentParser(); ap.add_argument('project'); args=ap.parse_args(); root=Path(args.project).resolve()
facts={'project':str(root),'unity_version':None,'packages':{},'counts':{},'signals':{}}
pv=root/'ProjectSettings/ProjectVersion.txt'
if pv.exists():
    m=re.search(r'm_EditorVersion:\s*(.+)',pv.read_text(errors='replace')); facts['unity_version']=m.group(1).strip() if m else None
manifest=root/'Packages/manifest.json'
if manifest.exists():
    try:facts['packages']=json.loads(manifest.read_text()).get('dependencies',{})
    except:pass
assets=root/'Assets'
for ext,key in [('.cs','scripts'),('.asmdef','asmdefs'),('.unity','scenes'),('.prefab','prefabs'),('.shader','shaders'),('.compute','compute_shaders')]: facts['counts'][key]=sum(1 for _ in assets.rglob('*'+ext)) if assets.exists() else 0
pk=' '.join(facts['packages'])
facts['signals']={
 'input_system':'com.unity.inputsystem' in facts['packages'], 'addressables':'com.unity.addressables' in facts['packages'],
 'entities':'com.unity.entities' in facts['packages'], 'ngo':'com.unity.netcode.gameobjects' in facts['packages'],
 'nfe': any('netcode' in x and 'entities' in x for x in facts['packages']), 'multiplayer_playmode':'com.unity.multiplayer.playmode' in facts['packages'],
 'multiplayer_tools':'com.unity.multiplayer.tools' in facts['packages'], 'mps_sdk':'com.unity.services.multiplayer' in facts['packages']}
print(json.dumps(facts,indent=2))
