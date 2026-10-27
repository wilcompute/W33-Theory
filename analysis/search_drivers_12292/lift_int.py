"""12292b: integer-lattice version of lift.py -- q_a + q_b must be an INTEGER combination of the singlet charge vectors (a monomial of
singlet vevs and conjugates).  Lattice basis by the Hermite normal form (charges scaled to integers by their common denominator)."""
import json, itertools, sys
import sympy as sp
import networkx as nx
from sympy.matrices.normalforms import hermite_normal_form
sys.argv = ['x']
exec(open('lift.py').read().split('Smat = ')[0])
den = sp.ilcm(*[x.q for r in S for x in r['q']] + [x.q for r in F for x in r['q']])
Sint = sp.Matrix.hstack(*[r['q'] * den for r in S])
assert all(e.is_integer for e in Sint)
Sint = Sint.applyfunc(lambda e: sp.Integer(e))
H = hermite_normal_form(Sint)            # columns span the same lattice
H = sp.Matrix.hstack(*[H[:, j] for j in range(H.shape[1]) if any(H[:, j])])
def in_lattice(v):
    v = v * den
    sol = H.gauss_jordan_solve(v)
    try:
        x, params = sol
    except Exception:
        return False
    x = x.subs({p: 0 for p in params})
    return all(e.is_integer for e in x)
conj = lambda d: [(-x if abs(x) in (3, 8, 28, 56) else x) for x in d]
G = nx.Graph(); G.add_nodes_from(range(len(F)))
for a, b in itertools.combinations(range(len(F)), 2):
    A, Bf = F[a], F[b]
    if conj(A['dims']) != Bf['dims'] or A['y'] + Bf['y'] != 0:
        continue
    try:
        ok = in_lattice(A['q'] + Bf['q'])
    except ValueError:
        ok = False
    if ok:
        G.add_edge(a, b)
M = nx.max_weight_matching(G, maxcardinality=True)
out = dict(lattice_rank=H.shape[1], allowed_pairs_integer=G.number_of_edges(), liftable_fields_integer=2 * len(M), fractional_fermions=len(F))
print(out); json.dump(out, open('lift_int.json', 'w'), indent=1)
