"""12483: structure of minimal even line sets of W(3,q), q odd.  (a) all minimum even line sets at q = 3 (CP-SAT enumeration, ONE
worker: multi-worker enumeration under-counts) classified by intersection graph; (b) the twin-pair test at every saved optimum:
twins {L, L'} (same neighbours) must be disjoint lines whose perp {L, L'}^perp (the q + 1 common transversals) lies inside the set;
(c) the pair graph (twin classes, adjacent when their lines meet) and its girth -- antiregularity of W(q)'s lines for q odd forbids
4-cycles, so girth >= 5 and #pairs >= 1 + ((q+1)/2)^2 (Moore bound) for every twin-paired even set.
usage: py -3 pair_structure.py"""
import json, itertools, collections
import networkx as nx
from ortools.sat.python import cp_model
from even_line_sets_gf import build


def graph_of(lines_pts):
    L = [frozenset(l) for l in lines_pts]
    G = nx.Graph(); G.add_nodes_from(range(len(L)))
    G.add_edges_from((a, b) for a, b in itertools.combinations(range(len(L)), 2) if L[a] & L[b])
    return L, G


def twin_report(q, lines, chosen_idx, all_lines_sets):
    L, G = graph_of([lines[j] for j in chosen_idx])
    nb = {v: frozenset(G[v]) for v in G}
    classes = collections.defaultdict(list)
    for v in G: classes[nb[v]].append(v)
    pairs = list(classes.values())
    rep = dict(n=len(L), twin_class_sizes=sorted(collections.Counter(len(c) for c in pairs).items()))
    if all(len(c) == 2 for c in pairs):
        ok = True
        for a, b in pairs:
            if L[a] & L[b]: ok = False                     # twins must be disjoint
            perp = {i for i, M in enumerate(all_lines_sets) if M & L[a] and M & L[b]}
            chosen_perp = {chosen_idx[v] for v in nb[a]}
            if perp != chosen_perp: ok = False             # their perp is exactly their neighbourhood in the set
        P = nx.Graph(); idx = {v: i for i, c in enumerate(pairs) for v in c}
        P.add_edges_from((idx[a], idx[b]) for a, b in G.edges if idx[a] != idx[b])
        rep.update(twin_paired=True, perps_inside=ok, pair_graph_n=P.number_of_nodes(),
                   pair_graph_degree=sorted(set(d for _, d in P.degree())), pair_graph_girth=nx.girth(P),
                   moore_bound_pairs=1 + ((q + 1) // 2) ** 2,
                   pair_graph_is_petersen=nx.is_isomorphic(P, nx.petersen_graph()),
                   pair_graph_is_c5=nx.is_isomorphic(P, nx.cycle_graph(5)))
    else:
        rep["twin_paired"] = False
    return rep


def enumerate_q3():
    pts, lines, N = build(3); n, m = N.shape
    md = cp_model.CpModel(); y = [md.NewBoolVar(f"y{j}") for j in range(m)]
    for i in range(n):
        z = md.NewIntVar(0, 2, f"z{i}"); md.Add(sum(y[j] for j in range(m) if N[i, j]) == 2 * z)
    md.Add(sum(y) == 10)
    sols = []

    class CB(cp_model.CpSolverSolutionCallback):
        def on_solution_callback(self):
            sols.append(tuple(j for j in range(m) if self.Value(y[j])))
    s = cp_model.CpSolver(); s.parameters.num_workers = 1; s.parameters.enumerate_all_solutions = True
    st = s.Solve(md, CB())
    sets = [frozenset(l) for l in lines]
    kinds = collections.Counter()
    twin = collections.Counter()
    for sol in sols:
        _, G = graph_of([lines[j] for j in sol])
        sig = (tuple(sorted(nx.adjacency_spectrum(G).real.round(3))),)
        kinds[sig] += 1
        r = twin_report(3, lines, list(sol), sets)
        twin[(r["twin_paired"], r.get("pair_graph_is_c5"), r.get("perps_inside"))] += 1
    # control: below 10 there is nothing (the MILP minimum)
    md2 = cp_model.CpModel(); y2 = [md2.NewBoolVar(f"y{j}") for j in range(m)]
    for i in range(n):
        z = md2.NewIntVar(0, 2, f"z{i}"); md2.Add(sum(y2[j] for j in range(m) if N[i, j]) == 2 * z)
    md2.Add(sum(y2) >= 1); md2.Add(sum(y2) <= 9)
    s2 = cp_model.CpSolver(); s2.parameters.num_workers = 1
    st2 = s2.Solve(md2)
    return dict(status=s.StatusName(st), count=len(sols), spectrum_classes={str(k): v for k, v in kinds.items()},
                twin_classes={str(k): v for k, v in twin.items()}, control_weight_1_to_9=s2.StatusName(st2))


if __name__ == "__main__":
    out = {"q3_enumeration": enumerate_q3()}
    for q in (3, 5, 7):
        for f in (f"even_line_sets_gf_q{q}.json", f"even_line_sets_gf_q{q}_sym2.json"):
            try: r = json.load(open(f))
            except OSError: continue
            pts, lines, N = build(q); pid = {tuple(p): i for i, p in enumerate(pts)}
            idx = {frozenset(l): j for j, l in enumerate(lines)}
            chosen = [idx[frozenset(pid[tuple(p)] for p in l)] for l in r["chosen_lines"]]
            out[f"q{q}_{'sym2' if 'sym2' in f else 'plain'}"] = twin_report(q, lines, chosen, [frozenset(l) for l in lines])
    print(json.dumps(out, indent=1))
    json.dump(out, open("pair_structure.json", "w"), indent=1)
