"""12235b: parity of V0.V1, V0.Wf and V0.W over the whole one-line admissible space (7 bases x 864 lambda x 6561 mu, 12161
admissibility) and over the 405 twisted-10 candidates: if V0.W is odd, the projection constant becomes (w + m)/2 on fixed points
with odd label m along the torus of W, and the scalar condition must be applied sector by sector."""
import itertools, json, sys
import numpy as np
from fractions import Fraction as Fr
src = open('../search_drivers_12217/exhaust10.py').read().split("D = r'C:")[0]
exec(src)
D = r'C:\tmp\toe_wt\analysis\search_drivers_12111'
BASES = ['N001_F1_04', 'N004_F1_03', 'N004_F1_04', 'N004_F1_05', 'N008_F1_02', 'N008_F1_03', 'N008_F1_04']
out = {}
for base in BASES:
    rows = open(D + '/' + base + '_9.txt').read().split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n')
    v = [np.array([float(Fr(x)) for x in r.split()[:16]]) for r in rows]
    V0, V1, Wf = v[0], v[1], v[3]
    d5 = next(c for c in g.comps(integ(R @ V0[:8]) & integ(R @ V1[:8]) & integ(R @ Wf[:8])) if len(c) == 40)
    P = integ(R[d5] @ L3.T)
    pool = [jj for jj in range(len(coefs)) if g.typ(np.isin(np.arange(240), np.array(d5)[P[:, jj]])) == ('A4',)]
    lam, mu = L3[pool], L3
    W2n = (lam * lam).sum(1)[:, None] + (mu * mu).sum(1)[None, :]
    c0 = (lam @ V0[:8])[:, None] + (mu @ V0[8:])[None, :]
    adm = (np.abs(3 * W2n / 2 - np.round(3 * W2n / 2)) < 1e-9) & integ(3 * ((lam @ V1[:8])[:, None] + (mu @ V1[8:])[None, :])) \
        & integ(c0) & integ(3 * ((lam @ Wf[:8])[:, None] + (mu @ Wf[8:])[None, :]))
    odd = adm & (np.abs(np.round(c0) % 2 - 1) < 1e-9)
    out[base] = dict(V0V1=float(V0 @ V1), V0Wf=float(V0 @ Wf), V0sq=float(V0 @ V0), admissible=int(adm.sum()), V0W_odd=int(odd.sum()))
    print(base, out[base], flush=True)
cand = json.load(open('../search_drivers_12217/candidate_pairs.json'))
json.dump(out, open('parity_space.json', 'w'), indent=1)
