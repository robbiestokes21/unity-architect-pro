#!/usr/bin/env python3
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]; errors=[]
required=['skills/multiplayer-harness/scripts/multiplayer_lab.py','skills/multiplayer-harness/scripts/provider_adapter.py','skills/multiplayer-harness/resources/scenario-schema.json','skills/multiplayer-harness/resources/harness-result-schema.json','skills/multiplayer-harness/resources/provider-adapter-contract.md','skills/multiplayer-harness/resources/adapters/standalone-project-template.json','tests/fixtures/multiplayer_lab_scenario.json','tests/fixtures/fake_multiplayer_peer.py','tests/test_multiplayer_lab.py','skills/multiplayer-harness/resources/fault-injection.md']
for relative in required:
 if not (ROOT/relative).is_file(): errors.append('missing '+relative)
for relative in [required[2],required[3],required[5],required[6]]:
 try: json.loads((ROOT/relative).read_text())
 except Exception as exc: errors.append(relative+': '+str(exc))
lab=(ROOT/required[0]).read_text()
for token in ['startAfterReady','fault_on','teardownCommand','restart','CREATE_NEW_PROCESS_GROUP']:
 if token not in lab: errors.append('lab missing '+token)
if 'shell=True' in lab: errors.append('lab must not use shell=True')
if errors: raise SystemExit('\n'.join('ERROR: '+error for error in errors))
print('Phase 7 validation: OK')
