"""12450b: the 4754 double count for the POINT graph.  A weight-(q+1) kernel word would be q+1 pairwise non-collinear points with every
other point collinear with 0 or 2 of them (equality case of sum c_x = w q(q+1), sum c_x(c_x-1) = w(w-1)(q+1)).  In Q(4,q) that set is a
conic (4754).  In W(3,q) the natural candidate -- the q+1 points of a hyperbolic (non-isotropic) line -- gives c_x in {1, q+1}: ODD.
Check exhaustively at q = 3 that NO 4-set of pairwise non-collinear points has all c_x in {0,2} (equivalently d > 4, the CP-SAT control)."""
import sys, json, itertools
import numpy as np
sys.path.insert(0, '../search_drivers_12419')
from two_codes import w3q
out = {}
for q in (3,):
    A = w3q(q); n = len(A)
    cnt = good = 0; hyp_profile = set()
    for S in itertools.combinations(range(n), q + 1):
        if any(A[a, b] for a, b in itertools.combinations(S, 2)): continue
        cnt += 1
        c = A[:, list(S)].sum(1)
        outside = [c[x] for x in range(n) if x not in S]
        if all(v in (0, 2) for v in outside): good += 1
        if set(outside) <= {1, q + 1}: hyp_profile.add(tuple(sorted(int(v) for v in set(outside))))
    out[q] = dict(partial_ovoids_of_size_q_plus_1=cnt, with_even_profile=good, hyperbolic_line_profiles=sorted(hyp_profile))
    print(q, out[q])
json.dump(out, open('equality_case.json', 'w'), indent=1)
