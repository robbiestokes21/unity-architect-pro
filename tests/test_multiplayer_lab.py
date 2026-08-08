#!/usr/bin/env python3
from pathlib import Path
import json, subprocess, sys, tempfile

ROOT=Path(__file__).resolve().parents[1]; LAB=ROOT/'skills/multiplayer-harness/scripts/multiplayer_lab.py'; ADAPTER=ROOT/'skills/multiplayer-harness/scripts/provider_adapter.py'; FIXTURE=ROOT/'tests/fixtures/multiplayer_lab_scenario.json'; PEER=ROOT/'tests/fixtures/fake_multiplayer_peer.py'
with tempfile.TemporaryDirectory() as td:
    temp=Path(td); scenario=json.loads(FIXTURE.read_text()); scenario['variables']={'PYTHON':sys.executable,'PEER':str(PEER)}
    scenario_path=temp/'scenario.json'; scenario_path.write_text(json.dumps(scenario)); result_path=temp/'result.json'
    completed=subprocess.run([sys.executable,str(LAB),str(scenario_path),'--out',str(result_path)],text=True,capture_output=True,timeout=15)
    assert completed.returncode==0, completed.stdout+completed.stderr
    result=json.loads(result_path.read_text()); assert result['schemaVersion']==2 and result['result']=='passed'
    peers={item['name']:item for item in result['processes']}; assert peers['server']['ready']; assert peers['client-1']['generation']==2; assert peers['client-2']['ready'] and peers['client-2']['completed']
    assert [item['type'] for item in result['actions']]==['start','restart'] and not result['failures']
    adapter_out=temp/'adapter.json'; adapter=ROOT/'skills/multiplayer-harness/resources/adapters/standalone-project-template.json'
    subprocess.check_call([sys.executable,str(ADAPTER),str(adapter),'--var','SCENARIO=fixture','--var','SERVER_EXE=server','--var','CLIENT_EXE=client','--var','PORT=7777','--out',str(adapter_out)])
    assert json.loads(adapter_out.read_text())['adapter']['requiresProjectBootstrap'] is True
print('multiplayer lab tests: OK')
