"""Fox p-colourings of a braid-word diagram, by arc linear algebra (shared by kauffman_golden.py).  Returns the nullity."""
from sympy import GF, Matrix
from sympy.polys.matrices import DomainMatrix


def rk(rows, ncols, p):
    if not rows:
        return 0
    return DomainMatrix.from_Matrix(Matrix(len(rows), ncols, [x % p for r in rows for x in r])).convert_to(GF(p)).rank()


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
