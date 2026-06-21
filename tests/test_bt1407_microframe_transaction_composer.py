#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORD_SHAPE = [
    "ERASE",
    "ROUTE",
    "PHASE",
    "X-CORR",
    "Z-CORR",
    "T-BIT",
    "RESTORE",
    "NEXT",
]


def run_tool() -> dict:
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "bt1407_microframe_transaction_composer.py"),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(proc.stdout)


def load_result() -> dict:
    return json.loads(
        (ROOT / "data" / "bt1407_microframe_transaction_composer.json").read_text(
            encoding="utf-8"
        )
    )


def epilogue_rows(data: dict, h: int) -> list[dict]:
    return [tick for tick in data["epilogue_ticks"] if tick["h"] == h]


def test_bt1407_transaction_composer_runs_true() -> None:
    out = run_tool()
    assert out == {
        "bt": 1407,
        "epilogue_hesse_outcomes": [3, 4, 5],
        "selected_route_branch": 1,
        "verified": True,
    }

    data = load_result()
    assert data["verified"] is True
    assert all(data["checks"].values())
    assert data["frame_identity"] == (
        "48 Q6 body pulse ticks + 3 Hesse return words * 8 ticks = 72 ticks"
    )


def test_bt1407_stress_route_composes_full_frame() -> None:
    data = load_result()

    assert data["stress_selection"] == {
        "program": "six_digit_stress",
        "final_target_digit": 4,
        "selected_route_branch": 1,
        "epilogue_hesse_outcomes": [3, 4, 5],
    }
    assert data["region_histogram"] == {
        "local_lift_hesse_epilogue": 24,
        "tomotope_body": 48,
    }
    assert len(data["body_ticks"]) == 48
    assert len(data["epilogue_ticks"]) == 24
    assert [tick["frame_tick"] for tick in data["frame_tick_summary"]] == list(
        range(72)
    )
    assert [tick["frame_tick"] for tick in data["body_ticks"]] == list(range(48))
    assert [tick["frame_tick"] for tick in data["epilogue_ticks"]] == list(
        range(48, 72)
    )


def test_bt1407_epilogue_is_selected_hesse_branch() -> None:
    data = load_result()

    expected = {
        3: (list(range(48, 56)), "X^1 Z^0", 1, 0),
        4: (list(range(56, 64)), "X^1 Z^1", 0, 1),
        5: (list(range(64, 72)), "X^1 Z^2", 1, 2),
    }
    for h, (ticks, correction, t_bit, phase_trit) in expected.items():
        rows = epilogue_rows(data, h)
        assert [row["frame_tick"] for row in rows] == ticks
        assert [row["op"] for row in rows] == WORD_SHAPE
        assert {row["branch"] for row in rows} == {"Z Omega"}
        assert {row["route_trit"] for row in rows} == {1}
        assert {row["phase_trit"] for row in rows} == {phase_trit}
        assert {row["pauli_correction"] for row in rows} == {correction}
        assert {row["t_frame_bit"] for row in rows} == {t_bit}


def test_bt1407_publication_anchors() -> None:
    docs = " ".join((ROOT / "docs" / "index.html").read_text(encoding="utf-8").split())
    holonet = " ".join(
        (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8").split()
    )
    single = " ".join(
        (ROOT / "single_photon_universal_computation.tex")
        .read_text(encoding="utf-8")
        .split()
    )

    assert "BT1407: 72-tick microframe transaction" in docs
    assert "BT1407_microframe_transaction_composer.md" in docs
    assert "BT1407 microframe transaction composer" in holonet
    assert "48 Q6 body pulse ticks plus 3 Hesse return words equals 72 ticks" in holonet
    assert "BT1407 Microframe Transaction Composer" in single


if __name__ == "__main__":
    test_bt1407_transaction_composer_runs_true()
    test_bt1407_stress_route_composes_full_frame()
    test_bt1407_epilogue_is_selected_hesse_branch()
    test_bt1407_publication_anchors()
    print("BT1407 focused tests passed")
