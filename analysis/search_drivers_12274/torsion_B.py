"""12274/12275: the torsion bicharacter induced by a Wilson-line lattice shift.
If the lattice vector lam is added to the Wilson lines in a set S (one line, or both lines of a Z3 torus pair), the left momenta of a
sector h form the same coset (Lambda + V_h + sigma_h lam = Lambda + V_h), and the projection phase of g on sector h changes by
      B(g, h) = 1/2 (sigma_g V_h.lam - sigma_h V_g.lam)  mod 1,     sigma_g = sum_{x in S} m_x(g)
(antisymmetric; the quadratic term is integral because lam^2 is even).  Space-group elements g = (w^e theta_k, m), V_g = e V0 + k.shifts
+ sum_b m_b W_b.  g = (theta_k, m) and h = (theta_l, f) commute iff (1 - theta_l) m = (1 - theta_k) f.  Exact integer arithmetic:
VL = 24 V.lam, and B != 0 iff sigma_g VL_h - sigma_h VL_g != 0 mod 48."""
import itertools, sys, collections
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, '../search_drivers_12267')
from mirage import read
dot = lambda a, b: sum(x * y for x, y in zip(a, b))
Z3T = np.array([[0, -1], [1, -1]])


def twists(geo):
    I2 = np.eye(2, dtype=np.int64)
    if 'Z2xZ2' in geo:
        blk = lambda s: np.kron(np.diag(s), I2)
        return [((0, 0), blk([1, 1, 1])), ((1, 0), blk([1, -1, -1])), ((0, 1), blk([-1, 1, -1])), ((1, 1), blk([-1, -1, 1]))], 2
    th = np.kron(np.eye(3, dtype=np.int64), Z3T)
    return [((0,), np.eye(6, dtype=np.int64)), ((1,), th), ((2,), th @ th)], 3


def table(rows, geo, S, lam):
    T, box = twists(geo)
    labs = np.array(list(itertools.product(range(box), repeat=6)), dtype=np.int64)
    Vlam = [int(24 * dot(r, lam)) for r in rows]       # 24 V.lam for each shift / Wilson-line row (all integral)
    assert all(F(24) * dot(r, lam) == int(24 * dot(r, lam)) for r in rows)
    out = []
    for e in (0, 1):
        for ti, (k, M) in enumerate(T):
            VL = e * Vlam[0] + sum(kj * Vlam[1 + j] for j, kj in enumerate(k)) + labs @ np.array(Vlam[3:9])
            sig = labs[:, S].sum(axis=1)
            out.append(dict(e=e, ti=ti, M=M, labs=labs, VL=VL, sig=sig))
    return out, T


def nonzero_B(rows, geo, S, lam):
    """count commuting pairs (g, h), h twisted, with B(g,h) != 0 mod 1; also the set of distinct nonzero values (in units of 1/48)"""
    blocks, T = table(rows, geo, S, lam)
    I = np.eye(6, dtype=np.int64)
    cnt, vals = 0, collections.Counter()
    for hb in blocks:
        if hb['ti'] == 0:
            continue                                  # untwisted h: B = 0 (V_h.lam integral, sigma_g V_h.lam/2 ... see note)
        l = hb['M']
        for gb in blocks:
            k = gb['M']
            # rows of hb: f ; rows of gb: m.  commute iff (I - l) m == (I - k) f
            A = gb['labs'] @ (I - l).T                # (I - theta_l) m   for every g
            Bf = hb['labs'] @ (I - k).T               # (I - theta_k) f   for every h
            # match rows exactly: hash vectors
            keyA = collections.defaultdict(list)
            for i, row in enumerate(map(tuple, A)):
                keyA[row].append(i)
            for j, row in enumerate(map(tuple, Bf)):
                gi = keyA.get(row)
                if not gi:
                    continue
                gi = np.array(gi)
                num = (gb['sig'][gi] * hb['VL'][j] - hb['sig'][j] * gb['VL'][gi]) % 48
                nz = num[num != 0]
                cnt += len(nz)
                for v in nz:
                    vals[int(v)] += 1
    return cnt, vals


def diff_relabel(orig, new):
    _, r0 = read(orig); _, r1 = read(new)
    S = [b for b in range(6) if r0[3 + b] != r1[3 + b]]
    lam = [y - x for x, y in zip(r0[3 + S[0]], r1[3 + S[0]])] if S else None
    return r0, S, lam
