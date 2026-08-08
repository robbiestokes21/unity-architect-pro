#!/usr/bin/env python3
"""Render a project/provider launch descriptor into a Phase 7 scenario file."""
import argparse, json
from pathlib import Path


def render(value, variables):
    if isinstance(value, str):
        for key, replacement in variables.items(): value = value.replace("${"+key+"}", str(replacement))
        if "${" in value: raise ValueError("unresolved adapter variable in "+value)
        return value
    if isinstance(value, list): return [render(item, variables) for item in value]
    if isinstance(value, dict): return {key: render(item, variables) for key, item in value.items()}
    return value


parser=argparse.ArgumentParser()
parser.add_argument("adapter",type=Path); parser.add_argument("--var",action="append",default=[]); parser.add_argument("--out",type=Path,required=True)
args=parser.parse_args(); variables={}
for item in args.var:
    if "=" not in item: raise SystemExit("--var uses KEY=VALUE")
    key,value=item.split("=",1); variables[key]=value
adapter=json.loads(args.adapter.read_text(encoding="utf-8"))
scenario=render(adapter["scenarioTemplate"],variables)
scenario["adapter"]={"name":adapter["name"],"provider":adapter["provider"],"requiresProjectBootstrap":adapter.get("requiresProjectBootstrap",True)}
args.out.parent.mkdir(parents=True,exist_ok=True); args.out.write_text(json.dumps(scenario,indent=2),encoding="utf-8"); print(args.out)
