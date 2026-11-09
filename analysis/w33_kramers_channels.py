"""Item 4: what the Kramers reversal theta = s_alpha does to the amplitude channels.  For each of the 216 codewords: the left and right
pezzotopes (Pass 12636) have 15 facets each (10 roots + 5 contexts).  Report: shared facets, the union (roots, contexts), the roots
used by neither, and whether alpha (the double-six root of the codeword) is among them; whether theta maps the left facet set onto
the right one (it must); and the theta-fixed channels.
usage: py -3 analysis/w33_kramers_channels.py"""
import json, os
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
rf = {"__name__": "x", "__file__": os.path.join(HERE, "w33_pezzotope_reflection.py")}
src = open(os.path.join(HERE, "w33_pezzotope_reflection.py"), encoding="utf-8").read().split("# --- Item 4")[0]
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, rf)
by_key, info, pents, reflect_perm, image_pentad, roots_of = rf["by_key"], rf["info"], rf["pents"], rf["reflect_perm"], rf["image_pentad"], rf["roots_of"]
roots_of_pent = {frozenset(C): frozenset(r.values()) for C, r in pents}
st = Counter()
for k, (p, q) in by_key.items():
    a = p["alphas"][0]
    RL, RR = roots_of_pent[p["C"]], roots_of_pent[q["C"]]
    CL, CR = p["C"], q["C"]
    perm = reflect_perm(a)
    maps = frozenset(perm[x] for x in RL) == RR
    unused = frozenset(range(36)) - RL - RR
    st[(len(RL & RR), len(CL & CR), len(RL | RR), len(unused), a in unused, maps)] += 1
res = {str(k): v for k, v in st.items()}
print("(shared roots, shared contexts, roots in union, roots unused, alpha unused, theta maps left roots to right): count", res)
json.dump(res, open(os.path.join(ROOT, "data", "w33_kramers_channels.json"), "w"), indent=1)
IP = rf["IP"]
chk = Counter()
for k, (p, q) in by_key.items():
    a = p["alphas"][0]
    RL, RR = roots_of_pent[p["C"]], roots_of_pent[q["C"]]
    unused = frozenset(range(36)) - RL - RR
    perp = frozenset(b for b in range(36) if IP[a, b] == 0)
    moved = frozenset(b for b in range(36) if b != a and IP[a, b] != 0)
    chk[(unused == perp | {a}, (RL | RR) == moved)] += 1
print("(unused = {alpha} + alpha-perp, channels = the 20 roots not orthogonal to alpha): count", dict(chk))
res["unused_is_alpha_and_perp"] = {str(k): v for k, v in chk.items()}
json.dump(res, open(os.path.join(ROOT, "data", "w33_kramers_channels.json"), "w"), indent=1)
