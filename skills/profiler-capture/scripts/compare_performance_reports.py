#!/usr/bin/env python3
import argparse, json
from pathlib import Path

def metrics(report): return {item['name']:item for item in report.get('metrics',[])}
def compare(baseline,current,maximum_regression):
    old,new=metrics(baseline),metrics(current); comparisons=[]; errors=[]; passed=current.get('verdict')=='passed'
    for key in ('scenarioId','platform','qualityLevel'):
        if baseline.get(key) and current.get(key) and baseline[key] != current[key]: errors.append(f'{key} differs: {baseline[key]} != {current[key]}')
    passed=passed and not errors
    for name,item in new.items():
        if name not in old: continue
        before=float(old[name].get('p95',0)); after=float(item.get('p95',0)); percent=0 if before == 0 else (after-before)/before*100
        ok=percent <= maximum_regression; passed=passed and ok
        comparisons.append({'name':name,'baselineP95':before,'currentP95':after,'regressionPercent':percent,'passed':ok})
    return {'schemaVersion':1,'verdict':'passed' if passed else 'failed','maximumRegressionPercent':maximum_regression,'metadataErrors':errors,'comparisons':comparisons}
def main():
    parser=argparse.ArgumentParser(); parser.add_argument('baseline',type=Path); parser.add_argument('current',type=Path); parser.add_argument('--maximum-regression-percent',type=float,default=10); parser.add_argument('--out',type=Path); args=parser.parse_args()
    result=compare(json.loads(args.baseline.read_text()),json.loads(args.current.read_text()),args.maximum_regression_percent)
    payload=json.dumps(result,indent=2); args.out.write_text(payload+'\n') if args.out else print(payload)
    raise SystemExit(0 if result['verdict']=='passed' else 1)
if __name__=='__main__': main()
