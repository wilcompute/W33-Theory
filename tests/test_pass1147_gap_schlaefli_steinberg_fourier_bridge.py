"""Focused regression for the GAP-owned Pass 1147 certificate."""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess

import pytest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT / "analysis" / "w33_pass1147_schlaefli_steinberg_fourier_bridge.g"
)
CERTIFICATE = (
    ROOT / "data" / "w33_pass1147_schlaefli_steinberg_fourier_bridge.json"
)


def _assert_exact_certificate(payload: dict[str, object]) -> None:
    assert payload["status"] == "PASS"
    assert payload["directed_schlaefli"] == {
        "object": (
            "three colored copies of the directed-edge carrier of "
            "SRG(27,16,10,8)"
        ),
        "shell_patterns": [
            [-4, 0, 4],
            [-4, 4, 0],
            [0, -4, 4],
            [0, 4, -4],
            [4, -4, 0],
            [4, 0, -4],
        ],
        "shell_sizes": [27] * 6,
        "color_fiber_sizes": [432, 432, 432],
        "a2_orbit_sizes": [
            1,
            27,
            27,
            27,
            270,
            432,
            27,
            27,
            270,
            27,
            1,
            432,
            432,
            240,
        ],
        "srg_parameters": [27, 16, 10, 8],
        "directed_edge_count": 432,
        "directed_edge_stabilizer": {"order": 120, "structure": "S5"},
        "objectwise_bijection_verified": True,
    }

    transform = payload["steinberg_transform"]
    assert transform["matrix_shape"] == [325, 432]
    assert transform["rank"] == 81
    assert transform["rank_mod_1000003"] == 81
    assert transform["reversal_odd"] is True
    assert transform["vector_norm_squared"] == 600
    assert transform["gram_identity"] == "G^2=3200G"
    assert transform["projective_lines"] == 216
    assert transform["projective_dimension"] == 81
    assert transform["projective_valencies"] == [120, 60, 35]
    assert transform["absolute_angle_relations_form_association_scheme"] is False

    torsor = payload["a2_color_torsor"]
    assert torsor["combined_matrix_shape"] == [975, 1296]
    assert torsor["combined_rank"] == 243
    assert torsor["rational_sector_ranks"] == [81, 162]
    assert torsor["complex_sector_ranks"] == [81, 81, 81]

    enhanced = payload["enhanced_map"]
    assert enhanced["matrix_shape"] == [1020, 2240]
    assert enhanced["rank"] == 288
    assert enhanced["kernel_dimension"] == 1952
    assert enhanced["active_source_profile"] == {
        "cubic": 240,
        "schlaefli": 1296,
        "silent": 704,
    }
    assert enhanced["supports_disjoint"] is True

    residual = payload["residual_representation"]
    assert residual["dimension"] == 1952
    assert residual["degree_multiplicities"] == [
        [1, 13],
        [6, 16],
        [15, 5],
        [15, 4],
        [20, 21],
        [24, 2],
        [30, 9],
        [60, 4],
        [64, 10],
        [90, 1],
    ]


def test_checked_in_certificate_has_exact_pass1147_invariants() -> None:
    _assert_exact_certificate(json.loads(CERTIFICATE.read_text(encoding="utf-8")))


@pytest.mark.skipif(shutil.which("gap") is None, reason="GAP is required")
def test_gap_rebuild_is_deterministic(tmp_path: Path) -> None:
    (tmp_path / "data").mkdir()
    completed = subprocess.run(
        ["gap", "-q", str(SOURCE)],
        cwd=tmp_path,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=300,
    )
    assert completed.returncode == 0, completed.stdout[-6000:]
    rebuilt = (
        tmp_path
        / "data"
        / "w33_pass1147_schlaefli_steinberg_fourier_bridge.json"
    )
    assert rebuilt.read_bytes() == CERTIFICATE.read_bytes()
    _assert_exact_certificate(json.loads(rebuilt.read_text(encoding="utf-8")))
