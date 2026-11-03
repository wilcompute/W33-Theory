"""12527: which monomial orbits are even sets, for all primes q <= 61?  Test without building all lines: an orbit T is even iff every singular line meets it evenly; a singular line through a point of T is enough only if T is nonempty on it, so test the lines through each orbit point of T (a line missing T is trivially even).  Orbit reps: all singular vectors of Hamming weight <= 5 up to monomials, i.e. multisets of squares.  usage: py -3 frame_family.py qmax"""
import itertools, json, sys, collections
def primes(n): return [p for p in range(3, n + 1) if all(p % d for d in range(2, int(p ** .5) + 1))]
def singular_rep_classes(q):
    """monomial classes of singular points: a multiset of 5 values |x_i| up to scalar; a canonical form is the smallest over scalars."""
    half = [min(a, q - a) for a in range(q)]; seen = {}
    for v in itertools.combinations_with_replacement(range(0, (q + 1) // 2), 5):
        if not any(v) or sum(x * x for x in v) % q: continue
        best = min(tuple(sorted(min(c * x % q, q - c * x % q) for x in v)) for c in range(1, q))
        seen[best] = 1
    return list(seen)
def orbit(v, q):
    S = set()
    for p in set(itertools.permutations(v)):
        nz = [i for i, x in enumerate(p) if x]
        for s in itertools.product((1, -1), repeat=len(nz) - 1):
            u = list(p)
            for i, e in zip(nz[1:], s): u[i] = e * u[i] % q
            f = pow(next(x for x in u if x), -1, q); S.add(tuple(x * f % q for x in u))
    return S
def is_even(T, q):
    """every singular line through a point of T meets T evenly; lines through x = points of x^perp singular"""
    T_ = list(T); Tset = set(T_); hist = collections.Counter()
    x = T_[0]                                # T is a group orbit, so one point's lines suffice
    done = set()
    # singular y perpendicular to x, y != x: enumerate by the affine chart
    for y in itertools.product(range(q), repeat=5):
        if not any(y): continue
        if next(t for t in y if t) != 1 or y == x: continue
        if sum(a * b for a, b in zip(x, y)) % q or sum(a * a for a in y) % q: continue
        L = frozenset(_norm(tuple((a + t * b) % q for a, b in zip(x, y)), q) for t in range(q)) | {y}
        if L in done: continue
        done.add(L); hist[len(L & Tset)] += 1
    return all(k % 2 == 0 for k in hist), dict(hist), len(done)
def _norm(v, q):
    f = pow(next(x for x in v if x), -1, q); return tuple(x * f % q for x in v)
out = {}
for q in primes(int(sys.argv[1])):
    good = []; total = 0
    for v in singular_rep_classes(q):
        total += 1; O = orbit(v, q)
        if len(O) > 2000: continue
        if q > 31 and (sum(1 for x in v if x) == 5 and len(O) > 1000): continue
        ok, h, nl = is_even(O, q)
        assert nl == q + 1, (q, v, nl)
        if ok: good.append(dict(vector=v, size=len(O), intersections_through_a_point=h))
    out[q] = dict(classes=total, even_orbits=good); print(q, total, [(g["vector"], g["size"]) for g in good], flush=True)
    json.dump(out, open("frame_family.json", "w"), indent=1)
