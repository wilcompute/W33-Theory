"""12365: are SM_2618's unpaired fractional-charge fermions forbidden at EVERY order?  For each conjugate candidate pair: (i) the degree-
bounded MILP with a large cap; (ii) an exact lattice test with no positivity and no degree bound -- integer z_s (net powers of each
singlet), all translation sectors allowed (the most permissive rule): Q^T z = -q, sum n = 0 mod 6, sum Witten = 0 mod 2, sum lat in
sum_k (1 - theta^k) Lambda.  Infeasible (ii) = forbidden at all orders by gauge + space-group rules."""
import os, sys, json, itertools
import numpy as np
import networkx as nx
from scipy.optimize import milp, LinearConstraint, Bounds
sys.path.insert(0, '.')
import mono
from mono import FS, S, NS, NQ, QS, DENS, D6, I3, I2, min_degree
import sympy as sp
def frac(f):
    d, y = f['d'], f['y']
    for t in ([sp.Rational(1, 2), -sp.Rational(1, 2)] if abs(d[I2]) == 2 else [0]):
        if (3 * (t + y) if abs(d[I3]) == 3 else t + y).is_integer is False:
            return True
    return False
Fr = [f for f in FS if f['m'] == 19 and frac(f)]
conj = lambda d: tuple(-x if abs(x) > 2 else x for x in d)
def lattice_ok(a, b):
    nv = NS + 30 + 2; A, rhs = [], []
    tq = [int((a['q'][j] + b['q'][j]) * DENS[j]) for j in range(NQ)]
    for j in range(NQ):
        A.append(list(QS[:, j]) + [0] * 32); rhs.append(-tq[j])
    A.append([f['n'] for f in S] + [0] * 30 + [-6, 0]); rhs.append(-(a['n'] + b['n']))
    A.append([f['w'] for f in S] + [0] * 30 + [0, -2]); rhs.append(-(a['w'] + b['w']))
    for i in range(6):
        yrow = []
        for k in range(1, 6): yrow += list(-D6[k][i, :])
        A.append([f['lat'][i] for f in S] + yrow + [0, 0]); rhs.append(-(a['lat'][i] + b['lat'][i]))
    B = 10 ** 4
    r = milp(np.zeros(nv), constraints=LinearConstraint(np.array(A, dtype=float), rhs, rhs), integrality=np.ones(nv), bounds=Bounds([-B] * nv, [B] * nv))
    return r.success
out = dict(model=mono.M_, fractional=len(Fr), pairs=[])
G1, G2 = nx.Graph(), nx.Graph(); G1.add_nodes_from(range(len(Fr))); G2.add_nodes_from(range(len(Fr)))
for i, j in itertools.combinations(range(len(Fr)), 2):
    a, b = Fr[i], Fr[j]
    if conj(a['d']) == b['d'] and a['y'] + b['y'] == 0:
        r = min_degree([(a, 1), (b, 1)], xmax=20, cap=40); lt = lattice_ok(a, b)
        out['pairs'].append(dict(i=i, j=j, degree=None if r is None else r[0], lattice=lt))
        if r is not None: G1.add_edge(i, j)
        if lt: G2.add_edge(i, j)
m1 = len(nx.max_weight_matching(G1, maxcardinality=True)); m2 = len(nx.max_weight_matching(G2, maxcardinality=True))
# Majorana self-pairing (Pass 12451): a single Weyl fermion in a REAL representation with Y = 0 (dims all 1 or 2, an even number of 2s) may
# take a mass psi psi s^n if the lattice test passes with the field taken twice.  Dirac-only matching (12353/12365/12443) missed this.
def is_real(d):
    return all(abs(x) in (1, 2) for x in d) and sum(1 for x in d if abs(x) == 2) % 2 == 0
if os.environ.get('LIFT_MAJORANA'):
    selfok = {i: bool(is_real(Fr[i]['d']) and Fr[i]['y'] == 0 and lattice_ok(Fr[i], Fr[i])) for i in range(len(Fr))}
    M2 = nx.max_weight_matching(G2, maxcardinality=True)
    left = [i for i in range(len(Fr)) if not any(i in e for e in M2)]
    out['majorana_rescued'] = sum(1 for i in left if selfok[i])
    out['liftable_with_majorana'] = 2 * len(M2) + out['majorana_rescued']
    out['real_y0_fields'] = sum(1 for i in range(len(Fr)) if is_real(Fr[i]['d']) and Fr[i]['y'] == 0)
    out['real_y0_self_ok'] = sum(selfok.values())
    out['self_lattice_ok_any_rep'] = sum(1 for i in range(len(Fr)) if lattice_ok(Fr[i], Fr[i]))  # control: the self-test must be able to fail
out.update(liftable_cap40=2 * m1, liftable_all_orders_upper=2 * m2,
           unmatched_types=sorted({str((Fr[i]['d'][I3], Fr[i]['d'][I2], str(Fr[i]['y']))) for i in range(len(Fr)) if i not in {x for e in nx.max_weight_matching(G2, maxcardinality=True) for x in e}}))
print({k: v for k, v in out.items() if k != 'pairs'})
json.dump(out, open(f'lift_exact_{mono.M_}' + ('_maj' if os.environ.get('LIFT_MAJORANA') else '') + '.json', 'w'), indent=1, default=str)
