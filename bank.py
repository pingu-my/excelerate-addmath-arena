"""Original bilingual practice questions. Every displayed menu has live generators."""
import math
import random
from fractions import Fraction
from curriculum import LEVELS, PROGRESSION, topics_for
from progression import advanced
from diagrams import specification


def latex_number(value):
    if isinstance(value, Fraction):
        return str(value.numerator) if value.denominator == 1 else rf'\dfrac{{{value.numerator}}}{{{value.denominator}}}'
    if isinstance(value, int) or float(value).is_integer():
        return str(int(value))
    return f'{float(value):.6g}'


def make(topic, level, variant, rng):
    if level != LEVELS[0]:
        return advanced(topic, level, variant, rng)
    d = LEVELS.index(level)
    a,b,k = rng.randint(2,5+2*d),rng.randint(1,5+d),rng.randint(2,5+d)
    x = rng.randint(1,4+d)
    v = variant % 3
    def q(en,bm,expression,answer,hint_en,hint_bm,steps,labels=None,unordered=False,tolerance=1e-7,context=None):
        answers = answer if isinstance(answer, list) else [answer]
        return {'topic':topic,'level':level,'variant':v,'en':en,'bm':bm,'latex':expression,
                'answers':[float(z) for z in answers],'answer_latex':[latex_number(z) for z in answers],
                'hints':[(hint_en,hint_bm)],'steps':steps,'labels':labels or [('Answer','Jawapan')]*len(answers),
                'unordered':unordered,'tolerance':tolerance,
                'diagram':specification(topic,level,v,context)}
    if topic == 'functions':
        if v == 0:
            return q(f'Find f({x}).',f'Cari f({x}).',rf'f(x)={a}x+{b}',a*x+b,'Substitute the input into the function.','Gantikan input ke dalam fungsi.',[('Substitute.','Gantikan.',rf'f({x})={a}({x})+{b}={a*x+b}')], context=locals())
        if v == 1:
            return q(f'Find f⁻¹({a*x+b}).',f'Cari f⁻¹({a*x+b}).',rf'f(x)={a}x+{b}',x,'Undo addition, then multiplication.','Songsangkan penambahan, kemudian pendaraban.',[('Rearrange y = ax + b.','Susun semula y = ax + b.',rf'f^{{-1}}(y)=\dfrac{{y-{b}}}{{{a}}}'),('Substitute the given value.','Gantikan nilai diberi.',rf'f^{{-1}}({a*x+b})={x}')], context=locals())
        return q(f'Find f(g({x})).',f'Cari f(g({x})).',rf'f(x)={a}x+{b},\quad g(x)=x^2+{k}',a*(x*x+k)+b,'Calculate g first, then apply f.','Hitung g dahulu, kemudian gunakan f.',[('Evaluate the inner function.','Nilai fungsi dalaman.',rf'g({x})={x*x+k}'),('Apply f to that value.','Gunakan f pada nilai itu.',rf'f(g({x}))={a}({x*x+k})+{b}={a*(x*x+k)+b}')], context=locals())
    if topic == 'quadratics':
        r,s=sorted(rng.sample(range(-5-d,7+d),2)); mid=rng.randint(-4,4)
        if v == 0:
            return q('Find both real roots. Order does not matter.','Cari kedua-dua punca nyata. Turutan tidak penting.',rf'x^2-({r+s})x+({r*s})=0',[r,s],'Factorise using two numbers with the required sum and product.','Faktorkan menggunakan dua nombor dengan hasil tambah dan hasil darab yang sesuai.',[('Factorise.','Faktorkan.',rf'(x-({r}))(x-({s}))=0'),('Set each factor to zero.','Samakan setiap faktor dengan sifar.',rf'x={r}\quad\mathrm{{or}}\quad x={s}')],unordered=True, context=locals())
        if v == 1:
            return q('Find the minimum value of y.','Cari nilai minimum y.',rf'y={a}(x-({mid}))^2+{b}',b,'A square is non-negative.','Kuasa dua adalah tidak negatif.',[('The square is zero at the turning point.','Kuasa dua ialah sifar pada titik pusingan.',rf'x={mid},\quad y_{{\min}}={b}')], context=locals())
        return q('Find the discriminant.','Cari diskriminan.',rf'{a}x^2+{b}x-{k}=0',b*b+4*a*k,'Use b² − 4ac.','Gunakan b² − 4ac.',[('Identify the three coefficients.','Kenal pasti tiga pekali.',rf'\Delta={b}^2-4({a})(-{k})={b*b+4*a*k}')], context=locals())
    if topic == 'polynomials':
        if v == 0:
            return q(f'Find the remainder when P(x) is divided by x − {x}.',f'Cari baki apabila P(x) dibahagi dengan x − {x}.',rf'P(x)=x^3+{a}x^2-{b}x+{k}',x**3+a*x*x-b*x+k,'The remainder is P(c) for divisor x − c.','Baki ialah P(c) bagi pembahagi x − c.',[('Apply the remainder theorem.','Gunakan teorem baki.',rf'P({x})={x}^3+{a}({x})^2-{b}({x})+{k}={x**3+a*x*x-b*x+k}')], context=locals())
        if v == 1:
            return q(f'Find c if x − {x} is a factor of P(x).',f'Cari c jika x − {x} ialah faktor P(x).',rf'P(x)=x^3+{a}x+c',-x**3-a*x,'A factor gives zero remainder.','Faktor memberikan baki sifar.',[('Set P(cut point) to zero.','Samakan nilai polinomial pada punca dengan sifar.',rf'{x}^3+{a}({x})+c=0\Rightarrow c={-x**3-a*x}')], context=locals())
        roots=sorted(rng.sample(range(-6,7),3))
        return q('Find all three roots. Order does not matter.','Cari ketiga-tiga punca. Turutan tidak penting.',''.join(rf'(x-({r}))' for r in roots)+'=0',roots,'Set each linear factor to zero.','Samakan setiap faktor linear dengan sifar.',[('Use the zero-product rule.','Gunakan hukum hasil darab sifar.',r'x\in\{'+','.join(map(str,roots))+r'\}')],unordered=True, context=locals())
    if topic == 'equations':
        if v == 0:
            return q('Solve for both values of x. Order does not matter.','Selesaikan kedua-dua nilai x. Turutan tidak penting.',rf'|{a}x-{b}|={k}',[Fraction(b+k,a),Fraction(b-k,a)],'Consider both signs of the quantity inside the modulus.','Pertimbangkan kedua-dua tanda bagi kuantiti dalam modulus.',[('Write two linear equations.','Tulis dua persamaan linear.',rf'{a}x-{b}=\pm{k}'),('Solve each equation.','Selesaikan setiap persamaan.',rf'x=\dfrac{{{b}+{k}}}{{{a}}}\quad\mathrm{{or}}\quad x=\dfrac{{{b}-{k}}}{{{a}}}')],unordered=True, context=locals())
        if v == 1:
            return q('Find the lower and upper boundaries of the solution interval, in that order.','Cari sempadan bawah dan atas selang penyelesaian, mengikut turutan.',rf'|x-{b}|<{a}',[b-a,b+a],'The distance from b is less than a.','Jarak daripada b adalah kurang daripada a.',[('Rewrite the double inequality.','Tulis semula ketaksamaan berganda.',rf'-{a}<x-{b}<{a}\Rightarrow {b-a}<x<{b+a}')],labels=[('Lower boundary','Sempadan bawah'),('Upper boundary','Sempadan atas')], context=locals())
        return q('Find the positive solution x.','Cari penyelesaian positif x.',rf'x^4-({a*a+b*b})x^2+{a*a*b*b}=0,\quad x>0,\quad x\geq {max(a,b)}',max(a,b),'Let u = x² and factorise the quadratic in u.','Ambil u = x² dan faktorkan kuadratik dalam u.',[('Factorise using x².','Faktorkan menggunakan x².',rf'(x^2-{a*a})(x^2-{b*b})=0'),('Use the stated restrictions.','Gunakan sekatan diberi.',rf'x={max(a,b)}')], context=locals())
    if topic == 'simultaneous':
        y=rng.randint(-3,5+d)
        if v < 2:
            return q('Find x and y, in that order.','Cari x dan y, mengikut turutan.',rf'{a}x+y={a*x+y},\quad x-y={x-y}',[x,y],'Add the equations to eliminate y.','Tambah persamaan untuk menghapuskan y.',[('Add both equations.','Tambah kedua-dua persamaan.',rf'({a}+1)x={a*x+x}\Rightarrow x={x}'),('Substitute x.','Gantikan x.',rf'y=x-({x-y})={y}')],labels=[('x','x'),('y','y')], context=locals())
        return q('Find the positive value of x.','Cari nilai positif x.',rf'y=x+{b},\quad xy={x*(x+b)},\quad x>0',x,'Substitute the linear equation into xy.','Gantikan persamaan linear ke dalam xy.',[('Form a quadratic.','Bentukkan persamaan kuadratik.',rf'x(x+{b})={x*(x+b)}'),('Factorise and select the positive root.','Faktorkan dan pilih punca positif.',rf'(x-{x})(x+{x+b})=0\Rightarrow x={x}')], context=locals())
    if topic in ('logarithms','indices'):
        if v == 0:
            return q('Solve for x.','Selesaikan x.',rf'{a}^{{x+{b}}}={a**(k+b)}',k,'Express both sides using the same base.','Ungkapkan kedua-dua belah dengan asas yang sama.',[('Equate exponents.','Samakan indeks.',rf'x+{b}={k+b}\Rightarrow x={k}')], context=locals())
        if v == 1:
            return q('Solve for x.','Selesaikan x.',rf'\log_{{{a}}}x={k}',a**k,'Use the exponential form of a logarithm.','Gunakan bentuk eksponen bagi logaritma.',[('Convert to exponential form.','Tukar kepada bentuk eksponen.',rf'x={a}^{k}={a**k}')], context=locals())
        if topic == 'indices':
            return q('Find the coefficient of √2 after simplifying.','Cari pekali √2 selepas pemudahan.',rf'\sqrt{{{2*a*a}}}+\sqrt{{{2*b*b}}}',a+b,'Extract the square factors.','Keluarkan faktor kuasa dua.',[('Simplify each surd.','Permudahkan setiap surd.',rf'{a}\sqrt2+{b}\sqrt2=({a+b})\sqrt2')], context=locals())
        return q('Find x.','Cari x.',rf'\ln x={b}\ln {a}+\ln {k}',a**b*k,'Apply the power and product laws of logarithms.','Gunakan hukum kuasa dan hasil darab logaritma.',[('Combine the logarithms.','Gabungkan logaritma.',rf'\ln x=\ln({a}^{b}\cdot{k})\Rightarrow x={a**b*k}')], context=locals())
    if topic in ('straight_lines','coordinates','linear_law'):
        if topic == 'linear_law':
            if v == 0:
                return q('A plot of Y = log₁₀y against X = log₁₀x has gradient 3 and intercept c. Find c.','Plot Y = log₁₀y melawan X = log₁₀x mempunyai kecerunan 3 dan pintasan c. Cari c.',rf'y={10**b}x^3',b,'Take logarithms on both sides.','Ambil logaritma pada kedua-dua belah.',[('Linearise.','Linearkan.',rf'\log_{{10}}y={b}+3\log_{{10}}x\Rightarrow c={b}')], context=locals())
            if v == 1:
                return q('Find the gradient of the straight-line plot of y/x against x.','Cari kecerunan plot garis lurus y/x melawan x.',rf'y={a}x^2+{b}x,\quad x\ne0',a,'Divide through by x.','Bahagikan dengan x.',[('Choose transformed variables.','Pilih pemboleh ubah terubah.',rf'\dfrac yx={a}x+{b}\Rightarrow m={a}')], context=locals())
            return q('A plot of ln y against x has intercept b. Find b.','Plot ln y melawan x mempunyai pintasan b. Cari b.',rf'y=e^{{{k}}}e^{{{a}x}}',k,'Take natural logarithms.','Ambil logaritma asli.',[('Linearise the exponential model.','Linearkan model eksponen.',rf'\ln y={k}+{a}x\Rightarrow b={k}')], context=locals())
        if v == 0:
            return q('Find the gradient of AB.','Cari kecerunan AB.',rf'A=({b},{k}),\quad B=({b+a},{k+a*x})',x,'Gradient is change in y divided by change in x.','Kecerunan ialah perubahan y dibahagi perubahan x.',[('Apply the gradient formula.','Gunakan rumus kecerunan.',rf'm=\dfrac{{{a*x}}}{{{a}}}={x}')], context=locals())
        if v == 1:
            return q('Find the gradient of a line perpendicular to the given line.','Cari kecerunan garis yang berserenjang dengan garis diberi.',rf'y={a}x+{b}',Fraction(-1,a),'Perpendicular gradients multiply to −1.','Hasil darab kecerunan berserenjang ialah −1.',[('Use the negative reciprocal.','Gunakan salingan negatif.',rf'm_2=-\dfrac1{{{a}}}')], context=locals())
        return q('Find the x-coordinate of the midpoint of AB.','Cari koordinat-x titik tengah AB.',rf'A=({a},{b}),\quad B=({k},{x})',Fraction(a+k,2),'Average the two x-coordinates.','Puratakan kedua-dua koordinat-x.',[('Apply the midpoint formula.','Gunakan rumus titik tengah.',rf'x_M=\dfrac{{{a}+{k}}}2={latex_number(Fraction(a+k,2))}')], context=locals())
    if topic == 'circles':
        if v == 0:
            return q('Find the radius.','Cari jejari.',rf'(x-{a})^2+(y+{b})^2={k*k}',k,'The right side is the square of the radius.','Sebelah kanan ialah kuasa dua jejari.',[('Compare with the standard equation.','Bandingkan dengan persamaan piawai.',rf'r^2={k*k}\Rightarrow r={k}')], context=locals())
        if v == 1:
            return q('Find the centre coordinates h and k, in that order.','Cari koordinat pusat h dan k, mengikut turutan.',rf'x^2+y^2-{2*a}x+{2*b}y+{a*a+b*b-k*k}=0',[a,-b],'Complete the square in x and y.','Lengkapkan kuasa dua dalam x dan y.',[('Complete the squares.','Lengkapkan kuasa dua.',rf'(x-{a})^2+(y+{b})^2={k*k}')],labels=[('Centre x','Pusat x'),('Centre y','Pusat y')], context=locals())
        return q('Find the radius of a circle whose diameter endpoints are A and B.','Cari jejari bulatan dengan hujung diameter A dan B.',rf'A=({b},{x}),\quad B=({b+6*a},{x+8*a})',5*a,'Use the distance formula and halve the diameter.','Gunakan rumus jarak dan bahagikan diameter dengan dua.',[('Calculate the diameter.','Hitung diameter.',rf'AB=\sqrt{{({6*a})^2+({8*a})^2}}={10*a}'),('Halve it.','Bahagikan dengan dua.',rf'r={5*a}')], context=locals())
    if topic == 'circular':
        theta=Fraction(rng.choice([1,2,3,4]),3)
        if v == 0:
            return q('Find the arc length in cm. θ is in radians.','Cari panjang lengkok dalam cm. θ dalam radian.',rf'r={a},\quad\theta={latex_number(theta)}',a*theta,'Use s = rθ.','Gunakan s = rθ.',[('Multiply radius by the radian angle.','Darab jejari dengan sudut radian.',rf's={a}\cdot{latex_number(theta)}={latex_number(a*theta)}')], context=locals())
        if v == 1:
            return q('Find the sector area in cm². θ is in radians.','Cari luas sektor dalam cm². θ dalam radian.',rf'r={a},\quad\theta={latex_number(theta)}',Fraction(a*a,2)*theta,'Use A = ½r²θ.','Gunakan A = ½r²θ.',[('Apply the sector formula.','Gunakan rumus sektor.',rf'A=\dfrac12({a})^2\cdot{latex_number(theta)}={latex_number(Fraction(a*a,2)*theta)}')], context=locals())
        return q('A sector has arc length s and radius r. Find its perimeter in cm.','Sektor mempunyai panjang lengkok s dan jejari r. Cari perimeter dalam cm.',rf's={a*b},\quad r={a}',a*b+2*a,'Add the arc and two radii.','Tambah lengkok dan dua jejari.',[('Add all boundary lengths.','Tambah semua panjang sempadan.',rf'P=s+2r={a*b}+2({a})={a*b+2*a}')], context=locals())
    if topic == 'trig':
        if v == 0:
            return q('Find both solutions in degrees. Order does not matter.','Cari kedua-dua penyelesaian dalam darjah. Turutan tidak penting.',r'\sin\theta=\dfrac12,\quad0^\circ\leq\theta\leq180^\circ',[30,150],'Use the reference angle and the sign of sine.','Gunakan sudut rujukan dan tanda sinus.',[('Sine is positive in the first two quadrants.','Sinus positif dalam dua sukuan pertama.',r'\theta=30^\circ,\quad180^\circ-30^\circ=150^\circ')],unordered=True, context=locals())
        if v == 1:
            return q('Find the period in radians.','Cari tempoh dalam radian.',rf'y={a}\sin({b}x)+{k}',2*math.pi/b,'A sine graph has period 2π/b.','Graf sinus mempunyai tempoh 2π/b.',[('Use the coefficient of x.','Gunakan pekali x.',rf'T=\dfrac{{2\pi}}{{{b}}}')],tolerance=0.0005, context=locals())
        return q('Find the maximum value of y.','Cari nilai maksimum y.',rf'y={a}\cos({b}x)-{k}',a-k,'Cosine ranges from −1 to 1.','Julat kosinus ialah −1 hingga 1.',[('Use cos(bx) = 1.','Gunakan cos(bx) = 1.',rf'y_{{\max}}={a}-{k}={a-k}')], context=locals())
    if topic == 'triangles':
        if v == 0:
            return q('Find side c in cm. Angle C is between sides a and b. Round to 3 decimal places.','Cari sisi c dalam cm. Sudut C di antara sisi a dan b. Bundarkan kepada 3 tempat perpuluhan.',rf'a={a},\quad b={b},\quad C=60^\circ',math.sqrt(a*a+b*b-a*b),'Use the cosine rule.','Gunakan petua kosinus.',[('Apply c² = a² + b² − 2ab cos C.','Gunakan c² = a² + b² − 2ab kos C.',rf'c=\sqrt{{{a*a+b*b-a*b}}}')],tolerance=0.0005, context=locals())
        if v == 1:
            return q('Find the triangle area in cm². Angle C lies between the two given sides.','Cari luas segi tiga dalam cm². Sudut C di antara dua sisi diberi.',rf'a={a},\quad b={b},\quad C=90^\circ',Fraction(a*b,2),'Use A = ½ab sin C.','Gunakan A = ½ab sin C.',[('Substitute sin 90° = 1.','Gantikan sin 90° = 1.',rf'A=\dfrac12({a})({b})={latex_number(Fraction(a*b,2))}')], context=locals())
        return q('Find side b in cm, opposite B. Side a is opposite A.','Cari sisi b dalam cm, bertentangan B. Sisi a bertentangan A.',rf'a={a},\quad A=30^\circ,\quad B=90^\circ',2*a,'Use the sine rule.','Gunakan petua sinus.',[('Compare opposite sides and angles.','Bandingkan sisi dan sudut bertentangan.',rf'\dfrac b{{\sin90^\circ}}=\dfrac{{{a}}}{{\sin30^\circ}}\Rightarrow b={2*a}')], context=locals())
    if topic == 'combinatorics':
        n=5+d+rng.randint(0,3); r=rng.randint(2,min(4,n-1))
        if v == 0:
            ans=math.comb(n,r)
            return q(f'Choose {r} members from {n} students. How many different groups are possible?',f'Pilih {r} ahli daripada {n} murid. Berapa kumpulan berlainan boleh dibentuk?',rf'{{{n}}}C_{{{r}}}',ans,'Order does not matter: use combinations.','Turutan tidak penting: gunakan gabungan.',[('Apply the combination formula.','Gunakan rumus gabungan.',rf'\dfrac{{{n}!}}{{{r}!({n-r})!}}={ans}')], context=locals())
        if v == 1:
            ans=math.perm(n,r)
            return q(f'Assign {r} distinct roles to {n} students. How many assignments are possible?',f'Agihkan {r} jawatan berlainan kepada {n} murid. Berapa agihan boleh dibuat?',rf'{{{n}}}P_{{{r}}}',ans,'The roles are distinct, so order matters.','Jawatan berlainan, maka turutan penting.',[('Apply the permutation formula.','Gunakan rumus pilih atur.',rf'\dfrac{{{n}!}}{{({n-r})!}}={ans}')], context=locals())
        ans=math.factorial(n)//2
        return q(f'Arrange {n} cards in a row. Exactly two have the same label; all others are distinct. How many arrangements?',f'Susun {n} kad dalam sebaris. Tepat dua mempunyai label sama; yang lain berbeza. Berapa susunan?',rf'\dfrac{{{n}!}}{{2!}}',ans,'Divide by the factorial of the repeated count.','Bahagi dengan faktorial bilangan berulang.',[('Correct for the repeated pair.','Laraskan bagi pasangan berulang.',rf'\dfrac{{{n}!}}{{2!}}={ans}')], context=locals())
    if topic == 'series':
        n=rng.randint(4,9+2*d)
        if v == 0:
            return q(f'Find the {n}th term of the arithmetic progression.',f'Cari sebutan ke-{n} bagi janjang aritmetik.',rf'{a},\ {a+b},\ {a+2*b},\ldots',a+(n-1)*b,'Use Tₙ = a + (n−1)d.','Gunakan Tₙ = a + (n−1)d.',[('Identify the first term and difference.','Kenal pasti sebutan pertama dan beza.',rf'T_{{{n}}}={a}+({n}-1)({b})={a+(n-1)*b}')], context=locals())
        if v == 1:
            ans=Fraction(n*(2*a+(n-1)*b),2)
            return q(f'Find the sum of the first {n} terms of the arithmetic progression.',f'Cari hasil tambah {n} sebutan pertama bagi janjang aritmetik.',rf'a={a},\quad d={b}',ans,'Use Sₙ = n/2 [2a+(n−1)d].','Gunakan Sₙ = n/2 [2a+(n−1)d].',[('Apply the AP sum formula.','Gunakan rumus hasil tambah JA.',rf'S_{{{n}}}=\dfrac{{{n}}}2[2({a})+({n}-1)({b})]={latex_number(ans)}')], context=locals())
        ratio=Fraction(1,b+1);ans=Fraction(a,1)/(1-ratio)
        return q('Find the sum to infinity of this geometric progression.','Cari hasil tambah ketakterhinggaan janjang geometri ini.',rf'a={a},\quad r={latex_number(ratio)}',ans,'Use a/(1−r), valid because |r| < 1.','Gunakan a/(1−r), sah kerana |r| < 1.',[('Check convergence and substitute.','Semak penumpuan dan gantikan.',rf'S_\infty=\dfrac{{{a}}}{{1-{latex_number(ratio)}}}={latex_number(ans)}')], context=locals())
    if topic == 'vectors':
        if v == 2 and (a,b)==(k,x):
            k += 1  # A section ratio needs distinct endpoints.
        if v == 0:
            return q('Find the magnitude of vector u.','Cari magnitud vektor u.',rf'\mathbf u=({3*a},{4*a})',5*a,'Use the length formula √(x²+y²).','Gunakan rumus panjang √(x²+y²).',[('Calculate the Euclidean length.','Hitung panjang Euclid.',rf'|\mathbf u|=\sqrt{{({3*a})^2+({4*a})^2}}={5*a}')], context=locals())
        if v == 1:
            return q('Find the x and y components of 2u − v, in that order.','Cari komponen x dan y bagi 2u − v, mengikut turutan.',rf'\mathbf u=({a},{b}),\quad\mathbf v=({k},{x})',[2*a-k,2*b-x],'Apply the operation to each component separately.','Lakukan operasi pada setiap komponen secara berasingan.',[('Subtract component by component.','Tolak komponen demi komponen.',rf'2\mathbf u-\mathbf v=({2*a-k},{2*b-x})')],labels=[('x component','Komponen x'),('y component','Komponen y')], context=locals())
        return q('M divides AB in the ratio AM:MB = 1:2. Find its x-coordinate.','M membahagi AB dalam nisbah AM:MB = 1:2. Cari koordinat-x M.',rf'A=({a},{b}),\quad B=({k},{x})',Fraction(2*a+k,3),'Move one third of the way from A to B.','Bergerak satu pertiga jarak dari A ke B.',[('Use the section formula.','Gunakan rumus pembahagian tembereng.',rf'x_M=\dfrac{{2({a})+{k}}}3={latex_number(Fraction(2*a+k,3))}')], context=locals())
    if topic in ('calculus','differentiation','integration','kinematics'):
        if topic == 'calculus':
            sub=['differentiation','integration','kinematics'][v]
        else: sub=topic
        if sub == 'differentiation':
            if v == 0:
                return q(f'Find dy/dx at x = {x}.',f'Cari dy/dx pada x = {x}.',rf'y={a}x^3+{b}x',3*a*x*x+b,'Differentiate each term using the power rule.','Bezakan setiap sebutan menggunakan hukum kuasa.',[('Differentiate.','Bezakan.',rf'\dfrac{{dy}}{{dx}}={3*a}x^2+{b}'),('Substitute the point.','Gantikan titik.',rf'y\prime({x})={3*a*x*x+b}')], context=locals())
            if v == 1:
                return q('Find the x-coordinate of the stationary point.','Cari koordinat-x titik pegun.',rf'y={a}x^2-{2*a*b}x+{k}',b,'At a stationary point, dy/dx = 0.','Pada titik pegun, dy/dx = 0.',[('Differentiate and set to zero.','Bezakan dan samakan dengan sifar.',rf'{2*a}x-{2*a*b}=0\Rightarrow x={b}')], context=locals())
            return q(f'Find the gradient at x = {x}.',f'Cari kecerunan pada x = {x}.',rf'y=({a}x+{b})^2',2*a*(a*x+b),'Apply the chain rule.','Gunakan petua rantai.',[('Differentiate the outer and inner functions.','Bezakan fungsi luaran dan dalaman.',rf'y\prime=2({a}x+{b})({a})'),('Evaluate the gradient.','Nilai kecerunan.',rf'y\prime({x})={2*a*(a*x+b)}')], context=locals())
        if sub == 'integration':
            upper=b+1
            if v == 0:
                ans=Fraction(a*upper*upper,2)+k*upper
                return q('Evaluate the definite integral.','Nilai kamiran tentu.',rf'\int_0^{{{upper}}}({a}x+{k})\,dx',ans,'Find an antiderivative and subtract its endpoint values.','Cari antiterbitan dan tolak nilainya pada had.',[('Integrate term by term.','Kamirkan sebutan demi sebutan.',rf'F(x)=\dfrac{{{a}}}2x^2+{k}x'),('Apply upper minus lower.','Gunakan had atas tolak had bawah.',rf'F({upper})-F(0)={latex_number(ans)}')], context=locals())
            if v == 1:
                return q('Find the area under the curve between the stated limits.','Cari luas di bawah lengkung antara had diberi.',rf'y={3*a}x^2,\quad0\leq x\leq {b}',a*b**3,'The curve is non-negative on this interval.','Lengkung tidak negatif pada selang ini.',[('Integrate to find area.','Kamirkan untuk mencari luas.',rf'A=[{a}x^3]_0^{{{b}}}={a*b**3}')], context=locals())
            return q(f'Given dy/dx and y(0), find y({x}).',f'Diberi dy/dx dan y(0), cari y({x}).',rf'\dfrac{{dy}}{{dx}}={2*a}x,\quad y(0)={k}',a*x*x+k,'Integrate, then use the initial condition to find C.','Kamirkan, kemudian gunakan syarat awal untuk mencari C.',[('Integrate and determine the constant.','Kamirkan dan tentukan pemalar.',rf'y={a}x^2+C,\quad C={k}'),('Substitute x.','Gantikan x.',rf'y({x})={a*x*x+k}')], context=locals())
        if v == 0:
            return q(f'Find velocity at t = {x} seconds, in m/s.',f'Cari halaju pada t = {x} saat, dalam m/s.',rf's(t)={a}t^2+{b}t',2*a*x+b,'Velocity is the derivative of displacement.','Halaju ialah terbitan sesaran.',[('Differentiate displacement.','Bezakan sesaran.',rf'v(t)={2*a}t+{b}'),('Substitute t.','Gantikan t.',rf'v({x})={2*a*x+b}')], context=locals())
        if v == 1:
            return q(f'Find acceleration at t = {x} seconds, in m/s².',f'Cari pecutan pada t = {x} saat, dalam m/s².',rf'v(t)={a}t^2+{b}',2*a*x,'Acceleration is dv/dt.','Pecutan ialah dv/dt.',[('Differentiate velocity.','Bezakan halaju.',rf'a(t)={2*a}t\Rightarrow a({x})={2*a*x}')], context=locals())
        return q(f'Find displacement from t = 0 to t = {x}, in metres.',f'Cari sesaran dari t = 0 hingga t = {x}, dalam meter.',rf'v(t)={2*a}t+{b}',a*x*x+b*x,'Integrate velocity over the stated interval.','Kamirkan halaju pada selang diberi.',[('Integrate between the limits.','Kamirkan antara had.',rf'\Delta s=[{a}t^2+{b}t]_0^{{{x}}}={a*x*x+b*x}')], context=locals())
    if topic == 'index_numbers':
        old=10*a;new=old+2*b
        if v == 0:
            return q('Find the price index, using the old price as base 100. Round to 3 decimal places.','Cari indeks harga, dengan harga lama sebagai asas 100. Bundarkan kepada 3 tempat perpuluhan.',rf'P_0={old},\quad P_1={new}',new/old*100,'Divide current price by base price, then multiply by 100.','Bahagi harga semasa dengan harga asas, kemudian darab 100.',[('Apply the index formula.','Gunakan rumus indeks.',rf'I=\dfrac{{{new}}}{{{old}}}\times100={new/old*100:.3f}')],tolerance=0.0005, context=locals())
        if v == 1:
            return q('Find the composite index.','Cari indeks gubahan.',rf'I_1={100+10*a},\ I_2={100+10*b},\quad w_1=2,\ w_2=3',Fraction(2*(100+10*a)+3*(100+10*b),5),'Use the weighted mean of the indices.','Gunakan min berwajaran bagi indeks.',[('Weight, sum and divide by total weight.','Darab wajaran, tambah dan bahagi dengan jumlah wajaran.',rf'\bar I=\dfrac{{2({100+10*a})+3({100+10*b})}}5={latex_number(Fraction(2*(100+10*a)+3*(100+10*b),5))}')], context=locals())
        return q('Find the new price in RM.','Cari harga baharu dalam RM.',rf'P_0={old},\quad I={100+10*b}',Fraction(old*(100+10*b),100),'Rearrange the price-index formula.','Susun semula rumus indeks harga.',[('Multiply base price by I/100.','Darab harga asas dengan I/100.',rf'P_1={old}\cdot\dfrac{{{100+10*b}}}{{100}}={latex_number(Fraction(old*(100+10*b),100))}')], context=locals())
    if topic == 'probability':
        n=rng.randint(3,6+d); p=Fraction(1,2)
        if v == 0:
            ans=Fraction(math.comb(n,2),2**n)
            return q('Find P(X = 2).','Cari P(X = 2).',rf'X\sim B({n},\dfrac12)',ans,'Use the binomial probability formula.','Gunakan rumus kebarangkalian binomial.',[('Choose successes and multiply probabilities.','Pilih kejayaan dan darab kebarangkalian.',rf'P(X=2)=\binom{{{n}}}2(\dfrac12)^{{{n}}}={latex_number(ans)}')], context=locals())
        if v == 1:
            return q('Find the variance of X.','Cari varians X.',rf'X\sim B({n},\dfrac12)',Fraction(n,4),'Binomial variance is np(1−p).','Varians binomial ialah np(1−p).',[('Substitute n and p.','Gantikan n dan p.',rf'\operatorname{{Var}}(X)={n}\cdot\dfrac12\cdot\dfrac12={latex_number(Fraction(n,4))}')], context=locals())
        mu=10*a; sigma=b
        return q('Find the standardised value z for the stated observation.','Cari nilai piawai z bagi cerapan diberi.',rf'X\sim N({mu},{sigma*sigma}),\quad X={mu+2*sigma}',2,'Use z = (x−μ)/σ; the second normal parameter is the variance.','Gunakan z = (x−μ)/σ; parameter normal kedua ialah varians.',[('Standardise.','Piawaikan.',rf'z=\dfrac{{{mu+2*sigma}-{mu}}}{{{sigma}}}=2')], context=locals())
    if topic == 'linear_programming':
        c=a*2+b
        if v == 0:
            ans=max(a,b)*k
            return q('For real x and y, find the maximum value of P.','Bagi x dan y nyata, cari nilai maksimum P.',rf'x\geq0,\ y\geq0,\ x+y\leq{k},\quad P={a}x+{b}y',ans,'Evaluate the objective at each feasible corner.','Nilai fungsi objektif pada setiap bucu rantau tersaur.',[('List the corners.','Senaraikan bucu.',rf'(0,0),({k},0),(0,{k})'),('Compare the three objective values.','Bandingkan tiga nilai objektif.',rf'P\in\{{0,{a*k},{b*k}\}}\Rightarrow P_{{\max}}={ans}')], context=locals())
        if v == 1:
            return q('For real x and y, find the minimum value of P.','Bagi x dan y nyata, cari nilai minimum P.',rf'x\geq0,\ y\geq0,\ x+y\geq{k},\quad P={a}x+{b}y',min(a,b)*k,'Positive costs make the minimum occur on x+y=k.','Kos positif menyebabkan minimum berlaku pada x+y=k.',[('Compare the boundary intercepts.','Bandingkan pintasan sempadan.',rf'P_{{\min}}=\min({a*k},{b*k})={min(a,b)*k}')], context=locals())
        return q('For real x and y, find the maximum value of P.','Bagi x dan y nyata, cari nilai maksimum P.',rf'0\leq x\leq{a},\ 0\leq y\leq{b},\quad P={k}x+{x}y',k*a+x*b,'Both coefficients are positive, so use the upper-right corner.','Kedua-dua pekali positif, maka gunakan bucu kanan atas.',[('Evaluate the objective at (a,b).','Nilai fungsi objektif pada (a,b).',rf'P_{{\max}}={k}({a})+{x}({b})={k*a+x*b}')], context=locals())
    raise ValueError('Unknown topic: '+topic)


def build(track, form, topic, level, count=10, seed=None):
    if level not in LEVELS + [PROGRESSION] or count not in (5,10,15):
        raise ValueError('Invalid practice settings.')
    keys=topics_for(track,form)
    if topic != 'mixed' and topic not in keys:
        raise ValueError('Topic is not in this path.')
    rng=random.Random(seed); questions=[];seen=set()
    for i in range(count):
        key=keys[i%len(keys)] if topic=='mixed' else topic
        if topic=='mixed' and i==0:
            keys=list(keys);rng.shuffle(keys);key=keys[0]
        for retry in range(100):
            question_level=LEVELS[min(2,3*i//count)] if level==PROGRESSION else level
            q=make(key,question_level,(i+retry)%3,rng)
            signature=(key,q['en'],q['latex'])
            if signature not in seen:
                seen.add(signature);q['id']=f'q{i+1}';questions.append(q);break
        else:
            raise RuntimeError('Could not generate enough distinct questions.')
    return questions
