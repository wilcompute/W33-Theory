"""12224: twisted-10 density with TWO A4-type second Wilson lines (W1 on torus 2, W2 on torus 3; each W = (lambda from the base's 864
pool, mu random), admissibility of 12161 for each and 3 W1.W2 integral; SU(5) = the A4 left by both).  The space (~10^13) is not
exhaustible: estimate the density of configurations with a twisted 10-type massless vector (|P|^2 = 4/3, A4 projection 6/5, all 27
fixed points x Witten partners), with a 95% Wilson interval.  usage: py -3 twoline.py N SEED"""
import itertools, json, math, random, sys
import numpy as np
from fractions import Fraction as Fr
src = open('../search_drivers_12217/exhaust10.py').read().split("D = r'C:")[0]
exec(src)
D = r'C:\tmp\toe_wt\analysis\search_drivers_12111'
BASES = ['N001_F1_04', 'N004_F1_03', 'N004_F1_04', 'N004_F1_05', 'N008_F1_02', 'N008_F1_03', 'N008_F1_04']
N, SEED = int(sys.argv[1]), int(sys.argv[2])
rnd = random.Random(SEED)
info = {}
for base in BASES:
    rows = open(D + '/' + base + '_9.txt').read().split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n')
    v = [np.array([float(Fr(x)) for x in r.split()[:16]]) for r in rows]
    V0, V1, Wf = v[0], v[1], v[3]
    d5 = next(c for c in g.comps(integ(R @ V0[:8]) & integ(R @ V1[:8]) & integ(R @ Wf[:8])) if len(c) == 40)
    P = integ(R[d5] @ L3.T)
    pool = [jj for jj in range(len(coefs)) if g.typ(np.isin(np.arange(240), np.array(d5)[P[:, jj]])) == ('A4',)]
    info[base] = (V0, V1, Wf, d5, pool)
ok3 = lambda x: abs(3 * x - round(3 * x)) < 1e-9
oki = lambda x: abs(x - round(x)) < 1e-9


def admissible(W, V0, V1, Wf):
    return abs(3 * (W @ W) / 2 - round(3 * (W @ W) / 2)) < 1e-9 and ok3(V1 @ W) and oki(V0 @ W) and ok3(Wf @ W)


draws = hits = tries = 0
while draws < N and tries < 50 * N:
    tries += 1
    base = rnd.choice(BASES); V0, V1, Wf, d5, pool = info[base]
    j1, j2 = rnd.choice(pool), rnd.choice(pool)
    W1 = np.concatenate([L3[j1], L3[rnd.randrange(len(coefs))]])
    W2 = np.concatenate([L3[j2], L3[rnd.randrange(len(coefs))]])
    if not (admissible(W1, V0, V1, Wf) and admissible(W2, V0, V1, Wf) and ok3(W1 @ W2)):
        continue
    mk = np.zeros(240, bool)
    sel = np.array(d5)[integ(R[d5] @ L3[j1]) & integ(R[d5] @ L3[j2])]
    mk[sel] = True
    if g.typ(mk) != ('A4',):
        continue
    B = np.linalg.svd(R[np.nonzero(mk)[0]])[2][:4]
    draws += 1
    found = False
    for n1, n2, n3, w in itertools.product(range(3), range(3), range(3), (0, 1)):
        u = V1 + n1 * Wf + n2 * W1 + n3 * W2 + w * V0
        Q1 = E8S + reduce(u[:8]); n1s = (Q1 * Q1).sum(1)
        pr = Q1 @ B.T
        ten = (np.abs((pr * pr).sum(1) - 6 / 5) < 1e-9) & (n1s <= 4 / 3 + 1e-9)
        if not ten.any():
            continue
        Q2 = E8S + reduce(u[8:]); n2s = (Q2 * Q2).sum(1)
        if any(np.any(np.abs(n2s - (4 / 3 - a)) < 1e-9) for a in set(np.round(n1s[ten], 9))):
            found = True
            break
    hits += found
p = hits / draws if draws else 0
z = 1.96
den = 1 + z * z / draws
ctr = (p + z * z / (2 * draws)) / den
half = z * math.sqrt(p * (1 - p) / draws + z * z / (4 * draws * draws)) / den
out = dict(draws=draws, tries=tries, hits=hits, density=p, wilson95=[max(0, ctr - half), ctr + half], one_line_density=405 / 231124)
print(out)
json.dump(out, open(f'twoline_{SEED}.json', 'w'), indent=1)
