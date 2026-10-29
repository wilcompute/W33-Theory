"""12451: which selection rule keeps the SM_2541 (1,2,0) fractional pair massless?  For SM_2541_c22 with its first relaxed hypercharge:
all (1,2,0) left-handed doublets (Y = 0, charges +-1/2); for every pair, the exact all-orders lattice test of 12365 (integer net singlet
powers, no degree bound) with ONE rule dropped at a time: gauge U(1) charges / point group (sum n = 0 mod 6) / Witten parity (sum = 0 mod 2)
/ space-group translations.  Reports the maximum matching of the (1,2,0) doublets under each relaxation: the rule whose removal completes
the matching is the obstruction."""
import os, sys, json, itertools
import numpy as np
import networkx as nx
from scipy.optimize import milp, LinearConstraint, Bounds
b = 'Z6II_06_SM_20260917_2541_c22'
D = os.path.dirname(os.path.abspath(__file__))
Y = json.load(open(os.path.join(D, '..', 'search_drivers_12364', f'ysearch_{b}_noanom_loose.json')))['solutions'][0]['t']
os.environ.update(MONO_MODEL=b, MONO_PATH=os.path.join(D, '..', 'search_drivers_12373', 'spec', f'{b}.nsoq'), MONO_Y=json.dumps(Y), MONO_I3='4', MONO_I2='5')
sys.path.insert(0, os.path.join(D, '..', 'search_drivers_12357'))
import mono
from mono import FS, S, NS, NQ, QS, DENS, D6, I3, I2
dbl = [f for f in FS if f['m'] == 19 and abs(f['d'][I3]) == 1 and abs(f['d'][I2]) == 2 and f['y'] == 0]
conj = lambda d: tuple(-x if abs(x) > 2 else x for x in d)
print('(1,2,0) doublets:', len(dbl), [f['d'] for f in dbl])


def ok(a, bb, drop):
    nv = NS + 30 + 2; A, rhs = [], []
    if drop != 'gauge':
        tq = [int((a['q'][j] + bb['q'][j]) * DENS[j]) for j in range(NQ)]
        for j in range(NQ):
            A.append(list(QS[:, j]) + [0] * 32); rhs.append(-tq[j])
    if drop != 'point_group':
        A.append([f['n'] for f in S] + [0] * 30 + [-6, 0]); rhs.append(-(a['n'] + bb['n']))
    if drop != 'witten':
        A.append([f['w'] for f in S] + [0] * 30 + [0, -2]); rhs.append(-(a['w'] + bb['w']))
    if drop != 'translation':
        for i in range(6):
            yrow = []
            for k in range(1, 6): yrow += list(-D6[k][i, :])
            A.append([f['lat'][i] for f in S] + yrow + [0, 0]); rhs.append(-(a['lat'][i] + bb['lat'][i]))
    if not A:
        return True
    B = 10 ** 4
    r = milp(np.zeros(nv), constraints=LinearConstraint(np.array(A, dtype=float), rhs, rhs), integrality=np.ones(nv), bounds=Bounds([-B] * nv, [B] * nv))
    return bool(r.success)


out = dict(doublets=len(dbl))
for drop in ('none', 'gauge', 'point_group', 'witten', 'translation'):
    G = nx.Graph(); G.add_nodes_from(range(len(dbl)))
    for i, j in itertools.combinations(range(len(dbl)), 2):
        if conj(dbl[i]['d']) == dbl[j]['d'] and ok(dbl[i], dbl[j], drop):
            G.add_edge(i, j)
    mt = len(nx.max_weight_matching(G, maxcardinality=True))
    out[drop] = dict(edges=G.number_of_edges(), matched=2 * mt, unmatched=len(dbl) - 2 * mt)
    print(drop, out[drop], flush=True)
json.dump(out, open(os.path.join(D, 'which_rule.json'), 'w'), indent=1)

# Majorana self-pairing: a single Weyl fermion in a REAL representation (here (2,2) of SU(2)_hidden x SU(2)_L: pseudo-real x pseudo-real)
# can have a mass psi psi s^n if the singlets cancel 2 q_psi and the space-group sums of the field taken twice.  Earlier lifting tests
# (12353, 12365, 12443) only paired DISTINCT fields.
def is_real(d):
    pseudo = sum(1 for x in d if abs(x) == 2)          # SU(2) doublets are pseudo-real; an even number of them gives a real rep
    return all(abs(x) in (1, 2) for x in d) and pseudo % 2 == 0
self_ok = {i: (is_real(f['d']) and ok(f, f, 'none')) for i, f in enumerate(dbl)}
G = nx.Graph(); G.add_nodes_from(range(len(dbl)))
for i, j in itertools.combinations(range(len(dbl)), 2):
    if conj(dbl[i]['d']) == dbl[j]['d'] and ok(dbl[i], dbl[j], 'none'):
        G.add_edge(i, j)
mt = nx.max_weight_matching(G, maxcardinality=True)
left = [i for i in range(len(dbl)) if not any(i in e for e in mt)]
out['majorana'] = dict(real_rep={i: is_real(f['d']) for i, f in enumerate(dbl)}, self_pairing_allowed={i: bool(v) for i, v in self_ok.items()},
                       unmatched_after_dirac=left, unmatched_after_majorana=[i for i in left if not self_ok[i]])
print('majorana', out['majorana'], flush=True)
json.dump(out, open(os.path.join(D, 'which_rule.json'), 'w'), indent=1)
