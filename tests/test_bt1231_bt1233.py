#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(rel):
    subprocess.run([sys.executable, str(ROOT / rel)], cwd=ROOT, check=True)


def load(rel):
    with (ROOT / rel).open(encoding="utf-8") as f:
        return json.load(f)


def test_bt1231_min_count():
    run("analysis/bt1231_sp43_minimal_transvection_count.py")
    d = load("data/bt1231_sp43_minimal_transvection_count_summary.json")
    assert d["target_order"] == 51840
    assert d["single_order_histogram"] == {"3": 40}
    assert d["pair_order_histogram"] == {"9": 240, "24": 540}
    assert d["triple_order_histogram"] == {"24": 360, "27": 160, "72": 2160, "648": 7200}
    assert d["total_triples_checked"] == 9880
    assert d["max_order_at_most_three"] == 648
    assert d["bt1228_four_set_order"] == 51840
    assert d["minimal_transvection_count"] == 4


def test_bt1232_r3_validator():
    run("analysis/bt1232_r3_evidence_gate.py")
    d = load("data/bt1232_r3_evidence_gate_summary.json")
    assert d["lanes"] == ["schema_stub", "blocked", "partial", "near_candidate", "candidate"]
    assert d["demo_counts"] == {"schema_stub": 1, "blocked": 1, "partial": 1, "near_candidate": 1, "candidate": 1}
    assert d["near_candidate_promoted"] is False
    assert d["certified_candidate_promoted"] is True
    assert d["fail_closed"] is True


def test_bt1233_word_metric():
    run("analysis/bt1233_sp43_word_metric_tomography_protocol.py")
    d = load("data/bt1233_sp43_word_metric_tomography_summary.json")
    assert d["symmetric_gate_count"] == 8
    assert d["generated_order"] == 51840
    assert d["closure_ok"] is True
    assert d["diameter"] == 14
    assert d["sphere_histogram"] == {"0":1,"1":8,"2":36,"3":126,"4":363,"5":916,"6":2052,"7":4096,"8":7396,"9":12170,"10":16916,"11":7247,"12":476,"13":36,"14":1}
    assert d["checkpoints"] == {"B4": 534, "B8": 14994, "B12": 51803, "B14": 51840}


def test_bt1240_synthetic_recovery_harness():
    run("analysis/bt1240_synthetic_word_metric_recovery_harness.py")
    d = load("data/bt1240_synthetic_word_metric_recovery_harness_summary.json")
    assert d["cases"]["exact"]["band"] == "pass"
    assert d["cases"]["exact"]["order"] == 51840
    assert d["cases"]["exact"]["diameter"] == 14
    assert d["cases"]["drop_last"]["band"] == "fail"
    assert d["cases"]["drop_last"]["order"] == 648
    assert d["cases"]["swap_last"]["band"] == "fail"
    assert d["cases"]["swap_last"]["order"] == 51840
    assert d["cases"]["swap_last"]["diameter"] == 10
    assert d["cases"]["identity_last"]["band"] == "fail"
    assert d["cases"]["identity_last"]["local_order3_ok"] is False


def test_bt1242_four_transvection_regimes():
    run("analysis/bt1242_four_transvection_regime_classifier.py")
    d = load("data/bt1242_four_transvection_regime_classifier_summary.json")
    assert d["all_four_sets"] == 91390
    assert d["stabilizer_orbit_representatives"] == 32
    assert d["unique_word_metric_profiles"] == 16
    assert d["global_counts_by_order"] == {"24": 90, "27": 40, "72": 1440, "576": 1620, "648": 26640, "51840": 61560}
    assert d["global_counts_by_order_and_diameter"] == {"24:diam3": 90, "27:diam2": 40, "72:diam4": 1440, "576:diam8": 1620, "648:diam6": 11520, "648:diam7": 15120, "51840:diam10": 22680, "51840:diam12": 25920, "51840:diam14": 12960}
    assert d["bt1228_profile_global_count"] == 12960
    assert d["full_order_structural_summary"] == {"diam10": {"count": 22680, "patterns": 3}, "diam12": {"count": 25920, "patterns": 1}, "diam14": {"count": 12960, "patterns": 1}}


def test_bt1248_stabilizer_regimes():
    run("analysis/bt1248_four_transvection_stabilizer_regimes.py")
    d = load("data/bt1248_four_transvection_stabilizer_regimes_summary.json")
    assert d["acting_group_order"] == 51840
    assert d["by_diameter"] == {
        "10": {"total_sets": 22680, "orbit_count": 3, "stabilizer_orders": [4, 8, 16]},
        "12": {"total_sets": 25920, "orbit_count": 1, "stabilizer_orders": [2]},
        "14": {"total_sets": 12960, "orbit_count": 1, "stabilizer_orders": [4]},
    }


def test_bt1249_paper_sections_and_integrator():
    sec1236 = ROOT / "paper" / "sections" / "sec_bt1236_minimal_clifford_word_metric.tex"
    sec1249 = ROOT / "paper" / "sections" / "sec_bt1249_four_transvection_regime_theorem.tex"
    integrator = ROOT / "tools" / "integrate_bt1236_insert.py"
    assert sec1236.exists()
    assert sec1249.exists()
    text = sec1249.read_text(encoding="utf-8")
    assert "61560" in text
    assert "51840_{\\operatorname{diam}=14}^{12960}" in text
    itext = integrator.read_text(encoding="utf-8")
    assert "sec_bt1236_minimal_clifford_word_metric" in itext
    assert "sec_bt1249_four_transvection_regime_theorem" in itext


if __name__ == "__main__":
    test_bt1231_min_count()
    test_bt1232_r3_validator()
    test_bt1233_word_metric()
    test_bt1240_synthetic_recovery_harness()
    test_bt1242_four_transvection_regimes()
    test_bt1248_stabilizer_regimes()
    test_bt1249_paper_sections_and_integrator()
    print("BT1231-BT1249 regression tests pass")
