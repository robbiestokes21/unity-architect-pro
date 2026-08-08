#!/usr/bin/env python3
from pathlib import Path
import json, subprocess, sys

ROOT=Path(__file__).resolve().parents[1]; errors=[]
required=['skills/gameplay-tester/assets/GameplayTestContracts.cs','skills/gameplay-tester/assets/GameplayScenarioRunner.cs','skills/gameplay-tester/assets/TransformGameplayTestAdapter.cs','skills/gameplay-tester/assets/UnityArchitectPro.Editor/GameplayScenarioValidator.cs','skills/gameplay-tester/resources/gameplay-scenario-schema.json','skills/gameplay-tester/resources/gameplay-result-schema.json','skills/gameplay-tester/resources/gameplay-adapter-contract.md','skills/gameplay-tester/scripts/validate_gameplay_scenario.py','skills/gameplay-tester/examples/player-movement.json','tests/fixtures/gameplay_scenario.json','tests/test_gameplay_testing.py','agents/gameplay-qa-operator.md']
for relative in required:
    if not (ROOT/relative).is_file(): errors.append('missing '+relative)
for relative in [required[4],required[5],required[8],required[9]]:
    try: json.loads((ROOT/relative).read_text())
    except Exception as exc: errors.append(relative+': '+str(exc))
if not errors:
    result=subprocess.run([sys.executable,str(ROOT/'tests/test_gameplay_testing.py')],capture_output=True,text=True)
    if result.returncode: errors.append(result.stdout+result.stderr)
if errors: raise SystemExit('\n'.join('ERROR: '+error for error in errors))
print('Phase 8 validation: OK')
