"""12247: completion of 12243 -- W2 now ranges over EVERY consistent admissible line whose first half preserves the A4 of W1 (A4-type or not, e.g. lines trivial on so(10)); W1 is A4-type.  Commuting order-3 lines diagonalise on the D5 Cartan, so an A4 intersection forces one line to be A4-type and the other to preserve that A4: this covers every Wilson-line configuration with an SU(5) (torus 1 carries the base family line).  Original header:
12243: EXHAUSTIVE two-line test for twisted 10s and scalar 10s.  Lines: all admissible one-line W = (lambda, mu) of 12217 with
V0.W even (consistency, 12235), grouped by the A4 they leave; pairs (W1 on torus 2, W2 on torus 3) inside one A4 class with 3 W1.W2
integral.  For fixed-point label (n1, n2, n3, w) the cosets are u1 = V1 + n1 Wf + w V0 + n2 lambda1 + n3 lambda2 (first E8) and
u2 likewise with mu (second E8); n2 lambda1 + n3 lambda2 is fixed mod E8 by its class in E8/3E8, so per base and label (n1, w) the
6561 coset classes are tabulated once: first-E8 vectors with |P1|^2 <= 4/3, second-E8 vectors with |P2|^2 <= 2/15.  A twisted 10-type
massless state needs |proj_A4 P1|^2 = 6/5 and |P1|^2 + |P2|^2 = 4/3; it is a scalar iff (P1.V0_1 + P2.V0_2) = w/2 mod 1 (12230/12235).
usage: py -3 exhaust2.py BASE"""
import itertools, json, sys, time
import numpy as np
from fractions import Fraction as Fr
src = open('../search_drivers_12217/exhaust10.py').read().split("D = r'C:")[0]
exec(src)
D = r'C:\tmp\toe_wt\analysis\search_drivers_12111'
base = sys.argv[1]
t0 = time.time()
rows = open(D + '/' + base + '_9.txt').read().split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n')
v = [np.array([float(Fr(x)) for x in r.split()[:16]]) for r in rows]
V0, V1, Wf = v[0], v[1], v[3]
d5 = next(c for c in g.comps(integ(R @ V0[:8]) & integ(R @ V1[:8]) & integ(R @ Wf[:8])) if len(c) == 40)
P = integ(R[d5] @ L3.T)
pool = [jj for jj in range(len(coefs)) if g.typ(np.isin(np.arange(240), np.array(d5)[P[:, jj]])) == ('A4',)]
lamall = L3; lam, mu = L3[pool], L3
W2n = (lam * lam).sum(1)[:, None] + (mu * mu).sum(1)[None, :]
c0 = (lam @ V0[:8])[:, None] + (mu @ V0[8:])[None, :]
adm = (np.abs(3 * W2n / 2 - np.round(3 * W2n / 2)) < 1e-9) & integ(3 * ((lam @ V1[:8])[:, None] + (mu @ V1[8:])[None, :])) \
    & integ(c0) & integ(3 * ((lam @ Wf[:8])[:, None] + (mu @ Wf[8:])[None, :])) & (np.abs(np.round(c0) % 2) < 1e-9)
W2a = (lamall * lamall).sum(1)[:, None] + (mu * mu).sum(1)[None, :]
c0a = (lamall @ V0[:8])[:, None] + (mu @ V0[8:])[None, :]
adma = (np.abs(3 * W2a / 2 - np.round(3 * W2a / 2)) < 1e-9) & integ(3 * ((lamall @ V1[:8])[:, None] + (mu @ V1[8:])[None, :]))     & integ(c0a) & integ(3 * ((lamall @ Wf[:8])[:, None] + (mu @ Wf[8:])[None, :])) & (np.abs(np.round(c0a) % 2) < 1e-9)
classes = {}
for i, jj in enumerate(pool):
    key = tuple(np.array(d5)[integ(R[d5] @ L3[jj])])
    for kk in np.nonzero(adm[i])[0]:
        classes.setdefault(key, []).append((jj, int(kk)))
pow3 = 3 ** np.arange(7, -1, -1)
C = np.array(coefs)
labels = [(n1, w) for n1 in range(3) for w in (0, 1)]
# coset tables
T1, T2 = {}, {}
for n1, w in labels:
    b = V1 + n1 * Wf + w * V0
    t1, t2 = [], []
    for c in range(6561):
        Q1 = E8S + reduce(b[:8] + L3[c]); n1s = (Q1 * Q1).sum(1); k1 = n1s <= 4 / 3 + 1e-9
        t1.append((Q1[k1], n1s[k1]))
        Q2 = E8S + reduce(b[8:] + L3[c]); n2s = (Q2 * Q2).sum(1); k2 = n2s <= 2 / 15 + 1e-9
        t2.append([(round(float(n), 9), round(float(q @ V0[8:]) % 1, 9)) for q, n in zip(Q2[k2], n2s[k2])])
    T1[(n1, w)], T2[(n1, w)] = t1, t2
print(base, 'tables', round(time.time() - t0), 's; A4 classes', len(classes), 'lines', sum(len(x) for x in classes.values()), flush=True)
tot_pairs = hit_pairs = scalar_pairs = 0
hitset = set()
for key, lines in classes.items():
    a4 = np.array(key); B = np.linalg.svd(R[a4])[2][:4]
    # per label and first-E8 class: set of (|P1|^2, P1.V0_1 mod 1) for 10-type vectors
    S1 = {}
    for lab in labels:
        arr = []
        for Q1, n1s in T1[lab]:
            if len(Q1) == 0:
                arr.append(()); continue
            pr = Q1 @ B.T; m = np.abs((pr * pr).sum(1) - 6 / 5) < 1e-9
            arr.append(tuple(sorted({(round(float(n), 9), round(float(q @ V0[:8]) % 1, 9)) for q, n in zip(Q1[m], n1s[m])})))
        S1[lab] = arr
    a4set = list(key)
    ext_l = np.nonzero(np.all(integ(R[a4set] @ L3.T), axis=0))[0]
    ext = [(int(jj), int(kk)) for jj in ext_l for kk in np.nonzero(adma[jj])[0]]
    J = np.array([C[j] for j, k in lines]); K = np.array([C[k] for j, k in lines])
    J2 = np.array([C[j] for j, k in ext]); K2 = np.array([C[k] for j, k in ext])
    Wv = np.array([np.concatenate([L3[j], L3[k]]) for j, k in lines])
    Wv2 = np.array([np.concatenate([L3[j], L3[k]]) for j, k in ext])
    mutual = integ(3 * (Wv @ Wv2.T))
    extindex = {e: q for q, e in enumerate(ext)}
    cache = {}
    def test(lab, c1, c2, w):
        key2 = (lab, c1, c2)
        if key2 in cache:
            return cache[key2]
        hit = scal = False
        for a, f1 in S1[lab][c1]:
            for bb, f2 in T2[lab][c2]:
                if abs(a + bb - 4 / 3) < 1e-7:
                    hit = True
                    ph = (f1 + f2 - w / 2) % 1
                    if min(ph, 1 - ph) < 1e-7:
                        scal = True
        cache[key2] = (hit, scal)
        return hit, scal
    for i1 in range(len(lines)):
        idx2 = np.nonzero(mutual[i1])[0]
        idx2 = idx2[np.array([ext[q] != lines[i1] for q in idx2], bool)] if len(idx2) else idx2
        if len(idx2) == 0:
            continue
        tot_pairs += len(idx2)
        hitv = np.zeros(len(idx2), bool); scv = np.zeros(len(idx2), bool)
        for n2, n3 in itertools.product(range(3), repeat=2):
            c1 = ((n2 * J[i1] + n3 * J2[idx2]) % 3) @ pow3
            c2 = ((n2 * K[i1] + n3 * K2[idx2]) % 3) @ pow3
            for lab in labels:
                nz = [q for q in range(len(idx2)) if S1[lab][c1[q]] and T2[lab][c2[q]]]
                for q in nz:
                    h, s = test(lab, int(c1[q]), int(c2[q]), lab[1])
                    hitv[q] |= h; scv[q] |= s
        hit_pairs += int(hitv.sum()); scalar_pairs += int(scv.sum())
        for q in np.nonzero(hitv)[0]:
            hitset.add((lines[i1], ext[int(idx2[q])]))
sampled = [tuple(x) for x in json.load(open('../search_drivers_12224/twoline4_hits_31.json')) if x[0] == base]
found = sum(1 for x in sampled if ((x[1], x[2]), (x[3], x[4])) in hitset)
out = dict(extended=True, control_sampled_hits=len(sampled), control_found=found, base=base, A4_classes=len(classes), lines=sum(len(x) for x in classes.values()), pairs=tot_pairs, twisted10_pairs=hit_pairs,
           scalar10_pairs=scalar_pairs, seconds=round(time.time() - t0))
print(out, flush=True)
json.dump(out, open(f'exhaust3_{base}.json', 'w'), indent=1)
