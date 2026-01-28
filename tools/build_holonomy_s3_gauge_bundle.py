#!/usr/bin/env python3
"""
Reproduce the S3/Z2 transport corrections for the quotient holonomy field on Q.

Core idea:
  - Each quotient edge carries a transport bijection between 3-element fibers, i.e. an S3 permutation.
  - The induced parity s(p,q) in Z2 acts on Z3 by inversion x -> -x.
  - Triangle holonomy values F(p,q,r) are naturally based at the first vertex; comparing faces of a tetrahedron
    requires transport of the (b,c,d) face to basepoint a, yielding a transported coboundary d_sF.

This script computes:
  - Edge transport permutations and parity cocycle s
  - A vertex 0-cochain t with s = dt (gauge-fix)
  - Transported Bianchi identity: d_sF == 0 on all tetrahedra
  - Gauge-adjusted field F^(t) and an explicit edge potential A with dA = F^(t)

Output:
  - W33_holonomy_s3_gauge_bundle.zip
"""

from __future__ import annotations

import csv
import io
import json
import zipfile
from collections import Counter, deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
MOD3 = 3


def mod3(x: int) -> int:
    return x % MOD3


def _read_csv_from_zip(zip_path: Path, inner_path: str) -> list[dict[str, str]]:
    with zipfile.ZipFile(zip_path) as zf:
        with zf.open(inner_path) as raw:
            text = io.TextIOWrapper(raw, encoding="utf-8")
            return list(csv.DictReader(text))


def _write_csv(
    path: Path, fieldnames: list[str], rows: list[dict[str, object]]
) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def _write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def _parse_dash_list(s: str) -> list[int]:
    return [int(x) for x in s.split("-") if x.strip()]


def _perm_parity_3(perm: tuple[int, int, int]) -> int:
    """
    Parity of a permutation of {0,1,2}:
      0 = even, 1 = odd.
    """
    inv = 0
    for i in range(3):
        for j in range(i + 1, 3):
            if perm[i] > perm[j]:
                inv += 1
    return inv % 2


def _solve_linear_system_mod3(A: np.ndarray, b: np.ndarray) -> tuple[np.ndarray, int]:
    """
    Solve A x = b over Z3 with free variables set to 0.
    Returns (x, rank). Raises ValueError if inconsistent.
    """
    A = (A.astype(np.int16) % MOD3).copy()
    b = (b.astype(np.int16) % MOD3).copy()
    m, n = A.shape
    where = [-1] * n
    row = 0
    for col in range(n):
        pivot = None
        for r in range(row, m):
            if A[r, col] != 0:
                pivot = r
                break
        if pivot is None:
            continue
        if pivot != row:
            A[[row, pivot]] = A[[pivot, row]]
            b[[row, pivot]] = b[[pivot, row]]

        pv = int(A[row, col])
        inv = 1 if pv == 1 else 2
        if inv != 1:
            A[row, :] = (A[row, :] * inv) % MOD3
            b[row] = (b[row] * inv) % MOD3

        where[col] = row

        if row + 1 < m:
            factors = A[row + 1 :, col].copy()
            nz = np.nonzero(factors)[0]
            if nz.size:
                sub = (factors[nz][:, None] * A[row, :][None, :]) % MOD3
                A[row + 1 + nz, :] = (A[row + 1 + nz, :] - sub) % MOD3
                b[row + 1 + nz] = (b[row + 1 + nz] - (factors[nz] * b[row])) % MOD3

        row += 1
        if row == m:
            break

    rank = sum(1 for w in where if w != -1)
    for r in range(rank, m):
        if np.all(A[r, :] == 0) and b[r] != 0:
            raise ValueError("inconsistent linear system over Z3")

    x = np.zeros(n, dtype=np.int16)
    for col in range(n - 1, -1, -1):
        r = where[col]
        if r == -1:
            continue
        s = int((A[r, :] @ x) % MOD3)
        x[col] = (b[r] - s) % MOD3

    if not np.array_equal((A @ x) % MOD3, b % MOD3):
        raise ValueError("solution verification failed")
    return x.astype(np.int8), rank


def main() -> int:
    quotient_bundle = (
        ROOT / "W33_quotient_closure_complement_and_noniso_line_curvature_bundle.zip"
    )
    test_bundle = ROOT / "W33_holonomy_phase_test_bundle.zip"
    h3_basis_bundle = ROOT / "W33_H3_basis_89_Z3_on_clique_complex_bundle.zip"

    for p in [quotient_bundle, test_bundle, h3_basis_bundle]:
        if not p.exists():
            raise FileNotFoundError(str(p))

    out_dir = ROOT / "_holonomy_s3_gauge_tmp"
    out_dir.mkdir(exist_ok=True)

    # --- Load triangles and F values (based at first vertex p<q<r)
    tri_rows = _read_csv_from_zip(
        test_bundle, "triangle_holonomy_vs_symplectic_phase.csv"
    )
    triangles = [(int(r["p"]), int(r["q"]), int(r["r"])) for r in tri_rows]
    F = {tri: mod3(int(r["F"])) for tri, r in zip(triangles, tri_rows, strict=True)}

    # --- Load quotient edges and edge matchings -> transport permutations in S3
    edge_rows = _read_csv_from_zip(
        quotient_bundle, "quotient_graph_edge_decorations_matchings.csv"
    )
    if len(edge_rows) != 540:
        raise ValueError(f"Expected 540 edges, got {len(edge_rows)}")

    edges: list[tuple[int, int]] = []
    edge_index: dict[tuple[int, int], int] = {}
    transport_perm: dict[tuple[int, int], tuple[int, int, int]] = {}
    parity_s: dict[tuple[int, int], int] = {}

    transport_rows_out: list[dict[str, object]] = []
    for r in edge_rows:
        p, q = int(r["p"]), int(r["q"])
        if p > q:
            raise ValueError("expected p<q in edge decorations file")
        tri_p = _parse_dash_list(r["tri_p"])
        tri_q = _parse_dash_list(r["tri_q"])
        if len(tri_p) != 3 or len(tri_q) != 3:
            raise ValueError("bad tri_p/tri_q format")

        pairs_raw = r["missing_matching_pairs"].split(";")
        mapping: dict[int, int] = {}
        for pr in pairs_raw:
            a, b = pr.split("-")
            mapping[int(a)] = int(b)
        if set(mapping.keys()) != set(tri_p):
            raise ValueError("missing matching does not cover tri_p")
        if set(mapping.values()) != set(tri_q):
            raise ValueError("missing matching does not cover tri_q")

        pos_q = {root: i for i, root in enumerate(tri_q)}
        perm = tuple(pos_q[mapping[root]] for root in tri_p)
        if sorted(perm) != [0, 1, 2]:
            raise ValueError("bad permutation computed")

        s = _perm_parity_3(perm)

        edges.append((p, q))
        edge_index[(p, q)] = len(edges) - 1
        transport_perm[(p, q)] = perm
        parity_s[(p, q)] = s

        transport_rows_out.append(
            {
                "p": p,
                "q": q,
                "tri_p": r["tri_p"],
                "tri_q": r["tri_q"],
                "perm_idx_map": f"{perm[0]}-{perm[1]}-{perm[2]}",
                "parity_s": s,
            }
        )

    # adjacency for BFS on vertices 0..39
    adj: list[list[int]] = [[] for _ in range(40)]
    for p, q in edges:
        adj[p].append(q)
        adj[q].append(p)

    def s_edge(u: int, v: int) -> int:
        if u == v:
            return 0
        a, b = (u, v) if u < v else (v, u)
        return parity_s[(a, b)]

    # --- Check ds=0 on all triangles
    ds_counts = Counter()
    for p, q, r in triangles:
        ds = (s_edge(q, r) - s_edge(p, r) + s_edge(p, q)) % 2
        ds_counts[ds] += 1
    if ds_counts.get(1, 0) != 0:
        raise ValueError(
            f"parity cocycle failed: ds nonzero on {ds_counts.get(1,0)} triangles"
        )

    # --- Solve s = dt by BFS (fix t(0)=0)
    t = [-1] * 40
    t[0] = 0
    dq = deque([0])
    while dq:
        u = dq.popleft()
        for v in adj[u]:
            if t[v] != -1:
                continue
            t[v] = (t[u] + s_edge(u, v)) % 2
            dq.append(v)
    if any(x == -1 for x in t):
        raise ValueError("Q graph not connected?")

    # Verify s=dt on all edges
    bad_edges = 0
    for p, q in edges:
        if ((t[q] - t[p]) % 2) != s_edge(p, q):
            bad_edges += 1
    if bad_edges:
        raise ValueError(f"s != dt on {bad_edges} edges")

    # --- Load tetra index map
    tetra_rows = _read_csv_from_zip(h3_basis_bundle, "tetra_index_map_9450.csv")
    if len(tetra_rows) != 9450:
        raise ValueError(f"Expected 9450 tetrahedra, got {len(tetra_rows)}")

    def tri(u: int, v: int, w: int) -> int:
        return F[tuple(sorted((u, v, w)))]

    # --- Compute naive dF and transported d_sF on all tetrahedra
    dF_naive = []
    dF_transport = []
    for row in tetra_rows:
        a, b, c, d = int(row["a"]), int(row["b"]), int(row["c"]), int(row["d"])
        # a<b<c<d
        naive = mod3(tri(b, c, d) - tri(a, c, d) + tri(a, b, d) - tri(a, b, c))
        sign = 1 if s_edge(a, b) == 0 else 2  # (-1)^s in Z3
        transported = mod3(
            sign * tri(b, c, d) - tri(a, c, d) + tri(a, b, d) - tri(a, b, c)
        )
        dF_naive.append(naive)
        dF_transport.append(transported)

    dF_naive_hist = Counter(dF_naive)
    dF_transport_hist = Counter(dF_transport)
    if dF_transport_hist.get(1, 0) != 0 or dF_transport_hist.get(2, 0) != 0:
        raise ValueError("transported Bianchi identity failed: d_sF not identically 0")

    # --- Gauge-adjust F^(t)(p,q,r) = (-1)^{t(p)} F(p,q,r)
    F_t: dict[tuple[int, int, int], int] = {}
    for p, q, r in triangles:
        sign = 1 if t[p] == 0 else 2
        F_t[(p, q, r)] = mod3(sign * F[(p, q, r)])

    # Verify untwisted dF^(t)=0
    dF_t_hist = Counter()
    for row in tetra_rows:
        a, b, c, d = int(row["a"]), int(row["b"]), int(row["c"]), int(row["d"])
        val = mod3(F_t[(b, c, d)] - F_t[(a, c, d)] + F_t[(a, b, d)] - F_t[(a, b, c)])
        dF_t_hist[val] += 1
    if dF_t_hist.get(1, 0) != 0 or dF_t_hist.get(2, 0) != 0:
        raise ValueError("expected dF^(t) == 0 on all tetrahedra")

    # --- Solve for edge potential A with dA = F^(t) on all triangles
    m = len(triangles)
    n = len(edges)
    A_mat = np.zeros((m, n), dtype=np.int8)
    b_vec = np.zeros((m,), dtype=np.int8)

    for i, (p, q, r) in enumerate(triangles):
        b_vec[i] = F_t[(p, q, r)]

        # dA(p,q,r) = A(q,r) - A(p,r) + A(p,q)
        # Variables are on undirected edges (u<v); oriented value flips sign.
        def add_edge(u: int, v: int, coef: int) -> None:
            if u == v:
                return
            a_, b_ = (u, v) if u < v else (v, u)
            col = edge_index[(a_, b_)]
            signed = coef if u < v else -coef
            A_mat[i, col] = mod3(A_mat[i, col] + signed)

        add_edge(q, r, 1)
        add_edge(p, r, -1)
        add_edge(p, q, 1)

    A_sol, rank = _solve_linear_system_mod3(A_mat, b_vec)

    # --- Outputs
    _write_csv(
        out_dir / "edge_transport_permutations_540.csv",
        ["p", "q", "tri_p", "tri_q", "perm_idx_map", "parity_s"],
        transport_rows_out,
    )
    _write_csv(
        out_dir / "vertex_gauge_t_40.csv",
        ["p", "t"],
        [{"p": p, "t": int(t[p])} for p in range(40)],
    )
    _write_csv(
        out_dir / "edge_potential_A_540.csv",
        ["p", "q", "A"],
        [{"p": p, "q": q, "A": int(A_sol[edge_index[(p, q)]])} for (p, q) in edges],
    )
    _write_csv(
        out_dir / "triangle_holonomy_F_3240.csv",
        ["p", "q", "r", "F"],
        [{"p": p, "q": q, "r": r, "F": int(F[(p, q, r)])} for (p, q, r) in triangles],
    )
    _write_csv(
        out_dir / "triangle_holonomy_F_t_3240.csv",
        ["p", "q", "r", "F_t"],
        [
            {"p": p, "q": q, "r": r, "F_t": int(F_t[(p, q, r)])}
            for (p, q, r) in triangles
        ],
    )

    report = {
        "triangle_count": 3240,
        "edge_count": 540,
        "tetra_count": 9450,
        "parity": {
            "s_hist_edges": {
                str(k): int(v) for k, v in sorted(Counter(parity_s.values()).items())
            },
            "ds_hist_triangles": {str(k): int(v) for k, v in sorted(ds_counts.items())},
        },
        "naive_untwisted": {
            "dF_hist_tetrahedra": {
                str(k): int(v) for k, v in sorted(dF_naive_hist.items())
            },
            "dF_nonzero_tetrahedra": int(9450 - dF_naive_hist.get(0, 0)),
        },
        "transported": {
            "d_sF_hist_tetrahedra": {
                str(k): int(v) for k, v in sorted(dF_transport_hist.items())
            },
        },
        "gauge_fix": {
            "t_hist_vertices": {str(k): int(v) for k, v in sorted(Counter(t).items())},
            "dF_t_hist_tetrahedra": {
                str(k): int(v) for k, v in sorted(dF_t_hist.items())
            },
            "edge_potential_rank": rank,
        },
    }
    _write_json(out_dir / "report.json", report)

    readme = """\
W33 holonomy as an S3/Z2 local-coefficient cocycle (gauge bundle)

This bundle derives an S3 transport interpretation of the quotient triangle holonomy field F on Q.

Computed facts:
  - Each quotient edge has a canonical transport bijection between 3-element fibers, giving an S3 permutation.
  - The parity s(p,q)∈Z2 is a 1-cocycle (ds=0) and is exact (s=dt for an explicit vertex function t).
  - The transported coboundary d_sF is identically zero on all 9450 tetrahedra (a discrete Bianchi identity).
  - After the gauge adjustment F^(t)(p,q,r)=(-1)^{t(p)}F(p,q,r), the untwisted coboundary dF^(t) vanishes,
    and there exists an explicit edge potential A with dA = F^(t).

Files:
  - edge_transport_permutations_540.csv
  - vertex_gauge_t_40.csv
  - triangle_holonomy_F_3240.csv
  - triangle_holonomy_F_t_3240.csv
  - edge_potential_A_540.csv
  - report.json
"""
    (out_dir / "README.txt").write_text(readme, encoding="utf-8")

    out_zip = ROOT / "W33_holonomy_s3_gauge_bundle.zip"
    if out_zip.exists():
        out_zip.unlink()
    with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(out_dir.iterdir()):
            zf.write(p, arcname=p.name)

    for p in out_dir.iterdir():
        p.unlink()
    out_dir.rmdir()

    print(f"Wrote {out_zip}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
