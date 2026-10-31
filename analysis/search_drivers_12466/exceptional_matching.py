"""12489: the good matchings are the antipodal systems of Galois' exceptional subgroups.  For each q with a good matching: the
PGL(2,q)-orbit of the matchings, the stabiliser (order and element-order profile: S4 = 1,9,8,6 for orders 1,2,3,4; A5 = 1,15,20,24
for orders 1,2,3,5), its transitivity on PG(1,q), and whether the matching is exactly the set of pairs {x, x'} fixed together by the
stabiliser's involution-free structure (antipodal blocks).  usage: py -3 exceptional_matching.py"""
import itertools, json, collections
from chord_condition import INF, mob, good, involutions, matchings


def pgl(q):
    seen, out = set(), []
    for a, b, c, d in itertools.product(range(q), repeat=4):
        if (a * d - b * c) % q == 0: continue
        key = tuple(mob(x, (a, b, c, d), q) for x in [INF] + list(range(q)))
        if key not in seen: seen.add(key); out.append(key)
    return out                                            # each element as the image tuple of [INF, 0, ..., q-1]


def order(perm):
    n = len(perm); k, cur = 1, perm
    ident = tuple(range(n))
    while cur != ident:
        cur = tuple(perm[i] for i in cur); k += 1
    return k


out = {}
for q in (3, 7, 11):
    pts = [INF] + list(range(q)); idx = {p: i for i, p in enumerate(pts)}
    sq = {x * x % q for x in range(1, q)}; invs = involutions(q)
    G = [tuple(idx[y] for y in g) for g in pgl(q)]
    goods = [frozenset(frozenset((idx[a], idx[b])) for a, b in m) for m in matchings(pts) if good(m, q, sq, invs)]
    m0 = goods[0]
    act = lambda g, m: frozenset(frozenset(g[i] for i in pr) for pr in m)
    orbit = {act(g, m0) for g in G}
    stab = [g for g in G if act(g, m0) == m0]
    prof = dict(sorted(collections.Counter(order(g) for g in stab).items()))
    transitive = len({g[0] for g in stab}) == q + 1
    # antipodal: the pairs of m0 are blocks of imprimitivity of the stabiliser
    blocks = all(frozenset(g[i] for i in pr) in m0 for g in stab for pr in m0)
    out[q] = dict(good=len(goods), PGL=len(G), orbit=len(orbit), one_orbit=len(orbit) == len(goods), stabiliser=len(stab),
                  order_profile=prof, transitive_on_PG1=transitive, pairs_are_blocks=blocks)
    print(q, out[q], flush=True)
json.dump({str(k): v for k, v in out.items()}, open("exceptional_matching.json", "w"), indent=1)
