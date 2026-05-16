from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclii_octahedral_poisson_green_bridge import build_bridge


def test_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]
    assert s["vertex_count"] == 6
    assert s["rank_laplacian"] == 5
    assert s["nullity_laplacian"] == 1
    assert abs(s["trace_l_plus"] - (13.0 / 12.0)) < 1e-9


def test_operator_shapes_and_core_entries() -> None:
    payload = build_bridge()
    L = payload["operators"]["L"]
    Lp = payload["operators"]["L_plus"]
    assert len(L) == 6 and len(L[0]) == 6
    assert len(Lp) == 6 and len(Lp[0]) == 6
    assert abs(L[0][0] - 4.0) < 1e-9
    assert abs(L[0][1] - 0.0) < 1e-9


def test_sample_poisson_solutions_have_zero_residual() -> None:
    payload = build_bridge()
    for item in payload["sample_poisson_solutions"].values():
        assert abs(item["source_sum"]) < 1e-9
        assert abs(item["solution_sum"]) < 1e-8
        assert max(abs(x) for x in item["residual"]) < 1e-8


def test_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
