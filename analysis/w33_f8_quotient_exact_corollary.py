"""Pass 12672: the Pass 12671 exact witness also gives EXACT bounds (47 - 32cos(2pi/9))/9 for both five-qubit quotient 9-sets.
Replays the other track's quotient objective (analysis/toe_20261114_regulus_quotient_witness.py, labels (x,z) in the determinant /
trace-pairing convention, shortening Paulis (12,51) [det 1, type 27] and (57,34) [det 3, type 17]) on the exact expectations of
data/w33_f8_exact_witness.json, in exact arithmetic over Q(g, sqrt3), g = 2cos(2pi/9).
Convention map: their operator on site y is i^{Tr det(x,z)} (-1)^{Tr det(y^x, z)} psi[y^x]; Tr det(y, z) = v.y with
v_i = Tr det(e_i, z), so it is a phase times this repo's P(x, v); squared expectations agree.  usage: py -3 analysis/w33_f8_quotient_exact_corollary.py"""
import json, os
from fractions import Fraction as Fr
from itertools import product
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)


def multiply(a, b):
    r = 0
    while b:
        if b & 1: r ^= a
        b >>= 1; a <<= 1
        if a & 8: a ^= 0b1011
    return r


def trace(a):
    s = multiply(a, a); return a ^ s ^ multiply(s, s)


det = lambda x, z: multiply(x & 7, z & 7) ^ multiply(x >> 3, z >> 3)
vmap = lambda z: sum(trace(det(1 << i, z)) << i for i in range(6))


def kmul(x, y):  # (a + b s)(c + d s), a..d in Q(g), g^3 = 3g - 1, s^2 = 3
    def qg(p, r):
        c = [Fr(0)] * 5
        for i in range(3):
            for j in range(3): c[i + j] += p[i] * r[j]
        c[2] += 3 * c[4]; c[1] -= c[4]; c[1] += 3 * c[3]; c[0] -= c[3]
        return c[:3]
    a, b, c, d = x[:3], x[3:], y[:3], y[3:]
    ac, bd, ad, bc = qg(a, c), qg(b, d), qg(a, d), qg(b, c)
    return [ac[i] + 3 * bd[i] for i in range(3)] + [ad[i] + bc[i] for i in range(3)]


W = json.load(open(os.path.join(ROOT, "data", "w33_f8_exact_witness.json")))
r = {tuple(map(int, k.split(","))): [Fr(c) for c in v] for k, v in W["expectations"].items()}
zero = [Fr(0)] * 6
sq = lambda x, z: kmul(r.get((x, vmap(z)), zero), r.get((x, vmap(z)), zero))
add = lambda p, q: [a + b for a, b in zip(p, q)]
covered = [(x, z) for x, z in product(range(64), repeat=2) if (x or z) and not det(x, z)]
assert len(covered) == 567
parent = zero
for x, z in covered: parent = add(parent, sq(x, z))
target = [Fr(47, 9), Fr(-16, 9)] + [Fr(0)] * 4
print("parent 64F from the other track's covered set (exact):", [str(v) for v in parent[:3]], parent == target)
res = dict(parent=[str(v) for v in parent], parent_equals_closed_form=parent == target, quotients={})
for (x, z) in [(12, 51), (57, 34), (53, 17)]:
    s = sq(x, z)
    is_stab = s == [Fr(1)] + [Fr(0)] * 5
    dd = det(x, z)
    if not trace(dd):
        res["quotients"][f"{x},{z}"] = dict(determinant=dd, trace=0, stabilises=is_stab, note="trace 0: not a shortening point"); continue
    reps = set(); restricted = zero; anti_nonzero = 0
    for a, b in covered:
        if trace(det(a, z) ^ det(x, b)):
            if sq(a, b) != zero: anti_nonzero += 1
            continue
        coset = min(a | (b << 6), (a ^ x) | ((b ^ z) << 6))
        assert coset not in reps; reps.add(coset)
        restricted = add(restricted, sq(a, b))
    ok = is_stab and anti_nonzero == 0 and len(reps) == 279 and restricted == parent
    res["quotients"][f"{x},{z}"] = dict(determinant=dd, type=27 if dd == 1 else 17, stabilises=is_stab, anticommuting_nonzero=anti_nonzero,
                                         quotient_covered=len(reps), restricted=[str(v) for v in restricted], equals_parent=ok)
    print((x, z), "det", dd, "stabilised", is_stab, "quotient reps", len(reps), "restricted == parent exactly:", ok)
res["both_quotients_exact"] = all(q.get("equals_parent") for q in res["quotients"].values() if q.get("trace") != 0)
print("both five-qubit quotient types: exact scaled value (47 - 32cos(2pi/9))/9:", res["both_quotients_exact"])
json.dump(res, open(os.path.join(ROOT, "data", "w33_f8_quotient_exact_corollary.json"), "w"), indent=1)
