import csv
import io
import math
import re
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import pytest
from bank import build,make
from checker import check,numeric
from curriculum import TOPICS,TRACKS,LEVELS
from storage import save,records,csv_bytes
from streamlit.testing.v1 import AppTest


@pytest.mark.parametrize('topic',list(TOPICS))
@pytest.mark.parametrize('level',LEVELS)
def test_all_topics_generate_and_grade(topic,level):
    track=TRACKS[0] if topic in ['polynomials','equations','straight_lines','circles','logarithms','calculus'] else TRACKS[1]
    for seed in range(15):
        questions=build(track,'All',topic,level,15,seed)
        assert len(questions)==15
        assert len({(q['en'],q['latex']) for q in questions})==15
        for q in questions:
            assert q['en'] and q['bm'] and q['steps'] and q['hints']
            assert len(q['answers'])==len(q['labels'])
            assert all(math.isfinite(v) for v in q['answers'])
            answer=[str(v) for v in q['answers']]
            assert check(answer,q)
            assert not check([str(v+1) for v in q['answers']],q)
            if q['unordered']: assert check(list(reversed(answer)),q)


@pytest.mark.parametrize('payload',["__import__('os')",'2**999999','(1).__class__','sqrt(-1)','1/0','exp(10000)','[1,2]','True','pi.__class__','1e999'])
def test_parser_rejects_bad_input(payload):
    with pytest.raises(ValueError): numeric(payload)


def test_parser_exact_forms():
    assert numeric('1/2')==.5
    assert abs(numeric('sqrt(3)^2')-3)<1e-9
    assert abs(numeric('2*pi/3')-2*math.pi/3)<1e-9
    assert numeric('-2 + 3*4')==10


class Fixed:
    def randint(self,lo,hi): return lo
    def sample(self,values,n): return list(values)[:n]
    def choice(self,values): return values[0]


def test_independent_known_mathematics():
    rng=Fixed();level=LEVELS[0]
    cases={
      ('functions',0):[3],('functions',1):[1],('functions',2):[7],
      ('quadratics',0):[-5,-4],('quadratics',1):[1],('quadratics',2):[17],
      ('polynomials',0):[4],('polynomials',1):[-3],('polynomials',2):[-6,-5,-4],
      ('equations',0):[1.5,-.5],('equations',1):[-1,3],('equations',2):[2],
      ('simultaneous',0):[1,-3],('simultaneous',2):[1],
      ('indices',0):[2],('indices',1):[4],('indices',2):[3],
      ('logarithms',2):[4],('linear_law',0):[1],('linear_law',1):[2],('linear_law',2):[2],
      ('straight_lines',0):[1],('coordinates',1):[-.5],('coordinates',2):[2],
      ('circles',0):[2],('circles',1):[2,-1],('circles',2):[10],
      ('circular',0):[2/3],('circular',1):[2/3],('circular',2):[6],
      ('trig',0):[30,150],('trig',1):[2*math.pi],('trig',2):[0],
      ('triangles',0):[math.sqrt(3)],('triangles',1):[1],('triangles',2):[4],
      ('combinatorics',0):[10],('combinatorics',1):[20],('combinatorics',2):[60],
      ('series',0):[5],('series',1):[14],('series',2):[4],
      ('vectors',0):[10],('vectors',1):[2,1],('vectors',2):[2],
      ('differentiation',0):[7],('differentiation',1):[1],('differentiation',2):[12],
      ('integration',0):[8],('integration',1):[2],('integration',2):[4],
      ('kinematics',0):[5],('kinematics',1):[4],('kinematics',2):[3],
      ('index_numbers',0):[110],('index_numbers',1):[114],('index_numbers',2):[22],
      ('probability',0):[3/8],('probability',1):[3/4],('probability',2):[2],
      ('linear_programming',0):[4],('linear_programming',1):[2],('linear_programming',2):[5],
    }
    for (topic,v),expected in cases.items():
        q=make(topic,level,v,rng)
        assert q['answers']==pytest.approx(expected), (topic,v,q['answers'],expected)


def test_storage_idempotent_private_and_export(tmp_path,monkeypatch):
    monkeypatch.setenv('ADDMATH_DB',str(tmp_path/'db.sqlite3'))
    run={'id':'test','name':'=EVIL()','track':'SPM','form':'All','topic':'functions','level':'Warm-up','results':[{'correct':True,'xp':10,'topic':'functions','response':['3']} ]}
    save(run);save(run)
    rows=records();assert len(rows)==1 and rows[0]['best_streak']==1
    data=list(csv.DictReader(io.StringIO(csv_bytes(rows).decode('utf-8-sig'))))
    assert data[0]['nickname']=="'=EVIL()"


def test_ui_complete_session_and_graph_lab(tmp_path,monkeypatch):
    monkeypatch.setenv('ADDMATH_DB',str(tmp_path/'ui.sqlite3'))
    app=AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py')).run(timeout=30)
    assert not app.exception
    # Language, course, form, topic, level, count are selectboxes on the setup view.
    app.text_input[0].set_value('Amy test')
    next(s for s in app.selectbox if s.label=='Questions / Soalan').select(5)
    next(b for b in app.button if b.label.startswith('Start my session')).click().run(timeout=30)
    assert not app.exception
    for _ in range(5):
        run=app.session_state['run'];q=run['questions'][run['index']]
        for field,value in zip(app.text_input,q['answers']): field.set_value(str(value))
        next(b for b in app.button if b.label.startswith('Check my answer')).click().run(timeout=30)
        assert not app.exception
        next(b for b in app.button if b.label.startswith(('Next challenge','See my results'))).click().run(timeout=30)
        assert not app.exception
    assert len(app.session_state['run']['results'])==5
    assert all(r['correct'] for r in app.session_state['run']['results'])
    assert not records() # Consent was not selected.
    app.radio[0].set_value('Graph Lab').run(timeout=30)
    assert not app.exception
    next(s for s in app.selectbox if s.label=='Function family / Keluarga fungsi').select('Logarithmic').run(timeout=30)
    assert not app.exception


def test_spm_malay_consent_and_retry(tmp_path,monkeypatch):
    monkeypatch.setenv('ADDMATH_DB',str(tmp_path/'spm.sqlite3'))
    app=AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py')).run(timeout=30)
    next(s for s in app.selectbox if s.key=='language').select('Bahasa Melayu').run()
    assert not app.exception
    app.text_input[0].set_value('Ujian SPM')
    next(s for s in app.selectbox if s.label=='Kursus anda').select(TRACKS[1]).run()
    next(s for s in app.selectbox if s.label=='Tingkatan SPM').select('Form 5 / Tingkatan 5').run()
    next(s for s in app.selectbox if s.label=='Soalan').select(5)
    app.checkbox[0].check()
    next(b for b in app.button if b.label.startswith('Mulakan sesi')).click().run()
    for i in range(5):
        run=app.session_state['run'];q=run['questions'][run['index']]
        for field,value in zip(app.text_input,q['answers']): field.set_value(str(value+1 if i==0 else value))
        next(b for b in app.button if b.label.startswith('Semak jawapan')).click().run()
        next(b for b in app.button if b.label.startswith(('Cabaran seterusnya','Lihat keputusan'))).click().run()
        assert not app.exception
    assert len(records())==1 and records()[0]['correct']==4
    next(b for b in app.button if b.label=='Cuba semula soalan salah').click().run()
    assert len(app.session_state['run']['questions'])==1
    assert not app.exception


def test_teacher_auth_gate(tmp_path,monkeypatch):
    monkeypatch.setenv('ADDMATH_DB',str(tmp_path/'auth.sqlite3'))
    app=AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py'))
    app.secrets={'teacher_password':'test-password-123'}
    app.run(); app.radio[0].set_value('Teacher').run()
    assert app.text_input[0].proto.type==app.text_input[0].proto.PASSWORD
    app.text_input[0].set_value('wrong')
    next(b for b in app.button if b.label.startswith('Log in')).click().run()
    assert len(app.error)==1 and not app.dataframe
    app.text_input[0].set_value('test-password-123')
    next(b for b in app.button if b.label.startswith('Log in')).click().run()
    assert any(b.label.startswith('Log out') for b in app.button)
    assert not app.exception
