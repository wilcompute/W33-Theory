#!/usr/bin/env python3
"""Canonical exact flavor spine for the live W33 repo.

This bridge reconciles the exact flavor layers that already existed before the
late paper-only §§83-91 stack:

1. The local action-backbone generator:
      tan(theta_C) = q / Phi_3 = 3/13.
2. The global observable Cabibbo packet:
      lambda = q^2 / v = 9/40,
   where v = |W(3,3)| = 40 and v - 1 = q * Phi_3 = 39, so
      lambda = (q / Phi_3) * ((v - 1) / v).
3. The exact Levi-family Wolfenstein packet at lambda = 9/40.
4. The exact projective-incidence PMNS packet:
      sin^2(theta_12) = 4/13, sin^2(theta_23) = 7/13, sin^2(theta_13) = 2/91.

The point is constructive: the repo does not merely have a "flavor audit."
It already has a canonical exact flavor spine. The real remaining flavor wall
is the phenomenology correction layer on top of that exact spine, with the
atmospheric PMNS angle as the main residual mismatch.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
import json
import math
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

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

try:
    from exploration.w33_levi_wolfenstein_bridge import build_summary as build_levi_wolfenstein_summary  # noqa: E402
except ModuleNotFoundError:
    from w33_levi_wolfenstein_bridge import build_summary as build_levi_wolfenstein_summary  # noqa: E402

try:
    from exploration.w33_standard_model_action_backbone_bridge import (  # noqa: E402
        build_standard_model_action_backbone_summary,
    )
except ModuleNotFoundError:
    from w33_standard_model_action_backbone_bridge import build_standard_model_action_backbone_summary  # noqa: E402


Q = 3
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
MU = Q + 1
TANGENT_SECTOR = Q - 1
V_W33 = (Q + 1) * PHI4

PDG_2025_CKM = {
    "source_url": "https://pdg.lbl.gov/2025/reviews/rpp2025-rev-ckm-matrix.pdf",
    "lambda": 0.22501,
    "A": 0.826,
    "rho_bar": 0.1591,
    "eta_bar": 0.3523,
    "Vus": 0.22501,
    "Vcb": 0.04183,
    "Vub": 0.003732,
    "Jarlskog": 3.12e-5,
    "delta_rad": 1.147,
}

NUFIT_6_1_IC24_NO = {
    "source_url": "https://www.nu-fit.org/sites/default/files/v61.tbl-parameters.pdf",
    "sin2_theta12": 0.3088,
    "sin2_theta13": 0.02248,
    "sin2_theta23": 0.470,
    "delta_cp_deg": 212.0,
}


def _fraction_payload(value: Fraction) -> Dict[str, Any]:
    return {"exact": str(value), "float": float(value)}


def _relative_error(predicted: float, observed: float) -> float:
    return abs(predicted - observed) / abs(observed)


@lru_cache(maxsize=1)
def exact_action_packet() -> Dict[str, Any]:
    summary = build_standard_model_action_backbone_summary()
    mixing = summary["mixing_backbone"]

    tan_theta_c = Fraction(mixing["tan_theta_c"]["exact"])
    pmns_12 = Fraction(mixing["sin2_theta_12"]["exact"])
    pmns_23 = Fraction(mixing["sin2_theta_23"]["exact"])
    pmns_13 = Fraction(mixing["sin2_theta_13"]["exact"])

    sin_theta_c = tan_theta_c.numerator / math.sqrt(tan_theta_c.denominator**2 + tan_theta_c.numerator**2)

    return {
        "tan_theta_c": _fraction_payload(tan_theta_c),
        "sin_theta_c_from_exact_tangent": {"float": sin_theta_c},
        "pmns": {
            "sin2_theta12": _fraction_payload(pmns_12),
            "sin2_theta23": _fraction_payload(pmns_23),
            "sin2_theta13": _fraction_payload(pmns_13),
        },
    }


@lru_cache(maxsize=1)
def exact_global_cabibbo_packet() -> Dict[str, Any]:
    local_generator = Fraction(Q, PHI3)
    visibility_factor = Fraction(V_W33 - 1, V_W33)
    lambda_global = Fraction(Q * Q, V_W33)

    return {
        "q": Q,
        "phi3": PHI3,
        "phi4": PHI4,
        "v_w33": V_W33,
        "local_generator_tan_theta_c": _fraction_payload(local_generator),
        "visibility_factor": _fraction_payload(visibility_factor),
        "lambda_global": _fraction_payload(lambda_global),
    }


@lru_cache(maxsize=1)
def exact_levi_ckm_packet() -> Dict[str, Any]:
    summary = build_levi_wolfenstein_summary()
    dictionary = summary["levi_wolfenstein_dictionary"]
    packet = summary["levi_wolfenstein_packet"]

    return {
        "lambda": _fraction_payload(Fraction(dictionary["lambda"]["exact"])),
        "A": dictionary["A_parameter"]["value"],
        "rho_bar": float(dictionary["rho_bar"]),
        "eta_bar": float(dictionary["eta_bar"]),
        "delta_rad": float(dictionary["delta_phase"]["value_rad"]),
        "Vus": float(packet["Vus"]),
        "Vcb": float(packet["Vcb"]),
        "Vub": float(packet["Vub"]),
        "Jarlskog": float(packet["Jarlskog"]),
    }


@lru_cache(maxsize=1)
def classify_exact_flavor_spine() -> tuple[Dict[str, Any], ...]:
    action = exact_action_packet()
    global_cabibbo = exact_global_cabibbo_packet()
    levi = exact_levi_ckm_packet()
    ckm = PDG_2025_CKM
    nu = NUFIT_6_1_IC24_NO

    local_sine = action["sin_theta_c_from_exact_tangent"]["float"]
    global_lambda = global_cabibbo["lambda_global"]["float"]

    pmns_12 = action["pmns"]["sin2_theta12"]["float"]
    pmns_23 = action["pmns"]["sin2_theta23"]["float"]
    pmns_13 = action["pmns"]["sin2_theta13"]["float"]

    return (
        {
            "name": "local_generator_backbone",
            "support_level": "repo-exact action backbone",
            "statement": (
                "The local flavor generator is exactly tan(theta_C)=q/Phi_3=3/13, "
                "shared with the electroweak generator in the action-backbone theorem."
            ),
            "evidence": {
                "tan_theta_c": action["tan_theta_c"],
                "sin_theta_c_from_exact_tangent": local_sine,
                "pmns_12": action["pmns"]["sin2_theta12"],
                "pmns_23": action["pmns"]["sin2_theta23"],
                "pmns_13": action["pmns"]["sin2_theta13"],
            },
        },
        {
            "name": "global_cabibbo_visibility_bridge",
            "support_level": "repo-exact geometric bridge",
            "statement": (
                "The observable CKM lambda is the global size-renormalized form of the "
                "local generator: lambda=q^2/v=9/40=(q/Phi_3)*((v-1)/v)."
            ),
            "evidence": {
                "v_w33": V_W33,
                "v_minus_1": V_W33 - 1,
                "q_phi3": Q * PHI3,
                "local_generator_tan_theta_c": global_cabibbo["local_generator_tan_theta_c"],
                "visibility_factor": global_cabibbo["visibility_factor"],
                "lambda_global": global_cabibbo["lambda_global"],
                "local_tangent_sine_relative_error": _relative_error(local_sine, ckm["lambda"]),
                "global_lambda_relative_error": _relative_error(global_lambda, ckm["lambda"]),
            },
        },
        {
            "name": "levi_ckm_packet",
            "support_level": "repo-exact Levi Wolfenstein closure",
            "statement": (
                "The exact Levi-family packet is the canonical observable CKM route in the "
                "live repo. It closes lambda, A, rho_bar, eta_bar, delta, Vcb, Vub, and J."
            ),
            "evidence": {
                "pdg_2025_ckm": ckm,
                "levi_packet": levi,
                "lambda_relative_error": _relative_error(levi["Vus"], ckm["Vus"]),
                "Vcb_relative_error": _relative_error(levi["Vcb"], ckm["Vcb"]),
                "Vub_relative_error": _relative_error(levi["Vub"], ckm["Vub"]),
                "J_relative_error": _relative_error(levi["Jarlskog"], ckm["Jarlskog"]),
                "delta_relative_error": _relative_error(levi["delta_rad"], ckm["delta_rad"]),
            },
        },
        {
            "name": "incidence_pmns_packet",
            "support_level": "repo-exact incidence geometry",
            "statement": (
                "The canonical exact PMNS packet is the incidence-geometry decomposition "
                "4/13, 7/13, 2/91. Solar and reactor remain tight; atmospheric is the "
                "largest phenomenology residual on top of the exact finite spine."
            ),
            "evidence": {
                "nufit_6_1_ic24_no": nu,
                "exact_pmns": {
                    "sin2_theta12": pmns_12,
                    "sin2_theta23": pmns_23,
                    "sin2_theta13": pmns_13,
                },
                "solar_relative_error": _relative_error(pmns_12, nu["sin2_theta12"]),
                "atmospheric_relative_error": _relative_error(pmns_23, nu["sin2_theta23"]),
                "reactor_relative_error": _relative_error(pmns_13, nu["sin2_theta13"]),
            },
        },
    )


@lru_cache(maxsize=1)
def analyze() -> Dict[str, Any]:
    records = classify_exact_flavor_spine()
    theorem = {
        "the_local_cabibbo_generator_is_exactly_q_over_phi3": (
            exact_action_packet()["tan_theta_c"]["exact"] == "3/13"
        ),
        "the_global_observable_lambda_is_exactly_q_squared_over_v": (
            exact_global_cabibbo_packet()["lambda_global"]["exact"] == "9/40"
        ),
        "the_global_lambda_equals_the_local_generator_times_the_w33_visibility_factor": (
            Fraction(exact_global_cabibbo_packet()["lambda_global"]["exact"])
            == Fraction(exact_global_cabibbo_packet()["local_generator_tan_theta_c"]["exact"])
            * Fraction(exact_global_cabibbo_packet()["visibility_factor"]["exact"])
        ),
        "the_global_lambda_outperforms_the_raw_local_tangent_projection_against_current_pdg_data": (
            records[1]["evidence"]["global_lambda_relative_error"]
            < records[1]["evidence"]["local_tangent_sine_relative_error"]
        ),
        "the_exact_levi_packet_uses_the_same_lambda_as_the_global_size_bridge": (
            exact_levi_ckm_packet()["lambda"]["exact"]
            == exact_global_cabibbo_packet()["lambda_global"]["exact"]
        ),
        "the_exact_pmns_packet_is_the_incidence_geometry_ratio_4_13_7_13_2_91": (
            exact_action_packet()["pmns"]["sin2_theta12"]["exact"] == "4/13"
            and exact_action_packet()["pmns"]["sin2_theta23"]["exact"] == "7/13"
            and exact_action_packet()["pmns"]["sin2_theta13"]["exact"] == "2/91"
        ),
    }

    return {
        "status": "ok",
        "reference_data": {
            "pdg_2025_ckm": PDG_2025_CKM,
            "nufit_6_1_ic24_no": NUFIT_6_1_IC24_NO,
        },
        "records": records,
        "exact_flavor_spine_theorem": theorem,
        "bridge_verdict": (
            "The exact flavor spine is now constructive and canonical in the repo: "
            "the local generator is tan(theta_C)=3/13, the global observable CKM "
            "lambda is its W33-size renormalization q^2/v=9/40, the Levi-family "
            "Wolfenstein packet is the canonical observable CKM closure, and the "
            "projective-incidence packet 4/13, 7/13, 2/91 is the canonical exact "
            "PMNS theorem. The main residual phenomenology wall is no longer Cabibbo "
            "or reactor-angle discovery; it is the atmospheric-angle correction layer "
            "and the still-open Yukawa spectrum."
        ),
    }


def main() -> None:
    started = time.time()
    payload = analyze()
    payload["analysis_duration_sec"] = round(time.time() - started, 6)

    output_dir = ROOT / "checks"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CXX_exact_flavor_spine_bridge_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("Exact flavor spine bridge")
    for key, value in payload["exact_flavor_spine_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")
    print(f"  Wrote: {output_path}")


if __name__ == "__main__":
    main()
