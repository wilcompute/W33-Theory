"""MCCXLVI: golden-selector obstruction Z20 cochain lift.

The draft Part XXIV selector builds a local sign rule on the 480 directed
line-transport edges but fails flatness on 864 ordered nonlocal quadrangles.
This verifier turns that failure into a solvable cochain problem.

The key distinction is:

* line phases are 0-cochains and telescope around every quadrangle, so they
  cannot repair a nonzero holonomy;
* transport-edge phases are 1-cochains, and an internal C2 solution exists.

We lift the C2 correction to a Z20 half-period phase by assigning phase 10 on
selected undirected transport edges and phase 0 elsewhere.  Around each
originally failing quadrangle the phase sum is 10 mod 20; around each passing
quadrangle it is 0 mod 20.  Equivalently the half-period sign cancels the
draft selector holonomy on every quadrangle.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.w33_golden_selector_draft_audit import (  # noqa: E402
    _classify_nonlocal_quadrangle_failures,
    _common_point,
    _line_adjacency,
    _load_draft_module,
)


@dataclass(frozen=True)
class Quadrangle:
    lines: tuple[int, int, int, int]
    points: tuple[int, int, int, int]
    holonomy: int
    edge_mask: int

    @property
    def rhs(self) -> int:
        return 0 if self.holonomy == 1 else 1


def canonical_cycle(lines: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    variants: list[tuple[int, int, int, int]] = []
    for sequence in (list(lines), list(reversed(lines))):
        for shift in range(4):
            variants.append(tuple(sequence[shift:] + sequence[:shift]))  # type: ignore[arg-type]
    return min(variants)


def load_selector_data() -> tuple[list[tuple[int, ...]], dict[tuple[int, int, int], int]]:
    module, _error = _load_draft_module()
    return list(module.lines), dict(module.sigma)


def build_transport_edges(lines: list[tuple[int, ...]]) -> tuple[list[tuple[int, int, int]], dict[tuple[int, int], int]]:
    adjacency = _line_adjacency(lines)
    edges: list[tuple[int, int, int]] = []
    edge_index: dict[tuple[int, int], int] = {}
    for left in range(len(lines)):
        for right in range(left + 1, len(lines)):
            if not adjacency[left][right]:
                continue
            point = _common_point(lines[left], lines[right])
            edge_index[(left, right)] = len(edges)
            edges.append((point, left, right))
    return edges, edge_index


def build_unique_quadrangles(
    lines: list[tuple[int, ...]],
    sigma: dict[tuple[int, int, int], int],
    edge_index: dict[tuple[int, int], int],
) -> list[Quadrangle]:
    adjacency = _line_adjacency(lines)
    seen: set[tuple[int, int, int, int]] = set()
    quadrangles: list[Quadrangle] = []

    for line0, neighbours0 in enumerate(adjacency):
        for line1, is_adjacent01 in enumerate(neighbours0):
            if not is_adjacent01:
                continue
            point01 = _common_point(lines[line0], lines[line1])

            for line2, is_adjacent12 in enumerate(adjacency[line1]):
                if line2 == line0 or not is_adjacent12:
                    continue
                point12 = _common_point(lines[line1], lines[line2])
                if point12 == point01:
                    continue

                for line3, is_adjacent23 in enumerate(adjacency[line2]):
                    if line3 == line1 or not is_adjacent23 or not adjacency[line3][line0]:
                        continue

                    point23 = _common_point(lines[line2], lines[line3])
                    point30 = _common_point(lines[line3], lines[line0])
                    points = (point01, point12, point23, point30)
                    if len(set(points)) < 4:
                        continue

                    cycle = (line0, line1, line2, line3)
                    key = canonical_cycle(cycle)
                    if key in seen:
                        continue
                    seen.add(key)

                    directed_edges = (
                        (point01, line0, line1),
                        (point12, line1, line2),
                        (point23, line2, line3),
                        (point30, line3, line0),
                    )
                    holonomy = 1
                    mask = 0
                    for point, left, right in directed_edges:
                        holonomy *= sigma[(point, left, right)]
                        edge_key = tuple(sorted((left, right)))
                        mask ^= 1 << edge_index[edge_key]

                    quadrangles.append(
                        Quadrangle(
                            lines=cycle,
                            points=points,
                            holonomy=holonomy,
                            edge_mask=mask,
                        )
                    )

    return quadrangles


def solve_gf2(rows: list[tuple[int, int]], variable_count: int) -> dict[str, Any]:
    """Solve a GF(2) system represented by integer bit masks.

    Free variables are set to zero.  Pivot selection is deterministic, using
    the highest live column first.  The returned support is one gauge-fixed
    correction, not a claimed minimum-weight correction.
    """

    pivots: dict[int, int] = {}
    pivot_rhs: dict[int, int] = {}

    for mask, rhs in rows:
        current = mask
        value = rhs
        while current:
            column = current.bit_length() - 1
            if column not in pivots:
                pivots[column] = current
                pivot_rhs[column] = value
                break
            current ^= pivots[column]
            value ^= pivot_rhs[column]
        else:
            if value:
                return {
                    "consistent": False,
                    "rank": len(pivots),
                    "free_dimension": variable_count - len(pivots),
                    "solution_mask": 0,
                    "support": [],
                }

    solution = 0
    for column in sorted(pivots):
        row = pivots[column] & ~(1 << column)
        parity = (row & solution).bit_count() % 2
        if parity ^ pivot_rhs[column]:
            solution |= 1 << column

    support = [index for index in range(variable_count) if (solution >> index) & 1]
    return {
        "consistent": True,
        "rank": len(pivots),
        "free_dimension": variable_count - len(pivots),
        "solution_mask": solution,
        "support": support,
    }


def corrected_holonomy_failures(
    quadrangles: list[Quadrangle],
    solution_mask: int,
) -> dict[str, int]:
    original_failures = 0
    corrected_failures = 0
    phase_profile: Counter[int] = Counter()

    for quadrangle in quadrangles:
        correction_bit = (quadrangle.edge_mask & solution_mask).bit_count() % 2
        corrected = quadrangle.holonomy * (-1 if correction_bit else 1)
        phase_profile[(10 * correction_bit) % 20] += 1
        if quadrangle.holonomy != 1:
            original_failures += 1
        if corrected != 1:
            corrected_failures += 1

    return {
        "original_unique_failures": original_failures,
        "corrected_unique_failures": corrected_failures,
        "phase_sum_mod20_profile": {str(key): int(value) for key, value in sorted(phase_profile.items())},
    }


def ordered_corrected_failures(
    lines: list[tuple[int, ...]],
    sigma: dict[tuple[int, int, int], int],
    edge_index: dict[tuple[int, int], int],
    solution_mask: int,
) -> int:
    adjacency = _line_adjacency(lines)
    corrected_failures = 0

    for line0, neighbours0 in enumerate(adjacency):
        for line1, is_adjacent01 in enumerate(neighbours0):
            if not is_adjacent01:
                continue
            point01 = _common_point(lines[line0], lines[line1])

            for line2, is_adjacent12 in enumerate(adjacency[line1]):
                if line2 == line0 or not is_adjacent12:
                    continue
                point12 = _common_point(lines[line1], lines[line2])
                if point12 == point01:
                    continue

                for line3, is_adjacent23 in enumerate(adjacency[line2]):
                    if line3 == line1 or not is_adjacent23 or not adjacency[line3][line0]:
                        continue

                    point23 = _common_point(lines[line2], lines[line3])
                    point30 = _common_point(lines[line3], lines[line0])
                    if len({point01, point12, point23, point30}) < 4:
                        continue

                    holonomy = (
                        sigma[(point01, line0, line1)]
                        * sigma[(point12, line1, line2)]
                        * sigma[(point23, line2, line3)]
                        * sigma[(point30, line3, line0)]
                    )
                    mask = 0
                    for left, right in ((line0, line1), (line1, line2), (line2, line3), (line3, line0)):
                        mask ^= 1 << edge_index[tuple(sorted((left, right)))]
                    correction_bit = (mask & solution_mask).bit_count() % 2
                    if holonomy * (-1 if correction_bit else 1) != 1:
                        corrected_failures += 1

    return corrected_failures


def line_phase_coboundary_is_invisible(quadrangles: list[Quadrangle]) -> bool:
    """Every 4-cycle boundary uses each line variable twice over GF(2)."""

    for quadrangle in quadrangles:
        counts = Counter(quadrangle.lines)
        if any(value != 1 for value in counts.values()):
            return False
        # For a line potential x, the edge boundary sum is
        # (x0+x1)+(x1+x2)+(x2+x3)+(x3+x0)=0.
    return True


def golden_selector_z20_cochain_lift_packet() -> dict[str, Any]:
    q = 3
    v = 40
    k = 12
    mu = 4
    g = 15
    e8_roots = 240

    lines, sigma = load_selector_data()
    transport_edges, edge_index = build_transport_edges(lines)
    quadrangles = build_unique_quadrangles(lines, sigma, edge_index)
    rows = [(quadrangle.edge_mask, quadrangle.rhs) for quadrangle in quadrangles]
    solution = solve_gf2(rows, len(transport_edges))
    solution_mask = int(solution["solution_mask"])
    correction = corrected_holonomy_failures(quadrangles, solution_mask)
    ordered_after = ordered_corrected_failures(lines, sigma, edge_index, solution_mask)
    draft_audit = _classify_nonlocal_quadrangle_failures(lines, sigma)

    selected_edges = [transport_edges[index] for index in solution["support"]]
    selected_point_profile = Counter(point for point, _left, _right in selected_edges)
    selected_line_degree = Counter(
        sum(1 for _point, left, right in selected_edges if left == line or right == line)
        for line in range(len(lines))
    )
    selected_sigma_profile = Counter(sigma[(point, left, right)] for point, left, right in selected_edges)

    checks = {
        "draft_ordered_quadrangle_count_is_v_k_q3": draft_audit["total_quadrangles_checked"] == v * k * q**3,
        "draft_ordered_violation_count_is_2_mu_plus_1_q3": draft_audit["flatness_violations"]
        == 2 ** (mu + 1) * q**3,
        "draft_violation_rate_is_one_over_g": draft_audit["flatness_violations"] * g
        == draft_audit["total_quadrangles_checked"],
        "transport_edges_are_two_e8_root_shells": len(sigma) == 2 * e8_roots,
        "unique_quadrangles_are_ordered_divided_by_eight": len(quadrangles) * 8
        == draft_audit["total_quadrangles_checked"],
        "unique_failures_are_ordered_divided_by_eight": correction["original_unique_failures"] * 8
        == draft_audit["flatness_violations"],
        "unique_failure_count_is_mu_q3": correction["original_unique_failures"] == mu * q**3,
        "gf2_obstruction_system_is_consistent": bool(solution["consistent"]),
        "gf2_rank_is_200": solution["rank"] == 200,
        "gf2_free_dimension_is_line_count": solution["free_dimension"] == len(lines) == v,
        "z20_half_period_lift_corrects_all_unique_quadrangles": correction["corrected_unique_failures"] == 0,
        "z20_half_period_lift_corrects_all_ordered_quadrangles": ordered_after == 0,
        "phase_sum_profile_matches_original_holonomy": correction["phase_sum_mod20_profile"]
        == {"0": len(quadrangles) - correction["original_unique_failures"], "10": correction["original_unique_failures"]},
        "line_phase_coboundaries_cannot_change_quadrangle_holonomy": line_phase_coboundary_is_invisible(
            quadrangles
        )
        and correction["original_unique_failures"] > 0,
        "gauge_fixed_support_is_2_q3": len(solution["support"]) == 2 * q**3,
        "gauge_fixed_support_is_sign_balanced": selected_sigma_profile == {1: q**3, -1: q**3},
    }

    return {
        "part": "MCCXLVI",
        "theorem": "Golden selector Z20 cochain lift",
        "input_audit": "scripts/w33_golden_selector_draft_audit.py",
        "draft_obstruction": {
            "line_count": len(lines),
            "directed_transport_edges": len(sigma),
            "undirected_transport_edges": len(transport_edges),
            "ordered_quadrangles": draft_audit["total_quadrangles_checked"],
            "ordered_violations": draft_audit["flatness_violations"],
            "local_violations": draft_audit["local_flatness_violations"],
            "nonlocal_violations": draft_audit["nonlocal_flatness_violations"],
            "violation_rate": "1/15",
            "substrate_identities": {
                "ordered_quadrangles": "v*k*q^3 = 40*12*27 = 12960",
                "ordered_violations": "2^(mu+1)*q^3 = 32*27 = 864",
                "unique_violations": "mu*q^3 = 4*27 = 108",
                "ordered_violations_over_transport_edges": "864/480 = q^2/5 = 9/5",
            },
        },
        "cochain_system": {
            "variables": len(transport_edges),
            "unique_quadrangles": len(quadrangles),
            "unique_failures": correction["original_unique_failures"],
            "rank": solution["rank"],
            "free_dimension": solution["free_dimension"],
            "consistent": solution["consistent"],
            "gauge_boundary": "The 40 free dimensions match the 40 line phases; line-phase coboundaries are invisible on quadrangle holonomy.",
        },
        "z20_lift": {
            "pisano_period_pi_5": 20,
            "phase_values": [0, 10],
            "sign_rule": "tau(e)=(-1)^(phase20(e)/10), with phase20=10 on selected edges",
            "selected_edge_count": len(solution["support"]),
            "selected_edge_formula": "2*q^3 = 54 for this deterministic gauge-fixed solution",
            "selected_point_profile": {str(key): int(value) for key, value in sorted(selected_point_profile.items())},
            "selected_line_degree_profile": {str(key): int(value) for key, value in sorted(selected_line_degree.items())},
            "selected_sigma_profile": {str(key): int(value) for key, value in sorted(selected_sigma_profile.items())},
            "phase_sum_mod20_profile": correction["phase_sum_mod20_profile"],
            "corrected_unique_failures": correction["corrected_unique_failures"],
            "corrected_ordered_failures": ordered_after,
        },
        "reading": (
            "The golden selector obstruction is spectrally quantized but not fatal: "
            "the 864 ordered failures are 8 copies of 108 unique nonlocal "
            "quadrangle failures, and the GF(2) cycle system admits an internal "
            "transport-edge correction. A Z20 half-period lift, using the Pisano "
            "period pi(5)=20 as a phase clock, cancels every failed holonomy."
        ),
        "boundary": (
            "A line-phase correction cannot work because 0-cochains telescope "
            "around quadrangles. The correction lives on transport edges. The "
            "displayed 54-edge support is a deterministic gauge-fixed solution, "
            "not a claimed unique or minimum-weight lift."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = golden_selector_z20_cochain_lift_packet()
    out_path = ROOT / "PART_MCCXLVI_GOLDEN_SELECTOR_Z20_COCHAIN_LIFT_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCCXLVI: Golden Selector Z20 Cochain Lift ===")
    print("draft obstruction:", packet["draft_obstruction"])
    print("cochain system:", packet["cochain_system"])
    print("z20 lift:", packet["z20_lift"])
    print("verified:", packet["n_verified"], "/", len(packet["checks"]))


if __name__ == "__main__":
    main()
