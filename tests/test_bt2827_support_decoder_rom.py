from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_decoder_rom_has_exact_81_valid_entries() -> None:
    rtl = (ROOT / "rtl" / "w33_pass2827_support_decoder_rom.sv").read_text(encoding="utf-8")
    entries = re.findall(
        r"8'b([01]{8}): begin state_o = 8'b([01]{8}); valid_o = 1'b1; end",
        rtl,
    )
    assert len(entries) == 81
    assert len({code for code, _ in entries}) == 81
    assert len({state for _, state in entries}) == 81

    for _, packed_state in entries:
        fields = [packed_state[index : index + 2] for index in range(0, 8, 2)]
        assert all(field in {"00", "01", "10"} for field in fields)


def test_decoder_rom_default_is_fail_closed() -> None:
    rtl = (ROOT / "rtl" / "w33_pass2827_support_decoder_rom.sv").read_text(encoding="utf-8")
    assert "default: begin state_o = 8'b0; valid_o = 1'b0; end" in rtl
