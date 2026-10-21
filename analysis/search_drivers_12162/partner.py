"""12164: is the Fricke partner the Wilson-line conjugate (W -> -W, W -> 2W) or a single-torus flip? Compare Witten-level multiplicities
of candidate partners at 0.52i with S002 at 0.641i (where 272 <-> 104 are swapped)."""
import sys, json
from fractions import Fraction as Fr
from collections import Counter
sys.path.insert(0, r'C:\tmp\toe_round\stype')
import marginal as Mg
rows = open(r'C:\tmp\toe_wt\analysis\search_drivers_12116\smwl\N004_F1_03_S002.txt').read().split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n')
rows = [r.strip().split() for r in rows]


def block(rr):
    return [','.join(r) for r in [rr[0], rr[1]] + rr[3:9]]


def scale(r, k):
    return [str(Fr(x) * k) for x in r]


cands = {'orig': rows,
         'minusW_both': [rows[0], rows[1], rows[2]] + [scale(r, -1) for r in rows[3:7]] + rows[7:9],
         'twoW_both': [rows[0], rows[1], rows[2]] + [scale(r, 2) for r in rows[3:7]] + rows[7:9],
         'minusW_family': [rows[0], rows[1], rows[2]] + [scale(r, -1) for r in rows[3:5]] + rows[5:9],
         'minusW_second': rows[0:5] + [scale(r, -1) for r in rows[5:7]] + rows[7:9],
         'minusV1': [rows[0], scale(rows[1], -1)] + rows[2:9]}
out = {}
for name, rr in cands.items():
    for y in ((0.52, 1 / (3 * 0.52)) if name == 'orig' else (0.52,)):
        f = Mg.levels(block(rr), [y * 1j, y * 1j], Mg.RHO, cut=0.6)
        c = Counter(round(s['Delta'], 9) for s in f)
        out['%s@%.4f' % (name, y)] = {str(k): v for k, v in sorted(c.items())}
        print(name, y, sorted(c.items()), flush=True)
json.dump(out, open('partner.json', 'w'), indent=1)
print('DONE')
