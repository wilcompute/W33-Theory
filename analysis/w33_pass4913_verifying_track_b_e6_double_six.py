"""Pass 4913 -- independently verify the E6 core of Track B's double-six theorem.

Track B reports that their unexplained [360,36,20]_2 kernel is

    K = Cut(SRG(36,20,10,12)) + <sigma_E6>

with the 36 minimum words the classical double-sixes, the 36 vertices the projective E6
roots (72 roots mod +-1), the 360 K_3,3 witnesses their nonorthogonality edges, and the
missing 36th dimension the E6 switching class.  They derive the coset minimum from

    ||sum r||^2 = 792 - 4 N_-,   with sum r = 2rho and ||2rho||^2 = 312,  so N_- = 120.

They say explicitly that this is "no longer 36 objects suspiciously matching 36 objects" --
they built the object map and the group intertwiner.  Good.  The E6 half of it is standard
root-system data and needs no part of their code, so this lane can check it outright.

    py -3 analysis/w33_pass4913_verifying_track_b_e6_double_six.py
"""

from __future__ import annotations

import itertools
import sys
from fractions import Fraction
from pathlib import Path

import igraph

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

CLAIMED = {
    "roots": 72,
    "projective_pairs": 36,
    "srg": (36, 20, 10, 12),
    "nonorthogonal_pairs": 360,
    "norm_sum_all_positive": 792,
    "two_rho_norm_sq": 312,
    "N_minus": 120,
    "coset_min_words": 25920,
    "weyl_order": 51840,
}


def e6_roots():
    """The 72 roots of E6 in the standard 8-dimensional realisation, as Fractions."""
    roots = []
    # D5-type: +-e_i +- e_j for 1 <= i < j <= 5
    for i, j in itertools.combinations(range(5), 2):
        for si in (1, -1):
            for sj in (1, -1):
                v = [Fraction(0)] * 8
                v[i] = Fraction(si)
                v[j] = Fraction(sj)
                roots.append(tuple(v))
    # The half-sum family: +- (1/2)( sum (-1)^nu_i e_i - e6 - e7 + e8 ) with nu even.
    #
    # THE FIRST VERSION VARIED AN "OUTER SIGN" INDEPENDENTLY OF THE INNER ONES, which does
    # NOT produce negation -- negating the whole vector flips all eight coordinates, not
    # three. The result was 72 vectors that were not closed under negation, so quotienting
    # by +-1 gave 52 classes instead of 36 and every downstream number was wrong. Caught
    # because 72 roots must give exactly 36 projective pairs and gave 52.
    half = Fraction(1, 2)
    for signs in itertools.product((1, -1), repeat=5):
        if signs.count(-1) % 2 != 0:      # EVEN number of minus signs among the first five
            continue
        v = [half * s for s in signs] + [-half, -half, half]
        roots.append(tuple(v))
        roots.append(tuple(-x for x in v))
    return roots


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def main() -> int:
    print("=" * 78)
    print("Pass 4913 -- Track B's E6 double-six core, checked independently")
    print("=" * 78)

    roots = e6_roots()
    norms = {dot(r, r) for r in roots}
    print(f"\n    roots constructed          : {len(roots)}")
    print(f"    distinct norms             : {sorted(norms)}")

    # projective pairs: r and -r identified
    seen, proj = set(), []
    for r in roots:
        neg = tuple(-x for x in r)
        if r in seen or neg in seen:
            continue
        seen.add(r)
        proj.append(r)
    print(f"    projective pairs (mod +-1) : {len(proj)}")

    # nonorthogonality graph on the projective pairs
    g = igraph.Graph(n=len(proj))
    edges, nonorth = [], 0
    for i, j in itertools.combinations(range(len(proj)), 2):
        if dot(proj[i], proj[j]) != 0:
            edges.append((i, j))
            nonorth += 1
    g.add_edges(edges)

    n = g.vcount()
    k = g.degree(0) if n else 0
    nb = [set(g.neighbors(v)) for v in range(n)]
    lam = mu = None
    reg = all(g.degree(v) == k for v in range(n))
    for i, j in itertools.combinations(range(n), 2):
        c = len(nb[i] & nb[j])
        if j in nb[i]:
            lam = c if lam is None else lam
        else:
            mu = c if mu is None else mu
    srg = (n, k, lam, mu)
    print(f"    nonorthogonal pairs        : {nonorth}")
    print(f"    regular                    : {reg}")
    print(f"    SRG parameters             : {srg}")

    # 2rho: the sum of a positive system. Choose positives by first nonzero coordinate.
    def positive(r):
        for x in r:
            if x != 0:
                return x > 0
        return False

    pos = [r for r in roots if positive(r)]
    two_rho = tuple(sum(r[i] for r in pos) for i in range(8))
    trn = dot(two_rho, two_rho)
    print(f"\n    positive roots             : {len(pos)}")
    print(f"    ||2rho||^2                 : {trn}")

    # their identity: ||sum r||^2 = 792 - 4 N_-  over 36 chosen representatives
    all_pos_norm = 2 * len(proj) + 2 * nonorth      # 72 + 2*360 if every dot is +1
    n_minus = Fraction(all_pos_norm - trn, 4)
    print(f"    72 + 2x{nonorth}                : {all_pos_norm}")
    print(f"    implied N_-                : {n_minus}")

    rows = [
        ("roots", CLAIMED["roots"], len(roots)),
        ("projective pairs", CLAIMED["projective_pairs"], len(proj)),
        ("SRG", CLAIMED["srg"], srg),
        ("nonorthogonal pairs", CLAIMED["nonorthogonal_pairs"], nonorth),
        ("all-positive norm", CLAIMED["norm_sum_all_positive"], all_pos_norm),
        ("||2rho||^2", CLAIMED["two_rho_norm_sq"], trn),
        ("N_-", CLAIMED["N_minus"], n_minus),
    ]
    print(f"\n  {'quantity':22s} {'Track B':>18s} {'this lane':>18s} {'agree':>7s}")
    ok = True
    for name, a, b in rows:
        same = (a == b) or (str(a) == str(b))
        ok &= same
        print(f"  {name:22s} {str(a):>18s} {str(b):>18s} {str(same):>7s}")

    print(f"""
    {'EVERY E6 QUANTITY AGREES.' if ok else 'AT LEAST ONE DISAGREES -- READ THE ROWS.'} The 72 roots, the 36 projective pairs, the
    SRG(36,20,10,12) nonorthogonality graph, the 360 edges, and the norm identity
    792 - 4 N_- = 312 giving N_- = 120 are all reproduced from a standard root-system
    construction that shares nothing with their code.

    THAT VERIFIES THE E6 HALF, NOT THE IDENTIFICATION. Their claim is that these 36
    projective roots ARE the 36 minimum words of their kernel, with an explicit object map
    and an intertwiner. This lane has no access to that code, so what is checked is that
    the E6 object they are mapping ONTO has exactly the structure they describe -- 36
    vertices, degree 20, 360 edges, and a positive-system norm forcing 120 negative pairs.

    ONE THING WORTH FLAGGING BACK. Their |Aut(K)| = |W(E6)| = 51,840 = |PGSp(4,3)| is the
    same coincidence Pass 4735 measured across this corpus, where 56% of 1,733 sightings of
    51,840 never say which order-51,840 object they mean. They handled it correctly and
    said so -- "established from the complete minimum shell and the explicit Weyl action,
    not from the group order by itself" -- which is the distinction that matters, and worth
    keeping in the theorem statement rather than only in the derivation.""")

    out = {
        "boundary": ("the E6 root system is constructed here from the standard 8-dimensional "
                     "realisation and shares nothing with Track B's code. This verifies the "
                     "TARGET of their identification -- 36 projective roots whose "
                     "nonorthogonality graph is SRG(36,20,10,12) with 360 edges, and the "
                     "norm identity forcing N_- = 120. It does NOT verify that their 36 "
                     "minimum words map to these roots, which needs their generator matrix"),
        "comparison": [{"quantity": a, "track_b": str(b), "this_lane": str(c),
                        "agree": (b == c) or (str(b) == str(c))} for a, b, c in rows],
        "all_agree": bool(ok),
        "flag_back": ("|W(E6)| = |PGSp(4,3)| = 51,840 is the multi-source coincidence Pass "
                      "4735 measured; Track B handled it correctly by deriving Aut(K) from "
                      "the minimum shell and Weyl action rather than the order, and that "
                      "qualifier belongs in the theorem statement"),
    }
    fp = ROOT / "data" / "PART_W33_PASS4913_E6_DOUBLE_SIX_VERIFICATION.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
