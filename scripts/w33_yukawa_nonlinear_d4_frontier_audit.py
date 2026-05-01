#!/usr/bin/env python3
"""Executable nonlinear D4 Yukawa frontier audit.

This audit freezes the nonlinear frontier as an explicit certificate built from
existing bridge summaries. It checks:

1. Minimal degree gate in the active packet.
2. D4 Galois-type gate for the two quartic lifts.
3. Branch-stable octic gate for canonical mixed product/ratio packets.
4. Reproducibility gate via deterministic JSON hash.
"""

from __future__ import annotations

from functools import lru_cache
import hashlib
import json
from pathlib import Path
import sys
import time
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
EXPLORATION = ROOT / "exploration"
for candidate in (ROOT, EXPLORATION):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

from w33_yukawa_nonlinear_frontier_bridge import (  # noqa: E402
    build_yukawa_nonlinear_frontier_summary,
)
from w33_yukawa_quartic_lift_bridge import (  # noqa: E402
    build_yukawa_quartic_lift_summary,
)
from scripts.w33_yukawa_frontier_audit import analyze as analyze_yukawa_frontier  # noqa: E402

DEFAULT_CERT_PATH = ROOT / "artifacts" / "w33_yukawa_nonlinear_d4_frontier_certificate.json"
DEFAULT_HASH_PATH = ROOT / "artifacts" / "w33_yukawa_nonlinear_d4_frontier_certificate.sha256"


def _stable_json_bytes(payload: Dict[str, Any]) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sha256_hex(payload: Dict[str, Any]) -> str:
    return hashlib.sha256(_stable_json_bytes(payload)).hexdigest()


@lru_cache(maxsize=1)
def build_nonlinear_d4_relation_certificate() -> Dict[str, Any]:
    nonlinear = build_yukawa_nonlinear_frontier_summary()
    quartic = build_yukawa_quartic_lift_summary()
    frontier = analyze_yukawa_frontier()

    nonlinear_theorem = nonlinear["nonlinear_frontier_theorem"]
    quartic_theorem = quartic["quartic_lift_theorem"]
    open_problem = frontier["current_open_problem"]

    max_active_factor_degree = int(
        nonlinear["finite_algebraic_packet"]["max_active_factor_degree"]
    )

    quartic_records = quartic["quartic_lift_packet"]["records"]
    galois_labels = {
        name: record["galois_group_label"] for name, record in quartic_records.items()
    }
    galois_orders = {
        name: int(record["galois_group_order"]) for name, record in quartic_records.items()
    }

    certificate = {
        "status": "ok",
        "degree_gate": {
            "max_active_factor_degree": max_active_factor_degree,
            "open_problem_max_active_factor_degree": int(open_problem["max_active_factor_degree"]),
            "native_mixed_seed_lift_reaches_11_to_12": bool(
                nonlinear_theorem["native_mixed_seed_lift_reaches_11_to_12"]
            ),
        },
        "d4_galois_gate": {
            "quartic_galois_labels": galois_labels,
            "quartic_galois_orders": galois_orders,
            "both_even_lifts_are_irreducible_d4_quartics": bool(
                quartic_theorem["both_even_lifts_are_irreducible_d4_quartics"]
            ),
            "quartic_root_fields_are_linearly_disjoint_over_q": bool(
                quartic_theorem["the_two_quartic_root_fields_are_linearly_disjoint_over_q"]
            ),
            "quartic_splitting_fields_are_linearly_disjoint_over_q": bool(
                quartic_theorem["the_two_d4_splitting_fields_are_linearly_disjoint_over_q"]
            ),
        },
        "branch_stability_gate": {
            "mixed_product_ratio_branch_stable_irreducible_octics": bool(
                quartic_theorem[
                    "the_canonical_mixed_product_and_ratio_packets_are_branch_stable_irreducible_octics"
                ]
            ),
            "mixed_product_ratio_even_lifts_of_irreducible_quartics": bool(
                quartic_theorem[
                    "the_canonical_mixed_product_and_ratio_packets_are_even_lifts_of_branch_stable_irreducible_quartics"
                ]
            ),
            "mixed_squared_packets_exact_resultants": bool(
                quartic_theorem[
                    "the_canonical_mixed_squared_packets_are_exact_product_quotient_resultants_of_the_base_quadratic_pair"
                ]
            ),
        },
        "frontier_consistency_gate": {
            "open_problem_kind": open_problem["kind"],
            "open_problem_relation_above_two_linearly_disjoint_d4_splitting_fields": (
                open_problem["kind"]
                == "relation_above_two_linearly_disjoint_d4_splitting_fields"
            ),
            "open_problem_branch_stable_irreducible_octics": bool(
                open_problem[
                    "canonical_mixed_product_and_ratio_are_branch_stable_irreducible_octics"
                ]
            ),
        },
    }

    theorem = {
        "degree_gate_passes": (
            certificate["degree_gate"]["max_active_factor_degree"]
            == certificate["degree_gate"]["open_problem_max_active_factor_degree"]
            and certificate["degree_gate"]["native_mixed_seed_lift_reaches_11_to_12"] is True
        ),
        "d4_galois_gate_passes": (
            certificate["d4_galois_gate"]["both_even_lifts_are_irreducible_d4_quartics"] is True
            and certificate["d4_galois_gate"]["quartic_root_fields_are_linearly_disjoint_over_q"] is True
            and certificate["d4_galois_gate"]["quartic_splitting_fields_are_linearly_disjoint_over_q"] is True
            and all(label == "D4" for label in galois_labels.values())
            and all(order == 8 for order in galois_orders.values())
        ),
        "branch_stability_gate_passes": (
            certificate["branch_stability_gate"][
                "mixed_product_ratio_branch_stable_irreducible_octics"
            ]
            is True
            and certificate["branch_stability_gate"][
                "mixed_product_ratio_even_lifts_of_irreducible_quartics"
            ]
            is True
            and certificate["branch_stability_gate"][
                "mixed_squared_packets_exact_resultants"
            ]
            is True
        ),
        "frontier_consistency_gate_passes": (
            certificate["frontier_consistency_gate"][
                "open_problem_relation_above_two_linearly_disjoint_d4_splitting_fields"
            ]
            is True
            and certificate["frontier_consistency_gate"][
                "open_problem_branch_stable_irreducible_octics"
            ]
            is True
        ),
    }
    theorem["nonlinear_d4_relation_certificate_passes"] = all(theorem.values())

    payload = {
        "status": "ok",
        "nonlinear_d4_relation_certificate": certificate,
        "nonlinear_d4_relation_certificate_theorem": theorem,
        "boundary_note": (
            "This certificate closes the nonlinear finite D4 frontier gates "
            "and freezes the resulting packet reproducibly."
        ),
    }

    payload_hash = _sha256_hex(payload)
    payload["certificate_sha256"] = payload_hash
    return payload


def write_frozen_certificate(
    cert_path: Path = DEFAULT_CERT_PATH,
    hash_path: Path = DEFAULT_HASH_PATH,
) -> Dict[str, Any]:
    payload = build_nonlinear_d4_relation_certificate()
    cert_path.parent.mkdir(parents=True, exist_ok=True)

    serialized = json.dumps(payload, indent=2, sort_keys=True)
    cert_path.write_text(serialized, encoding="utf-8")

    digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    hash_path.write_text(digest + "\n", encoding="utf-8")

    read_back = cert_path.read_text(encoding="utf-8")
    read_back_digest = hashlib.sha256(read_back.encode("utf-8")).hexdigest()

    return {
        "certificate_path": str(cert_path),
        "hash_path": str(hash_path),
        "written_sha256": digest,
        "read_back_sha256": read_back_digest,
        "reproducibility_verified": digest == read_back_digest,
    }


@lru_cache(maxsize=1)
def analyze() -> Dict[str, Any]:
    payload = build_nonlinear_d4_relation_certificate()
    frozen = write_frozen_certificate()
    payload["frozen_artifact"] = frozen
    payload["nonlinear_d4_relation_certificate_theorem"][
        "frozen_artifact_reproducibility_verified"
    ] = frozen["reproducibility_verified"]
    payload["nonlinear_d4_relation_certificate_theorem"][
        "nonlinear_d4_relation_certificate_passes"
    ] = all(payload["nonlinear_d4_relation_certificate_theorem"].values())
    return payload


def main() -> None:
    started = time.time()
    payload = analyze()
    payload["analysis_duration_sec"] = round(time.time() - started, 6)

    output_dir = ROOT / "checks"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_C_yukawa_nonlinear_d4_frontier_audit_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"[ok] wrote {output_path}")


if __name__ == "__main__":
    main()
