"""12523 generalisation test: for the minimal even sets at q = 3, 5, 7, 9: how many factorisations (non-degenerate pairs {H, H^perp}, each with 2(q+1) points) miss all points covered by S, so that every line of S is 'Bell' for them?  Do those sentinels recover S (all lines missing them)?  Controls: an expected count for a random set of |S| lines of the same geometry (10 samples), and for q = 5 a non-minimal 22+ hyperoval if available.  usage: py -3 bell_generalisation.py"""
import itertools, json, random
from star_cubes import build, orbits, solve_case
def analyse(q, S, B, seed=1):
    pts, lines, add, mul, neg, pid, norm, F = B["pts"], B["lines"], B["add"], B["mul"], B["neg"], B["pid"], B["norm"], B["F"]
    form = lambda u, v: add[add[mul[u[0]][v[2]]][neg[mul[u[2]][v[0]]]]][add[mul[u[1]][v[3]]][neg[mul[u[3]][v[1]]]]]
    n = len(pts); seen = {}; hyps = []
    for a in range(n):
        for b in range(a + 1, n):
            if (a, b) in seen or form(pts[a], pts[b]) == 0: continue
            H = sorted({pid[norm(tuple(add[mul[s][pts[a][i]]][mul[t][pts[b][i]]] for i in range(4)))] for s in F for t in F if s or t})
            for x, y in itertools.combinations(H, 2): seen[(x, y)] = 1
            hyps.append(frozenset(H))
    hid = {h: i for i, h in enumerate(hyps)}; assert all(len(h) == q + 1 for h in hyps)
    perp = {}
    for h in hyps:
        P = [p for p in range(n) if all(form(pts[p], pts[x]) == 0 for x in list(h)[:2])]; perp[h] = frozenset(P); assert frozenset(P) in hid
    sentinels = {frozenset((h, perp[h])) for h in hyps}
    sets = [frozenset(L) for L in lines]
    def count(T):
        cov = frozenset().union(*(sets[j] for j in T))
        good = [s for s in sentinels if not any(h & cov for h in s)]
        missing = frozenset().union(*(h for s in good for h in s)) if good else frozenset()
        closure = {j for j in range(len(lines)) if not (sets[j] & missing)} if good else None
        return dict(covered=len(cov), sentinels_missed=len(good), closure_size=None if closure is None else len(closure), closure_is_S=closure == set(T) if good else False, union_missed_pts=len(missing))
    out = dict(q=q, weight=len(S), sentinels=len(sentinels), result=count(S))
    rng = random.Random(seed); out["random_lines_sentinels_missed"] = sorted(count(rng.sample(range(len(lines)), len(S)))["sentinels_missed"] for _ in range(10))
    return out
res = []
for q, W, rep_hint in ((3, 10, None), (5, 20, None), (7, 40, 11905)):
    B = build(q); digits, reps, counts = orbits(B)
    S = None
    for r in ([rep_hint] if rep_hint else reps.tolist()):
        o = solve_case(B, digits[r], W, 600)
        if "chosen" in o: S = o["chosen"]; break
    res.append(analyse(q, S, B)); print(res[-1], flush=True)
B = build(9); S = json.load(open("symmetric_fast_q9_r10.json"))[0]["chosen"]
res.append(analyse(9, S, B)); print(res[-1], flush=True)
json.dump(res, open("bell_generalisation.json", "w"), indent=1)
