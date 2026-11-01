"""12510-12511: (a) the 4-anyon braid image G (order 648) -- is it 3^{1+2}:SL(2,3)?  O_3(G) = intersection of the Sylow 3-subgroups
(order 81 each); test |O_3| = 27, non-abelian, exponent 3, Z(O_3) = Z(G) of order 3, and G/O_3 with the SL(2,3) element-order
profile (1:1, 2:1, 3:8, 4:6, 6:8).  (b) chirality: the 432 SIGNED minimal codewords (support + choice of which 5-line half is '+'),
Pass 173's two chiral orbits of 216 under PSp(4,3) as a control, and the orbits of B_4 and B_5 on them.  usage: py -3 braid_structure.py"""
import json, collections, itertools
import networkx as nx
src = open("braid_codewords.py", encoding="utf-8").read().split('out = dict(path=path')[0]
exec(src)                                   # gens, group, compose, codewords, lmap, lines, n, T, pts, allT
e = tuple(range(n))
inv = lambda g: tuple(sorted(range(n), key=lambda i: g[i]))
def order(g):
    k, x = 1, g
    while x != e: x = compose(g, x); k += 1
    return k
G = list(group(gens[:3])); Gs = set(G)
def closure(S):
    H = {e}; fr = [e]; S = list(S)
    while fr:
        nx_ = []
        for h in fr:
            for s in S:
                k = compose(s, h)
                if k not in H: H.add(k); nx_.append(k)
        fr = nx_
    return H
# one Sylow 3-subgroup: grow greedily with 3-power elements
threes = [g for g in G if order(g) in (3, 9, 27, 81)]
P = {e}
for t in threes:
    if t in P: continue
    H = closure(list(P) + [t])
    if len(H) <= 81 and 81 % len(H) == 0: P = H
    if len(P) == 81: break
sylows = {frozenset(compose(compose(g, x), inv(g)) for x in P) for g in G}
O3 = frozenset.intersection(*sylows)
abel = all(compose(a, b) == compose(b, a) for a in O3 for b in O3)
expo = sorted(set(order(x) for x in O3))
ZO3 = [z for z in O3 if all(compose(z, x) == compose(x, z) for x in O3)]
ZG = [z for z in G if all(compose(z, g) == compose(g, z) for g in G)]
O3s = set(O3)
cos = {}
for g in G: cos[min(compose(g, x) for x in O3)] = g
def qord(g):
    k, x = 1, g
    while x not in O3s: x = compose(g, x); k += 1
    return k
qprof = collections.Counter(qord(g) for g in cos.values())
part_a = dict(G=len(G), sylow3_order=len(P), n_sylow3=len(sylows), O3_order=len(O3), O3_abelian=abel, O3_element_orders=expo,
              Z_O3=len(ZO3), Z_G=len(ZG), Z_equal=set(ZO3) == set(ZG), quotient_order=len(cos), quotient_profile=dict(sorted(qprof.items())),
              SL23_profile={1: 1, 2: 1, 3: 8, 4: 6, 6: 8})
part_a["is_3^{1+2}:SL(2,3)"] = (len(O3) == 27 and not abel and expo == [1, 3] and len(ZO3) == 3 and set(ZO3) == set(ZG)
                               and dict(qprof) == {1: 1, 2: 1, 3: 8, 4: 6, 6: 8})
print(json.dumps(part_a), flush=True)
# (b) signed codewords
sets_l = [frozenset(L) for L in lines]
signed = []
for S in codewords:
    Gr = nx.Graph(); Gr.add_nodes_from(S); Gr.add_edges_from((a, b) for a, b in itertools.combinations(S, 2) if sets_l[a] & sets_l[b])
    A, B = [frozenset(x) for x in nx.bipartite.sets(Gr)]
    signed += [(A, B), (B, A)]
def act_signed(lm, sv):
    A, B = sv; return (frozenset(lm[j] for j in A), frozenset(lm[j] for j in B))
def orbits_signed(lms):
    idx = {sv: i for i, sv in enumerate(signed)}; seen, out = set(), []
    for sv in signed:
        if sv in seen: continue
        o = {sv}; fr = [sv]
        while fr:
            nx_ = []
            for x in fr:
                for lm in lms:
                    y = act_signed(lm, x)
                    if y not in o: o.add(y); nx_.append(y)
            fr = nx_
        seen |= o; out.append(o)
    return out
full = orbits_signed(allT)
b4 = orbits_signed([lmap(g) for g in gens[:3]]); b5 = orbits_signed([lmap(g) for g in gens[:4]])
# relation: does each B4 orbit of signed codewords lie inside one PSp chiral orbit?
chir = {sv: i for i, o in enumerate(full) for sv in o}
b4_in_chiral = [sorted(collections.Counter(chir[sv] for sv in o).items()) for o in b4]
part_b = dict(signed=len(signed), PSp_orbits=sorted(len(o) for o in full), B4_orbits=sorted(len(o) for o in b4),
              B5_orbits=sorted(len(o) for o in b5), B4_orbit_chirality_composition=b4_in_chiral)
print(json.dumps(part_b), flush=True)
json.dump(dict(a=part_a, b=part_b), open("braid_structure.json", "w"), indent=1, default=str)
