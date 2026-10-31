"""12498: is a bipartite even line set S = P u P' (two partial spreads covering the same points) the symmetric difference of two SPREADS
of W(q)?  Exact-cover the uncovered points by pairwise disjoint lines (CP-SAT); if T exists, S1 = P u T and S2 = P' u T are spreads with
S1 ^ S2 = S.  usage: py -3 spread_switch.py q file k"""
import sys, json, itertools
import networkx as nx
from ortools.sat.python import cp_model
from even_line_sets_gf import build

q, fn, k = int(sys.argv[1]), sys.argv[2], int(sys.argv[3])
pts, lines, N = build(q); sets = [frozenset(l) for l in lines]
rec = next(r for r in json.load(open(fn)) if r["k"] == k and "chosen" in r)
S = rec["chosen"]
G = nx.Graph(); G.add_nodes_from(S); G.add_edges_from((a, b) for a, b in itertools.combinations(S, 2) if sets[a] & sets[b])
P, P2 = nx.bipartite.sets(G)
covered = set().union(*(sets[j] for j in S))
free = set(range(len(pts))) - covered
cand = [j for j in range(len(lines)) if sets[j] <= free]
md = cp_model.CpModel(); y = {j: md.NewBoolVar(f"y{j}") for j in cand}
for p in free:
    md.AddExactlyOne(y[j] for j in cand if p in sets[j])
s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 1800; s.parameters.num_workers = 8
st = s.Solve(md)
out = dict(q=q, k=k, size=len(S), halves=[len(P), len(P2)], covered=len(covered), free=len(free), candidate_lines=len(cand),
           status=s.StatusName(st))
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    T = [j for j in cand if s.Value(y[j])]
    S1, S2 = set(P) | set(T), set(P2) | set(T)
    part = lambda X: sorted(collections.Counter(p for j in X for p in sets[j]).values()) if False else None
    cov1 = [0] * len(pts); cov2 = [0] * len(pts)
    for j in S1:
        for p in sets[j]: cov1[p] += 1
    for j in S2:
        for p in sets[j]: cov2[p] += 1
    out.update(T=len(T), S1_is_spread=set(cov1) == {1}, S2_is_spread=set(cov2) == {1}, shared=len(T), S1=sorted(S1), S2=sorted(S2))
print(json.dumps({x: v for x, v in out.items() if x not in ("S1", "S2")}))
json.dump(out, open(f"spread_switch_q{q}_k{k}.json", "w"), indent=1)
