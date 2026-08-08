#!/usr/bin/env python3
from pathlib import Path
import json, subprocess, sys, tempfile

ROOT=Path(__file__).resolve().parents[1]
validator=ROOT/'skills/gameplay-tester/scripts/validate_gameplay_scenario.py'
fixture=ROOT/'tests/fixtures/gameplay_scenario.json'
subprocess.check_call([sys.executable,str(validator),str(fixture)])
with tempfile.TemporaryDirectory() as directory:
    bad=json.loads(fixture.read_text()); bad['steps'].append(dict(bad['steps'][0])); path=Path(directory)/'bad.json'; path.write_text(json.dumps(bad))
    completed=subprocess.run([sys.executable,str(validator),str(path)],capture_output=True,text=True)
    assert completed.returncode != 0 and 'duplicated' in completed.stderr
runner=(ROOT/'skills/gameplay-tester/assets/GameplayScenarioRunner.cs').read_text()
for token in ['UAP_GAMEPLAY_READY','UAP_TEST_COMPLETE','UAP_TEST_FAILED','CaptureScreenshot','ResetAdapter','Random.InitState']:
    assert token in runner, token
contracts=(ROOT/'skills/gameplay-tester/assets/GameplayTestContracts.cs').read_text()
assert 'IGameplayTestAdapter' in contracts and 'CaptureState' in contracts
adapter=(ROOT/'skills/gameplay-tester/assets/TransformGameplayTestAdapter.cs').read_text()
assert 'void CaptureState(' in adapter and 'ICollection<GameplayStateValue>' in adapter
print('gameplay testing tests: OK')
