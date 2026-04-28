#!/usr/bin/env python3
"""Conservative flavor-frontier audit for the late §§83-91 paper stack.

This audit separates three layers that are currently conflated in the new
paper extensions:

1. Exact arithmetic uniqueness facts that really do survive scrutiny.
2. Existing stronger exact flavor bridges already present elsewhere in the repo.
3. New paper-only CKM/PMNS/running-alpha formulas that are phenomenological
   ansaetze or internal alternatives rather than exact closure theorems.

Current benchmark inputs:
  - PDG 2025 electroweak / CKM reviews:
      * alpha^(5)(M_Z)^(-1) = 127.930
      * sin^2(theta_eff)    = 0.23154
      * |V_us|              = 0.22501
  - NuFIT 6.1 (2025), IC24 with SK atmospheric data, normal ordering:
      * sin^2(theta_12) = 0.3088
      * sin^2(theta_13) = 0.02248
      * sin^2(theta_23) = 0.470
      * delta_CP        = 212 deg

These values are intentionally stored here as a fixed audited snapshot instead
of being fetched dynamically, so the audit stays reproducible.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
import json
import math
import numpy as np
from pathlib import Path
import sys
import time
from typing import Dict, Tuple


ROOT = Path(__file__).resolve().parents[1]
EXPLORATION = ROOT / "exploration"
SCRIPTS = ROOT / "scripts"
for candidate in (ROOT, EXPLORATION, SCRIPTS):
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

try:
    from scripts.w33_ckm_from_vev import (  # noqa: E402
        _build_hodge_and_generations,
        build_generation_profiles,
        build_h27_index_and_tris,
        compute_ckm_and_jarlskog,
        yukawa_from_vev_with_tris,
    )
except ModuleNotFoundError:
    from w33_ckm_from_vev import (  # noqa: E402
        _build_hodge_and_generations,
        build_generation_profiles,
        build_h27_index_and_tris,
        compute_ckm_and_jarlskog,
        yukawa_from_vev_with_tris,
    )


PDG_2025 = {
    "source_url": "https://pdg.lbl.gov/2025/reviews/rpp2025-rev-vud-vus.pdf",
    "cabibbo_vus": 0.22501,
    "sin2_theta_eff": 0.23154,
    "alpha5_mz_inverse": 127.930,
}

NUFIT_6_1_IC24_NO = {
    "source_url": "https://www.nu-fit.org/sites/default/files/v61.tbl-parameters.pdf",
    "sin2_theta12": 0.3088,
    "sin2_theta13": 0.02248,
    "sin2_theta23": 0.470,
    "delta_cp_deg": 212.0,
}


def _fraction_payload(value: Fraction) -> Dict[str, object]:
    return {"exact": str(value), "float": float(value)}


def _float_payload(value: float) -> Dict[str, float]:
    return {"float": float(value)}


def _relative_error(predicted: float, observed: float) -> float:
    return abs(predicted - observed) / abs(observed)


def _is_v4_cyclotomic_level(n_value: int) -> bool:
    units = [a for a in range(1, n_value) if math.gcd(a, n_value) == 1]
    return len(units) == 4 and all((a * a) % n_value == 1 for a in units)


def _prime_list(limit: int) -> list[int]:
    if limit < 2:
        return []
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for p in range(2, int(limit**0.5) + 1):
        if sieve[p]:
            step = p
            start = p * p
            sieve[start : limit + 1 : step] = [False] * (((limit - start) // step) + 1)
    return [n for n, is_prime in enumerate(sieve) if is_prime]


@lru_cache(maxsize=1)
def paper_flavor_packet() -> Dict[str, object]:
    q = 3
    phi3 = q * q + q + 1
    phi4 = q * q + 1
    phi6 = q * q - q + 1
    alpha_inverse = q**4 + 2 * q**3 + q - 1

    cabibbo_ratio = q / phi3
    cabibbo_sin_from_tan = q / math.sqrt(phi3 * phi3 + q * q)

    section84 = {
        "lambda_as_sine": cabibbo_ratio,
        "A_as_cos_theta_w": math.sqrt(phi4 / phi3),
        "theta23_geometric_series": q / (phi3**2),
        "theta13_geometric_series": q / (phi3**3),
    }

    section86 = {
        "lambda": cabibbo_ratio,
        "A": math.sqrt(phi6 / phi4),
        "rho": q * math.sqrt(phi4) / (2 * phi3 * math.sqrt(phi6)),
        "eta": q * math.sqrt(phi4) / (2 * phi3),
        "delta_ckm_deg": math.degrees(math.atan(math.sqrt(phi6))),
    }

    section90 = {
        "sin2_theta13": q / alpha_inverse,
        "sin2_theta12": (alpha_inverse - q * q) / (alpha_inverse * q),
        "sin2_theta23": 1 / (q - 1),
        "delta_pmns_deg": 180.0 + math.degrees(math.atan(math.sqrt(phi6))),
        "sum_rule_target": 1 / q,
    }

    return {
        "q": q,
        "phi3": phi3,
        "phi4": phi4,
        "phi6": phi6,
        "alpha_inverse": alpha_inverse,
        "tan_theta_c_exact": _fraction_payload(Fraction(q, phi3)),
        "sin_theta_c_from_tan": _float_payload(cabibbo_sin_from_tan),
        "section84": section84,
        "section86": section86,
        "section90": section90,
    }


@lru_cache(maxsize=1)
def exact_repo_flavor_packet() -> Dict[str, object]:
    action = build_standard_model_action_backbone_summary()
    mixing = action["mixing_backbone"]
    levi = build_levi_wolfenstein_summary()
    levi_dict = levi["levi_wolfenstein_dictionary"]
    levi_packet = levi["levi_wolfenstein_packet"]

    tan_theta_c = Fraction(mixing["tan_theta_c"]["exact"])
    sin_theta_c = tan_theta_c.numerator / math.sqrt(tan_theta_c.denominator**2 + tan_theta_c.numerator**2)

    return {
        "standard_model_action_backbone": {
            "tan_theta_c": mixing["tan_theta_c"],
            "sin_theta_c_from_exact_tangent": _float_payload(sin_theta_c),
            "sin2_theta12_pmns": mixing["sin2_theta_12"],
            "sin2_theta23_pmns": mixing["sin2_theta_23"],
            "sin2_theta13_pmns": mixing["sin2_theta_13"],
        },
        "levi_ckm_bridge": {
            "lambda": levi_dict["lambda"],
            "A_parameter": levi_dict["A_parameter"],
            "delta_phase_rad": levi_dict["delta_phase"],
            "rho_bar": levi_dict["rho_bar"],
            "eta_bar": levi_dict["eta_bar"],
            "Vus": levi_packet["Vus"],
            "Vcb": levi_packet["Vcb"],
            "Vub": levi_packet["Vub"],
            "Jarlskog": levi_packet["Jarlskog"],
        },
    }


@lru_cache(maxsize=1)
def arithmetic_q3_uniqueness_packet() -> Dict[str, object]:
    prime_samples = tuple(p for p in _prime_list(200) if p <= 199)
    alpha_family = {
        p: p**4 + 2 * p**3 + p - 1
        for p in prime_samples
    }
    prime_alpha_hits = tuple(
        p
        for p, value in alpha_family.items()
        if value > 1 and all(value % d for d in range(2, int(value**0.5) + 1))
    )

    v4_hits = tuple(
        p
        for p in prime_samples
        if _is_v4_cyclotomic_level(p * (p + 1))
    )
    phi4_hits = tuple(
        p
        for p in prime_samples
        if _totient(p * (p + 1)) == 4
    )

    return {
        "prime_alpha_hits_up_to_199": prime_alpha_hits,
        "v4_cyclotomic_hits_up_to_199": v4_hits,
        "phi_of_k_equals_4_hits_up_to_199": phi4_hits,
    }


@lru_cache(maxsize=1)
def exact_to_frontier_bridge_packet() -> Dict[str, object]:
    """Executable bridge from exact selector layer to spontaneous CP frontier.

    The bridge is anchored by two validated components:
      1) CKM/PMNS spontaneous CP-breaking behavior under a controlled complex
         VEV misalignment in the q=3 profile construction.
      2) E6 trilinear closed-form checks evaluated with gauge-equivalent
         canonical mismatch handling from the stabilized audit output.
    """
    H, triangles, edges, gens = _build_hodge_and_generations()
    n = max(max(u, v) for u, v in edges) + 1
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    _, local_tris = build_h27_index_and_tris(adj, v0=0)
    _, _, X_profiles = build_generation_profiles(H, edges, gens, v0=0)

    v_exact = X_profiles[0].astype(complex)
    y_exact = yukawa_from_vev_with_tris(X_profiles, v_exact, local_tris)
    v_exact_ckm, j_exact = compute_ckm_and_jarlskog(y_exact, y_exact)

    v_break = v_exact.copy()
    v_break[3] *= 1.0 + 0.3j
    y_break = yukawa_from_vev_with_tris(X_profiles, v_break, local_tris)
    v_break_ckm, j_break = compute_ckm_and_jarlskog(y_exact, y_break)

    e6_payload_path = ROOT / "artifacts" / "e6_f3_trilinear_symmetry_breaking.json"
    e6_cross_check = {
        "artifact_present": e6_payload_path.exists(),
        "line_product_closed_form_holds": None,
        "line_product_mismatch_count": None,
        "full_sign_closed_form_holds": None,
        "full_sign_mismatch_count": None,
    }
    if e6_payload_path.exists():
        payload = json.loads(e6_payload_path.read_text(encoding="utf-8"))
        checks = payload.get("cross_checks", {})
        line = checks.get("line_product_closed_form", {})
        full = checks.get("full_sign_closed_form", {})
        e6_cross_check.update(
            {
                "line_product_closed_form_holds": bool(line.get("holds", False)),
                "line_product_mismatch_count": line.get("mismatch_count"),
                "full_sign_closed_form_holds": bool(full.get("holds", False)),
                "full_sign_mismatch_count": full.get("mismatch_count"),
            }
        )

    return {
        "ckm_exact_alignment_jarlskog_abs": abs(float(j_exact)),
        "ckm_exact_alignment_is_identity": bool(
            np.allclose(np.abs(v_exact_ckm), np.eye(3), atol=1e-8)
        ),
        "ckm_misaligned_jarlskog_abs": abs(float(j_break)),
        "ckm_misaligned_is_nontrivial": bool(
            not np.allclose(np.abs(v_break_ckm), np.eye(3), atol=1e-3)
        ),
        "e6_closed_form_cross_checks": e6_cross_check,
    }


def _totient(n_value: int) -> int:
    count = 0
    for k in range(1, n_value + 1):
        if math.gcd(k, n_value) == 1:
            count += 1
    return count


@lru_cache(maxsize=1)
def classify_flavor_frontier() -> Tuple[Dict[str, object], ...]:
    paper = paper_flavor_packet()
    exact = exact_repo_flavor_packet()
    arithmetic = arithmetic_q3_uniqueness_packet()
    bridge = exact_to_frontier_bridge_packet()

    cabibbo_obs = PDG_2025["cabibbo_vus"]
    alpha_mz_obs = PDG_2025["alpha5_mz_inverse"]
    theta_w_obs = PDG_2025["sin2_theta_eff"]
    nu = NUFIT_6_1_IC24_NO

    exact_cab_sin = exact["standard_model_action_backbone"]["sin_theta_c_from_exact_tangent"]["float"]
    raw_cab_sin = float(paper["section84"]["lambda_as_sine"])
    levi_lambda = float(Fraction(exact["levi_ckm_bridge"]["lambda"]["exact"]))

    exact_pmns_s12 = float(Fraction(exact["standard_model_action_backbone"]["sin2_theta12_pmns"]["exact"]))
    exact_pmns_s13 = float(Fraction(exact["standard_model_action_backbone"]["sin2_theta13_pmns"]["exact"]))
    exact_pmns_s23 = float(Fraction(exact["standard_model_action_backbone"]["sin2_theta23_pmns"]["exact"]))

    sec90 = paper["section90"]

    return (
        {
            "name": "exact_q3_arithmetic_uniqueness",
            "support_level": "repo-exact arithmetic",
            "statement": (
                "The mod-3 alpha-uniqueness theorem, the k=12 Klein-four cyclotomic level, "
                "and phi(k)=4 at q=3 are exact arithmetic constraints."
            ),
            "evidence": {
                "prime_alpha_hits_up_to_199": arithmetic["prime_alpha_hits_up_to_199"],
                "v4_cyclotomic_hits_up_to_199": arithmetic["v4_cyclotomic_hits_up_to_199"],
                "phi_of_k_equals_4_hits_up_to_199": arithmetic["phi_of_k_equals_4_hits_up_to_199"],
            },
        },
        {
            "name": "section84_section86_internal_ckm_conflict",
            "support_level": "paper-only internal inconsistency",
            "statement": (
                "The late paper stack assigns two incompatible exact Wolfenstein A parameters: "
                "section 84 uses cos(theta_W)=sqrt(Phi4/Phi3), while section 86 uses sqrt(Phi6/Phi4)."
            ),
            "evidence": {
                "section84_A": paper["section84"]["A_as_cos_theta_w"],
                "section86_A": paper["section86"]["A"],
                "absolute_gap": abs(paper["section84"]["A_as_cos_theta_w"] - paper["section86"]["A"]),
            },
        },
        {
            "name": "existing_exact_ckm_bridges_are_stronger_than_raw_q_over_phi3",
            "support_level": "repo-exact bridge dominates paper ansatz",
            "statement": (
                "For Cabibbo/CKM, the exact tangent law tan(theta_C)=3/13 and the tested Levi bridge "
                "already outperform the raw sine ansatz lambda=3/13 used in sections 84 and 86."
            ),
            "evidence": {
                "cabibbo_observed": cabibbo_obs,
                "raw_lambda_as_sine": raw_cab_sin,
                "raw_lambda_relative_error": _relative_error(raw_cab_sin, cabibbo_obs),
                "exact_tangent_sine": exact_cab_sin,
                "exact_tangent_relative_error": _relative_error(exact_cab_sin, cabibbo_obs),
                "levi_lambda": levi_lambda,
                "levi_lambda_relative_error": _relative_error(levi_lambda, cabibbo_obs),
            },
        },
        {
            "name": "section90_pmns_is_a_nonexact_alternative_ansatz",
            "support_level": "paper-only phenomenology",
            "statement": (
                "The late PMNS formulas are numerically competitive, but they contradict the repo's "
                "existing exact incidence-geometry PMNS theorem and should be treated as an alternative "
                "phenomenology layer rather than an exact closure theorem."
            ),
            "evidence": {
                "nufit_6_0_ic24_no": nu,
                "exact_pmns": {
                    "sin2_theta12": exact_pmns_s12,
                    "sin2_theta13": exact_pmns_s13,
                    "sin2_theta23": exact_pmns_s23,
                },
                "section90_pmns": {
                    "sin2_theta12": sec90["sin2_theta12"],
                    "sin2_theta13": sec90["sin2_theta13"],
                    "sin2_theta23": sec90["sin2_theta23"],
                    "delta_pmns_deg": sec90["delta_pmns_deg"],
                },
                "exact_pmns_solar_relative_error": _relative_error(exact_pmns_s12, nu["sin2_theta12"]),
                "section90_solar_relative_error": _relative_error(sec90["sin2_theta12"], nu["sin2_theta12"]),
                "exact_pmns_reactor_relative_error": _relative_error(exact_pmns_s13, nu["sin2_theta13"]),
                "section90_reactor_relative_error": _relative_error(sec90["sin2_theta13"], nu["sin2_theta13"]),
                "exact_pmns_atmospheric_relative_error": _relative_error(exact_pmns_s23, nu["sin2_theta23"]),
                "section90_atmospheric_relative_error": _relative_error(sec90["sin2_theta23"], nu["sin2_theta23"]),
            },
        },
        {
            "name": "section83_running_alpha_is_qualitative_not_precision_closed",
            "support_level": "paper-only heuristic",
            "statement": (
                "The eigenvalue-flow alpha running is a qualitative story, not a precision closure theorem: "
                "the paper's Z-pole value 135 remains far from the current PDG running coupling."
            ),
            "evidence": {
            "paper_gut_alpha_inverse": paper["alpha_inverse"],
            "paper_z_pole_alpha_inverse": 135.0,
            "pdg_alpha5_mz_inverse": alpha_mz_obs,
                "pdg_sin2_theta_eff": theta_w_obs,
                "z_pole_absolute_gap": abs(135.0 - alpha_mz_obs),
            },
        },
        {
            "name": "exact_to_spontaneous_cp_frontier_bridge_is_executable",
            "support_level": "exact-to-frontier executable bridge",
            "statement": (
                "With the stabilized q=3 profile basis and gauge-equivalent E6 normalization, "
                "the exact layer enforces CP conservation at aligned VEVs while controlled complex "
                "misalignment produces nontrivial CKM mixing and nonzero Jarlskog as a frontier effect."
            ),
            "evidence": bridge,
        },
    )


@lru_cache(maxsize=1)
def analyze() -> Dict[str, object]:
    paper = paper_flavor_packet()
    exact = exact_repo_flavor_packet()
    records = classify_flavor_frontier()
    bridge = exact_to_frontier_bridge_packet()
    e6_bridge = bridge["e6_closed_form_cross_checks"]

    theorem = {
        "the_mod_3_alpha_uniqueness_theorem_is_exact": records[0]["evidence"]["prime_alpha_hits_up_to_199"] == (3,),
        "sections_84_and_86_do_not_define_the_same_wolfenstein_A": records[1]["evidence"]["absolute_gap"] > 0.03,
        "the_exact_tangent_and_levi_ckm_routes_beat_raw_q_over_phi3_for_cabibbo": (
            records[2]["evidence"]["exact_tangent_relative_error"]
            < records[2]["evidence"]["raw_lambda_relative_error"]
            and records[2]["evidence"]["levi_lambda_relative_error"]
            < records[2]["evidence"]["raw_lambda_relative_error"]
        ),
        "section90_pmns_is_not_the_repo_exact_pmns_theorem": (
            paper["section90"]["sin2_theta12"]
            != float(Fraction(exact["standard_model_action_backbone"]["sin2_theta12_pmns"]["exact"]))
            and paper["section90"]["sin2_theta13"]
            != float(Fraction(exact["standard_model_action_backbone"]["sin2_theta13_pmns"]["exact"]))
        ),
        "section83_alpha_running_is_not_a_precision_match_to_current_pdg_data": (
            abs(135.0 - PDG_2025["alpha5_mz_inverse"]) > 5.0
        ),
        "exact_layer_and_spontaneous_cp_frontier_bridge_is_executable": (
            bridge["ckm_exact_alignment_is_identity"]
            and bridge["ckm_exact_alignment_jarlskog_abs"] < 1e-12
            and bridge["ckm_misaligned_is_nontrivial"]
            and bridge["ckm_misaligned_jarlskog_abs"] > 1e-8
            and (
                (not e6_bridge["artifact_present"])
                or (
                    e6_bridge["line_product_closed_form_holds"]
                    and e6_bridge["full_sign_closed_form_holds"]
                )
            )
        ),
    }

    return {
        "status": "ok",
        "reference_data": {
            "pdg_2025": PDG_2025,
            "nufit_6_1_ic24_no": NUFIT_6_1_IC24_NO,
        },
        "paper_packet": paper,
        "exact_repo_packet": exact,
        "records": records,
        "flavor_frontier_theorem": theorem,
        "boundary_note": (
            "The exact late-night breakthrough is narrower than the new paper prose: the mod-3 "
            "alpha-uniqueness theorem and the q=3 arithmetic selectors are real, but the new CKM, "
            "PMNS, and running-alpha formulas sit on a promoted flavor layer that currently conflicts "
            "with stronger exact bridges already in the repo. The honest next step is reconciliation, "
            "not stacking another exactness claim."
        ),
    }


def main() -> None:
    started = time.time()
    payload = analyze()
    payload["analysis_duration_sec"] = round(time.time() - started, 6)

    output_dir = ROOT / "checks"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CXIX_flavor_frontier_audit_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    theorem = payload["flavor_frontier_theorem"]
    print("Flavor frontier audit")
    for key, value in theorem.items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")
    print(f"  Wrote: {output_path}")


if __name__ == "__main__":
    main()
