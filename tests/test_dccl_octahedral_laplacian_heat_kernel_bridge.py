from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccl_octahedral_laplacian_heat_kernel_bridge import build_bridge


def test_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]
    assert s["vertex_count"] == 6
    assert s["edge_count"] == 12
    assert s["degree"] == 4
    assert s["triangle_count"] == 8
    assert s["spectral_gap"] == 4


def test_laplacian_spectrum_and_triangles() -> None:
    payload = build_bridge()
    spec = payload["spectral_data"]
    assert spec["laplacian_eigenvalues"] == [0, 4, 4, 4, 6, 6]
    assert spec["triangle_count"] == 8


def test_heat_kernel_normalization() -> None:
    payload = build_bridge()
    k0 = payload["sample_heat_kernels"]["0.0"]
    assert k0[0][0] == 1.0
    assert k0[0][1] == 0.0

    k1 = payload["sample_heat_kernels"]["1.0"]
    for row in k1:
        assert abs(sum(row) - 1.0) < 1e-9


def test_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
