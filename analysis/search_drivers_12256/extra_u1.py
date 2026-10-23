"""12256: the extra U(1) of the SM_2496 shift class.  u = the direction of the v0 hidden-A4 Cartan orthogonal to the A2 + A1 roots that
v9 keeps (12244); check it lies in v9's U(1) span, and compute Tr Q_u (mixed gravitational anomaly) over v9's left-handed fermions
(code 19, every left weight), alongside the same trace for each of v9's U(1) directions (the anomalous U(1) of the orbifolder has
nonzero trace)."""
import json, re, sys
import numpy as np
sys.path.insert(0, '../search_drivers_12238')
src = open('../search_drivers_12238/higgs_branch.py').read().split('u0 = unbroken')[0]
exec(src)
u0 = unbroken('../search_drivers_12238/model_2496_v0.txt'); u9 = unbroken('../search_drivers_12238/model_2496_v9.txt')
A4 = [c for c in comps(u0) if len(c) == 20][0]
B = np.linalg.svd(R[A4])[2][:4]
keep = [i for i in u9 if np.linalg.norm(R[i] - (R[i] @ B.T) @ B) < 1e-9]
K = np.linalg.svd(R[keep])[2][:3]
coef = np.linalg.svd(B @ K.T @ K - B)  # complement inside span(B)
P = B - (B @ K.T) @ K
uu = np.linalg.svd(P)[2][0]
u = (uu @ B.T) @ B
u = u / np.linalg.norm(u)
U1, fields, cur = [], [], None
for l in open('nsoq_v9.txt'):
    if l.startswith('U1 '):
        U1.append(np.array([float(x) for x in l.split('|')[1].split()]))
    elif l.startswith('FIELD'):
        m = re.match(r'FIELD \d+ m=(\d+)', l); cur = dict(m=int(m.group(1)), W=[]); fields.append(cur)
    elif l.startswith('W ') and cur:
        cur['W'].append(np.array([float(x) for x in l[2:].split(',')]))
U = np.array(U1)
resid = np.linalg.norm(u - (np.linalg.lstsq(U.T, u, rcond=None)[0] @ U))
left = [w for f in fields if f['m'] == 19 for w in f['W']]
trace = lambda d: float(sum(w @ d for w in left))
out = dict(n_u1=len(U1), u_in_u1_span_residual=float(resid), tr_u=trace(u), tr_u1_dirs=[round(trace(d / np.linalg.norm(d)), 6) for d in U],
           left_weights=len(left))
print(out)
json.dump(out, open('extra_u1.json', 'w'), indent=1)
