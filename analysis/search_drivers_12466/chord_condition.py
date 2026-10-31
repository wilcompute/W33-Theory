"""12489: the combinatorial condition behind the regulus-matching family, tested against the geometric enumeration.
A matching of PG(1,q) (the regulus R0) is GOOD iff every two pairs have non-square cross-ratio AND no three pairs are swapped by one
Moebius involution (= no three chords of the conic concurrent).  usage: py -3 chord_condition.py"""
import itertools, json
INF = "inf"


def cr(a, b, c, d, q):
    def df(x, y):
        if x == INF: return 1
        if y == INF: return -1
        return (x - y) % q
    return df(a, c) * df(b, d) % q * pow(df(a, d) * df(b, c) % q, -1, q) % q


def mob(x, M, q):
    a, b, c, d = M
    if x == INF: return INF if c == 0 else a * pow(c, -1, q) % q
    den = (c * x + d) % q
    return INF if den == 0 else (a * x + b) * pow(den, -1, q) % q


def involutions(q):
    """all Moebius involutions x -> (a x + b)/(c x - a), a^2 + bc != 0, up to scalar"""
    seen, out = set(), []
    for a, b, c in itertools.product(range(q), repeat=3):
        if (a * a + b * c) % q == 0: continue
        M = (a, b, c, (-a) % q)
        key = tuple(mob(x, M, q) for x in [INF] + list(range(q)))
        if key not in seen: seen.add(key); out.append(M)
    return out


def good(m, q, sq, invs, square=False):
    if not all((cr(a, b, c, d, q) in sq) == square for (a, b), (c, d) in itertools.combinations(m, 2)): return False
    for t in itertools.combinations(m, 3):
        if any(all(mob(x, M, q) == y for x, y in t) for M in invs): return False
    return True


def matchings(items):
    if not items: yield []; return
    a = items[0]
    for i in range(1, len(items)):
        for m in matchings(items[1:i] + items[i + 1:]): yield [(a, items[i])] + m


if __name__ == "__main__":
    out = {}
    for q in (3, 5, 7, 11):
        sq = {x * x % q for x in range(1, q)}; invs = involutions(q)
        pts = [INF] + list(range(q))
        n = sum(1 for m in matchings(pts) if good(m, q, sq, invs))
        geo = None
        try:
            r = json.load(open(f"regulus_matching_q{q}.json"))["results"][-1]
            geo = r["even"]
            agree = all(good([tuple(p) for p in m], q, sq, invs) for m in r.get("good_matchings_param", []))
        except (OSError, KeyError):
            agree = None
        out[q] = dict(condition_count=n, geometric_count=geo, geometric_ones_satisfy=agree)
        print(q, out[q], flush=True)
    json.dump(out, open("chord_condition.json", "w"), indent=1)
