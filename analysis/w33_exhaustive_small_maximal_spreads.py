"""Pass 12648 item 1: exhaustive decision of the smallest maximal partial spreads of W(2n-1, 2) for n = 2, 3, 4 at sizes 3, 4 (and 5).
Witt: Sp(2n,2) is transitive on ordered pairs of complementary Lagrangians, so every maximal partial spread of size k >= 2 is equivalent to
one containing a FIXED pair (L0, L1).  Enumerate the remaining k - 2 Lagrangians among those disjoint from L0 and L1 (pairwise disjoint)
and test maximality (every Lagrangian meets the union) with a boolean meet matrix.  Complete for the given k.
Controls: n = 2: size 3 must exist (two-qubit 3-sets); n = 3: sizes 3, 4 must not exist and size 5 must (24,192 sets, Pass 12636).
usage: py -3 analysis/w33_exhaustive_small_maximal_spreads.py"""
import json, os, itertools, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
pc = lambda x: bin(x).count("1")
def lagrangians(n):
    NV = 1 << (2 * n); lo = (1 << n) - 1
    w = lambda x, y: (pc((x & lo) & (y >> n)) + pc((x >> n) & (y & lo))) % 2
    L0 = frozenset(range(1, 1 << n)); seen = {L0}; stack = [L0]
    while stack:
        L = stack.pop()
        for u in range(1, NV):
            M = frozenset(x ^ (u if w(x, u) else 0) for x in L)
            if M not in seen: seen.add(M); stack.append(M)
    return sorted(seen, key=lambda s: sorted(s)), NV
def decide(n, ks):
    lags, NV = lagrangians(n); nL = len(lags)
    Inc = np.zeros((nL, NV), bool)
    for i, L in enumerate(lags): Inc[i, list(L)] = True
    meet = (Inc.astype(np.int32) @ Inc.T.astype(np.int32)) > 0
    i0 = 0; i1 = int(np.flatnonzero(~meet[i0])[0])
    cand = np.flatnonzero(~meet[i0] & ~meet[i1])
    base = meet[i0] | meet[i1]
    out = dict(n=n, n_lagrangians=nL, candidates_disjoint_from_pair=int(len(cand)))
    for k in ks:
        t = time.time(); count = 0; example = None
        if k == 3:
            for c in cand:
                if (base | meet[c]).all():
                    count += 1; example = example or [i0, i1, int(c)]
        elif k == 4:
            for a_idx, a in enumerate(cand):
                rest = cand[a_idx + 1:]; rest = rest[~meet[a, rest]]
                if len(rest) == 0: continue
                cov = (base | meet[a])[None, :] | meet[rest]
                ok = cov.all(1); count += int(ok.sum())
                if ok.any() and example is None: example = [i0, i1, int(a), int(rest[np.flatnonzero(ok)[0]])]
        elif k == 5:
            for a_idx, a in enumerate(cand):
                r1 = cand[a_idx + 1:]; r1 = r1[~meet[a, r1]]
                for b_idx, b in enumerate(r1):
                    r2 = r1[b_idx + 1:]; r2 = r2[~meet[b, r2]]
                    if len(r2) == 0: continue
                    cov = (base | meet[a] | meet[b])[None, :] | meet[r2]
                    ok = cov.all(1); count += int(ok.sum())
                    if ok.any() and example is None: example = [i0, i1, int(a), int(b), int(r2[np.flatnonzero(ok)[0]])]
        out["k%d" % k] = dict(count_containing_fixed_pair=count, exists=count > 0, example=example, seconds=round(time.time() - t, 1))
        print(n, k, out["k%d" % k], flush=True)
    return out
res = dict(two_qubits=decide(2, [3]), three_qubits=decide(3, [3, 4, 5]), four_qubits=decide(4, [3, 4]))
json.dump(res, open(os.path.join(ROOT, "data", "w33_exhaustive_small_maximal_spreads.json"), "w"), indent=1)
