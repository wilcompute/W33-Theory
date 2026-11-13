"""Pass 12652 item 2: is there a five-qubit maximal Pauli MUB set of size 8?  CP-SAT in the rank-code form (Pass 12649).
A maximal partial spread {L0, L1, graph(S1..S6)} of W(9,2) <-> nonsingular symmetric 5x5 S_i over F2, pairwise sums nonsingular, with
every nonsingular symmetric T having T + S_i singular for some i.  n odd => S1 = I up to congruence (Witt + GL(5)); S2 runs over the
8 orbits of O(5) = Stab(I) (w33_five_qubit_size6.py).  Remaining: choose k more S from the candidates compatible with I and S2, pairwise
compatible, covering the T's left uncovered by I and S2.  size 8 <-> k = 4.
Controls: size 9 (k = 5) must be FEASIBLE for some S2 orbit (Pass 12650 found one); n = 3 size 5 (k = 1) feasible, size 6 (k = 2) not.
Each solution found is re-verified directly (sums nonsingular, all T covered).
usage: py -3 analysis/w33_five_qubit_size8_cpsat.py [k] [seconds_per_orbit] [n]"""
import json, os, sys, time
import numpy as np
from ortools.sat.python import cp_model
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_five_qubit_size6.py")}
src = open(os.path.join(HERE, "w33_five_qubit_size6.py"), encoding="utf-8").read()
exec(src[: src.index(chr(10) + "def run(")], g)
setup, code_of, orthogonal_group, congr = g["setup"], g["code_of"], g["orthogonal_group"], g["congr"]
k = int(sys.argv[1]) if len(sys.argv) > 1 else 4
tl = float(sys.argv[2]) if len(sys.argv) > 2 else 1800
n = int(sys.argv[3]) if len(sys.argv) > 3 else 5
t0 = time.time(); pos, sing, alt, ns = setup(n)
I = code_of(n, pos, [[int(i == j) for j in range(n)] for i in range(n)])
O = orthogonal_group(n)
cand = ns[~sing[ns ^ I]]
seen = set(); reps = []
for s in cand.tolist():
    if s in seen: continue
    orb = {congr(n, pos, A, s) for A in O}; seen |= orb; reps.append((s, len(orb)))
print(f"n={n} size={k + 4} |O|={len(O)} N={len(ns)} cand={len(cand)} orbits={len(reps)}", flush=True)
def verify(S):
    ok_pairs = all(not sing[a ^ b] for i, a in enumerate(S) for b in S[i + 1:])
    covered = np.zeros(len(ns), bool)
    for s in S: covered |= sing[ns ^ s]
    return bool(ok_pairs and covered.all())
out = dict(n=n, k_more=k, size=k + 4, orbits=[])
for s2, osz in reps:
    c3 = cand[~sing[cand ^ s2]]
    cov = sing[ns ^ I] | sing[ns ^ s2]; R = ns[~cov]
    m = cp_model.CpModel(); x = [m.NewBoolVar(f"x{i}") for i in range(len(c3))]
    m.Add(sum(x) == k)
    C = sing[c3[:, None] ^ c3[None, :]]  # True = incompatible (diagonal True too but i<j only)
    ii, jj = np.nonzero(np.triu(C, 1))
    for a, b in zip(ii.tolist(), jj.tolist()): m.AddBoolOr([x[a].Not(), x[b].Not()])
    D = sing[R[:, None] ^ c3[None, :]]  # T in R covered by S
    for row in D:
        lits = np.flatnonzero(row)
        m.AddBoolOr([x[j] for j in lits.tolist()])
    sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = tl; sv.parameters.num_workers = 8
    tb = time.time(); st = sv.Solve(m)
    rec = dict(s2=int(s2), orbit_size=osz, n_cand=len(c3), n_uncovered=len(R), n_conflicts=len(ii), status=sv.StatusName(st), seconds=round(time.time() - tb, 1))
    if st in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        S = [I, int(s2)] + [int(c3[j]) for j in range(len(c3)) if sv.Value(x[j])]
        rec.update(solution=S, verified=verify(S))
    print(rec, flush=True); out["orbits"].append(rec)
stats = [r["status"] for r in out["orbits"]]
out["summary"] = dict(all_infeasible=all(s == "INFEASIBLE" for s in stats), any_feasible=any(s in ("FEASIBLE", "OPTIMAL") for s in stats), statuses=stats, seconds=round(time.time() - t0, 1))
print(out["summary"], flush=True)
json.dump(out, open(os.path.join(ROOT, "data", f"w33_rank_code_cpsat_n{n}_size{k + 4}.json"), "w"), indent=1)
