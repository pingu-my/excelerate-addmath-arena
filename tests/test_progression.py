"""Independently worked examples and complete progression/hint UI checks."""
import math
import random
from pathlib import Path
import pytest
from bank import make, build
from curriculum import TOPICS, TRACKS, LEVELS, PROGRESSION
from checker import check
from streamlit.testing.v1 import AppTest


class LowerBounds:
    def randint(self, lo, hi):
        return lo


# Results worked independently for a=2, b=1, k=2, t=2.
MID = {
 'functions':[2,6], 'quadratics':[1,-8,-1,3],
 'polynomials':[-2,4], 'equations':[-3,-2,2,3],
 'simultaneous':[2,1], 'logarithms':[3], 'indices':[2,4],
 'straight_lines':[-1,5], 'coordinates':[-1,5], 'linear_law':[2,2,32],
 'circles':[-3,5], 'circular':[1/3,2/3,14/3],
 'trig':[16.5,46.5,76.5], 'triangles':[math.sqrt(12),2*math.sqrt(3)],
 'combinatorics':[48], 'series':[2,1,27], 'vectors':[3,4,math.sqrt(8)],
 'differentiation':[8,-7], 'integration':[2,12], 'kinematics':[9,22/3],
 'index_numbers':[115,46], 'probability':[11/16,2,1],
 'linear_programming':[2,1,8],
}
angle = math.degrees(math.asin(.55))
BOSS = {
 'functions':[2,2,5], 'quadratics':[2,4,8],
 'polynomials':[-4,-4,-2,4], 'equations':[-2,1,3,-2],
 'simultaneous':[3,7,5,11,math.sqrt(20)],
 'logarithms':[math.log(2),math.log(3)/math.log(2),800], 'indices':[1,3,.5],
 'straight_lines':[2,13/8,math.sqrt(425)/8,8],
 'coordinates':[2,13/8,math.sqrt(425)/8,8], 'linear_law':[2,8,26/3,2],
 'circles':[-.75,61/4,math.sqrt(44)], 'circular':[.25,5.5],
 'trig':[1.5,31.5,151.5,181.5],
 'triangles':[angle,180-angle,8.8*(.55*math.sqrt(3)/2-math.sqrt(1-.55**2)/2)],
 'combinatorics':[2,12], 'series':[2,.5,3], 'vectors':[2/3,4/3,2,4,3],
 'differentiation':[1,3,10,2], 'integration':[0,8/3], 'kinematics':[1,3,5],
 'index_numbers':[130,137.5,27.5], 'probability':[4,.5,11/16,68.75],
 'linear_programming':[2,1,8,2],
}


@pytest.mark.parametrize('topic',list(MID))
@pytest.mark.parametrize('level,expected_map',[(LEVELS[1],MID),(LEVELS[2],BOSS)])
def test_independent_upper_level_examples(topic,level,expected_map):
    q=make(topic,level,0,LowerBounds())
    assert q['answers']==pytest.approx(expected_map[topic])
    assert len(q['hints'])==(3 if level==LEVELS[2] else 2)


@pytest.mark.parametrize('variant,sub',list(enumerate(['differentiation','integration','kinematics'])))
@pytest.mark.parametrize('level,expected_map',[(LEVELS[1],MID),(LEVELS[2],BOSS)])
def test_cambridge_calculus_routes(variant,sub,level,expected_map):
    assert make('calculus',level,variant,LowerBounds())['answers']==pytest.approx(expected_map[sub])


@pytest.mark.parametrize('topic',list(TOPICS))
def test_demand_changes_with_level(topic):
    questions=[make(topic,level,0,random.Random(7)) for level in LEVELS]
    assert len({q['en'] for q in questions})==3
    assert len(questions[2]['steps'])>=2
    assert questions[1]['demand']=='linked steps'
    assert questions[2]['demand']=='exam-style'


@pytest.mark.parametrize('track',TRACKS)
@pytest.mark.parametrize('count',[5,10,15])
def test_ladder_order(track,count):
    qs=build(track,'All','mixed',PROGRESSION,count,2026)
    order=[LEVELS.index(q['level']) for q in qs]
    assert order==sorted(order)
    assert set(order)=={0,1,2}


def test_ui_ladder_staged_hints_and_xp(tmp_path,monkeypatch):
    monkeypatch.setenv('ADDMATH_DB',str(tmp_path/'ladder.sqlite3'))
    app=AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py')).run()
    app.text_input[0].set_value('Ladder test')
    next(s for s in app.selectbox if s.label=='Topic / Topik').select('functions')
    next(s for s in app.selectbox if s.label=='Challenge / Cabaran').select(PROGRESSION)
    next(s for s in app.selectbox if s.label=='Questions / Soalan').select(5)
    next(b for b in app.button if b.label.startswith('Start my session')).click().run()
    for i in range(5):
        q=app.session_state['run']['questions'][i]
        for h in range(len(q['hints'])):
            next(b for b in app.button if b.label.startswith(('Show a hint','Show the next hint'))).click().run()
            assert len(app.info)==h+1
            assert not app.exception
        for field,value in zip(app.text_input,q['answers']):field.set_value(str(value))
        next(b for b in app.button if b.label.startswith('Check my answer')).click().run()
        result=app.session_state['run']['results'][i]
        assert result['xp']==[10,15,20][LEVELS.index(q['level'])]-3
        assert result['hints_viewed']==len(q['hints'])
        next(b for b in app.button if b.label.startswith(('Next challenge','See my results'))).click().run()
        assert not app.exception
    assert [r['level'] for r in app.session_state['run']['results']]==['Warm-up','Warm-up','Level up','Level up','Boss mode']
    assert all(r['correct'] for r in app.session_state['run']['results'])


def test_retry_preserves_levels_and_resets_hints(tmp_path,monkeypatch):
    monkeypatch.setenv('ADDMATH_DB',str(tmp_path/'retry.sqlite3'))
    app=AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py')).run()
    questions=build(TRACKS[0],'All','functions',PROGRESSION,5,99)
    app.session_state['run']={'id':'retry','name':'Retry test','track':TRACKS[0],
        'form':'All','topic':'functions','level':PROGRESSION,'consent':False,
        'questions':questions,'index':5,'results':[dict(question=q['id'],topic=q['topic'],
        response=['wrong'],correct=False,xp=0,hint_used=False,level=q['level']) for q in questions],
        'hint':3,'saved':False,'started':0}
    app.run()
    next(b for b in app.button if b.label.startswith('Retry missed questions')).click().run()
    assert app.session_state['run']['hint']==0
    assert [q['level'] for q in app.session_state['run']['questions']]==['Warm-up','Warm-up','Level up','Level up','Boss mode']
    assert not app.exception
