#!/usr/bin/env python3
"""Unity Architect Pro durable engineering memory store.

Repository-local SQLite database for evidence-backed project knowledge.
No network access. Never store credentials, secrets, personal data, or raw chat logs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
import sys
import time
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 2

SCHEMA = r"""
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS meta(
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS facts(
  id INTEGER PRIMARY KEY,
  category TEXT NOT NULL,
  key TEXT NOT NULL,
  value TEXT NOT NULL,
  source TEXT,
  evidence TEXT,
  confidence REAL NOT NULL DEFAULT 1.0 CHECK(confidence >= 0 AND confidence <= 1),
  status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active','stale','superseded','rejected')),
  first_seen_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  expires_at INTEGER,
  superseded_by INTEGER,
  FOREIGN KEY(superseded_by) REFERENCES facts(id),
  UNIQUE(category,key,status) ON CONFLICT ABORT
);
CREATE INDEX IF NOT EXISTS idx_facts_category ON facts(category);
CREATE INDEX IF NOT EXISTS idx_facts_status ON facts(status);
CREATE INDEX IF NOT EXISTS idx_facts_updated ON facts(updated_at);

CREATE TABLE IF NOT EXISTS decisions(
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL CHECK(status IN ('proposed','accepted','deprecated','superseded','rejected')),
  context TEXT,
  decision TEXT NOT NULL,
  rationale TEXT NOT NULL,
  consequences TEXT,
  source TEXT,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  supersedes TEXT,
  FOREIGN KEY(supersedes) REFERENCES decisions(id)
);
CREATE INDEX IF NOT EXISTS idx_decisions_status ON decisions(status);

CREATE TABLE IF NOT EXISTS incidents(
  id INTEGER PRIMARY KEY,
  fingerprint TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL,
  area TEXT,
  symptoms TEXT NOT NULL,
  root_cause TEXT,
  resolution TEXT,
  regression_test TEXT,
  source TEXT,
  status TEXT NOT NULL DEFAULT 'open' CHECK(status IN ('open','resolved','wontfix')),
  first_seen_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  resolved_at INTEGER
);

CREATE TABLE IF NOT EXISTS performance_samples(
  id INTEGER PRIMARY KEY,
  metric TEXT NOT NULL,
  scope TEXT NOT NULL DEFAULT 'project',
  value REAL NOT NULL,
  unit TEXT NOT NULL,
  build_target TEXT,
  scenario TEXT,
  source TEXT,
  captured_at INTEGER NOT NULL,
  commit_sha TEXT
);
CREATE INDEX IF NOT EXISTS idx_perf_metric ON performance_samples(metric,scope,captured_at);

CREATE TABLE IF NOT EXISTS feature_history(
  id INTEGER PRIMARY KEY,
  feature TEXT NOT NULL,
  event TEXT NOT NULL,
  summary TEXT NOT NULL,
  source TEXT,
  commit_sha TEXT,
  created_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_feature_name ON feature_history(feature,created_at);

CREATE TABLE IF NOT EXISTS relationships(
  id INTEGER PRIMARY KEY,
  subject_type TEXT NOT NULL,
  subject_key TEXT NOT NULL,
  relation TEXT NOT NULL,
  object_type TEXT NOT NULL,
  object_key TEXT NOT NULL,
  source TEXT,
  confidence REAL NOT NULL DEFAULT 1.0 CHECK(confidence >= 0 AND confidence <= 1),
  updated_at INTEGER NOT NULL,
  UNIQUE(subject_type,subject_key,relation,object_type,object_key)
);

CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
  record_type,
  record_key,
  title,
  body,
  source,
  tokenize='unicode61'
);
"""

SECRET_PATTERNS = [
    re.compile(r"github_pat_[A-Za-z0-9_]+", re.I),
    re.compile(r"ghp_[A-Za-z0-9]+", re.I),
    re.compile(r"(?:api[_-]?key|token|password|secret)\s*[:=]\s*[^\s]+", re.I),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
]


def now() -> int:
    return int(time.time())


def _columns(db: sqlite3.Connection, table: str) -> set[str]:
    try:
        return {r[1] for r in db.execute(f"PRAGMA table_info({table})")}
    except sqlite3.DatabaseError:
        return set()

def migrate_legacy(db: sqlite3.Connection) -> None:
    """Migrate the alpha.3 v1 schema without dropping remembered data."""
    tables = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    legacy_facts = 'facts' in tables and 'first_seen_at' not in _columns(db, 'facts')
    legacy_decisions = 'decisions' in tables and 'decision' not in _columns(db, 'decisions')
    legacy_regressions = 'regressions' in tables
    if not (legacy_facts or legacy_decisions or legacy_regressions):
        return
    db.execute('PRAGMA foreign_keys=OFF')
    if legacy_facts:
        db.execute('ALTER TABLE facts RENAME TO facts_v1')
    if legacy_decisions:
        db.execute('ALTER TABLE decisions RENAME TO decisions_v1')
    if legacy_regressions:
        db.execute('ALTER TABLE regressions RENAME TO regressions_v1')
    db.commit()
    db.executescript(SCHEMA)
    ts = now()
    if legacy_facts:
        for r in db.execute('SELECT category,key,value,source,confidence,updated_at FROM facts_v1'):
            stamp = r[5] or ts
            db.execute("INSERT OR IGNORE INTO facts(category,key,value,source,evidence,confidence,status,first_seen_at,updated_at) VALUES(?,?,?,?,NULL,?,'active',?,?)", (r[0],r[1],r[2],r[3],r[4],stamp,stamp))
        db.execute('DROP TABLE facts_v1')
    if legacy_decisions:
        for r in db.execute('SELECT id,title,status,rationale,updated_at FROM decisions_v1'):
            stamp = r[4] or ts
            status = r[2] if r[2] in ('proposed','accepted','deprecated','superseded','rejected') else 'accepted'
            db.execute("INSERT OR IGNORE INTO decisions(id,title,status,context,decision,rationale,consequences,source,created_at,updated_at) VALUES(?,?,?,NULL,?,?,NULL,'migrated:v1',?,?)", (r[0],r[1],status,r[1],r[3],stamp,stamp))
        db.execute('DROP TABLE decisions_v1')
    if legacy_regressions:
        for r in db.execute('SELECT fingerprint,summary,resolution,updated_at FROM regressions_v1'):
            stamp = r[3] or ts
            status = 'resolved' if r[2] else 'open'
            db.execute("INSERT OR IGNORE INTO incidents(fingerprint,title,area,symptoms,root_cause,resolution,regression_test,source,status,first_seen_at,updated_at,resolved_at) VALUES(?,?,NULL,?,NULL,?,NULL,'migrated:v1',?,?,?,?)", (r[0],r[1],r[1],r[2],status,stamp,stamp,stamp if status=='resolved' else None))
        db.execute('DROP TABLE regressions_v1')
    db.commit()
    db.execute('PRAGMA foreign_keys=ON')

def connect(path: str) -> sqlite3.Connection:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(p)
    db.row_factory = sqlite3.Row
    migrate_legacy(db)
    db.executescript(SCHEMA)
    db.execute("INSERT OR REPLACE INTO meta(key,value) VALUES('schema_version',?)", (str(SCHEMA_VERSION),))
    db.commit()
    rebuild_fts(db)
    return db


def reject_secret(*values: Any) -> None:
    text = "\n".join(str(v) for v in values if v is not None)
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            raise SystemExit("Refusing to store content that looks like a credential or secret")


def jprint(value: Any) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False))


def rowdict(row: sqlite3.Row | None) -> dict[str, Any] | None:
    return dict(row) if row else None


def rebuild_fts(db: sqlite3.Connection) -> None:
    db.execute("DELETE FROM memory_fts")
    for r in db.execute("SELECT category,key,value,source,status FROM facts WHERE status IN ('active','stale')"):
        db.execute("INSERT INTO memory_fts VALUES(?,?,?,?,?)", ("fact", f"{r['category']}:{r['key']}", r['key'], r['value'], r['source']))
    for r in db.execute("SELECT id,title,context,decision,rationale,consequences,source,status FROM decisions"):
        body = "\n".join(x or "" for x in (r['context'], r['decision'], r['rationale'], r['consequences']))
        db.execute("INSERT INTO memory_fts VALUES(?,?,?,?,?)", ("decision", r['id'], r['title'], body, r['source']))
    for r in db.execute("SELECT fingerprint,title,symptoms,root_cause,resolution,regression_test,source FROM incidents"):
        body = "\n".join(x or "" for x in (r['symptoms'], r['root_cause'], r['resolution'], r['regression_test']))
        db.execute("INSERT INTO memory_fts VALUES(?,?,?,?,?)", ("incident", r['fingerprint'], r['title'], body, r['source']))
    for r in db.execute("SELECT id,feature,event,summary,source FROM feature_history"):
        db.execute("INSERT INTO memory_fts VALUES(?,?,?,?,?)", ("feature", str(r['id']), f"{r['feature']} {r['event']}", r['summary'], r['source']))
    db.commit()


def upsert_fact(db: sqlite3.Connection, args: argparse.Namespace) -> None:
    reject_secret(args.category, args.key, args.value, args.source, args.evidence)
    ts = now()
    expires_at = ts + args.ttl_days * 86400 if args.ttl_days else None
    existing = db.execute("SELECT * FROM facts WHERE category=? AND key=? AND status='active'", (args.category, args.key)).fetchone()
    if existing:
        db.execute(
            "UPDATE facts SET value=?,source=?,evidence=?,confidence=?,updated_at=?,expires_at=? WHERE id=?",
            (args.value, args.source, args.evidence, args.confidence, ts, expires_at, existing['id'])
        )
        record_id = existing['id']
    else:
        cur = db.execute(
            "INSERT INTO facts(category,key,value,source,evidence,confidence,status,first_seen_at,updated_at,expires_at) VALUES(?,?,?,?,?,?,'active',?,?,?)",
            (args.category, args.key, args.value, args.source, args.evidence, args.confidence, ts, ts, expires_at)
        )
        record_id = cur.lastrowid
    db.commit(); rebuild_fts(db)
    jprint(rowdict(db.execute("SELECT * FROM facts WHERE id=?", (record_id,)).fetchone()))


def search(db: sqlite3.Connection, query: str, limit: int) -> None:
    # FTS5 query syntax is powerful but brittle for arbitrary user punctuation. Quote tokens conservatively.
    tokens = re.findall(r"[\w.-]+", query, re.UNICODE)
    if not tokens:
        jprint([]); return
    fts_q = " AND ".join('"' + t.replace('"', '""') + '"' for t in tokens)
    rows = db.execute(
        "SELECT record_type,record_key,title,body,source,bm25(memory_fts) AS rank FROM memory_fts WHERE memory_fts MATCH ? ORDER BY rank LIMIT ?",
        (fts_q, limit)
    ).fetchall()
    jprint([dict(r) for r in rows])


def review(db: sqlite3.Connection, stale_days: int) -> dict[str, Any]:
    ts = now(); stale_before = ts - stale_days * 86400
    expired = [dict(r) for r in db.execute("SELECT * FROM facts WHERE status='active' AND expires_at IS NOT NULL AND expires_at<=?", (ts,))]
    aging = [dict(r) for r in db.execute("SELECT * FROM facts WHERE status='active' AND updated_at<?", (stale_before,))]
    low_conf = [dict(r) for r in db.execute("SELECT * FROM facts WHERE status='active' AND confidence<0.7 ORDER BY confidence")]
    unresolved = [dict(r) for r in db.execute("SELECT * FROM incidents WHERE status='open' ORDER BY updated_at")]
    deprecated_decisions = [dict(r) for r in db.execute("SELECT * FROM decisions WHERE status IN ('deprecated','superseded') ORDER BY updated_at DESC")]
    return {
        "schema_version": SCHEMA_VERSION,
        "expired_facts": expired,
        "aging_facts": aging,
        "low_confidence_facts": low_conf,
        "open_incidents": unresolved,
        "deprecated_or_superseded_decisions": deprecated_decisions,
    }


def export_all(db: sqlite3.Connection) -> dict[str, Any]:
    result: dict[str, Any] = {"schema_version": SCHEMA_VERSION}
    for table in ("facts","decisions","incidents","performance_samples","feature_history","relationships"):
        result[table] = [dict(r) for r in db.execute(f"SELECT * FROM {table}")]
    return result


def main() -> None:
    p = argparse.ArgumentParser(description="Durable Unity engineering memory database")
    p.add_argument('--db', default='.claude/unity/project.db')
    sub = p.add_subparsers(dest='cmd', required=True)

    a = sub.add_parser('put-fact', aliases=['put'])
    a.add_argument('category'); a.add_argument('key'); a.add_argument('value')
    a.add_argument('--source'); a.add_argument('--evidence')
    a.add_argument('--confidence', type=float, default=1.0)
    a.add_argument('--ttl-days', type=int)

    a = sub.add_parser('get-fact', aliases=['get'])
    a.add_argument('category'); a.add_argument('key')
    a.add_argument('--include-inactive', action='store_true')

    a = sub.add_parser('list-facts', aliases=['list'])
    a.add_argument('--category'); a.add_argument('--status', default='active')

    a = sub.add_parser('supersede-fact')
    a.add_argument('category'); a.add_argument('key'); a.add_argument('--by-category'); a.add_argument('--by-key')

    a = sub.add_parser('add-decision')
    a.add_argument('id'); a.add_argument('title'); a.add_argument('decision'); a.add_argument('rationale')
    a.add_argument('--context'); a.add_argument('--consequences'); a.add_argument('--source'); a.add_argument('--status', default='accepted'); a.add_argument('--supersedes')

    a = sub.add_parser('add-incident')
    a.add_argument('title'); a.add_argument('symptoms'); a.add_argument('--fingerprint'); a.add_argument('--area'); a.add_argument('--root-cause'); a.add_argument('--resolution'); a.add_argument('--regression-test'); a.add_argument('--source'); a.add_argument('--status', default='open')

    a = sub.add_parser('resolve-incident')
    a.add_argument('fingerprint'); a.add_argument('resolution'); a.add_argument('--root-cause'); a.add_argument('--regression-test'); a.add_argument('--source')

    a = sub.add_parser('add-performance')
    a.add_argument('metric'); a.add_argument('value', type=float); a.add_argument('unit'); a.add_argument('--scope', default='project'); a.add_argument('--build-target'); a.add_argument('--scenario'); a.add_argument('--source'); a.add_argument('--commit-sha')

    a = sub.add_parser('performance-history')
    a.add_argument('metric'); a.add_argument('--scope', default='project'); a.add_argument('--limit', type=int, default=20)

    a = sub.add_parser('add-feature-event')
    a.add_argument('feature'); a.add_argument('event'); a.add_argument('summary'); a.add_argument('--source'); a.add_argument('--commit-sha')

    a = sub.add_parser('relate')
    a.add_argument('subject_type'); a.add_argument('subject_key'); a.add_argument('relation'); a.add_argument('object_type'); a.add_argument('object_key'); a.add_argument('--source'); a.add_argument('--confidence', type=float, default=1.0)

    a = sub.add_parser('search')
    a.add_argument('query'); a.add_argument('--limit', type=int, default=20)

    a = sub.add_parser('review')
    a.add_argument('--stale-days', type=int, default=90); a.add_argument('--mark-expired-stale', action='store_true')

    sub.add_parser('stats'); sub.add_parser('export'); sub.add_parser('rebuild-index')

    args = p.parse_args()
    if hasattr(args, 'confidence') and not (0 <= args.confidence <= 1):
        p.error('--confidence must be between 0 and 1')
    db = connect(args.db); ts = now()

    if args.cmd in ('put-fact','put'):
        upsert_fact(db,args)
    elif args.cmd in ('get-fact','get'):
        q = "SELECT * FROM facts WHERE category=? AND key=?" + ("" if args.include_inactive else " AND status='active'") + " ORDER BY updated_at DESC LIMIT 1"
        jprint(rowdict(db.execute(q,(args.category,args.key)).fetchone()))
    elif args.cmd in ('list-facts','list'):
        clauses=[]; vals=[]
        if args.category: clauses.append('category=?'); vals.append(args.category)
        if args.status != 'all': clauses.append('status=?'); vals.append(args.status)
        q='SELECT * FROM facts'+((' WHERE '+' AND '.join(clauses)) if clauses else '')+' ORDER BY category,key,updated_at DESC'
        jprint([dict(r) for r in db.execute(q,vals)])
    elif args.cmd=='supersede-fact':
        old=db.execute("SELECT * FROM facts WHERE category=? AND key=? AND status='active'",(args.category,args.key)).fetchone()
        if not old: raise SystemExit('active fact not found')
        by_id=None
        if args.by_category and args.by_key:
            newer=db.execute("SELECT id FROM facts WHERE category=? AND key=? AND status='active'",(args.by_category,args.by_key)).fetchone(); by_id=newer['id'] if newer else None
        db.execute("UPDATE facts SET status='superseded',superseded_by=?,updated_at=? WHERE id=?",(by_id,ts,old['id'])); db.commit(); rebuild_fts(db); jprint({'superseded': old['id'], 'by': by_id})
    elif args.cmd=='add-decision':
        reject_secret(args.title,args.decision,args.rationale,args.context,args.consequences,args.source)
        db.execute("INSERT INTO decisions(id,title,status,context,decision,rationale,consequences,source,created_at,updated_at,supersedes) VALUES(?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET title=excluded.title,status=excluded.status,context=excluded.context,decision=excluded.decision,rationale=excluded.rationale,consequences=excluded.consequences,source=excluded.source,updated_at=excluded.updated_at,supersedes=excluded.supersedes",(args.id,args.title,args.status,args.context,args.decision,args.rationale,args.consequences,args.source,ts,ts,args.supersedes)); db.commit(); rebuild_fts(db); jprint(rowdict(db.execute('SELECT * FROM decisions WHERE id=?',(args.id,)).fetchone()))
    elif args.cmd=='add-incident':
        reject_secret(args.title,args.symptoms,args.root_cause,args.resolution,args.regression_test,args.source)
        fp=args.fingerprint or hashlib.sha256((args.area or ''+'\n'+args.title+'\n'+args.symptoms).encode()).hexdigest()[:20]
        resolved_at=ts if args.status=='resolved' else None
        db.execute("INSERT INTO incidents(fingerprint,title,area,symptoms,root_cause,resolution,regression_test,source,status,first_seen_at,updated_at,resolved_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(fingerprint) DO UPDATE SET title=excluded.title,area=excluded.area,symptoms=excluded.symptoms,root_cause=COALESCE(excluded.root_cause,incidents.root_cause),resolution=COALESCE(excluded.resolution,incidents.resolution),regression_test=COALESCE(excluded.regression_test,incidents.regression_test),source=COALESCE(excluded.source,incidents.source),status=excluded.status,updated_at=excluded.updated_at,resolved_at=COALESCE(excluded.resolved_at,incidents.resolved_at)",(fp,args.title,args.area,args.symptoms,args.root_cause,args.resolution,args.regression_test,args.source,args.status,ts,ts,resolved_at)); db.commit(); rebuild_fts(db); jprint(rowdict(db.execute('SELECT * FROM incidents WHERE fingerprint=?',(fp,)).fetchone()))
    elif args.cmd=='resolve-incident':
        reject_secret(args.resolution,args.root_cause,args.regression_test,args.source)
        db.execute("UPDATE incidents SET status='resolved',resolution=?,root_cause=COALESCE(?,root_cause),regression_test=COALESCE(?,regression_test),source=COALESCE(?,source),updated_at=?,resolved_at=? WHERE fingerprint=?",(args.resolution,args.root_cause,args.regression_test,args.source,ts,ts,args.fingerprint)); db.commit(); rebuild_fts(db); jprint(rowdict(db.execute('SELECT * FROM incidents WHERE fingerprint=?',(args.fingerprint,)).fetchone()))
    elif args.cmd=='add-performance':
        reject_secret(args.metric,args.scope,args.source)
        cur=db.execute("INSERT INTO performance_samples(metric,scope,value,unit,build_target,scenario,source,captured_at,commit_sha) VALUES(?,?,?,?,?,?,?,?,?)",(args.metric,args.scope,args.value,args.unit,args.build_target,args.scenario,args.source,ts,args.commit_sha)); db.commit(); jprint(rowdict(db.execute('SELECT * FROM performance_samples WHERE id=?',(cur.lastrowid,)).fetchone()))
    elif args.cmd=='performance-history':
        rows=db.execute("SELECT * FROM performance_samples WHERE metric=? AND scope=? ORDER BY captured_at DESC LIMIT ?",(args.metric,args.scope,args.limit)).fetchall(); jprint([dict(r) for r in rows])
    elif args.cmd=='add-feature-event':
        reject_secret(args.feature,args.event,args.summary,args.source)
        cur=db.execute("INSERT INTO feature_history(feature,event,summary,source,commit_sha,created_at) VALUES(?,?,?,?,?,?)",(args.feature,args.event,args.summary,args.source,args.commit_sha,ts)); db.commit(); rebuild_fts(db); jprint(rowdict(db.execute('SELECT * FROM feature_history WHERE id=?',(cur.lastrowid,)).fetchone()))
    elif args.cmd=='relate':
        reject_secret(args.subject_type,args.subject_key,args.relation,args.object_type,args.object_key,args.source)
        db.execute("INSERT INTO relationships(subject_type,subject_key,relation,object_type,object_key,source,confidence,updated_at) VALUES(?,?,?,?,?,?,?,?) ON CONFLICT(subject_type,subject_key,relation,object_type,object_key) DO UPDATE SET source=excluded.source,confidence=excluded.confidence,updated_at=excluded.updated_at",(args.subject_type,args.subject_key,args.relation,args.object_type,args.object_key,args.source,args.confidence,ts)); db.commit(); jprint({'ok':True})
    elif args.cmd=='search': search(db,args.query,args.limit)
    elif args.cmd=='review':
        report=review(db,args.stale_days)
        if args.mark_expired_stale:
            db.execute("UPDATE facts SET status='stale',updated_at=? WHERE status='active' AND expires_at IS NOT NULL AND expires_at<=?",(ts,ts)); db.commit(); rebuild_fts(db)
        jprint(report)
    elif args.cmd=='stats':
        tables=['facts','decisions','incidents','performance_samples','feature_history','relationships']
        out={t: db.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0] for t in tables}; out['schema_version']=SCHEMA_VERSION; jprint(out)
    elif args.cmd=='export': jprint(export_all(db))
    elif args.cmd=='rebuild-index': rebuild_fts(db); jprint({'ok':True})

if __name__ == '__main__':
    main()
