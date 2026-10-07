"""Topic menus, not a claim of complete examination-objective coverage."""
TOPICS = {
 'functions': ('Functions', 'Fungsi'),
 'quadratics': ('Quadratic functions', 'Fungsi kuadratik'),
 'polynomials': ('Factors of polynomials', 'Faktor polinomial'),
 'equations': ('Equations, inequalities & graphs', 'Persamaan, ketaksamaan & graf'),
 'simultaneous': ('Simultaneous equations', 'Sistem persamaan'),
 'logarithms': ('Logarithmic & exponential functions', 'Fungsi logaritma & eksponen'),
 'straight_lines': ('Straight-line graphs', 'Graf garis lurus'),
 'circles': ('Coordinate geometry of the circle', 'Geometri koordinat bulatan'),
 'circular': ('Circular measure', 'Sukatan membulat'),
 'trig': ('Trigonometry', 'Trigonometri'),
 'combinatorics': ('Permutations & combinations', 'Pilih atur & gabungan'),
 'series': ('Series / progressions', 'Janjang'),
 'vectors': ('Vectors in two dimensions', 'Vektor dalam dua dimensi'),
 'calculus': ('Calculus', 'Kalkulus'),
 'indices': ('Indices, surds & logarithms', 'Indeks, surd & logaritma'),
 'linear_law': ('Linear law', 'Hukum linear'),
 'coordinates': ('Coordinate geometry', 'Geometri koordinat'),
 'triangles': ('Solution of triangles', 'Penyelesaian segi tiga'),
 'index_numbers': ('Index numbers', 'Nombor indeks'),
 'differentiation': ('Differentiation', 'Pembezaan'),
 'integration': ('Integration', 'Pengamiran'),
 'probability': ('Probability distributions', 'Taburan kebarangkalian'),
 'kinematics': ('Kinematics of linear motion', 'Kinematik gerakan linear'),
 'linear_programming': ('Linear programming', 'Pengaturcaraan linear'),
}
CAMBRIDGE = ['functions','quadratics','polynomials','equations','simultaneous','logarithms','straight_lines','circles','circular','trig','combinatorics','series','vectors','calculus']
SPM4 = ['functions','quadratics','simultaneous','indices','series','linear_law','coordinates','vectors','triangles','index_numbers']
SPM5 = ['circular','differentiation','integration','trig','combinatorics','probability','kinematics','linear_programming']
TRACKS = ['Cambridge IGCSE 0606', 'SPM KSSM Additional Mathematics']
LEVELS = ['Warm-up', 'Level up', 'Boss mode']


def topics_for(track, form='All'):
    if track == TRACKS[0]:
        return CAMBRIDGE
    return SPM4 if form == 'Form 4 / Tingkatan 4' else SPM5 if form == 'Form 5 / Tingkatan 5' else SPM4 + SPM5


def title(key, language='Bilingual'):
    en,bm = TOPICS[key]
    return en if language == 'English' else bm if language == 'Bahasa Melayu' else en + ' / ' + bm

PROGRESSION = 'Build my skills'
LEVEL_DESCRIPTIONS = {
 'Warm-up': ('Core skills and direct applications', 'Kemahiran asas dan aplikasi langsung'),
 'Level up': ('Linked steps, transformations and interpretation', 'Langkah berkaitan, transformasi dan pentafsiran'),
 'Boss mode': ('Multi-step exam-style reasoning and constraints', 'Penaakulan gaya peperiksaan berbilang langkah dan kekangan'),
 PROGRESSION: ('Start with core skills, then linked steps, then exam-style challenges', 'Mulakan dengan asas, kemudian langkah berkaitan, diikuti cabaran gaya peperiksaan'),
}
