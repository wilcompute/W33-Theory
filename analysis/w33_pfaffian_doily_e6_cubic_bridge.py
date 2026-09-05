#!/usr/bin/env python3
"""Explicit Pfaffian-doily truncation of the 27-coordinate E6 Cartan cubic.

This closes the open bridge between the rank-three 15-dimensional Pfaffian
Jordan member and the W33 architecture's 27-dimensional E6 cubic.

There are two exact coordinate cubics:

  Pf_6 = sum over the 15 perfect matchings of six labels.
  C_E6(A,B,C) = det(A)+det(B)+det(C)-tr(ABC).

The first has 15 variables (duads) and 15 monomials (synthemes), hence its
support incidence is the doily GQ(2,2). The second has 27 variables and 45
distinct monomials; its support incidence is GQ(2,4).

This verifier exhibits an explicit signed coordinate embedding of the 15
Pfaffian variables into the 27 trinification variables such that setting the
other 12 E6 variables to zero restricts the E6 Cartan cubic EXACTLY to Pf_6.
No floating point and no graph-isomorphism search is used in the certificate.

Classically, the Pfaffian cubic is the J3(H) / Gr(2,6) Severi member and the
27-dimensional E6 cubic is the J3(O) / Cayley-plane member. The executable
claim here is the stronger coordinate statement above; the Jordan names are
literature interpretation.
"""
from __future__ import annotations

from collections import Counter
import argparse
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pfaffian_doily_e6_cubic_bridge.json"

DUADS = tuple(itertools.combinations(range(6), 2))


def matchings(rem):
    if not rem:
        yield (), 1
        return
    a = rem[0]
    for k in range(1, len(rem)):
        b = rem[k]
        for tail, sign in matchings(rem[1:k] + rem[k + 1:]):
            yield ((a, b),) + tail, sign * ((-1) ** (k - 1))


MATCHINGS = tuple(matchings(tuple(range(6))))
DUAD_INDEX = {d: i for i, d in enumerate(DUADS)}


def pfaffian_terms():
    out = {}
    for matching, sign in MATCHINGS:
        support = tuple(sorted(DUAD_INDEX[tuple(sorted(d))] for d in matching))
        out[support] = sign
    return out


PF = pfaffian_terms()

BLOCKS = "ABC"
E6_POINTS = tuple((block, i, j) for block in BLOCKS for i in range(3) for j in range(3))
E6_INDEX = {p: i for i, p in enumerate(E6_POINTS)}


def perm_sign(p):
    inv = sum(p[i] > p[j] for i in range(3) for j in range(i + 1, 3))
    return -1 if inv % 2 else 1


def e6_terms():
    out = {}
    for block in BLOCKS:
        for perm in itertools.permutations(range(3)):
            support = tuple(sorted(E6_INDEX[(block, i, perm[i])] for i in range(3)))
            if support in out:
                raise AssertionError("determinant support collision")
            out[support] = perm_sign(perm)
    for i, j, k in itertools.product(range(3), repeat=3):
        support = tuple(sorted((
            E6_INDEX[("A", i, j)],
            E6_INDEX[("B", j, k)],
            E6_INDEX[("C", k, i)],
        )))
        if support in out:
            raise AssertionError("trace support collision")
        out[support] = -1
    return out


E6 = e6_terms()

# One explicit doily inside the 27-point GQ(2,4), found once and frozen here.
# Keys are the 15 Pfaffian coordinates x_ij, values are E6 trinification coords.
EMBED = {
    (0, 1): ("A", 0, 0),
    (0, 2): ("C", 2, 2),
    (0, 3): ("C", 1, 2),
    (0, 4): ("A", 0, 2),
    (0, 5): ("B", 1, 0),
    (1, 2): ("B", 2, 1),
    (1, 3): ("B", 2, 2),
    (1, 4): ("C", 0, 1),
    (1, 5): ("A", 2, 0),
    (2, 3): ("A", 1, 1),
    (2, 4): ("B", 0, 1),
    (2, 5): ("C", 2, 0),
    (3, 4): ("B", 0, 2),
    (3, 5): ("C", 1, 0),
    (4, 5): ("A", 2, 2),
}

# y_EMBED[d] = EPS[d] * x_d. With these signs C_E6|_15 = Pf_6 exactly.
NEGATIVE_DUADS = {
    (0, 1), (0, 4), (0, 5), (1, 2), (1, 4), (2, 3), (2, 4)
}
EPS = {d: (-1 if d in NEGATIVE_DUADS else 1) for d in DUADS}


def incidence_checks(npoints, supports, expected_lines_through, expected_collinear_degree,
                     expected_lambda, expected_mu):
    incident = [[] for _ in range(npoints)]
    adj = [[False] * npoints for _ in range(npoints)]
    pair_count = Counter()
    for li, line in enumerate(supports):
        if len(line) != 3 or len(set(line)) != 3:
            return False, {}
        for p in line:
            incident[p].append(li)
        for a, b in itertools.combinations(line, 2):
            a, b = sorted((a, b))
            pair_count[(a, b)] += 1
            adj[a][b] = adj[b][a] = True

    degree_ok = all(len(v) == expected_lines_through for v in incident)
    pair_ok = all(c == 1 for c in pair_count.values())
    graph_degree_ok = all(sum(row) == expected_collinear_degree for row in adj)
    srg_ok = True
    for a, b in itertools.combinations(range(npoints), 2):
        common = sum(adj[a][x] and adj[b][x] for x in range(npoints))
        want = expected_lambda if adj[a][b] else expected_mu
        if common != want:
            srg_ok = False
            break
    gq_ok = True
    for p in range(npoints):
        for line in supports:
            if p in line:
                continue
            if sum(adj[p][q] for q in line) != 1:
                gq_ok = False
                break
        if not gq_ok:
            break
    return all((degree_ok, pair_ok, graph_degree_ok, srg_ok, gq_ok)), {
        "points": npoints,
        "lines": len(supports),
        "linesThroughPoint": sorted({len(v) for v in incident}),
        "collinearityDegree": sorted({sum(row) for row in adj}),
        "pairMultiplicity": sorted(set(pair_count.values())),
        "gqAxiom": gq_ok,
        "srg": [npoints, expected_collinear_degree, expected_lambda, expected_mu],
    }


def build():
    e6_supports = tuple(sorted(E6))
    pf_supports = tuple(sorted(PF))
    e6_gq_ok, e6_stats = incidence_checks(27, e6_supports, 5, 10, 1, 5)
    doily_gq_ok, doily_stats = incidence_checks(15, pf_supports, 3, 6, 1, 3)

    selected = {E6_INDEX[EMBED[d]] for d in DUADS}
    contained = tuple(sorted(line for line in E6 if set(line) <= selected))

    # Translate the 15 contained E6 lines back to duads and compare to synthemes.
    e6_to_duad = {E6_INDEX[EMBED[d]]: DUAD_INDEX[d] for d in DUADS}
    translated = {
        tuple(sorted(e6_to_duad[p] for p in line))
        for line in contained
    }

    coefficient_ok = True
    coefficient_rows = []
    for pf_support, pf_sign in sorted(PF.items()):
        e6_support = tuple(sorted(E6_INDEX[EMBED[DUADS[d]]] for d in pf_support))
        e6_sign = E6.get(e6_support)
        eps_product = 1
        for d in pf_support:
            eps_product *= EPS[DUADS[d]]
        # Substitute y=eps*x into E6: coefficient becomes e6_sign*eps_product.
        restricted_sign = None if e6_sign is None else e6_sign * eps_product
        ok = restricted_sign == pf_sign
        coefficient_ok &= ok
        coefficient_rows.append({
            "duads": [list(DUADS[d]) for d in pf_support],
            "e6Coordinates": [list(EMBED[DUADS[d]]) for d in pf_support],
            "pfaffianCoefficient": pf_sign,
            "restrictedE6Coefficient": restricted_sign,
            "equal": ok,
        })

    # Current W33 sources: the old 9-trit determinant is explicitly superseded
    # by Pass 2660's 27-trit Cartan cubic, while the analysis layer names J3(O).
    source_requirements = {
        "rtl/w33_pass2660_e6_cartan_cubic.sv": [
            "actual E6 Cartan cubic",
            "27 trits",
            "det A + det B + det C - tr(A B C)",
            "Pass 2632's determinant is ONE OF THE FOUR TERMS",
        ],
        "analysis/w33_magic_square_substrate.py": [
            "27 = J3(O)",
            "cubic NORM (determinant)",
        ],
        "tools/compute_e6_cubic_tensor.py": [
            "dimension 27",
            "J3O_determinant",
        ],
    }
    source_checks = {}
    for rel, needles in source_requirements.items():
        path = ROOT / rel
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        source_checks[rel] = path.exists() and all(n in text for n in needles)

    checks = {
        "pfaffian_has_15_variables": len(DUADS) == 15,
        "pfaffian_has_15_distinct_cubic_terms": len(PF) == 15,
        "pfaffian_support_is_doily_GQ_2_2": doily_gq_ok,
        "e6_cartan_has_27_variables": len(E6_POINTS) == 27,
        "e6_cartan_has_45_distinct_cubic_terms": len(E6) == 45,
        "e6_support_is_GQ_2_4": e6_gq_ok,
        "explicit_embedding_selects_15_e6_coordinates": len(selected) == 15,
        "exactly_15_e6_terms_survive_restriction": len(contained) == 15,
        "surviving_supports_are_exactly_the_15_synthemes": translated == set(PF),
        "signed_coordinate_restriction_equals_pfaffian": coefficient_ok,
        "w33_current_sources_own_the_27_coordinate_cubic": all(source_checks.values()),
        "jordan_series_dimensions_match_15_to_27": 3 + 3 * 4 == 15 and 3 + 3 * 8 == 27,
    }

    return {
        "schema": "w33.pfaffian-doily-e6-cubic-bridge.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "pfaffianDoily": {
            "variables": len(DUADS),
            "terms": len(PF),
            "coefficientSigns": dict(Counter(PF.values())),
            "incidence": doily_stats,
            "interpretation": "15 duad variables; each Pfaffian monomial is one syntheme/perfect matching.",
        },
        "e6Trinification": {
            "variables": len(E6_POINTS),
            "terms": len(E6),
            "coefficientSigns": dict(Counter(E6.values())),
            "incidence": e6_stats,
            "formula": "det(A)+det(B)+det(C)-tr(ABC)",
        },
        "restriction": {
            "selectedCoordinates": {
                "%d%d" % d: list(EMBED[d]) for d in DUADS
            },
            "negativePfaffianCoordinates": ["%d%d" % d for d in sorted(NEGATIVE_DUADS)],
            "survivingTerms": len(contained),
            "identity": "C_E6(y)|_{12 unselected coordinates=0, y_embed(d)=eps_d*x_d} = Pf_6(x)",
            "termChecks": coefficient_rows,
        },
        "sourceAudit": source_checks,
        "literatureBoundary": {
            "standardInterpretation": "The 15-dimensional Pfaffian cubic is the J3(H) / Gr(2,6) Severi member; the 27-dimensional E6 cubic is the J3(O) / Cayley-plane member.",
            "finiteGeometry": "The support geometries are GQ(2,2) and GQ(2,4); the former is a distinguished 15-charge truncation of the latter in the E6 black-hole finite-geometry literature.",
            "explicitlyProvedHere": "The two support geometries and the signed coordinate restriction of the 27-coordinate W33 Cartan cubic to the 15-variable Pfaffian cubic.",
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    out = build()
    print(json.dumps(out, indent=2, sort_keys=True))
    if args.write:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    raise SystemExit(0 if out["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
