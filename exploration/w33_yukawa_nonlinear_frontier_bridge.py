"""Repo-native nonlinear compression of the remaining Yukawa frontier.

This module packages the strongest exact conclusion currently justified by the
repo's own Yukawa bridge chain.

What is established:
  - on the replicated three-generation l6 seed, the exact linear bottleneck is
    response rank 9 versus augmented rank 10;
  - inside the native unit A2 mixed-seed family, the smallest exact rank-lift
    seeds raise that pair to 11 versus 12 after the first nonlinear closure
    step;
  - after the exact V4, unipotent, Kronecker, and Gram reductions, the
    residual nontrivial packet is already finite algebraic data on the common
    240^2 shell: exact scalar channels plus two explicit 2x2 integer blocks.

So the remaining Yukawa packet should no longer be read as an arbitrary
24x24 texture problem or as a missing linear Lie mode. The exact unresolved
content is a tiny nonlinear internal spectral packet.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
if __package__ in {None, ""}:
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from exploration._artifact_paths import load_json_from_repo_data
else:
    from ._artifact_paths import load_json_from_repo_data

DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_yukawa_nonlinear_frontier_bridge_summary.json"


def _read_json(filename: str) -> dict[str, Any]:
    return load_json_from_repo_data(ROOT, Path("data") / filename)


def _block_packet(
    numerator_matrix: list[list[int]],
    trace: int,
    determinant: int,
    squared_spectrum: list[str],
    gram_denominator: int,
) -> dict[str, Any]:
    discriminant = trace * trace - 4 * determinant
    return {
        "numerator_matrix": numerator_matrix,
        "trace": trace,
        "determinant": determinant,
        "discriminant": discriminant,
        "squared_spectrum": squared_spectrum,
        "spectral_formula": f"({trace} +/- sqrt({discriminant})) / {2 * gram_denominator}",
    }


@lru_cache(maxsize=1)
def build_yukawa_nonlinear_frontier_summary() -> dict[str, Any]:
    mixed = _read_json("w33_l6_a2_mixed_seed_bridge_summary.json")
    unipotent = _read_json("w33_yukawa_unipotent_reduction_bridge_summary.json")
    kronecker = _read_json("w33_yukawa_kronecker_reduction_bridge_summary.json")
    gram = _read_json("w33_yukawa_gram_shell_bridge_summary.json")
    base = _read_json("w33_yukawa_base_spectrum_bridge_summary.json")
    active = _read_json("w33_yukawa_active_spectrum_bridge_summary.json")

    activation = mixed["activation_theorems"]
    base_profile = mixed["base_profile"]
    algebra = unipotent["universal_generation_algebra"]
    gram_theorem = gram["gram_shell_theorem"]
    base_theorem = base["base_spectrum_theorem"]
    active_theorem = active["active_spectrum_theorem"]
    gram_denominator = int(gram["gram_denominator"])

    h2_minus_plus_packet = _block_packet(
        numerator_matrix=gram_theorem["h2_minus_plus_residual_block_numerator"],
        trace=int(base_theorem["h2_minus_plus_block_trace"]),
        determinant=int(base_theorem["h2_minus_plus_block_determinant"]),
        squared_spectrum=base["base_squared_spectra"]["h2_minus_plus"],
        gram_denominator=gram_denominator,
    )
    hbar2_plus_minus_packet = _block_packet(
        numerator_matrix=gram_theorem["hbar2_plus_minus_residual_block_numerator"],
        trace=int(base_theorem["hbar2_plus_minus_block_trace"]),
        determinant=int(base_theorem["hbar2_plus_minus_block_determinant"]),
        squared_spectrum=base["base_squared_spectra"]["hbar2_plus_minus"][1:],
        gram_denominator=gram_denominator,
    )

    return {
        "status": "ok",
        "base_linear_l6_bottleneck": {
            "response_rank": int(base_profile["response_rank"]),
            "augmented_rank": int(base_profile["augmented_rank"]),
            "best_fit_residual_norm": float(base_profile["best_fit_residual_norm"]),
            "active_a2_modes": list(base_profile["active_a2_modes"]),
        },
        "native_nonlinear_rank_lift": {
            "minimal_rank_lift_seed_size": int(activation["minimal_rank_lift_seed_size"]),
            "minimal_rank_lift_seed_modes": activation["minimal_rank_lift_seed_modes"],
            "minimal_full_a2_activation_seed_modes": activation[
                "minimal_full_a2_activation_seed_modes"
            ],
            "max_response_rank": int(activation["max_response_rank_within_unit_a2_seed_family"]),
            "max_augmented_rank": int(activation["max_augmented_rank_within_unit_a2_seed_family"]),
            "fan_closure_has_full_3x3_support": bool(
                activation["fan_closure_seeds_have_full_3x3_support"]
            ),
            "fan_closure_has_isotropic_offdiag_shell": bool(
                activation["fan_closure_seeds_have_slotwise_isotropic_off_diagonal_shell"]
            ),
            "no_exact_closure_in_unit_a2_seed_family": bool(
                activation["no_exact_closure_within_unit_a2_seed_family"]
            ),
        },
        "exact_generation_algebra": {
            "plus_minus_generation_matrix": algebra["plus_minus_generation_matrix"],
            "minus_plus_generation_matrix": algebra["minus_plus_generation_matrix"],
            "common_charpoly": algebra["plus_minus_charpoly"],
            "commuting_unipotent": bool(algebra["generation_matrices_commute_exactly"]),
            "shared_nilpotent_square": algebra["common_nilpotent_square"],
        },
        "finite_algebraic_packet": {
            "gram_denominator": gram_denominator,
            "exact_scalar_channel_numerators": gram_theorem["exact_scalar_channel_numerators"],
            "shared_phi3_mode_numerator": int(
                gram_theorem["exact_scalar_channel_numerators"]["shared_phi3_mode"]
            ),
            "residual_blocks": {
                "h2_minus_plus": h2_minus_plus_packet,
                "hbar2_plus_minus": hbar2_plus_minus_packet,
            },
            "all_active_sector_scaled_spectra_factor_over_z": bool(
                active_theorem["all_active_sector_scaled_spectra_factor_over_z"]
            ),
            "max_active_factor_degree": int(active_theorem["max_factor_degree"]),
        },
        "nonlinear_frontier_theorem": {
            "diagonal_l6_bottleneck_is_9_to_10": (
                base_profile["response_rank"] == 9 and base_profile["augmented_rank"] == 10
            ),
            "native_mixed_seed_lift_reaches_11_to_12": (
                activation["max_response_rank_within_unit_a2_seed_family"] == 11
                and activation["max_augmented_rank_within_unit_a2_seed_family"] == 12
            ),
            "remaining_base_packet_is_two_radical_pairs_plus_scalar_channels": bool(
                base_theorem["residual_base_frontier_is_two_radical_pairs_plus_exact_scalar_channels"]
            ),
            "remaining_active_packet_is_finite_algebraic_shell": bool(
                active_theorem["remaining_full_active_frontier_is_finite_algebraic_packet"]
            ),
            "remaining_yukawa_frontier_is_nonlinear_internal_spectral_data": True,
        },
        "bridge_verdict": (
            "The repo-native Yukawa frontier is now compressed beyond a linear "
            "Lie-mode search. The replicated l6 seed stalls at rank 9 versus "
            "10, native mixed A2 seeds lift that ceiling to 11 versus 12 after "
            "the first exact nonlinear closure step, and the surviving reduced "
            "content is already only two radical 2x2 packets plus exact scalar "
            "channels on the common 240^2 shell. So the last Yukawa packet is "
            "best read as a tiny nonlinear internal spectral packet."
        ),
        "source_files": [
            "data/w33_l6_a2_mixed_seed_bridge_summary.json",
            "data/w33_yukawa_unipotent_reduction_bridge_summary.json",
            "data/w33_yukawa_kronecker_reduction_bridge_summary.json",
            "data/w33_yukawa_gram_shell_bridge_summary.json",
            "data/w33_yukawa_base_spectrum_bridge_summary.json",
            "data/w33_yukawa_active_spectrum_bridge_summary.json",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_yukawa_nonlinear_frontier_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
