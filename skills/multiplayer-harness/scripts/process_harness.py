#!/usr/bin/env python3
"""Generic local process harness. It intentionally knows nothing about a specific netcode provider.
Pass repeated --process JSON objects with name, command(list), cwd(optional), env(optional), ready_regex(optional).
Useful as a building block; projects should wrap it with provider/project-specific launch arguments.
"""
import argparse,json,subprocess,os,time,re,threading,queue,signal
from pathlib import Path
ap=argparse.ArgumentParser(); ap.add_argument('--process',action='append',default=[]); ap.add_argument('--timeout',type=int,default=120); ap.add_argument('--out',default='Temp/UnityArchitectPro/harness-result.json'); args=ap.parse_args()
specs=[json.loads(x) for x in args.process]; procs=[]; q=queue.Queue(); logs={}; start=time.time()
def reader(name,p):
    for line in iter(p.stdout.readline,''):
        logs[name].append(line.rstrip()); q.put((name,line.rstrip()))
try:
    for s in specs:
        env=os.environ.copy(); env.update({str(k):str(v) for k,v in s.get('env',{}).items()})
        p=subprocess.Popen(s['command'],cwd=s.get('cwd'),env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1)
        procs.append((s,p)); logs[s['name']]=[]; threading.Thread(target=reader,args=(s['name'],p),daemon=True).start()
    ready={s['name']: not s.get('ready_regex') for s in specs}
    while time.time()-start<args.timeout and not all(ready.values()):
        try: name,line=q.get(timeout=.25)
        except queue.Empty:
            if any(p.poll() is not None and p.returncode for _,p in procs): break
            continue
        s=next(x for x in specs if x['name']==name); rr=s.get('ready_regex')
        if rr and re.search(rr,line): ready[name]=True
    result='passed' if all(ready.values()) else 'timeout'
finally:
    for s,p in reversed(procs):
        if p.poll() is None:
            p.terminate()
    for s,p in reversed(procs):
        try:p.wait(timeout=5)
        except subprocess.TimeoutExpired:p.kill()
out={'scenario':'local-process-harness','topology':','.join(s['name'] for s in specs),'result':result,'processes':[{'name':s['name'],'exit_code':p.poll(),'ready':ready.get(s['name'],False),'log_tail':logs[s['name']][-80:]} for s,p in procs],'duration_seconds':round(time.time()-start,3)}
path=Path(args.out); path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(out,indent=2)); print(path); print(result)
