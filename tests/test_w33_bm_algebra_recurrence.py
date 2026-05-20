"""Tests for MCLIV: Bose-Mesner algebra matrix recurrence."""
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_bm_algebra_recurrence import bm_algebra_packet  # noqa: E402

PACKET = bm_algebra_packet()


def test_fundamental_identity_A2():
    """A^2 = 8I - 2A + 4J (fundamental SRG Bose-Mesner identity)."""
    n2 = PACKET["bm_coordinates"]["n_2"]
    assert n2["a"] == "8"
    assert n2["b"] == "-2"
    assert n2["c"] == "4"


def test_bm_n3():
    """A^3 = -16I + 12A + 40J."""
    n3 = PACKET["bm_coordinates"]["n_3"]
    assert n3["a"] == "-16"
    assert n3["b"] == "12"
    assert n3["c"] == "40"


def test_bm_n4():
    """A^4 = 96I - 40A + 528J."""
    n4 = PACKET["bm_coordinates"]["n_4"]
    assert n4["a"] == "96"
    assert n4["b"] == "-40"
    assert n4["c"] == "528"


def test_trace_bm_equals_trace_spectral():
    ids = PACKET["master_identities_summary"]
    assert ids["trace_bm_equals_trace_spectral"]


def test_b_n_closed_form():
    """b_n = (2^n - (-4)^n) / 6 for all n."""
    ids = PACKET["master_identities_summary"]
    assert ids["b_n_closed_form"]


def test_b_n_values():
    """First 6 values of b_n from closed form."""
    r, s = 2, -4
    for n, bm_key in enumerate([f"n_{i}" for i in range(6)]):
        expected = Fraction(r**n - s**n, r - s)
        actual = Fraction(PACKET["bm_coordinates"][bm_key]["b"])
        assert actual == expected, f"n={n}: b_n={actual} != {expected}"


def test_a_n_from_b_n():
    ids = PACKET["master_identities_summary"]
    assert ids["a_n_from_b_n"]


def test_minimal_polynomial():
    """A^3 = 10*A^2 + 32*A - 96*I (minimal polynomial recurrence)."""
    ids = PACKET["master_identities_summary"]
    assert ids["minimal_polynomial_A3_eq_10A2_32A_minus_96I"]
    mp = PACKET["minimal_polynomial"]
    assert mp["verified"]


def test_B2_normalized_equals_k():
    ids = PACKET["master_identities_summary"]
    assert ids["B2_normalized_trace_equals_k"]
    # B_2 = trace(A^2)/v = 480/40 = 12 = k
    assert PACKET["normalized_traces"]["B_2"] == "12"


def test_B3_normalized_equals_lambda_k():
    ids = PACKET["master_identities_summary"]
    assert ids["B3_normalized_trace_equals_lambda_k"]
    # B_3 = trace(A^3)/v = 960/40 = 24 = lambda*k
    assert PACKET["normalized_traces"]["B_3"] == "24"


def test_all_master_identities():
    ids = PACKET["master_identities_summary"]
    failed = [name for name, result in ids.items() if not result]
    assert not failed, f"Failed: {failed}"
    assert sum(ids.values()) == len(ids)
