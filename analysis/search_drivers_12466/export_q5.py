"""Export q = 5 line-permutation generators and one 20-set for GAP.  usage: py -3 export_q5.py"""
import json
from star_cubes import build, _pow
q = 5; B = build(q); add, mul, neg, F = B["add"], B["mul"], B["neg"], B["F"]
S = json.load(open("classify_q5_W20.json"))["feasible"][0]["sample"]
def transvection(a):
    w = lambda u, v: add[add[mul[u[0]][v[2]]][neg[mul[u[2]][v[0]]]]][add[mul[u[1]][v[3]]][neg[mul[u[3]][v[1]]]]]
    return lambda v: tuple(add[v[i]][mul[w(v, a)][a[i]]] for i in range(4))
prim = next(c for c in F if c and len({_pow(B, c, k) for k in range(q - 1)}) == q - 1)
E = [(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,0,1,0),(0,1,0,1),(1,1,0,0),(0,0,1,1),(1,0,0,1),(0,1,1,0)]
gens = [B["on_lines"](transvection(a)) for a in E] + [B["on_lines"](lambda v: (v[0], v[1], mul[prim][v[2]], mul[prim][v[3]]))]
open("gap_q5.g", "w").write("gens := [" + ",\n".join("PermList([" + ",".join(str(x + 1) for x in g) + "])" for g in gens) + "];;\nS := Set([" + ",".join(str(j + 1) for j in S) + "]);;\n")
