import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCER = ROOT / "analysis/w33_pass10954_regular_c8_clock_completion.py"
CERT = ROOT / "data/w33_pass10954_regular_c8_clock_completion.json"


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
    assert load()["status"] == "PASS_REGULAR_C8_CLOCK_COMPLETION"
def test_regular_c8_completion_is_exact():
    x = load()
    assert x["compressed_clock"]["C8_character_exponents"] == [0,1,3,4,5,7]
    assert x["compressed_clock"]["missing_character_exponents"] == [2,6]
    assert x["unique_minimal_completion"]["all_C8_characters_once"] is True
    assert x["unique_minimal_completion"]["minimal_polynomial"] == "x^8-1"
    assert x["regular_clock"]["trace_sequence"] == (
        [[8.0,0.0]] + [[0.0,0.0]] * 7
    )
    assert x["regular_clock"]["normalized_trace_visibility"] == [1.0] + [0.0] * 7
    assert x["regular_clock"]["uniform_spectral_clock_gram_identity_error"] < 1e-8


def test_orientation_double_cover_is_two_regular_orbits():
    o = load()["oriented_A2_4_clock_cover"]
    assert o["oriented_sign_states"] == 16
    assert o["clock_cycle_lengths"] == [8,8]
    assert o["four_ticks"] == "global complement x -> x+1111"
    assert o["eight_ticks"] == "identity"
    assert o["leaf_quotient_states"] == 8
    assert o["leaf_cycle_lengths"] == [4,4]
    assert o["regular_C8_orbit_count"] == 2
def test_pin_clock_embeds_and_missing_modes_are_deck_even():
    o = load()["oriented_A2_4_clock_cover"]
    assert o["full_8D_intertwiner_error"] < 1e-8
    assert o["compressed_6D_intertwiner_error"] < 1e-8
    assert o["missing_projector_error"] < 1e-8
    assert o["pin_subspace_deck_even_rank"] == 2
    assert o["pin_subspace_deck_odd_rank"] == 4
    assert o["missing_modes_deck_even"] is True
    assert "not orientation-odd" in load()["interpretation"]["deck_mode_correction"]


def test_determinant_is_orientation_parity_character_all48():
    d = load()["shared_determinant_character"]
    assert d["GL2_3_elements"] == 48
    assert d["det_plus_orientation_preserving"] == 24
    assert d["det_minus_orientation_flipping"] == 24
    assert d["all48_exact"] is True
    assert "CP/non-CP" in d["channel_weld"]
def test_temporal_weil_match_remains_firewalled():
    w = load()["temporal_weil_phase_comparison"]
    assert w["rank_one_phase_values"] == {
        "mu12_exponent_3": "i",
        "mu12_exponent_9": "-i",
    }
    assert "no objectwise map" in w["firewall"]


def test_visible_surfaces_are_unique():
    docs = (ROOT / "docs/index.html").read_text(encoding="utf-8")
    tail = (ROOT / "analysis/W33_SHARED_FRONTIER_TAIL.tex").read_text(
        encoding="utf-8"
    )
    assert docs.count('id="pass10954-regular-c8-orientation-clock"') == 1
    assert tail.count(
        "PASS10954_REGULAR_C8_CLOCK_COMPLETION_INSERT}%"
    ) == 1
