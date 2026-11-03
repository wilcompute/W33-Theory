"""12533: the Fox dictionary for odd primes p.  On V_p = {c in F_p^6 : alternating sum 0} / <1>: the closed form omega is Fox-invariant and non-degenerate, each sigma_i is a transvection, and the cap subspace is a Lagrangian.  Plat closures: Fox p-colourings of the diagram (independent arc linear algebra) = p^(1 + dim(L0 meet beta L0)).  Control: a Lagrangian other than L0 disagrees.  usage: py -3 fox_general_p.py"""
import itertools
import json
import random
from sympy import GF, Matrix
from sympy.polys.matrices import DomainMatrix


def rk(rows, ncols, p):
    if not rows:
        return 0
    return DomainMatrix.from_Matrix(Matrix(len(rows), ncols, [x % p for r in rows for x in r])).convert_to(GF(p)).rank()


def fox_mat(s, p):
    """6 x 6 matrix of sigma_s^(+-1) acting on column colourings"""
    M = [[int(i == j) for j in range(6)] for i in range(6)]
    i = abs(s) - 1
    if s > 0:
        M[i][i], M[i][i + 1] = 0, 1
        M[i + 1][i], M[i + 1][i + 1] = -1 % p, 2
    else:
        M[i][i], M[i][i + 1] = 2, -1 % p
        M[i + 1][i], M[i + 1][i + 1] = 1, 0
    return M


def mul(A, B, p):
    return [[sum(A[i][k] * B[k][j] for k in range(6)) % p for j in range(6)] for i in range(6)]


def colourings(word, n, p):
    cur = list(range(n))
    nv = n
    top = cur[:]
    eqs = []
    for s in word:
        i = abs(s) - 1
        x, y = cur[i], cur[i + 1]
        z = nv
        nv += 1
        if s > 0:
            eqs.append(((x, -1), (z, -1), (y, 2)))
            cur[i], cur[i + 1] = y, z
        else:
            eqs.append(((y, -1), (z, -1), (x, 2)))
            cur[i], cur[i + 1] = z, x
    rows = []
    for e in eqs:
        r = [0] * nv
        for k, c in e:
            r[k] = (r[k] + c) % p
        rows.append(r)
    for u, v in [(top[a], top[a + 1]) for a in range(0, n, 2)] + [(cur[a], cur[a + 1]) for a in range(0, n, 2)]:
        r = [0] * nv
        r[u] = (r[u] + 1) % p
        r[v] = (r[v] - 1) % p
        rows.append(r)
    return nv - rk(rows, nv, p)


out = {}
rng = random.Random(9)
for p in (3, 5, 7, 11):
    sign = lambda c: [((-1) ** i * x) % p for i, x in enumerate(c)]
    def om(c, d):
        u, v = sign(c), sign(d)
        return sum(u[i] * v[j] - u[j] * v[i] for i in range(6) for j in range(i + 1, 6)) % p
    samples = []
    while len(samples) < 40:
        c = [rng.randrange(p) for _ in range(5)]
        c.append(sum((-1) ** i * x for i, x in enumerate(c)) % p)
        samples.append(c)
    gens = {s: fox_mat(s, p) for s in range(1, 6)}
    app = lambda M, c: [sum(M[i][j] * c[j] for j in range(6)) % p for i in range(6)]
    invariant = all(om(app(gens[s], c), app(gens[s], d)) == om(c, d) for s in gens for c in samples[:20] for d in samples[20:])
    # non-degenerate on V: rank of the Gram of a basis
    bas = []
    for v in itertools.product(range(2), repeat=4):
        if sum(v) == 1:
            c = [0, *v, 0]
            c[5] = sum((-1) ** i * x for i, x in enumerate(c[:5])) % p
            bas.append(c)
    nd = rk([[om(a, b) for b in bas] for a in bas], 4, p) == 4
    caps = [[1, 1, 0, 0, 0, 0], [0, 0, 1, 1, 0, 0], [0, 0, 0, 0, 1, 1]]
    isotropic = all(om(a, b) == 0 for a in caps for b in caps)
    one = [1] * 6
    def dim_meet(word, L):
        M = [[int(i == j) for j in range(6)] for i in range(6)]
        for s in word:
            M = mul(fox_mat(s, p), M, p)
        im = [app(M, x) for x in L]
        rA = rk(L + [one], 6, p)
        rB = rk(im + [one], 6, p)
        rS = rk(L + im + [one], 6, p)
        return (rA - 1) + (rB - 1) - (rS - 1)
    other = [[1, 0, 0, 1, 0, 0], [0, 1, 1, 0, 0, 0], [0, 0, 0, 0, 1, 1]]
    ag = t = mismatch_other = 0
    for _ in range(120):
        wd = [rng.choice((1, -1)) * rng.randint(1, 5) for _ in range(rng.randint(2, 14))]
        t += 1
        nul = colourings(wd, 6, p)
        d = dim_meet(wd, caps)
        ag += nul == 1 + d
        mismatch_other += nul != 1 + dim_meet(wd, other) if all(om(a, b) == 0 for a in other for b in other) else 0
    out[p] = dict(form_invariant=invariant, nondegenerate=nd, caps_isotropic=isotropic, plat_tests=t, plat_agree=ag, other_lagrangian_is_isotropic=all(om(a, b) == 0 for a in other for b in other), control_mismatches=mismatch_other)
    print(p, out[p], flush=True)
json.dump(out, open("fox_general_p.json", "w"), indent=1)
