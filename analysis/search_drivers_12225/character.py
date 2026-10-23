"""12225: the split-parity character of the twisted 10-type massless momenta.  For each of the 405 candidate configurations of
12217: full momenta P = (P1, P2) in Gamma + V_f (+ V0 for w = 1) with |P|^2 = 4/3 and |proj_A4 P1|^2 = 6/5; record the sector
label w and the character P.V0 mod 1 (and 2 P.V0 mod 2)."""
import itertools, json, sys
import numpy as np
from collections import Counter
from fractions import Fraction as Fr
sys.path.insert(0, '../search_drivers_12217')
src = open('../search_drivers_12217/exhaust10.py').read().split("D = r'C:")[0]
exec(src)
D = r'C:\tmp\toe_wt\analysis\search_drivers_12111'
pairs = json.load(open('../search_drivers_12217/candidate_pairs.json'))
cache = {}
stats = Counter(); per_config = []
for base, j, k in pairs:
    if base not in cache:
        rows = open(D + '/' + base + '_9.txt').read().split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n')
        v = [np.array([float(Fr(x)) for x in r.split()[:16]]) for r in rows]
        V0, V1, Wf = v[0], v[1], v[3]
        d5 = next(c for c in g.comps(integ(R @ V0[:8]) & integ(R @ V1[:8]) & integ(R @ Wf[:8])) if len(c) == 40)
        cache[base] = (V0, V1, Wf, d5)
    V0, V1, Wf, d5 = cache[base]
    mk = np.zeros(240, bool); mk[np.array(d5)[integ(R[d5] @ L3[j])]] = True
    B = np.linalg.svd(R[np.nonzero(mk)[0]])[2][:4]
    W = np.concatenate([L3[j], L3[k]])
    labs = Counter()
    for n1, n2, w in itertools.product(range(3), range(3), (0, 1)):
        u = V1 + n1 * Wf + n2 * W + w * V0
        r1, r2 = reduce(u[:8]), reduce(u[8:])
        Q1 = E8S + r1; Q2 = E8S + r2
        n1s = (Q1 * Q1).sum(1); n2s = (Q2 * Q2).sum(1)
        pr = Q1 @ B.T; ten = np.abs((pr * pr).sum(1) - 6 / 5) < 1e-9
        for a in np.nonzero(ten & (n1s <= 4 / 3 + 1e-9))[0]:
            for b in np.nonzero(np.abs(n2s - (4 / 3 - n1s[a])) < 1e-9)[0]:
                P = np.concatenate([Q1[a], Q2[b]])
                ch = Fr(float(P @ V0)).limit_denominator(12) % 1
                stats[(w, str(ch))] += 1
                labs[(w, str(ch))] += 1
    per_config.append(dict(base=base, j=j, k=k, hits={f'{a}|{b}': c for (a, b), c in labs.items()}))
print('(w, P.V0 mod 1) over all 10-type twisted massless momenta of the 405 configurations:', dict(stats))
json.dump(dict(stats={f'{a}|{b}': c for (a, b), c in stats.items()}, per_config=per_config), open('character.json', 'w'), indent=1)
