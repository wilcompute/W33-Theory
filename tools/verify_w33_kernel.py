#!/usr/bin/env python3
"""
Verify the core mathematical claims in `W33_TOE_KERNEL_SECTIONS_3_7.tex`
using the provided artifact bundles (zip files in the workspace root).

This is intentionally dependency-light: stdlib + numpy.
"""

from __future__ import annotations

import csv
import io
import json
import sys
import zipfile
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def _read_csv_from_zip(zip_path: Path, inner_path: str) -> list[dict[str, str]]:
    with zipfile.ZipFile(zip_path) as zf:
        with zf.open(inner_path) as raw:
            text = io.TextIOWrapper(raw, encoding="utf-8")
            return list(csv.DictReader(text))


def _read_json_from_zip(zip_path: Path, inner_path: str) -> object:
    with zipfile.ZipFile(zip_path) as zf:
        with zf.open(inner_path) as raw:
            return json.load(raw)


def _parse_int_list(space_separated: str) -> list[int]:
    value = space_separated.strip()
    if not value:
        return []
    return [int(x) for x in value.split()]


def _build_undirected_adjacency(n: int, edges: list[tuple[int, int]]) -> np.ndarray:
    adj = np.zeros((n, n), dtype=np.uint8)
    for u, v in edges:
        if u == v:
            raise ValueError(f"Self-loop edge ({u},{v})")
        adj[u, v] = 1
        adj[v, u] = 1
    np.fill_diagonal(adj, 0)
    return adj


def _assert(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def _gf2_rank_from_rows_bitmasks(row_bitmasks: list[int]) -> int:
    basis: dict[int, int] = {}
    for row in row_bitmasks:
        x = int(row)
        while x:
            pivot = x.bit_length() - 1
            b = basis.get(pivot)
            if b is None:
                basis[pivot] = x
                break
            x ^= b
    return len(basis)


def _rows_to_bitmasks(mat: np.ndarray) -> list[int]:
    if mat.ndim != 2:
        raise ValueError("expected 2D array")
    rows: list[int] = []
    for r in mat.astype(np.uint8):
        bits = 0
        for j, v in enumerate(r.tolist()):
            if v & 1:
                bits |= 1 << j
        rows.append(bits)
    return rows


def _vec_support_to_binary(n: int, support: list[int]) -> np.ndarray:
    v = np.zeros((n,), dtype=np.uint8)
    for idx in support:
        v[idx] = 1
    return v


def _gf2_rank_from_binary_rows(mat: np.ndarray) -> int:
    return _gf2_rank_from_rows_bitmasks(_rows_to_bitmasks(mat % 2))


@dataclass(frozen=True)
class BundlePaths:
    symplectic: Path = ROOT / "W33_symplectic_audit_bundle.zip"
    gf2_code: Path = ROOT / "W33_GF2_kernel_code_bundle.zip"
    h8_qform: Path = ROOT / "W33_H8_quadratic_form_bundle.zip"
    roots120: Path = ROOT / "W33_to_H_to_120root_SRG_bundle.zip"
    gaugefix: Path = ROOT / "W33_global_gaugefix_no16_bundle.zip"
    quotient: Path = ROOT / "W33_quotient_closure_complement_and_noniso_line_curvature_bundle.zip"


def verify_w33_graph() -> np.ndarray:
    b = BundlePaths()
    edge_rows = _read_csv_from_zip(b.symplectic, "point_graph_edges.csv")
    edges = [(int(r["u"]), int(r["v"])) for r in edge_rows]
    _assert(len(edges) == 240, "W33 should have 240 edges (40*12/2)")
    A = _build_undirected_adjacency(40, edges)

    deg = A.sum(axis=1)
    _assert(np.all(deg == 12), f"W33 degree mismatch: {sorted(set(deg.tolist()))}")

    # SRG check via A^2 counts of common neighbors.
    A2 = (A.astype(np.int16) @ A.astype(np.int16)).astype(np.int16)
    _assert(np.all(np.diag(A2) == 12), "Diagonal of A^2 should be 12 (= degree)")
    mask_adj = A.astype(bool)
    mask_nonadj = ~mask_adj
    np.fill_diagonal(mask_nonadj, False)
    _assert(np.all(A2[mask_adj] == 2), "Adjacent pairs should have λ=2 common neighbors")
    _assert(np.all(A2[mask_nonadj] == 4), "Non-adjacent pairs should have μ=4 common neighbors")

    # Spectrum: 12^(1), 2^(24), (-4)^(15)
    evals = np.linalg.eigvalsh(A.astype(np.float64))
    rounded = np.rint(evals).astype(int)
    _assert(np.allclose(evals, rounded, atol=1e-6), "Eigenvalues not near integers as expected")
    unique, counts = np.unique(rounded, return_counts=True)
    spec = dict(zip(unique.tolist(), counts.tolist(), strict=True))
    _assert(spec.get(12) == 1, f"Expected eigenvalue 12 multiplicity 1, got {spec}")
    _assert(spec.get(2) == 24, f"Expected eigenvalue 2 multiplicity 24, got {spec}")
    _assert(spec.get(-4) == 15, f"Expected eigenvalue -4 multiplicity 15, got {spec}")

    # Square-zero mod 2: A^2 ≡ 0 (mod 2)
    A2_mod2 = (A.astype(np.uint8) @ A.astype(np.uint8)) & 1
    _assert(int(A2_mod2.sum()) == 0, "A^2 mod 2 should be the zero matrix")

    # Rank over GF(2)
    rank_gf2 = _gf2_rank_from_binary_rows(A)
    _assert(rank_gf2 == 16, f"Expected rank_GF2(A)=16, got {rank_gf2}")

    return A


def verify_gf2_kernel_code(A: np.ndarray) -> None:
    b = BundlePaths()
    gen_rows = _read_csv_from_zip(b.gf2_code, "generators_weight6_linepair_xors.csv")
    _assert(len(gen_rows) == 240, f"Expected 240 weight-6 generators, got {len(gen_rows)}")

    # Verify each generator is weight 6 and in ker(A) over GF(2).
    gen_mat = np.zeros((len(gen_rows), 40), dtype=np.uint8)
    for i, r in enumerate(gen_rows):
        support = _parse_int_list(r["support_points"])
        w = int(r["weight"])
        _assert(w == 6, f"Generator {i}: expected weight 6, got {w}")
        _assert(len(support) == 6, f"Generator {i}: support length != 6")
        _assert(int(r["in_kernel"]) == 1, f"Generator {i}: in_kernel flag not 1")
        gen_mat[i] = _vec_support_to_binary(40, support)
        Ax = (A.astype(np.uint8) @ gen_mat[i].astype(np.uint8)) & 1
        _assert(int(Ax.sum()) == 0, f"Generator {i}: A*x != 0 (mod 2)")

    gen_rank = _gf2_rank_from_binary_rows(gen_mat)
    _assert(gen_rank == 24, f"Generators should span dim 24 kernel, got rank {gen_rank}")

    # Verify the provided basis is a basis for ker(A).
    basis_rows = _read_csv_from_zip(b.gf2_code, "code_basis_24x40.csv")
    _assert(len(basis_rows) == 24, f"Expected 24 basis rows, got {len(basis_rows)}")
    basis = np.array(
        [[int(r[f"v{j}"]) for j in range(40)] for r in basis_rows],
        dtype=np.uint8,
    )
    basis_rank = _gf2_rank_from_binary_rows(basis)
    _assert(basis_rank == 24, f"Kernel basis should have rank 24, got {basis_rank}")
    Ax = (A.astype(np.uint8) @ basis.T.astype(np.uint8)) & 1
    _assert(int(Ax.sum()) == 0, "Some basis vectors are not in ker(A)")


def _eval_q_from_terms(x: np.ndarray, q_terms: list[str]) -> int:
    """
    Evaluate a quadratic polynomial over GF(2) given as a list of monomials like:
      'x3' or 'x1x7'
    """
    total = 0
    for term in q_terms:
        term = term.strip()
        if not term:
            continue
        if term.startswith("x") and "x" not in term[1:]:
            # linear term xk
            k = int(term[1:])
            total ^= int(x[k]) & 1
            continue
        if term.count("x") == 2:
            # quadratic term xixj
            parts = term.split("x")
            # e.g. ["", "0", "4"] for x0x4
            i = int(parts[1])
            j = int(parts[2])
            total ^= (int(x[i]) & 1) & (int(x[j]) & 1)
            continue
        raise ValueError(f"Unrecognized term: {term!r}")
    return total & 1


def verify_h8_quadratic_form() -> None:
    b = BundlePaths()
    q_data = _read_json_from_zip(b.h8_qform, "H_invariant_quadratic_form.json")
    assert isinstance(q_data, dict)
    q_terms = q_data["q_terms_mod2"]

    # Count q-values on all vectors in F2^8.
    counts = {0: 0, 1: 0}
    counts_nonzero = {0: 0, 1: 0}
    for i in range(256):
        x = np.array([(i >> k) & 1 for k in range(8)], dtype=np.uint8)
        q = _eval_q_from_terms(x, q_terms)
        counts[q] += 1
        if i != 0:
            counts_nonzero[q] += 1
    _assert(counts == {0: 136, 1: 120}, f"q-value counts on F2^8 mismatch: {counts}")
    _assert(counts_nonzero == {0: 135, 1: 120}, f"q-value counts on nonzero mismatch: {counts_nonzero}")

    # Orbit sizes under provided generators in GL(8,2).
    gen_data = _read_json_from_zip(b.h8_qform, "H_generator_matrices_8x8.json")
    assert isinstance(gen_data, dict)
    gens = [np.array(m, dtype=np.uint8) & 1 for m in gen_data["generator_matrices_8x8"]]

    def act(mat: np.ndarray, vec: int) -> int:
        x = np.array([(vec >> k) & 1 for k in range(8)], dtype=np.uint8)
        y = (mat @ x) & 1
        out = 0
        for k, bit in enumerate(y.tolist()):
            out |= (int(bit) & 1) << k
        return out

    unvisited = set(range(1, 256))
    orbit_sizes: list[int] = []
    while unvisited:
        start = next(iter(unvisited))
        orbit = {start}
        frontier = [start]
        unvisited.remove(start)
        while frontier:
            v = frontier.pop()
            for g in gens:
                w = act(g, v)
                if w not in orbit:
                    orbit.add(w)
                    if w in unvisited:
                        unvisited.remove(w)
                    frontier.append(w)
        orbit_sizes.append(len(orbit))

    orbit_sizes.sort()
    _assert(orbit_sizes == [120, 135], f"Expected two nonzero orbits [120,135], got {orbit_sizes}")


def verify_root_graph_srg() -> None:
    b = BundlePaths()
    roots = _read_csv_from_zip(b.roots120, "roots_120_list.csv")
    _assert(len(roots) == 120, f"Expected 120 roots, got {len(roots)}")
    for r in roots:
        _assert(int(r["q"]) == 1, "Root list contains a vector with q != 1")

    edge_rows = _read_csv_from_zip(b.roots120, "root_graph_edges_srg120_56_28_24.csv")
    edges = [(int(r["u"]), int(r["v"])) for r in edge_rows]
    _assert(len(edges) == 3360, f"Expected 3360 edges in SRG(120,56,...), got {len(edges)}")
    A = _build_undirected_adjacency(120, edges)
    deg = A.sum(axis=1)
    _assert(np.all(deg == 56), f"Root graph degree mismatch: {sorted(set(deg.tolist()))}")

    A2 = (A.astype(np.int16) @ A.astype(np.int16)).astype(np.int16)
    _assert(np.all(np.diag(A2) == 56), "Diagonal of A^2 should equal degree 56")
    mask_adj = A.astype(bool)
    mask_nonadj = ~mask_adj
    np.fill_diagonal(mask_nonadj, False)
    _assert(np.all(A2[mask_adj] == 28), "Adjacent pairs should have λ=28 common neighbors")
    _assert(np.all(A2[mask_nonadj] == 24), "Non-adjacent pairs should have μ=24 common neighbors")


def verify_240_to_120_projection() -> None:
    b = BundlePaths()
    roots = _read_csv_from_zip(b.roots120, "roots_120_list.csv")
    h8_to_root_id = {int(r["h8_int"]): int(r["root_id"]) for r in roots}
    _assert(len(h8_to_root_id) == 120, "Expected 120 distinct h8_int values in roots list")

    mapping_rows = _read_csv_from_zip(b.roots120, "generator_to_root_map.csv")
    _assert(len(mapping_rows) == 240, f"Expected 240 generator->root map rows, got {len(mapping_rows)}")
    counts: dict[int, int] = {}
    for r in mapping_rows:
        h8_int = int(r["h8_int"])
        root_id = h8_to_root_id[h8_int]
        counts[root_id] = counts.get(root_id, 0) + 1
    _assert(len(counts) == 120, f"Expected 120 distinct roots in map, got {len(counts)}")
    bad = [k for k, v in counts.items() if v != 2]
    _assert(not bad, f"Expected each root to have exactly 2 preimages; bad roots: {bad[:10]}")


def verify_global_gauge_fix_partition() -> None:
    b = BundlePaths()
    summary = _read_json_from_zip(b.gaugefix, "summary.json")
    assert isinstance(summary, dict)
    result = summary["result"]
    _assert(result["c16"] == 0, "Gauge-fix summary says some 16-weight edges remain")
    _assert(result["c0"] == 120 and result["c12"] == 3240, "Gauge-fix edge weight counts mismatch")

    edges = _read_csv_from_zip(b.gaugefix, "edge_triples_with_weights_3360.csv")
    _assert(len(edges) == 3360, "Expected 3360 root-graph edges in gauge-fix bundle")
    weight_counts: dict[int, int] = {}
    for r in edges:
        w = int(r["weight"])
        weight_counts[w] = weight_counts.get(w, 0) + 1
    _assert(weight_counts == {0: 120, 12: 3240}, f"Edge weight histogram mismatch: {weight_counts}")

    # Verify the 40 zero-defect triangles partition the 120 roots.
    zero_tris = _read_csv_from_zip(b.gaugefix, "zero_triangles_by_base_point_40.csv")
    _assert(len(zero_tris) == 40, f"Expected 40 flat triples, got {len(zero_tris)}")
    seen: set[int] = set()
    for r in zero_tris:
        tri = [int(x) for x in r["triangle_vertices"].split("-") if x.strip()]
        _assert(len(tri) == 3, f"Flat triple is not size 3: {tri}")
        _assert(len(set(tri)) == 3, f"Flat triple has repeats: {tri}")
        for v in tri:
            _assert(0 <= v < 120, f"Flat triple root id out of range: {v}")
        _assert(not (set(tri) & seen), "Flat triples do not partition (overlap found)")
        seen |= set(tri)
    _assert(len(seen) == 120, f"Flat triples cover {len(seen)} vertices, expected 120")


def verify_quotient_and_holonomy(A_w33: np.ndarray) -> None:
    b = BundlePaths()

    # Quotient edges = 540, degree 27 on 40 vertices.
    q_edges_rows = _read_csv_from_zip(b.quotient, "quotient_graph_edges_540.csv")
    _assert(len(q_edges_rows) == 540, f"Expected 540 quotient edges, got {len(q_edges_rows)}")
    q_edges = [(int(r["p"]), int(r["q"])) for r in q_edges_rows]
    Q = _build_undirected_adjacency(40, q_edges)
    q_deg = Q.sum(axis=1)
    _assert(np.all(q_deg == 27), f"Quotient graph degree mismatch: {sorted(set(q_deg.tolist()))}")

    # Q must be the complement of W33.
    W_comp = (1 - A_w33).astype(np.uint8)
    np.fill_diagonal(W_comp, 0)
    _assert(np.array_equal(Q, W_comp), "Quotient graph does not equal complement of W33 adjacency")

    # Holonomy classification: identity vs 3-cycle; identity triangles correspond to non-isotropic PG(3,3) lines.
    tri_rows = _read_csv_from_zip(b.quotient, "quotient_triangles_holonomy_3240.csv")
    _assert(len(tri_rows) == 3240, f"Expected 3240 quotient triangles, got {len(tri_rows)}")

    identity_tris: set[tuple[int, int, int]] = set()
    hol_counts: dict[str, int] = {}
    for r in tri_rows:
        hol = r["holonomy_type"]
        hol_counts[hol] = hol_counts.get(hol, 0) + 1
        tri = tuple(sorted((int(r["p"]), int(r["q"]), int(r["r"]))))
        if hol == "identity":
            identity_tris.add(tri)
    _assert(hol_counts.get("identity") == 360 and hol_counts.get("3-cycle") == 2880, f"Holonomy counts mismatch: {hol_counts}")

    # Independently compute the 360 triples arising from the 90 non-isotropic lines in PG(3,3).
    lines_all = _read_csv_from_zip(b.symplectic, "lines_all_PG33.csv")
    noniso_lines = [
        _parse_int_list(r["points(point_id list)"])
        for r in lines_all
        if int(r["is_isotropic"]) == 0
    ]
    _assert(len(noniso_lines) == 90, f"Expected 90 non-isotropic projective lines, got {len(noniso_lines)}")
    noniso_tris: set[tuple[int, int, int]] = set()
    for pts in noniso_lines:
        _assert(len(pts) == 4, f"Projective line does not have 4 points: {pts}")
        for a, b_, c in combinations(sorted(pts), 3):
            noniso_tris.add((a, b_, c))
    _assert(len(noniso_tris) == 360, f"Expected 360 triples from non-isotropic lines, got {len(noniso_tris)}")
    _assert(identity_tris == noniso_tris, "Identity-holonomy triangles do not match non-isotropic-line triples")


def main() -> int:
    missing = [p for p in BundlePaths().__dict__.values() if not Path(p).exists()]
    if missing:
        print("Missing required artifact bundles:", file=sys.stderr)
        for m in missing:
            print(f"  - {m}", file=sys.stderr)
        return 2

    print("Verifying W33 kernel artifacts…")
    A = verify_w33_graph()
    print("  OK: W33 SRG(40,12,2,4), spectrum, A^2≡0 (mod2), rank_GF2(A)=16")

    verify_gf2_kernel_code(A)
    print("  OK: GF(2) kernel code C=[40,24,6], 240 weight-6 generators span ker(A)")

    verify_h8_quadratic_form()
    print("  OK: H has quadratic form with nonzero orbit split 135/120 under |G|=51840")

    verify_240_to_120_projection()
    print("  OK: 240→120 projection has 2 preimages per root")

    verify_root_graph_srg()
    print("  OK: Root graph is SRG(120,56,28,24)")

    verify_global_gauge_fix_partition()
    print("  OK: Global gauge-fix eliminates all 16-weight defects; 40 flat triples partition roots")

    verify_quotient_and_holonomy(A)
    print("  OK: Quotient Q is complement of W33; identity holonomy triangles ↔ 90 non-isotropic lines")

    print("All checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
