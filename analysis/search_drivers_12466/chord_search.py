"""12489: backtracking search for a GOOD matching of PG(1,q) (pairwise non-square cross-ratios, no three pairs in one involution,
i.e. no three chords of the conic concurrent).  Three pairs {a,b},{c,d},{e,f} lie in one involution iff cr(a,b,c,e) = cr(b,a,d,f)
(the involution swapping a,b and sending c to d is the projectivity (a,b,c) -> (b,a,d)).  usage: py -3 chord_search.py q [q ...]"""
import sys, json, time
from chord_condition import cr, INF


def search(q, tl=None, want_square=False):
    tl = tl or float(__import__("os").environ.get("CHORD_TL", "600"))
    sq = {x * x % q for x in range(1, q)}
    pts = [INF] + list(range(q))
    pairs, used, t0 = [], set(), time.time()
    nodes = [0]

    def ok(a, b):
        for (c, d) in pairs:
            if (cr(a, b, c, d, q) in sq) != want_square: return False
        for i in range(len(pairs)):
            for j in range(i + 1, len(pairs)):
                (c, d), (e, f) = pairs[i], pairs[j]
                for (x, y), (z, w), (u, v) in (((a, b), (c, d), (e, f)), ((a, b), (d, c), (e, f))):
                    pass
                # triple {a,b},{c,d},{e,f}: involution swapping c,d with e -> f: test whether it sends a -> b
                if cr(c, d, e, a, q) == cr(d, c, f, b, q): return False
        return True

    def bt():
        nodes[0] += 1
        if time.time() - t0 > tl: raise TimeoutError
        free = [p for p in pts if p not in used]
        if not free: return True
        a = free[0]
        for b in free[1:]:
            if ok(a, b):
                pairs.append((a, b)); used.update((a, b))
                if bt(): return True
                pairs.pop(); used.difference_update((a, b))
        return False
    try:
        found = bt()
    except TimeoutError:
        return dict(q=q, status="timeout", nodes=nodes[0])
    return dict(q=q, status="found" if found else "none", matching=pairs if found else None, nodes=nodes[0],
                seconds=round(time.time() - t0, 1))


if __name__ == "__main__":
    res = {}
    sqmode = "--square" in sys.argv                     # the Moore family (opposite regulus with 2 isotropic lines): all square
    for q in [int(a) for a in sys.argv[1:] if a.isdigit()]:
        r = search(q, want_square=sqmode); res[q] = r
        print(json.dumps({k: v for k, v in r.items() if k != "matching"}), flush=True)
    json.dump(res, open(__import__("os").environ.get("CHORD_OUT") or ("chord_search_square.json" if sqmode else "chord_search.json"), "w"), indent=1)
