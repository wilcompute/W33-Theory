"""Second solver: re-prove star cases with CaDiCaL (a CDCL SAT solver, no shared code with CP-SAT).  CNF: at each point the chosen lines are 0 or exactly 2; sequential-counter at-most-W.  Controls: the known minimum weight must be SAT in some class and W-2 UNSAT in all.
usage: py -3 recheck_cadical.py q W [first] [last]   (classes first..last)"""
import itertools, json, sys, time
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from star_cubes import build, orbits
q, W = int(sys.argv[1]), int(sys.argv[2])
B = build(q); digits, reps, counts = orbits(B); lines, through, X = B["lines"], B["through"], B["X"]
m = len(lines); first = int(sys.argv[3]) if len(sys.argv) > 3 else 0; last = int(sys.argv[4]) if len(sys.argv) > 4 else len(reps)
base = []
for p in range(len(B["pts"])):
    L = [j + 1 for j in through[p]]
    base += [[-a, -b, -c] for a, b, c in itertools.combinations(L, 3)]
    for a in L: base.append([-a] + [b for b in L if b != a])
card = CardEnc.atmost(lits=list(range(1, m + 1)), bound=W, top_id=m, encoding=EncType.seqcounter).clauses
res = dict(q=q, W=W, classes=len(reps), range=[first, last], unsat=0, sat=[], seconds=None); t0 = time.time()
for n, r in enumerate(reps.tolist()[first:last]):
    star = digits[r]; fixed = {X} | {B["choices"][i][int(star[i])] for i in range(q + 1)}; banned = {j for pt in B["Xpts"] for j in through[pt]} - fixed
    with Cadical153(bootstrap_with=base + card) as s:
        ok = s.solve(assumptions=[j + 1 for j in fixed] + [-(j + 1) for j in banned])
        if ok: res["sat"].append(dict(rep=r, weight=sum(1 for v in s.get_model()[:m] if v > 0)))
        else: res["unsat"] += 1
    print(f"  {n + 1}: rep {r} {'SAT' if ok else 'UNSAT'} {time.time() - t0:.0f}s", flush=True)
res["seconds"] = round(time.time() - t0, 1); print(res, flush=True); json.dump(res, open(f"recheck_cadical_q{q}_W{W}.json", "w"), indent=1)
