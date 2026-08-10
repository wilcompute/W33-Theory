#!/usr/bin/env python3
"""Focused direct test for BT865 dual-torsor Steinberg compilation."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def test_bt865_dual_torsor_steinberg_compiler() -> None:
    subprocess.run(
        [sys.executable,
         str(ROOT / "analysis/bt865_dual_torsor_steinberg_compiler.py")],
        cwd=ROOT,
        check=True,
    )
    data = json.loads(
        (ROOT / "data/bt865_dual_torsor_steinberg_compiler.json").read_text(encoding="utf-8")
    )
    assert all(data["checks"].values())
    assert data["chain_complex"]["dim_H1_mod3"] == 81
    assert data["point_state_torsor"]["complex_restriction"] == "3 Reg(H27)"
    assert data["line_program_torsor"]["complex_restriction"] == "3 Reg(F3^3)"
    assert [w["rank_gain_mod_boundaries"]
            for w in data["point_state_torsor"]["orbit_basis_witnesses"]] == [27] * 3
    assert [w["rank_gain_mod_boundaries"]
            for w in data["line_program_torsor"]["orbit_basis_witnesses"]] == [27] * 3
    triality = data["canonical_triality_axis"]
    assert triality["complex_sector_dimensions"] == [27, 27, 27]
    assert triality["native_nilpotent_ranks"] == [54, 27, 0]
    assert triality["native_kernel_dimensions"] == [27, 54, 81]
    assert triality["native_successive_quotients"] == [27, 27, 27]
    assert triality["jordan_blocks_size_3"] == 27
    assert data["direction_census"]["point_c3_directions"] == 13
    assert data["direction_census"]["line_c3_directions"] == 13

    note = (ROOT / "analysis/BT865_dual_torsor_steinberg_compiler.md").read_text(encoding="utf-8")
    assert "H1(F3) restricted to O3" in note
    assert "rank(N), rank(N^2), rank(N^3) = 54, 27, 0" in note
    paper = (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8")
    docs = (ROOT / "docs/index.html").read_text(encoding="utf-8")
    assert "The dual-torsor Steinberg compiler" in paper
    assert "27\\subset54\\subset81" in paper
    assert "BT858&ndash;BT865" in docs
    assert "three regular copies of either torsor" in docs
    assert "dual 27-line Bell shell" in docs


if __name__ == "__main__":
    test_bt865_dual_torsor_steinberg_compiler()
    print("BT865 dual-torsor Steinberg compiler test passed")
