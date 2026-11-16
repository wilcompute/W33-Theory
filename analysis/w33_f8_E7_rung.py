"""Pass 12678: the E7 rung of the F_8 code-space configuration.  On the effective three-qubit space V = F_2^6, Sp(6,2) = W(E7)/{+-1}
acts on the 64 quadratic forms polarising the symplectic form: 28 odd (27 singular non-zero points; the 28 bitangents of a plane
quartic) and 36 even (35).  (1) sigma-orbits on the 28 and 36 forms (sigma fixes exactly one form, the elliptic Q of Pass 12675, i.e.
one bitangent).  (2) For each of the nine bases L_t: the even forms vanishing on L_t.  (3) The full stabiliser in Sp(6,2) of the
configuration {L_t} (backtracking over images of a symplectic basis with weight constraints; all of Sp(6,2) is allowed, not only
W(E6) = O^-(6,2)), compared with the W(E6) stabiliser D9 of order 18 (Pass 12676).   usage: py -3 analysis/w33_f8_E7_rung.py"""
import collections, contextlib, io, json, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
G = {"__name__": "x", "__file__": os.path.join(HERE, "w33_f8_torus_is_E6a1.py")}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(os.path.join(HERE, "w33_f8_torus_is_E6a1.py"), encoding="utf-8").read(), G)
L, S, pts, form, enc, dec, nq, N, wt = (G[k] for k in ("L", "S", "pts", "form", "enc", "dec", "nq", "N", "wt"))
pc = lambda n: bin(n).count("1") & 1
forms = {}
for a in range(N):
    for b in range(N):
        forms[(a, b)] = tuple(pc(p[0] & p[1]) ^ pc(a & p[0]) ^ pc(b & p[1]) for p in pts)
pidx = {p: i for i, p in enumerate(pts)}
odd = [k for k, v in forms.items() if v.count(0) == 27]; even = [k for k, v in forms.items() if v.count(0) == 35]
assert len(odd) == 28 and len(even) == 36
Sinv = {S(p): p for p in pts}
def act(k):   # (sigma . Q)(p) = Q(sigma^{-1} p)
    v = forms[k]; nv = tuple(v[pidx[Sinv[p]]] for p in pts)
    return next(kk for kk, vv in forms.items() if vv == nv)
def orbits(ks):
    seen = set(); out = []
    for k in ks:
        if k in seen: continue
        o = [k]; x = act(k)
        while x != k: o.append(x); x = act(x)
        seen |= set(o); out.append(len(o))
    return sorted(out)
orb_odd, orb_even = orbits(odd), orbits(even)
even_on_L = [sum(1 for k in even if all(forms[k][pidx[p]] == 0 for p in L[t])) for t in range(9)]
odd_on_L = [sum(1 for k in odd if all(forms[k][pidx[p]] == 0 for p in L[t])) for t in range(9)]
print("sigma orbits on the 28 bitangents:", orb_odd, "| on the 36 even forms:", orb_even)
print("even forms vanishing on each basis:", even_on_L, "| odd forms vanishing on a basis:", odd_on_L)
# ---- full Sp(6,2) stabiliser of the configuration
Lsets = [frozenset(L[t]) for t in range(9)]; conf = set(Lsets)
basis = [(1 << i, 0) for i in range(nq)] + [(0, 1 << i) for i in range(nq)]
def apply(img, p):
    x = (0, 0)
    for i in range(2 * nq):
        bit = (p[0] >> i & 1) if i < nq else (p[1] >> (i - nq) & 1)
        if bit: x = (x[0] ^ img[i][0], x[1] ^ img[i][1])
    return x
def span_points(k):  # all non-zero combinations of the first k basis vectors
    out = []
    for m in range(1, 1 << k):
        p = (0, 0)
        for i in range(k):
            if m >> i & 1: p = (p[0] ^ basis[i][0], p[1] ^ basis[i][1])
        out.append((m, p))
    return out
memb = {p: frozenset(t for t in range(9) if p in Lsets[t]) for p in pts}
stab = []
def ok(img):
    k = len(img)
    for i in range(k):
        for j in range(k):
            if form(img[i], img[j]) != form(basis[i], basis[j]): return False
    for m, p in span_points(k):
        y = (0, 0)
        for i in range(k):
            if m >> i & 1: y = (y[0] ^ img[i][0], y[1] ^ img[i][1])
        if y == (0, 0) or wt[y] != wt[p]: return False
    return True
def bt(img):
    if len(img) == 2 * nq:
        g = list(img)
        if {frozenset(apply(g, p) for p in Ls) for Ls in Lsets} == conf: stab.append(g)
        return
    for y in pts:
        img.append(y)
        if ok(img): bt(img)
        img.pop()
bt([])
print("full Sp(6,2) stabiliser of the nine-basis configuration: order", len(stab), "(W(E6) stabiliser: 18)")
json.dump(dict(sigma_orbits_bitangents=orb_odd, sigma_orbits_even=orb_even, even_forms_vanishing_on_basis=even_on_L,
               odd_forms_vanishing_on_basis=odd_on_L, Sp62_stabiliser_order=len(stab)),
          open(os.path.join(ROOT, "data", "w33_f8_E7_rung.json"), "w"), indent=1)
