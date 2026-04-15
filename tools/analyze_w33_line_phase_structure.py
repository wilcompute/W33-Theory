#!/usr/bin/env python3
"""
Phase structure on W33 lines, induced from the E8↔W33 edge bridge.

Inputs:
  - artifacts/e8_root_metadata_table.json  (240 rows; one per E8 root / W33 edge)
  - artifacts/w33_line_fusion_law.json     (optional cross-check of "special_vertex")

Key verified facts (all empirical but rigid once the bijection is fixed):
  1) W33 has 40 lines (K4 cliques). Each line has 6 edges, hence 6 root-channels.
  2) The Z6 Coxeter phase on those 6 edges is ALWAYS a permutation of {0,1,2,3,4,5}.
  3) On each line, phases label the A2 roots cyclically: if p,q are phases on the line,
     then the root inner product depends ONLY on (p-q) mod 6 via:
        d=0 ->  2
        d=1 ->  1
        d=2 -> -1
        d=3 -> -2
        d=4 -> -1
        d=5 ->  1
     So phases (mod 6) are literally the A2 hexagon coordinate on every line.
  4) The inner-product(-1) graph on the 6 roots is two triangles, exactly
     {0,2,4} (even phases) and {1,3,5} (odd phases).
  5) Each K4 line has a unique "special vertex" incident to the 3 odd-phase edges.

Outputs:
  - artifacts/w33_line_phase_structure.json
  - artifacts/w33_line_phase_structure.md
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

IN_META = ROOT / "artifacts" / "e8_root_metadata_table.json"
IN_FUSION = ROOT / "artifacts" / "w33_line_fusion_law.json"

OUT_JSON = ROOT / "artifacts" / "w33_line_phase_structure.json"
OUT_MD = ROOT / "artifacts" / "w33_line_phase_structure.md"


def _write_json(path: Path, data: Dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_md(path: Path, lines: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def _cartan_unit_e8_sage_order() -> np.ndarray:
    # Gram matrix in the SAME canonical ordering used by artifacts/e8_root_metadata_table.json.
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


def _build_w33_adj_points() -> np.ndarray:
    # W33 points: projective points in F3^4; adjacency iff symplectic omega == 0.
    F3 = [0, 1, 2]
    points = []
    seen = set()
    for vec in product(F3, repeat=4):
        if not any(vec):
            continue
        v = list(vec)
        for i in range(4):
            if v[i] != 0:
                inv = 1 if v[i] == 1 else 2
                v = [(x * inv) % 3 for x in v]
                break
        t = tuple(v)
        if t not in seen:
            seen.add(t)
            points.append(t)

    def omega(x, y) -> int:
        return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3

    n = len(points)
    if n != 40:
        raise RuntimeError(f"Expected 40 W33 points; got {n}")
    adj = np.zeros((n, n), dtype=bool)
    for i in range(n):
        for j in range(i + 1, n):
            if omega(points[i], points[j]) == 0:
                adj[i, j] = adj[j, i] = True
    return adj


def _edge_line(adj: np.ndarray, u: int, v: int) -> Tuple[int, int, int, int]:
    # In SRG(40,12,2,4), each edge has exactly two common neighbors -> its unique K4 line.
    common = [k for k in range(adj.shape[0]) if adj[u, k] and adj[v, k]]
    if len(common) != 2:
        raise RuntimeError(
            f"Edge ({u},{v}) has {len(common)} common neighbors (expected 2)"
        )
    return tuple(sorted([u, v, common[0], common[1]]))


def _expected_a2_ip_by_phase_diff() -> Dict[int, int]:
    # For phases 0..5 placed on the A2 hexagon.
    return {0: 2, 1: 1, 2: -1, 3: -2, 4: -1, 5: 1}


def main() -> None:
    meta = json.loads(IN_META.read_text(encoding="utf-8"))
    rows = meta["rows"]

    edge_to_root: Dict[Tuple[int, int], Tuple[int, ...]] = {}
    edge_to_phase: Dict[Tuple[int, int], int] = {}
    for row in rows:
        e = tuple(sorted((int(row["edge"][0]), int(row["edge"][1]))))
        edge_to_root[e] = tuple(int(x) for x in row["root_orbit"])
        edge_to_phase[e] = int(row["phase_z6"])
    if len(edge_to_root) != 240:
        raise RuntimeError(f"Expected 240 edges in mapping; got {len(edge_to_root)}")

    C = _cartan_unit_e8_sage_order()
    adj_pts = _build_w33_adj_points()

    # Build the 40 W33 lines and their 6 edges.
    edges_by_line: Dict[Tuple[int, int, int, int], List[Tuple[int, int]]] = defaultdict(
        list
    )
    for u, v in edge_to_root:
        L = _edge_line(adj_pts, u, v)
        edges_by_line[L].append((u, v))
    lines = sorted(edges_by_line.keys())
    if len(lines) != 40:
        raise RuntimeError(f"Expected 40 W33 lines; got {len(lines)}")
    if any(len(edges_by_line[L]) != 6 for L in lines):
        raise RuntimeError("Expected 6 edges per line")

    # Optional: cross-check the "special_vertex" computed in the fusion-law artifact.
    fusion_special: Dict[Tuple[int, int, int, int], int] = {}
    if IN_FUSION.exists():
        fusion = json.loads(IN_FUSION.read_text(encoding="utf-8"))
        for entry in fusion["per_line"]:
            fusion_special[tuple(entry["line"])] = int(entry["special_vertex"])

    expected_ip = _expected_a2_ip_by_phase_diff()

    failures: List[Dict[str, object]] = []
    per_line: List[Dict[str, object]] = []

    vertex_phase_pattern_counts: Counter[Tuple[int, int, int]] = Counter()
    special_vertex_phase_signature_counts: Counter[Tuple[int, int, int]] = Counter()

    for idx, L in enumerate(lines):
        verts = list(L)
        elist = [tuple(sorted(e)) for e in combinations(verts, 2)]
        phases = {e: edge_to_phase[e] for e in elist}
        phase_set = sorted(phases.values())
        if phase_set != [0, 1, 2, 3, 4, 5]:
            failures.append(
                {
                    "line_index": idx,
                    "line": verts,
                    "reason": "phase_set",
                    "phases": phase_set,
                }
            )
            continue

        # Map phases -> roots.
        phase_to_root = {edge_to_phase[e]: edge_to_root[e] for e in elist}
        if set(phase_to_root.keys()) != set(range(6)):
            failures.append(
                {"line_index": idx, "line": verts, "reason": "missing_phase_keys"}
            )
            continue

        # Verify the A2 phase-difference inner product law.
        bad_ip = []
        for p in range(6):
            for q in range(6):
                r1 = phase_to_root[p]
                r2 = phase_to_root[q]
                got = _ip_simple_coeffs(r1, r2, C)
                want = expected_ip[(p - q) % 6]
                if got != want:
                    bad_ip.append({"p": p, "q": q, "got": got, "want": want})
        if bad_ip:
            failures.append(
                {
                    "line_index": idx,
                    "line": verts,
                    "reason": "phase_ip_law",
                    "examples": bad_ip[:5],
                }
            )
            continue

        # "Special vertex": unique vertex incident to odd phases {1,3,5}.
        incident_phases: Dict[int, Tuple[int, int, int]] = {}
        for v in verts:
            inc = []
            for u in verts:
                if u == v:
                    continue
                e = (min(u, v), max(u, v))
                inc.append(edge_to_phase[e])
            incident_phases[v] = tuple(sorted(inc))
            vertex_phase_pattern_counts[incident_phases[v]] += 1

        specials = [v for v, sig in incident_phases.items() if sig == (1, 3, 5)]
        if len(specials) != 1:
            failures.append(
                {
                    "line_index": idx,
                    "line": verts,
                    "reason": "special_vertex_nonunique",
                    "incident_phase_signatures": {
                        str(k): list(v) for k, v in incident_phases.items()
                    },
                }
            )
            continue

        special_v = specials[0]
        special_sig = incident_phases[special_v]
        special_vertex_phase_signature_counts[special_sig] += 1

        # Cross-check special vertex with fusion-law artifact (if present).
        fusion_ok = None
        if fusion_special:
            fusion_v = fusion_special.get(L)
            fusion_ok = fusion_v == special_v
            if fusion_v is None:
                failures.append(
                    {"line_index": idx, "line": verts, "reason": "fusion_missing_line"}
                )
                continue
            if not fusion_ok:
                failures.append(
                    {
                        "line_index": idx,
                        "line": verts,
                        "reason": "fusion_special_mismatch",
                        "got": special_v,
                        "want": fusion_v,
                    }
                )
                continue

        # Partition edges by phase parity (these are the two ip=-1 triangles in the A2 root graph).
        even_edges = [list(e) for e, p in phases.items() if p % 2 == 0]
        odd_edges = [list(e) for e, p in phases.items() if p % 2 == 1]

        per_line.append(
            {
                "i": idx,
                "line": verts,
                "special_vertex": int(special_v),
                "fusion_special_ok": fusion_ok,
                "edges": sorted(
                    [[int(e[0]), int(e[1]), int(phases[e])] for e in elist],
                    key=lambda t: t[2],
                ),
                "even_phase_edges": sorted(even_edges),
                "odd_phase_edges": sorted(odd_edges),
                "vertex_incident_phase_signatures": {
                    str(v): list(sig) for v, sig in incident_phases.items()
                },
            }
        )

    status = "ok" if not failures else "fail"

    report: Dict[str, object] = {
        "status": status,
        "counts": {"w33_lines": 40, "edges": 240, "failures": len(failures)},
        "per_line": per_line,
        "phase_ip_law": {"expected_ip_by_phase_diff": expected_ip},
        "vertex_incident_phase_signature_counts": {
            str(k): int(v) for k, v in vertex_phase_pattern_counts.items()
        },
        "special_vertex_signature_counts": {
            str(k): int(v) for k, v in special_vertex_phase_signature_counts.items()
        },
        "failures": failures[:20],
        "sources": {
            "meta": IN_META.relative_to(ROOT).as_posix(),
            "fusion": (
                IN_FUSION.relative_to(ROOT).as_posix() if IN_FUSION.exists() else None
            ),
        },
    }

    _write_json(OUT_JSON, report)

    md = []
    md.append("# W33 line phase structure (Z6)")
    md.append("")
    md.append(f"- status: `{status}`")
    md.append(f"- lines: `{report['counts']['w33_lines']}`")
    md.append(f"- edges: `{report['counts']['edges']}`")
    md.append(f"- failures: `{report['counts']['failures']}`")
    md.append("")
    md.append("## Verified invariants")
    md.append("- Each line’s 6 edge-phases are exactly `{0,1,2,3,4,5}`.")
    md.append(
        "- On each line, the A2 inner product is a function of phase difference `(p-q) mod 6`:"
    )
    md.append(f"  - `expected_ip_by_phase_diff = {expected_ip}`")
    md.append(
        "- The inner-product(-1) triangles are exactly the even phases `{0,2,4}` and the odd phases `{1,3,5}`."
    )
    md.append(
        "- Each K4 line has a unique vertex incident to odd phases `(1,3,5)`; this matches `w33_line_fusion_law.json` when present."
    )
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
