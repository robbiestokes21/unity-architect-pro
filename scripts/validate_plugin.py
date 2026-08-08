#!/usr/bin/env python3
import json, pathlib, re, subprocess, sys
root=pathlib.Path(__file__).resolve().parents[1]; errors=[]
try:
 meta=json.loads((root/'.claude-plugin/plugin.json').read_text())
 for k in ('name','version','description'):
  if not meta.get(k): errors.append(f'missing plugin metadata: {k}')
except Exception as e: errors.append(f'plugin.json: {e}')
skills=list(root.glob('skills/*/SKILL.md'))
agents=list(root.glob('agents/*.md'))
for f in skills+agents:
 t=f.read_text(encoding='utf-8', errors='replace')
 kind='skill' if f in skills else 'agent'
 if not t.startswith('---\n'):
  errors.append(f'bad {kind} frontmatter (must start on line 1): {f}'); continue
 parts=t.split('---', 2)
 if len(parts)<3:
  errors.append(f'bad {kind} frontmatter (missing closing delimiter): {f}'); continue
 fields={}
 for line in parts[1].splitlines():
  if not line.strip(): continue
  if ':' not in line:
   errors.append(f'bad {kind} frontmatter line: {f}: {line}'); continue
  key,value=line.split(':',1)
  value=value.strip()
  try: fields[key.strip()]=json.loads(value)
  except json.JSONDecodeError as e:
   # YAML permits conservative unquoted plain scalars such as `model: inherit`.
   if re.fullmatch(r'[A-Za-z0-9_.-]+', value): fields[key.strip()]=value
   else: errors.append(f'bad {kind} YAML scalar: {f}: {key.strip()}: {e}')
 for key in ('name','description'):
  if not isinstance(fields.get(key),str) or not fields[key].strip(): errors.append(f'bad {kind} frontmatter {key}: {f}')
for f in root.rglob('*.py'):
 try: compile(f.read_text(), str(f), 'exec')
 except Exception as e: errors.append(f'python syntax {f}: {e}')
for bad in list(root.rglob('*.pyc'))+[p for p in root.rglob('__pycache__')]: errors.append(f'generated file present: {bad}')
if not errors:
 result=subprocess.run([sys.executable, str(root/'scripts/validate_phase5.py')], capture_output=True, text=True)
 if result.returncode: errors.append('phase5 validation: '+result.stdout+result.stderr)
if not errors:
 result=subprocess.run([sys.executable, str(root/'scripts/validate_phase6.py')], capture_output=True, text=True)
 if result.returncode: errors.append('phase6 validation: '+result.stdout+result.stderr)
if not errors:
 result=subprocess.run([sys.executable, str(root/'scripts/validate_phase7.py')], capture_output=True, text=True)
 if result.returncode: errors.append('phase7 validation: '+result.stdout+result.stderr)
if not errors:
 result=subprocess.run([sys.executable, str(root/'scripts/validate_phase8.py')], capture_output=True, text=True)
 if result.returncode: errors.append('phase8 validation: '+result.stdout+result.stderr)
if errors:
 print('\n'.join('ERROR: '+e for e in errors)); sys.exit(1)
print(f'OK: {len(skills)} skills, {len(agents)} agents')
