"""Pass 12655 addendum: the 72 six-coordinate and 216 five-coordinate maximal null sections of the signed cubic (other track:
analysis/toe_20261113_albert_six_coordinate_sections.py; maximal cocliques of the 27-line meeting graph) under W(E6):
orbit structure, stabiliser orders (prediction: 720 = |W(A5)| and 240 = |W(A4 x A1)|, the Levi types GL(6) and GL(5) x SL(2) of the
M-theory and type IIB solutions of the E6(6) section constraint, Hohm-Samtleben arXiv:1312.0614), and the overlap pattern between the
two families (prediction from M-theory on T^2 <-> IIB on S^1: a sixer and a fiver share at most 4 coordinates = the common T^4).
usage: py -3 analysis/w33_sections_levi_overlap.py"""
import itertools, json, os
from collections import Counter
import networkx as nx
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
canon = json.load(open(os.path.join(ROOT, "artifacts/canonical_su3_gauge_and_cubic.json"), encoding="utf-8"))
triads = sorted(tuple(sorted(map(int, r["triple"]))) for r in canon["solution"]["d_triples"])
G = nx.Graph(); G.add_nodes_from(range(27))
for t in triads: G.add_edges_from(itertools.combinations(t, 2))
coc = [frozenset(c) for c in nx.find_cliques(nx.complement(G))]
six = [c for c in coc if len(c) == 6]; five = [c for c in coc if len(c) == 5]
sizes = Counter(len(c) for c in coc)
# automorphisms and orbits
GM = nx.algorithms.isomorphism.GraphMatcher(G, G)
six_id = {c: i for i, c in enumerate(six)}; five_id = {c: i for i, c in enumerate(five)}
stab6 = stab5 = 0; orb6 = set(); orb5 = set(); n = 0
for iso in GM.isomorphisms_iter():
    n += 1
    i6 = frozenset(iso[x] for x in six[0]); i5 = frozenset(iso[x] for x in five[0])
    orb6.add(i6); orb5.add(i5); stab6 += i6 == six[0]; stab5 += i5 == five[0]
ov = Counter(len(a & b) for a in six for b in five)
ov66 = Counter(len(a & b) for a, b in itertools.combinations(six, 2))
ov55 = Counter(len(a & b) for a, b in itertools.combinations(five, 2))
per_five = Counter(sum(1 for a in six if len(a & b) == 4) for b in five)
per_six = Counter(sum(1 for b in five if len(a & b) == 4) for a in six)
res = dict(maximal_coclique_sizes=dict(sizes), n_automorphisms=n, sixers=len(six), fivers=len(five),
           sixer_orbit=len(orb6), fiver_orbit=len(orb5), sixer_stabiliser_order=stab6, fiver_stabiliser_order=stab5,
           overlap_sixer_fiver={str(k): v for k, v in sorted(ov.items())}, overlap_sixer_sixer={str(k): v for k, v in sorted(ov66.items())},
           overlap_fiver_fiver={str(k): v for k, v in sorted(ov55.items())},
           sixers_sharing_4_per_fiver={str(k): v for k, v in per_five.items()}, fivers_sharing_4_per_sixer={str(k): v for k, v in per_six.items()})
print(res)
json.dump(res, open(os.path.join(ROOT, "data", "w33_sections_levi_overlap.json"), "w"), indent=1)
