"""Pass 12648 item 5: degree-6 real SOS (Sym^3 block 165 + charge-1 block 405) for a two-qutrit pentad.  Degree 4 gives exactly 1/9
(Pass 12639); the true minimum is 0.1471137632635549 = (207 - 19 sqrt57)/432 (numerical identification, Pass 12644).  Does degree 6
reach it?  Uses the generic solver of w33_threequbit_degree6.py.  usage: py -3 analysis/w33_pentad_degree6_sos.py"""
import json, os, contextlib, io
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_threequbit_degree6.py")}
src = open(os.path.join(HERE, "w33_threequbit_degree6.py"), encoding="utf-8").read()
exec(src[: src.index(chr(10) + "res = {}")], g)
cs = g["cs"]
with contextlib.redirect_stdout(io.StringIO()):
    pts, lag, w = cs["geometry"](3, 2); B = cs["bases_for"](3, 2, pts, lag); mps, _ = cs["maximal_partial_spreads"](lag)
five = sorted(next(S for S in mps if len(S) == 5))
r = g["solve"]([b for L in five for b in B[L].T], 9)
print("pentad degree-6:", r, flush=True)
json.dump(dict(pentad_degree6=r, degree4=1 / 9, numeric_min=0.1471137632635549), open(os.path.join(ROOT, "data", "w33_pentad_degree6_sos.json"), "w"), indent=1, default=str)
