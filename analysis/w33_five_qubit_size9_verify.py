"""Pass 12650: independent verification of the five-qubit size-9 maximal partial spread found by local search.  Separate code (own GF(2)
rank, no lookup table): decode the 7 symmetric matrices, check each is nonsingular and pairwise sums nonsingular, check that graph(S) =
{(x, Sx)} is totally isotropic for the standard symplectic form (so a Lagrangian), and check maximality over ALL 2^15 symmetric T: every
nonsingular T has T + S_i singular for some i (a Lagrangian disjoint from the X- and Z-type Lagrangians is exactly such a graph).
usage: py -3 analysis/w33_five_qubit_size9_verify.py"""
import json, os, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
n = 5; pos = [(i, j) for i in range(n) for j in range(i, n)]
def decode(code):
    S = [[0] * n for _ in range(n)]
    for b, (i, j) in enumerate(pos):
        if code >> b & 1: S[i][j] = S[j][i] = 1
    return S
def rank2(M):
    rows = [sum(M[i][j] << j for j in range(n)) for i in range(n)]; r = 0
    for c in range(n):
        p = next((k for k in range(r, n) if rows[k] >> c & 1), None)
        if p is None: continue
        rows[r], rows[p] = rows[p], rows[r]
        for k in range(n):
            if k != r and rows[k] >> c & 1: rows[k] ^= rows[r]
        r += 1
    return r
add = lambda A, B: [[(A[i][j] + B[i][j]) % 2 for j in range(n)] for i in range(n)]
ex = json.load(open(os.path.join(ROOT, "data", "w33_five_qubit_local_search.json")))["n5_size9"]["example"] if os.path.exists(os.path.join(ROOT, "data", "w33_five_qubit_local_search.json")) else [980, 30085, 20322, 22520, 4690, 21838, 7411]
Ss = [decode(c) for c in ex]
nonsing = all(rank2(S) == n for S in Ss)
pairwise = all(rank2(add(A, B)) == n for A, B in itertools.combinations(Ss, 2))
def isotropic(S):
    vecs = [([(x >> i) & 1 for i in range(n)]) for x in range(1 << n)]
    for a in vecs:
        for b in vecs:
            Sa = [sum(S[i][j] * a[j] for j in range(n)) % 2 for i in range(n)]; Sb = [sum(S[i][j] * b[j] for j in range(n)) % 2 for i in range(n)]
            if (sum(a[i] * Sb[i] for i in range(n)) + sum(Sa[i] * b[i] for i in range(n))) % 2: return False
    return True
iso = all(isotropic(S) for S in Ss)
uncovered = 0; checked = 0
for code in range(1 << len(pos)):
    T = decode(code)
    if rank2(T) < n: continue
    checked += 1
    if all(rank2(add(T, S)) == n for S in Ss): uncovered += 1
res = dict(example=ex, all_nonsingular=nonsing, pairwise_disjoint=pairwise, graphs_isotropic=iso, nonsingular_T_checked=checked, extendible_T=uncovered,
           maximal=uncovered == 0, size=len(Ss) + 2)
print(res); json.dump(res, open(os.path.join(ROOT, "data", "w33_five_qubit_size9_verify.json"), "w"), indent=1)
