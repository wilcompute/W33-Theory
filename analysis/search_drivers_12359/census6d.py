"""12359b: large-radius tachyon census.  For every tachyon-free non-SUSY Z6-II parent (12324), the 6D theories of the two fixed tori:
theta^2 sub-orbifold with W5 = W6 = 0 (torus e5e6) and theta^3 sub-orbifold with W3 = W4 = 0 (torus e3e4).  Any 6D tachyon reappears in
the full model at nonzero fixed-torus momentum (the quotient by theta pairs p with -p and keeps one combination), so it makes the model
tachyonic at large radius of that torus.  This script writes the model files and the list; verb6d.sh runs the verbose solver."""
import json, os
from fractions import Fraction as F
tf = [os.path.basename(x.replace(chr(92), '/')) for x in json.load(open('../search_drivers_12322/tachfree_parents.json'))['tachyon_free_parents']]
os.makedirs('c6d', exist_ok=True); lst = []
for m in tf:
    p = f'../search_drivers_12281/bro/{m}__ctrl.txt'
    if not os.path.exists(p): p = f'../search_drivers_12302/bro/{m}__ctrl.txt'
    L = open(p).read().split('\n'); i = L.index('Shifts and Wilsonlines:')
    assert 'Geometry_Z6-II_1_1.txt' in L[2], (m, L[2])
    rows = [r.split() for r in L[i + 1:i + 10]]
    for tag, s, zero in (('t3', 2, (7, 8)), ('t2', 3, (5, 6))):
        r = [list(x) for x in rows]; r[1] = [str(F(x) * s) for x in r[1]]
        for z in zero: r[z] = ['0'] * 16
        out = list(L); out[i + 1:i + 10] = [' '.join(x) for x in r]
        out[2] = f'SpaceGroup:Geometry/Geometry_Z6-II_sub{s}.txt'
        f = f'c6d/{m}__{tag}.txt'; open(f, 'w', newline='\n').write('\n'.join(out)); lst.append(f)
open('c6d_list.txt', 'w', newline='\n').write('\n'.join(lst) + '\n')
print(len(tf), 'parents', len(lst), 'runs')
