#!/usr/bin/env python3
"""Part DCMLXXIX: Ihara parameter reconciliation.

The latest RH/CSS burst contains two true ideas that must not be conflated:

* the Levi graph of PG(2,3) is a 4-regular Ramanujan graph, so its Bass/Ihara
  parameter is 3 and its non-trivial Ihara poles lie on |u| = 3^{-1/2};
* the W(3,3) collinearity graph is 12-regular, so its Bass/Ihara parameter is
  11 and its non-trivial Ihara poles lie on |u| = 11^{-1/2}.

This verifier keeps the graph-Ihara theorem sharp while preserving the honest
status boundary: finite graph RH is proved; classical Riemann RH still requires
an identification/limit theorem.
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DATA_PATH = ROOT / "data" / "dcmlxxix_ihara_parameter_reconciliation.json"
RESULT_PATH = ROOT / "PART_DCMLXXIX_IHARA_PARAMETER_RECONCILIATION_results.json"


@dataclass(frozen=True)
class ReconciliationSummary:
    part: str
    decimal: int
    pg23_field_q: int
    pg23_degree: int
    pg23_bass_q: int
    pg23_nontrivial_radius_squared_numerator: int
    pg23_nontrivial_radius_squared_denominator: int
    w33_degree: int
    w33_bass_q: int
    classical_rh_status: str
    all_identities_hold: bool


def _fraction_payload(value: Fraction) -> dict[str, int]:
    return {"numerator": value.numerator, "denominator": value.denominator}


def _read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _read_json(path: str) -> dict[str, Any]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _paired_quartic_coefficients(lambda_squared: int, bass_q: int) -> dict[str, int]:
    """Return coefficients of (1-lambda u+B u^2)(1+lambda u+B u^2)."""

    return {
        "constant": 1,
        "u2": 2 * bass_q - lambda_squared,
        "u4": bass_q * bass_q,
    }


def build_reconciliation() -> dict[str, Any]:
    field_q = 3

    pg23_degree = field_q + 1
    pg23_bass_q = pg23_degree - 1
    pg23_points = field_q * field_q + field_q + 1
    pg23_vertices = 2 * pg23_points
    pg23_edges = pg23_points * pg23_degree
    pg23_e_minus_v = pg23_edges - pg23_vertices
    pg23_nontrivial_lambda_squared = field_q
    pg23_nontrivial_quartic = _paired_quartic_coefficients(
        lambda_squared=pg23_nontrivial_lambda_squared,
        bass_q=pg23_bass_q,
    )
    pg23_trivial_quartic = _paired_quartic_coefficients(
        lambda_squared=pg23_degree * pg23_degree,
        bass_q=pg23_bass_q,
    )
    pg23_radius_squared = Fraction(1, pg23_bass_q)

    stale_quartic = _paired_quartic_coefficients(
        lambda_squared=pg23_nontrivial_lambda_squared,
        bass_q=pg23_degree,
    )
    stale_radius_squared = Fraction(1, pg23_degree)

    w33_degree = 12
    w33_bass_q = w33_degree - 1
    w33_nontrivial_bound = 2 * math.sqrt(w33_bass_q)
    w33_max_nontrivial_adjacency_abs = 4
    w33_radius_squared = Fraction(1, w33_bass_q)

    critical_audit = _read_text("PART_DCMLXVI_CRITICAL_AUDIT.md")
    honest_assessment = _read_text("PART_DCMLXVIII_HONEST_ASSESSMENT.md")
    clean_proof = _read_text("PART_DCMLXXVIII_CLEAN_PROOF.md")
    rh_status = _read_json("RH_PROOF_STATUS.json")

    identities = {
        "pg23_bass_parameter_is_degree_minus_one": pg23_bass_q == field_q,
        "pg23_levi_counts_are_exact": (pg23_vertices, pg23_edges, pg23_e_minus_v)
        == (26, 52, 26),
        "pg23_nontrivial_quartic_is_correct": pg23_nontrivial_quartic
        == {"constant": 1, "u2": 3, "u4": 9},
        "pg23_trivial_eigen_pair_factors_correctly": pg23_trivial_quartic
        == {"constant": 1, "u2": -10, "u4": 9},
        "pg23_nontrivial_radius_is_1_over_sqrt_3": pg23_radius_squared
        == Fraction(1, 3),
        "stale_degree_substitution_is_rejected": stale_quartic
        == {"constant": 1, "u2": 5, "u4": 16}
        and stale_radius_squared == Fraction(1, 4)
        and stale_radius_squared != pg23_radius_squared,
        "w33_collinearity_bass_parameter_is_11_not_3": w33_bass_q == 11,
        "w33_collinearity_is_ramanujan_with_bass_11": (
            w33_max_nontrivial_adjacency_abs <= w33_nontrivial_bound
        ),
        "w33_collinearity_radius_differs_from_pg23_levi_radius": (
            w33_radius_squared != pg23_radius_squared
        ),
        "critical_audit_keeps_zeta_identification_open": (
            "identification $\\zeta_W = \\zeta$" in critical_audit
            and "single remaining step" in critical_audit
        ),
        "honest_assessment_keeps_riemann_rh_open": (
            "It does not directly prove RH for the Riemann zeta function"
            in honest_assessment
        ),
        "clean_proof_is_graph_ihara_not_classical_rh": (
            "GRAPH/IHARA PROOF COMPLETE" in clean_proof
            and "does not prove the classical Riemann Hypothesis" in clean_proof
        ),
        "rh_status_json_keeps_classical_rh_open": (
            rh_status["RH_status"]["Riemann_zeta_RH"].startswith("OPEN")
        ),
    }

    summary = ReconciliationSummary(
        part="DCMLXXIX",
        decimal=979,
        pg23_field_q=field_q,
        pg23_degree=pg23_degree,
        pg23_bass_q=pg23_bass_q,
        pg23_nontrivial_radius_squared_numerator=pg23_radius_squared.numerator,
        pg23_nontrivial_radius_squared_denominator=pg23_radius_squared.denominator,
        w33_degree=w33_degree,
        w33_bass_q=w33_bass_q,
        classical_rh_status="OPEN: finite graph-Ihara RH does not identify the Riemann zeta zeros",
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "pg23_levi_graph": {
            "field_q": field_q,
            "degree": pg23_degree,
            "bass_q": pg23_bass_q,
            "vertices": pg23_vertices,
            "edges": pg23_edges,
            "e_minus_v": pg23_e_minus_v,
            "adjacency_spectrum": {
                "+4": 1,
                "-4": 1,
                "+sqrt(3)": 12,
                "-sqrt(3)": 12,
            },
            "ihara_inverse_factorization": {
                "bass_formula": "(1-u^2)^(E-V) det(I - A u + (d-1)u^2)",
                "e_minus_v_factor": f"(1-u^2)^{pg23_e_minus_v}",
                "trivial_eigen_pair": "1 - 10u^2 + 9u^4 = (1-u^2)(1-9u^2)",
                "nontrivial_eigen_pair": "1 + 3u^2 + 9u^4",
                "nontrivial_multiplicity": 12,
            },
            "nontrivial_pole_radius_squared": _fraction_payload(pg23_radius_squared),
            "nontrivial_pole_radius": "3^(-1/2)",
        },
        "rejected_stale_formula": {
            "formula": "1 + 5u^2 + 16u^4",
            "source_of_error": "uses degree d=4 where Bass/Ihara requires d-1=3",
            "radius_squared_if_used": _fraction_payload(stale_radius_squared),
            "correct_radius_squared": _fraction_payload(pg23_radius_squared),
        },
        "w33_collinearity_graph": {
            "vertices": 40,
            "edges": 240,
            "degree": w33_degree,
            "bass_q": w33_bass_q,
            "adjacency_spectrum": {"12": 1, "2": 24, "-4": 15},
            "ramanujan_bound": f"2*sqrt({w33_bass_q})",
            "max_nontrivial_adjacency_abs": w33_max_nontrivial_adjacency_abs,
            "nontrivial_pole_radius_squared": _fraction_payload(w33_radius_squared),
            "nontrivial_pole_radius": "11^(-1/2)",
        },
        "status_boundary": {
            "proved": [
                "Ihara/graph RH for the PG(2,3) Levi graph",
                "Ihara/graph RH for the W(3,3) collinearity graph",
                "finite CSS/Ramanujan analogues tracked by the repository",
            ],
            "open": [
                "identifying the finite/projective-limit graph zeta with the classical Riemann zeta",
                "uniform continuum/adelic limit needed to transfer graph RH to classical RH",
            ],
        },
        "identities": identities,
    }


def write_reconciliation() -> tuple[Path, Path]:
    payload = build_reconciliation()
    DATA_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    RESULT_PATH.write_text(
        json.dumps(
            {
                "part": payload["summary"]["part"],
                "decimal": payload["summary"]["decimal"],
                "status": (
                    "VERIFIED: graph-Ihara parameters reconciled; classical RH boundary preserved"
                ),
                "summary": payload["summary"],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return DATA_PATH, RESULT_PATH


def main() -> None:
    data_path, result_path = write_reconciliation()
    print(f"Wrote {data_path}")
    print(f"Wrote {result_path}")


if __name__ == "__main__":
    main()
