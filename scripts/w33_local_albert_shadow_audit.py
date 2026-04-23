#!/usr/bin/env python3
"""Exact local Albert-shadow audit for the W33 program.

This audit packages the strongest already-exact *local* cubic/Jordan support
that now exists in the repo:

1. The local H27 shell is the exact Heisenberg/MUB/Schlafli package.
2. The local cubic support is exactly the classical 45 tritangent planes,
   split as 9 fibers + 36 affine-line lifts in AG(2,3).
3. The signed cubic is not just a bare 45-triad hypergraph: naive W(E6)
   permutation transport fails, while the canonical cocycle gauge closes with
   zero failures.

So the exact local object is stronger than "27 points with 45 triples" and
weaker than a full implemented Albert product law. The conservative exact
reading is: a local determinant-support package, or "Albert shadow".
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
import json
from pathlib import Path
import sys
import time
from typing import Dict, Iterable, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.e6_hessian_tritangents import analyze_hessian_tritangent_split
from scripts.w33_exact_lie_bridge_audit import (
    local_e6_bridge_summary,
    local_h27_affine_symmetry_summary,
)

CANONICAL_CUBIC_JSON = ROOT / "artifacts" / "canonical_su3_gauge_and_cubic.json"
CANONICAL_INVARIANCE_JSON = ROOT / "artifacts" / "e6_cubic_invariance_canonical_gauge.json"
NAIVE_WE6_INVARIANCE_JSON = ROOT / "artifacts" / "e6_cubic_invariance_we6.json"
H27_JORDAN_TEST_JSON = ROOT / "artifacts" / "h27_jordan_algebra_test.json"


Triad = Tuple[int, int, int]


def _load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _norm_triad(triad: Iterable[int]) -> Triad:
    a, b, c = sorted(int(x) for x in triad)
    return (a, b, c)


@lru_cache(maxsize=1)
def local_shell_summary() -> Dict[str, object]:
    bridge = local_e6_bridge_summary()
    affine = local_h27_affine_symmetry_summary()
    hessian = analyze_hessian_tritangent_split()

    return {
        "visible_shell_size": int(bridge["nonneighbor_count"]),
        "mub_class_count": int(bridge["mub_class_count"]),
        "mub_class_sizes": tuple(int(v) for v in bridge["mub_class_sizes"]),
        "fiber_count": int(bridge["fiber_count"]),
        "fiber_size": int(bridge["fiber_size"]),
        "generation_fiber_sizes": tuple(int(v) for v in bridge["generation_fiber_sizes"]),
        "schlafli_parameters": tuple(int(v) for v in bridge["schlafli_parameters"]),
        "classical_tritangent_total": int(hessian["counts"]["triads_total"]),
        "internal_tritangent_count": int(hessian["counts"]["affine_triads"]),
        "missing_center_coset_count": int(hessian["counts"]["fiber_triads"]),
        "local_projective_symmetry_order": int(
            affine["projective_h27_restriction_order"]
        ),
        "local_affine_symmetry_order": int(affine["local_affine_group_order"]),
        "local_affine_point_stabilizer_order": int(
            affine["local_affine_point_stabilizer_order"]
        ),
        "full_graph_group_order": int(affine["full_graph_group_order"]),
    }


@lru_cache(maxsize=1)
def canonical_signed_cubic_summary() -> Dict[str, object]:
    payload = _load_json(CANONICAL_CUBIC_JSON)
    hessian = analyze_hessian_tritangent_split()

    triads_top = {
        _norm_triad(triad) for triad in payload["triads"]  # type: ignore[index]
    }
    solution = payload["solution"]  # type: ignore[index]
    signed_entries = solution["d_triples"]  # type: ignore[index]
    sign_by_triad = {
        _norm_triad(entry["triple"]): int(entry["sign"]) for entry in signed_entries
    }
    triads_solution = set(sign_by_triad)

    fiber_triads = {
        _norm_triad(triad) for triad in hessian["fiber_triads"]  # type: ignore[index]
    }
    affine_triads = {
        _norm_triad(triad) for triad in hessian["affine_triads"]  # type: ignore[index]
    }

    incidence = Counter(vertex for triad in triads_solution for vertex in triad)
    total_signs = Counter(sign_by_triad.values())
    fiber_signs = Counter(sign_by_triad[triad] for triad in fiber_triads)
    affine_signs = Counter(sign_by_triad[triad] for triad in affine_triads)
    affine_lifts_per_u_line = len(affine_triads) // int(hessian["counts"]["u_lines"])

    return {
        "triad_count": len(triads_solution),
        "top_level_triads_match_solution": triads_top == triads_solution,
        "canonical_solution_solvable": bool(payload["counts"]["solvable"]),  # type: ignore[index]
        "triad_set_matches_hessian_partition": triads_solution
        == (fiber_triads | affine_triads),
        "fiber_triad_count": len(fiber_triads),
        "affine_triad_count": len(affine_triads),
        "u_line_count": int(hessian["counts"]["u_lines"]),
        "affine_lifts_per_u_line": int(affine_lifts_per_u_line),
        "point_tritangent_incidence_values": tuple(sorted(set(incidence.values()))),
        "uniform_point_tritangent_incidence": len(set(incidence.values())) == 1,
        "point_tritangent_incidence": next(iter(set(incidence.values()))),
        "total_positive_signs": int(total_signs[1]),
        "total_negative_signs": int(total_signs[-1]),
        "fiber_positive_signs": int(fiber_signs[1]),
        "fiber_negative_signs": int(fiber_signs[-1]),
        "affine_positive_signs": int(affine_signs[1]),
        "affine_negative_signs": int(affine_signs[-1]),
    }


@lru_cache(maxsize=1)
def cubic_cocycle_boundary_summary() -> Dict[str, object]:
    canonical = _load_json(CANONICAL_INVARIANCE_JSON)
    naive = _load_json(NAIVE_WE6_INVARIANCE_JSON)

    canonical_results = canonical["results"]  # type: ignore[index]
    naive_results = naive["generators"]  # type: ignore[index]

    return {
        "canonical_generator_count": int(canonical["counts"]["generators"]),  # type: ignore[index]
        "canonical_failure_count": int(canonical["counts"]["failures_total"]),  # type: ignore[index]
        "canonical_global_bits": tuple(int(entry["global_bit"]) for entry in canonical_results),
        "naive_generator_count": int(naive["counts"]["generators"]),  # type: ignore[index]
        "naive_strict_solved_count": int(naive["counts"]["strict_solved"]),  # type: ignore[index]
        "naive_projective_solved_count": int(naive["counts"]["projective_solved"]),  # type: ignore[index]
        "naive_projective_failure_count": sum(
            1 for entry in naive_results if not bool(entry["projective_ok"])
        ),
        "naive_strict_failure_count": sum(
            1 for entry in naive_results if not bool(entry["strict_ok"])
        ),
        "correct_invariance_requires_cocycle_gauge": (
            int(canonical["counts"]["failures_total"]) == 0  # type: ignore[index]
            and int(naive["counts"]["projective_solved"]) == 0  # type: ignore[index]
            and sum(1 for entry in naive_results if not bool(entry["projective_ok"]))  # noqa: B023
            == int(naive["counts"]["generators"])  # type: ignore[index]
        ),
    }


@lru_cache(maxsize=1)
def jordan_boundary_summary() -> Dict[str, object]:
    payload = _load_json(H27_JORDAN_TEST_JSON)
    keys = set(payload.keys())  # type: ignore[union-attr]

    return {
        "graph_test_available": True,
        "h27_edge_count": int(payload["h27_edges"]),  # type: ignore[index]
        "h27_degree_set": tuple(int(v) for v in payload["h27_degree_set"]),  # type: ignore[index]
        "cn_determines_h27_adjacency": bool(payload["cn_determines_h27_adj"]),  # type: ignore[index]
        "contains_explicit_jordan_identity_verdict": "jordan_identity_holds" in keys,
        "contains_explicit_local_product_table": "multiplication_table" in keys,
        "contains_explicit_rank_spectrum": "jordan_rank_spectrum" in keys,
    }


@lru_cache(maxsize=1)
def classify_local_albert_shadow() -> Tuple[Dict[str, object], ...]:
    shell = local_shell_summary()
    cubic = canonical_signed_cubic_summary()
    cocycle = cubic_cocycle_boundary_summary()
    jordan = jordan_boundary_summary()

    return (
        {
            "name": "local_h27_heisenberg_schlafli_shell",
            "support_level": "repo-exact + classical exact",
            "statement": (
                "The local H27 shell is an exact Heisenberg/MUB package with Schlafli "
                "parameters (27,16,10,8) and faithful 648/1296 local symmetry."
            ),
            "evidence": shell,
        },
        {
            "name": "canonical_45_tritangent_signed_cubic",
            "support_level": "repo-exact + classical exact",
            "statement": (
                "The canonical local cubic support is exactly the classical 45-tritangent "
                "incidence package, split as 9 fibers plus 36 affine AG(2,3) lifts."
            ),
            "evidence": cubic,
        },
        {
            "name": "cocycle_gauge_local_invariance_boundary",
            "support_level": "exact boundary condition",
            "statement": (
                "Bare W(E6) permutation transport does not preserve the signed cubic, but "
                "the canonical cocycle gauge does, so the exact local object carries phase "
                "data and is not just an unsigned hypergraph."
            ),
            "evidence": cocycle,
        },
        {
            "name": "full_local_jordan_product_theorem",
            "support_level": "not-yet-exact local product law",
            "statement": (
                "The repo's current exact local certificate is determinant support, not yet "
                "a full implemented Albert/Jordan product theorem on H27."
            ),
            "evidence": jordan,
        },
    )


@lru_cache(maxsize=1)
def analyze() -> Dict[str, object]:
    records = classify_local_albert_shadow()
    exact_record_names = tuple(
        record["name"]
        for record in records
        if record["support_level"] != "not-yet-exact local product law"
    )
    open_record_names = tuple(
        record["name"]
        for record in records
        if record["support_level"] == "not-yet-exact local product law"
    )

    shell = local_shell_summary()
    cubic = canonical_signed_cubic_summary()
    cocycle = cubic_cocycle_boundary_summary()
    jordan = jordan_boundary_summary()

    theorem = {
        "the_local_shell_has_exact_27_point_heisenberg_schlafli_geometry": (
            shell["visible_shell_size"] == 27
            and shell["mub_class_sizes"] == (3, 3, 3, 3)
            and shell["fiber_count"] == 9
            and shell["fiber_size"] == 3
            and shell["generation_fiber_sizes"] == (9, 9, 9)
            and shell["schlafli_parameters"] == (27, 16, 10, 8)
            and shell["classical_tritangent_total"] == 45
            and shell["internal_tritangent_count"] == 36
            and shell["missing_center_coset_count"] == 9
            and shell["local_projective_symmetry_order"] == 648
            and shell["local_affine_symmetry_order"] == 1296
        ),
        "the_canonical_signed_cubic_support_is_exactly_the_45_tritangents_split_as_9_plus_36": (
            cubic["triad_count"] == 45
            and cubic["top_level_triads_match_solution"] is True
            and cubic["canonical_solution_solvable"] is True
            and cubic["triad_set_matches_hessian_partition"] is True
            and cubic["fiber_triad_count"] == 9
            and cubic["affine_triad_count"] == 36
            and cubic["u_line_count"] == 12
            and cubic["affine_lifts_per_u_line"] == 3
        ),
        "each_local_line_lies_on_exactly_five_tritangents": (
            cubic["uniform_point_tritangent_incidence"] is True
            and cubic["point_tritangent_incidence"] == 5
            and cubic["point_tritangent_incidence_values"] == (5,)
        ),
        "the_signed_cubic_support_requires_the_canonical_cocycle_gauge_for_we6_invariance": (
            cocycle["canonical_failure_count"] == 0
            and cocycle["canonical_global_bits"] == (0, 0, 0, 0, 0, 0)
            and cocycle["naive_projective_solved_count"] == 0
            and cocycle["naive_projective_failure_count"] == 6
            and cocycle["correct_invariance_requires_cocycle_gauge"] is True
        ),
        "the_naive_we6_permutation_action_does_not_preserve_the_signed_cubic": (
            cocycle["naive_strict_solved_count"] == 0
            and cocycle["naive_projective_solved_count"] == 0
            and cocycle["naive_strict_failure_count"] == 6
            and cocycle["naive_projective_failure_count"] == 6
        ),
        "the_repo_currently_reaches_a_local_albert_shadow_not_a_full_local_jordan_product": (
            jordan["graph_test_available"] is True
            and jordan["h27_edge_count"] == 108
            and jordan["h27_degree_set"] == (8,)
            and jordan["cn_determines_h27_adjacency"] is True
            and jordan["contains_explicit_jordan_identity_verdict"] is False
            and jordan["contains_explicit_local_product_table"] is False
            and jordan["contains_explicit_rank_spectrum"] is False
        ),
    }

    return {
        "status": "ok",
        "local_shell": shell,
        "canonical_signed_cubic": cubic,
        "cocycle_gauge_boundary": cocycle,
        "jordan_boundary": jordan,
        "record_names_exact_or_boundary": exact_record_names,
        "record_names_open": open_record_names,
        "record_details": records,
        "local_albert_shadow_theorem": theorem,
        "boundary_note": (
            "The exact local package is now sharper than an unsigned 45-triad story: "
            "it is a 27-point Heisenberg/Schlafli shell carrying the full 45-tritangent "
            "signed determinant support, and that sign data closes only in the canonical "
            "cocycle gauge. The honest open step is not another local counting identity; "
            "it is a full local product law and then the global dynamical/continuum lift."
        ),
    }


def main() -> None:
    started = time.time()
    payload = analyze()
    payload["analysis_duration_sec"] = round(time.time() - started, 6)

    output_dir = ROOT / "checks"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CXIII_local_albert_shadow_audit_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("Local Albert-shadow audit")
    print(f"  H27 shell: {payload['local_shell']['schlafli_parameters']}")
    print(
        "  Tritangent support: "
        f"{payload['canonical_signed_cubic']['fiber_triad_count']} + "
        f"{payload['canonical_signed_cubic']['affine_triad_count']} = "
        f"{payload['canonical_signed_cubic']['triad_count']}"
    )
    print(
        "  Cocycle boundary: "
        f"naive projective solved = {payload['cocycle_gauge_boundary']['naive_projective_solved_count']}, "
        f"canonical failures = {payload['cocycle_gauge_boundary']['canonical_failure_count']}"
    )
    print(f"  Wrote: {output_path}")


if __name__ == "__main__":
    main()
