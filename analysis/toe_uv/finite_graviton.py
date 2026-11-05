"""Linearised gravity and the Wigner classification on finite Minkowski space F_q^4, Q = t^2 - x^2 - y^2 - z^2, exact over GF(p).
(1) Linearised Einstein operator G(k) acting on symmetric h, a 10 x 10 matrix over GF(p), indices raised with eta:
    2 G_mn = k^2 h_mn - k_m (h k)_n - k_n (h k)_m + k_m k_n tr h - eta_mn (k^2 tr h - k h k).
    At each k: Bianchi k^m G_mn = 0, gauge h = k xi + xi k in the kernel, rank, physical polarisations = dim ker - dim gauge.  Control: over the rationals, null k gives rank 4 and 2 polarisations, non-null rank 6 and 0.
(2) Fierz-Pauli with mass: M(k) = G(k) acting on h minus (m^2/2)(h - eta tr h) at k^2 = m^2 for every non-null value.  Physical massive polarisations = dim ker M.  Control over the rationals: 5.  The trace constraint carries the factor (d - 1) = 3, so characteristic 3 is the case to watch.
(3) Little group of null k = (1, 1, 0, 0): the rotation on (y, z), a^2 + b^2 = 1.  Order, whether k^perp/k is anisotropic, and action on the polarisations: the transverse traceless pair.  Helicity is defined mod the rotation order.  Reports for the full SO(2) and for its intersection with the spinor kernel Omega, where spinor norm is computed as the square class of the product of two reflection vectors.
    Collapse test: helicity h and -h are the same character iff 2h = 0 mod order.
Ranks use sympy DomainMatrix over GF(p).
usage: py -3 finite_graviton.py"""
import itertools
import json
import sympy as sp
from sympy.polys.domains import GF, QQ
from sympy.polys.matrices import DomainMatrix

IDX = [(i, j) for i in range(4) for j in range(i, 4)]
ETA = [1, -1, -1, -1]


def operator(k, m2=None, dom=None):
    """returns the 10 x 10 integer matrix, with h symmetric coordinates: h_ij = h_ji = coordinate.  Output covariant G_mn on the same index list."""
    kup = [ETA[i] * k[i] for i in range(4)]  # k^i, with k given lower
    k2 = sum(kup[i] * k[i] for i in range(4))
    M = [[0] * 10 for _ in range(10)]
    for c, (a, b) in enumerate(IDX):
        h = [[0] * 4 for _ in range(4)]
        h[a][b] = 1
        h[b][a] = 1
        hk = [sum(h[n][r] * kup[r] for r in range(4)) for n in range(4)]
        tr = sum(ETA[r] * h[r][r] for r in range(4))
        khk = sum(kup[n] * hk[n] for n in range(4))
        for row, (m, n) in enumerate(IDX):
            e = ETA[m] if m == n else 0
            v = k2 * h[m][n] - k[m] * hk[n] - k[n] * hk[m] + k[m] * k[n] * tr - e * (k2 * tr - khk)
            if m2 is not None:
                v -= m2 * (h[m][n] - e * tr)
            M[row][c] = v
    return M


def rank(M, p):
    if p == 0:
        return DomainMatrix([[QQ(x) for x in r] for r in M], (len(M), len(M[0])), QQ).rank()
    return DomainMatrix([[GF(p)(x % p) for x in r] for r in M], (len(M), len(M[0])), GF(p)).rank()


def gauge_matrix(k):
    A = [[0] * 4 for _ in range(10)]
    for c in range(4):
        xi = [0] * 4
        xi[c] = 1
        for row, (m, n) in enumerate(IDX):
            A[row][c] = k[m] * xi[n] + k[n] * xi[m]
    return A


def mul(A, B):
    return [[sum(a * b for a, b in zip(r, col)) for col in zip(*B)] for r in A]


def is_zero(M, p):
    return all((x % p if p else x) == 0 for r in M for x in r)


def bianchi(M, k):
    kup = [ETA[i] * k[i] for i in range(4)]
    B = [[0] * 10 for _ in range(4)]
    for n in range(4):
        for c in range(10):
            s = 0
            for m in range(4):
                a, b = (m, n) if m <= n else (n, m)
                s += ETA[m] * k[m] * M[IDX.index((a, b))][c]
            B[n][c] = s
    return B


out = {}
# controls over Q
null = [1, 1, 0, 0]
nonnull = [2, 1, 0, 0]
G0, G1 = operator(null), operator(nonnull)
out["control_Q"] = dict(rank_null=rank(G0, 0), gauge_null=rank(gauge_matrix(null), 0), rank_nonnull=rank(G1, 0), gauge_nonnull=rank(gauge_matrix(nonnull), 0), massive_kernel=10 - rank(operator(nonnull, m2=3), 0), kill_gauge=is_zero(mul(G0, gauge_matrix(null)), 0), bianchi=is_zero(bianchi(G0, null), 0))
print("Q control", out["control_Q"], flush=True)
rows = {}
for p in (3, 5, 7, 11, 13):
    census = {}
    bad_b, bad_g = 0, 0
    pts = list(itertools.product(range(p), repeat=4)) if p == 3 else []
    if p > 3:
        import random
        random.seed(5)
        pts = [tuple(random.randrange(p) for _ in range(4)) for _ in range(500)] + [(1, 1, 0, 0)]
    for k in pts:
        if not any(k):
            continue
        k = list(k)
        k2 = sum(ETA[i] * k[i] * k[i] for i in range(4)) % p
        G = operator(k)
        g = gauge_matrix(k)
        if not is_zero(mul(G, g), p):
            bad_g += 1
        if not is_zero(bianchi(G, k), p):
            bad_b += 1
        r = rank(G, p)
        rg = rank(g, p)
        key = ("null" if k2 == 0 else "nonnull", r, rg, 10 - r - rg)
        census[str(key)] = census.get(str(key), 0) + 1
    # massive: at non-null k with m2 = k2
    mass = {}
    for k in pts[:400]:
        k = list(k)
        k2 = sum(ETA[i] * k[i] * k[i] for i in range(4)) % p
        if k2 == 0 or not any(k):
            continue
        M = operator(k, m2=k2)
        mass[str(10 - rank(M, p))] = mass.get(str(10 - rank(M, p)), 0) + 1
    # little group
    rot = [(a, b) for a in range(p) for b in range(p) if (a * a + b * b) % p == 1]
    def order(a, b):
        x, y, n = a, b, 1
        while (x, y) != (1, 0):
            x, y = (x * a - y * b) % p, (x * b + y * a) % p
            n += 1
        return n
    ords = [order(a, b) for a, b in rot]
    N = len(rot)
    aniso = all((a * a + b * b) % p for a in range(p) for b in range(p) if (a, b) != (0, 0))
    # spinor norm of rotation by (a, b): for R = reflections in u, v, spinor norm Q(u) Q(v).  R = product of reflection in e1 and in w, w = (1 + a, b) up to scale (or e2 if a = -1): spinor norm = Q(w) = 2 (1 + a) mod squares.
    squares = {(x * x) % p for x in range(1, p)}
    omega = []
    for (a, b) in rot:
        if (a + 1) % p == 0 and b == 0:
            sn = 1  # rotation by pi: reflections in e1 and e2, Q = 1 x 1
        else:
            sn = (2 * (1 + a)) % p
        if sn in squares:
            omega.append((a, b))
    No = len(omega)
    hel = {}
    for name, n in (("SO2", N), ("Omega", No)):
        hel[name] = dict(order=n, photon_pm1_distinct=(2 % n != 0) if n else None, graviton_pm2_distinct=(4 % n != 0) if n else None, graviton_same_as_scalar=(2 % n == 0) if n else None, gravitino_note=None)
    # action on TT polarisations (y y - z z, y z) by a generator: eigenvalue squared
    gen = max(rot, key=lambda r: order(*r))
    a, b = gen
    # rotation by theta acts on (h_yy - h_zz, 2 h_yz) by rotation by 2 theta: (a^2 - b^2, 2 a b)
    tt = ((a * a - b * b) % p, (2 * a * b) % p)
    rows[str(p)] = dict(census=census, bad_gauge=bad_g, bad_bianchi=bad_b, massive_kernel=mass, rotation_group_order=N, cyclic=(max(ords) == N), anisotropic_transverse=aniso, helicity=hel, generator=gen, tt_rotation=tt, tt_is_scalar=(tt[1] == 0))
    print(p, "census", census, "bad", bad_g, bad_b, "massive dim", mass, "rot order", N, "aniso", aniso, "omega", No, "pm2 distinct", hel["SO2"]["graviton_pm2_distinct"], hel["Omega"]["graviton_pm2_distinct"], "pm1 distinct", hel["SO2"]["photon_pm1_distinct"], hel["Omega"]["photon_pm1_distinct"], "tt", tt, flush=True)
out["rows"] = rows
json.dump(out, open("finite_graviton.json", "w"), indent=1, default=str)
