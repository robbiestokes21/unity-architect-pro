#!/usr/bin/env python3
from pathlib import Path
import json, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]; errors=[]
required=['skills/visual-verification/assets/VisualQaContracts.cs','skills/visual-verification/assets/VisualQaRunner.cs','skills/visual-verification/assets/VisualLayoutAudit.cs','skills/visual-verification/assets/UnityArchitectPro.Editor/QualityGateValidator.cs','skills/visual-verification/resources/visual-result-schema.json','skills/profiler-capture/assets/PerformanceBudgetContracts.cs','skills/profiler-capture/assets/PerformanceBudgetProbe.cs','skills/profiler-capture/resources/performance-result-schema.json','skills/profiler-capture/scripts/compare_performance_reports.py','tests/fixtures/performance_baseline.json','tests/fixtures/performance_current.json','tests/test_visual_performance.py']
for relative in required:
    if not (ROOT/relative).is_file(): errors.append('missing '+relative)
for relative in [required[4],required[7],required[9],required[10]]:
    try: json.loads((ROOT/relative).read_text())
    except Exception as exc: errors.append(relative+': '+str(exc))
runner=(ROOT/'skills/gameplay-tester/assets/GameplayScenarioRunner.cs').read_text()
for token in ['ScenarioStarted','StepStarted','StepCompleted','ScenarioCompleted']:
    if token not in runner: errors.append('gameplay runner missing '+token)
if not errors:
    result=subprocess.run([sys.executable,str(ROOT/'tests/test_visual_performance.py')],capture_output=True,text=True)
    if result.returncode: errors.append(result.stdout+result.stderr)
if errors: raise SystemExit('\n'.join('ERROR: '+error for error in errors))
print('Phase 9-10 validation: OK')
