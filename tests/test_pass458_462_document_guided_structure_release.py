from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(n: int) -> dict:
    suffix = {
        458: "collision_coherent_configuration",
        459: "prime_power_cyclotomic_covariance",
        460: "switching_trade_search",
        461: "integral_representation_lattices",
        462: "formal_cover_l1_audit",
    }[n]
    path = ROOT / "data" / f"w33_pass{n}_{suffix}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_pass458_coherent_separator() -> None:
    p = load(458)
    assert p["status"] == "PASS"
    assert [x["rank_history"][1] for x in p["two_wl_coherent_closures"]] == [19, 18]
    assert [x["trace_AA1A1"] for x in p["terwilliger_word_algebras"]] == [622, 650]


def test_pass459_prime_power_covariance() -> None:
    p = load(459)
    assert p["status"] == "PASS"
    assert p["q9_witness"]["number_of_character_lines"] == 4
    assert p["q25_witness"]["number_of_character_lines"] == 6
    assert p["q25_kernel_profile"] == {"5": 6}


def test_pass460_switching_negative() -> None:
    p = load(460)
    assert p["status"] == "PASS"
    assert len(p["phase_subtrade_hits"]) == 2
    assert sorted(x["weight"] for x in p["phase_subtrade_hits"]) == [0, 10]
    assert p["candidate_vertex_sets"] == 420
    assert p["godsil_mckay"]["isomorphic_to_target"] == []
    assert p["seidel"]["isomorphic_to_target"] == []
    assert p["golden_quartic_audit"]["nontrivial_gcd_hits"] == []


def test_pass461_integral_lattice_separator() -> None:
    p = load(461)
    assert p["status"] == "PASS"
    assert p["lattices"]["H3"]["discriminant_module"] == {"3": 3}
    assert p["lattices"]["R9"]["discriminant_module"] == {"3": 9, "9": 9}
    assert [p["lattices"][k]["central_gap_valuation"] for k in ("H3", "R9")] == [1, 3]


def test_pass462_formal_source_audit() -> None:
    p = load(462)
    assert p["status"] == "PASS"
    assert all(p["checks"].values())
    src = (ROOT / "formal" / "W33" / "Pass462CoverLawL1Q3.lean").read_text(encoding="utf-8")
    assert "theorem q3_cover_law_L1" in src
    assert "native_decide" in src
    assert "sorry" not in src.lower()
