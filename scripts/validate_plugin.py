#!/usr/bin/env python3
import json, pathlib, subprocess, sys
root=pathlib.Path(__file__).resolve().parents[1]; errors=[]
try:
 meta=json.loads((root/'.claude-plugin/plugin.json').read_text())
 for k in ('name','version','description'):
  if not meta.get(k): errors.append(f'missing plugin metadata: {k}')
except Exception as e: errors.append(f'plugin.json: {e}')
skills=list(root.glob('skills/*/SKILL.md'))
for f in skills:
 t=f.read_text(errors='ignore')
 if not t.startswith('---\n') or '\nname:' not in t[:500] or '\ndescription:' not in t[:1000]: errors.append(f'bad skill frontmatter: {f}')
for f in root.rglob('*.py'):
 try: compile(f.read_text(), str(f), 'exec')
 except Exception as e: errors.append(f'python syntax {f}: {e}')
for bad in list(root.rglob('*.pyc'))+[p for p in root.rglob('__pycache__')]: errors.append(f'generated file present: {bad}')
if not errors:
 result=subprocess.run([sys.executable, str(root/'scripts/validate_phase5.py')], capture_output=True, text=True)
 if result.returncode: errors.append('phase5 validation: '+result.stdout+result.stderr)
if errors:
 print('\n'.join('ERROR: '+e for e in errors)); sys.exit(1)
print(f'OK: {len(skills)} skills, {len(list(root.glob("agents/*.md")))} agents')
