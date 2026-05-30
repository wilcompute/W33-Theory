#!/usr/bin/env python3
"""Anchor spread-sector fiber labels.

This verifies the next bridge after the symplectic projection-fiber theorem.

Existing spread audit facts:
  - W(3,3) has 36 symplectic spreads.
  - Fix an anchor p.  The four isotropic lines through p split the 36 spreads
    into four sectors of size 9.
  - A spread in a sector consists of the chosen anchor line plus 9 affine lines,
    one in each of the 9 directions of p^perp not on that anchor line.

New check:
  For every anchor-line sector and every allowed affine direction d, the map

      spread -> the affine line in direction d contained in that spread

  is a bijection from the 9 spreads in the sector to the 9 parallel affine lines
  of that direction in the 27-point affine bulk.

Thus the nine spreads in a fixed sector are canonically coordinatized by the
9 labels of an affine F3^2 quotient AG(3,3)/d.  This is the same abstract
9-label set as the PG(5,3)->W33 projection fiber.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
for candidate in (ROOT, ROOT / "scripts"):
    s = str(candidate)
    if s not in sys.path:
        sys.path.insert(0, s)

from scripts.w33_projective_affine_shell_audit import (  # noqa: E402
    isotropic_lines,
    point_perp,
    projective_lines,
    projective_points,
)
from scripts.w33_symplectic_spread_frame_audit import symplectic_spreads  # noqa: E402


def line_key(line: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sorted(line))


def analyze_anchor(anchor_index: int = 0) -> dict[str, Any]:
    points = projective_points()
    lines = isotropic_lines(points, projective_lines(points))
    spreads = symplectic_spreads(lines, n_points=len(points))
    hyperplane = point_perp(anchor_index, points)
    affine_points = set(range(len(points))) - set(hyperplane)
    anchor_line_indices = [i for i, line in enumerate(lines) if anchor_index in line]

    sector_records = []
    all_sector_ok = []
    for anchor_line_index in anchor_line_indices:
        anchor_line = set(lines[anchor_line_index])
        directions = sorted(set(hyperplane) - anchor_line)
        sector = [spread for spread in spreads if anchor_line_index in spread]
        direction_records = []
        sector_ok_parts = [len(sector) == 9, len(directions) == 9]

        for direction in directions:
            # All affine lines of this direction in the full W33 line set.
            parallel_lines = [
                i for i, line in enumerate(lines)
                if direction in line
                and len(set(line) & affine_points) == 3
                and len(set(line) & set(hyperplane)) == 1
            ]
            chosen_by_spread = []
            for spread in sector:
                chosen = [i for i in spread if i in parallel_lines]
                chosen_by_spread.append(tuple(chosen))
            chosen_flat = [x[0] for x in chosen_by_spread if len(x) == 1]
            chosen_line_sets = [set(lines[i]) & affine_points for i in chosen_flat]
            affine_cover = set().union(*chosen_line_sets) if chosen_line_sets else set()
            record = {
                "direction": direction,
                "parallel_line_count": len(parallel_lines),
                "sector_spread_count": len(sector),
                "unique_chosen_lines": len(set(chosen_flat)),
                "each_spread_chooses_one": all(len(x) == 1 for x in chosen_by_spread),
                "chosen_lines_cover_affine_bulk": len(affine_cover) == 27,
                "chosen_lines_disjoint": sum(len(x) for x in chosen_line_sets) == len(affine_cover) == 27,
                "bijection": len(set(chosen_flat)) == len(sector) == len(parallel_lines) == 9,
            }
            record["ok"] = all(
                record[key]
                for key in ("each_spread_chooses_one", "chosen_lines_cover_affine_bulk", "chosen_lines_disjoint", "bijection")
            )
            direction_records.append(record)
            sector_ok_parts.append(record["ok"])

        sector_records.append(
            {
                "anchor_line_index": anchor_line_index,
                "anchor_line": line_key(lines[anchor_line_index]),
                "sector_size": len(sector),
                "direction_count": len(directions),
                "direction_records": direction_records,
                "all_directions_ok": all(r["ok"] for r in direction_records),
            }
        )
        all_sector_ok.append(all(sector_ok_parts))

    return {
        "anchor_index": anchor_index,
        "point_count": len(points),
        "line_count": len(lines),
        "spread_count": len(spreads),
        "hyperplane_size": len(hyperplane),
        "affine_size": len(affine_points),
        "anchor_line_count": len(anchor_line_indices),
        "sector_records": sector_records,
        "sector_size_distribution": dict(Counter(r["sector_size"] for r in sector_records)),
        "direction_count_distribution": dict(Counter(r["direction_count"] for r in sector_records)),
        "all_sector_bijections_hold": all(all_sector_ok),
    }


def build_payload() -> dict[str, Any]:
    canonical = analyze_anchor(0)
    identities = {
        "base_counts": canonical["point_count"] == 40 and canonical["line_count"] == 40 and canonical["spread_count"] == 36,
        "local_shell_13_27": canonical["hyperplane_size"] == 13 and canonical["affine_size"] == 27,
        "four_anchor_line_sectors": canonical["anchor_line_count"] == 4,
        "sector_sizes_are_9": canonical["sector_size_distribution"] == {9: 4},
        "direction_counts_are_9": canonical["direction_count_distribution"] == {9: 4},
        "every_sector_direction_gives_9_label_bijection": canonical["all_sector_bijections_hold"],
    }
    return {
        "theorem": "anchor_spread_sector_fiber_labels",
        "canonical_anchor_analysis": canonical,
        "interpretation": {
            "sector": "choose one of four anchor lines through p",
            "fiber_label": "within that sector, choose one of nine parallel affine lines in any fixed allowed direction",
            "bridge": "the nine spreads in a sector are the nine labels of AG(3,3)/direction, an affine F3^2 quotient matching the 9-point projection fiber",
            "count": "36 = 4 anchor-line sectors * 9 affine fiber labels",
        },
        "identities": identities,
        "all_identities_hold": all(identities.values()),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_anchor_spread_sector_fiber_labels.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
