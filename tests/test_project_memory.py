#!/usr/bin/env python3
import json, subprocess, sys, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'skills/project-memory/scripts/memory_db.py'

def run(db,*args,ok=True):
    p=subprocess.run([sys.executable,str(SCRIPT),'--db',str(db),*args],text=True,capture_output=True)
    if ok and p.returncode:
        raise AssertionError(f"failed: {args}\nstdout={p.stdout}\nstderr={p.stderr}")
    return p

with tempfile.TemporaryDirectory() as td:
    db=Path(td)/'project.db'
    out=run(db,'put-fact','networking','provider','FishNet','--source','Packages/manifest.json','--confidence','1').stdout
    assert json.loads(out)['value']=='FishNet'
    out=run(db,'add-decision','ADR-001','Authority','Server authoritative combat','Clients submit intent; server validates outcomes','--source','.claude/unity/decisions/ADR-001.md').stdout
    assert json.loads(out)['status']=='accepted'
    out=run(db,'add-incident','Duplicate item','Inventory transaction applied twice','--area','inventory','--root-cause','replayed request','--resolution','idempotency key','--regression-test','InventoryReplayTests').stdout
    fp=json.loads(out)['fingerprint']
    run(db,'resolve-incident',fp,'idempotency key + server-side replay cache')
    run(db,'add-performance','server_tick_ms','8.3','ms','--scope','32-player-match','--scenario','combat','--build-target','StandaloneLinux64')
    run(db,'add-feature-event','inventory','fixed','Prevent duplicate transaction replay','--source','Assets/Game/Inventory')
    run(db,'relate','system','inventory','depends-on','system','items','--confidence','0.9')
    results=json.loads(run(db,'search','server authority').stdout)
    assert any(r['record_type']=='decision' for r in results)
    stats=json.loads(run(db,'stats').stdout)
    assert stats['schema_version']==2 and stats['facts']==1 and stats['decisions']==1 and stats['incidents']==1
    exported=json.loads(run(db,'export').stdout)
    assert len(exported['performance_samples'])==1 and len(exported['feature_history'])==1
    bad=run(db,'put-fact','auth','token','github_pat_EXAMPLESECRET','--confidence','1',ok=False)
    assert bad.returncode != 0 and 'credential' in (bad.stdout+bad.stderr).lower()
print('project memory tests: OK')

# Legacy alpha.3 schema migration preserves prior data.
with tempfile.TemporaryDirectory() as td:
    import sqlite3, time
    db=Path(td)/'legacy.db'
    con=sqlite3.connect(db)
    con.executescript('''
    CREATE TABLE facts(id INTEGER PRIMARY KEY, category TEXT NOT NULL, key TEXT NOT NULL, value TEXT NOT NULL, source TEXT, confidence REAL NOT NULL DEFAULT 1.0, updated_at INTEGER NOT NULL, UNIQUE(category,key));
    CREATE TABLE decisions(id TEXT PRIMARY KEY, title TEXT NOT NULL, status TEXT NOT NULL, rationale TEXT NOT NULL, updated_at INTEGER NOT NULL);
    CREATE TABLE regressions(id INTEGER PRIMARY KEY, fingerprint TEXT UNIQUE NOT NULL, summary TEXT NOT NULL, resolution TEXT, updated_at INTEGER NOT NULL);
    ''')
    ts=int(time.time())
    con.execute("INSERT INTO facts(category,key,value,source,confidence,updated_at) VALUES('networking','provider','Mirror','Packages/manifest.json',1,?)",(ts,))
    con.execute("INSERT INTO decisions(id,title,status,rationale,updated_at) VALUES('ADR-OLD','Legacy transport','accepted','Historical reason',?)",(ts,))
    con.execute("INSERT INTO regressions(fingerprint,summary,resolution,updated_at) VALUES('abc','Old crash','Fixed guard',?)",(ts,))
    con.commit(); con.close()
    stats=json.loads(run(db,'stats').stdout)
    assert stats['facts']==1 and stats['decisions']==1 and stats['incidents']==1
    fact=json.loads(run(db,'get-fact','networking','provider').stdout)
    assert fact['value']=='Mirror'
print('legacy memory migration: OK')
