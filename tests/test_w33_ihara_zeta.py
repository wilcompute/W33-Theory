"""Tests for MCLIII: Ihara Zeta Function and Graph Riemann Hypothesis."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_ihara_zeta import ihara_zeta_packet, spectral_trace_L  # noqa: E402

PACKET = ihara_zeta_packet()


def test_ihara_rh_holds():
    rh = PACKET["riemann_hypothesis"]
    assert rh["ihara_rh_holds"]
    assert rh["r_factor_zeros_on_rh_circle"]
    assert rh["s_factor_zeros_on_rh_circle"]


def test_discriminants_negative():
    """Both r and s factor discriminants are negative (complex zeros on RH circle)."""
    rh = PACKET["riemann_hypothesis"]
    assert rh["disc_r"] < 0, f"disc_r = {rh['disc_r']}"
    assert rh["disc_s"] < 0, f"disc_s = {rh['disc_s']}"


def test_discriminant_values():
    """r^2 - 4(k-1) = 4 - 44 = -40; s^2 - 4(k-1) = 16 - 44 = -28."""
    rh = PACKET["riemann_hypothesis"]
    assert rh["disc_r"] == -40
    assert rh["disc_s"] == -28


def test_trace_A0():
    """trace(A^0) = tr(I) = v = 40."""
    assert PACKET["spectral_traces"]["trace_A_0"] == 40
    assert PACKET["trace_identities"]["L0_equals_v"]


def test_trace_A1():
    """trace(A^1) = 0 (no self-loops)."""
    assert PACKET["spectral_traces"]["trace_A_1"] == 0
    assert PACKET["trace_identities"]["L1_equals_0"]


def test_trace_A2():
    """trace(A^2) = kv = 480."""
    assert PACKET["spectral_traces"]["trace_A_2"] == 480
    assert PACKET["trace_identities"]["L2_equals_kv"]


def test_trace_A3_triangle_count():
    """trace(A^3) = 6 * number_of_triangles = 6 * 160 = 960."""
    assert PACKET["spectral_traces"]["trace_A_3"] == 960
    assert PACKET["trace_identities"]["L3_equals_lambda_v_k"]
    assert PACKET["trace_identities"]["triangle_count"] == 160
    assert PACKET["trace_identities"]["triangles_times_6"] == 960


def test_hashimoto_eigenvalue_count():
    """Hashimoto matrix has 2|E| = 480 eigenvalues total."""
    ha = PACKET["hashimoto"]
    assert ha["count_correct"]
    assert ha["total_eigenvalues"] == 480
    assert ha["two_times_edges"] == 480


def test_hashimoto_breakdown():
    """Principal 2, r-type 48, s-type 30, trivial 400 sums to 480."""
    bd = PACKET["hashimoto"]["breakdown"]
    assert bd["principal_non_trivial"] == 2
    assert bd["r_non_trivial"] == 48
    assert bd["s_non_trivial"] == 30
    assert bd["trivial"] == 400
    assert sum(bd.values()) == 480


def test_spectral_trace_direct():
    """Direct computation: trace(A^L) = k^L + m_r*r^L + m_s*s^L."""
    k, r, s, m_r, m_s = 12, 2, -4, 24, 15
    assert spectral_trace_L(k, r, s, m_r, m_s, 0) == 40
    assert spectral_trace_L(k, r, s, m_r, m_s, 1) == 0
    assert spectral_trace_L(k, r, s, m_r, m_s, 2) == 480
    assert spectral_trace_L(k, r, s, m_r, m_s, 3) == 960


def test_all_master_identities():
    ids = PACKET["master_identities_summary"]
    failed = [name for name, result in ids.items() if not result]
    assert not failed, f"Failed identities: {failed}"
    assert sum(ids.values()) == len(ids)
