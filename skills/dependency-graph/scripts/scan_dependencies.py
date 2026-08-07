#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, os, re, sys
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
from pathlib import Path

GUID_RE=re.compile(r'\bguid:\s*([0-9a-fA-F]{32})\b')
META_GUID_RE=re.compile(r'^guid:\s*([0-9a-fA-F]{32})\s*$',re.M)
ASM_GUID_REF_RE=re.compile(r'^GUID:([0-9a-fA-F]{32})$')
CS_NAMESPACE_RE=re.compile(r'^\s*namespace\s+([A-Za-z_][\w.]*)',re.M)
CS_USING_RE=re.compile(r'^\s*using\s+([A-Za-z_][\w.]*)\s*;',re.M)
CS_TYPE_RE=re.compile(r'\b(?:class|struct|interface|record|enum)\s+([A-Za-z_][\w]*)')
SERIALIZED_EXTS={'.unity','.prefab','.asset','.mat','.anim','.controller','.overridecontroller','.playable','.mask','.physicmaterial','.physicsmaterial2d','.rendertexture','.spriteatlas','.terrainlayer','.guiskin','.lighting','.preset','.inputactions'}
SKIP_DIRS={'Library','Temp','Logs','Obj','Build','Builds','.git','.idea','.vs','UserSettings'}

def norm(p): return str(p).replace('\\','/')
def rel(root,p):
    try:return norm(p.resolve().relative_to(root.resolve()))
    except:return norm(p)
def read_text(p):
    try:return p.read_text(encoding='utf-8',errors='replace')
    except:return ''
def read_json(p):
    try:return json.loads(p.read_text(encoding='utf-8'))
    except:return None
def walk(root):
    for dp,dns,fns in os.walk(root):
        dns[:]=[d for d in dns if d not in SKIP_DIRS]
        for n in fns: yield Path(dp)/n
def kind(path):
    e=Path(path).suffix.lower()
    return {'.unity':'scene','.prefab':'prefab','.cs':'script','.asmdef':'asmdef','.asmref':'asmref','.asset':'asset','.shader':'shader','.shadergraph':'shader','.compute':'shader','.mat':'material','.png':'texture','.jpg':'texture','.jpeg':'texture','.tga':'texture','.psd':'texture','.fbx':'model','.obj':'model','.wav':'audio','.mp3':'audio','.ogg':'audio','.anim':'animation','.controller':'animation'}.get(e,e[1:] if e else 'file')

@dataclass
class Finding:
    severity:str; type:str; message:str; path:str|None=None; evidence:dict|None=None

class Graph:
    def __init__(self,root,code_heuristics=False):
        self.root=Path(root).resolve(); self.code_heuristics=code_heuristics
        self.nodes={}; self.edges=[]; self.edge_keys=set(); self.guid_to_path={}; self.path_to_guid={}; self.findings=[]; self.roots=defaultdict(list); self.asm_name_to_path={}; self.asm_guid_to_name={}
    def node(self,i,**attrs):
        n=self.nodes.setdefault(i,{'id':i}); n.update({k:v for k,v in attrs.items() if v is not None})
    def edge(self,s,t,typ,confidence='authoritative',**attrs):
        k=(s,t,typ,confidence)
        if k in self.edge_keys:return
        self.edge_keys.add(k); e={'source':s,'target':t,'type':typ,'confidence':confidence}; e.update({k:v for k,v in attrs.items() if v is not None}); self.edges.append(e)
    def discover_assets(self):
        for base in [self.root/'Assets',self.root/'Packages']:
            if not base.exists():continue
            for f in walk(base):
                if f.name.endswith('.meta'):continue
                rp=rel(self.root,f)
                try:size=f.stat().st_size
                except:size=None
                self.node(rp,kind=kind(rp),path=rp,size=size,source='filesystem')
        assets=self.root/'Assets'
        if not assets.exists(): self.findings.append(Finding('error','missing-assets-directory','Assets directory is missing')); return
        for meta in assets.rglob('*.meta'):
            m=META_GUID_RE.search(read_text(meta))
            if not m:continue
            g=m.group(1).lower(); target=Path(str(meta)[:-5]); rp=rel(self.root,target)
            if g in self.guid_to_path and self.guid_to_path[g]!=rp:self.findings.append(Finding('error','duplicate-guid',f'GUID {g} is owned by multiple assets',rp,{'guid':g,'paths':[self.guid_to_path[g],rp]}))
            else:self.guid_to_path[g]=rp; self.path_to_guid[rp]=g; self.node(rp,guid=g)
            if not target.exists():self.findings.append(Finding('warning','orphan-meta','Meta file has no matching asset',rel(self.root,meta)))
        for rp in list(self.nodes):
            if rp.startswith('Assets/') and rp not in self.path_to_guid:self.findings.append(Finding('warning','missing-meta','Asset has no .meta file',rp))
    def serialized_edges(self):
        for rp,n in list(self.nodes.items()):
            p=self.root/rp
            if not p.is_file() or p.suffix.lower() not in SERIALIZED_EXTS:continue
            txt=read_text(p)
            if 'm_Script: {fileID: 0}' in txt:self.findings.append(Finding('error','missing-script-reference','Serialized object contains m_Script fileID 0',rp))
            for g in sorted(set(x.lower() for x in GUID_RE.findall(txt))):
                t=self.guid_to_path.get(g)
                if t:self.edge(rp,t,'serialized-guid','authoritative',guid=g)
                else:
                    t='guid:'+g; self.node(t,kind='missing-guid',guid=g); self.edge(rp,t,'serialized-guid','authoritative',guid=g); self.findings.append(Finding('error','missing-guid-reference',f'Serialized asset references GUID {g}, but no matching Assets/*.meta was found',rp,{'guid':g}))
    def assembly_edges(self):
        defs=[]
        for rp,n in list(self.nodes.items()):
            if n.get('kind')!='asmdef':continue
            d=read_json(self.root/rp)
            if not isinstance(d,dict):self.findings.append(Finding('error','invalid-asmdef','Could not parse asmdef JSON',rp));continue
            name=d.get('name') or rp; self.asm_name_to_path[name]=rp
            if self.path_to_guid.get(rp):self.asm_guid_to_name[self.path_to_guid[rp]]=name
            self.node(rp,assemblyName=name,autoReferenced=d.get('autoReferenced',True),includePlatforms=d.get('includePlatforms',[]),excludePlatforms=d.get('excludePlatforms',[])); defs.append((rp,d))
        for rp,d in defs:
            for rv in d.get('references',[]) or []:
                m=ASM_GUID_REF_RE.match(rv) if isinstance(rv,str) else None; name=self.asm_guid_to_name.get(m.group(1).lower()) if m else rv if isinstance(rv,str) else None; tp=self.asm_name_to_path.get(name)
                if tp:self.edge(rp,tp,'asmdef-reference','authoritative',assembly=name)
                else:
                    ext='assembly:'+str(name or rv); self.node(ext,kind='external-assembly',assemblyName=name or rv); self.edge(rp,ext,'asmdef-reference','authoritative',assembly=name or rv)
        asm_dirs=sorted([(Path(rp).parent,rp) for rp,n in self.nodes.items() if n.get('kind')=='asmdef'],key=lambda x:len(x[0].parts),reverse=True)
        for rp,n in list(self.nodes.items()):
            if n.get('kind')!='script' or not rp.startswith('Assets/'):continue
            pp=Path(rp); assigned=None
            for d,ap in asm_dirs:
                try:pp.relative_to(d);assigned=ap;break
                except ValueError:pass
            if assigned:self.edge(rp,assigned,'compiled-into','authoritative')
            else:
                a='assembly:Assembly-CSharp-Editor' if 'Editor' in pp.parts else 'assembly:Assembly-CSharp'; self.node(a,kind='implicit-assembly',assemblyName=a.split(':',1)[1]); self.edge(rp,a,'compiled-into','inferred')
    def code_edges(self):
        if not self.code_heuristics:return
        owners=defaultdict(set); facts={}
        for rp,n in self.nodes.items():
            if n.get('kind')!='script':continue
            txt=read_text(self.root/rp); ns=set(CS_NAMESPACE_RE.findall(txt)); us=set(CS_USING_RE.findall(txt)); types=set(CS_TYPE_RE.findall(txt)); facts[rp]={'namespaces':sorted(ns),'usings':sorted(us),'types':sorted(types)}; self.node(rp,codeFacts=facts[rp])
            for x in ns:owners[x].add(rp)
        for rp,f in facts.items():
            for u in f['usings']:
                matches=set()
                for ns,paths in owners.items():
                    if ns==u or ns.startswith(u+'.'):matches.update(paths)
                if 0<len(matches)<=20:
                    for t in matches:
                        if t!=rp:self.edge(rp,t,'namespace-import','heuristic',namespace=u)
    def discover_roots(self):
        txt=read_text(self.root/'ProjectSettings/EditorBuildSettings.asset')
        for m in re.finditer(r'- enabled:\s*(\d+)\s*\n\s*path:\s*(.+?)\s*$',txt,re.M):
            if m.group(1)=='1' and m.group(2).strip() in self.nodes:self.roots['enabled-build-scenes'].append(m.group(2).strip())
        for rp in self.nodes:
            parts=Path(rp).parts
            if 'Resources' in parts:self.roots['resources'].append(rp)
            if 'StreamingAssets' in parts:self.roots['streaming-assets'].append(rp)
            if rp.startswith('Assets/AddressableAssetsData/'):self.roots['addressables-config'].append(rp)
        for g in set(x.lower() for x in GUID_RE.findall(read_text(self.root/'ProjectSettings/ProjectSettings.asset'))):
            if g in self.guid_to_path:self.roots['project-settings'].append(self.guid_to_path[g])
        for k in list(self.roots):self.roots[k]=sorted(set(self.roots[k]))
    def cycles(self):
        adj=defaultdict(list)
        for e in self.edges:
            if e['type']=='asmdef-reference' and self.nodes.get(e['target'],{}).get('kind')=='asmdef':adj[e['source']].append(e['target'])
        color={}; stack=[]; out=[]; seen=set()
        def dfs(v):
            color[v]=1;stack.append(v)
            for w in adj[v]:
                if color.get(w,0)==0:dfs(w)
                elif color.get(w)==1:
                    i=stack.index(w); c=stack[i:]+[w]; key=tuple(sorted(c[:-1]))
                    if key not in seen:seen.add(key);out.append(c)
            stack.pop();color[v]=2
        for v in list(adj):
            if color.get(v,0)==0:dfs(v)
        for c in out:self.findings.append(Finding('error','asmdef-cycle','Assembly definition cycle detected',c[0],{'cycle':c}))
        return out
    def resolve(self,t):
        t=t.replace('\\','/')
        if t in self.nodes:return t
        if t.lower() in self.guid_to_path:return self.guid_to_path[t.lower()]
        if t.startswith('guid:') and t[5:].lower() in self.guid_to_path:return self.guid_to_path[t[5:].lower()]
        m=[p for p in self.nodes if Path(p).name==t];return m[0] if len(m)==1 else None
    def impact(self,target,max_depth=8):
        target=self.resolve(target)
        if not target:return None
        rev=defaultdict(list)
        for e in self.edges:rev[e['target']].append(e)
        q=deque([(target,0)]);vis={target:0};via=defaultdict(list)
        while q:
            cur,d=q.popleft()
            if d>=max_depth:continue
            for e in rev[cur]:
                s=e['source'];via[s].append({'dependsOn':cur,'edge':e['type'],'confidence':e['confidence']})
                if s not in vis:vis[s]=d+1;q.append((s,d+1))
        arr=[{'id':p,'depth':d,'kind':self.nodes.get(p,{}).get('kind'),'via':via.get(p,[])} for p,d in sorted(vis.items(),key=lambda x:(x[1],x[0])) if p!=target]
        return {'target':target,'directDependents':[x for x in arr if x['depth']==1],'transitiveDependents':arr,'maxDepth':max_depth}
    def reachability(self):
        adj=defaultdict(list)
        for e in self.edges:
            if e['type']=='serialized-guid':adj[e['source']].append(e['target'])
        roots=set(x for vals in self.roots.values() for x in vals);q=deque(roots);seen=set(roots)
        while q:
            cur=q.popleft()
            for t in adj[cur]:
                if t not in seen and not t.startswith('guid:'):seen.add(t);q.append(t)
        candidates=[]
        for rp,n in self.nodes.items():
            if not rp.startswith('Assets/') or n.get('kind') in {'script','asmdef','asmref'} or '/Editor/' in rp or rp.startswith('Assets/Editor/') or rp.startswith('Assets/AddressableAssetsData/') or rp in seen:continue
            if not (self.root/rp).is_file():continue
            candidates.append({'path':rp,'kind':n.get('kind'),'size':n.get('size'),'classification':'candidate-only','reason':'not reachable from known static runtime roots through serialized GUID edges','caveat':'may still be loaded dynamically by strings, Addressables/runtime catalogs, AssetBundles, reflection, custom loaders, disabled scenes, editor tooling, or external code'})
        return {'reachableCount':len(seen),'unusedCandidates':sorted(candidates,key=lambda x:x['path'])}
    def build(self):
        self.discover_assets();self.serialized_edges();self.assembly_edges();self.code_edges();self.discover_roots();cyc=self.cycles();reach=self.reachability()
        return {'schema':2,'project':norm(self.root),'capabilities':{'serializedGuidEdges':'authoritative for GUID references present in text-serialized Unity assets','asmdefEdges':'authoritative for explicit asmdef references','scriptAssemblyAssociation':'authoritative for nearest explicit asmdef; inferred for default assemblies','codeEdges':'heuristic namespace-import signals only' if self.code_heuristics else 'disabled','unusedDetection':'candidate-only reachability heuristic; never deletion authority'},'stats':{'nodes':len(self.nodes),'edges':len(self.edges),'assetGuids':len(self.guid_to_path),'findings':len(self.findings),'asmdefCycles':len(cyc),'unusedCandidates':len(reach['unusedCandidates'])},'nodes':sorted(self.nodes.values(),key=lambda x:x['id']),'edges':sorted(self.edges,key=lambda x:(x['source'],x['target'],x['type'])),'roots':dict(self.roots),'reachability':reach,'findings':[asdict(x) for x in self.findings]}

def dot(d):
    lines=['digraph UnityProject {','  rankdir="LR";','  node [shape=box,fontname="Arial",fontsize=9];']
    esc=lambda s:str(s).replace('\\','\\\\').replace('"','\\"')
    for n in d['nodes']:lines.append(f'  "{esc(n["id"])}" [label="{esc(Path(n["id"]).name or n["id"])}\\n[{esc(n.get("kind",""))}]"];')
    for e in d['edges']:lines.append(f'  "{esc(e["source"])}" -> "{esc(e["target"])}" [label="{esc(e["type"])}",style={"dashed" if e.get("confidence") in {"heuristic","inferred"} else "solid"}];')
    return '\n'.join(lines+['}'])+'\n'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('project',nargs='?',default='.');ap.add_argument('--target');ap.add_argument('--max-depth',type=int,default=8);ap.add_argument('--code-heuristics',action='store_true');ap.add_argument('--json',action='store_true');ap.add_argument('--write-json');ap.add_argument('--write-dot');a=ap.parse_args();root=Path(a.project).resolve()
    if not (root/'Assets').exists():print('Not a Unity project: Assets directory missing',file=sys.stderr);return 3
    g=Graph(root,a.code_heuristics);d=g.build();impact=None
    if a.target:
        impact=g.impact(a.target,a.max_depth)
        if impact is None:print('Target not found or ambiguous: '+a.target,file=sys.stderr);return 4
        d['impact']=impact
    if a.write_json:Path(a.write_json).parent.mkdir(parents=True,exist_ok=True);Path(a.write_json).write_text(json.dumps(d,indent=2)+'\n')
    if a.write_dot:Path(a.write_dot).parent.mkdir(parents=True,exist_ok=True);Path(a.write_dot).write_text(dot(d))
    if a.json:print(json.dumps(d,indent=2))
    else:
        s=d['stats'];print(f"Unity project graph: {s['nodes']} nodes, {s['edges']} edges, {s['assetGuids']} asset GUIDs\nFindings: {s['findings']} | asmdef cycles: {s['asmdefCycles']} | unused candidates: {s['unusedCandidates']}")
        if impact:print(f"Impact target: {impact['target']}\nDirect dependents: {len(impact['directDependents'])}; transitive dependents: {len(impact['transitiveDependents'])}")
    return 0
if __name__=='__main__':raise SystemExit(main())
