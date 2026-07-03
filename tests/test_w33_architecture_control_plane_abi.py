import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_abi() -> dict:
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "analysis" / "w33_architecture_control_plane_abi.py"),
        ],
        cwd=ROOT,
        check=True,
    )
    return json.loads(
        (ROOT / "data" / "w33_architecture_control_plane_abi.json").read_text(
            encoding="utf-8"
        )
    )


def test_control_plane_word_closes_the_supercycle():
    data = run_abi()
    arch = data["derived_architecture"]
    radix = data["control_word"]["radix"]

    assert data["verified"] is True
    assert all(data["checks"].values())
    assert data["control_word"]["identity"] == "51840 = 24 * 5 * 6 * 9 * 2 * 4"
    assert (
        radix["mirror_atlases"]
        * radix["selector_sheets_per_atlas"]
        * radix["packet_frames_per_selector_sheet"]
        * radix["hesse_bins"]
        * radix["hashimoto_sectors"]
        * radix["probe_slots"]
        == 51840
    )
    assert arch["supercycle_slots"] == 51840
    assert arch["supercycle_probes"] == 12960
    assert arch["packet_frames_per_supercycle"] == 720


def test_control_plane_splits_selector_and_signed_sheets():
    data = run_abi()
    arch = data["derived_architecture"]

    assert arch["selector_sheet_count"] == 120
    assert arch["signed_sheet_count"] == 240
    assert arch["selector_sheet_slots"] == 432
    assert arch["signed_sheet_slots"] == 216
    assert arch["probes_per_selector_sheet"] == 108
    assert arch["probes_per_signed_sheet"] == 54
    assert arch["packet_frames_per_mirror_atlas"] == 30


def test_control_plane_decoder_hits_boundary_slots():
    data = run_abi()
    samples = {row["runtime_slot"]: row for row in data["runtime_decode_samples"]}

    assert samples[0]["mirror_atlas_id"] == 0
    assert samples[0]["selector_sheet_id"] == 0
    assert samples[0]["sign_label"] == "positive"
    assert samples[215]["signed_sheet_id"] == 0
    assert samples[216]["signed_sheet_id"] == 1
    assert samples[431]["selector_sheet_id"] == 0
    assert samples[432]["selector_sheet_id"] == 1
    assert samples[2159]["mirror_atlas_id"] == 0
    assert samples[2160]["mirror_atlas_id"] == 1
    assert samples[51839]["mirror_atlas_id"] == 23
    assert samples[51839]["selector_sheet_id"] == 119
    assert samples[51839]["signed_sheet_id"] == 239
    assert samples[51839]["hashimoto_sector"] == "chiral"
    assert samples[51839]["probe_slot"] == 3


def test_control_plane_keeps_architecture_boundary_honest():
    data = run_abi()
    boundary = " ".join(data["claim_boundary"])

    assert "not a canonical E8-root ordering" in boundary
    assert "bench work" in boundary
    assert "does not replace route, fault, or calibration policy" in boundary
    assert "data/w33_selector_e6_e8_runtime_bridge.json" in data["source_certificates"]
    assert "data/w33_frequency_bin_lab_packet.json" in data["source_certificates"]


def test_control_plane_publication_anchor():
    docs = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

    assert 'id="holonet-control-plane-abi"' in docs
    assert "w33_architecture_control_plane_abi.py" in docs
    assert "w33_architecture_control_plane_abi.json" in docs
    assert "24&times;5&times;6&times;9&times;2&times;4 = 51840" in docs
