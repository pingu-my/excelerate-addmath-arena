import io
import json
import math
import random
from pathlib import Path
import pytest
from PIL import Image
from bank import make
from curriculum import LEVELS
from diagrams import VISUAL_TOPICS, render, caption
from streamlit.testing.v1 import AppTest


@pytest.mark.parametrize('topic',sorted(VISUAL_TOPICS))
@pytest.mark.parametrize('level',LEVELS)
def test_every_visual_template_renders(topic,level):
    import matplotlib.pyplot as plt
    for variant in range(3):
        q=make(topic,level,variant,random.Random(27+variant))
        spec=q['diagram']
        if spec is None:
            assert topic=='simultaneous'
            continue
        # Specs are numerical givens and drawing instructions, not stored answers.
        encoded=json.dumps(spec,allow_nan=False)
        assert 'answers' not in encoded and 'answer_latex' not in encoded
        data=render(spec,'Bilingual')
        with Image.open(io.BytesIO(data)) as image:
            assert image.format=='PNG' and image.width>=1200 and image.height>=600
            assert image.getextrema()[0][0]!=image.getextrema()[0][1]
        assert caption(spec)[0] and caption(spec)[1]
        assert not plt.get_fignums()


@pytest.mark.parametrize('language',['English','Bahasa Melayu','Bilingual'])
def test_ambiguous_triangle_matches_both_given_sides(language):
    q=make('triangles','Boss mode',0,random.Random(27))
    tris=q['diagram']['triangles']
    assert len(tris)==2
    for tri in tris:
        A,B,C=tri['points']
        a=math.dist(B,C);b=math.dist(A,C)
        assert tri['sides'][1]==f'a = {a:g}'
        assert float(tri['sides'][2].split('=')[1])==pytest.approx(b)
        # The given A is genuinely 30 degrees, not a decorative sketch.
        angle=math.degrees(math.atan2(B[1]-A[1],B[0]-A[0]))
        assert angle==pytest.approx(30)
        assert all('B =' not in label for label in tri['angles'])
    assert len(render(q['diagram'],language))>10000


def test_annular_sector_and_lp_data_match_question():
    q=make('circular','Boss mode',0,random.Random(5))
    spec=q['diagram']; theta=q['answers'][0]
    assert spec['theta']==theta
    assert (spec['outer']+spec['inner'])*theta+2*(spec['outer']-spec['inner'])==pytest.approx(q['answers'][1])
    q=make('linear_programming','Boss mode',0,random.Random(5))
    x,y=q['answers'][:2]
    assert q['diagram']['integer']
    for p,r,c in q['diagram']['constraints']:
        assert p*x+r*y==pytest.approx(c)


def test_diagram_visible_in_question_and_review(tmp_path,monkeypatch):
    monkeypatch.setenv('ADDMATH_DB',str(tmp_path/'images.sqlite3'))
    app=AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py')).run(timeout=30)
    app.text_input[0].set_value('Diagram test')
    next(s for s in app.selectbox if s.label=='Topic / Topik').select('circles')
    next(s for s in app.selectbox if s.label=='Challenge / Cabaran').select('Boss mode')
    next(s for s in app.selectbox if s.label=='Questions / Soalan').select(5)
    next(b for b in app.button if b.label.startswith('Start my session')).click().run(timeout=30)
    assert len(app.get('image'))==1 and not app.exception
    for i in range(5):
        q=app.session_state['run']['questions'][i]
        for field,value in zip(app.text_input,q['answers']):field.set_value(str(value))
        next(b for b in app.button if b.label.startswith('Check my answer')).click().run(timeout=30)
        assert len(app.get('image'))==1
        next(b for b in app.button if b.label.startswith(('Next challenge','See my results'))).click().run(timeout=30)
        assert not app.exception
    assert len(app.get('image'))==5
