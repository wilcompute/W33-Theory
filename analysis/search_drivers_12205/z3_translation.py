"""12207: order-3 translations commuting with the T6/Z3 twist: common kernel of (M_theta - 1) mod 3 (exact, GF(3)), and of
(M - 1) mod 2 (control: 0, Pass 12177)."""
import json, sys
import numpy as np
from sympy import Matrix, GF
from sympy.polys.matrices import DomainMatrix
sys.path.insert(0, '../search_drivers_12174')
from ss_translations import parse, rot

tw, B = parse('../search_drivers_12174/geometry/Geometry_Z3_SU3^3.txt')
M = np.round(np.linalg.solve(B, rot(tw[0]) @ B)).astype(int)
out = {}
for p in (2, 3):
    dm = DomainMatrix.from_Matrix(Matrix(((M - np.eye(6, dtype=int)) % p).tolist())).convert_to(GF(p))
    out[f'kernel_mod{p}'] = 6 - dm.rank()
out['det(1-theta)'] = int(round(np.linalg.det(np.eye(6) - M)))
print(out)
json.dump(out, open('z3_translation.json', 'w'), indent=1)
