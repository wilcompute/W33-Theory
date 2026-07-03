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


def test_frequency_bin_hashimoto_compiler_closes_probe_budget():
    run_script("w33_hashimoto_sector_spectrum.py", "w33_hashimoto_sector_spectrum.json")
    run_script("w33_ternary_energy.py", "w33_ternary_energy.json")
    run_script("w33_holonet_retro_export.py", "w33_holonet_retro_export.json")
    run_script("w33_packet_energy.py", "w33_packet_energy.json")
    run_script(
        "w33_holonet_firmware_fabric_profile.py",
        "w33_holonet_firmware_fabric_profile.json",
    )
    run_script(
        "w33_hashimoto_packet_phase_bridge.py",
        "w33_hashimoto_packet_phase_bridge.json",
    )
    result = run_script(
        "w33_frequency_bin_hashimoto_compiler.py",
        "w33_frequency_bin_hashimoto_compiler.json",
    )

    assert result["verified"] is True
    assert all(result["checks"].values())
    assert result["frequency_plan"]["total_bins"] == 11
    assert len(result["frequency_plan"]["hesse_bins"]) == 9
    assert len(result["frequency_plan"]["hashimoto_sidebands"]) == 2
    assert result["frequency_plan"]["hashimoto_branch_width"] == 11
    assert result["frequency_plan"]["all_bin_labels"] == [
        "H0",
        "H1",
        "H2",
        "H3",
        "H4",
        "H5",
        "H6",
        "H7",
        "H8",
        "S_gauge",
        "S_chiral",
    ]
    assert [
        row["phase_lane_tick"] for row in result["frequency_plan"]["hesse_bins"]
    ] == list(range(2, 72, 8))
    assert sorted(
        {row["qutrit_phase_degrees"] for row in result["frequency_plan"]["hesse_bins"]}
    ) == [
        0,
        120,
        240,
    ]
    assert result["probe_budget"]["phase_probes_per_mirror_atlas"] == 540
    assert result["probe_budget"]["phase_probes_per_supercycle"] == 12960
    assert result["probe_budget"]["runtime_slots_per_supercycle"] == 51840
    assert result["probe_budget"]["runtime_slots_per_phase_probe"] == 4
    assert result["checks"]["phase_probe_budget_is_one_quarter_runtime_slots"] is True


def test_frequency_bin_hashimoto_compiler_publication_anchors():
    docs = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    ci = (ROOT / ".github" / "workflows" / "holonet-ci.yml").read_text(encoding="utf-8")

    assert "Frequency-Bin Hashimoto Compiler" in docs
    assert "w33_frequency_bin_hashimoto_compiler.py" in docs
    assert "w33_frequency_bin_hashimoto_compiler.json" in docs
    assert "720&times;9&times;2 = 12960" in docs
    assert "w33_frequency_bin_hashimoto_compiler.py" in ci
    assert "tests/test_frequency_bin_hashimoto_compiler.py" in ci
