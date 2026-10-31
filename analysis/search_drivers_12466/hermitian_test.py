"""12497: is the 48-line even set of W(3,9) the union of two parallel classes of the Hermitian lines missing a Baer subgeometry?
Find all Hermitian forms h(x) = sum h_ij x_i xbar_j (xbar = x^3, h_ji = conj(h_ij)) vanishing on the 240 covered points (linear algebra
over GF(3) on the 16 F3-coordinates of h), then check: the surface has 280 points, the 40 extra points form a Baer subgeometry PG(3,3)
(every line through two of them meets them in 4 points), and all 48 lines lie on the surface and miss those 40 points.
usage: py -3 hermitian_test.py file k"""
import sys, json, itertools
from sympy import Matrix
from sympy.polys.matrices import DomainMatrix
from sympy.polys.domains import GF
from symmetric_fast import fast_build
from symmetric_even_sets_gf import setup

q = 9
pts, lines = fast_build(q); F, add, mul, inv, neg = setup(q)
frob = lambda x: mul[mul[x][x]][x]
# F9 = F3[i], i^2 = -1 (even_line_sets_gf: element index = c0 + 3 c1 for (c0, c1) low degree first)
coords = lambda a: (a % 3, a // 3)                    # F9 element -> (c0, c1) over F3 with a = c0 + c1 i
elem = lambda c0, c1: (c0 % 3) + 3 * (c1 % 3)
fn, k = sys.argv[1], int(sys.argv[2])
rec = next(r for r in json.load(open(fn)) if r["k"] == k and "chosen" in r)
S = rec["chosen"]
cov = set(p for j in S for p in lines[j])


def herm_terms(x):
    """h(x) = sum_i h_ii x_i xbar_i + sum_{i<j} Tr(h_ij x_i xbar_j); unknowns: h_ii in F3 (4), h_ij = u + v i (12): returns the F3
    coefficient row of h(x) (h(x) is in F3)."""
    row = []
    for i in range(4):
        nrm = mul[x[i]][frob(x[i])]                     # in F3
        row.append(coords(nrm)[0])
    for i, j in itertools.combinations(range(4), 2):
        z = mul[x[i]][frob(x[j])]                       # h_ij z + conj(h_ij z) = Tr(h_ij z); with h = u + v i:
        # Tr(u z) = u Tr(z), Tr(v i z) = v Tr(i z); Tr(w) = w + w^3 = 2 c0(w)
        tz = (2 * coords(z)[0]) % 3
        iz = mul[elem(0, 1)][z]; tiz = (2 * coords(iz)[0]) % 3
        row += [tz, tiz]
    return row


M = DomainMatrix([[GF(3)(v) for v in herm_terms(pts[p])] for p in sorted(cov)], (len(cov), 16), GF(3))
ns = M.to_Matrix().nullspace() if False else None
# nullspace over GF(3): use rref of the matrix
R, piv = M.rref()
free = [c for c in range(16) if c not in piv]
out = dict(covered=len(cov), rank=len(piv), nullity=len(free))
if len(free) >= 1:
    # build one nullspace vector per free column
    Rm = R.to_Matrix()
    sols = []
    for f in free:
        v = [0] * 16; v[f] = 1
        for r_i, pc in enumerate(piv):
            v[pc] = int(-Rm[r_i, f]) % 3
        sols.append(v)
    res = []
    for v in sols:
        on = [p for p in range(len(pts)) if sum(c * t for c, t in zip(herm_terms(pts[p]), v)) % 3 == 0]
        extra = sorted(set(on) - cov)
        ex = set(extra)
        # Baer test: every line of PG(3,9) through two extra points meets them in exactly 4 points (= q0 + 1)
        S_on = all(set(lines[j]) <= set(on) for j in S)
        miss = all(not (set(lines[j]) & ex) for j in S)
        res.append(dict(form=v, points_on_surface=len(on), extra=len(extra), lines_on_surface=S_on, lines_miss_extra=miss))
    out["forms"] = res
print(json.dumps(out, default=str))
json.dump(out, open(f"hermitian_test_k{k}.json", "w"), indent=1, default=str)
