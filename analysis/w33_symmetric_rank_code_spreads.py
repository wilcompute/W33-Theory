"""Pass 12649 item 5: smallest maximal partial spreads of W(2n-1,2) as symmetric-matrix rank codes, up to n = 5 qubits.
Fix L0 = X-type and L1 = Z-type Lagrangians (Witt: WLOG for any spread of size >= 2).  A Lagrangian disjoint from L1 is a graph
{(x, Sx)} with S symmetric; disjoint from L0 too iff S is nonsingular.  graph(S) and graph(T) are disjoint iff S + T is nonsingular.
So a maximal partial spread {L0, L1, graph(S_1..S_k)} <=> nonsingular symmetric S_i with pairwise nonsingular differences such that every
nonsingular symmetric T has T + S_i singular for some i (maximality only needs Lagrangians disjoint from L0 and L1).
All sums are symmetric: one singularity lookup table over all 2^{n(n+1)/2} symmetric matrices.  S_1 runs over congruence-class
representatives of nonsingular symmetric forms (n odd: one class, I; n even: I and the alternating form), and
#sets through (L0,L1) = sum_classes |class| * c_class / k.
Controls: n = 3 -> sizes 3, 4 none, size 5: 56 through the pair; n = 4 -> 3, 4 none, size 5: 896 through the pair (Pass 12648).
usage: py -3 analysis/w33_symmetric_rank_code_spreads.py"""
import json, os, itertools, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
def setup(n):
    pos = [(i, j) for i in range(n) for j in range(i, n)]  # bit index of upper-triangular entries
    nb_ = len(pos)
    def to_rows(code):
        rows = [0] * n
        for b, (i, j) in enumerate(pos):
            if code >> b & 1:
                rows[i] |= 1 << j; rows[j] |= 1 << i
        return rows
    def rank(rows):
        rows = rows[:]; r = 0
        for col in range(n):
            piv = next((k for k in range(r, n) if rows[k] >> col & 1), None)
            if piv is None: continue
            rows[r], rows[piv] = rows[piv], rows[r]
            for k in range(n):
                if k != r and rows[k] >> col & 1: rows[k] ^= rows[r]
            r += 1
        return r
    allc = np.arange(1 << nb_)
    sing = np.array([rank(to_rows(c)) < n for c in allc])
    alt = np.array([all(not (c >> b & 1) for b, (i, j) in enumerate(pos) if i == j) for c in allc])
    ns = np.flatnonzero(~sing)  # nonsingular symmetric codes
    return pos, sing, alt, ns
def code_of(n, pos, M):
    return sum(1 << b for b, (i, j) in enumerate(pos) if M[i][j])
def run(n, ks):
    t0 = time.time(); pos, sing, alt, ns = setup(n); N = len(ns)
    reps = [code_of(n, pos, [[int(i == j) for j in range(n)] for i in range(n)])]
    if n % 2 == 0:
        A = [[0] * n for _ in range(n)]
        for i in range(0, n, 2): A[i][i + 1] = A[i + 1][i] = 1
        reps.append(code_of(n, pos, A))
    class_size = {reps[0]: int((~alt[ns]).sum())}
    if n % 2 == 0: class_size[reps[1]] = int(alt[ns].sum())
    nbhd = lambda c: sing[ns ^ c]  # bool over ns: T + S singular
    out = dict(n=n, n_nonsingular_symmetric=N, classes={str(r): class_size[r] for r in reps})
    for k in ks:
        through_pair = 0.0; per_class = {}
        for r in reps:
            base = nbhd(r); cand = ns[~sing[ns ^ r]]  # S with S + r nonsingular (excludes r itself)
            c = 0
            if k == 1:
                c = int(base.all())
            elif k == 2:
                for s in cand:
                    c += int((base | nbhd(s)).all())
                c //= 1
            elif k == 3:
                NB = sing[ns[None, :] ^ cand[:, None]]  # |cand| x N
                for a in range(len(cand)):
                    rest = np.arange(a + 1, len(cand))
                    rest = rest[~sing[cand[rest] ^ cand[a]]]
                    if len(rest) == 0: continue
                    cov = (base | NB[a])[None, :] | NB[rest]
                    c += int(cov.all(1).sum())
            per_class[str(r)] = c
            # sets containing r with r as one of k elements: c counts sets containing r (unordered among the other k-1)
            through_pair += class_size[r] * c / k
        out["k%d_size%d" % (k, k + 2)] = dict(sets_containing_rep=per_class, sets_through_pair=through_pair, exists=through_pair > 0)
        print(n, "size", k + 2, out["k%d_size%d" % (k, k + 2)], "(%.0fs)" % (time.time() - t0), flush=True)
    return out
res = {}
res["n3"] = run(3, [1, 2, 3])
res["n4"] = run(4, [1, 2, 3])
res["n5"] = run(5, [1, 2, 3])
json.dump(res, open(os.path.join(ROOT, "data", "w33_symmetric_rank_code_spreads.json"), "w"), indent=1)
