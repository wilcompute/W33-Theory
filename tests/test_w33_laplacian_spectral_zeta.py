"""Tests for MCLV: Laplacian spectral zeta function."""
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_laplacian_spectral_zeta import laplacian_spectral_zeta_packet, laplacian_zeta_s  # noqa: E402

PACKET = laplacian_spectral_zeta_packet()


def test_zeta_0_equals_v_minus_1():
    """ζ_L(0) = m_r + m_s = v - 1 = 39."""
    assert PACKET["zeta_values"]["0"] == "39"
    assert PACKET["master_identities_summary"]["zeta_L_0_equals_v_minus_1"]


def test_zeta_1_kirchhoff():
    """ζ_L(1) = 24/10 + 15/16 = 267/80."""
    assert PACKET["zeta_values"]["1"] == "267/80"


def test_v_times_zeta_1_equals_K_f():
    """v * ζ_L(1) = 40 * 267/80 = 267/2 = K_f (bridge to MCLI)."""
    kb = PACKET["kirchhoff_bridge"]
    assert kb["match"]
    assert kb["K_f_from_v_times_zeta_1"] == "267/2"
    assert PACKET["master_identities_summary"]["v_times_zeta_L_1_equals_K_f"]


def test_zeta_minus1_equals_twice_E():
    """ζ_L(-1) = 24*10 + 15*16 = 480 = 2|E| = kv."""
    assert PACKET["zeta_values"]["-1"] == "480"
    assert PACKET["master_identities_summary"]["zeta_L_minus1_equals_2_times_E"]


def test_equal_energy_split():
    """m_r*(k-r) = m_s*(k-s) = |E| = 240 (unique balanced energy property)."""
    ee = PACKET["equal_energy_split"]
    assert ee["check"]
    assert ee["energy_r"] == 240
    assert ee["energy_s"] == 240
    assert ee["edges"] == 240


def test_energy_ratio_equals_eigenvalue_ratio():
    """m_r/m_s = (k-s)/(k-r) = 8/5 (guarantees equal energy split)."""
    assert PACKET["master_identities_summary"]["energy_ratio_equals_eigenvalue_ratio"]


def test_spanning_tree_from_det():
    """det(non-zero Laplacian eigenvalues) = v * τ = 10^24 * 16^15 = 2^84 * 5^24."""
    sb = PACKET["spanning_tree_bridge"]
    assert sb["check"]
    assert sb["tau"] == "2^81 * 5^23"
    assert PACKET["master_identities_summary"]["det_nonzero_eigenvalues_eq_v_times_tau"]
    assert PACKET["master_identities_summary"]["tau_from_det_matches_kirchhoff_tau"]


def test_zeta_2_exact():
    """ζ_L(2) = 24/100 + 15/256 = 1911/6400."""
    assert PACKET["zeta_values"]["2"] == "1911/6400"
    assert PACKET["master_identities_summary"]["zeta_L_2_exact"]


def test_zeta_minus2():
    """ζ_L(-2) = 24*100 + 15*256 = 6240."""
    assert PACKET["zeta_values"]["-2"] == "6240"
    assert PACKET["master_identities_summary"]["zeta_L_minus2_equals_6240"]


def test_zeta_function_direct():
    """Direct evaluation of laplacian_zeta_s at various s."""
    m_r, m_s, kminusr, kminuss = 24, 15, 10, 16
    assert laplacian_zeta_s(0, m_r, m_s, kminusr, kminuss) == Fraction(39)
    assert laplacian_zeta_s(1, m_r, m_s, kminusr, kminuss) == Fraction(267, 80)
    assert laplacian_zeta_s(-1, m_r, m_s, kminusr, kminuss) == Fraction(480)
    assert laplacian_zeta_s(-2, m_r, m_s, kminusr, kminuss) == Fraction(6240)


def test_all_master_identities():
    ids = PACKET["master_identities_summary"]
    failed = [name for name, result in ids.items() if not result]
    assert not failed, f"Failed: {failed}"
    assert sum(ids.values()) == len(ids)
