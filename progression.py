"""Original linked-step and exam-style templates; no official paper content.

Each upper level has a distinct mathematical task, rather than scaled numbers.
Final numerical parts are checked together; working receives no method marks.
"""
import math
from fractions import Fraction as F


def num(x):
    if isinstance(x, F):
        return str(x.numerator) if x.denominator == 1 else rf'\dfrac{{{x.numerator}}}{{{x.denominator}}}'
    if float(x).is_integer():
        return str(int(x))
    return f'{x:.9g}'


def advanced(topic, level, variant, rng):
    boss = level == 'Boss mode'
    a, b, k = rng.randint(2, 7), rng.randint(1, 6), rng.randint(2, 6)
    t = rng.randint(2, 6)

    def q(en, bm, expr, answers, labels, steps, hints, tolerance=1e-7, unordered=False):
        values = answers if isinstance(answers, list) else [answers]
        return dict(topic=topic, level=level, variant=variant % 3, en=en, bm=bm,
                    latex=expr, answers=[float(z) for z in values],
                    answer_latex=[num(z) for z in values], labels=labels,
                    steps=steps, hints=hints, tolerance=tolerance, unordered=unordered,
                    demand='exam-style' if boss else 'linked steps')

    if topic == 'functions':
        if not boss:
            target = a*(t*t+k)+b
            return q('Solve f(g(x)) = N for x > 0. Then find g(x).',
                     'Selesaikan f(g(x)) = N bagi x > 0. Kemudian cari g(x).',
                     rf'f(x)={a}x+{b},\ g(x)=x^2+{k},\ N={target}',
                     [t,t*t+k], [('x','x'),('g(x)','g(x)')],
                     [('Compose the functions.','Gubah fungsi.',rf'{a}(x^2+{k})+{b}={target}'),
                      ('Isolate the square and choose the positive root.','Asingkan kuasa dua dan pilih punca positif.',rf'x^2={t*t}\Rightarrow x={t}'),
                      ('Evaluate g.','Nilai g.',rf'g({t})={t*t+k}')],
                     [('Apply g first, then f.','Gunakan g dahulu, kemudian f.'),
                      ('Undo the addition and multiplication before taking a square root.','Songsangkan penambahan dan pendaraban sebelum mengambil punca kuasa dua.')])
        return q('f uses its full increasing branch x ≥ h, so its inverse exists. Find h, then solve f⁻¹(g(x)) = r for x. Finally find f(r).',
                 'f menggunakan cabang menaik penuh x ≥ h supaya fungsi songsangnya wujud. Cari h, kemudian selesaikan f⁻¹(g(x)) = r bagi x. Akhir sekali cari f(r).',
                 rf'f(x)=(x-{k})^2+{b},\ g(x)={a}x+{b},\ r={k+t}',
                 [k,F(t*t,a),t*t+b], [('Domain lower bound h','Had bawah domain h'),('x','x'),('f(r)','f(r)')],
                 [('Use the increasing branch.','Gunakan cabang menaik.',rf'f^{{-1}}(y)={k}+\sqrt{{y-{b}}},\ y\geq{b}'),
                  ('Apply f to both sides.','Gunakan f pada kedua-dua belah.',rf'g(x)=f({k+t})={t*t+b}'),
                  ('Solve the linear equation.','Selesaikan persamaan linear.',rf'{a}x+{b}={t*t+b}\Rightarrow x={num(F(t*t,a))}')],
                 [('The domain begins at the turning point.','Domain bermula pada titik pusingan.'),
                  ('f⁻¹(g(x)) = r implies g(x) = f(r).','f⁻¹(g(x)) = r bermaksud g(x) = f(r).'),
                  ('Use the positive square-root branch for the inverse.','Gunakan cabang punca kuasa dua positif untuk fungsi songsang.')])

    if topic == 'quadratics':
        if not boss:
            return q('Find the turning-point coordinates, then both roots. Enter the smaller root first.',
                     'Cari koordinat titik pusingan, kemudian kedua-dua punca. Masukkan punca lebih kecil dahulu.',
                     rf'y={a}x^2-{2*a*b}x+{a*(b*b-k*k)}',
                     [b,-a*k*k,b-k,b+k], [('Turning-point x','Titik pusingan x'),('Turning-point y','Titik pusingan y'),('Smaller root','Punca lebih kecil'),('Larger root','Punca lebih besar')],
                     [('Complete the square.','Lengkapkan kuasa dua.',rf'y={a}(x-{b})^2-{a*k*k}'),
                      ('Read the vertex and solve y = 0.','Baca titik pusingan dan selesaikan y = 0.',rf'({b},-{a*k*k}),\quad x={b}\pm{k}')],
                     [('Complete the square before finding the roots.','Lengkapkan kuasa dua sebelum mencari punca.'),
                      ('Rewrite using (x − b)²; the constant determines the minimum.','Tulis semula menggunakan (x − b)²; pemalar menentukan minimum.')])
        a = rng.randint(2, 50)
        length = 4*a
        return q(f'A farmer has {length} m of fencing for three sides of a rectangular pen beside a straight wall. Let x be each perpendicular side. Find the optimal x, the other side, and the maximum area.',
                 f'Seorang penternak mempunyai pagar sepanjang {length} m untuk tiga sisi kandang segi empat tepat di tepi dinding lurus. Ambil x sebagai setiap sisi berserenjang. Cari x optimum, sisi yang lain dan luas maksimum.',
                 rf'2x+y={length},\quad A=xy,\quad x,y>0',
                 [a,2*a,2*a*a], [('Optimal x (m)','x optimum (m)'),('Other side y (m)','Sisi lain y (m)'),('Maximum area (m²)','Luas maksimum (m²)')],
                 [('Eliminate the second length.','Hapuskan panjang kedua.',rf'A=x({length}-2x)=-2(x-{a})^2+{2*a*a}'),
                  ('Use the maximum of the quadratic.','Gunakan maksimum fungsi kuadratik.',rf'x={a},\ y={2*a},\ A_{{\max}}={2*a*a}')],
                 [('Express the area using just one variable.','Ungkapkan luas menggunakan satu pemboleh ubah sahaja.'),
                  ('The fencing equation gives y = total − 2x.','Persamaan pagar memberikan y = jumlah − 2x.'),
                  ('Complete the square or use the vertex formula; check both lengths are positive.','Lengkapkan kuasa dua atau gunakan rumus titik pusingan; semak kedua-dua panjang positif.')])

    if topic == 'polynomials':
        r, s, u = b+1, -k, t+k
        total=r+s+u; pairs=r*s+r*u+s*u; constant=-r*s*u
        if not boss:
            return q(f'x − {r} is a factor. Find the two remaining roots, smaller first.',
                     f'x − {r} ialah faktor. Cari dua punca yang lain, punca lebih kecil dahulu.',
                     rf'P(x)=x^3-({total})x^2+({pairs})x+({constant})',
                     [s,u], [('Smaller remaining root','Punca lain lebih kecil'),('Larger remaining root','Punca lain lebih besar')],
                     [('Divide by the known factor.','Bahagi dengan faktor diketahui.',rf'P(x)=(x-{r})[x^2-({s+u})x+({s*u})]'),
                      ('Factorise the quadratic.','Faktorkan kuadratik.',rf'P(x)=(x-{r})(x-({s}))(x-{u})')],
                     [('Use polynomial division to reduce the cubic to a quadratic.','Gunakan pembahagian polinomial untuk menurunkan kubik kepada kuadratik.'),
                      ('The other two roots come from the quotient, not the known linear factor.','Dua punca lain datang daripada hasil bahagi, bukan faktor linear diketahui.')])
        # Reconstruct two coefficients from independent remainders, then factor.
        p=-total; z=pairs; rem=1+p+z+constant
        return q(f'P(x) has factor x − {r}, and its remainder on division by x − 1 is {rem}. Find p and q, then its smallest and largest roots.',
                 f'P(x) mempunyai faktor x − {r}, dan baki apabila dibahagi dengan x − 1 ialah {rem}. Cari p dan q, kemudian punca terkecil dan terbesar.',
                 rf'P(x)=x^3+px^2+qx+({constant})',
                 [p,z,min(r,s,u),max(r,s,u)], [('p','p'),('q','q'),('Smallest root','Punca terkecil'),('Largest root','Punca terbesar')],
                 [('Use the factor and remainder conditions.','Gunakan syarat faktor dan baki.',rf'{r*r}p+{r}q={-r**3-constant},\quad p+q={rem-1-constant}'),
                  ('Solve for the coefficients.','Selesaikan pekali.',rf'p={p},\ q={z}'),
                  ('Divide and factorise.','Bahagi dan faktorkan.',rf'P(x)=(x-{r})(x-({s}))(x-{u})')],
                 [('Convert both conditions into equations in p and q.','Tukarkan kedua-dua syarat kepada persamaan dalam p dan q.'),
                  ('A factor gives P(r) = 0; the stated remainder gives P(1).','Faktor memberikan P(r) = 0; baki diberi memberikan P(1).'),
                  ('After finding p and q, divide by the known factor and solve the quotient.','Selepas mencari p dan q, bahagi dengan faktor diketahui dan selesaikan hasil bahagi.')])

    if topic == 'equations':
        if not boss:
                # Avoid repeated roots, keeping four labelled responses.
            t=k+b
            return q('Solve the equation for all four real roots, in ascending order.',
                     'Selesaikan persamaan bagi keempat-empat punca nyata, dalam turutan menaik.',
                     rf'x^4-{k*k+t*t}x^2+{k*k*t*t}=0', [-t,-k,k,t],
                     [('Root 1','Punca 1'),('Root 2','Punca 2'),('Root 3','Punca 3'),('Root 4','Punca 4')],
                     [('Substitute u = x².','Gantikan u = x².',rf'(u-{k*k})(u-{t*t})=0'),
                      ('Take both signs of each square root.','Ambil kedua-dua tanda bagi setiap punca kuasa dua.',rf'x=\pm{k},\ \pm{t}')],
                     [('Treat the equation as a quadratic in x².','Anggap persamaan sebagai kuadratik dalam x².'),
                      ('Each positive value of x² produces a positive and a negative root.','Setiap nilai positif x² menghasilkan punca positif dan negatif.')])
        left=b; right=b+k
        return q('The rational inequality has two solution intervals. Enter the three finite boundaries in ascending order. Also enter the boundary excluded because the expression is undefined. The displayed interval pattern specifies open/closed endpoints.',
                 'Ketaksamaan nisbah mempunyai dua selang penyelesaian. Masukkan tiga sempadan terhingga dalam turutan menaik. Masukkan juga sempadan yang dikecualikan kerana ungkapan tidak ditakrifkan. Corak selang diberi menentukan hujung terbuka/tertutup.',
                 rf'\dfrac{{(x-{left})(x-{right})}}{{x+{a}}}\geq0,\quad (-\infty,c_1)\cup[c_2,c_3]\ \text{{or}}\ (c_1,c_2]\cup[c_3,\infty)',
                 [-a,left,right,-a], [('Boundary c₁','Sempadan c₁'),('Boundary c₂','Sempadan c₂'),('Boundary c₃','Sempadan c₃'),('Excluded boundary','Sempadan dikecualikan')],
                 [('Locate zeros and the excluded denominator zero.','Cari sifar pembilang dan sifar penyebut dikecualikan.',rf'x=-{a},{left},{right}'),
                  ('Test the sign in each interval.','Uji tanda dalam setiap selang.',r'-\ ,\ +\ ,\ -\ ,\ +'),
                  ('Include numerator zeros only.','Masukkan sifar pembilang sahaja.',rf'x\in(-{a},{left}]\cup[{right},\infty)')],
                 [('Create a sign table using numerator and denominator zeros.','Bina jadual tanda menggunakan sifar pembilang dan penyebut.'),
                  ('The denominator zero is never part of the solution.','Sifar penyebut tidak pernah termasuk dalam penyelesaian.'),
                  ('Test one value in each of the four intervals; include numerator zeros for ≥.','Uji satu nilai dalam setiap empat selang; masukkan sifar pembilang bagi ≥.')])

    if topic == 'simultaneous':
        if not boss:
            total=a+b; product=a*b
            return q('Find x and y, given x ≥ y.', 'Cari x dan y, diberi x ≥ y.',
                     rf'x+y={total},\quad xy={product}', [max(a,b),min(a,b)], [('x','x'),('y','y')],
                     [('Substitute y = total − x.','Gantikan y = jumlah − x.',rf'x^2-{total}x+{product}=0'),
                      ('Solve the quadratic and use x ≥ y.','Selesaikan kuadratik dan gunakan x ≥ y.',rf'(x-{a})(x-{b})=0')],
                     [('Eliminate y to form a quadratic.','Hapuskan y untuk membentuk kuadratik.'),
                      ('The same two roots are possible for x and y; use the ordering restriction.','Dua punca yang sama mungkin bagi x dan y; gunakan sekatan turutan.')])
        u=b+k; v=u+a
        # line y=kx+b; parabola y=x²+(k-u-v)x+uv+b
        c=k-u-v; const=u*v+b
        return q('Find both intersection points of the line and curve, with the smaller x point first. Then find the distance between the points, to 3 decimal places.',
                 'Cari kedua-dua titik persilangan garis dan lengkung, dengan titik x lebih kecil dahulu. Kemudian cari jarak antara titik, kepada 3 tempat perpuluhan.',
                 rf'y={k}x+{b},\quad y=x^2+({c})x+{const}',
                 [u,k*u+b,v,k*v+b,(v-u)*math.sqrt(1+k*k)],
                 [('First x','x pertama'),('First y','y pertama'),('Second x','x kedua'),('Second y','y kedua'),('Distance','Jarak')],
                 [('Equate the expressions for y.','Samakan ungkapan bagi y.',rf'x^2-{u+v}x+{u*v}=0'),
                  ('Find both points.','Cari kedua-dua titik.',rf'({u},{k*u+b}),\quad({v},{k*v+b})'),
                  ('Use the distance formula.','Gunakan rumus jarak.',rf'd=\sqrt{{({v-u})^2+({k*(v-u)})^2}}')],
                 [('Eliminate y by equating the line and curve.','Hapuskan y dengan menyamakan garis dan lengkung.'),
                  ('Solve the resulting quadratic, then substitute both x values into the line.','Selesaikan kuadratik terhasil, kemudian gantikan kedua-dua nilai x ke dalam garis.'),
                  ('Distance uses both coordinate differences, not just the difference in x.','Jarak menggunakan kedua-dua beza koordinat, bukan beza x sahaja.')], tolerance=.0005)

    if topic == 'logarithms':
        if not boss:
            root=b+k
            return q('Solve for x, applying the logarithm domain restrictions.',
                     'Selesaikan x dengan menggunakan sekatan domain logaritma.',
                     rf'\log_{{{a}}}(x-{b})+\log_{{{a}}}(x+{b})=\log_{{{a}}}{root*root-b*b}',root,[('Valid x','x sah')],
                     [('Combine the logarithms.','Gabungkan logaritma.',rf'x^2-{b*b}={root*root-b*b}'),
                      ('Reject the root outside the domain.','Tolak punca di luar domain.',rf'x=\pm{root},\quad x>{b}\Rightarrow x={root}')],
                     [('Use the product law, then check both log arguments are positive.','Gunakan hukum hasil darab, kemudian semak kedua-dua argumen log positif.'),
                      ('The quadratic gives two candidates, but only one satisfies x > b.','Kuadratik memberikan dua calon, tetapi hanya satu memenuhi x > b.')])
        initial=100*a; hours=b; doubled=initial*2
        return q(f'A culture follows N(t)=Ae^(kt). It has {initial} cells at t=0 and {doubled} cells after {hours} hours. Find k (hour⁻¹), the time to reach three times the initial population, and N({2*hours}). Round k and the time to 3 decimal places.',
                 f'Kultur mengikut N(t)=Ae^(kt). Terdapat {initial} sel pada t=0 dan {doubled} sel selepas {hours} jam. Cari k (jam⁻¹), masa untuk mencapai tiga kali populasi awal dan N({2*hours}). Bundarkan k dan masa kepada 3 tempat perpuluhan.',
                 r'N(t)=Ae^{kt}',[math.log(2)/hours,hours*math.log(3)/math.log(2),initial*4],
                 [('k','k'),('Tripling time (h)','Masa menjadi tiga kali ganda (j)'),('Final population','Populasi akhir')],
                 [('Use the initial condition and second observation.','Gunakan syarat awal dan cerapan kedua.',rf'A={initial},\quad e^{{{hours}k}}=2'),
                  ('Take natural logarithms.','Ambil logaritma asli.',rf'k=\dfrac{{\ln2}}{{{hours}}},\quad t_3=\dfrac{{{hours}\ln3}}{{\ln2}}'),
                  ('Evaluate after two doubling intervals.','Nilai selepas dua selang penggandaan.',rf'N({2*hours})={initial}\times2^2={initial*4}')],
                 [('Determine A first, then use a population ratio to find k.','Tentukan A dahulu, kemudian gunakan nisbah populasi untuk mencari k.'),
                  ('Divide N(t) by N(0) before taking logarithms.','Bahagi N(t) dengan N(0) sebelum mengambil logaritma.'),
                  ('For tripling use e^(kt) = 3; keep k unrounded in later calculations.','Untuk tiga kali ganda gunakan e^(kt) = 3; kekalkan k tanpa pembundaran dalam pengiraan seterusnya.')],tolerance=.0005)

    if topic == 'indices':
        if not boss:
            exponent=b+k
            return q('Solve the exponential equation, then evaluate the stated surd expression.',
                     'Selesaikan persamaan eksponen, kemudian nilai ungkapan surd diberi.',
                     rf'{a}^{{2x}}-{a**k+a**b}\cdot {a}^x+{a**exponent}=0,\quad x\geq {max(b,k)},\quad E=\dfrac{{\sqrt{{{a*a*2}}}}}{{\sqrt2}}+x',
                     [max(b,k),a+max(b,k)],[('x','x'),('E','E')],
                     [('Let u = aˣ and solve the quadratic.','Ambil u = aˣ dan selesaikan kuadratik.',rf'(u-{a**b})(u-{a**k})=0'),
                      ('Apply the restriction and simplify the surd.','Gunakan sekatan dan permudahkan surd.',rf'x={max(b,k)},\quad E={a}+{max(b,k)}')],
                     [('Substitute aˣ as one variable.','Gantikan aˣ sebagai satu pemboleh ubah.'),
                      ('After solving for aˣ, take logarithms or compare powers; simplify √(2a²).','Selepas menyelesaikan aˣ, ambil logaritma atau bandingkan kuasa; permudahkan √(2a²).')])
        # Rationalised surds give a quadratic in positive u = 2ˣ.
        lower=b; upper=b+k
        return q('Solve for both real x values, smaller first. Then rationalise R and give its coefficient of √2.',
                 'Selesaikan kedua-dua nilai x nyata, yang lebih kecil dahulu. Kemudian rasionalkan R dan berikan pekali √2.',
                 rf'4^x-{2**lower+2**upper}\cdot 2^x+{2**(lower+upper)}=0,\quad R=\dfrac{{{a}}}{{\sqrt{{{2*k*k}}}}}',
                 [lower,upper,F(a,2*k)], [('Smaller x','x lebih kecil'),('Larger x','x lebih besar'),('Coefficient of √2','Pekali √2')],
                 [('Use u = 2ˣ.','Gunakan u = 2ˣ.',rf'u^2-{2**lower+2**upper}u+{2**(lower+upper)}=0'),
                  ('Factorise and convert back to x.','Faktorkan dan tukar semula kepada x.',rf'u={2**lower},{2**upper}\Rightarrow x={lower},{upper}'),
                  ('Rationalise the denominator.','Rasionalkan penyebut.',rf'R=\dfrac{{{a}\sqrt2}}{{{2*k}}}')],
                 [('Recognise that 4ˣ = (2ˣ)².','Kenal pasti bahawa 4ˣ = (2ˣ)².'),
                  ('The quadratic gives values of 2ˣ, not values of x.','Kuadratik memberikan nilai 2ˣ, bukan nilai x.'),
                  ('Simplify the denominator to k√2, then multiply numerator and denominator by √2.','Permudahkan penyebut kepada k√2, kemudian darab pembilang dan penyebut dengan √2.')])

    if topic in ('straight_lines','coordinates'):
        if not boss:
            h=b+a; cy=k
            return q('Find the perpendicular bisector of AB in the form y = mx + c. Enter m and c.',
                     'Cari pembahagi dua sama serenjang AB dalam bentuk y = mx + c. Masukkan m dan c.',
                     rf'A=({b},{k-a}),\quad B=({b+2*a},{k+a})',[-1,h+cy], [('m','m'),('c','c')],
                     [('Find midpoint and gradient of AB.','Cari titik tengah dan kecerunan AB.',rf'M=({h},{cy}),\quad m_{{AB}}=1'),
                      ('Use the perpendicular gradient through M.','Gunakan kecerunan berserenjang melalui M.',rf'y-{cy}=-(x-{h})\Rightarrow y=-x+{h+cy}')],
                     [('A perpendicular bisector passes through the midpoint.','Pembahagi dua sama serenjang melalui titik tengah.'),
                      ('Use the negative reciprocal gradient and substitute the midpoint to find c.','Gunakan kecerunan salingan negatif dan gantikan titik tengah untuk mencari c.')])
        # Triangle A=(0,0), B=(2a,0), C=(b,2k).
        intercept=F(b*b+4*k*k-2*a*b,4*k)
        radius=math.sqrt(a*a+float(intercept)**2)
        return q('A circle passes through A, B and C. Use perpendicular bisectors to find its centre (h,j), its radius, and the area of triangle ABC. Round only the radius to 3 decimal places.',
                 'Bulatan melalui A, B dan C. Gunakan pembahagi dua sama serenjang untuk mencari pusat (h,j), jejari dan luas segi tiga ABC. Bundarkan jejari sahaja kepada 3 tempat perpuluhan.',
                 rf'A=(0,0),\ B=({2*a},0),\ C=({b},{2*k})',
                 [a,intercept,radius,2*a*k], [('Centre h','Pusat h'),('Centre j','Pusat j'),('Radius','Jejari'),('Triangle area','Luas segi tiga')],
                 [('The perpendicular bisector of AB is vertical.','Pembahagi dua sama serenjang AB adalah menegak.',rf'h={a}'),
                  ('Equate distances from the centre to A and C.','Samakan jarak pusat ke A dan C.',rf'{2*b}h+{4*k}j={b*b+4*k*k}\Rightarrow j={num(intercept)}'),
                  ('Use a radius and the base-height area formula.','Gunakan jejari dan rumus luas tapak-tinggi.',rf'r=\sqrt{{{a*a}+({num(intercept)})^2}},\quad A_\triangle={2*a*k}')],
                 [('The centre is equidistant from all three points.','Pusat mempunyai jarak sama dari ketiga-tiga titik.'),
                  ('AB is horizontal, so its perpendicular bisector fixes h.','AB mendatar, maka pembahagi dua sama serenjangnya menentukan h.'),
                  ('Expand OA² = OC²; the squared h and j terms cancel.','Kembangkan OA² = OC²; sebutan kuasa dua h dan j terhapus.')],tolerance=.0005)

    if topic == 'linear_law':
        if not boss:
            power=k; coeff=2**b
            return q('The data follow y = axⁿ. Find a and n, then predict y when x = 4.',
                     'Data mengikut y = axⁿ. Cari a dan n, kemudian ramalkan y apabila x = 4.',
                     rf'(x,y)=(1,{coeff}),(2,{coeff*2**power})',
                     [coeff,power,coeff*4**power], [('a','a'),('n','n'),('y(4)','y(4)')],
                     [('Linearise the power model.','Linearkan model kuasa.',r'\ln y=\ln a+n\ln x'),
                      ('Use the data ratio for the gradient.','Gunakan nisbah data untuk kecerunan.',rf'a={coeff},\quad 2^n={2**power}\Rightarrow n={power}'),
                      ('Predict with the original model.','Ramalkan dengan model asal.',rf'y(4)={coeff}\cdot4^{power}={coeff*4**power}')],
                     [('Take logarithms or divide the two observations.','Ambil logaritma atau bahagikan dua cerapan.'),
                      ('At x = 1 the value of y equals a; the ratio determines n.','Pada x = 1 nilai y sama dengan a; nisbah menentukan n.')])
        return q('A straight-line plot uses X = x² and Y = xy for the model y = ax + b/x. From the two given points, find a, b, and y when x = 3. Then find the positive x where y is minimum.',
                 'Plot garis lurus menggunakan X = x² dan Y = xy bagi model y = ax + b/x. Daripada dua titik diberi, cari a, b dan y apabila x = 3. Kemudian cari x positif apabila y minimum.',
                 rf'(X,Y)=(1,{a+a*k*k}),(4,{4*a+a*k*k}),\quad x>0',
                 [a,a*k*k,F(3*a,1)+F(a*k*k,3),k], [('a','a'),('b','b'),('y(3)','y(3)'),('x at minimum','x pada minimum')],
                 [('Multiply the model by x.','Darab model dengan x.',r'xy=ax^2+b\Rightarrow Y=aX+b'),
                  ('Calculate gradient and intercept.','Hitung kecerunan dan pintasan.',rf'a={a},\quad b={a*k*k}'),
                  ('Use AM-GM, or complete a square after comparing to the minimum.','Gunakan AM-GM, atau lengkapkan kuasa dua selepas membandingkan dengan minimum.',rf'y-2\sqrt{{ab}}=\dfrac{{(\sqrt a\,x-\sqrt b)^2}}{{x}}\geq0,\quad x=\sqrt{{b/a}}={k}')],
                 [('Recover the original parameters from gradient and intercept.','Dapatkan parameter asal daripada kecerunan dan pintasan.'),
                  ('The minimum of ax + b/x for x > 0 occurs when the two terms are equal.','Minimum ax + b/x bagi x > 0 berlaku apabila kedua-dua sebutan sama.'),
                  ('Solve ax = b/x, or show the non-negative square divided by x.','Selesaikan ax = b/x, atau tunjukkan kuasa dua tidak negatif dibahagi x.')])

    if topic == 'circles':
        if not boss:
            rad=a+k
            return q('The horizontal line intersects the circle. Find both x coordinates, smaller first.',
                     'Garis mengufuk memotong bulatan. Cari kedua-dua koordinat x, yang lebih kecil dahulu.',
                     rf'(x-{b})^2+(y-{k})^2={rad*rad},\quad y={k}', [b-rad,b+rad], [('Smaller x','x lebih kecil'),('Larger x','x lebih besar')],
                     [('Substitute the line into the circle.','Gantikan garis ke dalam bulatan.',rf'(x-{b})^2={rad*rad}'),
                      ('Take both square roots.','Ambil kedua-dua punca kuasa dua.',rf'x={b}\pm{rad}')],
                     [('Substitute y before solving for x.','Gantikan y sebelum menyelesaikan x.'),
                      ('A squared expression gives two signs for its square root.','Ungkapan kuasa dua memberikan dua tanda bagi punca kuasa duanya.')])
        # 3-4-5 radius triangle to a point and external tangent lengths.
        rad=5*a; px=b+3*a; py=k+4*a
        c=F(py,1)+F(3*px,4)
        return q('T lies on the circle. Find the tangent at T in the form y = mx + c. A point P lies horizontally to the right of the centre. Find the length of either tangent from P, to 3 decimal places.',
                 'T terletak pada bulatan. Cari tangen di T dalam bentuk y = mx + c. Titik P terletak mengufuk di kanan pusat. Cari panjang mana-mana tangen dari P, kepada 3 tempat perpuluhan.',
                 rf'(x-{b})^2+(y-{k})^2={rad*rad},\quad T=({px},{py}),\quad P=({b+rad+k},{k})',
                 [F(-3,4),c,math.sqrt((rad+k)**2-rad**2)], [('Tangent m','m tangen'),('Tangent c','c tangen'),('Tangent length','Panjang tangen')],
                 [('The tangent is perpendicular to CT.','Tangen berserenjang dengan CT.',r'm_{CT}=\dfrac43\Rightarrow m_T=-\dfrac34'),
                  ('Substitute T into the tangent equation.','Gantikan T ke dalam persamaan tangen.',rf'c={py}+\dfrac34({px})={num(c)}'),
                  ('Use the right triangle from the centre to the contact point.','Gunakan segi tiga bersudut tegak dari pusat ke titik sentuhan.',rf'PT=\sqrt{{({rad+k})^2-{rad}^2}}')],
                 [('Use the radius gradient to find the perpendicular tangent gradient.','Gunakan kecerunan jejari untuk mencari kecerunan tangen berserenjang.'),
                  ('For the tangent length, radius and tangent meet at 90°.','Bagi panjang tangen, jejari dan tangen bertemu pada 90°.'),
                  ('The centre-to-P distance is the hypotenuse, not a tangent length.','Jarak pusat-ke-P ialah hipotenus, bukan panjang tangen.')],tolerance=.0005)

    if topic == 'circular':
        if not boss:
            theta=F(b,3); area=F(a*a,2)*theta
            return q('Given the sector area and radius, find its angle in radians, arc length and perimeter.',
                     'Diberi luas sektor dan jejari, cari sudut dalam radian, panjang lengkok dan perimeter.',
                     rf'r={a}\ \mathrm{{cm}},\quad A={num(area)}\ \mathrm{{cm}}^2',
                     [theta,a*theta,a*theta+2*a], [('Angle θ','Sudut θ'),('Arc length (cm)','Panjang lengkok (cm)'),('Perimeter (cm)','Perimeter (cm)')],
                     [('Rearrange the sector area formula.','Susun semula rumus luas sektor.',rf'\theta=2A/r^2={num(theta)}'),
                      ('Find arc length, then add two radii.','Cari panjang lengkok, kemudian tambah dua jejari.',rf's=r\theta={num(a*theta)},\quad P=s+2r={num(a*theta+2*a)}')],
                     [('Start with A = ½r²θ, not s = rθ.','Mulakan dengan A = ½r²θ, bukan s = rθ.'),
                      ('A sector perimeter includes two radii as well as the arc.','Perimeter sektor merangkumi dua jejari serta lengkok.')])
        theta=F(b,4); inner=a; outer=a+k
        area=F(outer*outer-inner*inner,2)*theta
        perimeter=(outer+inner)*theta+2*k
        return q('An annular sector has common angle θ in radians, inner radius r and outer radius R. Find θ from the shaded area, then the complete shaded boundary length. The boundary has two arcs and two radial edges.',
                 'Sektor gelang mempunyai sudut sepunya θ dalam radian, jejari dalam r dan jejari luar R. Cari θ daripada luas berlorek, kemudian jumlah panjang sempadan berlorek. Sempadan mempunyai dua lengkok dan dua sisi jejari.',
                 rf'r={inner},\ R={outer},\ A={num(area)}',
                 [theta,perimeter], [('Angle θ (rad)','Sudut θ (rad)'),('Boundary length','Panjang sempadan')],
                 [('Subtract the inner sector from the outer sector.','Tolak sektor dalam daripada sektor luar.',rf'A=\dfrac12(R^2-r^2)\theta\Rightarrow\theta={num(theta)}'),
                  ('Add both arcs and both radial gaps.','Tambah kedua-dua lengkok dan dua jurang jejari.',rf'P=(R+r)\theta+2(R-r)={num(perimeter)}')],
                 [('Model the shaded region as the difference of two sectors.','Modelkan rantau berlorek sebagai beza dua sektor.'),
                  ('The radial boundary lengths are R − r, not R.','Panjang sempadan jejari ialah R − r, bukan R.'),
                  ('The two curved boundaries have lengths Rθ and rθ.','Dua sempadan melengkung mempunyai panjang Rθ dan rθ.')])

    if topic == 'trig':
        # A trig quadratic requiring an identity, compound input and full interval.
        n=rng.randint(2,5); shift=rng.randint(1,20)*3
        if not boss:
            return q('Solve for θ in the stated degree interval; smaller solution first.',
                     'Selesaikan θ dalam selang darjah diberi; penyelesaian lebih kecil dahulu.',
                     rf'2\sin^2({n}\theta-{shift}^\circ)-3\sin({n}\theta-{shift}^\circ)+1=0,\quad {num(F(shift,n))}^\circ\leq\theta\leq{num(F(180+shift,n))}^\circ',
                     [F(30+shift,n),F(90+shift,n),F(150+shift,n)], [('Solution 1 (°)','Penyelesaian 1 (°)'),('Solution 2 (°)','Penyelesaian 2 (°)'),('Solution 3 (°)','Penyelesaian 3 (°)')],
                     [('Set u = nθ − shift and factorise.','Ambil u = nθ − anjakan dan faktorkan.',r'(2\sin u-1)(\sin u-1)=0'),
                      ('Find all angles in the interval.','Cari semua sudut dalam selang.',rf'u=30^\circ,90^\circ,150^\circ,\quad\theta=(u+{shift}^\circ)/{n}')],
                     [('Use the compound angle as one variable, then factorise in its sine.','Gunakan sudut gabungan sebagai satu pemboleh ubah, kemudian faktorkan dalam sinusnya.'),
                      ('For each sine value, list every angle in the interval.','Bagi setiap nilai sinus, senaraikan setiap sudut dalam selang.')])
        # 2cos²u−3cosu+1=0 gives u=0,60,300,360 across full cycle.
        vals=[F(shift,n),F(60+shift,n),F(300+shift,n),F(360+shift,n)]
        return q('Use a trigonometric identity to solve for all θ in the degree interval, in ascending order. Include both interval endpoints when they satisfy the equation.',
                 'Gunakan identiti trigonometri untuk menyelesaikan semua θ dalam selang darjah, dalam turutan menaik. Masukkan kedua-dua hujung selang apabila memenuhi persamaan.',
                 rf'\cos(2({n}\theta-{shift}^\circ))-3\cos({n}\theta-{shift}^\circ)+2=0,\quad {num(vals[0])}^\circ\leq\theta\leq{num(vals[-1])}^\circ',
                 vals, [(f'Solution {i+1} (°)',f'Penyelesaian {i+1} (°)') for i in range(4)],
                 [('Use cos 2u = 2cos²u − 1.','Gunakan kos 2u = 2kos²u − 1.',r'(2\cos u-1)(\cos u-1)=0'),
                  ('Solve over the transformed interval.','Selesaikan dalam selang terubah.',rf'u={n}\theta-{shift}^\circ,\quad0^\circ\leq u\leq360^\circ,\quad u=0^\circ,60^\circ,300^\circ,360^\circ'),
                  ('Transform every solution back to θ.','Tukarkan setiap penyelesaian semula kepada θ.',rf'\theta=(u+{shift}^\circ)/{n}')],
                 [('Set u = nθ − shift and transform the interval too.','Ambil u = nθ − anjakan dan tukarkan selang juga.'),
                  ('Replace cos 2u by 2cos²u − 1, then factorise.','Gantikan kos 2u dengan 2kos²u − 1, kemudian faktorkan.'),
                  ('cos u = 1 occurs at both 0° and 360° here; convert all u values back.','kos u = 1 berlaku pada 0° dan 360° di sini; tukarkan semua nilai u semula.')])

    if topic == 'triangles':
        if not boss:
            c=math.sqrt(a*a+(a+k)**2-a*(a+k)); area=a*(a+k)*math.sqrt(3)/4
            return q('Two sides meet at 60°. Find the third side and the triangle area, both to 3 decimal places.',
                     'Dua sisi bertemu pada 60°. Cari sisi ketiga dan luas segi tiga, kedua-duanya kepada 3 tempat perpuluhan.',
                     rf'AB={a}\ \mathrm{{cm}},\ AC={a+k}\ \mathrm{{cm}},\ \angle BAC=60^\circ',
                     [c,area], [('BC (cm)','BC (cm)'),('Area (cm²)','Luas (cm²)')],
                     [('Use the cosine rule.','Gunakan petua kosinus.',rf'BC^2={a}^2+{a+k}^2-2({a})({a+k})\cos60^\circ'),
                      ('Use the included-angle area formula.','Gunakan rumus luas sudut kandung.',rf'A=\dfrac12({a})({a+k})\sin60^\circ')],
                     [('The given angle is between the sides, so use cosine rule.','Sudut diberi di antara sisi, maka gunakan petua kosinus.'),
                      ('Area can be found directly without computing another angle.','Luas boleh dicari terus tanpa menghitung sudut lain.')],tolerance=.0005)
        # Ambiguous sine rule with sin B = 3/4, A=30°. Two valid triangles.
        a=rng.randint(2,20)
        sine=F(rng.randint(11,18),20)
        opposite=4*a*sine
        small=math.degrees(math.asin(float(sine))); large=180-small
        c2=150-large
        side=2*a
        return q('Angle A and opposite sides a and b are given. Two triangles are possible. Find both B values, smaller first, then the area of the triangle with the larger B. Round all answers to 3 decimal places.',
                 'Sudut A dan sisi bertentangan a dan b diberi. Dua segi tiga mungkin terbentuk. Cari kedua-dua nilai B, yang lebih kecil dahulu, kemudian luas segi tiga dengan B lebih besar. Bundarkan semua jawapan kepada 3 tempat perpuluhan.',
                 rf'A=30^\circ,\quad a={side},\quad b={num(opposite)}',
                 [small,large,.5*side*float(opposite)*math.sin(math.radians(c2))],
                 [('Smaller B (°)','B lebih kecil (°)'),('Larger B (°)','B lebih besar (°)'),('Area for larger B','Luas bagi B lebih besar')],
                 [('Apply the sine rule.','Gunakan petua sinus.',rf'\sin B=\dfrac{{b\sin A}}{{a}}={num(sine)}'),
                  ('Consider the supplementary angle and check C > 0.','Pertimbangkan sudut penggenap dan semak C > 0.',rf'B_1=\sin^{{-1}}({num(sine)}),\ B_2=180^\circ-B_1,\ C=180^\circ-A-B'),
                  ('Use the angle between sides a and b.','Gunakan sudut di antara sisi a dan b.',r'\text{Area}=\dfrac12ab\sin C')],
                 [('This is the ambiguous sine-rule case.','Ini ialah kes berambiguiti petua sinus.'),
                  ('Both B and 180° − B can share the same sine; test their remaining angles.','B dan 180° − B boleh mempunyai sinus sama; uji sudut bakinya.'),
                  ('The included angle for area ½ab sin C is C, not A or B.','Sudut kandung bagi luas ½ab sin C ialah C, bukan A atau B.')],tolerance=.0005)

    if topic == 'combinatorics':
        n=rng.randint(5,12); r=rng.randint(2,4)
        if not boss:
            return q(f'{n} distinct students stand in a row. {r} named students must stand together. Find the number of arrangements.',
                     f'{n} murid berlainan berdiri sebaris. {r} murid tertentu mesti berdiri bersama. Cari bilangan susunan.',
                     rf'n={n}',math.factorial(r)*math.factorial(n-r+1), [('Arrangements','Susunan')],
                     [('Treat the named group as one block.','Anggap kumpulan tertentu sebagai satu blok.',rf'(n-r+1)!={math.factorial(n-r+1)}'),
                      ('Allow every internal order.','Benarkan setiap turutan dalaman.',rf'N={r}!({n-r+1})!={math.factorial(r)*math.factorial(n-r+1)}')],
                     [('Count n − r + 1 objects by treating the group as a block.','Hitung n − r + 1 objek dengan menganggap kumpulan sebagai blok.'),
                      ('The named people can be permuted inside the block.','Orang tertentu boleh disusun dalam blok.')])
        boys=a; girls=k; size=min(4,boys+girls-1)
        committees=sum(math.comb(girls,j)*math.comb(boys,size-j) for j in range(2,min(girls,size)+1) if size-j<=boys)
        return q(f'A club has {boys} boys and {girls} girls, all distinct. A {size}-person committee needs at least two girls. Find the number of committees, then the number of ways to choose such a committee and appoint a chair and secretary from it.',
                 f'Kelab mempunyai {boys} lelaki dan {girls} perempuan, semuanya berlainan. Jawatankuasa {size} orang memerlukan sekurang-kurangnya dua perempuan. Cari bilangan jawatankuasa, kemudian bilangan cara memilih jawatankuasa itu serta melantik pengerusi dan setiausaha daripadanya.',
                 rf'n_B={boys},\ n_G={girls},\ r={size}',
                 [committees,committees*size*(size-1)], [('Committees','Jawatankuasa'),('Committees with roles','Jawatankuasa dengan jawatan')],
                 [('Split into disjoint cases by the number of girls.','Bahagikan kepada kes berasingan mengikut bilangan perempuan.',rf'N=\sum_{{j=2}}^{{{min(girls,size)}}}\binom{{{girls}}}j\binom{{{boys}}}{{{size}-j}}={committees}'),
                  ('Assign the two distinct roles within each committee.','Agihkan dua jawatan berbeza dalam setiap jawatankuasa.',rf'{committees}\times{size}\times{size-1}={committees*size*(size-1)}')],
                 [('At least two means sum the cases for two, three, and possibly four girls.','Sekurang-kurangnya dua bermaksud tambah kes dua, tiga dan mungkin empat perempuan.'),
                  ('Use combinations for membership; the chair and secretary roles are ordered.','Gunakan gabungan untuk keahlian; jawatan pengerusi dan setiausaha mempunyai turutan.'),
                  ('Multiply the committee count by r(r − 1), not by the total club membership.','Darab bilangan jawatankuasa dengan r(r − 1), bukan jumlah ahli kelab.')])

    if topic == 'series':
        if not boss:
            n=k+4
            return q('An arithmetic progression has the two stated terms. Find the first term, common difference, and sum of the first n terms.',
                     'Janjang aritmetik mempunyai dua sebutan diberi. Cari sebutan pertama, beza sepunya dan hasil tambah n sebutan pertama.',
                     rf'T_3={a+2*b},\ T_7={a+6*b},\ n={n}',
                     [a,b,F(n*(2*a+(n-1)*b),2)], [('First term','Sebutan pertama'),('Common difference','Beza sepunya'),('Sum','Hasil tambah')],
                     [('Subtract the term equations.','Tolak persamaan sebutan.',rf'4d={4*b}\Rightarrow d={b}'),
                      ('Find a, then use the sum formula.','Cari a, kemudian gunakan rumus hasil tambah.',rf'a={a},\quad S_{{{n}}}=\dfrac{{{n}}}2[2({a})+({n-1})({b})]')],
                     [('Write T₃ = a + 2d and T₇ = a + 6d.','Tulis T₃ = a + 2d dan T₇ = a + 6d.'),
                      ('Find d first; do not confuse term values with their positions.','Cari d dahulu; jangan keliru nilai sebutan dengan kedudukannya.')])
        first=a; ratio=F(1,k); inf=F(first,1)/(1-ratio); gap=inf*ratio**t
        return q('A positive geometric progression has sum to infinity S. The sum of its first two terms is U. Find the first term and common ratio (0 < r < 1). Then find the least n for which the remaining sum is strictly less than ε.',
                 'Janjang geometri positif mempunyai hasil tambah ketakterhinggaan S. Hasil tambah dua sebutan pertama ialah U. Cari sebutan pertama dan nisbah sepunya (0 < r < 1). Kemudian cari n terkecil apabila baki hasil tambah kurang secara ketat daripada ε.',
                 rf'S={num(inf)},\ U={num(F(first)*(1+ratio))},\ \varepsilon={num(gap)}',
                 [first,ratio,t+1], [('First term','Sebutan pertama'),('Ratio r','Nisbah r'),('Least n','n terkecil')],
                 [('Compare the finite and infinite sums.','Bandingkan hasil tambah terhingga dan tak terhingga.',r'U=S(1-r^2)\Rightarrow r=\sqrt{1-U/S}'),
                  ('Recover a and express the tail.','Dapatkan a dan ungkapkan baki.',rf'a=S(1-r)={first},\quad S-S_n=Sr^n'),
                  ('Apply the strict inequality.','Gunakan ketaksamaan ketat.',rf'r^n<r^{{{t}}},\ 0<r<1\Rightarrow n>{t}\Rightarrow n_{{\min}}={t+1}')],
                 [('Use S₂/S∞ = 1 − r² to determine r.','Gunakan S₂/S∞ = 1 − r² untuk menentukan r.'),
                  ('The remaining sum after n terms equals S∞rⁿ.','Baki hasil tambah selepas n sebutan sama dengan S∞rⁿ.'),
                  ('Equality at the threshold is not enough: the problem requires strictly less.','Kesamaan pada ambang tidak mencukupi: masalah memerlukan kurang secara ketat.')])

    if topic == 'vectors':
        if not boss:
            vx=b+3*a; vy=k+3*t
            return q('M divides AB internally in ratio AM:MB = 1:2. Find both coordinates of M and the magnitude of AM.',
                     'M membahagi AB secara dalaman dalam nisbah AM:MB = 1:2. Cari kedua-dua koordinat M dan magnitud AM.',
                     rf'A=({b},{k}),\ B=({vx},{vy})', [b+a,k+t,math.sqrt(a*a+t*t)],
                     [('M x','M x'),('M y','M y'),('Magnitude AM (3 d.p.)','Magnitud AM (3 t.p.)')],
                     [('Move one third of AB from A.','Bergerak satu pertiga AB dari A.',rf'\overrightarrow{{AM}}=\dfrac13\overrightarrow{{AB}}=({a},{t})'),
                      ('Add to A and calculate the magnitude.','Tambah kepada A dan hitung magnitud.',rf'M=({b+a},{k+t}),\quad |AM|=\sqrt{{{a*a+t*t}}}')],
                     [('The ratio 1:2 corresponds to one third, not one half, of AB.','Nisbah 1:2 bersamaan satu pertiga, bukan separuh, AB.'),
                      ('The magnitude uses displacement components, not the coordinates of M.','Magnitud menggunakan komponen sesaran, bukan koordinat M.')],tolerance=.0005)
        # OA=u, OB=v; P on AB with AP:PB=1:2 and Q on OP meeting B-line parallel OA.
        ux=a; uy=b; vx=-k; vy=t
        # Q = lambda P = v + mu u -> lambda/3=1 hence lambda3, mu2.
        return q('O is the origin, OA = u and OB = v. P divides AB with AP:PB = 1:2. Q is the intersection of line OP and the line through B parallel to OA. Find the coordinates of P and Q, then the scalar λ satisfying OQ = λ OP.',
                 'O ialah asalan, OA = u dan OB = v. P membahagi AB dengan AP:PB = 1:2. Q ialah persilangan garis OP dan garis melalui B selari dengan OA. Cari koordinat P dan Q, kemudian skalar λ yang memenuhi OQ = λ OP.',
                 rf'\mathbf u=({ux},{uy}),\quad\mathbf v=({vx},{vy})',
                 [F(2*ux+vx,3),F(2*uy+vy,3),2*ux+vx,2*uy+vy,3],
                 [('P x','P x'),('P y','P y'),('Q x','Q x'),('Q y','Q y'),('λ','λ')],
                 [('Use the section vector.','Gunakan vektor pembahagian.',r'\overrightarrow{OP}=\dfrac23\mathbf u+\dfrac13\mathbf v'),
                  ('Express Q in two ways and compare coefficients.','Ungkapkan Q dalam dua cara dan bandingkan pekali.',r'\lambda(\dfrac23\mathbf u+\dfrac13\mathbf v)=\mathbf v+\mu\mathbf u\Rightarrow\lambda=3,\mu=2'),
                  ('Evaluate the vectors.','Nilai vektor.',rf'\overrightarrow{{OQ}}=2\mathbf u+\mathbf v=({2*ux+vx},{2*uy+vy})')],
                 [('Write OP as a combination of u and v.','Tulis OP sebagai gabungan u dan v.'),
                  ('Q lies on OP, so OQ is a scalar multiple of OP; it also equals v + μu.','Q pada OP, maka OQ ialah gandaan skalar OP; ia juga sama dengan v + μu.'),
                  ('Compare the v coefficients first, then calculate the coordinate components.','Bandingkan pekali v dahulu, kemudian hitung komponen koordinat.')])

    if topic in ('calculus','differentiation','integration','kinematics'):
        sub=topic if topic!='calculus' else ['differentiation','integration','kinematics'][variant%3]
        if sub=='differentiation':
            if not boss:
                value=a*t*t+b; grad=2*a*t; intercept=value-grad*t
                return q(f'Find the gradient at x = {t}, then the tangent in the form y = mx + c. Enter the gradient and c.',
                         f'Cari kecerunan pada x = {t}, kemudian tangen dalam bentuk y = mx + c. Masukkan kecerunan dan c.',
                         rf'y={a}x^2+{b}',[grad,intercept], [('Gradient m','Kecerunan m'),('Intercept c','Pintasan c')],
                         [('Differentiate and evaluate at the point.','Bezakan dan nilai pada titik.',rf'y\prime={2*a}x\Rightarrow m={grad},\quad y({t})={value}'),
                          ('Use point-gradient form.','Gunakan bentuk titik-kecerunan.',rf'y-{value}={grad}(x-{t})\Rightarrow c={intercept}')],
                         [('A tangent needs both the gradient and the point on the curve.','Tangen memerlukan kecerunan dan titik pada lengkung.'),
                          ('Substitute the point into y = mx + c after differentiating.','Gantikan titik ke dalam y = mx + c selepas membezakan.')])
            # Cubic with stationary points b and b+k, derivative3a(x-b)(x-b-k).
            u=b; v=b+k; coeff=F(3*a*(u+v),2); lin=3*a*u*v
            val=lambda z: F(a*z**3)-coeff*z*z+lin*z+t
            return q('Find both stationary-point x coordinates, smaller first. Then give the local maximum y and local minimum y, in that order.',
                     'Cari kedua-dua koordinat x titik pegun, yang lebih kecil dahulu. Kemudian berikan maksimum tempatan y dan minimum tempatan y, mengikut turutan.',
                     rf'y={a}x^3-{num(coeff)}x^2+{lin}x+{t}',
                     [u,v,val(u),val(v)], [('Smaller stationary x','x pegun lebih kecil'),('Larger stationary x','x pegun lebih besar'),('Local maximum y','Maksimum tempatan y'),('Local minimum y','Minimum tempatan y')],
                     [('Set the first derivative to zero.','Samakan terbitan pertama dengan sifar.',rf'y\prime={3*a}(x-{u})(x-{v})=0'),
                      ('Classify with the second derivative.','Kelaskan menggunakan terbitan kedua.',rf'y\prime\prime={6*a}x-{3*a*(u+v)},\quad y\prime\prime({u})<0,\ y\prime\prime({v})>0'),
                      ('Evaluate the original curve, not its derivative.','Nilai lengkung asal, bukan terbitannya.',rf'y({u})={num(val(u))},\quad y({v})={num(val(v))}')],
                     [('Solve dy/dx = 0 before classifying the stationary points.','Selesaikan dy/dx = 0 sebelum mengelaskan titik pegun.'),
                      ('A negative second derivative means a local maximum; positive means minimum.','Terbitan kedua negatif bermaksud maksimum tempatan; positif bermaksud minimum.'),
                      ('Substitute the two x values into y to obtain the requested extreme values.','Gantikan dua nilai x ke dalam y untuk mendapatkan nilai ekstrem diminta.')])
        if sub=='integration':
            if not boss:
                value=a*t*t+k
                return q(f'Given dy/dx and a point, find the integration constant C in y = ax² + bx + C, then y({t}).',
                         f'Diberi dy/dx dan satu titik, cari pemalar pengamiran C dalam y = ax² + bx + C, kemudian y({t}).',
                         rf'\dfrac{{dy}}{{dx}}={2*a}x+{b},\quad y(1)={a+b+k}',
                         [k,a*t*t+b*t+k], [('C','C'),(f'y({t})',f'y({t})')],
                         [('Integrate term by term.','Kamirkan sebutan demi sebutan.',rf'y={a}x^2+{b}x+C'),
                          ('Use the known point before evaluating.','Gunakan titik diketahui sebelum menilai.',rf'C={k},\quad y({t})={a*t*t+b*t+k}')],
                         [('The integration constant is determined by the point, not assumed zero.','Pemalar pengamiran ditentukan oleh titik, bukan diandaikan sifar.'),
                          ('Substitute x = 1 and the given y value into the antiderivative.','Gantikan x = 1 dan nilai y diberi ke dalam antiterbitan.')])
            upper=b+k
            signed=F(upper**3,3)-F((b+upper)*upper*upper,2)+b*upper*upper
            f=lambda z:F(z**3,3)-F((b+upper)*z*z,2)+b*upper*z
            area=f(b)-f(0)-(f(upper)-f(b))
            return q('The curve crosses the x-axis inside the interval. Find the signed integral, then the total area between the curve and x-axis on that interval.',
                     'Lengkung melintasi paksi-x di dalam selang. Cari kamiran bertanda, kemudian jumlah luas antara lengkung dan paksi-x pada selang itu.',
                     rf'y=(x-{b})(x-{upper}),\quad0\leq x\leq{upper}',
                     [signed,area], [('Signed integral','Kamiran bertanda'),('Total area','Jumlah luas')],
                     [('Locate the crossings and an antiderivative.','Cari persilangan dan antiterbitan.',rf'x={b},{upper},\quad F(x)=\dfrac{{x^3}}3-\dfrac{{{b+upper}x^2}}2+{b*upper}x'),
                      ('Integrate normally for the signed value.','Kamirkan seperti biasa untuk nilai bertanda.',rf'\int_0^{{{upper}}}y\,dx={num(signed)}'),
                      ('Split at the internal root and reverse the negative part.','Pisahkan pada punca dalaman dan songsangkan bahagian negatif.',rf'A=[F({b})-F(0)]-[F({upper})-F({b})]={num(area)}')],
                     [('Area and signed integral differ when the curve changes sign.','Luas dan kamiran bertanda berbeza apabila lengkung berubah tanda.'),
                      ('Find both roots; split the integral at the root inside the interval.','Cari kedua-dua punca; pisahkan kamiran pada punca di dalam selang.'),
                      ('The curve is positive before the first root and negative between the roots.','Lengkung positif sebelum punca pertama dan negatif di antara punca.')])
        if not boss:
            return q(f'A particle has the stated acceleration and initial velocity. Find v({t}), then displacement between t=0 and t={t}.',
                     f'Zarah mempunyai pecutan diberi dan halaju awal. Cari v({t}), kemudian sesaran antara t=0 dan t={t}.',
                     rf'a(t)={2*a}t,\quad v(0)={b}', [a*t*t+b,F(a*t**3,3)+b*t],
                     [('Final velocity (m/s)','Halaju akhir (m/s)'),('Displacement (m)','Sesaran (m)')],
                     [('Integrate acceleration and apply the initial condition.','Kamirkan pecutan dan gunakan syarat awal.',rf'v(t)={a}t^2+{b}'),
                      ('Integrate velocity for displacement.','Kamirkan halaju untuk sesaran.',rf'\Delta s=\dfrac{{{a}({t})^3}}3+{b}({t})')],
                     [('Two integrations are needed: acceleration to velocity, then velocity to displacement.','Dua pengamiran diperlukan: pecutan kepada halaju, kemudian halaju kepada sesaran.'),
                      ('The first integration constant is the initial velocity.','Pemalar pengamiran pertama ialah halaju awal.')])
        u=b; end=b+k
        signed=F(a*end*end,2)-a*u*end
        total=F(a*u*u,2)+F(a*k*k,2)
        return q('Find when the particle changes direction, its displacement over the full interval, and its total distance travelled. Motion is in a straight line; s(0)=0.',
                 'Cari masa zarah menukar arah, sesarannya sepanjang selang penuh dan jumlah jarak dilalui. Gerakan adalah dalam garis lurus; s(0)=0.',
                 rf'v(t)={a}(t-{u}),\quad0\leq t\leq{end}',
                 [u,signed,total], [('Direction-change time (s)','Masa perubahan arah (s)'),('Displacement (m)','Sesaran (m)'),('Distance (m)','Jarak (m)')],
                 [('Find the zero of velocity and verify the sign change.','Cari sifar halaju dan sahkan perubahan tanda.',rf't={u},\quad v<0\ \text{{before}},\ v>0\ \text{{after}}'),
                  ('Integrate velocity for displacement.','Kamirkan halaju untuk sesaran.',rf'\Delta s=[{num(F(a,2))}t^2-{a*u}t]_0^{{{end}}}={num(signed)}'),
                  ('Add the magnitudes before and after reversal.','Tambah magnitud sebelum dan selepas perubahan arah.',rf'D=\dfrac{{{a}({u})^2}}2+\dfrac{{{a}({k})^2}}2={num(total)}')],
                 [('Direction changes where velocity is zero and changes sign.','Arah berubah apabila halaju sifar dan berubah tanda.'),
                  ('Displacement is the signed integral of v; distance is the integral of |v|.','Sesaran ialah kamiran bertanda v; jarak ialah kamiran |v|.'),
                  ('Split the distance calculation at the direction-change time.','Pisahkan pengiraan jarak pada masa perubahan arah.')])

    if topic=='index_numbers':
        i1=100+10*a; i2=100+10*b; w=k
        composite=F(w*i1+2*i2,w+2)
        if not boss:
            cost=20*t
            return q('Find the weighted composite price index, then the new cost of a basket whose base-year cost is C.',
                     'Cari indeks harga gubahan berwajaran, kemudian kos baharu bakul dengan kos tahun asas C.',
                     rf'I_1={i1},\ I_2={i2},\ w_1={w},\ w_2=2,\ C=\mathrm{{RM}}{cost}',
                     [composite,F(cost,100)*composite], [('Composite index','Indeks gubahan'),('New cost (RM)','Kos baharu (RM)')],
                     [('Compute the weighted mean.','Hitung min berwajaran.',rf'I=\dfrac{{{w}({i1})+2({i2})}}{{{w+2}}}={num(composite)}'),
                      ('Apply the index to the base cost.','Gunakan indeks pada kos asas.',rf'C_1={cost}\cdot I/100={num(F(cost,100)*composite)}')],
                     [('Use weights in both numerator and denominator.','Gunakan wajaran dalam pembilang dan penyebut.'),
                      ('An index of I multiplies the base cost by I/100.','Indeks I mendarab kos asas dengan I/100.')])
        missing=110+10*t; comp=F(w*i1+2*missing,w+2); next_index=100+10*b
        cost=10*a
        return q('The composite index for year B relative to year A is given, with one component missing. Find that component. A basket then has index J for year C relative to B. Find its C-to-A composite index and C cost if it cost C₀ in A.',
                 'Indeks gubahan tahun B berbanding tahun A diberi, dengan satu komponen hilang. Cari komponen itu. Bakul kemudian mempunyai indeks J bagi tahun C berbanding B. Cari indeks gubahan C-ke-A dan kos C jika kosnya C₀ dalam A.',
                 rf'I_1={i1},\ w_1={w},\ w_2=2,\ I_{{B/A}}={num(comp)},\ J_{{C/B}}={next_index},\ C_0=\mathrm{{RM}}{cost}',
                 [missing,comp*F(next_index,100),F(cost,100)*comp*F(next_index,100)],
                 [('Missing component index','Indeks komponen hilang'),('C-to-A index','Indeks C-ke-A'),('Year C cost (RM)','Kos tahun C (RM)')],
                 [('Rearrange the weighted mean.','Susun semula min berwajaran.',rf'I_2=\dfrac{{({w+2})({num(comp)})-{w}({i1})}}2={missing}'),
                  ('Chain the indices multiplicatively.','Rantaikan indeks secara pendaraban.',rf'I_{{C/A}}=\dfrac{{I_{{C/B}}I_{{B/A}}}}{{100}}={num(comp*F(next_index,100))}'),
                  ('Use the chained index on the original cost.','Gunakan indeks berantai pada kos asal.',rf'C_C={num(F(cost,100)*comp*F(next_index,100))}')],
                 [('Solve the weighted mean equation for the missing index first.','Selesaikan persamaan min berwajaran untuk indeks hilang dahulu.'),
                  ('Indices with different base years cannot simply be added.','Indeks dengan tahun asas berlainan tidak boleh ditambah terus.'),
                  ('C/A = (C/B)(B/A)/100; use the resulting index with the A-year cost.','C/A = (C/B)(B/A)/100; gunakan indeks terhasil dengan kos tahun A.')])

    if topic=='probability':
        n=a+2; p=F(1,k)
        if not boss:
            ans=1-(1-p)**n-n*p*(1-p)**(n-1)
            return q('For this binomial variable, find P(X ≥ 2), its mean and variance.',
                     'Bagi pemboleh ubah binomial ini, cari P(X ≥ 2), min dan variansnya.',
                     rf'X\sim B({n},{num(p)})', [ans,n*p,n*p*(1-p)],
                     [('P(X ≥ 2)','P(X ≥ 2)'),('Mean','Min'),('Variance','Varians')],
                     [('Use the complement for the tail.','Gunakan pelengkap bagi hujung taburan.',rf'P(X\geq2)=1-(1-p)^{{{n}}}-{n}p(1-p)^{{{n-1}}}'),
                      ('Use binomial moments.','Gunakan momen binomial.',r'\mu=np,\quad\sigma^2=np(1-p)')],
                     [('It is shorter to subtract P(0) and P(1) from 1.','Lebih ringkas menolak P(0) dan P(1) daripada 1.'),
                      ('The mean is np; multiply it by 1 − p for the variance.','Min ialah np; darabkannya dengan 1 − p untuk varians.')])
        # Infer binomial parameters from moments, then compute an acceptance tail.
        mean=n*p; variance=n*p*(1-p); cutoff=2
        accept=sum(F(math.comb(n,j))*p**j*(1-p)**(n-j) for j in range(cutoff+1))
        return q('The number of defective units in a batch follows a binomial distribution. Given its mean and variance, find n and p. A batch is accepted when at most two units are defective. Find its acceptance probability and the expected number of accepted batches out of 100 independent batches.',
                 'Bilangan unit cacat dalam satu kelompok mengikut taburan binomial. Diberi min dan varians, cari n dan p. Kelompok diterima apabila paling banyak dua unit cacat. Cari kebarangkalian penerimaan dan jangkaan bilangan kelompok diterima daripada 100 kelompok bebas.',
                 rf'\mu={num(mean)},\quad\sigma^2={num(variance)}',
                 [n,p,accept,100*accept], [('n','n'),('p','p'),('Acceptance probability','Kebarangkalian penerimaan'),('Expected accepted batches','Jangkaan kelompok diterima')],
                 [('Recover p using the variance-to-mean ratio.','Dapatkan p menggunakan nisbah varians kepada min.',rf'1-p=\sigma^2/\mu\Rightarrow p={num(p)},\quad n=\mu/p={n}'),
                  ('Sum the three permitted defect counts.','Tambah tiga bilangan cacat yang dibenarkan.',rf'P(X\leq2)=\sum_{{j=0}}^2\binom{{{n}}}j p^j(1-p)^{{{n}-j}}={num(accept)}'),
                  ('Multiply the probability by the number of batches.','Darab kebarangkalian dengan bilangan kelompok.',rf'E=100P(X\leq2)={num(100*accept)}')],
                 [('Use mean = np and variance = np(1 − p) simultaneously.','Gunakan min = np dan varians = np(1 − p) secara serentak.'),
                  ('At most two includes zero, one and two defects.','Paling banyak dua merangkumi sifar, satu dan dua kecacatan.'),
                  ('The expected count need not be an integer; keep exact fractions where possible.','Bilangan jangkaan tidak semestinya integer; kekalkan pecahan tepat jika boleh.')])

    if topic=='linear_programming':
        # Two resource constraints cross at (a,b), non-negative feasible polygon.
        c1=2*a+b; c2=a+2*b
        corners=[(F(0),F(0)),(min(F(c1,2),F(c2)),F(0)),(F(a),F(b)),(F(0),min(F(c1),F(c2,2)))]
        if not boss:
            vals=[3*x+2*y for x,y in corners]; idx=vals.index(max(vals)); pt=corners[idx]
            return q('For real non-negative x and y, find the optimal x, y, and maximum P. Construct the feasible region or compare all feasible corners.',
                     'Bagi x dan y nyata yang tidak negatif, cari x, y optimum dan maksimum P. Bina rantau tersaur atau bandingkan semua bucu tersaur.',
                     rf'2x+y\leq{c1},\quad x+2y\leq{c2},\quad P=3x+2y',
                     [pt[0],pt[1],max(vals)], [('Optimal x','x optimum'),('Optimal y','y optimum'),('Maximum P','Maksimum P')],
                     [('Intersect both resource boundaries.','Silangkan kedua-dua sempadan sumber.',rf'(x,y)=({a},{b})'),
                      ('Compare the objective at all feasible corners.','Bandingkan objektif pada semua bucu tersaur.',r'P\in\{'+','.join(num(v) for v in vals)+r'\}'),
                      ('Select the largest value.','Pilih nilai terbesar.',rf'P_{{\max}}={num(max(vals))}')],
                     [('The intersection of constraints is a candidate, not automatically the optimum.','Persilangan kekangan ialah calon, bukan optimum secara automatik.'),
                      ('Find the feasible intercepts on both axes and compare with the intersection.','Cari pintasan tersaur pada kedua-dua paksi dan bandingkan dengan persilangan.')])
        # Profit 3x+2y is strictly inside the normal cone, maximum at integer (a,b).
        profit=3*a+2*b; target=profit-k
        feasible=[(xx,yy) for xx in range(c1//2+1) for yy in range(c2//2+1) if 2*xx+yy<=c1 and xx+2*yy<=c2]
        count=sum(3*xx+2*yy>=target for xx,yy in feasible)
        return q('A workshop makes whole numbers x and y of two products. Resources impose the constraints below and profit is P. Find the optimal quantities and maximum profit. Then count all feasible integer plans earning at least the stated target.',
                 'Bengkel menghasilkan bilangan bulat x dan y bagi dua produk. Sumber mengenakan kekangan di bawah dan keuntungan ialah P. Cari kuantiti optimum dan keuntungan maksimum. Kemudian hitung semua rancangan integer tersaur yang memperoleh sekurang-kurangnya sasaran diberi.',
                 rf'x,y\in\mathbb Z_{{\geq0}},\quad2x+y\leq{c1},\quad x+2y\leq{c2},\quad P=3x+2y,\quad P\geq{target}',
                 [a,b,profit,count], [('Optimal x','x optimum'),('Optimal y','y optimum'),('Maximum profit','Keuntungan maksimum'),('Plans meeting target','Rancangan mencapai sasaran')],
                 [('Solve the intersection and compare feasible corners.','Selesaikan persilangan dan bandingkan bucu tersaur.',rf'(x,y)=({a},{b}),\quad P_{{\max}}={profit}'),
                  ('Restrict the final count to integer lattice points.','Hadkan pengiraan akhir kepada titik kekisi integer.',rf'0\leq x\leq{c1//2},\quad0\leq y\leq\min({c1}-2x,\lfloor({c2}-x)/2\rfloor)'),
                  ('Apply the profit target to each integer plan.','Gunakan sasaran keuntungan pada setiap rancangan integer.',rf'3x+2y\geq{target}\Rightarrow N={count}')],
                 [('First solve the continuous corner problem, then check that the optimum is an integer plan.','Selesaikan masalah bucu selanjar dahulu, kemudian semak optimum ialah rancangan integer.'),
                  ('For the count, include boundary points and restrict x and y to non-negative integers.','Untuk bilangan, masukkan titik sempadan dan hadkan x dan y kepada integer tidak negatif.'),
                  ('For each feasible x, list integer y values satisfying both resources and the profit target.','Bagi setiap x tersaur, senaraikan y integer yang memenuhi kedua-dua sumber dan sasaran keuntungan.')])
    raise ValueError('No progression template for '+topic)
