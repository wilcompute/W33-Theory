"""12458b: controls for the empty D-flat support of vacuum_c22.py.  (i) homogeneous (xi = 0) D-flat directions of the full singlets: support
of the cone {v >= 0, Q^T v = 0}; (ii) FI-cancelling support when SM singlets charged under the HIDDEN non-abelian factors are admitted
(abelian D-terms only -- a necessary condition; non-abelian D-flatness not imposed); (iii) the same with every scalar admitted (SM-charged
too) -- shows which fields CAN cancel the FI term."""
import os, sys, json
import numpy as np
from scipy.optimize import linprog
b = sys.argv[1] if len(sys.argv) > 1 else 'Z6II_06_SM_20260917_2541_c22'
sys.argv = [sys.argv[0], b]
D = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(D, 'vacuum_c22.py'), encoding='utf-8').read().split("def support(sign):")[0])   # reuse the set-up (fields, qT, Q)
def supp(fields, sign, homogeneous=False):
    Qm = np.array([[float(f['q'][j]) for j in range(NQ)] for f in fields]); n = len(fields); out = []
    for i in range(n):
        c = np.zeros(n + 1); c[i] = -1
        Aeq = np.hstack([Qm.T, (sign * qT)[:, None]])
        bnds = [(0, 10)] * n + ([(0, 0)] if homogeneous else [(1e-4, 1e-4)])
        r = linprog(c, A_eq=Aeq, b_eq=np.zeros(NQ), bounds=bnds, method='highs')
        if r.status == 0 and -r.fun > 1e-9: out.append(i)
    return out
sc = [f for f in FS if f['m'] in (15, 16) and f['P'] is not None]
sm_single = [f for f in sc if abs(f['d'][I3]) == 1 and abs(f['d'][I2]) == 1 and f['y'] == 0]
res = dict(full_singlets=NS, homogeneous_support=len(supp(S, 1, True)),
           sm_singlets_incl_hidden=len(sm_single), fi_support_hidden_plus=len(supp(sm_single, 1)), fi_support_hidden_minus=len(supp(sm_single, -1)),
           all_scalars=len(sc), fi_support_all_plus=len(supp(sc, 1)), fi_support_all_minus=len(supp(sc, -1)))
print(res)
json.dump(res, open(os.path.join(D, f'dflat_controls_{b}.json'), 'w'), indent=1)
# (iv) negative control: a target OUTSIDE the singlet charge span must give empty support (the LP can say no)
import sympy as sp
Qx = sp.Matrix([[f['q'][j] for j in range(NQ)] for f in S]); ns = Qx.nullspace()            # 9-vectors orthogonal to every singlet charge row, hence outside their span
bad = np.array([float(x) for x in ns[0]]) if ns else None
if bad is not None:
    saved = qT.copy(); qT = bad * 100
    res['control_outside_span_support'] = len(supp(S, 1)); qT = saved
print(res); json.dump(res, open(os.path.join(D, f'dflat_controls_{b}.json'), 'w'), indent=1)
