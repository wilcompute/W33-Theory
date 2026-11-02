"""12522: every hyperoval (coverage-{0,2} even set) of 40 lines in W(3,7): enumerate ALL solutions in each star class (CP-SAT, ONE
worker -- multi-worker enumeration under-counts) and apply cube_recognise.recognise to each.  Star classes are exhaustive up to the
symmetry group, so "all recognised" proves: every 40-line hyperoval of W(3,7) is a cube-family set.  usage: py -3 classify_q7.py [secs]"""
import json, sys, time, collections
from ortools.sat.python import cp_model
from star_cubes import build, orbits
from cube_recognise import recognise

q, W = 7, 40; tl = float(sys.argv[1]) if len(sys.argv) > 1 else 3600
B = build(q); digits, reps, counts = orbits(B)
lines, through, X = B["lines"], B["through"], B["X"]; sets = [frozenset(L) for L in lines]
out = dict(q=q, W=W, classes=len(reps), per_class=[]); total = collections.Counter(); t0 = time.time()
for r in reps:
    star = digits[r]
    fixed = {X} | {B["choices"][i][int(star[i])] for i in range(q + 1)}
    banned = {j for p in B["Xpts"] for j in through[p]} - fixed
    md = cp_model.CpModel(); y = {}
    for j in range(len(lines)):
        y[j] = 1 if j in fixed else 0 if j in banned else md.NewBoolVar(f"y{j}")
    for p in range(len(B["pts"])):
        z = md.NewBoolVar(f"z{p}"); md.Add(sum(y[j] for j in through[p]) == 2 * z)
    md.Add(sum(y.values()) == W)
    found = []

    class CB(cp_model.CpSolverSolutionCallback):
        def on_solution_callback(self):
            found.append([j for j in range(len(lines)) if (y[j] if isinstance(y[j], int) else self.Value(y[j]))])
    sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = tl; sv.parameters.num_workers = 1; sv.parameters.enumerate_all_solutions = True
    st = sv.Solve(md, CB())
    rec = collections.Counter(bool(recognise(S, sets, q)["cube"]) for S in found)
    out["per_class"].append(dict(rep=int(r), orbit=int(counts[list(reps).index(r)]), status=sv.StatusName(st), solutions=len(found), cubes=rec[True], non_cubes=rec[False]))
    total["solutions"] += len(found); total["cubes"] += rec[True]; total["non_cubes"] += rec[False]; total["status_" + sv.StatusName(st)] += 1
    print(out["per_class"][-1], round(time.time() - t0), flush=True)
out["total"] = dict(total); print(out["total"]); json.dump(out, open("classify_q7.json", "w"), indent=1)
