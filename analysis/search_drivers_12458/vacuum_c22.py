"""12458: a D-flat vacuum for SM_2541 that lifts every fractional state?  Fields: the full singlets S of mono (scalars m = 15, singlets of
every non-abelian factor, Y = 0), so only abelian D-terms act.  Anomalous U(1): T_anom = sum of all weights of all massless Weyl fermions
(m = 19), projected on the U(1) subspace; FI term xi ~ Tr Q_A > 0, so D-flatness is
        sum_i v_i q(s_i) = -c q(T_anom),   v_i = |<s_i>|^2 >= 0,  c > 0   (q = coordinates in the U(1) basis UB of mono).
LP 1: the maximal simultaneous support S* (union over i of {max v_i > 0}; a convex combination of the witnesses realises all of them).
LP 2: re-run the exact all-orders lifting (Dirac pairs of distinct conjugate fields + Majorana self-masses of real-rep Y = 0 fields), with
net singlet powers restricted to S* (powers of singlets outside S* forced to zero).  Not imposed: F-terms do not exist (non-SUSY); the
one-loop potential, its minimisation and the VEV sizes are not computed; the FI sign follows the standard Tr Q_A > 0 convention, and the
opposite sign is reported as a control.  usage: py -3 vacuum_c22.py MODEL [Ylabel]"""
import os, sys, json, itertools
import numpy as np
import networkx as nx
from scipy.optimize import linprog, milp, LinearConstraint, Bounds
b = sys.argv[1] if len(sys.argv) > 1 else 'Z6II_06_SM_20260917_2541_c22'
D = os.path.dirname(os.path.abspath(__file__))
F3 = {json.loads(l)['base']: json.loads(l) for f in __import__('glob').glob(os.path.join(D, '..', 'search_drivers_12373', 'filt3_*.jsonl')) for l in open(f)}
Y = json.load(open(os.path.join(D, '..', 'search_drivers_12364', f'ysearch_{b}_noanom_loose.json')))['solutions'][0]['t']
su3, su2 = F3[b]['su3su2']
os.environ.update(MONO_MODEL=b, MONO_PATH=os.path.join(D, '..', 'search_drivers_12373', 'spec', f'{b}.nsoq'), MONO_Y=json.dumps(Y),
                  MONO_I3=str(su3), MONO_I2=str(su2))
sys.path.insert(0, os.path.join(D, '..', 'search_drivers_12357'))
import mono
from mono import FS, S, NS, NQ, QS, DENS, D6, UB, I3, I2
import sympy as sp

# anomalous direction: all weights of all Weyl fermions
P = os.environ['MONO_PATH']; T = sp.zeros(16, 1); cur = None
for l in open(P, errors='ignore'):
    if l.startswith('FIELD'):
        cur = int(l.split()[2][2:])
    elif l.startswith('W ') and cur == 19:
        T += sp.Matrix([sp.nsimplify(float(x), tolerance=1e-9, rational=True) for x in l[2:].split(',')])
qT = np.array([float((u.T * T)[0]) for u in UB])
Q = np.array([[float(f['q'][j]) for j in range(NQ)] for f in S])        # NS x NQ
rec = dict(model=b, singlets=NS, n_u1=NQ, qT_norm=float(np.linalg.norm(qT)))


def support(sign):
    sup = []
    for i in range(NS):
        c = np.zeros(NS + 1); c[i] = -1
        Aeq = np.hstack([Q.T, (sign * qT)[:, None]]); beq = np.zeros(NQ)
        bnds = [(0, 10)] * NS + [(1e-4, 1e-4)]                         # c fixed small: v <= 10 must not cap the scale (12458c: c = 1 with v <= 10 gave a false empty support)
        r = linprog(c, A_eq=Aeq, b_eq=beq, bounds=bnds, method='highs')
        if r.status == 0 and -r.fun > 1e-9: sup.append(i)
    return sup


sup = support(+1)            # sum v q = -qT  <=>  Q^T v + qT = 0
sup_wrong = support(-1)
rec.update(support=len(sup), support_opposite_FI_sign=len(sup_wrong))
allowed = np.zeros(NS, dtype=bool); allowed[sup] = True

def frac(f):                                     # as lift_exact.py (12365): some component has non-integer charge (colour-adjusted)
    d, y = f['d'], f['y']
    for t in ([sp.Rational(1, 2), -sp.Rational(1, 2)] if abs(d[I2]) == 2 else [0]):
        if (3 * (t + y) if abs(d[I3]) == 3 else t + y).is_integer is False:
            return True
    return False
Fr = [f for f in FS if f['m'] == 19 and frac(f)]
conj = lambda d: tuple(-x if abs(x) > 2 else x for x in d)


def lat(a, bb, allowed):
    nv = NS + 30 + 2; A, rhs = [], []
    tq = [int((a['q'][j] + bb['q'][j]) * DENS[j]) for j in range(NQ)]
    for j in range(NQ):
        A.append(list(QS[:, j]) + [0] * 32); rhs.append(-tq[j])
    A.append([f['n'] for f in S] + [0] * 30 + [-6, 0]); rhs.append(-(a['n'] + bb['n']))
    A.append([f['w'] for f in S] + [0] * 30 + [0, -2]); rhs.append(-(a['w'] + bb['w']))
    for i in range(6):
        yrow = []
        for k in range(1, 6): yrow += list(-D6[k][i, :])
        A.append([f['lat'][i] for f in S] + yrow + [0, 0]); rhs.append(-(a['lat'][i] + bb['lat'][i]))
    B = 10 ** 4
    lo = [(-B if allowed[i] else 0) for i in range(NS)] + [-B] * 32; hi = [(B if allowed[i] else 0) for i in range(NS)] + [B] * 32
    r = milp(np.zeros(nv), constraints=LinearConstraint(np.array(A, dtype=float), rhs, rhs), integrality=np.ones(nv), bounds=Bounds(lo, hi))
    return bool(r.success)


def is_real(d):
    return all(abs(x) in (1, 2) for x in d) and sum(1 for x in d if abs(x) == 2) % 2 == 0


for tag, al in (('all_singlets', np.ones(NS, dtype=bool)), ('dflat_support', allowed)):
    G = nx.Graph(); G.add_nodes_from(range(len(Fr)))
    for i, j in itertools.combinations(range(len(Fr)), 2):
        if conj(Fr[i]['d']) == Fr[j]['d'] and Fr[i]['y'] + Fr[j]['y'] == 0 and lat(Fr[i], Fr[j], al): G.add_edge(i, j)
    M = nx.max_weight_matching(G, maxcardinality=True)
    left = [i for i in range(len(Fr)) if not any(i in e for e in M)]
    maj = [i for i in left if is_real(Fr[i]['d']) and Fr[i]['y'] == 0 and lat(Fr[i], Fr[i], al)]
    rec[tag] = dict(fractional=len(Fr), dirac=2 * len(M), majorana=len(maj), liftable=2 * len(M) + len(maj))
    print(tag, rec[tag], flush=True)
print({k: v for k, v in rec.items() if not isinstance(v, dict)})
json.dump(rec, open(os.path.join(D, f'vacuum_{b}.json'), 'w'), indent=1)
