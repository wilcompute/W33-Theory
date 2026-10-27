"""12292: can the left-right candidate's vector-like fractional-charge fermions be lifted by SM-singlet scalar vevs?
Left-handed Weyl fermions (m=19; the m=20 list is their CPT conjugates).  A mass term chi_a chi_b S_1 ... S_n needs conjugate
representations (SU3, SU2_a, SU2_b, SU8), Y_a + Y_b = 0, and q_a + q_b in the span of the U(1) charge vectors of the SM-singlet scalars
(all dims 1, Y = 0 at t = -1/148; scalars are complex, so signed combinations).  Span over Q here: necessary, not sufficient (integer
span and discrete selection rules not imposed) -- an UPPER BOUND.  The number of fields liftable at once = 2 x maximum matching."""
import re, sys, json, itertools, collections
import sympy as sp
import networkx as nx
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
        m = re.match(r'FIELD (\d+) m=(\S+) k=\S+ mm=\S+ n=\S+ lat=\S+ dim=(\S*) q=(\S*)', l)
        if m and int(m.group(2)) in kinds:
            d = [int(re.match(r'-?\d+', x).group(0)) for x in m.group(3).split(',')] if m.group(3) else []
            q = sp.Matrix([sp.nsimplify(float(x), tolerance=1e-9, rational=True) for x in m.group(4).split(',') if x])
            out.append(dict(i=int(m.group(1)), dims=d, q=q, y=sum(a * b for a, b in zip(cv, q))))
    return out
def frac(d, y):
    tl = [sp.Rational(1, 2), -sp.Rational(1, 2)] if abs(d[1]) == 2 else [0]
    tr = [sp.Rational(1, 2), -sp.Rational(1, 2)] if abs(d[2]) == 2 else [0]
    return any((3 * (a + b + y) if abs(d[0]) == 3 else a + b + y).is_integer is False for a in tl for b in tr)
L = recs({19}); S = [r for r in recs({15, 16}) if all(abs(x) == 1 for x in r['dims']) and r['y'] == 0]
F = [r for r in L if frac(r['dims'], r['y'])]
Smat = sp.Matrix.hstack(*[r['q'] for r in S])
rk = Smat.rank()
def in_span(v):
    return sp.Matrix.hstack(Smat, v).rank() == rk
conj = lambda d: [(-x if abs(x) in (3, 8, 28, 56) else x) for x in d]
G = nx.Graph(); G.add_nodes_from(range(len(F)))
cache = {}
for a, b in itertools.combinations(range(len(F)), 2):
    A, Bf = F[a], F[b]
    if conj(A['dims']) != Bf['dims'] or A['y'] + Bf['y'] != 0:
        continue
    key = tuple(A['q'] + Bf['q'])
    if key not in cache:
        cache[key] = in_span(A['q'] + Bf['q'])
    if cache[key]:
        G.add_edge(a, b)
M = nx.max_weight_matching(G, maxcardinality=True)
# rep-and-Y balance: a vector-like set needs every (rep, Y) matched by (conj rep, -Y)
bal = collections.Counter()
for r in F:
    bal[(tuple(r['dims']), r['y'])] += 1
unbalanced = sum(abs(v - bal.get((tuple(conj(list(k[0]))), -k[1]), 0)) for k, v in bal.items()) // 2
out = dict(fractional_fermions=len(F), singlet_scalars=len(S), singlet_charge_rank=int(rk), allowed_pairs=G.number_of_edges(),
           liftable_fields=2 * len(M), unbalanced=int(unbalanced))
print(out)
json.dump(out, open('lift.json', 'w'), indent=1)
