from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccli_octahedral_spectral_projector_semigroup_bridge import build_bridge


def test_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]
    assert s["vertex_count"] == 6
    assert s["rank_p0"] == 1
    assert s["rank_p4"] == 3
    assert s["rank_p6"] == 2
    assert s["spectral_gap"] == 4


def test_projector_mode_checks() -> None:
    payload = build_bridge()
    p0 = payload["projectors"]["P0"]
    assert abs(p0[0][0] - (1.0 / 6.0)) < 1e-9
    assert abs(p0[0][5] - (1.0 / 6.0)) < 1e-9


def test_sample_semigroup_match() -> None:
    payload = build_bridge()
    sample = payload["sample_semigroup_checks"]
    assert sample["0.0"]["spectral"] == sample["0.0"]["direct"]
    assert sample["1.0"]["spectral"] == sample["1.0"]["direct"]


def test_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
