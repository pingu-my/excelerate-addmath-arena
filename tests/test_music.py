import shutil
import subprocess
import tomllib
from pathlib import Path
from streamlit.testing.v1 import AppTest
import pytest
import json
import base64

ROOT=Path(__file__).resolve().parents[1]


def test_packaged_music_and_static_configuration():
    assert (ROOT/'static'/'study_music.mp3').stat().st_size>100000
    config=tomllib.loads((ROOT/'.streamlit/config.toml').read_text())
    assert config['server']['enableStaticServing']


def test_music_javascript_lifecycle():
    node=shutil.which('node')
    if not node:pytest.skip('Node.js required for the optional audio lifecycle test')
    result=subprocess.run([node,str(ROOT/'tests/music_harness.mjs')],capture_output=True,text=True)
    assert result.returncode==0,result.stderr


def test_focus_removed_and_music_component_mounted():
    app=AppTest.from_file(str(ROOT/'app.py')).run(timeout=30)
    assert not app.exception
    assert not app.toggle
    assert 'focus_mode' not in (ROOT/'app.py').read_text()
    assert len(app.get('bidi_component'))==1


def test_audio_embedded_once_and_acknowledged():
    app=AppTest.from_file(str(ROOT/'app.py')).run(timeout=30)
    data=json.loads(app.get('bidi_component')[0].proto.json)
    assert data['source'].startswith('data:audio/mpeg;base64,')
    assert base64.b64decode(data['source'].split(',',1)[1])==(ROOT/'static/study_music.mp3').read_bytes()
    app.session_state['persistent_study_music']={'loaded':data['track_id']}
    app.run(timeout=30)
    next_data=json.loads(app.get('bidi_component')[0].proto.json)
    assert next_data['track_id']==data['track_id'] and 'source' not in next_data
    assert not app.exception
