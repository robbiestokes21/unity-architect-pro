#!/usr/bin/env python3
import argparse, re, json
from pathlib import Path

parser=argparse.ArgumentParser(description='Conservatively summarize Unity Editor/Player/server logs.')
parser.add_argument('log')
parser.add_argument('--json', action='store_true')
parser.add_argument('--tail', type=int, default=12000)
args=parser.parse_args()
lines=Path(args.log).read_text(errors='replace').splitlines()[-args.tail:]
pat=re.compile(r'(error|exception|assert|failed|warning|disconnect|timeout|crash)', re.I)
secret=re.compile(r'(?i)(authorization|bearer|token|secret|password|api[_-]?key)(\s*[:=]\s*)(\S+)')
items=[]; seen={}
for i,line in enumerate(lines,1):
    if not pat.search(line): continue
    clean=secret.sub(lambda m:m.group(1)+m.group(2)+'<redacted>', line.strip())
    key=re.sub(r'0x[0-9a-fA-F]+','0x…',clean)
    if key in seen:
        seen[key]['count']+=1; continue
    rec={'line':i,'message':clean,'count':1}; seen[key]=rec; items.append(rec)
result={'source':str(Path(args.log)),'scanned_lines':len(lines),'findings':items[-250:]}
if args.json: print(json.dumps(result,indent=2))
else:
    print(f"Scanned {len(lines)} lines; {len(items)} unique suspicious entries")
    for x in items[-80:]: print(f"[{x['count']}x] {x['message']}")
