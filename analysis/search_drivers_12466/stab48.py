"""12501: the exact stabiliser of the q = 9 48-line even set.  It fixes {X, Y} (the only degree-10 free lines), so it lies in
H = GL(2,9).2; enumerate all of H.  Report |Stab| (projective: M and -M act alike), its orbits on the 48 lines, element orders, and
whether the two 24-line halves are swapped.  usage: py -3 stab48.py"""
import json, itertools, collections
exec(open("passant_orbits.py", encoding="utf-8").read().split("rng = random.Random(2)")[0])
import networkx as nx
G = nx.Graph(); G.add_nodes_from(S); G.add_edges_from((a, b) for a, b in itertools.combinations(sorted(S), 2) if sets[a] & sets[b])
P1, P2 = [frozenset(x) for x in nx.bipartite.sets(G)]
Spts = {j: lines[j] for j in S}
stab = []
for a, b, c, d in itertools.product(F, repeat=4):
    if add[mul[a][d]][neg[mul[b][c]]] == 0: continue
    g = elem(((a, b), (c, d)))
    for sw in (False, True):
        def h(p): return swap(g(p)) if sw else g(p)
        img = set()
        ok = True
        for j, L in Spts.items():
            t = lid.get(tuple(sorted(h(x) for x in L)))
            if t not in S: ok = False; break
            img.add(t)
        if ok: stab.append((((a, b), (c, d)), sw, {j: lid[tuple(sorted(h(x) for x in L))] for j, L in Spts.items()}))
perm_set = {tuple(sorted(m.items())) for _, _, m in stab}
orb = []
seen = set()
for j in S:
    if j in seen: continue
    o = {m[j] for _, _, m in stab}; seen |= o; orb.append(len(o))
swaps_halves = sum(1 for _, _, m in stab if m[next(iter(P1))] in P2)
def order(m):
    k, cur = 1, dict(m)
    while any(cur[j] != j for j in cur):
        cur = {j: m[cur[j]] for j in cur}; k += 1
    return k
prof = collections.Counter(order(m) for _, _, m in stab)
out = dict(H_elements_tested=2 * 5760, stabiliser_elements=len(stab), distinct_line_permutations=len(perm_set),
           orbits_on_S=sorted(orb), elements_swapping_halves=swaps_halves, order_profile_on_lines=dict(sorted(prof.items())))
print(json.dumps(out)); json.dump(out, open("stab48_q9.json", "w"))
