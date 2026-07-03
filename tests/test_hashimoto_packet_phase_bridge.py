import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_script(script_name: str, data_name: str) -> dict:
    subprocess.run(
        [sys.executable, str(ROOT / "analysis" / script_name)],
        cwd=ROOT,
        check=True,
    )
    return json.loads((ROOT / "data" / data_name).read_text(encoding="utf-8"))


def test_hashimoto_packet_phase_bridge_closes_packet_and_mirror_tiling():
    run_script("w33_hashimoto_sector_spectrum.py", "w33_hashimoto_sector_spectrum.json")
    run_script("w33_ternary_energy.py", "w33_ternary_energy.json")
    run_script("w33_holonet_retro_export.py", "w33_holonet_retro_export.json")
    run_script("w33_packet_energy.py", "w33_packet_energy.json")
    run_script(
        "w33_holonet_firmware_fabric_profile.py",
        "w33_holonet_firmware_fabric_profile.json",
    )
    result = run_script(
        "w33_hashimoto_packet_phase_bridge.py",
        "w33_hashimoto_packet_phase_bridge.json",
    )

    assert result["verified"] is True
    assert all(result["checks"].values())
    assert result["phase_analyzers"]["gauge"]["complex_mode_count"] == 48
    assert result["phase_analyzers"]["chiral"]["complex_mode_count"] == 30
    assert result["packet_binding"]["packet_body_phase_trits"] == 48
    assert result["packet_binding"]["mirror_atlas_packet_frames"] == 30
    assert result["packet_binding"]["supercycle_packet_frames"] == 720
    assert result["packet_binding"]["phase_lane_ticks"] == list(range(2, 72, 8))
    assert result["checks"]["gauge_complex_modes_fill_packet_body"] is True
    assert result["checks"]["chiral_complex_modes_fill_one_mirror_atlas"] is True
    assert (
        result["checks"]["supercycle_tiles_gauge_modes_by_chiral_multiplicity"] is True
    )
    assert (
        result["checks"]["supercycle_tiles_chiral_modes_by_gauge_multiplicity"] is True
    )
    assert (
        abs(
            result["phase_analyzers"]["gauge"]["analyzer_phase_degrees"] - 72.4515993862
        )
        < 1e-9
    )
    assert (
        abs(
            result["phase_analyzers"]["chiral"]["analyzer_phase_degrees"]
            - 127.0866899341
        )
        < 1e-9
    )


def test_hashimoto_packet_phase_bridge_publication_anchors():
    docs = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    ci = (ROOT / ".github" / "workflows" / "holonet-ci.yml").read_text(encoding="utf-8")

    assert "Hashimoto Packet Phase Bridge" in docs
    assert "w33_hashimoto_packet_phase_bridge.py" in docs
    assert "w33_hashimoto_packet_phase_bridge.json" in docs
    assert "15&times;48 = 24&times;30" in docs
    assert "w33_hashimoto_packet_phase_bridge.py" in ci
    assert "tests/test_hashimoto_packet_phase_bridge.py" in ci
