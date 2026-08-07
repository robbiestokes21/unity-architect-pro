#!/usr/bin/env python3
import argparse,re,json
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('project'); p.add_argument('--json',action='store_true'); a=p.parse_args()
root=Path(a.project).resolve(); assets=root/'Assets'; findings=[]; guid_owner={}
if not assets.exists(): raise SystemExit('Assets directory not found')
for meta in assets.rglob('*.meta'):
    target=Path(str(meta)[:-5])
    if not target.exists(): findings.append({'severity':'warning','type':'orphan-meta','path':str(meta.relative_to(root))})
    try: txt=meta.read_text(errors='replace')
    except: continue
    m=re.search(r'^guid:\s*([0-9a-fA-F]{32})\s*$',txt,re.M)
    if m:
        g=m.group(1).lower()
        if g in guid_owner: findings.append({'severity':'error','type':'duplicate-guid','guid':g,'paths':[guid_owner[g],str(meta.relative_to(root))]})
        else: guid_owner[g]=str(meta.relative_to(root))
for f in assets.rglob('*'):
    if not f.is_file() or f.suffix=='.meta': continue
    if not Path(str(f)+'.meta').exists(): findings.append({'severity':'warning','type':'missing-meta','path':str(f.relative_to(root))})
for f in list(assets.rglob('*.unity'))+list(assets.rglob('*.prefab')):
    try: txt=f.read_text(errors='replace')
    except: continue
    if '<<<<<<<' in txt or '>>>>>>>' in txt or '=======' in txt: findings.append({'severity':'error','type':'merge-marker','path':str(f.relative_to(root))})
    if 'm_Script: {fileID: 0}' in txt: findings.append({'severity':'error','type':'missing-script-reference','path':str(f.relative_to(root))})
out={'project':str(root),'finding_count':len(findings),'findings':findings}
print(json.dumps(out,indent=2) if a.json else '\n'.join([f"{x['severity'].upper()} {x['type']}: {x.get('path',x.get('paths'))}" for x in findings]) or 'No filesystem-level integrity findings.')
