"""Question-specific vector diagrams rendered as PNGs from generator givens.

No equations are parsed and no external image assets are required. Unknown
quantities are labelled symbolically rather than with the stored answers.
"""
import math
from threading import RLock

_RENDER_LOCK = RLock()


VISUAL_TOPICS = {'functions','logarithms','linear_law','quadratics','straight_lines','coordinates','circles','circular',
                 'trig','triangles','vectors','calculus','differentiation',
                 'integration','kinematics','linear_programming','simultaneous'}


def specification(topic, level, variant, ctx):
    """Build a serialisable drawing specification from the question's own values."""
    if topic not in VISUAL_TOPICS:
        return None
    a,b,k=ctx['a'],ctx['b'],ctx['k']
    warm=level=='Warm-up'; boss=level=='Boss mode'; v=variant%3
    x=ctx.get('x',ctx.get('t',2)); t=ctx.get('t',x)
    def curve(coeff, domain, label='y', shade=None, points=None):
        return dict(kind='graph',curves=[dict(coeff=[float(z) for z in coeff],label=label)],
                    domain=list(domain),shade=shade,points=points or [])
    def geometry(points, edges=None, arrows=None, circles=None, lines=None):
        return dict(kind='geometry',points=points,edges=edges or [],arrows=arrows or [],
                    circles=circles or [],lines=lines or [])
    def point(name, xx, yy, given=True):
        return dict(name=name,x=float(xx),y=float(yy),given=given)
    if topic=='functions':
        if warm and v<2:
            return curve([a,b],(-2,x+2),label='f(x)')
        end=max(6,t+3,k+t+1)
        if boss:
            return dict(kind='graph',domain=[0,end],curves=[
                dict(coeff=[1,-2*k,k*k+b],label='f(x)',domain=[k,end]),
                dict(coeff=[a,b],label='g(x)')],points=[],shade=None)
        return dict(kind='graph',domain=[0,end],curves=[
            dict(coeff=[a,b],label='f(x)'),dict(coeff=[1,0,k],label='g(x)')],points=[],shade=None)
    if topic=='logarithms':
        if boss:
            return dict(kind='graph',domain=[0,2*ctx['hours']],curves=[
                dict(func='exp',scale=ctx['initial'],rate=math.log(2)/ctx['hours'],label='N(t)')],
                points=[],shade=None,x_label='t (h)',y_label='N(t)')
        if not warm:
            return dict(kind='graph',domain=[b+.05,ctx['root']+3],curves=[
                dict(func='log_product',base=a,shift=b,label='log sum')],points=[],shade=None)
        if v==0:
            return dict(kind='graph',domain=[0,k+1],curves=[
                dict(func='exp',scale=a**b,rate=math.log(a),label='exponential')],points=[],shade=None)
        end=a**k if v==1 else a**b*k
        return dict(kind='graph',domain=[.1,max(3,end)],curves=[
            dict(func='log',base=a if v==1 else math.e,label='logarithm')],points=[],shade=None)
    if topic=='linear_law':
        if warm:
            coeff=[3,b] if v==0 else [a,b] if v==1 else [a,k]
            result=curve(coeff,(0,3))
            result['x_label']='log₁₀ x' if v==0 else 'x'
            result['y_label']='log₁₀ y' if v==0 else 'y/x' if v==1 else 'ln y'
            return result
        if boss:
            result=curve([a,a*k*k],(0,5));result['x_label']='X = x²';result['y_label']='Y = xy'
            return result
        result=curve([ctx['power'],math.log(ctx['coeff'])],(0,math.log(4)))
        result['x_label']='ln x';result['y_label']='ln y'
        return result
    if topic=='quadratics':
        if warm:
            if v==0:
                r,s=ctx['r'],ctx['s']; return curve([1,-r-s,r*s],(r-2,s+2))
            if v==1:
                m=ctx['mid']; return curve([a,-2*a*m,a*m*m+b],(m-3,m+3))
            return curve([a,b,-k],(-4,4))
        if not boss:
            return curve([a,-2*a*b,a*(b*b-k*k)],(b-k-2,b+k+2))
        length=ctx['length']
        # A schematic pen: no optimal side lengths are used or displayed.
        return dict(kind='pen',length=length)
    if topic in ('straight_lines','coordinates'):
        if warm and v==1:
            return curve([a,b],(-3,5))
        if boss:
            pts=[point('A',0,0),point('B',2*a,0),point('C',b,2*k)]
            # The unknown circumcentre and circle are deliberately not drawn.
            return geometry(pts,[(0,1),(1,2),(2,0)])
        if warm and v==2:
            pts=[point('A',a,b),point('B',k,x)]
        elif warm:
            pts=[point('A',b,k),point('B',b+a,k+a*x)]
        else:
            pts=[point('A',b,k-a),point('B',b+2*a,k+a)]
        return geometry(pts,[(0,1)])
    if topic=='simultaneous':
        if warm:
            if v<2:
                yy=ctx['y']
                return dict(kind='graph',domain=[x-4,x+4],curves=[
                    dict(coeff=[-a,a*x+yy],label='1'),dict(coeff=[1,-(x-yy)],label='2')],points=[],shade=None)
            return None # The product relation is kept in equations, not an incomplete plot.
        if not boss:
            return None
        return dict(kind='graph',domain=[ctx['u']-2,ctx['v']+2],curves=[
            dict(coeff=[k,b],label='line'),dict(coeff=[1,ctx['c'],ctx['const']],label='curve')],points=[],shade=None)
    if topic=='circles':
        if warm and v==2:
            ax,ay=b,x; bx,by=b+6*a,x+8*a
            return geometry([point('A',ax,ay),point('B',bx,by)],[(0,1)],
                            circles=[dict(x=(ax+bx)/2,y=(ay+by)/2,r=5*a)])
        if warm:
            # Do not print centre coordinates when the question asks for them.
            return geometry([point('C',a,-b,False)],circles=[dict(x=a,y=-b,r=k)])
        if not boss:
            return geometry([],circles=[dict(x=b,y=k,r=a+k)],lines=[dict(m=0,c=k)])
        rad=ctx['rad']; px=ctx['px']; py=ctx['py']
        return geometry([point('C',b,k,False),point('T',px,py),point('P',b+rad+k,k)],
                        edges=[(0,1),(0,2)],circles=[dict(x=b,y=k,r=rad)])
    if topic=='circular':
        if warm:
            theta=float(ctx['theta']) if v<2 else float(b)
            if v<2:
                given=ctx['theta']
                exact=str(given.numerator) if given.denominator==1 else rf'\frac{{{given.numerator}}}{{{given.denominator}}}'
                label=rf'$\theta = {exact}\,\mathrm{{rad}}$'
            else:
                label='θ'
            return dict(kind='sector',inner=0,outer=a,theta=theta,angle_label=label,
                        outer_label=f'r = {a}',inner_label=None)
        if not boss:
            return dict(kind='sector',inner=0,outer=a,theta=float(ctx['theta']),
                        angle_label='θ',outer_label=f'r = {a}',inner_label=None)
        return dict(kind='sector',inner=ctx['inner'],outer=ctx['outer'],theta=float(ctx['theta']),
                    angle_label='θ',outer_label=f'R = {ctx["outer"]}',inner_label=f'r = {ctx["inner"]}')
    if topic=='triangles':
        if warm:
            if v==2:
                return dict(kind='triangles',triangles=[dict(points=[[0,a*math.sqrt(3)],[0,0],[a,0]],
                    names=['A','B','C'],sides=['c','a = '+str(a),'b'],angles=['30°','90°',''])])
            ang=math.pi/3 if v==0 else math.pi/2
            return dict(kind='triangles',triangles=[dict(points=[[b*math.cos(ang),b*math.sin(ang)],[a,0],[0,0]],
                names=['A','B','C'],sides=['c',f'a = {a}',f'b = {b}'],angles=['','', '60°' if v==0 else '90°'])])
        if not boss:
            return dict(kind='triangles',triangles=[dict(points=[[0,0],[a,0],[(a+k)/2,(a+k)*math.sqrt(3)/2]],
                names=['A','B','C'],sides=[f'{a}','?',f'{a+k}'],angles=['60°','',''])])
        side=ctx['side']; opposite=float(ctx['opposite']); ang=math.pi/6
        base=opposite*math.cos(ang); gap=math.sqrt(side*side-(opposite*math.sin(ang))**2)
        tris=[]
        for length in (base+gap,base-gap):
            tris.append(dict(points=[[0,0],[length*math.cos(ang),length*math.sin(ang)],[opposite,0]],
                             names=['A','B','C'],sides=['c',f'a = {side}',f'b = {opposite:g}'],angles=['30°','','']))
        return dict(kind='triangles',triangles=tris)
    if topic=='vectors':
        if warm and v==0:
            return geometry([point('O',0,0,False),point('u',3*a,4*a)],arrows=[(0,1)])
        if warm and v==1:
            return geometry([point('O',0,0,False),point('u',a,b),point('v',k,x)],arrows=[(0,1),(0,2)])
        if warm:
            ax,ay=a,b; bx,by=k,x
            return geometry([point('A',ax,ay),point('B',bx,by),point('M',(2*ax+bx)/3,(2*ay+by)/3,False)],[(0,1)])
        if not boss:
            return geometry([point('A',b,k),point('B',ctx['vx'],ctx['vy']),point('M',b+a,k+t,False)],[(0,1)])
        ux,uy,vx,vy=ctx['ux'],ctx['uy'],ctx['vx'],ctx['vy']
        pts=[point('O',0,0,False),point('A',ux,uy),point('B',vx,vy),
             point('P',(2*ux+vx)/3,(2*uy+vy)/3,False),point('Q',2*ux+vx,2*uy+vy,False)]
        return geometry(pts,edges=[(1,2),(2,4),(0,4)],arrows=[(0,1),(0,2)])
    if topic=='trig':
        if warm and v>0:
            return dict(kind='graph',domain=[0,2*math.pi],curves=[dict(
                func='sin' if v==1 else 'cos',scale=a,rate=b,offset=k if v==1 else -k,label='y')],
                points=[],shade=None,x_label='x (rad)')
        # Symbolic unit-circle sketch avoids printing the requested angles or period.
        return dict(kind='unit_circle')
    if topic in ('calculus','differentiation','integration','kinematics'):
        sub=ctx['sub']
        if sub=='differentiation':
            if warm:
                coeff=[a,0,b,0] if v==0 else [a,-2*a*b,k] if v==1 else [a*a,2*a*b,b*b]
                return curve(coeff,(-2,max(4,x+2)))
            if not boss:
                return curve([a,0,b],(-2,t+2))
            return curve([a,-float(ctx['coeff']),ctx['lin'],t],(0,ctx['v']+1))
        if sub=='integration':
            if warm:
                if v==0:
                    upper=ctx['upper']; return curve([a,k],(0,upper),shade=[0,upper])
                if v==1:
                    return curve([3*a,0,0],(0,b),shade=[0,b])
                # Show the given derivative, not the curve whose constant is unknown.
                return curve([2*a,0],(0,x+1),label='dy/dx')
            if not boss:
                return curve([2*a,b],(0,t+1),label='dy/dx')
            end=ctx['upper']; return curve([1,-(b+end),b*end],(0,end),shade=[0,end])
        if warm:
            if v==0:return curve([a,b,0],(0,x+1),label='s(t)')
            if v==1:return curve([a,0,b],(0,x+1),label='v(t)')
            return curve([2*a,b],(0,x),label='v(t)',shade=[0,x])
        if not boss:
            return curve([2*a,0],(0,t),label='a(t)')
        end=ctx['end']; return curve([a,-a*ctx['u']],(0,end),label='v(t)',shade=[0,end])
    if topic=='linear_programming':
        if warm and v==0:
            return dict(kind='feasible',constraints=[[1,1,k]],domain=[0,k,0,k],integer=False)
        if warm and v==1:
            return dict(kind='feasible',constraints=[[-1,-1,-k]],domain=[0,k*1.8,0,k*1.8],integer=False,unbounded=True)
        if warm:
            return dict(kind='feasible',constraints=[[1,0,a],[0,1,b]],domain=[0,a*1.2,0,b*1.2],integer=False)
        c1,c2=ctx['c1'],ctx['c2']
        return dict(kind='feasible',constraints=[[2,1,c1],[1,2,c2]],
                    domain=[0,c1/2*1.15,0,c2/2*1.15],integer=boss)
    return None


def render(spec, language='Bilingual'):
    # Matplotlib drawing is serialised across concurrent Streamlit sessions.
    with _RENDER_LOCK:
        return _render(spec, language)


def _render(spec, language='Bilingual'):
    """Return an in-memory high-resolution PNG; close every figure after rendering."""
    import io
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon, Circle, Arc
    from matplotlib.ticker import MaxNLocator
    colors=['#ceff75','#bd9efa','#80d6ea']; fg='#f5f3ff'; bg='#20232f'
    def tr(en,bm):return en if language=='English' else bm if language=='Bahasa Melayu' else en+' / '+bm
    count=len(spec['triangles']) if spec['kind']=='triangles' else 1
    fig,axes=plt.subplots(count,1,figsize=(9,4.8 if count==1 else 7.5),squeeze=False,facecolor=bg)
    def base(ax,geometric=False):
        ax.set_facecolor(bg)
        ax.tick_params(colors=fg,labelsize=10)
        ax.xaxis.get_offset_text().set_color(fg)
        ax.yaxis.get_offset_text().set_color(fg)
        for spine in ax.spines.values():spine.set_color('#606679')
        if geometric:
            ax.set_aspect('equal',adjustable='box');ax.axis('off')
        else:
            ax.grid(alpha=.18,color=fg);ax.axhline(0,color='#959bad',lw=1);ax.axvline(0,color='#959bad',lw=1)
            ax.xaxis.set_major_locator(MaxNLocator(nbins=7));ax.yaxis.set_major_locator(MaxNLocator(nbins=6))
        ax.margins(.18)
    def label(ax,x,y,s,dx=8,dy=8):
        ax.annotate(s,(x,y),xytext=(dx,dy),textcoords='offset points',color=fg,fontsize=11,
                    bbox=dict(boxstyle='round,pad=.2',facecolor=bg,edgecolor='none',alpha=.88))
    try:
        kind=spec['kind']; ax=axes[0,0];base(ax,kind in ('sector','triangles','pen','unit_circle'))
        if kind=='graph':
            lo,hi=spec['domain']; xs=np.linspace(lo,hi,500)
            for i,entry in enumerate(spec['curves']):
                xx=np.linspace(*entry.get('domain',[lo,hi]),500)
                fn=entry.get('func')
                if fn=='exp':ys=entry['scale']*np.exp(entry['rate']*xx)
                elif fn=='log':ys=np.log(xx)/math.log(entry['base'])
                elif fn=='log_product':ys=np.log((xx-entry['shift'])*(xx+entry['shift']))/math.log(entry['base'])
                elif fn in ('sin','cos'):ys=entry['scale']*(np.sin if fn=='sin' else np.cos)(entry['rate']*xx)+entry['offset']
                else:ys=np.polyval(entry['coeff'],xx)
                name=entry['label']; name=tr('Line','Garis') if name=='line' else tr('Curve','Lengkung') if name=='curve' else name
                name={'exponential':tr('Exponential','Eksponen'),'logarithm':tr('Logarithm','Logaritma'),
                      'log sum':tr('Logarithm sum','Hasil tambah logaritma')}.get(name,name)
                ax.plot(xx,ys,color=colors[i%3],lw=2.5,label=name)
                if spec.get('shade'):
                    left,right=spec['shade'];mask=(xx>=left)&(xx<=right)
                    ax.fill_between(xx,0,ys,where=mask,color=colors[i%3],alpha=.18)
            ax.set_xlim(lo,hi);ax.legend(facecolor=bg,edgecolor='#555d70',labelcolor=fg)
            time=spec['curves'][0]['label'] in ('s(t)','v(t)','a(t)')
            ax.set_xlabel(spec.get('x_label',tr('Time t (s)','Masa t (s)') if time else 'x'),color=fg)
            name=spec['curves'][0]['label']
            units={'s(t)':'m','v(t)':'m/s','a(t)':'m/s²'}
            ax.set_ylabel(spec.get('y_label',name+' ('+units[name]+')' if time else 'dy/dx' if name=='dy/dx' else 'y'),color=fg)
        elif kind=='geometry':
            ax.set_aspect('equal',adjustable='box')
            pts=spec['points']
            for edge in spec['edges']:
                p,r=pts[edge[0]],pts[edge[1]];ax.plot([p['x'],r['x']],[p['y'],r['y']],color=colors[1],lw=2)
            for edge in spec['arrows']:
                p,r=pts[edge[0]],pts[edge[1]]
                ax.annotate('',(r['x'],r['y']),(p['x'],p['y']),arrowprops=dict(arrowstyle='->',color=colors[0],lw=2.5))
            bounds=[]
            labelled=set()
            for p in pts:
                ax.plot(p['x'],p['y'],'o',color=colors[0],ms=5)
                coord=(p['x'],p['y'])
                bounds.append(coord)
                if coord not in labelled:
                    labelled.add(coord)
                    group=[z for z in pts if (z['x'],z['y'])==coord]
                    name='\n'.join(z['name']+(f" ({z['x']:g}, {z['y']:g})" if z['given'] else '') for z in group)
                    label(ax,p['x'],p['y'],name)
            for c in spec['circles']:
                ax.add_patch(Circle((c['x'],c['y']),c['r'],fill=False,edgecolor=colors[0],lw=2.5))
                bounds.extend([(c['x']-c['r'],c['y']-c['r']),(c['x']+c['r'],c['y']+c['r'])])
            if bounds:
                xx,yy=zip(*bounds);xr=max(max(xx)-min(xx),2);yr=max(max(yy)-min(yy),2)
                ax.set_xlim(min(xx)-xr*.25,max(xx)+xr*.3);ax.set_ylim(min(yy)-yr*.25,max(yy)+yr*.3)
            for line in spec['lines']:
                xx=np.linspace(*ax.get_xlim(),200);ax.plot(xx,line['m']*xx+line['c'],color=colors[1],lw=2)
            ax.set_xlabel('x',color=fg);ax.set_ylabel('y',color=fg)
        elif kind=='sector':
            ri,ro,angle=spec['inner'],spec['outer'],spec['theta']
            ts=np.linspace(0,angle,200);out=np.c_[ro*np.cos(ts),ro*np.sin(ts)]
            inn=np.c_[ri*np.cos(ts[::-1]),ri*np.sin(ts[::-1])] if ri else np.array([[0,0]])
            ax.add_patch(Polygon(np.vstack([out,inn]),closed=True,facecolor='#bd9efa40',edgecolor=colors[1],lw=2.5))
            ax.plot(0,0,'o',color=fg);label(ax,0,0,'O',-14,-14)
            label(ax,ro*.62,0,spec['outer_label'],0,-25)
            if ri:label(ax,ri*.6*math.cos(angle),ri*.6*math.sin(angle),spec['inner_label'],-20,12)
            rr=max(ri*.4,ro*.18)
            ax.add_patch(Arc((0,0),2*rr,2*rr,theta1=0,theta2=math.degrees(angle),edgecolor=colors[0],lw=1.5))
            label(ax,rr*math.cos(angle/2),rr*math.sin(angle/2),spec['angle_label'],4,4)
            ax.update_datalim(np.vstack([out,inn,[[0,0]]]));ax.autoscale_view();ax.margins(.3)
        elif kind=='triangles':
            for i,tri in enumerate(spec['triangles']):
                aa=axes[i,0];base(aa,True);pts=np.asarray(tri['points'],float)
                aa.add_patch(Polygon(pts,closed=True,facecolor='#bd9efa22',edgecolor=colors[1],lw=2.3))
                centre=pts.mean(axis=0)
                for j,p in enumerate(pts):
                    direction=p-centre; norm=np.linalg.norm(direction); offset=direction/max(norm,1e-10)*17
                    label(aa,*p,tri['names'][j],offset[0],offset[1])
                    end=pts[(j+1)%3];mid=(p+end)/2; outward=mid-centre;outward/=max(np.linalg.norm(outward),1e-10)
                    label(aa,*mid,tri['sides'][j],outward[0]*24,outward[1]*24)
                    if tri['angles'][j]:
                        toward=centre-p;toward/=max(np.linalg.norm(toward),1e-10)
                        short=min(np.linalg.norm(p-pts[(j+1)%3]),np.linalg.norm(p-pts[(j+2)%3]))
                        pos=p+toward*short*.24
                        if count>1:
                            label(aa,*p,tri['angles'][j],22,-30)
                        else:
                            label(aa,*pos,tri['angles'][j],0,0)
                aa.update_datalim(pts);aa.autoscale_view();aa.margins(.38)
                if count>1:aa.set_title(tr(f'Possible triangle {i+1}',f'Segi tiga mungkin {i+1}'),color=fg,fontsize=11)
        elif kind=='pen':
            ax.add_patch(Polygon([[0,0],[5,0],[5,3],[0,3]],fill=False,edgecolor=colors[0],lw=3))
            ax.plot([-1,6],[3,3],color=colors[1],lw=8)
            label(ax,2.5,3,tr('Wall — no fence','Dinding — tiada pagar'),-50,18)
            label(ax,0,1.5,'x',-28,0);label(ax,5,1.5,'x',12,0);label(ax,2.5,0,'y',0,-25)
            ax.set_xlim(-1.5,6.5);ax.set_ylim(-1.3,4.3)
            ax.set_title(tr(f'Three fenced sides: {spec["length"]} m',f'Tiga sisi berpagar: {spec["length"]} m'),color=fg,fontsize=12)
        elif kind=='unit_circle':
            ax.add_patch(Circle((0,0),1,fill=False,edgecolor=colors[1],lw=2.5))
            angle=.85;xx,yy=math.cos(angle),math.sin(angle)
            ax.plot([0,xx],[0,yy],color=colors[0],lw=2.5);ax.plot([xx,xx],[0,yy],'--',color=colors[2])
            ax.plot([-1.2,1.2],[0,0],color=fg,lw=1);ax.plot([0,0],[-1.2,1.2],color=fg,lw=1)
            ax.add_patch(Arc((0,0),.5,.5,theta1=0,theta2=math.degrees(angle),edgecolor=colors[0]))
            label(ax,.25,.13,'u');label(ax,xx,yy,'(cos u, sin u)');label(ax,1.12,0,'x');label(ax,0,1.12,'y')
            ax.set_xlim(-1.4,1.8);ax.set_ylim(-1.3,1.4)
            ax.set_title(tr('Reference sketch — u is a general angle','Lakaran rujukan — u ialah sudut umum'),color=fg,fontsize=12)
        elif kind=='feasible':
            lo,hi,bottom,top=spec['domain'];xx=np.linspace(lo,hi,450);yy=np.linspace(bottom,top,450)
            X,Y=np.meshgrid(xx,yy);mask=np.ones_like(X,dtype=bool)
            for i,(p,r,c) in enumerate(spec['constraints']):
                mask&=p*X+r*Y<=c+1e-9
                if r:ax.plot(xx,(c-p*xx)/r,color=colors[i%3],lw=2,label=f'{p:g}x + {r:g}y = {c:g}')
                else:ax.axvline(c/p,color=colors[i%3],lw=2,label=f'x = {c/p:g}')
            ax.contourf(X,Y,mask.astype(float),levels=[.5,1.5],colors=['#bd9efa'],alpha=.22)
            if spec['integer']:
                lattice=[(i,j) for i in range(math.floor(hi)+1) for j in range(math.floor(top)+1)
                         if all(p*i+r*j<=c+1e-9 for p,r,c in spec['constraints'])]
                if lattice:
                    xxp,yyp=zip(*lattice);ax.scatter(xxp,yyp,color=colors[0],s=16,zorder=4)
            ax.set_xlim(lo,hi);ax.set_ylim(bottom,top);ax.set_aspect('equal',adjustable='box')
            ax.set_xlabel('x',color=fg);ax.set_ylabel('y',color=fg)
            ax.legend(facecolor=bg,edgecolor='#555d70',labelcolor=fg,fontsize=10)
            ax.set_title(tr('Feasible region (shaded)','Rantau tersaur (berlorek)')+(tr(' — continues beyond view',' — berterusan di luar paparan') if spec.get('unbounded') else ''),color=fg,fontsize=12)
        else:
            raise ValueError('Unknown diagram kind: '+kind)
        fig.tight_layout(pad=2)
        output=io.BytesIO();fig.savefig(output,format='png',dpi=160,facecolor=bg)
        return output.getvalue()
    finally:
        plt.close(fig)


def caption(spec):
    if spec['kind']=='unit_circle':
        return ('General reference sketch; the marked angle is not a numerical solution.',
                'Lakaran rujukan umum; sudut ditanda bukan penyelesaian berangka.')
    if spec['kind']=='pen':
        return ('Schematic, not to scale. Side lengths x and y are unknown.',
                'Rajah skematik, tidak mengikut skala. Panjang sisi x dan y tidak diketahui.')
    return ('Diagram matches the generated givens. Compute your answers; do not estimate them from the image.',
            'Rajah sepadan dengan maklumat soalan terjana. Hitung jawapan anda; jangan anggarkannya daripada imej.')
