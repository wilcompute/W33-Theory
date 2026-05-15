"""Part DCCXXIII -- Genus-equation spectrum tests."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxxiii_genus_equation_spectrum import (  # noqa: E402
    CODEC,
    HEAWOOD,
    OUT_PATH,
    Q,
    QP1,
    W33_E6_FUND,
    W33_H1,
    W33_K,
    W33_V,
    build_bridge,
    genus_of_complete_graph,
    genus_oscillator,
    integer_spectrum,
    is_integer_genus,
    oscillator_increments_mod12,
    three_clock_dictionary,
    w33_primitive_audit,
    write_bridge,
)


def test_tetrahedron_is_K4_genus_0():
    assert int(genus_of_complete_graph(4)) == 0
    assert is_integer_genus(4)


def test_csaszar_is_K7_genus_1():
    assert int(genus_of_complete_graph(7)) == 1
    assert is_integer_genus(7)


def test_K12_genus_6_at_codec():
    assert int(genus_of_complete_graph(12)) == 6
    assert is_integer_genus(12)


def test_K27_genus_46_at_q_to_q():
    assert int(genus_of_complete_graph(27)) == 46
    assert is_integer_genus(27)


def test_K40_genus_111_at_v():
    assert int(genus_of_complete_graph(40)) == 111
    assert is_integer_genus(40)


def test_H1_81_off_spectrum():
    assert not is_integer_genus(81)


def test_q_factorial_6_off_spectrum():
    # q! = 6: (6-3)(6-4) = 6, 6/12 = 0.5 not integer
    assert not is_integer_genus(6)


def test_genus_equation_coefficients_match_dccxxii():
    # x^2 - 7x + 12 = 12g, with 7 = HEAWOOD, 12 = CODEC
    assert HEAWOOD == 7
    assert CODEC == 12


def test_quadratic_evaluates_correctly():
    # For n=7: n^2 - 7n + 12 = 49 - 49 + 12 = 12. So g = 12/12 = 1.
    n = 7
    rhs = n * n - HEAWOOD * n + CODEC
    assert rhs == 12 * 1


def test_genus_oscillator_h_0_is_tetrahedron():
    osc = genus_oscillator(0)
    assert osc["v"] == 4
    assert osc["E"] == 6
    assert osc["F"] == 4
    assert osc["chi"] == 2


def test_genus_oscillator_h_1_is_csaszar_szilassi():
    osc = genus_oscillator(1)
    assert osc["v"] == 7
    assert osc["E"] == 21
    assert osc["F"] == 14
    assert osc["chi"] == 0


def test_oscillator_increments_mod_12():
    inc = oscillator_increments_mod12()
    assert inc["delta_v_mod_12"] == 3 == Q
    assert inc["delta_E_mod_12"] == 3
    assert inc["delta_F_mod_12"] == 10
    assert inc["delta_chi"] == -2


def test_three_clocks_are_12_7_10():
    clocks = three_clock_dictionary()
    assert clocks["mod_12_clock"]["modulus"] == 12
    assert clocks["mod_7_clock"]["modulus"] == 7
    assert clocks["mod_10_clock"]["modulus"] == 10


def test_spectrum_residues_in_0_3_8_11_mod_12():
    spec = integer_spectrum(50)
    for r in spec:
        assert r["m_mod_12"] in {0, 3, 8, 11}


def test_spectrum_contains_4_7_12():
    spec = integer_spectrum(50)
    ns = [r["n"] for r in spec]
    for required in (4, 7, 12, 15, 16, 19, 24, 27, 40):
        assert required in ns


def test_w33_primitive_audit_separates_on_and_off():
    audit = w33_primitive_audit()
    on = [r["name"] for r in audit if r["in_spectrum"]]
    off = [r["name"] for r in audit if not r["in_spectrum"]]
    # Heawood, codec, q^q, v all on
    assert "q + (q+1) = sum = Heawood" in on
    assert "q (q+1) = product = codec" in on
    assert "q^q" in on
    assert "v" in on
    # q! and H_1 off
    assert "q! = 2q" in off
    assert "q^(q+1) = H_1" in off


def test_summary_all_identities_hold():
    b = build_bridge()
    assert b["summary"]["all_identities_hold"] is True


def test_identities_all_pass():
    b = build_bridge()
    failed = [k for k, v in b["identities"].items() if not v]
    assert failed == []


def test_write_and_reload():
    out = write_bridge()
    assert out.exists()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["summary"]["all_identities_hold"] is True


def test_theorem_and_one_line_present():
    b = build_bridge()
    assert "Genus-Equation Spectrum Theorem" in b["theorem"]
    assert "(n-3)(n-4)/12" in b["one_line"]


def test_json_has_expected_keys():
    if not OUT_PATH.exists():
        write_bridge()
    data = json.loads(OUT_PATH.read_text(encoding="utf-8"))
    for key in (
        "summary",
        "genus_equation",
        "integer_spectrum_n_le_50",
        "w33_primitive_audit",
        "genus_oscillator",
        "increments_mod_12",
        "three_clocks",
        "identities",
        "theorem",
        "one_line",
        "honesty_boundary",
    ):
        assert key in data
