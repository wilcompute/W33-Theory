#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_tool() -> dict:
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "bt1412_toroidal_q4_oscillator_boundary.py"),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(proc.stdout)


def load_result() -> dict:
    return json.loads(
        (ROOT / "data" / "bt1412_toroidal_q4_oscillator_boundary.json").read_text(
            encoding="utf-8"
        )
    )


def test_bt1412_generator_runs_true() -> None:
    out = run_tool()
    assert out == {
        "bt": 1412,
        "edge_boundary": 21,
        "oscillator_mark_aperture": "1/6",
        "q4_square_faces": 24,
        "verified": True,
    }

    data = load_result()
    assert data["verified"] is True
    assert all(data["checks"].values())


def test_bt1412_q4_clock_and_parity_projection() -> None:
    data = load_result()
    clock = data["q4_toroidal_clock"]

    assert clock["vertices"] == 16
    assert clock["edges"] == 32
    assert clock["square_faces"] == 24
    assert clock["gray_flip_sequence"] == [
        1,
        2,
        1,
        3,
        1,
        2,
        1,
        0,
        1,
        2,
        1,
        3,
        1,
        2,
        1,
        0,
    ]
    assert [row["board_parity"] for row in clock["parity_trace"]] == [
        row["q4_parity"] for row in clock["parity_trace"]
    ]
    assert [row["q4_parity"] for row in clock["parity_trace"]] == [0, 1] * 8

    projection = clock["even_projection"]
    assert projection["ticks"] == [0, 6, 3, 5, 9, 15, 10, 12]
    assert projection["parity"] == [0]
    assert projection["cyclic_hamming_distances"] == [2] * 8
    assert projection["min_pairwise_hamming_distance"] == 2
    assert projection["max_pairwise_hamming_distance"] == 4


def test_bt1412_oscillator_toroidal_edge_splice() -> None:
    data = load_result()

    assert data["bridge_identities"] == {
        "codec_sum": "(2+7+7)*12 = 16*12 = 192",
        "dual_polyhedron_e_equals_v_plus_f": "7+14=14+7=21",
        "edge_boundary_from_forbidden_genus": "24 - 3 = 21",
        "one_sixth_aperture": "4/24 = 1/6",
        "q4_face_formula": "C(4,2)*2^2 = 24 = q*(q-1)*(q+1)",
        "q4_square_faces": 24,
    }
    assert data["oscillator_boundary"] == {
        "carrier_level": 6,
        "forbidden_genus": 3,
        "forbidden_genus_discriminant": 145,
        "mark_aperture": "1/6",
        "mark_count": 4,
        "mod12_marks": [0, 3, 4, 7],
    }
    assert data["toroidal_dual_boundary"]["csaszar"] == {
        "edges": 21,
        "faces": 14,
        "genus": 1,
        "vertices": 7,
    }
    assert data["toroidal_dual_boundary"]["szilassi"] == {
        "edges": 21,
        "faces": 7,
        "genus": 1,
        "vertices": 14,
    }
    assert data["toroidal_dual_boundary"]["shared_edge_invariant"] == 21


def test_bt1412_snake_boundary_and_publication_anchors() -> None:
    data = load_result()
    assert data["q4_toroidal_clock"]["extra_q4_chords_outside_gray_cycle"] == 16
    assert "not an induced snake/coil" in data["q4_toroidal_clock"]["snake_boundary"]
    assert "not claimed to be an induced snake code" in data["physical_reading"]

    docs = " ".join((ROOT / "docs" / "index.html").read_text(encoding="utf-8").split())
    holonet = " ".join(
        (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8").split()
    )

    assert "BT1412: toroidal Q4 oscillator boundary" in docs
    assert "BT1412_toroidal_q4_oscillator_boundary.md" in docs
    assert "BT1412 toroidal Q4 oscillator boundary" in holonet
    assert "24\\ \\text{Q4 square faces}" in holonet
    assert "\\frac{4}{24}=\\frac16" in holonet
    assert "24-3=21" in holonet


if __name__ == "__main__":
    test_bt1412_generator_runs_true()
    test_bt1412_q4_clock_and_parity_projection()
    test_bt1412_oscillator_toroidal_edge_splice()
    test_bt1412_snake_boundary_and_publication_anchors()
    print("BT1412 focused tests passed")
