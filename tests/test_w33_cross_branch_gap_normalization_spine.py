import importlib.util
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_cross_branch_gap_normalization_spine_packet():
    spine = _load_module(
        ROOT / "analysis" / "w33_cross_branch_gap_normalization_spine.py",
        "w33_cross_branch_gap_normalization_spine",
    )
    packet = spine.cross_branch_gap_normalization_packet()

    assert packet["normalization_spine_detected"]
    assert packet["ym_floor"]["formula_aligned"]
    assert packet["ym_floor"]["p2_floor"]["fraction"] == "1/12"
    assert packet["ym_floor"]["global_floor_scan"]["fraction"] == "1/12"
    assert packet["ym_floor"]["declared_floor"]["fraction"] == "1/12"

    assert packet["navier_stokes"]["delta_matches_ym_floor"]
    assert packet["navier_stokes"]["delta"]["fraction"] == "1/12"
    assert packet["navier_stokes"]["enstrophy_decay_rate_2nu_delta"]["fraction"] == "1/6"
    assert packet["navier_stokes"]["vortex_barrier_delta_over_2"]["fraction"] == "1/24"

    assert packet["heat_kernel"]["lambda_2_equals_theta"]
    assert packet["heat_kernel"]["lambda_2"]["fraction"] == "10"
    assert packet["heat_kernel"]["residual_floor_amplitudes_integral"]
    assert packet["heat_kernel"]["residual_amplitudes"]["C4_times_floor"]["fraction"] == "30"
    assert packet["heat_kernel"]["residual_amplitudes"]["C2_times_floor"]["fraction"] == "20"
    assert packet["heat_kernel"]["residual_amplitudes"]["C0_times_floor"]["fraction"] == "880"

    spine_packet = packet["cross_branch_spine"]
    assert spine_packet["lambda2_decay_equals_kolmogorov"]
    assert spine_packet["integer_gap"]["fraction"] == "5"
    assert spine_packet["integer_gap_over_q"]["fraction"] == "5/3"
    assert spine_packet["lambda_2_times_ns_decay_rate"]["fraction"] == "5/3"
    assert spine_packet["ym_floor_to_decay_rate_ratio"]["fraction"] == "2"

    assert packet["einstein_hilbert_ratios"]["a0_over_a2"]["fraction"] == "55/7"
    assert packet["einstein_hilbert_ratios"]["a4_over_a0"]["fraction"] == "3/110"
    assert packet["einstein_hilbert_ratios"]["c_EH_over_theta"]["fraction"] == "32"


def test_yang_mills_spectral_floor_uses_squared_mass_gap():
    ym = _load_module(
        ROOT / "analysis" / "w33_ym_mass_gap_spectral_floor.py",
        "w33_ym_mass_gap_spectral_floor",
    )

    assert ym.MASS_GAP_SQUARED == Fraction(1, 9)
    assert ym.substrate_laplacian_spectrum(0, 1, 2) == Fraction(1, 12)
    assert ym.substrate_laplacian_spectrum(0, 1, 3) == Fraction(1, 9)
    assert ym.substrate_laplacian_spectrum(1, 0, 2) == Fraction(1, 12)
    assert abs(ym.spectral_floor_theorem()["global_infimum"] - (1 / 12)) < 1e-15
    vacuum = ym.vacuum_uniqueness_proof()
    assert vacuum["first_excited_prime"] == 2
    assert abs(vacuum["spectral_gap"] - (1 / 12)) < 1e-15
    assert abs(ym.clay_ym_bridge_summary()["spectral_gap"] - (1 / 12)) < 1e-15
