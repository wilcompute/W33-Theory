"""Item 4: the pentad's stabiliser vs the doily's S6.  The 5 sentinel splits of a pentad are the star transpositions (k 6) of the doily S6
(Pass 12639); as duads containing the letter 6 they form an ovoid of the doily.  Prediction: the pentad's stabiliser in PSp(4,3) (order 120)
is the S5 fixing the letter 6, acting on the 5 sentinels as the natural S5 (faithful, transitive), and it preserves the 15 doily splits.
usage: py -3 analysis/w33_pentad_stab_doily.py"""
import itertools, json, os
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
d6 = {"__name__": "x", "__file__": os.path.join(HERE, "w33_doily_s6_kramers.py")}
src = open(os.path.join(HERE, "w33_doily_s6_kramers.py"), encoding="utf-8").read().split("sid = json.load")[0]
exec(src, d6)
group, splits, P = d6["group"], d6["splits"], d6["P"]
sb = {"__name__": "x", "__file__": os.path.join(HERE, "w33_pass12635_burkhardt_fan.py")}
exec(open(os.path.join(HERE, "w33_pass12635_burkhardt_fan.py"), encoding="utf-8").read().split("res = dict(")[0], sb)
lines = [frozenset(L) for L in sb["iso"]]
import contextlib, io
ns = {"__name__": "x", "__file__": os.path.join(HERE, "w33_pentad_umub.py")}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(os.path.join(HERE, "w33_pentad_umub.py"), encoding="utf-8").read().split("# --- (3)")[0], ns)
assert [frozenset(L) for L in ns["lines"]] == lines
pent = sorted(ns["maxsets"][0])
pent_pts = [lines[L] for L in pent]
covered = frozenset().union(*pent_pts); unc = frozenset(range(40)) - covered
sent = [s for s, (b, bp) in enumerate(splits) if (b | bp) <= unc]
sid = json.load(open(os.path.join(ROOT, "data", "w33_sentinel_identity.json")))
fifteen = set(sid["fifteen_splits"])
line_index = {L: i for i, L in enumerate(lines)}
split_index = {frozenset((b, bp)): s for s, (b, bp) in enumerate(splits)}
stab = [g for g in group if {line_index[frozenset(g[p] for p in lines[L])] for L in pent} == set(pent)]
acts = set(); keeps15 = True
for g in stab:
    img = []
    for s in sent:
        b, bp = splits[s]
        img.append(split_index[frozenset((frozenset(g[p] for p in b), frozenset(g[p] for p in bp)))])
    acts.add(tuple(sent.index(x) for x in img))
    for s in fifteen:
        b, bp = splits[s]
        if split_index[frozenset((frozenset(g[p] for p in b), frozenset(g[p] for p in bp)))] not in fifteen:
            keeps15 = False
res = dict(stabiliser_order=len(stab), sentinels=sent, sentinels_in_doily=set(sent) <= fifteen, image_on_sentinels=len(acts), preserves_doily_15=keeps15)
print(res)
json.dump(res, open(os.path.join(ROOT, "data", "w33_pentad_stab_doily.json"), "w"), indent=1, default=str)
