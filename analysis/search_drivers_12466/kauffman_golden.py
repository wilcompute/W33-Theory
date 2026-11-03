"""12533 follow-up: the Brandt-Lickorish-Millett-Ho polynomial Q against Fox colourings at other primes.  Classical theorems (Rong; Jones; Lickorish-Millett): |Q_L((sqrt5 - 1)/2)| = sqrt5^r with r = dim H_1(M; F_5), and Q_L(-1) = (-3)^s with s = dim H_1(M; F_3) (my first recollection put this at x = 1, which the trefoil refutes).  So p = 5 should see W(3,5) as Jones sees W(3,3).
Q is computed by its skein Q(+) + Q(-) = x (Q(0) + Q(inf)), Q(unknot) = 1, via descending diagrams, with no colouring input; plat closures of B6 words.  Controls: Q(trefoil) = -3 + 2x + 2x^2, Q(figure-eight) = -3 - 4x... evaluated through its known values at x = 1 and x = 2.  usage: py -3 kauffman_golden.py"""
import json
import math
import random
import sys
from fractions import Fraction
from fox_general_p_lib import colourings


def build(word, n, closure="plat"):
    """half-edges (c, slot), slots TL, TR, BR, BL = 0, 1, 2, 3.  Strands: TL-BR, TR-BL.  over[c] = 0: TR-BL over; over[c] = 1: TL-BR over."""
    adj = {}
    last = {p: None for p in range(n)}
    first = {}
    over = {}
    for c, s in enumerate(word):
        i = abs(s) - 1
        over[c] = 0 if s > 0 else 1
        for p, slot in ((i, 0), (i + 1, 1)):
            if last[p] is None:
                first[p] = (c, slot)
            else:
                adj[last[p]] = (c, slot)
                adj[(c, slot)] = last[p]
        last[i] = (c, 3)
        last[i + 1] = (c, 2)
    free = 0
    # closure: tops and bottoms; a strand with no crossing is an arc
    ends_top, ends_bot = {}, {}
    for p in range(n):
        ends_top[p] = first.get(p)
        ends_bot[p] = last[p]
    pairs_top = [(a, a + 1) for a in range(0, n, 2)] if closure == "plat" else None
    # glue with the strand-through graph: treat plain strands as direct links between top and bottom
    links = {}
    def add(a, b):
        links.setdefault(a, []).append(b)
        links.setdefault(b, []).append(a)
    for p in range(n):
        if ends_top[p] is None:
            add(("T", p), ("B", p))
        else:
            add(("T", p), ends_top[p])
            add(("B", p), ends_bot[p])
    if closure == "plat":
        for a in range(0, n, 2):
            add(("T", a), ("T", a + 1))
            add(("B", a), ("B", a + 1))
    else:
        for p in range(n):
            add(("T", p), ("B", p))
    seen = set()
    for start in list(links):
        if start in seen or isinstance(start[0], str):
            continue
        cur, prev = start, None
        seen.add(start)
        node = links[start][0]
        back = start
        while isinstance(node[0], str):
            seen.add(node)
            nx = [v for v in links[node] if v != back]
            back, node = node, nx[0] if nx else back
        adj[start] = node
        adj[node] = start
        seen.add(node)
    # loops made only of T, B nodes
    vis = set()
    for s in links:
        if s in vis or not isinstance(s[0], str):
            continue
        comp = [s]
        vis.add(s)
        crossing = False
        while comp:
            a = comp.pop()
            for b in links[a]:
                if not isinstance(b[0], str):
                    crossing = True
                elif b not in vis:
                    vis.add(b)
                    comp.append(b)
        if not crossing:
            free += 1
    return dict(adj=adj, over=over, free=free)


def smooth(D, c, kind):
    adj = dict(D["adj"])
    free = D["free"]
    pairs = [((c, 0), (c, 1)), ((c, 3), (c, 2))] if kind == 0 else [((c, 0), (c, 3)), ((c, 1), (c, 2))]
    for p, q in pairs:
        a, b = adj[p], adj[q]
        if a == q:
            free += 1
            del adj[p], adj[q]
        else:
            adj[a] = b
            adj[b] = a
            del adj[p], adj[q]
    return dict(adj=adj, over={k: v for k, v in D["over"].items() if k != c}, free=free)


OPP = {0: 2, 2: 0, 1: 3, 3: 1}


def is_over(over, c, slot):
    return (slot in (1, 3)) if over[c] == 0 else (slot in (0, 2))


def violation(D):
    """walk components; returns the first crossing met on its under strand, or None and the number of components"""
    adj, over = D["adj"], D["over"]
    used = set()
    seen_c = set()
    comps = 0
    for c in sorted(over):
        for slot in (0, 1):
            if (c, slot) in used or (c, OPP[slot]) in used:
                continue
            comps += 1
            cur = (c, slot)
            while True:
                cc, ss = cur
                if (cc, ss) in used:
                    break
                if cc not in seen_c:
                    if not is_over(over, cc, ss):
                        return cc, None
                    seen_c.add(cc)
                used.add((cc, ss))
                used.add((cc, OPP[ss]))
                cur = adj[(cc, OPP[ss])]
    return None, comps


def Q(D, x, mu):
    if not D["over"]:
        return mu ** (D["free"] - 1) if D["free"] >= 1 else 1
    c, comps = violation(D)
    if c is None:
        return mu ** (comps + D["free"] - 1)
    sw = dict(D, over={**D["over"], c: 1 - D["over"][c]})
    return x * (Q(smooth(D, c, 0), x, mu) + Q(smooth(D, c, 1), x, mu)) - Q(sw, x, mu)


def value(word, n, x, closure="plat"):
    mu = 2 / x - 1
    return Q(build(word, n, closure), x, mu)


out = {}
g = (math.sqrt(5) - 1) / 2
out["trefoil_at_golden_vs_formula"] = (value([1, 1, 1], 2, g, "closure"), -3 + 2 * g + 2 * g * g)
out["trefoil_at_minus1"] = value([1, 1, 1], 2, -1.0, "closure")
out["figure8_at_minus1"] = value([1, -2, 1, -2], 3, -1.0, "closure")
out["unknot_twist"] = value([1], 2, 0.7, "closure")
out["two_unlinked"] = value([], 2, 0.7, "closure")
out["reidemeister2_invariance"] = (value([1, -1], 2, 0.7, "closure"), value([], 2, 0.7, "closure"))
rng = random.Random(3)
res = dict(golden=[0, 0], at_minus1=[0, 0])
bad = []
hist = {}
for _ in range(150):
    wd = [rng.choice((1, -1)) * rng.randint(1, 5) for _ in range(rng.randint(2, 9))]
    r5 = colourings(wd, 6, 5) - 1
    r3 = colourings(wd, 6, 3) - 1
    v5 = value(wd, 6, g)
    v3 = value(wd, 6, -1.0)
    res["golden"][0] += 1
    res["at_minus1"][0] += 1
    ok5 = abs(abs(v5) - 5 ** (r5 / 2)) < 1e-7
    ok3 = abs(v3 - (-3) ** r3) < 1e-7
    res["golden"][1] += ok5
    res["at_minus1"][1] += ok3
    hist[r5] = hist.get(r5, 0) + 1
    if not (ok5 and ok3):
        bad.append((wd, r5, v5, r3, v3))
out["tests"] = res
out["r5_histogram"] = hist
out["bad"] = bad[:3]
print(json.dumps(out, default=str))
json.dump(out, open("kauffman_golden.json", "w"), indent=1, default=str)
