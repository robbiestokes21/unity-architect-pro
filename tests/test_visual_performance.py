#!/usr/bin/env python3
from pathlib import Path
import importlib.util, json, sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
module_path=ROOT/'skills/profiler-capture/scripts/compare_performance_reports.py'; spec=importlib.util.spec_from_file_location('compare',module_path); module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
baseline=json.loads((ROOT/'tests/fixtures/performance_baseline.json').read_text()); current=json.loads((ROOT/'tests/fixtures/performance_current.json').read_text())
assert module.compare(baseline,current,10)['verdict']=='passed'
assert module.compare(baseline,current,4)['verdict']=='failed'
different=dict(current); different['scenarioId']='other'; assert module.compare(baseline,different,10)['verdict']=='failed'
visual=(ROOT/'skills/visual-verification/assets/VisualQaRunner.cs').read_text()
for token in ['WaitForEndOfFrame','GetPixels32','ignoreMask','heatmap','UAP_VISUAL_PASS','StepCompleted'] : assert token in visual,token
performance=(ROOT/'skills/profiler-capture/assets/PerformanceBudgetProbe.cs').read_text()
for token in ['warmupFrames','measurementFrames','FrameTimingManager','ProfilerRecorder','p95','UAP_PERFORMANCE_PASS'] : assert token in performance,token
print('visual/performance tests: OK')
