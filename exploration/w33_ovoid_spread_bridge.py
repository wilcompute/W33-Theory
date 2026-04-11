"""Corrected q=3 spread/ovoid status on the explicit W(3,3) geometry.

The older version of this file repeated a false claim:

    alpha(W(3,3)) = 10 and the 40 points partition into four ovoids.

That is not true for the explicit q = 3 symplectic generalized quadrangle.
The corrected exact status is:

    - point graph independence number = 7,
    - no 10-coclique exists,
    - hence no point-ovoid partition exists at q = 3,
    - one spread still consists of 10 disjoint lines of size 4,
    - there are exactly 36 spreads.

This light wrapper keeps the old filename alive while exposing the corrected
mathematical statement and, when available, the explicit certificate generated
by ``w33_spread_not_ovoid_bridge.py``.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
CERT_PATH = DATA_DIR / "w33_spread_not_ovoid_bridge_summary.json"


@lru_cache(maxsize=1)
def build_ovoid_spread_summary() -> dict[str, Any]:
    v, q = 40, 3
    line_size = q + 1          # 4
    spread_size = q**2 + 1     # 10
    spread_count = 36
    alpha_point_graph = 7

    cert = None
    if CERT_PATH.exists():
        cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    summary = {
        "status": "corrected",
        "q3_spread_dictionary": {
            "vertex_count": v,
            "line_size": line_size,
            "spread_size": spread_size,
            "spread_count": spread_count,
            "point_graph_alpha": alpha_point_graph,
        },
        "q3_spread_ovoid_theorem": {
            "spread_size_is_q_squared_plus_one": spread_size == 10,
            "spread_count_is_36": spread_count == 36,
            "the_explicit_point_graph_has_alpha_7": alpha_point_graph == 7,
            "there_is_no_point_ovoid_of_size_10_at_q_3": alpha_point_graph < spread_size,
            "the_honest_4_times_10_law_is_line_size_times_spread_size": v == line_size * spread_size,
        },
        "interpretation": (
            "At q = 3 the spread side survives exactly, but the point-ovoid side does not. "
            "One spread is still a partition of the 40 points into 10 disjoint lines of size 4, "
            "and there are 36 such spreads. But the explicit point graph has independence number 7, "
            "so the old four-ovoids reading is false. The honest `4 x 10` structure is line size "
            "times spread size."
        ),
    }

    if cert is not None:
        summary["explicit_certificate"] = {
            "size_7_witness_indices": cert["independence_certificate"]["size_7_witness_indices"],
            "size_8_exists": cert["independence_certificate"]["size_8_exists"],
            "spread_lines": cert["spread_certificate"]["spread_lines"],
        }

    return summary

