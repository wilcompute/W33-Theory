"""A natural reason for Model A's light fragments: the missing-partner mechanism, searched exhaustively at the level of representation content.
Model A's light fermions are fragments of vectorlike SU(5) multiplets: from a 5: (3,1,-1/3) light, (1,2,1/2) heavy; from each of two 10's: (3,2,1/6) light, (3bar,1,-2/3) and (1,1,1) heavy.
Missing partner: a fragment of F gets a GUT mass only by pairing with a conjugate fragment in another multiplet R through a GUT-breaking vev.  If R has no conjugate of the wanted fragment, that fragment stays exactly massless at the GUT scale, whatever the couplings; it then gets M_X from the PQ field.  R's other fragments pair with Rbar by a bare mass.
Criterion for R, for F = 10 (conjugates: R must contain (3,1,2/3) and (1,1,-1), the conjugates of the heavy fragments, and must NOT contain (3bar,2,-1/6), the conjugate of the light one).  Then 10 x R must contain a GUT-breaking Higgs with an SM-singlet vev: 24 or 75 (also 200), checked by branching 10 x R.  Same for F = 5: R contains (1,2,-1/2), not (3bar,1,1/3).
This is content only: an accidental zero Clebsch could also make something light, and a nonzero Clebsch for every wanted pairing is assumed, as in the standard mechanism.  Model building beyond this (the Higgs potential, the Landau pole from big representations) is not done here.
Branching: SU(5) irreps from semistandard Young tableaux on {1..5}, indices 1-3 colour, 4-5 weak, Y = -1/3 per colour index, +1/2 per weak index (so 5 = (3,1,-1/3) + (1,2,1/2)); the weight multiset is peeled into SU(3) x SU(2) x U(1) irreps.
Controls: 5, 10, 24, 45, 50, 75 must reproduce their textbook decompositions, and the standard doublet-triplet missing partner: 50 contains the colour triplet (3,1,-1/3)'s conjugate partner but not a doublet.
usage: py -3 missing_partner_search.py"""
import itertools
import json
from collections import Counter
from fractions import Fraction as Fr


def ssyt(shape, n=5):
    """all semistandard tableaux of a partition shape with entries 1..n, as lists of rows"""
    cells = [(r, c) for r, l in enumerate(shape) for c in range(l)]
    res = []
    fill = {}

    def rec(i):
        if i == len(cells):
            res.append(dict(fill))
            return
        r, c = cells[i]
        lo = 1
        if c > 0:
            lo = max(lo, fill[(r, c - 1)])
        if r > 0:
            lo = max(lo, fill[(r - 1, c)] + 1)
        for v in range(lo, n + 1):
            fill[(r, c)] = v
            rec(i + 1)
        fill.pop((r, c), None)

    rec(0)
    return res


def weights(shape):
    out = []
    for t in ssyt(shape):
        cnt = Counter(t.values())
        out.append(tuple(cnt.get(i, 0) for i in range(1, 6)))
    return out


def sm_weight(w):
    """(su3 weight as (a1 - a2, a2 - a3) Dynkin-type from occupation numbers, su2 2*m, Y)"""
    c1, c2, c3, w1, w2 = w
    return (c1 - c2, c2 - c3, w1 - w2, Fr(-1, 3) * (c1 + c2 + c3) + Fr(1, 2) * (w1 + w2))


def su3_weights(p, q):
    """weights of SU(3) irrep (p,q) as Dynkin pairs with multiplicity, from tableaux of shape (p+q, q)"""
    if p == 0 and q == 0:
        return Counter({(0, 0): 1})
    sh = [p + q, q] if q else [p]
    out = Counter()
    for t in ssyt(sh, 3):
        cnt = Counter(t.values())
        n = [cnt.get(i, 0) for i in (1, 2, 3)]
        out[(n[0] - n[1], n[1] - n[2])] += 1
    return out


def su3_dim(p, q):
    return (p + 1) * (q + 1) * (p + q + 2) // 2


def branch(shape):
    ws = Counter()
    for w in weights(shape):
        a, b, m, y = sm_weight(w)
        # normalise: tableaux occupation gives SU(5) weights; the overall shift of the trace part is absorbed in Y with the convention above only for the traceless part; the true Y needs subtracting the U(5) trace
        ws[(a, b, m, y)] += 1
    # remove the U(1) of U(5): Y as computed includes a term proportional to the box count; subtract the average so that sum of Y over the rep is 0
    n = sum(ws.values())
    ybar = sum(k[3] * v for k, v in ws.items()) / n
    ws = Counter({(a, b, m, y - ybar): v for (a, b, m, y), v in ws.items()})
    irreps = Counter()
    while ws:
        # highest: max m, then max a+b, ...: take the weight maximising (y irrelevant) 2*a+b ordering via (a+b, a) and m
        key = max(ws, key=lambda k: (k[3], k[0] + k[1], k[0], k[2]))
        a, b, m, y = key
        # within fixed y, find the highest su3 x su2 weight
        cands = [k for k in ws if k[3] == y and k[0] >= 0 and k[1] >= 0 and k[2] >= 0]
        key = max(cands, key=lambda k: (k[0] + k[1], 2 * k[0] + k[1], k[2]))
        a, b, m, y = key
        irreps[(a, b, m + 1, y)] += 1
        for (wa, wb), mul in su3_weights(a, b).items():
            for mm in range(-m, m + 1, 2):
                k = (wa, wb, mm, y)
                ws[k] -= mul
                if ws[k] == 0:
                    del ws[k]
                assert ws.get(k, 0) >= 0, (shape, key)
    return irreps


def label(ir):
    (a, b, d2, y) = ir
    d3 = su3_dim(a, b)
    bar = "bar" if (b > a) else ""
    return f"({d3}{bar},{d2},{y})"


def dimension(shape):
    return len(ssyt(shape))


# enumerate SU(5) irreps up to a dimension cap
shapes = []
for k in range(1, 9):
    for sh in itertools.product(range(0, 9), repeat=4):
        if sh[0] < 1 or any(sh[i] < sh[i + 1] for i in range(3)) or sum(sh) != k:
            continue
        shapes.append(tuple(x for x in sh if x))
shapes = sorted(set(shapes), key=lambda s: (sum(s), s))
reps = {}
for sh in shapes:
    d = dimension(sh)
    if d > 220:
        continue
    reps[sh] = dict(dim=d, content={label(k): v for k, v in branch(sh).items()})
out = dict(n_reps=len(reps))
# controls
byname = {}
for sh, r in reps.items():
    byname.setdefault(r["dim"], []).append((sh, r["content"]))
ctl = {}
for d in (5, 10, 24, 45, 50, 75):
    ctl[str(d)] = [dict(shape=sh, content=c) for sh, c in byname.get(d, [])]
out["controls"] = ctl
for d in (5, 10, 24, 45, 50, 75):
    for sh, c in byname.get(d, [])[:2]:
        print(d, sh, sorted(c), flush=True)


def conj(lbl):
    # (d,dbar?,d2,y) -> conjugate label
    import re
    m = re.match(r"\((\d+)(bar)?,(\d+),(.+)\)", lbl)
    d3, bar, d2, y = m.group(1), m.group(2), m.group(3), Fr(m.group(4))
    if d3 in ("1", "8", "27") and not bar:
        nb = ""
    else:
        nb = "" if bar else "bar"
    return f"({d3}{nb},{d2},{-y})"


def has(content, lbl):
    return content.get(lbl, 0) > 0


# products: content of F x R contains a GUT Higgs singlet direction: the SU(5) rep must contain (1,1,0); we check that the product F x R contains the 24 or 75 SU(5) irreps by dimension matching through weights: compute F x R weight multiset and peel SU(5) irreps is heavy; use a necessary condition: F x R must contain an SM singlet (1,1,0) beyond those from the identity, and the candidate Higgs 24/75 must appear in F x R by the Littlewood-Richardson rule.
def lr_product(s1, s2, n=5):
    """Littlewood-Richardson for SU(5): returns Counter of shapes (columns of height 5 removed)"""
    def add_box_rows(shape, k, row_used):
        pass
    # brute force via weights: product weight multiset, peel highest weights of SU(5)
    w1 = Counter(weights(s1))
    w2 = Counter(weights(s2))
    prod = Counter()
    for a, x in w1.items():
        for b, y in w2.items():
            prod[tuple(i + j for i, j in zip(a, b))] += x * y
    # convert occupation vectors to Dynkin labels
    def dyn(w):
        return tuple(w[i] - w[i + 1] for i in range(4))
    pw = Counter()
    for w, m in prod.items():
        pw[dyn(w)] += m
    res = Counter()
    cache = {}
    while pw:
        top = max(pw, key=lambda d: (d[0] * 4 + d[1] * 6 + d[2] * 6 + d[3] * 4, d))
        # shape from Dynkin
        dl = top
        shape = []
        for i in range(4):
            shape.append(sum(dl[i:]))
        shape = tuple(x for x in shape if x)
        res[shape] += 1
        if shape not in cache:
            cache[shape] = Counter(tuple(w[i] - w[i + 1] for i in range(4)) for w in weights(shape)) if shape else Counter({(0, 0, 0, 0): 1})
        for k, v in cache[shape].items():
            pw[k] -= v
            if pw[k] == 0:
                del pw[k]
    return res


HIGGS = {(2, 1, 1, 1): "24", (2, 2, 1): "75", (2, 2, 2, 2): "200"}
F10 = (1, 1)
F5 = (1,)
need = {"10": dict(F=F10, must=["(3,1,2/3)", "(1,1,-1)"], mustnot=["(3bar,2,-1/6)"]), "5": dict(F=F5, must=["(1,2,-1/2)"], mustnot=["(3bar,1,1/3)"])}
found = {}
for name, req in need.items():
    hits = []
    for sh, r in reps.items():
        c = r["content"]
        if all(has(c, m) for m in req["must"]) and not any(has(c, m) for m in req["mustnot"]):
            prod = lr_product(req["F"], sh)
            higgs = [HIGGS[s] for s in prod if s in HIGGS]
            if higgs:
                hits.append(dict(shape=sh, dim=r["dim"], higgs=higgs, content=c))
    hits.sort(key=lambda h: h["dim"])
    found[name] = hits
    print(name, "partners found:", [(h["dim"], h["shape"], h["higgs"]) for h in hits[:12]], flush=True)
out["found"] = found
json.dump(out, open("missing_partner_search.json", "w"), indent=1, default=str)
