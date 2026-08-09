#!/usr/bin/env python3
"""Pass 4531 -- exact bipartite schedule compiler for the 13-line flag gauge.

Input is the exhaustive Pass-4504 optimum section: ten quotient columns with 42
total line incidences supported on the Pass-4510 13-line K1 join 4K3 cell.

Scheduling model (stated, not smuggled in): each primitive operation routes one
source-line bit into one quotient-column XOR accumulator; in one clock a source
line may feed at most one accumulator and an accumulator may accept at most one
source.  The conflict graph is therefore the edge-coloring problem of a
bipartite incidence graph.  Its maximum degree is 9, so Konig's line-coloring
theorem gives a lower bound/optimum of 9.  A frozen 9-round schedule is verified
edge-for-edge and realizes the bound.

This is a Boolean/register schedule, not FPGA PPA, optical timing, a fault
threshold, or a claim of physical optimality under another hardware model.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS4531_FLAG_GAUGE_COMPILER.json"

SCHEDULE = [
    [(0,0),(1,1),(2,8),(3,4),(6,5),(7,7),(8,6),(9,9)],
    [(1,7),(2,9),(3,8),(4,5),(6,4),(9,6)],
    [(0,9),(1,6),(2,4),(3,5),(9,8)],
    [(0,8),(1,4),(2,5),(3,6),(4,9),(9,7)],
    [(1,5),(2,6),(3,7),(4,8),(5,4),(32,9)],
    [(2,7),(3,9),(6,8)],
    [(2,2),(3,3),(5,9),(7,8)],
    [(8,9),(32,8)],
    [(28,9),(36,8)],
]


def main() -> int:
    c = json.loads((ROOT / "data/PART_W33_PASS4504_MINIMAL_FLAG_SECTION.json").read_text())
    supports = c["optimum"]["ambient_line_supports"]
    assert len(supports) == 10
    incidences = {(line, col) for col, supp in enumerate(supports) for line in supp}
    assert len(incidences) == 42
    assert set().union(*map(set, supports)) == {0,1,2,3,4,5,6,7,8,9,28,32,36}

    source_degree = Counter(line for line, _ in incidences)
    column_degree = Counter(col for _, col in incidences)
    delta = max(max(source_degree.values()), max(column_degree.values()))
    assert delta == 9
    assert [column_degree[i] for i in range(10)] == [1,1,1,1,5,5,5,5,9,9]

    scheduled = set()
    for rnd in SCHEDULE:
        sources = [x for x, _ in rnd]
        cols = [y for _, y in rnd]
        assert len(sources) == len(set(sources))
        assert len(cols) == len(set(cols))
        for edge in rnd:
            assert edge in incidences
            assert edge not in scheduled
            scheduled.add(edge)
    assert scheduled == incidences
    assert len(SCHEDULE) == delta

    out = {
        "pass": 4531,
        "model": "one source-line -> one quotient XOR accumulator per primitive operation; no source or accumulator reused within a clock",
        "source_lines": sorted(source_degree),
        "quotient_columns": 10,
        "primitive_operations": 42,
        "column_degrees": [column_degree[i] for i in range(10)],
        "source_degrees": {str(k): source_degree[k] for k in sorted(source_degree)},
        "maximum_degree": delta,
        "depth_lower_bound": 9,
        "schedule_depth": len(SCHEDULE),
        "depth_optimal_in_model": True,
        "instantaneous_source_fanout": 1,
        "maximum_total_source_fanout": max(source_degree.values()),
        "rounds": [
            [{"line": line, "column": col} for line, col in rnd]
            for rnd in SCHEDULE
        ],
        "theorem": "The exact Pass-4504 flag section compiles to 42 primitive XOR routes in 9 conflict-free clocks, and 9 is optimal in the stated bipartite single-port model.",
        "boundary": "Model-level Boolean scheduling only. No synthesis, placement, optical loss, timing closure, decoder threshold, Landauer minimum, or physical optimum is claimed."
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
