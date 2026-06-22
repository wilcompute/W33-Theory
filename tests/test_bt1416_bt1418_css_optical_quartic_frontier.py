#!/usr/bin/env python3
"""Regression tests for BT1416-BT1418."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_tool(relpath: str) -> dict:
    proc = subprocess.run(
        [sys.executable, str(ROOT / relpath)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(proc.stdout)


def load_json(relpath: str) -> dict:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def test_bt1416_sparse_css_intertwiner() -> None:
    out = run_tool("tools/bt1416_css_sparse_intertwiner_matrices.py")
    assert out == {
        "bt": 1416,
        "logical_qutrits": 81,
        "verified": True,
    }

    data = load_json("data/bt1416_css_sparse_intertwiner_matrices.json")
    assert data["verified"] is True
    assert all(data["checks"].values())
    assert data["css_summary"]["parameters"] == "[[240,81,3]]_3 edge-chain carrier"
    assert data["css_summary"]["HX_shape"] == [40, 240]
    assert data["css_summary"]["HZ_shape"] == [160, 240]
    assert data["css_summary"]["rank_HX"] == 39
    assert data["css_summary"]["rank_HZ"] == 120
    assert data["css_summary"]["logical_qutrits"] == 81
    assert data["css_summary"]["commuting"] is True
    assert data["frontend_summary"]["frontend_check_shape"] == [216, 4]
    assert data["frontend_summary"]["frontend_rank"] == 1
    assert data["frontend_summary"]["min_even_kernel_distance"] == 2
    assert data["intertwiner_summary"]["shape"] == [240, 240]
    assert data["intertwiner_summary"]["nonzero_entries"] == 240
    assert data["intertwiner_summary"]["guard_tail"] == [216, 239]


def test_bt1417_linear_optical_dual_port_primitives() -> None:
    out = run_tool("tools/bt1417_linear_optical_dual_port_primitives.py")
    assert out == {
        "bt": 1417,
        "total_detector_bins": 192,
        "verified": True,
    }

    data = load_json("data/bt1417_linear_optical_dual_port_primitives.json")
    assert data["verified"] is True
    assert all(data["checks"].values())
    assert data["primitive_summary"] == {
        "active_residue_detector_bins": 168,
        "edge_channel_couplers": 21,
        "guard_apertures": 24,
        "identity": "21 couplers, 42 orientation latches, 168 active bins, 24 guard apertures",
        "oriented_phase_latches": 42,
        "total_detector_bins": 192,
    }
    csaszar_gram = data["analyzer_matrices"]["csaszar_gram"]
    szilassi_gram = data["analyzer_matrices"]["szilassi_gram"]
    assert all(csaszar_gram[i][i] == 6 for i in range(7))
    assert all(szilassi_gram[i][i] == 6 for i in range(7))
    assert all(csaszar_gram[i][j] == 1 for i in range(7) for j in range(7) if i != j)
    assert [
        row["tomotope_flag"] for row in data["primitive_layers"]["guard_apertures"]
    ] == list(range(168, 192))


def test_bt1418_d4_quartic_magic_injection() -> None:
    out = run_tool("tools/bt1418_d4_quartic_magic_injection_frontier.py")
    assert out == {
        "bt": 1418,
        "guard_apertures": 24,
        "oriented_tomotope_tokens": 192,
        "verified": True,
    }

    data = load_json("data/bt1418_d4_quartic_magic_injection_frontier.json")
    assert data["verified"] is True
    assert all(data["checks"].values())
    assert data["atom_summary"]["identity"] == (
        "2 atoms * 4 branches * 3 qutrit phases = 24; times 8 D4 orientations = 192"
    )
    assert data["atom_summary"]["guard_apertures"] == 24
    assert data["atom_summary"]["oriented_tomotope_tokens"] == 192
    assert [row["css_edge_index"] for row in data["resource_apertures"]] == list(
        range(216, 240)
    )
    assert data["golden_shell_comparison"] == {
        "identity": "4 quartic branches * 27 Steinberg cycles * 8 D4 orientations = 864 per atom",
        "per_atom_steinberg_d4_shell": 864,
        "reading": (
            "The exact finite counterpart of a golden-quartic topology is the "
            "repo's D4/Weyl orientation shell, not the continuum Moebius-ball "
            "electron hypothesis."
        ),
        "repo_golden_d4_weyl_shell": 864,
        "two_atom_steinberg_d4_shell": 1728,
    }


def test_bt1416_bt1418_publication_anchors() -> None:
    docs = " ".join((ROOT / "docs" / "index.html").read_text(encoding="utf-8").split())
    holonet = " ".join(
        (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8").split()
    )
    runner = (ROOT / "tools" / "bt1389_run_runtime_frontier_release_lock.sh").read_text(
        encoding="utf-8"
    )
    focused = (ROOT / "scripts" / "run_focused_bridge_tests.py").read_text(
        encoding="utf-8"
    )

    assert (
        "BT1416&ndash;BT1418: CSS matrix, optical primitive, D4-quartic injection"
        in docs
    )
    assert "BT1416_BT1418_css_optical_quartic_frontier.md" in docs
    assert "BT1416 sparse CSS intertwiner" in holonet
    assert "BT1417 linear-optical dual-port primitive synthesis" in holonet
    assert "BT1418 finite D4-quartic magic injection" in holonet
    assert "bt1416_css_sparse_intertwiner_matrices.py" in runner
    assert "bt1418_d4_quartic_magic_injection_frontier.py" in runner
    assert "test_bt1416_bt1418_css_optical_quartic_frontier.py" in runner
    assert "test_bt1416_bt1418_css_optical_quartic_frontier.py" in focused


if __name__ == "__main__":
    test_bt1416_sparse_css_intertwiner()
    test_bt1417_linear_optical_dual_port_primitives()
    test_bt1418_d4_quartic_magic_injection()
    test_bt1416_bt1418_publication_anchors()
    print("BT1416-BT1418 focused tests passed")
