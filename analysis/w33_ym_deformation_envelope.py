"""Part MCLXII: Yang-Mills gap-shell deformation envelope for W(3,3).

This module reconciles the live MCLI substrate gap calculation with the
canonical W33 spectrum:

  normalized Laplacian spectrum = {0^1, (5/6)^24, (4/3)^15}
  S_holo / (5/6) = 20 / (5/6) = 24 = mult(5/6)

The one-parameter Davis-Kahan envelope closes at 25/18.  The older 25/144
number is retained as the E8-rank distributed per-channel safe radius:

  (25/18) / 8 = 25/144.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.w33_geometry import adjacency_matrix, verify_srg  # noqa: E402


V = 40
K = 12
LAMBDA = 2
MU = 4
R = 2
S = -4
M_R = 24
M_S = 15
EDGES = V * K // 2
G_N = Fraction(K, MU)
S_HOLO = Fraction(EDGES, 4 * G_N)
NU_GAP = Fraction(K - R, K)
NU_UV = Fraction(K - S, K)
DAVIS_KAHAN_COEFFICIENT = Fraction(2 * K, V)
EPS_CRITICAL = NU_GAP / DAVIS_KAHAN_COEFFICIENT
E8_RANK = 8
E8_RANK_CHANNEL_RADIUS = EPS_CRITICAL / E8_RANK


def exact_entry(value: Fraction | int) -> dict[str, object]:
    fraction = Fraction(value)
    return {
        "fraction": str(fraction),
        "numerator": fraction.numerator,
        "denominator": fraction.denominator,
        "float": float(fraction),
    }


def normalized_laplacian_matrix(weight: Fraction | int = 1) -> np.ndarray:
    """Return the normalized Laplacian for a uniform edge-weight rescaling."""
    scale = Fraction(weight)
    if scale <= 0:
        raise ValueError("uniform edge weight must be positive")
    adjacency = adjacency_matrix().astype(float) * float(scale)
    degrees = adjacency.sum(axis=1)
    inv_sqrt = np.diag(1.0 / np.sqrt(degrees))
    return np.eye(V) - inv_sqrt @ adjacency @ inv_sqrt


def normalized_spectrum_counts() -> dict[str, int]:
    """Compute the normalized Laplacian spectrum from the actual W33 matrix."""
    eigenvalues = np.linalg.eigvalsh(normalized_laplacian_matrix())
    counts: Counter[str] = Counter()
    for value in eigenvalues:
        if abs(value) < 1e-10:
            counts["0"] += 1
        elif abs(value - float(NU_GAP)) < 1e-10:
            counts[str(NU_GAP)] += 1
        elif abs(value - float(NU_UV)) < 1e-10:
            counts[str(NU_UV)] += 1
        else:
            raise AssertionError(f"unexpected normalized eigenvalue {value!r}")
    return dict(counts)


def gap_lower_bound(epsilon: Fraction | int) -> Fraction:
    """Davis-Kahan lower envelope for the W33 normalized mass gap."""
    return NU_GAP - Fraction(epsilon) * DAVIS_KAHAN_COEFFICIENT


def uniform_rescale_errors() -> dict[str, str]:
    """Check that uniform edge scaling leaves L_hat unchanged."""
    base = normalized_laplacian_matrix()
    samples = (Fraction(1, 2), Fraction(4, 3), Fraction(3), Fraction(25, 18))
    errors: dict[str, str] = {}
    for scale in samples:
        shifted = normalized_laplacian_matrix(scale)
        max_error = float(np.max(np.abs(shifted - base)))
        if max_error < 1e-12:
            max_error = 0.0
        errors[str(scale)] = f"{max_error:.1e}"
    return errors


def ym_deformation_envelope_packet() -> dict[str, object]:
    """Return the exact MCLXII deformation-envelope certificate."""
    srg = verify_srg()
    spectrum_counts = normalized_spectrum_counts()
    gap_shell_ratio = S_HOLO / NU_GAP
    safe_gap = gap_lower_bound(E8_RANK_CHANNEL_RADIUS)
    eight_channel_total = E8_RANK * E8_RANK_CHANNEL_RADIUS
    uniform_errors = uniform_rescale_errors()

    checks = {
        "srg_parameters_verified": srg["vertices"] == V
        and srg["degree"] == K
        and srg["lambda_parameter"] == LAMBDA
        and srg["mu_parameter"] == MU,
        "normalized_gap_value_is_5_over_6": NU_GAP == Fraction(5, 6),
        "normalized_uv_value_is_4_over_3": NU_UV == Fraction(4, 3),
        "gap_multiplicity_is_24": spectrum_counts == {"0": 1, "5/6": 24, "4/3": 15},
        "S_holo_equals_20": S_HOLO == 20,
        "gap_shell_ratio_equals_multiplicity": gap_shell_ratio == M_R == 24,
        "uv_multiplicity_is_su4_adjoint_count": M_S == 15,
        "davis_kahan_coefficient_is_3_over_5": DAVIS_KAHAN_COEFFICIENT == Fraction(3, 5),
        "one_parameter_critical_radius_is_25_over_18": EPS_CRITICAL == Fraction(25, 18),
        "rank_channel_radius_is_25_over_144": E8_RANK_CHANNEL_RADIUS == Fraction(25, 144),
        "rank_channel_radius_is_one_eighth_of_critical": eight_channel_total == EPS_CRITICAL,
        "safe_radius_keeps_positive_gap": safe_gap == Fraction(35, 48) and safe_gap > 0,
        "uniform_scaling_is_lhat_invariant": all(error == "0.0e+00" for error in uniform_errors.values()),
    }

    return {
        "part": "MCLXII",
        "theorem": "Yang-Mills gap-shell deformation envelope",
        "parameters": {
            "v": V,
            "k": K,
            "lambda": LAMBDA,
            "mu": MU,
            "r": R,
            "s": S,
            "m_r": M_R,
            "m_s": M_S,
            "edges": EDGES,
        },
        "normalized_laplacian_spectrum": [
            {"eigenvalue": "0", "multiplicity": 1},
            {"eigenvalue": str(NU_GAP), "multiplicity": M_R},
            {"eigenvalue": str(NU_UV), "multiplicity": M_S},
        ],
        "gap_shell_lock": {
            "S_holo": exact_entry(S_HOLO),
            "nu_gap": exact_entry(NU_GAP),
            "S_holo_over_nu_gap": exact_entry(gap_shell_ratio),
            "gap_multiplicity": M_R,
            "dim_su5_adjoint": 24,
            "uv_multiplicity": M_S,
            "dim_su4_adjoint": 15,
            "lock_verified": gap_shell_ratio == M_R == 24,
        },
        "deformation_envelope": {
            "davis_kahan_coefficient": exact_entry(DAVIS_KAHAN_COEFFICIENT),
            "gap_lower_bound": "nu_gap - epsilon*(3/5)",
            "one_parameter_critical_radius": exact_entry(EPS_CRITICAL),
            "e8_rank": E8_RANK,
            "rank_distributed_per_channel_radius": exact_entry(E8_RANK_CHANNEL_RADIUS),
            "eight_channels_saturate_exact_radius": exact_entry(eight_channel_total),
            "gap_lower_at_rank_channel_radius": exact_entry(safe_gap),
            "classification": (
                "25/18 is the one-parameter closure radius; 25/144 is the "
                "rank-8 per-channel strict safe radius."
            ),
        },
        "uniform_scaling": {
            "statement": "A -> cA and D -> cD leave L_hat = I - D^{-1/2} A D^{-1/2} unchanged.",
            "sample_max_errors": uniform_errors,
            "invariant": all(error == "0.0e+00" for error in uniform_errors.values()),
        },
        "claim_boundary": (
            "finite W33 normalized-Laplacian mass-gap envelope; continuum Yang-Mills "
            "remains a limit/identification bridge"
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = ym_deformation_envelope_packet()
    out_path = ROOT / "PART_MCLXII_YM_DEFORMATION_ENVELOPE_results.json"
    data_path = ROOT / "data" / "w33_ym_deformation_envelope.json"
    data_path.parent.mkdir(exist_ok=True)
    with open(out_path, "w") as fh:
        json.dump(packet, fh, indent=2)
    with open(data_path, "w") as fh:
        json.dump(packet, fh, indent=2)

    print("=== Part MCLXII: Yang-Mills Gap-Shell Deformation Envelope ===")
    print(f"  spectrum: {packet['normalized_laplacian_spectrum']}")
    print("  S_holo/nu_gap = 24 = mult(nu_gap)")
    print("  eps_c = 25/18; rank-channel safe radius = 25/144")
    print(f"  verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
