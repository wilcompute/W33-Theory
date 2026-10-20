import sys, json
import sympy as sp
from fractions import Fraction as Fr
sys.path.insert(0, r'C:\tmp\toe_round\stype')
import hyper as H

res = {}
for m in sys.argv[1:]:
    fac, u1, fields = H.parse(r'C:\tmp\toe_round\stype\q4\%s.q' % m)
    r = H.analyse(r'C:\tmp\toe_round\stype\q4\%s.q' % m)
    exact = [s for s in r['sols'] if H.is_sm(s['net'])]
    res[m] = dict(L=r['L'], R=r['R'], nsol=r['nsol'], n_exact_sm=len(exact),
                  exact_y2=sorted(set(str(s['y2']) for s in exact)), free=sorted(set(s['free'] for s in exact)))
    print(m, res[m], flush=True)
json.dump(res, open(r'C:\tmp\toe_round\stype\hyper_4.json', 'w'), indent=1)
