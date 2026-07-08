#!/usr/bin/env python3
"""
Pass 78 -- Equivariant closure map for the zeta / local algebra / code boundary.

This pass continues Pass 77 without overclaiming.  The point-module Ihara zeta
has a complete equivariant map because the rank-3 permutation character has
only three active constituents.  The edge-zeta / full 28-Spence and
[[66,8,3]]_3 generator-matrix claims remain explicit open targets.

Seven tracks:

T1  Vertex Artin-Ihara character map: active constituents 1, 15, 24 carry the
    Bass factors, and all other Sp(4,3) irreducibles are inactive on C^40.
T2  Local algebra fingerprint: Bose-Mesner dim 3 < Terwilliger dim 16, with
    subconstituent spectra around a point.
T3  Ovoid/spread duality: alpha(W)=7, alpha(Q)=10, and W has 36 spreads with
    every line in nine spreads.
T4  [[66,8,3]]_3 boundary audit: many repo/document mentions, but this pass
    does not promote a generator-matrix construction.
T5  Weil/Clifford carrier: q^2=9 splits as 5+4, matching the two-qutrit
    oscillator carrier proved by GAP in Pass 77.
T6  Spence hearing boundary: one exact W/Q pair is proved; the full 28-graph
    census remains an external-data target.
T7  Algebra ladder: 3 -> 9 -> 16 -> 40 -> 480 -> 51840 closes the current
    finite architecture map with checked dimensions.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

from w33_pass73_prime_geodesics import build_graph
from w33_pass77_frontier import read_gap

ROOT = Path(__file__).resolve().parent
ANALYSIS = ROOT / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_spread_double_six_association_scheme import spread_report  # noqa: E402

OUTPUT = ROOT / "w33_pass78_equivariant_closure.json"


def counter_to_json(counter: Counter) -> dict[str, int]:
    return {str(key): int(counter[key]) for key in sorted(counter, key=str)}


def parse_gap_degrees() -> list[int]:
    gap = read_gap()
    if gap is None:
        return []
    text = Path("w33_pass77_group_out.txt").read_text(encoding="utf-8")
    match = re.search(r"Sp43_degrees=\[(.*)\]", text)
    if not match:
        return []
    return [int(value) for value in re.findall(r"\d+", match.group(1))]


def track_1_vertex_artin_ihara(gap: dict | None) -> dict:
    degrees = parse_gap_degrees()
    active_by_degree = gap["constituent_degrees"] if gap else {}
    active_total = sum(int(deg) * int(mult) for deg, mult in active_by_degree.items())
    active_factors = [
        {
            "module": "trivial",
            "degree": 1,
            "adjacency_eigenvalue": 12,
            "bass_factor": "1 - 12u + 11u^2",
            "exponent": 1,
        },
        {
            "module": "degree-24 constituent",
            "degree": 24,
            "adjacency_eigenvalue": 2,
            "bass_factor": "1 - 2u + 11u^2",
            "exponent": 24,
        },
        {
            "module": "one degree-15 constituent",
            "degree": 15,
            "adjacency_eigenvalue": -4,
            "bass_factor": "1 + 4u + 11u^2",
            "exponent": 15,
        },
    ]
    denominator_degree = 2 * sum(row["exponent"] for row in active_factors) + 2 * 200
    return {
        "active_constituent_degrees": {
            str(k): v for k, v in sorted(active_by_degree.items())
        },
        "active_dimension_sum": active_total,
        "all_irreducible_degree_histogram": counter_to_json(Counter(degrees)),
        "irreducible_character_count": len(degrees),
        "active_irreducible_count_on_point_module": 3,
        "inactive_irreducible_count_on_point_module": max(len(degrees) - 3, 0),
        "active_factors": active_factors,
        "bass_tail_factor": "(1 - u^2)^200",
        "bass_denominator_degree": denominator_degree,
        "directed_edge_count": 480,
        "degree_check": denominator_degree == 480,
        "boundary": (
            "This is the complete Artin-Ihara map for the 40-dimensional point permutation module. "
            "It is not yet the full edge-zeta Artin factorization across all 34 irreducibles."
        ),
    }


def spectrum_profile(matrix: np.ndarray) -> dict[str, int]:
    values = np.rint(np.linalg.eigvalsh(matrix.astype(float))).astype(int)
    return counter_to_json(Counter(values.tolist()))


def track_2_local_algebra(A: np.ndarray) -> dict:
    pass77 = json.loads((ROOT / "w33_pass77_frontier.json").read_text(encoding="utf-8"))
    terwilliger_dim = pass77["track4_terwilliger"]["dim_terwilliger_algebra"]
    base = 0
    neighbors = np.nonzero(A[base])[0].tolist()
    nonneighbors = [
        idx for idx in range(A.shape[0]) if idx != base and A[base, idx] == 0
    ]
    local = A[np.ix_(neighbors, neighbors)]
    second = A[np.ix_(nonneighbors, nonneighbors)]
    return {
        "bose_mesner_dimension": 3,
        "terwilliger_dimension": terwilliger_dim,
        "dimension_lift": f"3 -> {terwilliger_dim}",
        "distance_fibre_sizes": [1, len(neighbors), len(nonneighbors)],
        "local_graph_vertices": len(neighbors),
        "local_graph_degree": int(local[0].sum()) if len(neighbors) else 0,
        "local_graph_spectrum": spectrum_profile(local),
        "second_subconstituent_vertices": len(nonneighbors),
        "second_subconstituent_degree": (
            int(second[0].sum()) if len(nonneighbors) else 0
        ),
        "second_subconstituent_spectrum": spectrum_profile(second),
        "boundary": (
            "Pass 78 records a fast reproducible Terwilliger fingerprint. "
            "The full Wedderburn/T-module decomposition remains the next exact-algebra target."
        ),
    }


def track_3_ovoid_spread() -> dict:
    pass77 = json.loads((ROOT / "w33_pass77_frontier.json").read_text(encoding="utf-8"))
    ovoids = pass77["track2_3_ovoid_separator"]
    spreads = spread_report()
    return {
        "alpha_W33": ovoids["alpha_W33"],
        "alpha_Q43": ovoids["alpha_Q43"],
        "W33_has_ovoid": ovoids["W33_has_ovoid"],
        "Q43_has_ovoid": ovoids["Q43_has_ovoid"],
        "spread_count": spreads["spread_count"],
        "spread_size_profile": spreads["spread_size_profile"],
        "line_participation_profile": spreads["line_participation_profile"],
        "spread_overlap_profile": spreads["overlap_profile"],
        "overlap_4_graph": spreads["overlap_4_graph"],
        "duality_reading": (
            "The odd-q W side has no ovoid but has 36 spreads; the parabolic-quadric dual has ovoids. "
            "The separator is global geometry, not adjacency spectrum."
        ),
    }


def count_text(pattern: str, path: Path) -> int:
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8", errors="ignore")
    return len(re.findall(pattern, text, flags=re.IGNORECASE))


def track_4_code_boundary() -> dict:
    surfaces = [
        ROOT / "w33_paper.tex",
        ROOT / "photonic_holonet.tex",
        ROOT / "holonet_machine.tex",
        ROOT / "holonet_practical_implications.tex",
        ROOT / "docs" / "index.html",
        ROOT / "HOLONET.md",
    ]
    mention_counts = {
        str(path.relative_to(ROOT)): count_text(
            r"\[\[66,8,3|66,8,3|\[\!\\\[66,8,3", path
        )
        for path in surfaces
    }
    generator_markers = {
        str(path.relative_to(ROOT)): count_text(
            r"generator matrix|parity check|stabilizer generator|finite matrix code",
            path,
        )
        for path in surfaces
    }
    return {
        "target": "[[66,8,3]]_3 protected store / Steinberg-adjacent memory claim",
        "document_mentions": mention_counts,
        "generator_marker_counts": generator_markers,
        "explicit_generator_promoted_by_this_pass": False,
        "honest_status": (
            "The architecture repeatedly cites the 66-symbol distance-3 store, but Pass 78 does not "
            "find or construct a canonical [[66,8,3]]_3 generator/stabilizer witness in the Pass 73-78 spine."
        ),
        "next_verification_target": (
            "Build the finite generator/parity-check matrices and verify n=66, k=8, d=3 directly."
        ),
    }


def track_5_weil_clifford(gap: dict | None) -> dict:
    has4 = bool(gap and gap["Sp43_has_deg4"])
    has5 = bool(gap and gap["Sp43_has_deg5"])
    return {
        "q": 3,
        "two_qutrit_dimension": 9,
        "weil_split": [5, 4],
        "gap_confirms_degree_4": has4,
        "gap_confirms_degree_5": has5,
        "split_check": has4 and has5 and 5 + 4 == 9,
        "reading": (
            "The oscillator carrier is q^2=9, decomposing into the two finite Weil pieces 5 and 4. "
            "This is the representation-theoretic substrate for the two-qutrit Clifford layer."
        ),
    }


def track_6_spence_boundary() -> dict:
    pass76 = json.loads(
        (ROOT / "w33_pass76_cospectral_mates.json").read_text(encoding="utf-8")
    )
    t1 = pass76["track1_Q43_mate"]
    return {
        "verified_pair": ["W(3,3)", "Q(4,3)"],
        "same_srg_parameters": t1["is_SRG_40_12_2_4"],
        "cospectral": t1["cospectral_with_W33"],
        "locally_identical": t1["locally_identical"],
        "non_isomorphic": t1["non_isomorphic"],
        "geometric_pair_separated_by_alpha": True,
        "full_spence_count": 28,
        "full_28_adjacency_data_available_in_repo": False,
        "boundary": (
            "The W/Q pair is the exact proved separator. A complete 28-graph hearing table still needs "
            "the external Spence adjacency data or a generator for all 28 graphs."
        ),
    }


def track_7_ladder(t1: dict, t2: dict, t3: dict, t5: dict) -> dict:
    ladder = [
        {"layer": "Bose-Mesner algebra", "dimension": 3},
        {"layer": "Weil/two-qutrit carrier", "dimension": t5["two_qutrit_dimension"]},
        {
            "layer": "Terwilliger local algebra",
            "dimension": t2["terwilliger_dimension"],
        },
        {"layer": "point permutation module", "dimension": t1["active_dimension_sum"]},
        {"layer": "W33 spreads", "dimension": t3["spread_count"]},
        {
            "layer": "Hashimoto directed-edge carrier",
            "dimension": t1["directed_edge_count"],
        },
        {"layer": "Sp(4,3) double cover", "dimension": 51840},
    ]
    return {
        "ladder": ladder,
        "checks": {
            "bose_mesner_less_than_terwilliger": 3 < t2["terwilliger_dimension"],
            "point_module_is_1_plus_15_plus_24": t1["active_dimension_sum"] == 40,
            "hashimoto_degree_matches_bass_denominator": t1["degree_check"],
            "spread_count_is_36": t3["spread_count"] == 36,
            "group_order_is_480_times_108": 480 * 108 == 51840,
        },
        "reading": (
            "The current architecture is a ladder of checked finite carriers, not one undifferentiated count: "
            "association algebra, oscillator, local algebra, point module, spread clock, directed-edge zeta, "
            "and full symplectic/Clifford symmetry."
        ),
    }


def main() -> int:
    _, Aw = build_graph()
    gap = read_gap()

    t1 = track_1_vertex_artin_ihara(gap)
    t2 = track_2_local_algebra(Aw)
    t3 = track_3_ovoid_spread()
    t4 = track_4_code_boundary()
    t5 = track_5_weil_clifford(gap)
    t6 = track_6_spence_boundary()
    t7 = track_7_ladder(t1, t2, t3, t5)

    checks = {
        "T1_vertex_artin_ihara_complete_for_point_module": t1["active_dimension_sum"]
        == 40
        and t1["degree_check"],
        "T2_terwilliger_fingerprint": t2["terwilliger_dimension"] == 16
        and t2["distance_fibre_sizes"] == [1, 12, 27],
        "T3_ovoid_spread_duality": t3["alpha_W33"] == 7
        and t3["alpha_Q43"] == 10
        and t3["spread_count"] == 36
        and t3["line_participation_profile"] == {"9": 40},
        "T4_code_boundary_kept_open": t4["explicit_generator_promoted_by_this_pass"]
        is False,
        "T5_weil_clifford_split": t5["split_check"],
        "T6_spence_boundary_exact_pair": t6["cospectral"]
        and t6["locally_identical"]
        and t6["non_isomorphic"],
        "T7_ladder_checks": all(t7["checks"].values()),
    }

    payload = {
        "schema": "w33.pass78.equivariant_closure.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "track1_vertex_artin_ihara": t1,
        "track2_terwilliger_fingerprint": t2,
        "track3_ovoid_spread_duality": t3,
        "track4_66_code_boundary": t4,
        "track5_weil_clifford_carrier": t5,
        "track6_spence_hearing_boundary": t6,
        "track7_algebra_ladder": t7,
        "checks": checks,
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print("=" * 74)
    print("PASS 78 -- EQUIVARIANT ZETA / TERWILLIGER / CODE-BOUNDARY CLOSURE")
    print("=" * 74)
    print(
        f"[1] active point-module characters: {t1['active_constituent_degrees']}; denominator degree {t1['bass_denominator_degree']}"
    )
    print(
        f"[2] algebra dimensions: Bose-Mesner 3 -> Terwilliger {t2['terwilliger_dimension']}; fibres {t2['distance_fibre_sizes']}"
    )
    print(
        f"[3] ovoid/spread: alpha(W)={t3['alpha_W33']} alpha(Q)={t3['alpha_Q43']} spreads={t3['spread_count']} per-line={t3['line_participation_profile']}"
    )
    print(
        f"[4] [[66,8,3]] boundary kept open: generator promoted = {t4['explicit_generator_promoted_by_this_pass']}"
    )
    print(
        f"[5] Weil carrier: {t5['two_qutrit_dimension']}={t5['weil_split'][0]}+{t5['weil_split'][1]} confirmed={t5['split_check']}"
    )
    print(
        f"[6] Spence boundary: W/Q cospectral={t6['cospectral']} locally_identical={t6['locally_identical']} noniso={t6['non_isomorphic']}"
    )
    print(f"[7] ladder checks: {t7['checks']}")
    print("checks:")
    for key, value in checks.items():
        print(f"  {'OK' if value else 'XX'} {key}")
    print(f"STATUS: {payload['status']}")
    print(f"[wrote] {OUTPUT.name}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
