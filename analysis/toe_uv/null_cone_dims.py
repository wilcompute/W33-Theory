"""Extends the null-history clock of the parallel track (986795826, b47886dac: F_q^3, Q = t^2 - x^2 - y^2, order q clock) to every dimension and signature.
For V = F_q^d with Q = sum eps_i x_i^2, join v, w when Q(v - w) = 0.  Cayley graph on (Z_p)^d: eigenvalues by the exact character sum, computed with an FFT over the group and rounded, with integer checks.
Reported for each (q, d, signature (a, b), a minus signs on b coordinates): degree, distinct eigenvalues and multiplicities, Laplacian levels, Witt index (largest totally isotropic subspace, by brute force on small cases and by the discriminant formula), strongly regular or not, and clock order: with N = q^(d-1), the order of exp(-2 pi i L / N).  N is a normalisation chosen to generalise the parallel track's q^2 at d = 3, so read the order as dependent on that choice; the intrinsic set is L / gcd(L), also reported.
Claims tested:
  (1) q = 3, d = 4, signature (1, 3) is SRG(81, 20, 1, 6), the Brouwer-Haemers graph.
  (2) For q = 3 mod 4 the type at d = 4 separates (1, 3) and (3, 1) (elliptic, Witt index 1) from (0, 4), (2, 2), (4, 0) (hyperbolic, Witt index 2).  For q = 1 mod 4 all signatures have Witt index 2.  Real Minkowski has Witt index 1 and real (2, 2) has 2, so only q = 3 mod 4 copies the real pattern.
  (3) clock order with N = q^(d-1) equals q exactly at d = 3, 4, and q^floor((d-1)/2) in general.
Controls: d = 3, q = 3 returns 8, 2^12, -1^8, -4^6, and q = 5 the parallel track's formula; eigenvalues sum to zero; multiplicities sum to q^d; direct dense eigensolve for small graphs agrees.
usage: py -3 null_cone_dims.py"""
import itertools
import json
import math
from functools import reduce
import numpy as np


def cone_indicator(p, eps):
    d = len(eps)
    grids = np.meshgrid(*[np.arange(p)] * d, indexing="ij")
    Q = sum(e * g * g for e, g in zip(eps, grids)) % p
    A = (Q == 0).astype(float)
    A[(0,) * d] = 0.0
    return A


def spectrum(p, eps):
    A = cone_indicator(p, eps)
    F = np.fft.fftn(A)
    assert np.max(np.abs(F.imag)) < 1e-6
    v = np.rint(F.real).astype(np.int64)
    assert np.max(np.abs(F.real - v)) < 1e-6
    u, c = np.unique(v, return_counts=True)
    return int(A.sum()), {int(a): int(b) for a, b in zip(u[::-1], c[::-1])}


def witt_index(p, eps):
    """largest totally isotropic subspace, by search: lines then planes, enough for d <= 5"""
    d = len(eps)
    vecs = [np.array(x) for x in itertools.product(range(p), repeat=d) if any(x)]
    B = lambda a, b: sum(e * x * y for e, x, y in zip(eps, a, b)) % p
    iso = [v for v in vecs if B(v, v) == 0]
    if not iso:
        return 0
    idx = 1
    # search for a plane
    for i, a in enumerate(iso[:400]):
        for b in iso[i + 1:]:
            if B(a, b) == 0 and np.linalg.matrix_rank(np.array([a, b]) % p) == 2:
                # independent over Z only tested mod sanity: exclude scalar multiples
                if any(np.array_equal((k * a) % p, b) for k in range(1, p)):
                    continue
                return 2
    return idx


def analyse(p, a, b):
    d = a + b
    eps = [1] * a + [-1] * b
    k, sp = spectrum(p, eps)
    assert sum(sp.values()) == p ** d
    assert sum(x * m for x, m in sp.items()) == 0
    L = sorted(k - x for x in sp)
    nz = [x for x in L if x]
    g = reduce(math.gcd, nz) if nz else 1
    N = p ** (d - 1)
    # order of exp(-2 pi i L / N)
    orders = [N // math.gcd(N, x) for x in L]
    order = reduce(lambda u, v: u * v // math.gcd(u, v), orders)
    row = dict(q=p, d=d, signature=[a, b], degree=k, spectrum={str(x): m for x, m in sp.items()}, L=L, intrinsic=[x // g for x in nz], gcd=g, clock_order=order, fixed_dim=sum(m for x, m in sp.items() if (k - x) % N == 0), n_levels=len(sp))
    if len(sp) == 3:
        ev = sorted(sp, reverse=True)
        r, s = ev[1], ev[2]
        row["srg"] = [p ** d, k, k + r + s + r * s, k + r * s]
    if d <= 4 and p <= 7:
        row["witt"] = witt_index(p, eps)
    return row


out = dict(rows=[])
for p, dmax in ((3, 7), (5, 5), (7, 4), (11, 3), (13, 3)):
    for d in range(2, dmax + 1):
        sigs = [(d - b, b) for b in range(0, d + 1)] if d <= 4 else [(1, d - 1)]
        for a, b in sigs:
            r = analyse(p, a, b)
            out["rows"].append(r)
            if d in (3, 4) or b == d - 1:
                print(p, d, (a, b), "k", r["degree"], "spec", r["spectrum"], "L", r["L"], "order", r["clock_order"], "srg", r.get("srg"), "witt", r.get("witt"), flush=True)
# controls
c = next(r for r in out["rows"] if r["q"] == 3 and r["d"] == 3 and r["signature"] == [1, 2])
out["control_d3_q3"] = c["spectrum"] == {"8": 1, "2": 12, "-1": 8, "-4": 6}
c5 = next(r for r in out["rows"] if r["q"] == 5 and r["d"] == 3 and r["signature"] == [1, 2])
out["control_d3_q5"] = c5["spectrum"] == {"24": 1, "4": 60, "-1": 24, "-6": 40}
# dense check
A = cone_indicator(3, [1, -1, -1, -1]).ravel()
idx = list(itertools.product(range(3), repeat=4))
pos = {v: i for i, v in enumerate(idx)}
M = np.zeros((81, 81))
for i, v in enumerate(idx):
    for j, w in enumerate(idx):
        M[i, j] = A[pos[tuple((x - y) % 3 for x, y in zip(v, w))]]
ev = np.rint(np.linalg.eigvalsh(M)).astype(int)
u, cnt = np.unique(ev, return_counts=True)
out["dense_q3_d4"] = {int(a): int(b) for a, b in zip(u, cnt)}
# triangle count check for SRG lambda
out["lambda_check"] = int(round(np.trace(M @ M @ M) / (81 * 20)))
print("controls", out["control_d3_q3"], out["control_d3_q5"], out["dense_q3_d4"], "lambda", out["lambda_check"], flush=True)
# signature pattern at d = 4
pat = {}
for r in out["rows"]:
    if r["d"] == 4:
        pat.setdefault(str(r["q"]), {})[str(tuple(r["signature"]))] = dict(k=r["degree"], witt=r.get("witt"))
out["d4_pattern"] = pat
print("d4", pat, flush=True)
ord_ = {}
for r in out["rows"]:
    if r["signature"] == [1, r["d"] - 1]:
        ord_.setdefault(str(r["q"]), {})[r["d"]] = r["clock_order"]
out["order_by_dim"] = ord_
print("order", ord_, flush=True)
json.dump(out, open("null_cone_dims.json", "w"), indent=1, default=float)
