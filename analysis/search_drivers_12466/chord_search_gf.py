"""12490: the good-matching search of chord_search.py over any GF(q) (prime powers too), for both families:
  cube family  (opposite regulus with 0 isotropic lines): all cross-ratios NON-square, no three pairs in one involution;
  Moore family (opposite regulus with 2 isotropic lines): all cross-ratios SQUARE,     no three pairs in one involution.
Field tables from even_line_sets_gf.field (element 1 has index 1).  usage: py -3 chord_search_gf.py q [q ...]"""
import sys, json, time
from even_line_sets_gf import field

INF = -1


def make(q):
    F, add, mul = field(q)
    neg = [next(b for b in F if add[a][b] == 0) for a in F]
    inv = {a: next(b for b in F if mul[a][b] == 1) for a in F if a}
    sub = lambda a, b: add[a][neg[b]]
    sq = {mul[x][x] for x in F if x}

    def cr(a, b, c, d):
        def df(x, y):
            if x == INF: return 1
            if y == INF: return neg[1]
            return sub(x, y)
        num = mul[df(a, c)][df(b, d)]; den = mul[df(a, d)][df(b, c)]
        return mul[num][inv[den]]
    return F, cr, sq


def search(q, square, tl=1800):
    F, cr, sq = make(q)
    pts = [INF] + list(F)
    pairs, used, t0, nodes = [], set(), time.time(), [0]

    def ok(a, b):
        for (c, d) in pairs:
            if (cr(a, b, c, d) in sq) != square: return False
        for i in range(len(pairs)):
            for j in range(i + 1, len(pairs)):
                (c, d), (e, f) = pairs[i], pairs[j]
                if cr(c, d, e, a) == cr(d, c, f, b): return False
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
        return dict(status="timeout", nodes=nodes[0])
    return dict(status="found" if found else "none", nodes=nodes[0], seconds=round(time.time() - t0, 1), matching=pairs if found else None)


if __name__ == "__main__":
    out = {}
    for q in map(int, sys.argv[1:]):
        for fam, square in (("cube", False), ("moore", True)):
            r = search(q, square); out[f"{q}_{fam}"] = r
            print(q, fam, {k: v for k, v in r.items() if k != "matching"}, flush=True)
    json.dump(out, open("chord_search_gf.json", "w"), indent=1)
