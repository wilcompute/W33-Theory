"""Why this matter?  Brute force over chiral gauge theories SU(N) x SU(2) x U(1): left-handed Weyl multiplets of types Q (N,2), u (Nbar,1), f (N,1), L (1,2), e (1,1), integer charges |Y| <= Ymax.  Conditions: SU(N)^3, SU(N)^2 U(1), SU(2)^2 U(1), U(1)^3, gravity^2 U(1), Witten (even number of doublets).  Chirality: no multiplet may pair with another into a gauge-invariant mass term (no vector-like pair, no neutral singlet), and all charges non-zero.  Control: the SM generation (1, -4, 2, -3, 6) must appear at N = 3.
Questions: the smallest anomaly-free chiral theory that has both a bifundamental and a singlet-of-SU(2) coloured fermion, for each N; whether it is unique up to overall charge scale; does Witten pick odd N; do all fermions get mass from one Higgs doublet.  Then purely abelian and SU(2) x U(1) theories for comparison.  usage: py -3 anomaly_enum.py"""
import itertools
import json
from fractions import Fraction
from math import gcd


def anomalies(N, nQ, us, fs, Ls, es, Qs):
    # SU(N)^3: each Q is 2 fundamentals (+1 each), f fundamental (+1), u antifundamental (-1)
    su3 = 2 * nQ + len(fs) - len(us) if N >= 3 else 0
    if su3:
        return False
    # SU(N)^2 U(1): sum over fundamentals of multiplicity * Y
    if 2 * sum(Qs) + sum(us) + sum(fs) != 0:
        return False
    # SU(2)^2 U(1)
    if N * sum(Qs) + sum(Ls) != 0:
        return False
    # gravity
    if 2 * N * sum(Qs) + N * sum(us) + N * sum(fs) + 2 * sum(Ls) + sum(es) != 0:
        return False
    # U(1)^3
    if 2 * N * sum(q ** 3 for q in Qs) + N * sum(u ** 3 for u in us) + N * sum(x ** 3 for x in fs) + 2 * sum(L ** 3 for L in Ls) + sum(e ** 3 for e in es) != 0:
        return False
    # Witten: number of SU(2) doublets
    if (N * nQ + len(Ls)) % 2:
        return False
    return True


def chiral(us, fs, Ls, es):
    if any(u + x == 0 for u in us for x in fs):
        return False
    if any(a + b == 0 for a, b in itertools.combinations(Ls, 2)):
        return False
    if any(a + b == 0 for a, b in itertools.combinations(es, 2)):
        return False
    return True


def primitive(t):
    vals = [abs(v) for v in t if v]
    g = 0
    for v in vals:
        g = gcd(g, v)
    return g == 1


def one_higgs_gives_all_mass(Qs, us, fs, Ls, es, H):
    """Yukawas Q u H, Q u H*, L e H, L e H*, and bare invariants: does each field appear in some allowed coupling?"""
    used = set()
    for a in range(len(Qs)):
        for b, u in enumerate(us):
            if Qs[a] + u + H == 0 or Qs[a] + u - H == 0:
                used.add(("Q", a))
                used.add(("u", b))
    for a, L in enumerate(Ls):
        for b, e in enumerate(es):
            if L + e + H == 0 or L + e - H == 0:
                used.add(("L", a))
                used.add(("e", b))
    return len(used) == len(Qs) + len(us) + len(Ls) + len(es)


out = {}
results = {}
YM = 12
for N in (3, 4, 5, 6, 7):
    sols = []
    # one Q, two antifundamentals (forced by SU(N)^3 at N >= 3), up to 2 doublets, up to 2 singlets: the smallest shape
    for nL, ne in ((0, 0), (0, 1), (1, 0), (1, 1), (1, 2), (2, 1), (2, 2)):
        rng = [y for y in range(-YM, YM + 1) if y]
        for q in rng:
            for u1, u2 in itertools.combinations_with_replacement(rng, 2):
                if 2 * q + u1 + u2:
                    continue
                for Ls in itertools.combinations_with_replacement(rng, nL):
                    if N * q + sum(Ls):
                        continue
                    for es in itertools.combinations_with_replacement(rng, ne):
                        if not anomalies(N, 1, [u1, u2], [], list(Ls), list(es), [q]):
                            continue
                        if not chiral([u1, u2], [], list(Ls), list(es)):
                            continue
                        t = (q, u1, u2) + tuple(Ls) + tuple(es)
                        if not primitive(t) or q < 0:
                            continue
                        weyl = 2 * N + 2 * N + 2 * nL + ne
                        H = [h for h in rng if one_higgs_gives_all_mass([q], [u1, u2], [], list(Ls), list(es), h)]
                        sols.append(dict(q=q, u=(u1, u2), L=Ls, e=es, weyl=weyl, higgs=H[:4]))
    sols.sort(key=lambda s: (s["weyl"], abs(s["q"])))
    results[N] = dict(count=len(sols), smallest=sols[:6], smallest_weyl=sols[0]["weyl"] if sols else None)
    print(N, results[N]["count"], sols[:3], flush=True)
out["bifundamental_shape_by_N"] = results
sm = [s for s in results[3]["smallest"] if sorted(map(abs, [s["q"], *s["u"], *s["L"], *s["e"]])) == [1, 2, 3, 4, 6]]
out["control_SM_found"] = bool(sm)
# is the SM shape unique at N = 3?  With Q + 2 u + L + e the anomaly equations have a one-parameter solution up to scale, tested on the grid
s3 = [s for s in results[3]["smallest"] if len(s["L"]) == 1 and len(s["e"]) == 1]
all3 = results[3]
print(json.dumps({k: v for k, v in out.items() if k != "bifundamental_shape_by_N"}))
# abelian theories for comparison: smallest chiral U(1)-only sets
ab = {}
for n in range(2, 7):
    found = []
    for t in itertools.combinations_with_replacement([y for y in range(-9, 10) if y], n):
        if sum(t) or sum(y ** 3 for y in t):
            continue
        if any(a + b == 0 for a, b in itertools.combinations(t, 2)):
            continue
        if primitive(t):
            found.append(t)
    ab[n] = dict(count=len(found), sample=found[:3])
    print("abelian", n, ab[n], flush=True)
out["abelian_chiral"] = ab
json.dump(out, open("anomaly_enum.json", "w"), indent=1, default=str)
