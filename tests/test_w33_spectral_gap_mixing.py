"""Tests for MCLII: Spectral Gap and Mixing Time Certificate."""
import sys
from pathlib import Path
from fractions import Fraction

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_spectral_gap_mixing import spectral_gap_mixing_packet  # noqa: E402

PACKET = spectral_gap_mixing_packet()


def test_spectral_gap_exact_value():
    sg = PACKET["spectral_gap"]
    assert sg["delta"]["fraction"] == "5/6"
    assert sg["delta"]["numerator"] == 5
    assert sg["delta"]["denominator"] == 6


def test_gap_three_forms_equal():
    sg = PACKET["spectral_gap"]
    assert sg["gap_all_forms_equal"]


def test_k_times_delta_equals_k_minus_r():
    """k * delta = k - r = q^2 + 1 = 10."""
    sg = PACKET["spectral_gap"]
    assert sg["k_times_delta"]["fraction"] == "10"
    assert sg["k_times_delta_equals_k_minus_r"]
    assert sg["k_times_delta_equals_q2_plus_1"]


def test_kemeny_decomposition():
    """K = m_r*(k/(k-r)) + m_s*(k/(k-s)) = 801/20."""
    km = PACKET["kemeny_decomposition"]
    assert km["kemeny_decomposed"]
    assert km["K_total"]["fraction"] == "801/20"
    assert km["K_expected"]["fraction"] == "801/20"


def test_K_r_term():
    """m_r * (k/(k-r)) = 24 * 6/5 = 144/5."""
    km = PACKET["kemeny_decomposition"]
    assert km["K_r_term"]["fraction"] == "144/5"


def test_K_s_term():
    """m_s * (k/(k-s)) = 15 * 3/4 = 45/4."""
    km = PACKET["kemeny_decomposition"]
    assert km["K_s_term"]["fraction"] == "45/4"


def test_K_term_ratio_64_25():
    """(m_r*(k-s)) / (m_s*(k-r)) = 64/25 = (8/5)^2."""
    km = PACKET["kemeny_decomposition"]
    assert km["ratio_equals_64_over_25"]
    assert km["K_r_term_over_K_s_term"]["fraction"] == "64/25"


def test_ramanujan_property():
    """W(3,3) is a Ramanujan graph."""
    ram = PACKET["ramanujan"]
    assert ram["is_ramanujan_r"]
    assert ram["is_ramanujan_s"]
    assert ram["both_satisfy_ramanujan"]


def test_expander_constant():
    """Expander constant = |s|/k = 1/3."""
    exp = PACKET["expander"]
    assert exp["constant_is_1_over_3"]
    assert exp["spectral_expansion_constant"]["fraction"] == "1/3"


def test_norm_P_sq_v_over_k():
    """||P||^2 = v/k where P = A/k."""
    np_ = PACKET["norm_P"]
    assert np_["norm_P_sq_equals_v_over_k"]
    assert np_["norm_P_sq"]["fraction"] == "10/3"  # v/k = 40/12 = 10/3


def test_all_master_identities():
    ids = PACKET["master_identities_summary"]
    failed = [name for name, result in ids.items() if not result]
    assert not failed, f"Failed identities: {failed}"
    assert sum(ids.values()) == len(ids)
