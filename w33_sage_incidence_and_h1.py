"""Sage + PySymmetry pipeline for W33 incidence automorphisms and H1 action.

Run (recommended):

    sage -python w33_sage_incidence_and_h1.py

Options:

    --field=QQ            (default) exact arithmetic (recommended for PySymmetry)
    --field=GF            finite-field arithmetic (faster; set --prime)
    --prime=1000003       prime used when --field=GF
    --pysymmetry          attempt isotypic analysis (gated by group order)
    --pysymmetry-max-order=2000

Outputs JSON to:

    data/w33_sage_incidence_h1.json (or claude_workspace/data/w33_sage_incidence_h1.json)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict, List, Sequence, Tuple


def _parse_args(argv: Sequence[str]) -> dict:
    opts = {
        "field": "QQ",
        "prime": 1_000_003,
        "use_pysymmetry": False,
        "pysymmetry_max_order": 2000,
        "enumerate_max_order": 5000,
        "compute_character": False,
    }
    for a in argv[1:]:
        if a == "--pysymmetry":
            opts["use_pysymmetry"] = True
        elif a.startswith("--pysymmetry-max-order="):
            opts["pysymmetry_max_order"] = int(a.split("=", 1)[1])
        elif a.startswith("--enumerate-max-order="):
            opts["enumerate_max_order"] = int(a.split("=", 1)[1])
        elif a == "--character":
            opts["compute_character"] = True
        elif a.startswith("--field="):
            opts["field"] = a.split("=", 1)[1]
        elif a.startswith("--prime="):
            opts["prime"] = int(a.split("=", 1)[1])
        else:
            raise SystemExit(f"Unknown argument: {a}")
    if opts["field"] not in {"QQ", "GF"}:
        raise SystemExit("--field must be QQ or GF")
    return opts


def main() -> None:
    print("=== W33 Sage Incidence Pipeline Starting ===", flush=True)
    opts = _parse_args(sys.argv)

    here = Path(__file__).resolve().parent

    # Make local helpers importable under Sage's Python.
    sys.path.insert(0, str(here))

    # Make the bundled PySymmetry importable (when running under Sage).
    pysymmetry_root = here / "external" / "pysymmetry"
    if pysymmetry_root.exists():
        sys.path.insert(0, str(pysymmetry_root))

    from sage.all import GF, QQ, Graph, VectorSpace, matrix

    from lib.simplicial_homology import boundary_matrix, faces
    from lib.w33_io import W33DataPaths, load_w33_lines, simplices_from_lines

    field = QQ
    if opts["field"] == "GF":
        field = GF(int(opts["prime"]))

    paths = W33DataPaths.from_this_file(__file__)
    lines = load_w33_lines(paths)

    # Incidence bipartite graph: points 1..40, lines 41..80
    edges: List[Tuple[int, int]] = []
    for line_index, pts in enumerate(lines):
        line_vertex = 41 + line_index
        for p in pts:
            edges.append((p + 1, line_vertex))

    G = Graph(multiedges=False, loops=False)
    G.add_vertices(range(1, 81))
    G.add_edges(edges)

    # Compute automorphisms preserving the bipartition.
    A = G.automorphism_group(partition=[list(range(1, 41)), list(range(41, 81))])

    group_order = int(A.order())
    gens = list(A.gens())

    def gen_point_perm(gen) -> List[int]:
        # 0-based point permutation: i -> perm[i]
        return [int(gen(i + 1)) - 1 for i in range(40)]

    def gen_line_perm(gen) -> List[int]:
        # 0-based line permutation: i -> perm[i]
        return [int(gen(41 + i)) - 41 for i in range(40)]

    gen_data = []
    for g in gens:
        gen_data.append({"points": gen_point_perm(g), "lines": gen_line_perm(g)})

    point_orbits = [
        sorted([int(v) - 1 for v in orb]) for orb in A.orbits() if min(orb) <= 40
    ]
    line_orbits = [
        sorted([int(v) - 41 for v in orb]) for orb in A.orbits() if min(orb) >= 41
    ]

    simplices = simplices_from_lines(lines)
    vertices = simplices[0]
    edges1 = simplices[1]
    tris2 = simplices[2]

    n0 = len(vertices)
    n1 = len(edges1)
    n2 = len(tris2)

    def boundary_matrix_exact(k_simplices, km1_simplices):
        idx = {s: i for i, s in enumerate(km1_simplices)}
        m = len(km1_simplices)
        n = len(k_simplices)
        M = [[0] * n for _ in range(m)]
        for j, s in enumerate(k_simplices):
            for sign, f in faces(s):
                i = idx.get(f)
                if i is None:
                    continue
                M[i][j] += sign
        return M

    # Boundary matrices over the chosen field.
    if opts["field"] == "GF":
        p = int(opts["prime"])
        d1 = matrix(field, boundary_matrix(edges1, vertices, p=p))
        d2 = matrix(field, boundary_matrix(tris2, edges1, p=p))
    else:
        d1 = matrix(field, boundary_matrix_exact(edges1, vertices))
        d2 = matrix(field, boundary_matrix_exact(tris2, edges1))

    V = VectorSpace(field, n1)
    Z1 = d1.right_kernel()  # cycles
    B1 = d2.column_space()  # boundaries

    beta1 = int(Z1.dimension() - B1.dimension())

    # Extend basis(B1) to a basis(Z1) to get explicit coset representatives for H1.
    B_basis = list(B1.basis())
    Z_basis = list(Z1.basis())

    span = V.subspace(B_basis)
    H_basis = []
    for v in Z_basis:
        if v not in span:
            H_basis.append(v)
            span = V.subspace(list(span.basis()) + [v])
        if len(H_basis) == beta1:
            break
    if len(H_basis) != beta1:
        raise RuntimeError(
            f"Failed to build H1 basis: expected {beta1}, got {len(H_basis)}"
        )

    # Matrix whose columns are a basis of Z1: [B_basis | H_basis]
    Z_cols = [*B_basis, *H_basis]
    M = matrix(field, [list(v) for v in Z_cols]).transpose()

    edge_index = {e: i for i, e in enumerate(edges1)}

    def edge_action_maps(point_perm: Sequence[int]) -> Tuple[List[int], List[int]]:
        idx_map = [0] * n1
        sgn_map = [0] * n1
        for i, (a, b) in enumerate(edges1):
            ua = point_perm[a]
            ub = point_perm[b]
            if ua < ub:
                idx_map[i] = edge_index[(ua, ub)]
                sgn_map[i] = 1
            else:
                idx_map[i] = edge_index[(ub, ua)]
                sgn_map[i] = -1
        return idx_map, sgn_map

    def apply_edge_action(v, idx_map: Sequence[int], sgn_map: Sequence[int]):
        # Build result vector using list arithmetic, then convert
        w_list = [field(0)] * n1
        for i in range(n1):
            c = v[i]
            if c == 0:
                continue
            j = idx_map[i]
            w_list[j] += c * field(sgn_map[i])
        return V(w_list)

    # Induced action on H1 for each generator.
    h1_action_mats: List[List[List[str]]] = []
    h1_action_mats_sage = []
    for g in gens:
        perm = gen_point_perm(g)
        idx_map, sgn_map = edge_action_maps(perm)

        Acols = []
        for basis_vec in H_basis:
            w = apply_edge_action(basis_vec, idx_map, sgn_map)
            # Solve [B|H] * coeffs = w in Z1 basis.
            coeffs = M.solve_right(w)
            h_coords = coeffs[len(B_basis) :]
            Acols.append(list(h_coords))

        Ah = matrix(field, Acols).transpose()  # columns correspond to action on basis
        h1_action_mats_sage.append(Ah)

        # JSON-safe: stringify entries (QQ elements / finite field elements)
        h1_action_mats.append(
            [[str(Ah[r, c]) for c in range(beta1)] for r in range(beta1)]
        )

    out = {
        "field": opts["field"],
        "prime": int(opts["prime"]) if opts["field"] == "GF" else None,
        "incidence": {
            "group_order": group_order,
            "structure_description": str(A.structure_description()),
            "is_abelian": bool(A.is_abelian()),
            "is_solvable": bool(A.is_solvable()),
            "generators": gen_data,
            "point_orbits": point_orbits,
            "line_orbits": line_orbits,
        },
        "simplicial_complex": {"n0": n0, "n1": n1, "n2": n2, "n3": len(simplices[3])},
        "homology": {
            "beta1": beta1,
            "dim_Z1": int(Z1.dimension()),
            "dim_B1": int(B1.dimension()),
        },
        "h1_action": {
            "basis": "H_basis extends B1 basis inside Z1",
            "generator_matrices": h1_action_mats,
        },
        "pysymmetry": None,
    }

    # Optional: compute the character values (trace) of the H1 representation.
    # We only do this by enumerating the full group when it is reasonably small.
    if opts["compute_character"]:
        if group_order <= int(opts["enumerate_max_order"]):
            elements = list(A)
            # Build action matrices for all elements by multiplying generator matrices.
            # For now, compute traces using the induced permutation on edges directly.
            # (This avoids repeated H1 re-solving.)
            traces = []
            for g in elements:
                perm = gen_point_perm(g)
                idx_map, sgn_map = edge_action_maps(perm)
                # Action on H1 basis vectors: reuse the same solve routine.
                Acols = []
                for basis_vec in H_basis:
                    w = apply_edge_action(basis_vec, idx_map, sgn_map)
                    coeffs = M.solve_right(w)
                    h_coords = coeffs[len(B_basis) :]
                    Acols.append(list(h_coords))
                Ah = matrix(field, Acols).transpose()
                traces.append(str(Ah.trace()))

            out["h1_action"]["character"] = {
                "enumerated": True,
                "num_elements": len(elements),
                "traces": traces,
            }
        else:
            out["h1_action"]["character"] = {
                "enumerated": False,
                "skipped": True,
                "reason": f"group_order={group_order} exceeds --enumerate-max-order={opts['enumerate_max_order']}",
            }

    # Optional: attempt a PySymmetry isotypic analysis (only safe for small groups).
    if opts["use_pysymmetry"]:
        if group_order <= int(opts["pysymmetry_max_order"]):
            try:
                from pysymmetry import representation

                rep = representation(list(A.gens()), h1_action_mats_sage, field=field)
                FG = rep.domain()

                proj = FG.isotypic_projection(rep)
                iso_dims = [int(P.rank()) for P in proj]
                out["pysymmetry"] = {
                    "enabled": True,
                    "group_order": group_order,
                    "num_isotypic_components": len(iso_dims),
                    "isotypic_component_dims": iso_dims,
                }
            except Exception as e:  # pragma: no cover
                out["pysymmetry"] = {"enabled": False, "error": str(e)}
        else:
            out["pysymmetry"] = {
                "enabled": False,
                "skipped": True,
                "reason": f"group_order={group_order} exceeds --pysymmetry-max-order={opts['pysymmetry_max_order']}",
            }

    out_path = paths.data_root / "w33_sage_incidence_h1.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    print(f"Wrote: {out_path}")
    print(f"Incidence automorphism group order: {group_order}")
    print(f"H1 dimension (beta1): {beta1}")


if __name__ == "__main__":
    main()
