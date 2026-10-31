"""12502: is there an even line set of W(3,9) with at most 46 lines?  (The minimum is >= 32 by the other track's bound and <= 48 by
12496/12501; even sets have even size.)  CP-SAT feasibility, weight in [2, 46], with the 12474 line-pair symmetry break (line 0 and the
first line meeting it are chosen -- valid because PSp(4,q) is transitive on incident line pairs and some chosen line meets a chosen
line in any even set).  INFEASIBLE proves the minimum is 48; UNKNOWN proves nothing.  usage: py -3 q9_le46.py [seconds]"""
import sys, json, time
from ortools.sat.python import cp_model
from symmetric_fast import fast_build

q = 9; tl = float(sys.argv[1]) if len(sys.argv) > 1 else 10800
pts, lines = fast_build(q); sets = [frozenset(L) for L in lines]
through = [[] for _ in pts]
for j, L in enumerate(lines):
    for p in L: through[p].append(j)
md = cp_model.CpModel(); y = [md.NewBoolVar(f"y{j}") for j in range(len(lines))]
for p in range(len(pts)):
    z = md.NewIntVar(0, (q + 1) // 2, f"z{p}"); md.Add(sum(y[j] for j in through[p]) == 2 * z)
md.Add(sum(y) >= 2); md.Add(sum(y) <= 46)
md.Add(y[0] == 1)
first = next(j for j in range(1, len(lines)) if sets[j] & sets[0]); md.Add(y[first] == 1)
s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tl; s.parameters.num_workers = 8
t0 = time.time(); st = s.Solve(md)
out = dict(q=q, max_weight=46, status=s.StatusName(st), seconds=round(time.time() - t0, 1))
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    out["weight"] = sum(s.Value(v) for v in y); out["chosen"] = [j for j in range(len(lines)) if s.Value(y[j])]
print(json.dumps({k: v for k, v in out.items() if k != "chosen"})); json.dump(out, open("q9_le46.json", "w"))
