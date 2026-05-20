#!/usr/bin/env python3
"""Probe the Hamming/Fano zero sheet against the completed spectral branch.

The previous experiment found that the Hamming/Fano zero sheet is not a loose
remainder: it is a connected, triangle-free 8-vertex/9-edge graph with cycle
rank 2 and simple cycle lengths 4, 4, 6.

The completed spectral package has a deformation variable lambda with a
uniform analytic wall at |lambda| = 6.  This file tests the obvious dangerous
connection:

    zero-sheet cycles: 4, 4, 6
    spectral wall:         6

Thus the two independent zero-sheet cycles sit naturally at the interior
deformation scale lambda=4, while their symmetric-difference 6-cycle lands on
the analytic wall and must be approached from below.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from w33.cyclotomic import (
    completed_defect_spectral_action,
    completed_defect_spectral_dual_stiffness,
    completed_defect_spectral_hessian_real_global,
    completed_defect_spectral_infinite_dual_branch_profile,
    completed_defect_spectral_infinite_dual_stiffness_profile,
    completed_defect_spectral_order_parameter_real_global,
    completed_defect_spectral_uniform_radius_lower_bound,
)


OUT = ROOT / "data" / "w33_zero_sheet_spectral_cycle_response.json"
RESULT = ROOT / "PART_MCXIV_zero_sheet_spectral_cycle_response_results.json"
FUNCTOR_PATH = ROOT / "analysis" / "w33_hamming_horizon_functor_search.py"


def load_hamming_functor_payload() -> dict[str, Any]:
    spec = importlib.util.spec_from_file_location("w33_hamming_horizon_functor_search", FUNCTOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {FUNCTOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.build_payload()


def finite_branch_rows(
    prime_limits: list[int],
    s: float,
    deformations: list[float],
) -> dict[str, list[dict[str, float | int]]]:
    rows: dict[str, list[dict[str, float | int]]] = {}
    for deformation in deformations:
        key = str(deformation)
        rows[key] = []
        for prime_limit in prime_limits:
            order = completed_defect_spectral_order_parameter_real_global(prime_limit, s, deformation)
            hessian = completed_defect_spectral_hessian_real_global(prime_limit, s, deformation)
            action = completed_defect_spectral_action(prime_limit, s, deformation).real
            dual = deformation * order - action
            rows[key].append(
                {
                    "prime_limit": prime_limit,
                    "deformation": deformation,
                    "order_parameter": order,
                    "hessian": hessian,
                    "stiffness": 1 / hessian,
                    "action": action,
                    "dual": dual,
                }
            )
    return rows


def rows_strictly_contract(rows: list[dict[str, float | int]], key: str) -> bool:
    values = [float(row[key]) for row in rows]
    return all(later < earlier for earlier, later in zip(values, values[1:]))


def rows_strictly_increase(rows: list[dict[str, float | int]], key: str) -> bool:
    values = [float(row[key]) for row in rows]
    return all(later > earlier for earlier, later in zip(values, values[1:]))


def rows_strictly_decrease(rows: list[dict[str, float | int]], key: str) -> bool:
    values = [float(row[key]) for row in rows]
    return all(later < earlier for earlier, later in zip(values, values[1:]))


def build_payload() -> dict[str, Any]:
    functor_payload = load_hamming_functor_payload()
    zero_graph = functor_payload["zero_sheet_subgraph"]
    cycle_lengths = zero_graph["simple_cycle_lengths"]

    spectral_wall = completed_defect_spectral_uniform_radius_lower_bound()
    independent_cycle_deformation = 4.0
    wall_cycle_length = 6.0
    wall_probe_deformations = [5.0, 5.5, 5.9]
    deformations = [independent_cycle_deformation] + wall_probe_deformations
    prime_limits = [10**3, 10**4, 10**5]
    s = 1.0

    branch_rows = finite_branch_rows(prime_limits, s, deformations)
    inverse_profiles = completed_defect_spectral_infinite_dual_branch_profile(
        10**3,
        prime_limits,
        [s],
        [independent_cycle_deformation, wall_probe_deformations[-1]],
    )
    stiffness_profiles = completed_defect_spectral_infinite_dual_stiffness_profile(
        10**3,
        prime_limits,
        [s],
        [independent_cycle_deformation, wall_probe_deformations[-1]],
    )

    terminal_rows = [branch_rows[str(deformation)][-1] for deformation in deformations]
    interior_profile = inverse_profiles[str(s)][str(independent_cycle_deformation)]["rows"]
    wall_profile = inverse_profiles[str(s)][str(wall_probe_deformations[-1])]["rows"]
    interior_stiffness_profile = stiffness_profiles[str(s)][str(independent_cycle_deformation)]["rows"]
    wall_stiffness_profile = stiffness_profiles[str(s)][str(wall_probe_deformations[-1])]["rows"]

    identities = {
        "zero_sheet_cycles_are_4_4_6": cycle_lengths == [4, 4, 6],
        "zero_sheet_cycle_rank_is_two": zero_graph["cycle_rank"] == 2,
        "independent_cycle_scale_is_inside_wall": independent_cycle_deformation < spectral_wall,
        "dependent_cycle_lands_on_spectral_wall": wall_cycle_length == spectral_wall,
        "wall_is_not_sampled_directly": all(deformation < spectral_wall for deformation in deformations),
        "interior_inverse_intervals_contract": rows_strictly_contract(interior_profile, "interval_width"),
        "wall_approach_inverse_intervals_contract": rows_strictly_contract(wall_profile, "interval_width"),
        "interior_stiffness_intervals_contract": rows_strictly_contract(
            interior_stiffness_profile,
            "stiffness_interval_width",
        ),
        "wall_approach_stiffness_intervals_contract": rows_strictly_contract(
            wall_stiffness_profile,
            "stiffness_interval_width",
        ),
        "hessian_increases_toward_wall": rows_strictly_increase(terminal_rows, "hessian"),
        "stiffness_decreases_toward_wall": rows_strictly_decrease(terminal_rows, "stiffness"),
    }

    return {
        "summary": {
            "experiment": "zero-sheet cycle response against the completed spectral equation of state",
            "zero_sheet_cycle_lengths": cycle_lengths,
            "zero_sheet_cycle_rank": zero_graph["cycle_rank"],
            "spectral_wall": spectral_wall,
            "interior_cycle_deformation": independent_cycle_deformation,
            "wall_probe_deformations": wall_probe_deformations,
            "prime_limits": prime_limits,
            "s": s,
            "all_identities_hold": all(identities.values()),
        },
        "zero_sheet_subgraph": zero_graph,
        "cycle_to_spectral_dictionary": {
            "two_independent_4_cycles": (
                "probe the interior completed spectral branch at lambda=4"
            ),
            "dependent_6_cycle": (
                "lands on the uniform analytic wall |lambda|=6, so it is treated as a limiting wall cycle"
            ),
            "reading": (
                "The Hamming/Fano zero sheet behaves like a rank-two residual gauge source: "
                "its independent cycles live inside the completed spectral branch, while their "
                "symmetric-difference cycle marks the analytic boundary."
            ),
        },
        "finite_branch_rows": branch_rows,
        "infinite_inverse_profiles": inverse_profiles,
        "infinite_stiffness_profiles": stiffness_profiles,
        "terminal_wall_approach_rows": terminal_rows,
        "identities": identities,
        "honesty_boundary": (
            "This is an exploratory cross-connection between the coordinate zero sheet and the "
            "completed spectral equation of state. It verifies compatible cycle/wall arithmetic "
            "and monotone spectral response, but it does not prove that the zero sheet generates "
            "the spectral deformation variable."
        ),
    }


def main() -> None:
    payload = build_payload()
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    result = {
        "theorem": "Zero-sheet spectral cycle-response law",
        "summary": payload["summary"],
        "terminal_wall_approach_rows": payload["terminal_wall_approach_rows"],
        "interior_inverse_profile": payload["infinite_inverse_profiles"]["1.0"]["4.0"]["rows"],
        "wall_inverse_profile": payload["infinite_inverse_profiles"]["1.0"]["5.9"]["rows"],
        "interior_stiffness_profile": payload["infinite_stiffness_profiles"]["1.0"]["4.0"]["rows"],
        "wall_stiffness_profile": payload["infinite_stiffness_profiles"]["1.0"]["5.9"]["rows"],
    }
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")

    print("=== MCXIV Zero-Sheet Spectral Cycle Response ===")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"wrote {RESULT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
