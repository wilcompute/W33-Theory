import csv
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


def regenerate_lab_packet() -> dict:
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
    run_script(
        "w33_frequency_bin_hashimoto_compiler.py",
        "w33_frequency_bin_hashimoto_compiler.json",
    )
    return run_script(
        "w33_frequency_bin_lab_packet.py",
        "w33_frequency_bin_lab_packet.json",
    )


def test_frequency_bin_lab_packet_closes_mirror_and_supercycle_schedule():
    result = regenerate_lab_packet()

    assert result["verified"] is True
    assert all(result["checks"].values())
    assert result["schedule_summary"]["rows"] == 540
    assert result["schedule_summary"]["probes_per_packet"] == 18
    assert result["schedule_summary"]["runtime_slots_per_probe"] == 4
    assert result["schedule_summary"]["runtime_slots_per_mirror_atlas"] == 2160
    assert result["schedule_summary"]["supercycle_probe_rows"] == 12960
    assert result["schedule_summary"]["supercycle_runtime_slots"] == 51840
    assert result["checks"]["mirror_identity_540_times_4_equals_2160"] is True
    assert (
        result["checks"]["supercycle_identity_24_times_schedule_equals_12960"] is True
    )


def test_frequency_bin_lab_packet_writes_csv_and_jsonl_schema():
    regenerate_lab_packet()

    csv_path = ROOT / "docs" / "holonet_frequency_bin_phase_probe_schedule.csv"
    jsonl_path = ROOT / "docs" / "holonet_frequency_bin_raw_shot_template.jsonl"

    with csv_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 540
    assert rows[0]["probe_id"] == "0"
    assert rows[0]["runtime_slot_start"] == "0"
    assert rows[-1]["probe_id"] == "539"
    assert rows[-1]["runtime_slot_end"] == "2159"
    assert {row["sector"] for row in rows} == {"gauge", "chiral"}
    assert {row["qutrit_phase_degrees"] for row in rows} == {"0", "120", "240"}

    template_rows = [
        json.loads(line)
        for line in jsonl_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert len(template_rows) == 4
    assert template_rows[0]["pulse_shaper_phase_degrees"] == 72.4515993862077
    assert template_rows[1]["pulse_shaper_phase_degrees"] == 127.08668993406384
    assert template_rows[0]["plus_counts"] is None
    assert template_rows[0]["accepted_flag"] is None
    assert (
        template_rows[0]["claim_boundary"]
        == "template row only; fill counts from bench data"
    )


def test_frequency_bin_lab_packet_publication_anchors():
    docs = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    ci = (ROOT / ".github" / "workflows" / "holonet-ci.yml").read_text(encoding="utf-8")

    assert "Frequency-Bin Phase-Probe Lab Packet" in docs
    assert "w33_frequency_bin_lab_packet.py" in docs
    assert "w33_frequency_bin_lab_packet.json" in docs
    assert "540&times;4 = 2160" in docs
    assert "w33_frequency_bin_lab_packet.py" in ci
    assert "tests/test_frequency_bin_lab_packet.py" in ci
