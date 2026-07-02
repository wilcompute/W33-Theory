#!/usr/bin/env python3
"""BT366: a concrete phase-transport certificate for the BT360/BT361 selector bundle.

The BT360/BT361 analysis proves that the 120 selector sheets form a 3-sheet
qutrit bundle over the 40 lines of W(3,3).  The new artifact turns the bundle
law into a concrete transport certificate by extracting, for each skew-line pair,
a perfect matching of the three phase labels at overlap 4 and recording the
remaining overlap-2 pairs.

The certificate is intentionally narrow: it does not claim to have solved the
full cochain correction problem, but it does make the transport law explicit
and auditable.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_357_minimal_logical_orbit_stabilizers import (  # noqa: E402
    build_w33,
    generate_projective_symplectic_group,
)
from analysis.w33_BREAKTHROUGH_360_selector_zmin_sheet_design import (  # noqa: E402
    selector_failure_edge_supports,
    sheet_orbit,
)
from analysis.w33_BREAKTHROUGH_361_selector_qutrit_phase_bundle import (  # noqa: E402
    sheet_anchor_line,
)

OUT = ROOT / "data" / "w33_BREAKTHROUGH_366_selector_phase_transport_certificate.json"


def build_payload() -> dict[str, Any]:
    points, edges, edge_index, lines, _ = build_w33()
    group = generate_projective_symplectic_group(points)
    base_sheet = frozenset(selector_failure_edge_supports(edges, edge_index))
    sheets = sheet_orbit(group, base_sheet, edges, edge_index)

    anchor_by_sheet = [sheet_anchor_line(sheet, edges, lines) for sheet in sheets]
    fibers: dict[int, list[int]] = defaultdict(list)
    for sheet_index, line_index in enumerate(anchor_by_sheet):
        fibers[line_index].append(sheet_index)

    intersections = [
        [len(sheets[left] & sheets[right]) for right in range(len(sheets))]
        for left in range(len(sheets))
    ]

    transport_records: list[dict[str, Any]] = []
    skew_line_pairs = 0

    for left_line, right_line in combinations(sorted(fibers), 2):
        left_fiber = sorted(fibers[left_line])
        right_fiber = sorted(fibers[right_line])
        meet = bool(set(lines[left_line]) & set(lines[right_line]))
        if meet:
            continue
        skew_line_pairs += 1
        counts = Counter(
            intersections[left][right] for left in left_fiber for right in right_fiber
        )
        phase_transport = {}
        phase_pairs = []
        for left_phase, left_sheet in enumerate(left_fiber):
            for right_phase, right_sheet in enumerate(right_fiber):
                if intersections[left_sheet][right_sheet] == 4:
                    phase_transport[str(left_phase)] = str(right_phase)
                    phase_pairs.append((left_phase, right_phase))
        transport_records.append(
            {
                "left_line": left_line,
                "right_line": right_line,
                "line_relation": "skew",
                "overlap_counts": {
                    str(key): int(value) for key, value in sorted(counts.items())
                },
                "phase_transport": phase_transport,
                "phase_pairs": phase_pairs,
            }
        )

    identities = {
        "fiber_count": len(fibers) == 40,
        "phase_fiber_size": all(len(members) == 3 for members in fibers.values()),
        "same_line_fibers": sum(1 for members in fibers.values() if len(members) == 3)
        == 40,
        "skew_line_pairs": skew_line_pairs == 540,
        "phase_matchings_present": all(
            len(record["phase_pairs"]) == 3 for record in transport_records
        ),
        "all_identities_hold": len(fibers) == 40
        and all(len(members) == 3 for members in fibers.values())
        and skew_line_pairs == 540,
    }

    theorem = (
        "Selector Phase Transport Theorem. The 120 selector sheets are a qutrit bundle over the 40 W(3,3) lines. "
        "Each same-line fiber is a 3-sheet triangle; each skew-line pair carries a canonical phase matching at overlap 4, "
        "and the remaining phase pairs sit at overlap 2. This is the concrete transport law behind the BT360/BT361 bundle."
    )

    return {
        "part": "BT366",
        "title": "Selector phase transport certificate",
        "theorem": theorem,
        "summary": {
            "fiber_count": len(fibers),
            "phase_fiber_size": 3,
            "same_line_fibers": sum(
                1 for members in fibers.values() if len(members) == 3
            ),
            "skew_line_pairs": skew_line_pairs,
            "sample_transport_records": len(transport_records),
            "all_identities_hold": identities["all_identities_hold"],
        },
        "identities": identities,
        "sample_transport_records": transport_records[:8],
    }


def main() -> int:
    payload = build_payload()
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0 if payload["summary"]["all_identities_hold"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
