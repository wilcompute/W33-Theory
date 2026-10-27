"""12286d: hypercharge as a lattice vector, Y_vec = sum_i c_i u_i + alpha_R/2 (u_i = the engine's U(1) directions, alpha_R the simple
root of the second A1), verified on every field's left-moving weights against the charge-based Y (T3R included via the weight), and
k_Y = 2 |Y_vec|^2 (GUT normalisation 5/3)."""
import re, json, sys
import numpy as np
import sympy as sp
sys.path.insert(0, '.')
from lr_hypercharge import solve, fermions
p = '../search_drivers_12281/bro/Z6II_60_SM_20260917_810_v9__w6odd.nsoq'
T0 = sp.Rational(-1, 148)
fs = fermions(p); c, eqs, sol = solve(fs); s = sol[0]
free = sorted((set(c) - set(s)) | {x for v in s.values() for x in sp.sympify(v).free_symbols}, key=str)
cv = np.array([float(sp.sympify(s.get(ci, ci)).subs(free[0], T0)) for ci in c])
L = open(p).read().split('\n')
U = np.array([[float(x) for x in l.split('|')[1].split()] for l in L if l.startswith('U1 ')])
fac = [l for l in L if l.startswith('FACTOR')]
print([f.split('|')[0] for f in fac])
roots = {}
for f in fac:
    head, *rs = f.split('|')
    roots[head.strip()] = [np.array([float(x) for x in r.split()]) for r in rs]
# second A1 = SU(2)_R: the third FACTOR in 'A2 + A1 + A1 and A7'
keys = list(roots)
aR = roots[keys[2]][0]
# the charges q_i printed by the engine: test q_i = u_i . P / |u_i|^2 or u_i . P on the first weights
Yvec = None
recs = []
cur = None
for l in L:
    if l.startswith('FIELD'):
        m = re.match(r'FIELD \d+ m=(\S+) .* dim=(\S*) q=(\S*)', l)
        cur = dict(q=np.array([float(x) for x in m.group(3).split(',') if x]), W=[])
        recs.append(cur)
    elif l.startswith('W ') and cur is not None:
        cur['W'].append(np.array([float(x) for x in l[2:].split(',')]))
r = [x for x in recs if x['W']][:40]
dots = np.array([[u @ x['W'][0] for u in U] for x in r]); qs = np.array([x['q'][:len(U)] for x in r])
ratio = np.nanmedian(qs / np.where(np.abs(dots) > 1e-9, dots, np.nan), axis=0)
print('q_i / (u_i.P) =', np.round(ratio, 6))
Yvec = (cv * ratio) @ U + aR / 2
err = max(abs(Yvec @ x['W'][0] - (cv @ (x['q'][:len(U)]) + (aR / 2) @ x['W'][0])) for x in recs if x['W'])
kY = 2 * Yvec @ Yvec
print('consistency max err', err, ' k_Y =', kY, ' (as fraction', sp.nsimplify(kY, tolerance=1e-9, rational=True), ')')
json.dump(dict(kY=str(sp.nsimplify(kY, tolerance=1e-9, rational=True)), kY_float=kY, ratio=ratio.tolist(), Yvec=Yvec.tolist()), open('lr_ky.json', 'w'), indent=1)
