"""Export line-permutation generators and the minimal sets for GAP: q = 7 cube, q = 9 48-set, with transvections, a similitude and (q = 9) Frobenius.  usage: py -3 export_gap.py"""
import json
from star_cubes import build, orbits, solve_case, _pow, _char
def run(q, S, name):
    B = build(q); add, mul, neg, F = B["add"], B["mul"], B["neg"], B["F"]
    def transvection(a):
        w = lambda u, v: add[add[mul[u[0]][v[2]]][neg[mul[u[2]][v[0]]]]][add[mul[u[1]][v[3]]][neg[mul[u[3]][v[1]]]]]
        return lambda v: tuple(add[v[i]][mul[w(v, a)][a[i]]] for i in range(4))
    prim = next(c for c in F if c and len({_pow(B, c, k) for k in range(q - 1)}) == q - 1)
    E = [(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,0,1,0),(0,1,0,1),(1,1,0,0),(0,0,1,1),(1,0,0,1),(0,1,1,0),(prim,0,1,0),(0,prim,0,1),(1,prim,0,0),(0,0,1,prim)]
    gens = [B["on_lines"](transvection(a)) for a in E]
    gens.append(B["on_lines"](lambda v: (v[0], v[1], mul[prim][v[2]], mul[prim][v[3]])))
    p, k = _char(q)
    if k > 1: gens.append(B["on_lines"](lambda v: tuple(_pow(B, t, p) for t in v)))
    if S is None:
        digits = orbits(B)[0]; S = solve_case(B, digits[11905], 40, 300)["chosen"]
    with open(f"gap_{name}.g", "w") as f:
        f.write("gens := [" + ",\n".join("PermList([" + ",".join(str(x + 1) for x in g) + "])" for g in gens) + "];;\n")
        f.write("S := Set([" + ",".join(str(int(j) + 1) for j in S) + "]);;\n")
run(7, None, "q7")
o = json.load(open("symmetric_fast_q9_r10.json"))[0]["chosen"]
run(9, o, "q9")
