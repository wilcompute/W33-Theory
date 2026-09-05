#!/usr/bin/env python3
"""All 36 double-sixes cut exact signed Pfaffian cubics from the E6 Cartan cubic.

The earlier bridge froze one 15-coordinate doily and one sign gauge.  Here the
36 cubic-surface double-sixes are reconstructed, and every complement is
handled independently.

For each double-six D:
  * its 15-line complement is labelled by the 15 duads of a six-set;
  * the 15 Cartan-cubic terms supported entirely on the complement are exactly
    the 15 synthemes/perfect matchings;
  * a 15-variable GF(2) sign system is solved exactly so that the restricted
    E6 coefficient of every syntheme equals the Pfaffian coefficient;
  * the sign-system rank is 10, leaving the expected five local sign-gauge
    freedoms; a canonical free-bits-zero representative is emitted.

Thus all 36 complements are literal signed coordinate restrictions
C_E6|_D = Pf_6, not merely GQ(2,2) support copies.
"""
from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

import networkx as nx

from w33_pass4992_4999_common import build_base
from w33_pfaffian_doily_e6_cubic_bridge import DUADS, DUAD_INDEX, PF, E6, E6_POINTS, E6_INDEX

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_all36_pfaffian_double_six_sections.json"


def e6_graph() -> nx.Graph:
    G = nx.Graph()
    G.add_nodes_from(range(27))
    for line in E6:
        for a, b in itertools.combinations(line, 2):
            G.add_edge(a, b)
    return G


def gf2_solve(rows: list[int], rhs: list[int], n: int) -> tuple[list[int], int]:
    """RREF over F2, free variables fixed to zero; fail on inconsistency."""
    A = [(int(r), int(b) & 1) for r, b in zip(rows, rhs)]
    pivots: list[int] = []
    r = 0
    for c in range(n):
        p = next((i for i in range(r, len(A)) if (A[i][0] >> c) & 1), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        pr, pb = A[r]
        for i in range(len(A)):
            if i != r and ((A[i][0] >> c) & 1):
                A[i] = (A[i][0] ^ pr, A[i][1] ^ pb)
        pivots.append(c)
        r += 1
    for mask, b in A:
        if mask == 0 and b:
            raise AssertionError("inconsistent sign system")
    x = [0] * n
    # RREF means each pivot row has no other pivot variables; free bits are zero.
    for i, c in enumerate(pivots):
        x[c] = A[i][1]
    return x, len(pivots)


def build_sections() -> tuple[dict, dict]:
    base = build_base()
    Ge = e6_graph()
    assert Ge.number_of_nodes() == 27 and Ge.number_of_edges() == 135
    phi = next(nx.algorithms.isomorphism.GraphMatcher(Ge, base["G27"]).isomorphisms_iter())
    invphi = {v: k for k, v in phi.items()}
    assert len(phi) == 27 and len(invphi) == 27

    records = []
    all_selected = []
    all_surviving = []
    rank_counter = Counter()
    negative_counter = Counter()

    for dsi, D in enumerate(base["DS"]):
        H = base["G27"].subgraph(D)
        assert nx.is_bipartite(H)
        color = nx.algorithms.bipartite.color(H)
        classes = [sorted(v for v in D if color[v] == c) for c in sorted(set(color.values()))]
        assert sorted(map(len, classes)) == [6, 6]
        # Deterministic side choice; swapping sides changes only local S6 gauge.
        A = min(classes)

        complement = sorted(set(range(27)) - set(D))
        assert len(complement) == 15
        base_to_duad = {}
        for v in complement:
            meets = tuple(i for i, a in enumerate(A) if base["G27"].has_edge(v, a))
            assert len(meets) == 2
            base_to_duad[v] = tuple(sorted(meets))
        assert set(base_to_duad.values()) == set(DUADS)

        embed = {d: invphi[v] for v, d in base_to_duad.items()}
        assert len(set(embed.values())) == 15
        selected = frozenset(embed.values())
        contained = {line: coeff for line, coeff in E6.items() if set(line) <= selected}
        assert len(contained) == 15

        e6_to_duad_index = {embed[d]: DUAD_INDEX[d] for d in DUADS}
        translated = {
            tuple(sorted(e6_to_duad_index[p] for p in line)): coeff
            for line, coeff in contained.items()
        }
        assert set(translated) == set(PF)

        rows, rhs = [], []
        term_rows = []
        for pf_support, pf_coeff in sorted(PF.items()):
            e6_support = tuple(sorted(embed[DUADS[i]] for i in pf_support))
            e6_coeff = E6[e6_support]
            mask = sum(1 << i for i in pf_support)
            need = 0 if e6_coeff == pf_coeff else 1
            rows.append(mask)
            rhs.append(need)
        bits, srank = gf2_solve(rows, rhs, 15)
        assert srank == 10
        eps = {DUADS[i]: (-1 if bits[i] else 1) for i in range(15)}

        for pf_support, pf_coeff in sorted(PF.items()):
            e6_support = tuple(sorted(embed[DUADS[i]] for i in pf_support))
            e6_coeff = E6[e6_support]
            ep = 1
            for i in pf_support:
                ep *= eps[DUADS[i]]
            restricted = e6_coeff * ep
            assert restricted == pf_coeff
            term_rows.append({
                "duads": ["%d%d" % DUADS[i] for i in pf_support],
                "pfaffianCoefficient": pf_coeff,
                "e6CoefficientBeforeSigns": e6_coeff,
                "restrictedE6Coefficient": restricted,
            })

        negatives = ["%d%d" % d for d in DUADS if eps[d] < 0]
        rank_counter[srank] += 1
        negative_counter[len(negatives)] += 1
        all_selected.append(selected)
        all_surviving.extend(contained)
        records.append({
            "doubleSixIndex": dsi,
            "doubleSixE6Coordinates": [list(E6_POINTS[invphi[v]]) for v in sorted(D)],
            "sectionCoordinates": [list(E6_POINTS[i]) for i in sorted(selected)],
            "duadToE6Coordinate": {"%d%d" % d: list(E6_POINTS[embed[d]]) for d in DUADS},
            "negativeDuadsCanonicalGauge": negatives,
            "signEquationRank": srank,
            "signGaugeDimension": 15 - srank,
            "survivingTerms": 15,
            "supportsAreExactlySynthemes": True,
            "signedRestrictionEqualsPfaffian": True,
            "termChecks": term_rows,
        })

    point_mult = Counter(p for S in all_selected for p in S)
    term_mult = Counter(all_surviving)
    assert len(records) == 36 and len(set(all_selected)) == 36
    assert set(point_mult.values()) == {20}
    assert len(point_mult) == 27
    assert set(term_mult.values()) == {12}
    assert len(term_mult) == 45

    summary = {
        "sections": 36,
        "uniqueSections": len(set(all_selected)),
        "sectionSize": 15,
        "survivingTermsPerSection": 15,
        "signEquationRankDistribution": {str(k): v for k, v in sorted(rank_counter.items())},
        "signGaugeDimension": 5,
        "canonicalNegativeCountDistribution": {str(k): v for k, v in sorted(negative_counter.items())},
        "sectionsThroughEachE6Coordinate": 20,
        "sectionsContainingEachE6CubicTerm": 12,
    }
    return summary, {"phiE6ToBaseG27": {str(k): int(v) for k, v in phi.items()}, "records": records}


def build() -> dict:
    summary, detail = build_sections()
    checks = {
        "all_36_double_sixes_checked": summary["sections"] == 36,
        "all_36_sections_distinct": summary["uniqueSections"] == 36,
        "all_sections_have_15_coordinates": summary["sectionSize"] == 15,
        "all_sections_have_15_surviving_terms": summary["survivingTermsPerSection"] == 15,
        "all_sign_systems_have_rank_10": summary["signEquationRankDistribution"] == {"10": 36},
        "all_sections_have_five_sign_gauge_bits": summary["signGaugeDimension"] == 5,
        "every_E6_coordinate_lies_in_20_sections": summary["sectionsThroughEachE6Coordinate"] == 20,
        "every_E6_cubic_term_lies_in_12_sections": summary["sectionsContainingEachE6CubicTerm"] == 12,
        "all_supports_are_doily_synthemes": all(r["supportsAreExactlySynthemes"] for r in detail["records"]),
        "all_signed_restrictions_equal_pfaffian": all(r["signedRestrictionEqualsPfaffian"] for r in detail["records"]),
    }
    assert all(checks.values())
    return {
        "schema": "w33.all36-pfaffian-double-six-sections.v1",
        "status": "PASS",
        "checks": checks,
        "summary": summary,
        "coordinateIsomorphism": detail["phiE6ToBaseG27"],
        "sections": detail["records"],
        "identity": "for every double-six D, there is an explicit signed coordinate gauge on its 15-point complement S_D with C_E6|_{S_D} = Pf_6",
        "gaugeBoundary": "Each local sign system has five free bits. The emitted free-bits-zero signs are a deterministic gauge choice, not a canonical PSp-invariant orientation.",
        "theorem": "The 36 Schlaefli double-sixes are exactly 36 explicit Pfaffian/doily linear sections of the committed 27-coordinate E6 Cartan cubic, coefficient-by-coefficient.",
        "boundary": "Exact finite cubic/support statement. The Jordan/Severi naming is classical interpretation; no physical consequence is inferred here.",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    out = build()
    if args.write:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": out["status"], "summary": out["summary"]}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
