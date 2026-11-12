"""Pass 12649: does W(9,2) (five qubits) have a maximal partial spread of size 6?  Rank-code form (w33_symmetric_rank_code_spreads.py):
sets {I, S2, S3, S4} of nonsingular symmetric 5x5 matrices over F2, pairwise sums nonsingular, whose 'singular-sum' neighbourhoods cover
all 13,888 nonsingular symmetric T.  S2 is reduced modulo the orthogonal group O = {A : A A^T = I} (stabiliser of I under congruence,
enumerated by backtracking over orthonormal rows); for each S2 representative, loop S3 and filter S4 against the uncovered set.
Counts ordered (S2,S3,S4) completions weighted by orbit size -> sets containing I -> sets through the fixed pair (n odd: one class).
Control: n = 4 is not covered by this odd-n code; the n = 3 run (size 6 must be 0: sizes are 5 and 9) and a size-5 recount for n = 3
(56 through the pair) validate the machinery.
usage: py -3 analysis/w33_five_qubit_size6.py"""
import json, os, itertools, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_symmetric_rank_code_spreads.py")}
src = open(os.path.join(HERE, "w33_symmetric_rank_code_spreads.py"), encoding="utf-8").read()
exec(src[: src.index("def run(")], g)
setup, code_of = g["setup"], g["code_of"]
def orthogonal_group(n):
    odd = [v for v in range(1, 1 << n) if bin(v).count("1") % 2 == 1]
    out = []
    def rec(rows):
        if len(rows) == n: out.append(rows[:]); return
        for v in odd:
            if all(bin(v & r).count("1") % 2 == 0 for r in rows) and v not in rows:
                rows.append(v); rec(rows); rows.pop()
    rec([]); return out  # rows as bitmasks (row i = A[i,:]); orthonormal & independent automatically
def congr(n, pos, A_rows, code):
    S = [[0] * n for _ in range(n)]
    for b, (i, j) in enumerate(pos):
        if code >> b & 1: S[i][j] = S[j][i] = 1
    A = [[(A_rows[i] >> j) & 1 for j in range(n)] for i in range(n)]
    M = [[sum(A[i][k] * S[k][l] * A[j][l] for k in range(n) for l in range(n)) % 2 for j in range(n)] for i in range(n)]
    return code_of(n, pos, M)
def run(n, k_target):
    t0 = time.time(); pos, sing, alt, ns = setup(n); N = len(ns)
    I = code_of(n, pos, [[int(i == j) for j in range(n)] for i in range(n)])
    O = orthogonal_group(n)
    nb = lambda c: sing[ns ^ c]
    base = nb(I); cand = ns[~sing[ns ^ I]]; cset = set(cand.tolist())
    # orbits of S2 under O
    seen = set(); reps = []
    for s in cand.tolist():
        if s in seen: continue
        orb = {congr(n, pos, A, s) for A in O}; seen |= orb; reps.append((s, len(orb)))
    print("n", n, "|O| =", len(O), "| N =", N, "| cand =", len(cand), "| S2 orbits =", len(reps), flush=True)
    ordered = 0; example = None
    for s2, osz in reps:
        cov2 = base | nb(s2)
        c3 = cand[~sing[cand ^ s2]]
        for s3 in c3:
            cov3 = cov2 | nb(s3)
            if k_target == 3:
                if cov3.all(): ordered += osz; example = example or [I, s2, int(s3)]
                continue
            R = ns[~cov3]
            c4 = c3[~sing[c3 ^ s3]]
            for T in R:
                if len(c4) == 0: break
                c4 = c4[sing[c4 ^ T]]
            c4 = c4[c4 != s3]
            ordered += osz * len(c4)
            if len(c4) and example is None: example = [I, s2, int(s3), int(c4[0])]
    kk = k_target - 1  # number of matrices other than I
    sets_with_I = ordered / np.prod(range(1, kk + 1))
    through = N * sets_with_I / k_target
    r = dict(n=n, size=k_target + 2, ordered_completions=ordered, sets_containing_I=sets_with_I, sets_through_pair=through, exists=through > 0, example=example, seconds=round(time.time() - t0, 1))
    print(r, flush=True); return r
res = dict(control_n3_size5=run(3, 3), control_n3_size6=run(3, 4), n5_size6=run(5, 4))
json.dump(res, open(os.path.join(ROOT, "data", "w33_five_qubit_size6.json"), "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
