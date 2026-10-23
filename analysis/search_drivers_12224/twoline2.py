"""12224b: two A4-type Wilson lines sampled correctly: enumerate every admissible single line W = (lambda, mu) per base (as in 12217),
group lambda by the A4 they leave, and draw pairs (W1, W2) inside one group with 3 W1.W2 integral (and W1 != W2).  Lattice test for a
twisted 10-type massless vector over all 27 x 3 fixed-point labels and Witten partners; density with a 95% Wilson interval.
usage: py -3 twoline2.py N SEED"""
import itertools, json, math, random, sys
import numpy as np
from collections import defaultdict
exec(open('twoline.py').read().split("ok3 = lambda")[0].replace("N, SEED = int(sys.argv[1]), int(sys.argv[2])", "N, SEED = int(sys.argv[1]), int(sys.argv[2])"))
ok3 = lambda x: abs(3 * x - round(3 * x)) < 1e-9
oki = lambda x: abs(x - round(x)) < 1e-9
groups = {}
for base in BASES:
    V0, V1, Wf, d5, pool = info[base]
    lam = L3[pool]; mu = L3
    W2n = (lam * lam).sum(1)[:, None] + (mu * mu).sum(1)[None, :]
    adm = (np.abs(3 * W2n / 2 - np.round(3 * W2n / 2)) < 1e-9) & integ(3 * ((lam @ V1[:8])[:, None] + (mu @ V1[8:])[None, :])) \
        & integ((lam @ V0[:8])[:, None] + (mu @ V0[8:])[None, :]) & integ(3 * ((lam @ Wf[:8])[:, None] + (mu @ Wf[8:])[None, :]))
    byA4 = defaultdict(list)
    for i, jj in enumerate(pool):
        key = tuple(np.array(d5)[integ(R[d5] @ L3[jj])])
        for kk in np.nonzero(adm[i])[0]:
            byA4[key].append((jj, int(kk)))
    groups[base] = [v for v in byA4.values() if len(v) > 1]
    print(base, 'A4 classes', len(byA4), 'admissible lines', sum(len(v) for v in byA4.values()), flush=True)
draws = hits = tries = 0
hitcfg = []
while draws < N and tries < 200 * N:
    tries += 1
    base = rnd.choice(BASES); V0, V1, Wf, d5, pool = info[base]
    grp = rnd.choice(groups[base])
    (j1, k1), (j2, k2) = rnd.sample(grp, 2)
    W1 = np.concatenate([L3[j1], L3[k1]]); W2 = np.concatenate([L3[j2], L3[k2]])
    if not ok3(W1 @ W2):
        continue
    mk = np.zeros(240, bool); mk[np.array(d5)[integ(R[d5] @ L3[j1]) & integ(R[d5] @ L3[j2])]] = True
    if g.typ(mk) != ('A4',):
        continue
    B = np.linalg.svd(R[np.nonzero(mk)[0]])[2][:4]
    draws += 1
    found = False
    for n1, n2, n3, w in itertools.product(range(3), range(3), range(3), (0, 1)):
        u = V1 + n1 * Wf + n2 * W1 + n3 * W2 + w * V0
        Q1 = E8S + reduce(u[:8]); n1s = (Q1 * Q1).sum(1); pr = Q1 @ B.T
        ten = (np.abs((pr * pr).sum(1) - 6 / 5) < 1e-9) & (n1s <= 4 / 3 + 1e-9)
        if not ten.any():
            continue
        Q2 = E8S + reduce(u[8:]); n2s = (Q2 * Q2).sum(1)
        if any(np.any(np.abs(n2s - (4 / 3 - a)) < 1e-9) for a in set(np.round(n1s[ten], 9))):
            found = True
            break
    hits += found
    if found:
        hitcfg.append((base, int(j1), int(k1), int(j2), int(k2)))
p = hits / draws
z = 1.96; den = 1 + z * z / draws; ctr = (p + z * z / (2 * draws)) / den
half = z * math.sqrt(p * (1 - p) / draws + z * z / (4 * draws * draws)) / den
out = dict(draws=draws, tries=tries, hits=hits, density=p, wilson95=[max(0.0, ctr - half), ctr + half], one_line_density=405 / 231124)
print(out)
json.dump(out, open(f'twoline2_{SEED}.json', 'w'), indent=1)
json.dump(hitcfg, open(f'twoline2_hits_{SEED}.json', 'w'))
