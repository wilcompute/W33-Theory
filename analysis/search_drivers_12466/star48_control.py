"""12518 positive control: move the known 48-line even set of W(3,9) onto X, read its star, take its normal form and class.  That class must come out
FEASIBLE at W = 48, while star_cubes_q9_W46.json has it INFEASIBLE at W = 46.  Exercises the whole chain: star extraction, normal form, label propagation,
case model.  usage: py -3 star48_control.py"""
import json, random, sys
import numpy as np
from star_cubes import build, orbits, solve_case
src = open("passant_orbits.py", encoding="utf-8").read().split("rng = random.Random(2)")[0]
exec(src)
S48 = {tuple(sorted(lines[j])) for j in S}
assert len(S48) == 48
B = build(9); digits, reps, counts = orbits(B)
Bl = B["lines"]; lid = {tuple(sorted(L)): j for j, L in enumerate(Bl)}
Bpts = B["pts"]
same_labelling = all(p in lid for p in [])  # the point labels are compared below
ptsA = list(pts); assert [tuple(p) for p in ptsA] == [tuple(p) for p in Bpts], "the two builds must share a labelling"
St = {lid[L] for L in S48}
F, add, mul = B["F"], B["add"], B["mul"]; X = B["X"]
def transvection(a):
    o = lambda u, v: add[add[mul[u[0]][v[2]]][B["neg"][mul[u[2]][v[0]]]]][add[mul[u[1]][v[3]]][B["neg"][mul[u[3]][v[1]]]]]
    return lambda v: tuple(add[v[i]][mul[o(v, a)][a[i]]] for i in range(4))
rng = random.Random(1); cur = set(St); moves = 0
while X not in cur:
    a = Bpts[rng.randrange(len(Bpts))]; lp = B["on_lines"](transvection(a)); cur = {lp[j] for j in cur}; moves += 1
    assert moves < 2000
through = B["through"]; star = []
for i, p in enumerate(B["Xpts"]):
    pick = [j for j in through[p] if j != X and j in cur]; assert len(pick) == 1, "the 48-set must be a hyperoval at this line"
    star.append(B["choices"][i].index(pick[0]))
T = np.array([star], dtype=np.int16); idx = int(B["normal_index"](T)[0]); rep = int(B["label"][idx])
assert rep in set(reps.tolist())
o = solve_case(B, digits[rep], 48, 900)
o46 = json.load(open("star_cubes_q9_W46.json"))
out = dict(moves=moves, representative=rep, status_W48=o["status"], weight=len(o.get("chosen", [])), W46_infeasible_classes=o46["infeasible"], W46_classes=o46["star_orbits"])
print(out); json.dump(out, open("star48_control.json", "w"), indent=1)
