"""Run before deployment to detect missing or incomplete source files."""
from pathlib import Path
import ast

root=Path(__file__).parent
for name in ['app.py','bank.py','progression.py','diagrams.py','music.py','checker.py','curriculum.py','storage.py']:
    file=root/name
    if not file.exists(): raise SystemExit('MISSING FILE: '+name)
    ast.parse(file.read_text(encoding='utf-8'),filename=name)
for name in ['music_player.js','static/study_music.mp3','.streamlit/config.toml']:
    if not (root/name).is_file(): raise SystemExit('MISSING FILE: '+name)
from bank import build
from checker import check
from curriculum import TRACKS, LEVELS, PROGRESSION
for path in TRACKS:
    for level in LEVELS+[PROGRESSION]:
      for question in build(path,'All','mixed',level,15,seed=2026):
        if not check([str(v) for v in question['answers']],question):
            raise SystemExit('Answer check failed.')
print('Project complete: source files parse, generators import and both course paths work.')
