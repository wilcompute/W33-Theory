"""12267 (exact): a lattice shift D of one torus' Wilson lines changes the Ploger data by a group homomorphism of E8 x E8:
  c(D) = (2 D.V0 mod 4, 3 D.V1 mod 2, 3 D.W_b mod 2 for the off-torus lines b)        [self/in-torus terms change by even amounts]
so a single-torus repair exists iff the defect lies in the image subgroup.  The image is built by closure from the 480 roots (which
generate the lattice), each element with an explicit representative D (a sum of roots); two-torus repairs add the cross term
3 D_t.D_u mod 2 and are searched over pairs of representatives with every kernel adjustment of one of them."""
import itertools
from fractions import Fraction as F
import numpy as np
from mirage import read, fails, fmt, e8_short

ROOTS8 = [r for r in e8_short(2) if sum(x * x for x in r) == 2]
Z8 = [F(0)] * 8
ROOTS = [list(r) + Z8 for r in ROOTS8] + [Z8 + list(r) for r in ROOTS8]
dot = lambda a, b: sum(x * y for x, y in zip(a, b))


def nz(rows):
    return [a for a in range(6) if any(rows[3 + a])]


def cvec(rows, torus, D):
    V0, V1 = rows[0], rows[1]
    off = [b for b in nz(rows) if b // 2 != torus]
    return (int(2 * dot(D, V0)) % 4, int(3 * dot(D, V1)) % 2) + tuple(int(3 * dot(D, rows[3 + b])) % 2 for b in off)


def image(rows, torus):
    """closure of the image subgroup with representatives"""
    gens = [(cvec(rows, torus, r), r) for r in ROOTS]
    zero = tuple(0 for _ in gens[0][0])
    mods = (4, 2) + (2,) * (len(zero) - 2)
    rep = {zero: [F(0)] * 16}
    frontier = [zero]
    while frontier:
        new = []
        for g in frontier:
            for c, r in gens:
                h = tuple((x + y) % m for x, y, m in zip(g, c, mods))
                if h not in rep:
                    rep[h] = [x + y for x, y in zip(rep[g], r)]
                    new.append(h)
        frontier = new
    return rep


def apply(rows, torus, D):
    new = [r[:] for r in rows]
    for k in (3 + 2 * torus, 4 + 2 * torus):
        if any(new[k]):
            new[k] = [x + y for x, y in zip(new[k], D)]
    return new


def repairs(rows, want=2):
    """up to `want` distinct repairs: single-torus ones first (one per torus, then a second element of the coset), then two-torus."""
    out = []
    for torus in (2, 1, 0):
        if not any(rows[3 + 2 * torus]) and not any(rows[4 + 2 * torus]):
            continue
        rep = image(rows, torus)
        kernel = [D for g, D in rep.items() if not any(g)]
        for g, D in rep.items():
            new = apply(rows, torus, D)
            if not fails(new):
                out.append(((torus,), (D,), new))
                break
    if len(out) < want and out:                 # a second vector for the same torus: add a kernel element of the image
        torus, (D,), _ = out[0]
        for r in ROOTS:
            if cvec(rows, torus[0], r) == tuple(0 for _ in cvec(rows, torus[0], r)) or True:
                D2 = [x + y + y for x, y in zip(D, r)]          # D + 2r: same parity data, different vector
                new = apply(rows, torus[0], D2)
                if not fails(new):
                    out.append((torus, (D2,), new)); break
    if not out:                                  # two tori
        ts = [t for t in (0, 1, 2) if any(rows[3 + 2 * t]) or any(rows[4 + 2 * t])]
        for t, u in itertools.combinations(ts, 2):
            rt, ru = image(rows, t), image(rows, u)
            cand_t = list(rt.values()); cand_u = list(ru.values())
            kt = [r for r in ROOTS]
            for Dt in cand_t:
                for Du in cand_u:
                    for adj in [None] + kt:
                        Du2 = Du if adj is None else [x + y for x, y in zip(Du, adj)]
                        new = apply(apply(rows, t, Dt), u, Du2)
                        if not fails(new):
                            out.append(((t, u), (Dt, Du2), new))
                            break
                    if out: break
                if out: break
            if out: break
    return out[:want]
