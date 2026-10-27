"""12322b: the Witten-twisted untwisted sector (V_h = V0; right-moving vacuum -1/2): minimal left level P^2/2 - 1 over E8 x E8 + V0
(and + V0 + W5, the coset reached by winding along e5).  Tachyon channels need L_int = -1/2 (n w = 0) or -1 (n w = 1/2)."""
import sys, json
from fractions import Fraction as F
sys.argv = ['x']
exec(open('lmin.py').read().split('def lmin(')[0])
out = {}
for v in ('v9', 'v4', 'v0'):
    for tag in ('ctrl', 'w6odd'):
        p = f'../search_drivers_12281/bro/Z6II_60_SM_20260917_810_{v}__{tag}.txt'
        try:
            _, rows = read(p)
        except FileNotFoundError:
            _, rows = read(p.replace('12281', '12302'))
        V0, W5 = rows[0], rows[7]
        r = {}
        for lab, Vh in (('V0', V0), ('V0+W5', [a + b for a, b in zip(V0, W5)])):
            n2 = e8_min_norm_coset(Vh[:8]) + e8_min_norm_coset(Vh[8:])
            r[lab] = str(n2 / 2 - 1)
        out[f'{v}_{tag}'] = r; print(v, tag, r)
json.dump(out, open('lmin0.json', 'w'), indent=1)
