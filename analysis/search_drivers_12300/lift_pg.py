"""12300: the candidate's mass pairings under gauge + point-group + Witten selection: chi_a chi_b S_1...S_n needs q_a + q_b + sum x_k q_k = 0
(x_k integer, conjugate scalars = negative x), and sum of Z6 powers n = 0 mod 6, sum of Witten labels = 0 mod 2 over all fields
(conjugates negated).  Implemented as an integer lattice: generators = singlet vectors (q, n, mm) plus 6 e_n and 2 e_mm.
The fixed-point (translation) part of the space-group rule is not imposed: still an upper bound, tighter than 12292."""
import re, sys, itertools, json
import sympy as sp
import networkx as nx
from sympy.matrices.normalforms import hermite_normal_form
sys.path.insert(0, '../search_drivers_12286')
from lr_hypercharge import solve, fermions
P = '../search_drivers_12281/bro/Z6II_60_SM_20260917_810_v9__w6odd.nsoq'
T0 = sp.Rational(-1, 148)
fs = fermions(P); c, eqs, sol = solve(fs); s = sol[0]
free = sorted((set(c) - set(s)) | {x for v in s.values() for x in sp.sympify(v).free_symbols}, key=str)
cv = [sp.sympify(s.get(ci, ci)).subs(free[0], T0) for ci in c]
def recs(kinds):
    out = []
    for l in open(P):
        m = re.match(r'FIELD (\d+) m=(\S+) k=\S+ mm=(\S+) n=(\S+) lat=\S+ dim=(\S*) q=(\S*)', l)
        if m and int(m.group(2)) in kinds:
            d = [int(re.match(r'-?\d+', x).group(0)) for x in m.group(5).split(',')] if m.group(5) else []
            q = [sp.nsimplify(float(x), tolerance=1e-9, rational=True) for x in m.group(6).split(',') if x]
            out.append(dict(dims=d, q=q, mm=int(m.group(3)), n=int(m.group(4)), y=sum(a * b for a, b in zip(cv, q))))
    return out
def frac(d, y):
    tl = [sp.Rational(1, 2), -sp.Rational(1, 2)] if abs(d[1]) == 2 else [0]
    tr = [sp.Rational(1, 2), -sp.Rational(1, 2)] if abs(d[2]) == 2 else [0]
    return any((3 * (a + b + y) if abs(d[0]) == 3 else a + b + y).is_integer is False for a in tl for b in tr)
L = recs({19}); S = [r for r in recs({15, 16}) if all(abs(x) == 1 for x in r['dims']) and r['y'] == 0]
Fr = [r for r in L if frac(r['dims'], r['y'])]
den = sp.ilcm(*[x.q for r in S + Fr for x in r['q']])
vec = lambda r: sp.Matrix([x * den for x in r['q']] + [r['n'], r['mm']])
nq = len(S[0]['q'])
gens = [vec(r) for r in S] + [sp.Matrix([0] * nq + [6, 0]), sp.Matrix([0] * nq + [0, 2])]
M = sp.Matrix.hstack(*gens).applyfunc(lambda e: sp.Integer(e))
H = hermite_normal_form(M); H = sp.Matrix.hstack(*[H[:, j] for j in range(H.shape[1]) if any(H[:, j])])
def in_lattice(v):
    try:
        x, params = H.gauss_jordan_solve(v)
    except ValueError:
        return False
    return all(e.is_integer for e in x.subs({p: 0 for p in params}))
conj = lambda d: [(-x if abs(x) in (3, 8, 28, 56) else x) for x in d]
G = nx.Graph(); G.add_nodes_from(range(len(Fr)))
for a, b in itertools.combinations(range(len(Fr)), 2):
    A, B = Fr[a], Fr[b]
    if conj(A['dims']) != B['dims'] or A['y'] + B['y'] != 0:
        continue
    if in_lattice(vec(A) + vec(B)):
        G.add_edge(a, b)
Mt = nx.max_weight_matching(G, maxcardinality=True)
out = dict(fractional_fermions=len(Fr), allowed_pairs=G.number_of_edges(), liftable=2 * len(Mt))
print(out); json.dump(out, open('lift_pg.json', 'w'), indent=1)
