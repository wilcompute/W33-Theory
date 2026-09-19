from __future__ import annotations
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "analysis" / "w33_punctured_hesse_packet_group.py"
FROZEN = ROOT / "data" / "w33_punctured_hesse_packet_group.json"

spec = importlib.util.spec_from_file_location("punctured_hesse_packet_group", MOD)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def test_two_punctured_plane_controls():
    for q in (3, 5, 7, 11):
        r = mod.punctured_plane(q)
        assert r["size"] == q * q + q - 1
        assert len(r["affine"]) == q * q
        assert len(r["infinity"]) == q - 1
        assert r["line_size_histogram"] == {
            str(q - 1): 1,
            str(q): 2 * q,
            str(q + 1): q * (q - 1),
        }


def test_q3_packet_group_is_72_with_9_plus_2_orbits():
    g = mod.packet_group_72()
    assert g["order"] == 72
    assert g["structure"] == "F_3^2 semidirect D_8"
    assert g["distinct_projective_permutations"] == 72
    assert g["orbit_sizes"] == [2, 9]
    assert [row["packet_slot"] for row in g["slot_rows"]] == list(range(72))


def test_frequency_compiler_is_affine_chart_plus_two_infinity_points():
    f = mod.check_frequency_compiler()
    assert f["total_bins"] == 11
    assert len(f["hesse_bins"]) == 9
    assert len(f["sidebands"]) == 2
    for h, row in enumerate(f["hesse_bins"]):
        assert row["bin_index"] == h
        assert row["affine_coordinate"] == [h // 3, h % 3, 1]
    assert {tuple(x["projective_coordinate"]) for x in f["sidebands"]} == {
        (1, 1, 0),
        (1, 2, 0),
    }
    assert f["packet_frame_slots"] == 72


def test_full_build_and_frozen_summary_agree():
    out = mod.build()
    frozen = json.loads(FROZEN.read_text())
    assert out["status"] == frozen["status"] == "PASS_TWO_PUNCTURE_PACKET_GROUP"
    assert out["checks"] == frozen["checks"]
    assert out["q3_geometry"]["line_size_histogram"] == {"2": 1, "3": 6, "4": 6}
    assert out["q3_group"]["order"] == frozen["q3_group"]["order"] == 72
    assert out["q3_group"]["orbit_sizes"] == frozen["q3_group"]["orbit_sizes"] == [2, 9]
    assert out["frequency_compiler_bridge"]["packet_frame_slots"] == 72
    assert out["cz_hashimoto_parent"]["branch_counts"] == {
        "affine": 9,
        "infinity": 2,
        "total": 11,
    }
