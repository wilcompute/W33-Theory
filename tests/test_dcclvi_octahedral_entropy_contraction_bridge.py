from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclvi_octahedral_entropy_contraction_bridge import build_bridge


def test_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]
    assert s["state_count"] == 6
    assert abs(s["initial_entropy_nats"] - 0.0) < 1e-12
    assert abs(s["initial_kl_nats"] - math.log(6.0)) < 1e-12
    assert abs(s["mixing_ratio"] - 0.5) < 1e-12


def test_support_and_monotonicity() -> None:
    payload = build_bridge()
    tl = payload["timeline"]
    assert tl[1]["support_size"] == 4
    H = [x["entropy_nats"] for x in tl]
    D = [x["kl_to_uniform_nats"] for x in tl]
    assert all(H[t + 1] > H[t] for t in range(0, 4))
    assert all(D[t + 1] < D[t] for t in range(0, 4))


def test_tv_ratio_and_pinsker() -> None:
    payload = build_bridge()
    tl = payload["timeline"]
    tv = [x["tv_to_uniform"] for x in tl]
    for t in range(1, 6):
        assert abs(tv[t + 1] / tv[t] - 0.5) < 1e-8
    for x in tl:
        assert x["pinsker_lhs"] <= x["pinsker_rhs"] + 1e-12


def test_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
