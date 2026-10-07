"""Private opt-in session records. Set ADDMATH_DB on a persistent host for durability."""
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
import csv
import io
import json
import os
import sqlite3


def connect():
    path=Path(os.getenv('ADDMATH_DB', str(Path(__file__).parent/'data'/'arena.sqlite3')))
    path.parent.mkdir(parents=True,exist_ok=True)
    connection=sqlite3.connect(path,timeout=20)
    connection.row_factory=sqlite3.Row
    connection.execute('''CREATE TABLE IF NOT EXISTS sessions(
        run_id TEXT PRIMARY KEY, nickname TEXT, track TEXT, form TEXT, topic TEXT,
        level TEXT, score INTEGER, correct INTEGER, total INTEGER, best_streak INTEGER,
        completed_at TEXT, details TEXT)''')
    connection.commit()
    return connection


def save(run):
    results=run['results']; streak=best=0
    for r in results:
        streak=streak+1 if r['correct'] else 0;best=max(best,streak)
    row=(run['id'],run['name'],run['track'],run['form'],run['topic'],run['level'],
         sum(r['xp'] for r in results),sum(r['correct'] for r in results),len(results),best,
         datetime.now(timezone.utc).isoformat(timespec='seconds'),json.dumps(results,ensure_ascii=False))
    with closing(connect()) as con:
        with con:
            con.execute('INSERT OR IGNORE INTO sessions VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',row)


def records():
    with closing(connect()) as con:
        return [dict(r) for r in con.execute('SELECT * FROM sessions ORDER BY completed_at DESC').fetchall()]


def csv_bytes(rows):
    if not rows:
        return b''
    stream=io.StringIO(newline='');fields=list(rows[0]); writer=csv.DictWriter(stream,fieldnames=fields,extrasaction='ignore');writer.writeheader()
    for row in rows:
        safe={k: ("'"+v if isinstance(v,str) and v.lstrip().startswith(('=','+','-','@')) else v) for k,v in row.items()}
        writer.writerow(safe)
    return stream.getvalue().encode('utf-8-sig')
