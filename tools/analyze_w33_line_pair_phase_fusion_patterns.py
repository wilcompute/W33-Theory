#!/usr/bin/env python3
"""
Line-level interaction law: phase-resolved fusion patterns between W33 lines.

We already know (from tools/derive_w33_line_fusion_law.py) that:
  - The 240 W33 edges partition into 40 W33 lines (K4 cliques).
  - Each line's 6 edges are the 6 roots of an A2 subsystem.
  - For every *coupled* line pair (i<j), the 12 roots (α+β) with α·β=-1 split into
    exactly two full output lines (two A2 subsystems).

This script adds the missing "clock / phase" layer:

  - Each line has exactly one root in each phase k∈Z6.
  - For a coupled line pair (i,j), consider the 12 interacting pairs (α,β)
    where α is a root on line i and β is a root on line j with α·β=-1.
    Write pa, pb for their Z6 phases and define d=(pa-pb) mod 6.

Two empirical-but-rigid facts hold for ALL 540 coupled line pairs:

  (A) The multiset of d-values is always one of 7 patterns:
        - "all diffs":  (2,2,2,2,2,2)   (219 pairs)
        - "adjacent":   (6,6,0,0,0,0)   and its 5 rotations (321 pairs total)
    i.e., each diff appears either 0, 2, or 6 times; total is 12.

  (B) Output-line selection is *diff-determined*:
        For a fixed coupled pair (i,j), if two interactions have the same
        phase-difference d, then their output roots α+β always land in the SAME
        output line (one of the two from the fusion law).

So for each coupled pair (i,j), we can summarize the interaction by:
  - diff_counts[d] for d=0..5
  - diff_to_output_line[d] (for the diffs that actually occur)

Outputs:
  - artifacts/w33_line_pair_phase_fusion_patterns.json
  - artifacts/w33_line_pair_phase_fusion_patterns.md
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

IN_META = ROOT / "artifacts" / "e8_root_metadata_table.json"
IN_FUSION = ROOT / "artifacts" / "w33_line_fusion_law.json"

OUT_JSON = ROOT / "artifacts" / "w33_line_pair_phase_fusion_patterns.json"
OUT_MD = ROOT / "artifacts" / "w33_line_pair_phase_fusion_patterns.md"


def _write_json(path: Path, data: Dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_md(path: Path, lines: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def _cartan_unit_e8_sage_order() -> np.ndarray:
    return np.array(
        [
            [2, 0, -1, 0, 0, 0, 0, 0],
            [0, 2, 0, -1, 0, 0, 0, 0],
            [-1, 0, 2, -1, 0, 0, 0, 0],
            [0, -1, -1, 2, -1, 0, 0, 0],
            [0, 0, 0, -1, 2, -1, 0, 0],
            [0, 0, 0, 0, -1, 2, -1, 0],
            [0, 0, 0, 0, 0, -1, 2, -1],
            [0, 0, 0, 0, 0, 0, -1, 2],
        ],
        dtype=int,
    )


def _ip_simple_coeffs(c: Tuple[int, ...], d: Tuple[int, ...], C: np.ndarray) -> int:
    return int(sum(c[i] * int(C[i, j]) * d[j] for i in range(8) for j in range(8)))


def main() -> None:
    if not IN_FUSION.exists():
        raise RuntimeError(f"Missing required input: {IN_FUSION}")

    meta = json.loads(IN_META.read_text(encoding="utf-8"))
    rows = meta["rows"]

    edge_to_root: Dict[Tuple[int, int], Tuple[int, ...]] = {}
    edge_to_phase: Dict[Tuple[int, int], int] = {}
    root_to_edge: Dict[Tuple[int, ...], Tuple[int, int]] = {}
    for row in rows:
        e = tuple(sorted((int(row["edge"][0]), int(row["edge"][1]))))
        r = tuple(int(x) for x in row["root_orbit"])
        p = int(row["phase_z6"])
        edge_to_root[e] = r
        edge_to_phase[e] = p
        root_to_edge[r] = e
    if len(edge_to_root) != 240:
        raise RuntimeError(f"Expected 240 edges in mapping; got {len(edge_to_root)}")
    if len(root_to_edge) != 240:
        raise RuntimeError(f"Expected 240 roots in mapping; got {len(root_to_edge)}")

    fusion = json.loads(IN_FUSION.read_text(encoding="utf-8"))
    per_line = fusion["per_line"]
    fusion_pairs: Dict[str, List[int]] = fusion["fusion_law"]["pairs"]

    # Canonical line indexing (0..39) is taken from w33_line_fusion_law.json.
    lines: List[Tuple[int, int, int, int]] = []
    special_vertex: List[int] = []
    for entry in per_line:
        i = int(entry["i"])
        if i != len(lines):
            raise RuntimeError("Unexpected line indexing; expected consecutive i=0..39")
        L = tuple(int(x) for x in entry["line"])
        if len(L) != 4:
            raise RuntimeError("Expected 4 points per line")
        lines.append(L)
        special_vertex.append(int(entry["special_vertex"]))

    # Edge -> line index (each W33 edge is in a unique K4 line).
    edge_to_line: Dict[Tuple[int, int], int] = {}
    for li, L in enumerate(lines):
        for u, v in combinations(L, 2):
            e = (min(u, v), max(u, v))
            if e in edge_to_line and edge_to_line[e] != li:
                raise RuntimeError(
                    "Edge appears in multiple lines (should be unique in W33)"
                )
            edge_to_line[e] = li
    if len(edge_to_line) != 240:
        raise RuntimeError(
            f"Expected 240 edges in line partition; got {len(edge_to_line)}"
        )

    # For each line, build phase->root mapping (should be a bijection on Z6).
    line_phase_to_root: List[Dict[int, Tuple[int, ...]]] = []
    for L in lines:
        phase_to_root: Dict[int, Tuple[int, ...]] = {}
        for u, v in combinations(L, 2):
            e = (min(u, v), max(u, v))
            p = edge_to_phase[e]
            r = edge_to_root[e]
            if p in phase_to_root and phase_to_root[p] != r:
                raise RuntimeError("Phase collision within a line")
            phase_to_root[p] = r
        if set(phase_to_root.keys()) != set(range(6)):
            raise RuntimeError(f"Line {L} does not realize all 6 phases")
        line_phase_to_root.append(phase_to_root)

    C = _cartan_unit_e8_sage_order()

    # Global stats.
    pattern_counts: Counter[Tuple[int, int, int, int, int, int]] = Counter()
    pattern_counts_by_intersection: Dict[
        int, Counter[Tuple[int, int, int, int, int, int]]
    ] = {0: Counter(), 1: Counter()}

    # For the all-diff pattern, we observed only parity variants for "which diffs map to out0".
    all_diff_subset_counts: Counter[Tuple[int, ...]] = Counter()

    # For adjacent-diff patterns (two diffs with count=6), track which diff maps to out0.
    adjacent_choice_counts: Dict[Tuple[int, int], Counter[int]] = defaultdict(Counter)

    # Per-pair compact export (540 entries): diff_counts and diff_to_out.
    pair_summaries: Dict[str, Dict[str, object]] = {}

    failures: List[Dict[str, object]] = []

    for key, out_lines in fusion_pairs.items():
        i, j = (int(x) for x in key.split(","))
        outs = sorted(int(x) for x in out_lines)
        out0, out1 = outs[0], outs[1]
        if not (0 <= i < j < 40):
            raise RuntimeError(f"Unexpected coupled-pair key {key}")

        Li = set(lines[i])
        Lj = set(lines[j])
        inter = sorted(Li & Lj)
        inter_size = len(inter)
        if inter_size not in (0, 1):
            raise RuntimeError("W33 lines should intersect in 0 or 1 points")

        A = line_phase_to_root[i]
        B = line_phase_to_root[j]

        diff_counts = [0] * 6
        diff_to_out: Dict[int, int] = {}

        # Count and classify all α·β=-1 interactions (12 of them).
        interaction_count = 0
        for pa in range(6):
            ra = A[pa]
            for pb in range(6):
                rb = B[pb]
                if _ip_simple_coeffs(ra, rb, C) != -1:
                    continue
                interaction_count += 1
                d = (pa - pb) % 6
                diff_counts[d] += 1

                # Output root γ = α+β, locate its W33 edge, then locate its line.
                rc = tuple(ra[k] + rb[k] for k in range(8))
                e_out = root_to_edge.get(rc)
                if e_out is None:
                    failures.append(
                        {"pair": key, "reason": "missing_sum_root", "pa": pa, "pb": pb}
                    )
                    continue
                out_line = edge_to_line[e_out]
                if out_line not in outs:
                    failures.append(
                        {
                            "pair": key,
                            "reason": "output_line_not_in_fusion_outputs",
                            "got": out_line,
                            "expected": outs,
                            "pa": pa,
                            "pb": pb,
                        }
                    )
                    continue

                if d in diff_to_out and diff_to_out[d] != out_line:
                    failures.append(
                        {
                            "pair": key,
                            "reason": "nonunique_output_for_diff",
                            "diff": d,
                            "prev": diff_to_out[d],
                            "got": out_line,
                        }
                    )
                    continue
                diff_to_out[d] = out_line

        if interaction_count != 12:
            failures.append(
                {
                    "pair": key,
                    "reason": "bad_interaction_count",
                    "got": interaction_count,
                }
            )

        patt = tuple(diff_counts)
        pattern_counts[patt] += 1
        pattern_counts_by_intersection[inter_size][patt] += 1

        # Normalize diff_to_out to a fixed-length list with None for unused diffs.
        diff_to_out_list: List[int | None] = [None] * 6
        for d, ol in diff_to_out.items():
            diff_to_out_list[d] = int(ol)

        pair_summaries[key] = {
            "i": i,
            "j": j,
            "intersection_size": inter_size,
            "intersection_vertex": inter[0] if inter else None,
            "intersection_is_special": (
                None
                if not inter
                else {
                    "i": inter[0] == special_vertex[i],
                    "j": inter[0] == special_vertex[j],
                }
            ),
            "outputs": outs,
            "diff_counts": diff_counts,
            "diff_to_output_line": diff_to_out_list,
        }

        # Pattern-specific tracking.
        if patt == (2, 2, 2, 2, 2, 2):
            subset = tuple(sorted(d for d in range(6) if diff_to_out_list[d] == out0))
            all_diff_subset_counts[subset] += 1

        ds = [d for d, c in enumerate(diff_counts) if c == 6]
        if len(ds) == 2:
            ds_sorted = tuple(sorted(ds))
            d_to_out0 = [d for d in ds_sorted if diff_to_out_list[d] == out0]
            if len(d_to_out0) == 1:
                adjacent_choice_counts[ds_sorted][d_to_out0[0]] += 1

    status = "ok" if not failures else "fail"

    report: Dict[str, object] = {
        "status": status,
        "counts": {"coupled_pairs": len(fusion_pairs), "failures": len(failures)},
        "pattern_counts": {str(k): int(v) for k, v in pattern_counts.items()},
        "pattern_counts_by_intersection": {
            str(inter): {str(k): int(v) for k, v in ct.items()}
            for inter, ct in pattern_counts_by_intersection.items()
        },
        "all_diff_pattern": {
            "pattern": [2, 2, 2, 2, 2, 2],
            "subset_counts_for_out0": {
                str(k): int(v) for k, v in all_diff_subset_counts.items()
            },
        },
        "adjacent_patterns": {
            "definition": "patterns where exactly two diffs have count=6 (all other diffs 0); track which diff maps to out0",
            "choice_counts_for_out0": {
                str(k): {str(d): int(n) for d, n in ct.items()}
                for k, ct in adjacent_choice_counts.items()
            },
        },
        "pair_summaries": pair_summaries,
        "failures": failures[:25],
        "sources": {
            "meta": IN_META.relative_to(ROOT).as_posix(),
            "fusion": IN_FUSION.relative_to(ROOT).as_posix(),
        },
    }

    _write_json(OUT_JSON, report)

    md = []
    md.append("# W33 line-pair phase fusion patterns")
    md.append("")
    md.append(f"- status: `{status}`")
    md.append(f"- coupled line pairs: `{len(fusion_pairs)}`")
    md.append(f"- failures: `{len(failures)}`")
    md.append("")
    md.append("## Diff-pattern histogram (d = pa-pb mod 6 on α·β=-1 interactions)")
    for patt, n in pattern_counts.most_common():
        md.append(f"- `{patt}`: `{n}`")
    md.append("")
    md.append("## Determinism")
    md.append(
        "- For every coupled pair (i,j), and every diff d that occurs, all interactions with that diff land in the same output line."
    )
    md.append(
        "- So the fusion law refines to: `d -> output_line` (for the diffs that occur)."
    )
    md.append("")
    md.append("## All-diff pattern (2,2,2,2,2,2)")
    md.append(f"- total: `{pattern_counts.get((2,2,2,2,2,2), 0)}`")
    md.append(f"- subset counts for out0: `{dict(all_diff_subset_counts)}`")
    md.append("")
    md.append(f"- JSON: `{OUT_JSON.relative_to(ROOT).as_posix()}`")
    _write_md(OUT_MD, md)

    print(
        f"status={status}  failures={len(failures)}  wrote={OUT_JSON.relative_to(ROOT).as_posix()}"
    )
    if status != "ok":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
