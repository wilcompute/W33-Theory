#!/usr/bin/env python3
"""Read-only compatibility validator for the former duality postprocessor.

The Pass4945--4947 owner producer now emits corrected Q(4,3)-line and
W(3,3)-point labels directly and rebuilds the claimed cross-incidence.  This
historical entry point remains for workflows, but a stale producer must now
fail rather than be repaired after generation.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P4945 = ROOT / "data/PART_W33_PASS4945_STEINER_NONEDGE_S3_HOLONOMY.json"
P4946 = ROOT / "data/PART_W33_PASS4946_MAXCUT_STEINER_DUAL_W33_INCIDENCE.json"
P4947 = ROOT / "data/PART_W33_PASS4947_W33_TRIAD_CURVATURE.json"


def main() -> int:
    p45 = json.loads(P4945.read_text())
    p46 = json.loads(P4946.read_text())
    p47 = json.loads(P4947.read_text())

    assert p45["base_graph"].startswith("complement of Q(4,3)")
    assert "disjoint W33 lines" in p45["carrier"]
    q = p46["quotient"]
    assert q["maximum_cut_triples"] == "40 W(3,3) points"
    assert q["Steiner_triples"].startswith("40 W(3,3) lines")
    assert q["F3_rank_A_plus_I"] == {
        "columns_Q43_lines": 15,
        "rows_W33_points": 11,
    }
    assert q["gram_identities"] == ["ZZ^T=4I+A_W", "Z^TZ=4I+A_Q"]
    assert q["rank"] == 25
    assert p47["Q43_independent_triads"] == 3240
    assert p47["geometric_classification"]["zero_common_neighbors"] == 1080
    assert p47["geometric_classification"]["two_common_neighbors"] == 2160
    assert p47["standard_W33_point_graph_baseline"]["one_common_neighbor"] == 2880
    assert p47["standard_W33_point_graph_baseline"]["four_common_neighbors"] == 360

    print("PASS Pass4945-4947 owner producer emits corrected carriers directly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
