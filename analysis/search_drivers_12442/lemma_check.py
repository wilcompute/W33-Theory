"""12442: numerical test of the odd-case lemma on real kernel words.  For q = 3, 5: kernel words of A over F_2 (all weight-2q
intersecting-line sums + random kernel words); for every odd line L, every x0 in L \\ S, every odd line M through x0 (M != L):
bound = q + max(a, c) + #(S-points on the other q - 1 lines through x0).  The lemma says |S| >= bound; count violations (must be 0) and
record how often the bound is tight."""
import sys, json, random, itertools
import numpy as np
sys.path.insert(0, '../search_drivers_12419')
sys.path.insert(0, '../search_drivers_12426')
from two_codes import w3q
from mindist import kernel2

out = {}
rng = np.random.default_rng(12442)
for q in (3, 5):
    A = w3q(q); n = len(A)
    lines = set()
    for i in range(n):
        for j in range(i + 1, n):
            if A[i, j]:
                lines.add(frozenset([i, j] + [k for k in range(n) if A[i, k] and A[j, k]]))
    lines = [sorted(l) for l in lines]
    through = {x: [li for li, l in enumerate(lines) if x in l] for x in range(n)}
    K = kernel2((A % 2).astype(np.uint8))
    words = []
    for x, ls in through.items():
        for a, b in itertools.combinations(ls, 2):
            v = np.zeros(n, dtype=np.int64); v[list(set(lines[a]) ^ set(lines[b]))] = 1; words.append(v)
            if len(words) > 300: break
        if len(words) > 300: break
    for _ in range(300):
        c = rng.integers(0, 2, len(K))
        v = (c @ K) % 2
        if v.any(): words.append(v.astype(np.int64))
    viol = tight = tested = 0
    for v in words:
        assert not ((A @ v) % 2).any()
        S = set(np.nonzero(v)[0].tolist())
        s = [len(S & set(l)) for l in lines]
        for L, l in enumerate(lines):
            if s[L] % 2 == 0: continue
            for x0 in l:
                if x0 in S: continue
                for M in through[x0]:
                    if M == L or s[M] % 2 == 0: continue
                    others = sum(s[o] for o in through[x0] if o not in (L, M))
                    bound = q + max(s[L], s[M]) + others
                    tested += 1
                    viol += len(S) < bound
                    tight += len(S) == bound
    out[q] = dict(words=len(words), configurations_tested=tested, violations=viol, tight=tight)
    print(q, out[q], flush=True)
json.dump(out, open('lemma_check.json', 'w'), indent=1)
