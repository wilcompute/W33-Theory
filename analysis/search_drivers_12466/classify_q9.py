"""12525: minimal even line sets of W(3,9) at weight 48, hyperoval half: test all 511 star classes at W = 48 (with sum == 48); in each feasible class list every set by exclusion, blocking each found set singly (8 workers = search, not enumeration).
Prediction if the 48-set is unique up to symmetry (GAP: stabiliser 1920, transitive on its 48 lines): exactly one feasible class, with (normal forms in class) x (sets per normal form) = 3586680*48/820/729 = 288.  usage: py -3 classify_q9.py [secs]"""
import json, sys, time
from ortools.sat.python import cp_model
from star_cubes import build, orbits
from cube_recognise import recognise
q, W = 9, 48; tl = float(sys.argv[1]) if len(sys.argv) > 1 else 1800
B = build(q); digits, reps, counts = orbits(B); lines, through, X = B["lines"], B["through"], B["X"]
res = dict(q=q, W=W, classes=len(reps), infeasible=0, unknown=[], feasible=[]); t0 = time.time()
for n, (r, size) in enumerate(zip(reps.tolist(), counts.tolist())):
    star = digits[r]; fixed = {X} | {B["choices"][i][int(star[i])] for i in range(q + 1)}; banned = {j for p in B["Xpts"] for j in through[p]} - fixed
    md = cp_model.CpModel(); y = {j: (1 if j in fixed else 0 if j in banned else md.NewBoolVar(f"y{j}")) for j in range(len(lines))}
    for p in range(len(B["pts"])):
        z = md.NewBoolVar(f"z{p}"); md.Add(sum(y[j] for j in through[p]) == 2 * z)
    md.Add(sum(y.values()) == W); found = []; status = None
    while True:
        sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = tl; sv.parameters.num_workers = 8
        st = sv.Solve(md); status = sv.StatusName(st)
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE): break
        T = [j for j in range(len(lines)) if (y[j] if isinstance(y[j], int) else sv.Value(y[j]))]; found.append(T)
        free = [j for j in T if not isinstance(y[j], int)]; md.Add(sum(y[j] for j in free) <= len(free) - 1)
    if status == "INFEASIBLE" and not found: res["infeasible"] += 1
    elif status == "INFEASIBLE": res["feasible"].append(dict(rep=r, normal_forms=size, sets=len(found), sample=found[0]))
    else: res["unknown"].append(dict(rep=r, partial=len(found)))
    print(f"  {n + 1}/{len(reps)} rep {r} size {size}: {status} found {len(found)}; inf {res['infeasible']} feas {len(res['feasible'])} unk {len(res['unknown'])} {time.time() - t0:.0f}s", flush=True)
    json.dump(res, open("classify_q9.json", "w"), indent=1)
res["done"] = True; json.dump(res, open("classify_q9.json", "w"), indent=1); print("DONE", res["infeasible"], [(f["rep"], f["normal_forms"], f["sets"]) for f in res["feasible"]], res["unknown"])
