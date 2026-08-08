#!/usr/bin/env python3
import argparse, json
from pathlib import Path

def validate(document):
    errors=[]
    if document.get('schemaVersion') != 1: errors.append('schemaVersion must be 1')
    if not str(document.get('id','')).strip(): errors.append('id is required')
    steps=document.get('steps')
    if not isinstance(steps,list) or not steps: return errors+['steps must be a non-empty array']
    seen=set()
    for index,step in enumerate(steps):
        prefix=f'steps[{index}]'
        step_id=step.get('id') if isinstance(step,dict) else None
        if not step_id: errors.append(prefix+'.id is required')
        elif step_id in seen: errors.append(prefix+'.id is duplicated: '+step_id)
        else: seen.add(step_id)
        for label,operation in [('action',step.get('action'))]+[(f'assertions[{i}]',v) for i,v in enumerate(step.get('assertions',[]))]:
            if not isinstance(operation,dict): errors.append(prefix+'.'+label+' is required'); continue
            if not operation.get('adapter'): errors.append(prefix+'.'+label+'.adapter is required')
            if not operation.get('kind'): errors.append(prefix+'.'+label+'.kind is required')
            if float(operation.get('timeoutSeconds',1)) <= 0: errors.append(prefix+'.'+label+'.timeoutSeconds must be positive')
    return errors

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('scenario',type=Path); args=parser.parse_args()
    try: document=json.loads(args.scenario.read_text(encoding='utf-8'))
    except Exception as exc: raise SystemExit('invalid JSON: '+str(exc))
    errors=validate(document)
    if errors: raise SystemExit('\n'.join('ERROR: '+error for error in errors))
    print('Gameplay scenario validation: OK')

if __name__ == '__main__': main()
