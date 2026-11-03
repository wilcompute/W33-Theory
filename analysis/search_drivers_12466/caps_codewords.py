"""12533 follow-up: the 2 codewords containing all 5 non-crossing cap lines.  Are the 5 caps a pentad (a side of the crown, pairwise disjoint)?  Relations among the 5 non-crossing lines; which codewords contain them; the other side of the crown for each; relation of the two codewords (same double-six? share lines?); the sixth bipartite matching.  Also: the Gram matrix of the 5 cap stabiliser states against the TL loop values delta^(loops-3).  usage: py -3 caps_codewords.py"""
import collections
import itertools
import json
import runpy

src = open("fox_w33.py", encoding="utf-8").read().split('caps = {to4(c) for c in ALL')[0]
exec(src)
bc = runpy.run_path("braid_codewords.py")
cw = bc["codewords"]
ls = [frozenset(L) for L in bc["lines"]]
lid = {L: j for j, L in enumerate(ls)}


def matching_line(M):
    pts_ = set()
    for s in itertools.product(range(3), repeat=3):
        c = [0] * 6
        for si, (a_, b_) in zip(s, M):
            c[a_] = c[b_] = si
        if any(to4(tuple(c))):
            pts_.add(pt_of(to4(tuple(c))))
    return frozenset(pts_)


NC = [[(0, 1), (2, 3), (4, 5)], [(0, 1), (2, 5), (3, 4)], [(0, 3), (1, 2), (4, 5)], [(0, 5), (1, 2), (3, 4)], [(0, 5), (1, 4), (2, 3)]]
XC = [(0, 3), (1, 4), (2, 5)]
caps = [matching_line(M) for M in NC]
assert all(c in lid for c in caps)
ids = [lid[c] for c in caps]
out = dict(noncrossing_line_ids=ids)


def loops(M1, M2):
    g = {}
    for a_, b_ in M1 + M2:
        g.setdefault(a_, []).append(b_)
        g.setdefault(b_, []).append(a_)
    seen, n = set(), 0
    for v in range(6):
        if v in seen:
            continue
        n += 1
        st = [v]
        while st:
            x = st.pop()
            if x in seen:
                continue
            seen.add(x)
            st.extend(g[x])
    return n


rel = []
for i, j in itertools.combinations(range(5), 2):
    rel.append(dict(pair=(i, j), loops=loops(NC[i], NC[j]), common_points=len(caps[i] & caps[j])))
out["pairs_loops_vs_common_points"] = rel
out["loops_to_common_points_law"] = sorted({(r["loops"], r["common_points"]) for r in rel})
six = [S for S in cw if set(ids) <= set(S)]
out["codewords_containing_all_five"] = len(six)
for t, S in enumerate(six):
    S = sorted(S)
    other = [j for j in S if j not in ids]
    graph = collections.Counter(sum(1 for b in S if b != a_ and ls[a_] & ls[b]) for a_ in S)
    five_side_edges = sum(1 for a_, b in itertools.combinations(ids, 2) if ls[a_] & ls[b])
    other_edges = sum(1 for a_, b in itertools.combinations(other, 2) if ls[a_] & ls[b])
    cross = sum(1 for a_ in ids for b in other if ls[a_] & ls[b])
    out[f"codeword_{t}"] = dict(degrees=dict(graph), edges_among_five=five_side_edges, edges_among_other_five=other_edges, cross_edges=cross)
if len(six) == 2:
    a_, b = map(set, six)
    out["two_codewords_common_lines"] = len(a_ & b)
    out["the_other_five_lines_differ"] = len((a_ - set(ids)) & (b - set(ids))) == 0
    third = frozenset((a_ ^ b))
    out["symmetric_difference_of_the_two_is_a_codeword"] = third in {frozenset(S) for S in cw}
    out["third_codeword_contains_caps"] = len(third & set(ids))
xc = matching_line(XC)
out["crossing_sixth_matching_is_a_line"] = xc in lid
out["crossing_sixth_points"] = len(xc)
print(json.dumps(out, default=str))
json.dump(out, open("caps_codewords.json", "w"), indent=1, default=str)
