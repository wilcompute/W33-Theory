"""12366: all-radius tachyon census of the 99 tachyon-free non-SUSY Z6-II parents (Wilson lines ON):
  e5e6 small radius: theta^2 sub-orbifold with constructing elements shifted by -e5 (odd winding; w = +1 trips an engine assertion,
  every other odd w gives identical output, 12363);  e3e4 small radius: theta^3 sub-orbifold shifted by -e3 and by -2 e3 (W3 = W4, so
  the classes w3 + w4 = 2, 1 mod 3).  Untwisted and Witten-untwisted elements are left unshifted (the engine cannot take a shifted
  untwisted element; those channels keep 12352's necessary-condition status).  Large radius: 12359b (Wilson lines off)."""
import sys, os, json
from fractions import Fraction as F
sys.path.insert(0, '.')
from gen_wind import build_off
src = open('../search_drivers_12359/parent_geom.txt').read()
H0 = src.split('begin constructing elements')[0].replace('point group\n2\n6\n1', 'point group\n2\n@N@\n1').replace(' 0/1 1/6 1/3 -1/2', ' @TWIST@')
heads = {2: H0.replace('allowed order of Wilson lines\n1\n1\n3\n3\n2\n2', 'allowed order of Wilson lines\n3\n3\n3\n3\n2\n2').replace('begin identical WLs\n 3 4', 'begin identical WLs\n 1 2\n 3 4'),
         3: H0.replace('allowed order of Wilson lines\n1\n1\n3\n3\n2\n2', 'allowed order of Wilson lines\n2\n2\n3\n3\n2\n2').replace('begin identical WLs\n 3 4\n', 'begin identical WLs\n')}
GEO = dict(e5=(2, [0, 0, 0, 0, -1, 0]), e3a=(3, [0, 0, -1, 0, 0, 0]), e3b=(3, [0, 0, -2, 0, 0, 0]))
for tag, (s, off) in GEO.items():
    g = build_off(s, heads[s], off); h, rest = g.split('begin constructing elements')
    o = ' '.join(str(x) for x in off)
    for k0 in ('0 0', '1 0'):
        rest = rest.replace(f'{k0} 0 {o} ', f'{k0} 0 0 0 0 0 0 0 ')
    open(f'Geometry_Z6-II_win_{tag}.txt', 'w', newline='\n').write(h + 'begin constructing elements' + rest)
tf = [os.path.basename(x.replace(chr(92), '/')) for x in json.load(open('../search_drivers_12322/tachfree_parents.json'))['tachyon_free_parents']]
os.makedirs('ca', exist_ok=True); lst = []
for m in tf:
    p = f'../search_drivers_12281/bro/{m}__ctrl.txt'
    if not os.path.exists(p): p = f'../search_drivers_12302/bro/{m}__ctrl.txt'
    L = open(p).read().split('\n'); i = L.index('Shifts and Wilsonlines:')
    rows = [r.split() for r in L[i + 1:i + 10]]
    for tag, (s, off) in GEO.items():
        r = [list(x) for x in rows]; r[1] = [str(F(x) * s) for x in r[1]]
        out = list(L); out[i + 1:i + 10] = [' '.join(x) for x in r]; out[2] = f'SpaceGroup:Geometry/Geometry_Z6-II_win_{tag}.txt'
        f = f'ca/{m}__{tag}'; open(f + '.txt', 'w', newline='\n').write('\n'.join(out)); lst.append(f)
open('ca_list.txt', 'w', newline='\n').write('\n'.join(lst) + '\n'); print(len(lst))
