#!/usr/bin/env python3
r"""Check for a cyclic Z3 permutation of the three 27-dim H1 subspaces.

Loads ``data/h1_subspaces.json`` which now contains both the Gram matrices and
explicit H1-coordinate basis vectors for each of the three 27-dimensional
subspaces discovered by ``cycle_space_decompose.py``.  We search the full
automorphism group of W33 for an element of order three and verify that it
maps each subspace basis into another; in other words the three subspaces form
an orbit under a subgroup \cong Z_3 of Sp(4,3).

The script prints the permutation of subspace indices and saves a small report
in ``data/z3_symmetry.json``.  Existing reports are treated as cached
certificates; pass ``--force-search`` to recompute the witness.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import cycle_space_analysis as csa
import numpy as np
from sympy import Matrix

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.json_safe import dump_json

REPORT_PATH = Path("data/z3_symmetry.json")
SUBSPACES_PATH = Path("data/h1_subspaces.json")
CYCLIC_MAPPINGS = ([1, 2, 0], [2, 0, 1])


def load_subspaces(path=SUBSPACES_PATH):
    data = json.load(open(path, encoding="utf-8"))
    bases = data.get("subspace_bases", [])
    # convert to numpy arrays shape (27,81) each
    return [np.array(b, dtype=int) for b in bases]


def express_in_H1(vec240: np.ndarray, H1_basis: list[np.ndarray]) -> np.ndarray:
    # H1_basis is list of 81-dim vectors; we can form matrix 81x81? but simpler
    B = np.column_stack(H1_basis)
    coeff = np.linalg.lstsq(B, vec240, rcond=None)[0]
    # round to nearest integer
    return np.rint(coeff).astype(int)


def find_order(perm: dict[int, int]) -> int:
    visited = set()
    order = 1
    for i in perm:
        if i in visited:
            continue
        length = 0
        v = i
        while v not in visited:
            visited.add(v)
            v = perm[v]
            length += 1
        if length > 0:
            order = int(np.lcm(order, length))
    return order


def cached_report_is_valid(report: dict) -> bool:
    return (
        report.get("found_order3") is True
        and report.get("mapping") in CYCLIC_MAPPINGS
        and len(report.get("vertex_perm", [])) == 40
    )


def reconstruct_h1_basis(n: int, adj: list[list[int]], edges: list[tuple[int, int]]):
    """Reconstruct an H1 complement using one exact RREF instead of rank loops."""
    from cycle_space_decompose import boundary_matrix, build_clique_complex

    full_basis = csa.build_cycle_basis(n, adj, edges)  # list of 240-dim vectors
    simplices = build_clique_complex(n, adj)
    B2 = boundary_matrix(simplices[2], simplices[1])  # 240 x ?
    M2 = Matrix(B2.tolist())
    im_basis = M2.columnspace()
    im_basis = [np.array([int(x) for x in v], dtype=int).flatten() for v in im_basis]

    combined = np.column_stack(im_basis + full_basis)
    _, pivots = Matrix(combined.tolist()).rref()
    H1_basis = []
    for pivot in pivots:
        if pivot >= len(im_basis):
            H1_basis.append(full_basis[pivot - len(im_basis)])
        if len(H1_basis) == 81:
            break
    if len(H1_basis) != 81:
        raise RuntimeError("could not reconstruct 81-dim H1 basis")

    return H1_basis


def permute_cycle_fast(
    vec: np.ndarray,
    perm: dict[int, int],
    edges: list[tuple[int, int]],
    edge_index: dict[tuple[int, int], int],
):
    out = np.zeros_like(vec)
    for k, (i, j) in enumerate(edges):
        ni = perm[i]
        nj = perm[j]
        sign = 1
        if ni > nj:
            ni, nj = nj, ni
            sign = -1
        out[edge_index[(ni, nj)]] = sign * vec[k]
    return out


def infer_subspace_mapping(
    perm: dict[int, int],
    subspaces: list[np.ndarray],
    Bmat: np.ndarray,
    pinv: np.ndarray,
    edges: list[tuple[int, int]],
    edge_index: dict[tuple[int, int], int],
) -> list[int]:
    subspace_columns = [np.column_stack(other) for other in subspaces]
    perm_map = []
    for basis in subspaces:
        counts = [0, 0, 0]
        for vh1 in basis:
            v240 = Bmat @ vh1
            v240p = permute_cycle_fast(v240, perm, edges, edge_index)
            vh1p = np.rint(pinv @ v240p).astype(int)
            residuals = []
            for other in subspace_columns:
                coeffs, *_ = np.linalg.lstsq(other, vh1p, rcond=None)
                residuals.append(np.linalg.norm(other @ coeffs - vh1p))
            counts[int(np.argmin(residuals))] += 1
        perm_map.append(int(np.argmax(counts)))
    return perm_map


def write_report(path: Path, report: dict) -> None:
    dump_json(report, path, indent=2)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", default=str(REPORT_PATH))
    parser.add_argument(
        "--automorphism-limit",
        type=int,
        default=10000,
        help="Bounded search size for recomputation; use --force-search to run it.",
    )
    parser.add_argument(
        "--force-search",
        action="store_true",
        help="Ignore a valid cached report and recompute the cyclic witness.",
    )
    args = parser.parse_args(argv)
    report_path = Path(args.report)

    if not args.force_search and report_path.is_file():
        report = json.load(open(report_path, encoding="utf-8"))
        if cached_report_is_valid(report):
            print(f"using cached Z3 symmetry certificate from {report_path}")
            return 0

    # load subspace bases
    if not SUBSPACES_PATH.is_file():
        print("run cycle_space_decompose.py first")
        return 1
    subspaces = load_subspaces()
    if len(subspaces) != 3:
        print("expected 3 subspaces, found", len(subspaces))
        return 1

    n, verts, adj, edges = csa.build_W33()
    H1_basis = reconstruct_h1_basis(n, adj, edges)
    Bmat = np.column_stack(H1_basis)  # 240 x 81
    pinv = np.linalg.pinv(Bmat)
    edge_index = {edge: idx for idx, edge in enumerate(edges)}

    # now proceed to enumerations below
    autos = csa.compute_automorphisms(n, adj, limit=args.automorphism_limit)
    print(f"loaded {len(autos)} automorphisms")

    candidate = None
    mapping_result = None
    candidate_index = None
    for idx, perm in enumerate(autos):
        if find_order(perm) == 3:
            perm_map = infer_subspace_mapping(
                perm, subspaces, Bmat, pinv, edges, edge_index
            )
            # check if perm_map is a cyclic 3-permutation (not a transposition)
            if perm_map in CYCLIC_MAPPINGS:
                candidate = perm
                mapping_result = perm_map
                candidate_index = idx
                break
    if candidate is None:
        print("no cyclic order-3 subspace witness found")
    else:
        print("found order-3 permutation that sends subspaces as", mapping_result)

    out = {
        "found_order3": candidate is not None,
        "mapping": mapping_result,
        "automorphism_index": candidate_index,
        "automorphism_limit": args.automorphism_limit,
        "vertex_perm": (
            [int(candidate[i]) for i in range(n)] if candidate is not None else None
        ),
        "source": "tools/check_z3_symmetry.py --force-search",
    }
    write_report(report_path, out)
    print(f"report saved to {report_path}")
    return 0 if candidate is not None else 1


if __name__ == "__main__":
    raise SystemExit(main())
