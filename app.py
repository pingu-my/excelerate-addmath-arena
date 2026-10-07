from pathlib import Path
from uuid import uuid4
from datetime import datetime
from html import escape
import hashlib
import hmac
import math
import time

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from bank import build, latex_number
from checker import check, numeric
from curriculum import TRACKS, LEVELS, PROGRESSION, LEVEL_DESCRIPTIONS, TOPICS, title, topics_for
from storage import save, records, csv_bytes

st.set_page_config(page_title='EXCELerate · AddMath Arena',page_icon='✦',layout='wide',initial_sidebar_state='expanded')

with st.sidebar:
    language=st.selectbox('Language / Bahasa',['Bilingual','English','Bahasa Melayu'],key='language')
    focus=st.toggle('Focus mode / Mod fokus',key='focus_mode')


def tr(en,bm):
    return en if language=='English' else bm if language=='Bahasa Melayu' else en+' / '+bm


def text(en,bm):
    if language != 'Bahasa Melayu': st.write(en)
    if language != 'English': st.write(bm)


st.markdown('''<style>
.stApp {background:#11121a;color:#f4f3fa;background-image:radial-gradient(ellipse at 80% 0%,#33244980,transparent 55%);}
[data-testid="stMainBlockContainer"] {max-width:1240px;padding-top:2.6rem;}
[data-testid="stSidebar"] {background:#191b25;border-right:1px solid #353847;}
h1,h2,h3,p,label,[data-testid="stCaptionContainer"], [data-testid="stMetricLabel"] {color:#f2f1f8;}
[data-testid="stMetric"] {background:#20232f;border:1px solid #3a3e50;border-radius:16px;padding:14px;}
[data-testid="stMetricValue"] {color:#ceff75;}
.stButton button,.stDownloadButton button {min-height:46px;border-radius:12px;font-weight:700;}
.stButton button[kind="primary"] {background:#ceff75;color:#152014;border:0;box-shadow:0 4px 0 #80a242;}
.stButton button[kind="primary"] p {color:#152014;}
[data-testid="stTextInput"] input {min-height:48px;}
.hero {position:relative;overflow:hidden;background:linear-gradient(120deg,#272632,#1d2030);border:1px solid #56506f;border-radius:24px;padding:34px 40px;margin-bottom:24px;}
.kicker {font:700 11px monospace;letter-spacing:3px;color:#c7b6f7;}
.hero h1 {font-size:clamp(40px,6vw,74px);letter-spacing:-3px;line-height:1.02;margin:16px 0 12px;font-weight:900;}
.hero h1 span {color:#ceff75;}
.hero p {color:#c4c6d8;max-width:650px;}
.sticker {display:inline-block;background:#ceff75;color:#17230d;padding:6px 13px;border-radius:5px;transform:rotate(-3deg);font:800 12px monospace;}
.orb {position:absolute;right:30px;top:25px;width:135px;height:135px;border-radius:50%;background:radial-gradient(circle at 30% 30%,#fff,#b5a5e4 20%,#3d2e63 55%,#18192b 75%);box-shadow:0 0 45px #a489da35;opacity:.65;}
.orb:after {content:'✦';position:absolute;inset:18px;text-align:center;font-size:85px;color:#dcff94;transform:rotate(20deg);}
.questline {border-left:3px solid #bcabef;padding:8px 14px;margin:12px 0;color:#c8cadd;}
.card {border:1px solid #434454;border-radius:18px;padding:20px;background:#21232f;height:100%;}
.card .code {font:12px monospace;color:#bcabef;letter-spacing:2px;}
.card h3 {font-size:23px;margin:10px 0;color:#f5f4fa;}
.card p {color:#c2c6d8;font-size:14px;}
.badge {display:inline-block;background:#353045;color:#e2d4ff;border:1px solid #655682;border-radius:50px;padding:8px 16px;margin:4px;font-weight:700;}
.mission {display:flex;gap:7px;flex-wrap:wrap;margin:8px 0 20px;}
.node {width:27px;height:27px;border:1px solid #53566a;border-radius:8px;text-align:center;font:12px/27px monospace;color:#bec3d9;}
.node.done {background:#ceff75;color:#1b2610;border-color:#ceff75;}
.node.current {border:2px solid #bea6fc;color:#fff;}
@media(max-width:720px) {.hero {padding:24px;}.orb {display:none;}.hero h1 {font-size:44px;letter-spacing:-2px;}}
</style>''',unsafe_allow_html=True)
if focus:
    st.markdown('<style>.stApp{background:#161821}.orb,.sticker{display:none}.hero{background:#20222d} .hero h1{font-size:42px}</style>',unsafe_allow_html=True)

with st.sidebar:
    st.markdown('### ✦ EXCELerate')
    page=st.radio(tr('Open','Buka'),['Arena','Graph Lab','Teacher'],format_func=lambda p: {'Arena':tr('Practice arena','Arena latihan'),'Graph Lab':tr('Graph lab','Makmal graf'),'Teacher':tr('Teacher dashboard','Papan pemuka guru')}[p],key='page')
    st.caption(tr('Write your working. Build understanding.','Tulis jalan kerja. Bina kefahaman.'))
    run=st.session_state.get('run')
    results=run['results'] if run else []
    streak=0
    for r in reversed(results):
        if not r['correct']: break
        streak+=1
    st.metric('XP',sum(r['xp'] for r in results))
    st.metric(tr('Correct','Betul'),sum(r['correct'] for r in results))
    st.metric(tr('Streak','Rentetan'),streak)
    if run:
        st.caption(title(run['topic'],language) if run['topic']!='mixed' else tr('Mixed mission','Misi campuran'))
        st.progress(len(results)/len(run['questions']))
        if st.button(tr('End session / new setup','Tamat sesi / tetapan baharu')):
            del st.session_state['run'];st.rerun()
    st.divider()
    st.caption(tr('Ages 16–18 · EN / BM','Umur 16–18 · EN / BM'))


def hero():
    subtitle=tr('Lock in. Learn the move. Level up your maths.','Fokus. Fahami langkah. Tingkatkan kemahiran matematik.')
    st.markdown(f'<div class="hero"><div class="orb"></div><div class="kicker">EXCELERATE LEARNING SPACE · 16–18</div><h1>AddMath<br><span>Arena.</span></h1><p>{escape(subtitle)}</p><span class="sticker">YOUR NEXT LEVEL STARTS HERE ✦</span></div>',unsafe_allow_html=True)


def worked(q):
    for i,(en,bm,formula) in enumerate(q['steps'],1):
        st.markdown(f'**{i}. {tr(en,bm)}**')
        st.latex(formula)
    st.markdown('**'+tr('Final answer','Jawapan akhir')+'**')
    for label,ans in zip(q['labels'],q['answer_latex']):
        st.caption(tr(*label));st.latex(ans)


def teacher():
    st.title(tr('Teacher dashboard','Papan pemuka guru'))
    try: password=st.secrets.get('teacher_password','')
    except (FileNotFoundError,KeyError): password=''
    if not isinstance(password,str) or not password.strip():
        st.info(tr('Set teacher_password in Streamlit Settings → Secrets to enable login.','Tetapkan teacher_password dalam Streamlit Settings → Secrets untuk mengaktifkan log masuk.'));return
    expected=hashlib.sha256(password.encode()).hexdigest()
    if not hmac.compare_digest(st.session_state.get('teacher_auth',''),expected):
        with st.form('login',clear_on_submit=True):
            entered=st.text_input(tr('Password','Kata laluan'),type='password')
            submit=st.form_submit_button(tr('Log in','Log masuk'))
        if submit:
            if hmac.compare_digest(hashlib.sha256(entered.encode()).hexdigest(),expected):
                st.session_state.teacher_auth=expected;st.rerun()
            else: st.error(tr('Incorrect password.','Kata laluan salah.'))
        return
    if st.button(tr('Log out','Log keluar')):
        st.session_state.pop('teacher_auth',None);st.rerun()
    st.caption(tr('Only opted-in completed sessions are saved. Records are private to this dashboard.','Hanya sesi lengkap yang dipersetujui disimpan. Rekod adalah peribadi dalam papan pemuka ini.'))
    st.button(tr('Refresh','Muat semula'))
    try: rows=records()
    except Exception:
        st.error(tr('Could not read saved sessions.','Tidak dapat membaca sesi tersimpan.'));return
    if not rows:
        st.info(tr('No saved sessions yet.','Belum ada sesi tersimpan.'));return
    st.metric(tr('Saved sessions','Sesi tersimpan'),len(rows))
    st.download_button(tr('Export all results CSV','Eksport semua keputusan CSV'),csv_bytes(rows),'AddMath_All_Results.csv','text/csv')
    path=st.selectbox(tr('Path filter','Penapis laluan'),['All']+sorted({r['track'] for r in rows}))
    search=st.text_input(tr('Find nickname','Cari nama panggilan')).strip().casefold()
    filtered=[{k:v for k,v in r.items() if k!='details'} for r in rows if (path=='All' or r['track']==path) and (not search or search in r['nickname'].casefold())]
    st.dataframe(filtered,hide_index=True,width='stretch')


def graph_lab():
    st.title(tr('Graph Lab','Makmal Graf'))
    st.caption(tr('Move the sliders. Notice what changes before reading the explanation.','Gerakkan peluncur. Perhatikan perubahan sebelum membaca penerangan.'))
    family=st.selectbox(tr('Function family','Keluarga fungsi'),['Quadratic','Sine','Exponential','Logarithmic'],format_func=lambda x:tr(x,{'Quadratic':'Kuadratik','Sine':'Sinus','Exponential':'Eksponen','Logarithmic':'Logaritma'}[x]))
    c1,c2,c3=st.columns(3)
    a=c1.slider('a',-3.0,3.0,1.0,0.25)
    h=c2.slider('h',-5.0,5.0,0.0,0.25)
    k=c3.slider('k',-5.0,5.0,0.0,0.25)
    if family=='Quadratic':
        f=lambda x:a*(x-h)**2+k;parent=lambda x:x*x;domain=(-8,8);formula=rf'y={a}(x-({h}))^2+({k})'
        explanation=tr('Vertex (h,k) when a ≠ 0. Negative a reflects the graph. |a| changes vertical scale.','Puncak (h,k) apabila a ≠ 0. a negatif memantulkan graf. |a| mengubah skala menegak.')
    elif family=='Sine':
        b=st.slider('b',0.25,4.0,1.0,0.25)
        f=lambda x:a*np.sin(b*(x-h))+k;parent=np.sin;domain=(-2*math.pi,2*math.pi);formula=rf'y={a}\sin({b}(x-({h})))+({k})'
        explanation=tr(f'Amplitude = {abs(a)}. Period = 2π/b ≈ {2*math.pi/b:.3f} radians when a ≠ 0. Midline y = {k}.',f'Amplitud = {abs(a)}. Tempoh = 2π/b ≈ {2*math.pi/b:.3f} radian apabila a ≠ 0. Garis tengah y = {k}.')
    elif family=='Exponential':
        f=lambda x:a*np.exp(x-h)+k;parent=np.exp;domain=(-5,5);formula=rf'y={a}e^{{x-({h})}}+({k})'
        explanation=tr('For a ≠ 0, the horizontal asymptote is y = k. An exponential has no vertical asymptote.','Bagi a ≠ 0, asimptot mengufuk ialah y = k. Fungsi eksponen tiada asimptot mencancang.')
    else:
        f=lambda x:a*np.log(x-h)+k;parent=np.log;domain=(h+0.02,h+8);formula=rf'y={a}\ln(x-({h}))+({k})'
        explanation=tr('Domain x > h. For a ≠ 0, the vertical asymptote is x = h.','Domain x > h. Bagi a ≠ 0, asimptot mencancang ialah x = h.')
    st.latex(formula)
    xs=np.linspace(*domain,500); fig=go.Figure()
    if family=='Logarithmic':
        parentxs=np.linspace(.02,8,500)
    else: parentxs=xs
    fig.add_trace(go.Scatter(x=parentxs,y=parent(parentxs),name=tr('Parent','Asal'),line=dict(color='#777b94',dash='dash')))
    fig.add_trace(go.Scatter(x=xs,y=f(xs),name=tr('Your graph','Graf anda'),line=dict(color='#ceff75',width=3)))
    if family=='Quadratic' and a!=0: fig.add_trace(go.Scatter(x=[h],y=[k],mode='markers',name=tr('Vertex','Puncak'),marker=dict(size=10,color='#bd9efa')))
    if family=='Logarithmic' and a!=0: fig.add_vline(x=h,line_dash='dot',line_color='#bd9efa')
    if family=='Exponential' and a!=0: fig.add_hline(y=k,line_dash='dot',line_color='#bd9efa')
    fig.update_layout(template='plotly_dark',paper_bgcolor='#20222d',plot_bgcolor='#20222d',height=450,margin=dict(l=30,r=20,t=20,b=40),xaxis_title=tr('x (radians for sine)','x (radian bagi sinus)'),yaxis_title='y',legend=dict(orientation='h'),xaxis=dict(zeroline=True),yaxis=dict(zeroline=True))
    st.plotly_chart(fig,width='stretch');st.info(explanation)
    st.caption(tr('Drag to zoom; double-click to reset. The graph lab does not add XP.','Seret untuk zum; klik dua kali untuk set semula. Makmal graf tidak menambah XP.'))


if page=='Teacher': teacher();st.stop()
if page=='Graph Lab': graph_lab();st.stop()
hero()

if 'run' not in st.session_state:
    st.markdown('### '+tr('Choose your next move','Pilih langkah seterusnya'))
    c1,c2,c3=st.columns(3)
    cards=[('01 / PRACTISE','Skill reps','Latihan kemahiran','Fresh questions. Hints when you need them.','Soalan baharu. Petunjuk apabila diperlukan.'),('02 / UNDERSTAND','Learn the move','Fahami langkah','Worked steps in English and Bahasa Melayu.','Langkah penyelesaian dalam bahasa Inggeris dan Bahasa Melayu.'),('03 / EXPLORE','Make it visual','Lihat secara visual','Use Graph Lab to connect equations to graphs.','Gunakan Makmal Graf untuk menghubungkan persamaan dengan graf.')]
    for col,(code,en,bm,desc,desc_bm) in zip((c1,c2,c3),cards):
        with col: st.markdown(f'<div class="card"><div class="code">{code}</div><h3>{escape(tr(en,bm))}</h3><p>{escape(tr(desc,desc_bm))}</p></div>',unsafe_allow_html=True)
    st.write('')
    name=st.text_input(tr('First name or nickname','Nama pertama atau nama panggilan'),max_chars=40)
    c1,c2=st.columns(2)
    track=c1.selectbox(tr('Your course','Kursus anda'),TRACKS)
    form=c2.selectbox(tr('SPM form','Tingkatan SPM'),['All','Form 4 / Tingkatan 4','Form 5 / Tingkatan 5'],disabled=track==TRACKS[0])
    keys=topics_for(track,form)
    topic=st.selectbox(tr('Topic','Topik'),['mixed']+keys,format_func=lambda key:tr('Mixed mission','Misi campuran') if key=='mixed' else title(key,language))
    c1,c2=st.columns(2)
    level=c1.selectbox(tr('Challenge','Cabaran'),[PROGRESSION]+LEVELS,format_func=lambda x:tr(x,{PROGRESSION:'Bina kemahiran saya','Warm-up':'Pemanasan','Level up':'Naik tahap','Boss mode':'Cabaran utama'}[x]))
    count=c2.selectbox(tr('Questions','Soalan'),[5,10,15],index=1)
    consent=st.checkbox(tr('Save this completed session privately for my teacher.','Simpan sesi lengkap ini secara peribadi untuk guru saya.'),value=False)
    st.info(tr(*LEVEL_DESCRIPTIONS[level]))
    st.caption(tr('Original topic practice, not official past-paper questions or a full mock exam. Answers earn practice XP; this is not an examination grade.','Latihan topik asli, bukan soalan peperiksaan rasmi atau peperiksaan percubaan penuh. Jawapan memperoleh XP latihan; ini bukan gred peperiksaan.'))
    if st.button(tr('Start my session →','Mulakan sesi saya →'),type='primary'):
        if not name.strip(): st.warning(tr('Enter a nickname first.','Masukkan nama panggilan dahulu.'))
        else:
            st.session_state.run={'id':uuid4().hex,'name':name.strip(),'track':track,'form':form,'topic':topic,'level':level,'consent':consent,'questions':build(track,form,topic,level,count),'index':0,'results':[],'hint':False,'saved':False,'started':time.time()}
            st.rerun()
    with st.expander(tr('Topic map & sources','Peta topik & sumber')):
        st.write([title(k,language) for k in keys])
        st.markdown('[Cambridge 0606 syllabus (2025–2027)](https://www.cambridgeinternational.org/Images/662470-2025-2027-syllabus.pdf) · [KSSM DSKP reference](https://sites.google.com/moe-dl.edu.my/td2addmath/dskp)')
        st.caption(tr('Progressive practice for each menu topic; this bank does not cover every syllabus objective or award examination method marks. Cambridge menu is for 2025–2027 examinations.','Latihan progresif bagi setiap topik; bank ini tidak meliputi setiap objektif sukatan atau memberi markah kaedah peperiksaan. Menu Cambridge adalah untuk peperiksaan 2025–2027.'))
    st.stop()

run=st.session_state.run
if run['index']==len(run['questions']):
    correct=sum(r['correct'] for r in run['results']); total=len(run['results']);xp=sum(r['xp'] for r in run['results'])
    st.title(tr('Session complete. Keep the momentum.','Sesi selesai. Teruskan usaha.'))
    c1,c2,c3=st.columns(3);c1.metric(tr('Accuracy','Ketepatan'),f'{correct/total:.0%}');c2.metric('XP',xp);c3.metric(tr('Correct','Betul'),f'{correct}/{total}')
    stage_rows=[]
    for stage in LEVELS:
        stage_results=[r for r in run['results'] if r.get('level')==stage]
        if stage_results:
            stage_rows.append({tr('Level','Tahap'):stage,tr('Correct','Betul'):f"{sum(r['correct'] for r in stage_results)}/{len(stage_results)}",tr('Questions with hints','Soalan dengan petunjuk'):sum(bool(r.get('hint_used')) for r in stage_results)})
    if stage_rows:
        st.dataframe(stage_rows,hide_index=True,width='stretch')
    badges=[tr('Session finisher','Penamat sesi')]
    if correct==total: badges.append(tr('Perfect run','Sesi sempurna'))
    elif correct/total>=.8: badges.append(tr('Strong finish','Penamat cemerlang'))
    st.markdown(''.join(f'<span class="badge">✦ {escape(b)}</span>' for b in badges),unsafe_allow_html=True)
    if run['consent'] and not run['saved']:
        try: save(run);run['saved']=True
        except Exception: st.warning(tr('Saving failed. Your download is still available; use Retry save.','Penyimpanan gagal. Muat turun masih tersedia; gunakan Cuba simpan semula.'))
    if run['consent'] and not run['saved'] and st.button(tr('Retry save','Cuba simpan semula')): st.rerun()
    if run['saved']: st.caption(tr('Saved privately for your teacher.','Disimpan secara peribadi untuk guru anda.'))
    export=[dict(nickname=run['name'],track=run['track'],session_mode=run['level'],**r) for r in run['results']]
    st.download_button(tr('Download my results CSV','Muat turun keputusan CSV'),csv_bytes(export),'AddMath_My_Results.csv','text/csv')
    weak=list(dict.fromkeys(r['topic'] for r in run['results'] if not r['correct']))
    if weak: st.info(tr('Next practice: ','Latihan seterusnya: ')+', '.join(title(k,language) for k in weak))
    with st.expander(tr('Review every worked solution','Semak setiap penyelesaian')):
        for i,(q,r) in enumerate(zip(run['questions'],run['results']),1):
            st.markdown(f'### {i}. '+title(q['topic'],language));text(q['en'],q['bm']);st.latex(q['latex']);st.caption(tr('Your answer: ','Jawapan anda: ')+', '.join(r['response']));worked(q);st.divider()
    c1,c2=st.columns(2)
    missed=[q for q,r in zip(run['questions'],run['results']) if not r['correct']]
    if c1.button(tr('Retry missed questions','Cuba semula soalan salah'),disabled=not missed):
        st.session_state.run={**run,'id':uuid4().hex,'questions':missed,'index':0,'results':[],'hint':False,'saved':False,'started':time.time()};st.rerun()
    if c2.button(tr('New session','Sesi baharu')): del st.session_state['run'];st.rerun()
    st.stop()

q=run['questions'][run['index']];answered=len(run['results'])>run['index']
markers=''.join(f'<div class="node {"done" if i<len(run["results"]) else "current" if i==run["index"] else ""}">{i+1}</div>' for i in range(len(run['questions'])))
st.markdown('<div class="mission">'+markers+'</div>',unsafe_allow_html=True)
st.caption(run['track']+' · '+title(q['topic'],language)+' · '+tr(q['level'],{'Warm-up':'Pemanasan','Level up':'Naik tahap','Boss mode':'Cabaran utama'}[q['level']]))
st.caption(tr(*LEVEL_DESCRIPTIONS[q['level']]))
st.markdown(f'### {tr("Challenge","Cabaran")} {run["index"]+1}/{len(run["questions"])}')
text(q['en'],q['bm']);st.latex(q['latex'])
if not answered:
    st.caption(tr('Use numbers only, e.g. 1/2, sqrt(3), 2*pi/3. Use * for multiplication. Functions sin/cos/tan use radians. Exact forms are accepted; round only when requested.','Gunakan nombor sahaja, contohnya 1/2, sqrt(3), 2*pi/3. Gunakan * untuk pendaraban. Fungsi sin/cos/tan menggunakan radian. Bentuk tepat diterima; bundarkan hanya apabila diminta.'))
    shown=int(run['hint'])
    label=tr('Show a hint (−3 XP if correct)','Tunjuk petunjuk (−3 XP jika betul)') if not shown else tr('Show the next hint (no extra XP penalty)','Tunjuk petunjuk seterusnya (tiada penalti XP tambahan)')
    if st.button(label,disabled=shown>=len(q['hints'])):
        run['hint']=shown+1;st.rerun()
    for i,hint in enumerate(q['hints'][:int(run['hint'])],1):
        st.info(f'{tr("Hint","Petunjuk")} {i}: '+tr(*hint))
    with st.form(run['id']+q['id']):
        responses=[st.text_input(tr(*label)+(f' {i+1}' if len(q['labels'])>1 else ''),key=run['id']+q['id']+str(i)) for i,label in enumerate(q['labels'])]
        submitted=st.form_submit_button(tr('Check my answer →','Semak jawapan saya →'),type='primary')
    if submitted:
        try: correct=check(responses,q)
        except ValueError:
            st.warning(tr('Complete each field with a valid real number or arithmetic expression.','Lengkapkan setiap medan dengan nombor nyata atau ungkapan aritmetik yang sah.'))
        else:
            points=[10,15,20][LEVELS.index(q['level'])]-3*int(bool(run['hint']))
            run['results'].append({'question':q['id'],'topic':q['topic'],'response':responses,'correct':correct,'xp':points if correct else 0,'hint_used':bool(run['hint']),'hints_viewed':int(run['hint']),'level':q['level']})
            st.rerun()
else:
    r=run['results'][run['index']]
    if r['correct']: st.success(tr(f'Clean solve. +{r["xp"]} XP',f'Penyelesaian tepat. +{r["xp"]} XP'))
    else: st.info(tr('A useful miss. Study the method, then take the next rep.','Kesilapan membantu pembelajaran. Fahami kaedah, kemudian teruskan latihan.'))
    st.caption(tr('Your answer: ','Jawapan anda: ')+', '.join(r['response']))
    worked(q)
    if st.button(tr('See my results →','Lihat keputusan →') if run['index']==len(run['questions'])-1 else tr('Next challenge →','Cabaran seterusnya →'),type='primary'):
        run['index']+=1;run['hint']=False;st.rerun()
