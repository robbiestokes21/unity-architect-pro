#!/usr/bin/env python3
from pathlib import Path
import json, subprocess, tempfile
ROOT=Path(__file__).resolve().parents[1]; SCANNER=ROOT/'skills/dependency-graph/scripts/scan_dependencies.py'
with tempfile.TemporaryDirectory() as td:
    p=Path(td)
    for x in ['Assets/Scenes','Assets/Data','Assets/Scripts','ProjectSettings']:(p/x).mkdir(parents=True,exist_ok=True)
    (p/'ProjectSettings/EditorBuildSettings.asset').write_text('m_Scenes:\n- enabled: 1\n  path: Assets/Scenes/Main.unity\n')
    files={
      'Assets/Scenes/Main.unity.meta':'guid: 11111111111111111111111111111111\n','Assets/Data/Config.asset.meta':'guid: 22222222222222222222222222222222\n','Assets/Data/Unused.asset.meta':'guid: 33333333333333333333333333333333\n',
      'Assets/Scenes/Main.unity':'--- !u!1 &1\nThing: {fileID: 11400000, guid: 22222222222222222222222222222222, type: 2}\n','Assets/Data/Config.asset':'--- !u!114 &11400000\n','Assets/Data/Unused.asset':'--- !u!114 &11400001\n',
      'Assets/Scripts/A.asmdef':json.dumps({'name':'A','references':['B']}),'Assets/Scripts/A.asmdef.meta':'guid: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n','Assets/Scripts/B.asmdef':json.dumps({'name':'B','references':['A']}),'Assets/Scripts/B.asmdef.meta':'guid: bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n'}
    for path,text in files.items():(p/path).write_text(text)
    d=json.loads(subprocess.check_output(['python3',str(SCANNER),str(p),'--target','Assets/Data/Config.asset','--json'],text=True))
    assert d['stats']['asmdefCycles']>=1
    assert any(x['id']=='Assets/Scenes/Main.unity' for x in d['impact']['directDependents'])
    assert any(x['path']=='Assets/Data/Unused.asset' for x in d['reachability']['unusedCandidates'])
    assert not any(x['path']=='Assets/Data/Config.asset' for x in d['reachability']['unusedCandidates'])
print('dependency graph tests: OK')
