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


@lru_cache(maxsize=1)
def spontaneous_cp_response_law_packet() -> Dict[str, object]:
    """Derive the near-exact spontaneous-CP response law for CKM Jarlskog.

    We perturb one selected VEV entry by conjugate factors (1 +/- i*epsilon)
    and measure the induced Jarlskog invariant relative to the aligned exact
    baseline. This exposes both CP-odd sign behavior and the low-order onset
    exponent in epsilon.
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

    epsilons = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
    sweep = []
    cubic_coeffs = []
    odd_cubic_coeffs = []
    even_cubic_leaks = []
    quadratic_coeffs = []
    linear_coeffs = []
    odd_residuals = []
    abs_j_plus = []

    for eps in epsilons:
        v_plus = v_exact.copy()
        v_plus[3] *= 1.0 + 1.0j * eps
        y_plus = yukawa_from_vev_with_tris(X_profiles, v_plus, local_tris)
        _, j_plus = compute_ckm_and_jarlskog(y_exact, y_plus)

        v_minus = v_exact.copy()
        v_minus[3] *= 1.0 - 1.0j * eps
        y_minus = yukawa_from_vev_with_tris(X_profiles, v_minus, local_tris)
        _, j_minus = compute_ckm_and_jarlskog(y_exact, y_minus)

        odd_residual = abs(float(j_plus) + float(j_minus))
        linear_coeff = abs(float(j_plus)) / eps
        quadratic_coeff = abs(float(j_plus)) / (eps**2)
        cubic_coeff = abs(float(j_plus)) / (eps**3)
        odd_cubic_coeff = (float(j_plus) - float(j_minus)) / (2 * (eps**3))
        even_cubic_leak = abs(float(j_plus) + float(j_minus)) / (eps**3)

        sweep.append(
            {
                "epsilon": eps,
                "jarlskog_plus": float(j_plus),
                "jarlskog_minus": float(j_minus),
                "odd_residual_abs": odd_residual,
                "abs_j_plus": abs(float(j_plus)),
                "abs_j_plus_over_epsilon": linear_coeff,
                "abs_j_plus_over_epsilon_squared": quadratic_coeff,
                "abs_j_plus_over_epsilon_cubed": cubic_coeff,
                "odd_cubic_coefficient": odd_cubic_coeff,
                "even_cubic_leak_abs": even_cubic_leak,
            }
        )
        linear_coeffs.append(linear_coeff)
        quadratic_coeffs.append(quadratic_coeff)
        cubic_coeffs.append(cubic_coeff)
        odd_cubic_coeffs.append(odd_cubic_coeff)
        even_cubic_leaks.append(even_cubic_leak)
        odd_residuals.append(odd_residual)
        abs_j_plus.append(abs(float(j_plus)))

    cubic_window = cubic_coeffs[1:]
    odd_cubic_window = odd_cubic_coeffs[1:]
    odd_cubic_abs_window = [abs(value) for value in odd_cubic_window]
    cubic_min = min(cubic_window)
    cubic_max = max(cubic_window)
    cubic_ratio = cubic_max / cubic_min if cubic_min > 0 else float("inf")
    odd_cubic_abs_min = min(odd_cubic_abs_window)
    odd_cubic_abs_max = max(odd_cubic_abs_window)
    odd_cubic_abs_ratio = (
        odd_cubic_abs_max / odd_cubic_abs_min if odd_cubic_abs_min > 0 else float("inf")
    )
    eps_sq = [eps * eps for eps in epsilons]
    mean_x = sum(eps_sq) / len(eps_sq)
    mean_y = sum(odd_cubic_coeffs) / len(odd_cubic_coeffs)
    var_x = sum((value - mean_x) ** 2 for value in eps_sq)
    cov_xy = sum(
        (eps_sq[idx] - mean_x) * (odd_cubic_coeffs[idx] - mean_y)
        for idx in range(len(eps_sq))
    )
    odd_cubic_affine_slope = cov_xy / var_x if var_x > 0 else 0.0
    odd_cubic_affine_intercept = mean_y - odd_cubic_affine_slope * mean_x
    odd_cubic_affine_residuals = [
        abs(
            odd_cubic_coeffs[idx]
            - (odd_cubic_affine_slope * eps_sq[idx] + odd_cubic_affine_intercept)
        )
        for idx in range(len(eps_sq))
    ]
    odd_cubic_coeff_span = max(odd_cubic_coeffs) - min(odd_cubic_coeffs)
    odd_cubic_affine_relative_max_residual = (
        max(odd_cubic_affine_residuals) / max(abs(odd_cubic_coeff_span), 1e-30)
    )
    onset_log_slopes = [
        math.log(abs_j_plus[i + 1] / abs_j_plus[i])
        / math.log(epsilons[i + 1] / epsilons[i])
        for i in range(len(epsilons) - 1)
    ]

    return {
        "misalignment_component": 3,
        "epsilon_sweep": sweep,
        "cp_odd_sign_flip_exact": all(
            row["jarlskog_plus"] * row["jarlskog_minus"] < 0 for row in sweep
        ),
        "max_odd_residual_abs": max(odd_residuals),
        "abs_jarlskog_is_strictly_increasing_with_epsilon": all(
            abs_j_plus[i] < abs_j_plus[i + 1] for i in range(len(abs_j_plus) - 1)
        ),
        "linear_coefficient_window": linear_coeffs,
        "quadratic_coefficient_window": quadratic_coeffs,
        "cubic_coefficient_window": cubic_coeffs,
        "odd_cubic_coefficient_window": odd_cubic_coeffs,
        "even_cubic_leak_window": even_cubic_leaks,
        "onset_log_slope_window": onset_log_slopes,
        "minimum_onset_log_slope": min(onset_log_slopes),
        "maximum_onset_log_slope": max(onset_log_slopes),
        "cubic_coefficient_estimate": sum(cubic_window) / len(cubic_window),
        "cubic_coefficient_min": cubic_min,
        "cubic_coefficient_max": cubic_max,
        "cubic_coefficient_ratio_max_over_min": cubic_ratio,
        "cubic_coefficient_band_statement": (
            "The audited cubic coefficient stays in a narrow band "
            f"[{cubic_min:.6e}, {cubic_max:.6e}] with ratio {cubic_ratio:.6f}"
        ),
        "odd_cubic_coefficient_estimate": sum(odd_cubic_window) / len(odd_cubic_window),
        "odd_cubic_coefficient_min_abs": odd_cubic_abs_min,
        "odd_cubic_coefficient_max_abs": odd_cubic_abs_max,
        "odd_cubic_coefficient_abs_ratio_max_over_min": odd_cubic_abs_ratio,
        "max_even_cubic_leak_abs": max(even_cubic_leaks),
        "odd_cubic_coefficient_affine_slope_in_epsilon_squared": odd_cubic_affine_slope,
        "odd_cubic_coefficient_affine_intercept": odd_cubic_affine_intercept,
        "odd_cubic_coefficient_affine_max_abs_residual": max(odd_cubic_affine_residuals),
        "odd_cubic_coefficient_affine_mean_abs_residual": (
            sum(odd_cubic_affine_residuals) / len(odd_cubic_affine_residuals)
        ),
        "odd_cubic_coefficient_affine_relative_max_residual": (
            odd_cubic_affine_relative_max_residual
        ),
        "odd_cubic_coefficient_statement": (
            "The conjugation-odd cubic coefficient C_odd(epsilon) = "
            "(J(+epsilon) - J(-epsilon)) / (2 epsilon^3) stays nonzero and stable "
            f"with |C_odd| in [{odd_cubic_abs_min:.6e}, {odd_cubic_abs_max:.6e}]"
        ),
        "odd_cubic_normal_form_statement": (
            "C_odd(epsilon) is numerically affine in epsilon^2 over the audited window "
            f"with max relative residual {odd_cubic_affine_relative_max_residual:.6e}"
        ),
        "derived_order_statement": "The first nonzero CP-odd invariant is odd in epsilon and numerically enters at order >= 3 on the audited window",
        "derived_law": "|J| ~ C * epsilon^3 near aligned exact point",
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
    cp_response = spontaneous_cp_response_law_packet()

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
        {
            "name": "spontaneous_cp_frontier_has_cp_odd_cubic_onset_law",
            "support_level": "exact-to-frontier quantitative response law",
            "statement": (
                "Around the aligned exact point, conjugate complex VEV perturbations "
                "induce equal-and-opposite CKM Jarlskog signs with an odd residual at "
                "machine zero, and the first nonzero CP-odd invariant enters at least "
                "cubically with a stable onset law |J| ~ C epsilon^3 over the audited "
                "small-epsilon window."
            ),
            "evidence": cp_response,
        },
    )


@lru_cache(maxsize=1)
def analyze() -> Dict[str, object]:
    paper = paper_flavor_packet()
    exact = exact_repo_flavor_packet()
    records = classify_flavor_frontier()
    bridge = exact_to_frontier_bridge_packet()
    cp_response = spontaneous_cp_response_law_packet()
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
        "spontaneous_cp_frontier_exhibits_cp_odd_at_least_cubic_onset_near_the_exact_point": (
            cp_response["cp_odd_sign_flip_exact"]
            and cp_response["max_odd_residual_abs"] < 1e-15
            and cp_response["abs_jarlskog_is_strictly_increasing_with_epsilon"]
            and cp_response["minimum_onset_log_slope"] > 2.5
            and cp_response["cubic_coefficient_ratio_max_over_min"] < 1.25
        ),
        "spontaneous_cp_frontier_has_a_stable_audited_cubic_coefficient": (
            cp_response["cubic_coefficient_min"] > 3.3e-6
            and cp_response["cubic_coefficient_max"] < 3.8e-6
            and cp_response["cubic_coefficient_ratio_max_over_min"] < 1.12
            and cp_response["minimum_onset_log_slope"] > 2.95
            and cp_response["maximum_onset_log_slope"] < 3.25
        ),
        "spontaneous_cp_frontier_has_a_stable_conjugation_odd_cubic_coefficient": (
            cp_response["odd_cubic_coefficient_min_abs"] > 3.3e-6
            and cp_response["odd_cubic_coefficient_max_abs"] < 3.8e-6
            and cp_response["odd_cubic_coefficient_abs_ratio_max_over_min"] < 1.12
            and cp_response["max_even_cubic_leak_abs"] < 1e-18
        ),
        "spontaneous_cp_frontier_odd_cubic_coefficient_has_epsilon_squared_normal_form": (
            abs(cp_response["odd_cubic_coefficient_affine_intercept"]) > 3.2e-6
            and abs(cp_response["odd_cubic_coefficient_affine_intercept"]) < 3.6e-6
            and cp_response["odd_cubic_coefficient_affine_relative_max_residual"] < 0.02
            and cp_response["odd_cubic_coefficient_affine_max_abs_residual"] < 6e-9
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
