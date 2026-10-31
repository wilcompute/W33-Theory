"""12487: structure of the symmetric even line sets of symmetric_even_sets.py (twin pairs, pair graph, girth, Moore/cage bound).
usage: py -3 sym_structure.py q r"""
import sys, json
import networkx as nx
from even_line_sets_gf import build
from pair_structure import twin_report

q, r = int(sys.argv[1]), int(sys.argv[2])
pts, lines, N = build(q); sets = [frozenset(l) for l in lines]
out = []
for rec in json.load(open(f"symmetric_q{q}_r{r}.json")):
    if "chosen" not in rec: continue
    rep = twin_report(q, lines, rec["chosen"], sets)
    rep.update(k=rec["k"], weight=rec["weight"], verified_even=rec["verified_even"], coverage=rec["coverage_profile"])
    print(json.dumps(rep)); out.append(rep)
json.dump(out, open(f"sym_structure_q{q}_r{r}.json", "w"), indent=1)
