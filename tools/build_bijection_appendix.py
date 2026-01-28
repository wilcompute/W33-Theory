#!/usr/bin/env python3
"""Build canonical edge-root bijection table and LaTeX appendix.

Outputs:
- artifacts/edge_root_bijection_canonical.json
- artifacts/edge_root_bijection_canonical.csv
- latex/appendix_bijection.tex
"""

from __future__ import annotations

import csv
import json
from collections import deque
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build_w33():
    F3 = [0, 1, 2]
    vectors = [v for v in product(F3, repeat=4) if any(x != 0 for x in v)]

    proj_points = []
    seen = set()
    for v in vectors:
        v = list(v)
        for i in range(4):
            if v[i] != 0:
                inv = 1 if v[i] == 1 else 2
                v = tuple((x * inv) % 3 for x in v)
                break
        if v not in seen:
            seen.add(v)
            proj_points.append(v)

    def omega(x, y):
        return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3

    edges = []
    for i in range(40):
        for j in range(i + 1, 40):
            if omega(proj_points[i], proj_points[j]) == 0:
                edges.append((i, j))

    return proj_points, edges


def normalize_proj(v):
    v = list(v)
    for i in range(4):
        if v[i] != 0:
            inv = 1 if v[i] == 1 else 2
            return tuple((x * inv) % 3 for x in v)
    return tuple(v)


def check_symplectic(M):
    import numpy as np

    Omega = np.array(
        [[0, 0, 1, 0], [0, 0, 0, 1], [2, 0, 0, 0], [0, 2, 0, 0]], dtype=int
    )
    M = np.array(M, dtype=int) % 3
    return np.all(((M.T @ Omega @ M) % 3) == Omega)


def apply_matrix(M, v):
    import numpy as np

    M = np.array(M, dtype=int) % 3
    v = np.array(v, dtype=int) % 3
    result = (M @ v) % 3
    return normalize_proj(result.tolist())


def generator_matrices():
    return [
        [[1, 0, 1, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
        [[1, 0, 0, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]],
        [[1, 0, 0, 0], [0, 1, 0, 0], [1, 0, 1, 0], [0, 0, 0, 1]],
        [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 1, 0, 1]],
        [[1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 2, 1]],
        [[1, 0, 0, 0], [1, 1, 0, 0], [0, 0, 1, 2], [0, 0, 0, 1]],
        [[0, 0, 1, 0], [0, 1, 0, 0], [2, 0, 0, 0], [0, 0, 0, 1]],
        [[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 2, 0, 0]],
        [[2, 0, 0, 0], [0, 1, 0, 0], [0, 0, 2, 0], [0, 0, 0, 1]],
        [[1, 0, 0, 0], [0, 2, 0, 0], [0, 0, 1, 0], [0, 0, 0, 2]],
    ]


def bfs_edge_words(edges, vertices, edge_to_idx):
    # Build edge permutations for generators
    perms = []
    for M in generator_matrices():
        if not check_symplectic(M):
            continue
        v_to_idx = {tuple(v): i for i, v in enumerate(vertices)}
        vperm = [None] * 40
        for i, v in enumerate(vertices):
            vperm[i] = v_to_idx[apply_matrix(M, v)]

        eperm = [None] * len(edges)
        for i, e in enumerate(edges):
            a, b = e
            na, nb = vperm[a], vperm[b]
            eperm[i] = edge_to_idx[tuple(sorted((na, nb)))]
        perms.append(eperm)

    # BFS from edge 0
    labels = {0: (0, ())}
    q = deque([0])
    while q:
        cur = q.popleft()
        dist, word = labels[cur]
        for gi, perm in enumerate(perms):
            nxt = perm[cur]
            if nxt not in labels:
                labels[nxt] = (dist + 1, word + (gi,))
                q.append(nxt)
    return labels


def main():
    vertices, edges = build_w33()
    edge_to_idx = {tuple(sorted(e)): i for i, e in enumerate(edges)}

    # Canonical word labels
    labels = bfs_edge_words(edges, vertices, edge_to_idx)

    # load mapping
    edge_map = json.loads(
        (ROOT / "artifacts" / "explicit_bijection_decomposition.json").read_text()
    )
    edge_to_root_idx = {int(k): v for k, v in edge_map["edge_to_root_index"].items()}
    root_coords = [tuple(r) for r in edge_map["root_coords"]]

    we6 = json.loads((ROOT / "artifacts" / "we6_orbit_labels.json").read_text())
    root_to_orbit = {eval(k): v for k, v in we6["mapping"].items()}

    rows = []
    for eidx, (i, j) in enumerate(edges):
        ridx = edge_to_root_idx.get(eidx)
        if ridx is None:
            continue
        r = root_coords[ridx]
        info = root_to_orbit.get(tuple(r), {})
        dist, word = labels.get(eidx, (None, None))
        rows.append(
            {
                "order_key": (dist, word),
                "edge_index": eidx,
                "word_len": dist,
                "word": word,
                "v_i": i,
                "v_j": j,
                "root_index": ridx,
                "root_coords": r,
                "we6_orbit_id": info.get("orbit_id"),
                "we6_orbit_size": info.get("orbit_size"),
            }
        )

    rows.sort(key=lambda r: (r["order_key"][0], r["order_key"][1]))

    # Write JSON/CSV
    out_json = ROOT / "artifacts" / "edge_root_bijection_canonical.json"
    out_csv = ROOT / "artifacts" / "edge_root_bijection_canonical.csv"

    out_json.write_text(
        json.dumps(
            [{k: v for k, v in r.items() if k != "order_key"} for r in rows], indent=2
        ),
        encoding="utf-8",
    )

    with out_csv.open("w", newline="", encoding="utf-8") as f:
        fieldnames = [k for k in rows[0].keys() if k != "order_key"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            r2 = {k: v for k, v in r.items() if k != "order_key"}
            writer.writerow(r2)

    # Build LaTeX longtable
    latex_path = ROOT / "latex" / "appendix_bijection.tex"
    with latex_path.open("w", encoding="utf-8") as f:
        f.write("\\begin{footnotesize}\n")
        f.write("\\begin{longtable}{r r r r l r r}\n")
        f.write("\\toprule\n")
        f.write(
            r"Ord & Edge & $v_i$ & $v_j$ & Root $(r_1,\ldots,r_8)$ & Orbit & Size \\\\ "
            + "\n"
        )
        f.write("\\midrule\n")
        f.write("\\endfirsthead\n")
        f.write("\\toprule\n")
        f.write(
            r"Ord & Edge & $v_i$ & $v_j$ & Root $(r_1,\ldots,r_8)$ & Orbit & Size \\\\ "
            + "\n"
        )
        f.write("\\midrule\n")
        f.write("\\endhead\n")

        for order, r in enumerate(rows, start=1):
            root_str = "(" + ",".join(str(x) for x in r["root_coords"]) + ")"
            f.write(
                f"{order} & {r['edge_index']} & {r['v_i']} & {r['v_j']} & {root_str} & {r.get('we6_orbit_id','')} & {r.get('we6_orbit_size','')} \\\\ \n"
            )

        f.write("\\bottomrule\n")
        f.write("\\end{longtable}\n")
        f.write("\\end{footnotesize}\n")

    print(f"Wrote {out_json}")
    print(f"Wrote {out_csv}")
    print(f"Wrote {latex_path}")


if __name__ == "__main__":
    main()
