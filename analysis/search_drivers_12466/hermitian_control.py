"""12496 control for hermitian_test.py: the same GF(3) solver must find a Hermitian form on 240 points of the surface
x0 xbar0 + x1 xbar1 + x2 xbar2 + x3 xbar3 = 0 (280 points in PG(3,9)).  usage: py -3 hermitian_control.py"""
import sys, json, random
sys.argv = ["x", "symmetric_fast_q9_r10.json", "1"]
src = open("hermitian_test.py", encoding="utf-8").read().split("M = DomainMatrix")[0]
exec(src)
from sympy.polys.matrices import DomainMatrix
from sympy.polys.domains import GF
surf = [p for p in range(len(pts)) if (sum(mul[pts[p][i]][frob(pts[p][i])] for i in range(4)) % 3) == 0]
sample = random.Random(1).sample(surf, 240)
M = DomainMatrix([[GF(3)(v) for v in herm_terms(pts[p])] for p in sample], (240, 16), GF(3))
R, piv = M.rref()
out = dict(surface_points=len(surf), sample=240, nullity=16 - len(piv))
print(out); json.dump(out, open("hermitian_control.json", "w"))
