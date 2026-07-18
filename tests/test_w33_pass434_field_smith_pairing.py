from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from collections import Counter

PATH = Path(__file__).resolve().parents[1] / "analysis" / "w33_pass434_field_smith_pairing.py"
SPEC = spec_from_file_location("pass434", PATH)
MOD = module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MOD)


def test_q7_gate_shape():
    result = MOD.certify(7, "prime")
    assert result["status"] == "PASS"
    assert result["two_primary_shape"] == {"2^1": 42, "2^4": 126}
    assert result["tree_v2"] == 546


def test_gf9_field_ring_boundary():
    field = MOD.certify(9, "gf9")
    ring = MOD.certify(9, "zmod")
    assert field["status"] == "PASS"
    assert field["two_primary_shape"] == {"2^3": 72, "2^4": 288}
    assert ring["two_primary_shape"] == {"2^1": 6, "2^3": 60, "2^4": 216}
    assert ring["adjacency_spectrum_multiplicities"] == {
        "80": 1,
        "26": 12,
        "8": 270,
        "-1": 224,
        "-10": 216,
        "-28": 6,
    }
    assert ring["checks"]["smith_tree_v2_matches_actual_spectrum"]
    assert ring["two_primary_shape"] != field["two_primary_shape"]


def test_spectral_pairing_multiplicities():
    for q in (3, 5, 7, 9, 11):
        m_plus = q * (q * q - 1) // 2
        m_minus = q * (q - 1) ** 2 // 2
        assert m_plus - m_minus == q * (q - 1)
        assert MOD.expected_shape(q) == Counter({
            MOD.v2(q - 1): q * (q - 1),
            MOD.v2(q * q - 1): m_minus,
        })
