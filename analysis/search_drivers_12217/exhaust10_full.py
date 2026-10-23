"""12217b: the twisted-10 THEOREM on the full 7 x 864 x 6561 space of admissible second Wilson lines W = (lambda, mu) (lambda one
of the 864 A4-type first-E8 classes, mu any of the 6561 second-E8 order-3 classes; admissibility of Pass 12161: 3 W^2 even,
3 V1.W, V0.W, 3 Wf.W integral).  A twisted 10 needs P = (P1, P2), |P|^2 = 4/3, |proj_A4 P1|^2 = 6/5.  Step 1 (exhaust10.py):
the first-E8 hits have |P1|^2 in {4/3, 11/9}, so they need |P2|^2 = 0 resp. 1/9 in the second-E8 class
v2 = V1_2 + n1 Wf_2 + n2 mu + w V0_2.  Step 2: for every admissible (lambda, mu) and every fixed-point label (n1, n2, w) with a
first-E8 hit of norm a, test whether E8 + v2 contains a vector of norm exactly 4/3 - a.  Reports the number of admissible pairs
and of pairs admitting a twisted 10-type massless vector."""
import itertools, json, sys
import numpy as np
from fractions import Fraction as Fr
src = open('exhaust10.py').read().split("D = r'C:")[0]
exec(src)
D = r'C:\tmp\toe_wt\analysis\search_drivers_12111'
BASES = ['N001_F1_04', 'N004_F1_03', 'N004_F1_04', 'N004_F1_05', 'N008_F1_02', 'N008_F1_03', 'N008_F1_04']


def norms_in(u, targets):
    Q = E8S + reduce(u)
    nn = (Q * Q).sum(1)
    return {t for t in targets if np.any(np.abs(nn - t) < 1e-9)}


out = {}
pairs = []
for base in BASES:
    rows = open(D + '/' + base + '_9.txt').read().split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n')
    v = [np.array([float(Fr(x)) for x in r.split()[:16]]) for r in rows]
    V0, V1, Wf = v[0], v[1], v[3]
    d5 = next(c for c in g.comps(integ(R @ V0[:8]) & integ(R @ V1[:8]) & integ(R @ Wf[:8])) if len(c) == 40)
    P = integ(R[d5] @ L3.T)
    lam_idx, need = [], []
    for j in range(len(coefs)):
        mk = np.zeros(240, bool); mk[np.array(d5)[P[:, j]]] = True
        if g.typ(mk) != ('A4',):
            continue
        B = np.linalg.svd(R[np.nonzero(mk)[0]])[2][:4]
        req = {}
        for n1, n2, w in itertools.product(range(3), range(3), (0, 1)):
            u = V1[:8] + n1 * Wf[:8] + n2 * L3[j] + w * V0[:8]
            Q = E8S + reduce(u); nn = (Q * Q).sum(1); keep = nn <= 4 / 3 + 1e-9
            pr = Q[keep] @ B.T; m = np.abs((pr * pr).sum(1) - 6 / 5) < 1e-9
            if m.any():
                req[(n1, n2, w)] = {round(4 / 3 - a, 9) for a in nn[keep][m]}
        lam_idx.append(j); need.append(req)
    lam = L3[lam_idx]
    mu = L3
    # admissibility, vectorised over (lambda, mu)
    W2 = (lam * lam).sum(1)[:, None] + (mu * mu).sum(1)[None, :]
    c1 = (lam @ V1[:8])[:, None] + (mu @ V1[8:])[None, :]
    c0 = (lam @ V0[:8])[:, None] + (mu @ V0[8:])[None, :]
    cf = (lam @ Wf[:8])[:, None] + (mu @ Wf[8:])[None, :]
    adm = (np.abs(3 * W2 / 2 - np.round(3 * W2 / 2)) < 1e-9) & integ(3 * c1) & integ(c0) & integ(3 * cf)
    # second-E8 attainable norms per (mu, n1, n2, w)
    cache = {}
    def attain(k, n1, n2, w, targets):
        key = (k, n1, n2, w)
        if key not in cache:
            cache[key] = norms_in(V1[8:] + n1 * Wf[8:] + n2 * mu[k] + w * V0[8:], {0.0, round(1 / 9, 9)})
        return cache[key] & targets
    bad = 0
    for i, req in enumerate(need):
        for k in np.nonzero(adm[i])[0]:
            if any(attain(k, n1, n2, w, t) for (n1, n2, w), t in req.items()):
                bad += 1
                pairs.append((base, int(lam_idx[i]), int(k)))
    out[base] = dict(lambdas=len(lam_idx), admissible_pairs=int(adm.sum()), pairs_with_twisted_10_vector=bad)
    print(base, out[base], flush=True)
json.dump(out, open('exhaust10_full.json', 'w'), indent=1)
json.dump(pairs, open('candidate_pairs.json', 'w'))
