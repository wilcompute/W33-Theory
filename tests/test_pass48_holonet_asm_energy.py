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


def test_holonet_asm_compiles_to_4bit_and_6502_style_targets():
    result = run_script("w33_holonet_asm.py", "w33_holonet_asm.json")

    assert result["verified"] is True
    assert result["four_bit_target"]["matches_reference"] is True
    assert result["four_bit_target"]["program_instructions"] == 22
    assert result["eight_bit_6502_style_target"]["matches_reference"] is True
    assert result["eight_bit_6502_style_target"]["verified_pairs"] == 1600
    assert result["eight_bit_6502_style_target"]["has_mul_mod_primitives"] is False
    assert result["checks"]["eight_bit_synthesizes_arithmetic_from_branches"] is True


def test_packet_energy_lifts_per_trit_tax_to_minimal_packet():
    # Refresh the per-trit source first, because packet energy depends on it.
    run_script("w33_ternary_energy.py", "w33_ternary_energy.json")
    result = run_script("w33_packet_energy.py", "w33_packet_energy.json")

    assert result["verified"] is True
    assert result["traffic_model"]["total_packet_trits"] == 72
    assert result["traffic_model"]["body_phase_trits"] == 48
    assert result["traffic_model"]["epilogue_trits"] == 8
    assert result["binary_vs_ternary"]["binary_host_bits"] == 144
    assert 1.26 < result["binary_vs_ternary"]["bit_traffic_tax"] < 1.263


def test_pass48_publication_anchors():
    note_files = [
        ROOT / "analysis" / "w33_holonet_asm.py",
        ROOT / "analysis" / "w33_packet_energy.py",
    ]
    docs = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    holonet = (ROOT / "HOLONET.md").read_text(encoding="utf-8")
    main_paper = (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8")
    practical = (ROOT / "holonet_practical_implications.tex").read_text(
        encoding="utf-8"
    )
    ci = (ROOT / ".github" / "workflows" / "holonet-ci.yml").read_text(encoding="utf-8")

    assert all(path.exists() for path in note_files)
    assert "Holonet Router Widget" in docs
    assert "w33_holonet_asm.py" in holonet
    assert "Pass 48" in main_paper
    assert "Pass 48" in practical
    assert "w33_packet_energy.py" in ci
    assert "Pass 49" in docs
    assert "w33_holonet_retro_export.py" in holonet
    assert "Pass 49" in main_paper
    assert "Pass 49" in practical
    assert "w33_holonet_retro_export.py" in ci


def test_pass49_retro_exports_are_generated_and_verified():
    result = run_script("w33_holonet_retro_export.py", "w33_holonet_retro_export.json")

    assert result["verified"] is True
    assert result["targets"]["4004_style"]["instructions"] == 22
    assert result["targets"]["6502_style"]["instructions"] == 130
    assert result["targets"]["z80_style"]["instructions"] == 111
    assert result["targets"]["z80_style"]["matches_reference"] is True
    assert result["targets"]["z80_style"]["verified_pairs"] == 1600
    assert result["checks"]["sample_agrees_across_targets"] is True
    assert result["checks"]["z80_has_no_mul_or_mod_opcode"] is True

    for target in result["targets"].values():
        assert (ROOT / target["artifact"]).exists()
        assert (ROOT / target["trace"]).exists()
