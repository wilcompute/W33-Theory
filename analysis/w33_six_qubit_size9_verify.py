"""Pass 12651: independent verification of the six-qubit size-9 maximal partial spread from biased greedy (own GF(2) rank, no lookup
table): all matrices nonsingular, pairwise sums nonsingular, and no nonsingular symmetric 6x6 T (all 2^21 checked) has T + S_i
nonsingular for every i.  usage: py -3 analysis/w33_six_qubit_size9_verify.py"""
import json, os, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
n = 6; pos = [(i, j) for i in range(n) for j in range(i, n)]
ex = json.load(open(os.path.join(ROOT, "data", "w33_six_qubit_greedy.json")))["n6_biased"]["example"]
def rows_of(code):
    rows = [0] * n
    for b, (i, j) in enumerate(pos):
        if code >> b & 1: rows[i] |= 1 << j; rows[j] |= 1 << i
    return rows
def rank(rows):
    rows = rows[:]; r = 0
    for c in range(n):
        p = next((k for k in range(r, n) if rows[k] >> c & 1), None)
        if p is None: continue
        rows[r], rows[p] = rows[p], rows[r]
        for k in range(n):
            if k != r and rows[k] >> c & 1: rows[k] ^= rows[r]
        r += 1
    return r
full = lambda c: rank(rows_of(c)) == n
res = dict(example=ex, size=len(ex) + 2, all_nonsingular=all(full(c) for c in ex), pairwise=all(full(a ^ b) for a, b in itertools.combinations(ex, 2)))
ext = 0; checked = 0
for T in range(1 << len(pos)):
    if not full(T): continue
    checked += 1
    if all(full(T ^ s) for s in ex): ext += 1
res.update(nonsingular_T_checked=checked, extendible_T=ext, maximal=ext == 0)
print(res); json.dump(res, open(os.path.join(ROOT, "data", "w33_six_qubit_size9_verify.json"), "w"), indent=1)
