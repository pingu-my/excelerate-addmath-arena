"""Persistent low-volume music player using a same-page Streamlit component."""
from pathlib import Path
import streamlit as st
import streamlit.components.v2 as components

ROOT = Path(__file__).parent
def register_player():
    return components.component(
        'addmath_study_music',
        html='''<section><strong data-heading></strong>
        <button type="button" data-play></button>
        <label><span data-volume-label></span>
        <input data-volume type="range" min="0" max="1" step="0.01" aria-label="Music volume / Kelantangan muzik"></label>
        <p data-status aria-live="polite"></p></section>''',
        css='''section {font:14px sans-serif;color:#f4f3fa;padding:8px 0;}
        strong {display:block;margin-bottom:10px;}
        button {padding:8px 14px;margin-bottom:10px;border:1px solid #bd9efa;border-radius:10px;background:#20232f;color:#f4f3fa;cursor:pointer;}
        label {display:block;} input {width:100%;accent-color:#ceff75;}
        p {font-size:12px;line-height:1.5;color:#c4c6d8;}''',
        js=(ROOT/'music_player.js').read_text(encoding='utf-8'),
    )


def study_music(language, active=True):
    if not (ROOT/'static'/'study_music.mp3').is_file():
        st.caption('Add static/study_music.mp3 to enable music. / Tambah static/study_music.mp3 untuk muzik.')
        return
    register_player()(key='persistent_study_music',data={'language':language,'active':active})
