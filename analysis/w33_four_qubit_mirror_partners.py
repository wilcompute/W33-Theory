"""Pass 12645 item 4: mirror partners at four qubits.  All partitions of the covered set C (135 points) of the saved size-9 set into 9
Lagrangians (exact cover by the Lagrangians contained in C; enumerated completely by recursion).  Each partition is automatically a maximal
partial spread with the same covered set, hence the same second moments.  For every partner: lines shared with the original and the meeting
pattern of a left line with the right set.  (Result for the saved set: the partition is UNIQUE -- no mirror partner.)
usage: py -3 analysis/w33_four_qubit_mirror_partners.py"""
import json, os, itertools
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
ex = {"__name__": "x", "__file__": os.path.join(HERE, "w33_four_qubit_theta_exact.py")}
src = open(os.path.join(HERE, "w33_four_qubit_theta_exact.py"), encoding="utf-8").read()
exec(src[: src.index("rows, cols = []")], ex)
lags, w = ex["lags"], ex["w"]; n = 4; d = 16
sol = sorted(json.load(open(os.path.join(ROOT, "data", "w33_four_qubit_theta_exact.json")))["lines"])
C = frozenset().union(*[lags[i] for i in sol])
inside = [i for i, L in enumerate(lags) if L <= C]
print("Lagrangians inside C:", len(inside), flush=True)
parts = []
def rec(rem, chosen, cand):
    if not rem:
        parts.append(sorted(chosen)); return
    p = min(rem)
    for i in cand:
        if p in lags[i] and lags[i] <= rem:
            rec(rem - lags[i], chosen + [i], [j for j in cand if not (lags[j] & lags[i])])
rec(C, [], inside)
print("partitions of C into 9 Lagrangians:", len(parts), flush=True)
out = dict(n_inside=len(inside), n_partitions=len(parts), partners=[])
for P in parts:
    if P == sol: continue
    shared = len(set(P) & set(sol))
    meet = Counter(tuple(sorted(len(lags[a] & lags[b]) for b in P)) for a in sol if a not in P)
    out["partners"].append(dict(lines=P, shared_lines=shared, meeting_patterns={str(k): v for k, v in meet.items()}))
    print(out["partners"][-1], flush=True)
json.dump(out, open(os.path.join(ROOT, "data", "w33_four_qubit_mirror_partners.json"), "w"), indent=1)
