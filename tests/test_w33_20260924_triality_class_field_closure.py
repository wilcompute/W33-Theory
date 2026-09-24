import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/w33_20260924_triality_class_field_closure.json"


def load():
    return json.loads(DATA.read_text(encoding="utf-8"))


def test_arithmetic_core():
    d = load()
    assert d["status"] == "PASS_TRIALITY_CLASS_FIELD_CLOSURE"
    c = d["cubic"]
    assert c["discriminant"] == 94557
    assert c["squarefree"] is True
    assert c["ramified_primes"] == [3, 43, 733]
    assert c["signature"] == [3, 0]


def test_quadratic_resolvent_class_group():
    q = load()["quadratic_resolvent"]
    assert q["polynomial"] == "x**2 - x - 23639"
    assert q["pell_period"] == [1, 1, 204, 1, 1, 614]
    assert q["fundamental_unit"] == "252151 + 820*sqrt(94557)"
    assert q["fundamental_unit_norm"] == 1
    assert abs(q["class_number_formula_float"] - 6.0) < 1e-10
    assert q["class_number"] == 6
    assert q["class_group"] == "C6"
    assert q["three_primary_class_group"] == "C3"


def test_hilbert_three_class_field_closure():
    n = load()["normal_closure"]
    assert n["degree_over_Q"] == 6
    assert n["galois_group_over_Q"] == "S3"
    assert n["degree_over_resolvent"] == 3
    assert n["galois_group_over_resolvent"] == "C3"
    assert n["field_discriminant"] == 94557**3
    assert n["relative_discriminant_norm"] == 1
    assert n["everywhere_unramified_over_resolvent"] is True
    assert n["unique_unramified_cyclic_cubic_extension"] is True
    assert n["identification"].startswith("Hilbert 3-class field")


def test_triality_semidirect_mechanism():
    t = load()["triality"]
    assert t["exact_sequence"] == "1 -> C3 -> S3 -> C2 -> 1"
    assert t["C2_action_on_C3"] == "inversion"
    assert t["semidirect_product"] == "C3 : C2 = S3"


def test_frobenius_decoder():
    data = json.loads((ROOT / "data/w33_20260924_frobenius_triality_decoder.json").read_text(encoding="utf-8"))
    assert data["status"] == "PASS_FROBENIUS_TRIALITY_DECODER"
    c = data["prime_census_below_10000"]
    assert c["unramified_prime_count"] == 1226
    assert c["counts"] == {"transposition": 629, "3-cycle": 394, "identity": 203}
    assert c["parity_mismatch_count"] == 0
    dec = data["decoder"]
    assert "1+2" in dec["rule_minus_1"]
    assert "1+1+1" in dec["rule_plus_1_artin_0"]
    assert dec["orientation_boundary"].startswith("factorization sees")
