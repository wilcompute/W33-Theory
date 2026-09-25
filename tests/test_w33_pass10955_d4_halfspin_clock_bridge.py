import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCER = ROOT / "analysis/w33_pass10955_d4_halfspin_clock_bridge.py"
CERT = ROOT / "data/w33_pass10955_d4_halfspin_clock_bridge.json"


def load():
    return json.loads(CERT.read_text(encoding="utf-8"))


def test_producer_replays():
    subprocess.run(
        [sys.executable, str(PRODUCER)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert load()["status"] == "PASS_D4_HALFSPIN_CLOCK_DETERMINANT_BRIDGE"
def test_faithful_signed_d4_embedding():
    e = load()["signed_permutation_embedding"]
    assert e["group"] == "GL(2,3)"
    assert e["order"] == 48
    assert e["dimension"] == 4
    assert e["faithful"] is True
    assert e["all_48_squared_products_checked"] is True
    assert e["D4_root_count"] == 24
    assert e["all_elements_preserve_D4_roots"] is True
    assert e["det_plus_subgroup"] == "SL(2,3) lies in W(D4)"


def test_three_eight_weight_sets_and_outer_transposition():
    w = load()["D4_minuscule_weight_sets"]
    assert w["vector_weights"] == 8
    assert w["half_spin_plus_weights"] == 8
    assert w["half_spin_minus_weights"] == 8
    o = load()["outer_D4_action"]
    assert o["det_plus_count"] == 24
    assert o["det_minus_count"] == 24
    assert o["outer_image"] == "C2 inside Out(D4)=S3"
    assert "not a triality 3-cycle" in o["triality_boundary"]
def test_order_eight_clock_alternates_halfspin_sheets():
    c = load()["clock"]
    assert c["order"] == 8
    assert c["one_tick"] == "S+ <-> S-"
    assert c["two_ticks"] == "preserves S+ and S- separately"
    assert c["four_ticks"].startswith("-I4")
    assert c["eight_ticks"] == "identity"
    assert c["halfspin_union_cycle_lengths"] == [8, 8]


def test_shared_character_weld_is_explicit():
    s = load()["shared_character"]
    assert "det=+1 preserves" in s["determinant"]
    assert "CPTP" in s["pass10952_CP"]
    assert "Fano-hinge" in s["pass10954_Fano"]
    assert "same GL(2,3) character" in s["new_weld"]


def test_prior_d4_result_is_cited_not_rediscovered():
    r = load()["repo_crosscheck"]
    assert "independent" in r["pass540"]
    assert "same 16 sign states" in r["pass10954"]
def test_visible_surfaces_are_unique():
    docs = (ROOT / "docs/index.html").read_text(encoding="utf-8")
    tail = (ROOT / "analysis/W33_SHARED_FRONTIER_TAIL.tex").read_text(
        encoding="utf-8"
    )
    assert docs.count('id="pass10955-d4-halfspin-clock"') == 1
    assert tail.count("PASS10955_D4_HALFSPIN_CLOCK_BRIDGE_INSERT}%") == 1
