#!/usr/bin/env python3
"""Match C2(W33) triangle irreducible components to PSp(4,3) irreps (via GAP).

Produces a JSON report in `checks/` with the GAP-irrep indices and multiplicities
for the 160-dimensional triangle representation.

This script supports two modes:
 - libgap (Sage) when available (original path),
 - GAP CLI fallback (no Sage required) using the repo's pure‑Python generators.

Usage:
  python scripts/w33_triangle_irrep_match_gap.py
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

# allow importing local modules
here = Path(__file__).resolve().parent
sys.path.insert(0, str(here))

# project helpers (pure-Python triangle building)
from w33_homology import build_clique_complex, build_w33

# Sage / GAP (prefer libgap when available; otherwise use GAP CLI)
try:
    from sage.all import Graph, libgap  # type: ignore

    _HAS_LIBGAP = True
except Exception:
    Graph = None
    libgap = None
    _HAS_LIBGAP = False

import ast
import shlex
import subprocess


def _gap_line_payload(stdout: str, marker: str) -> str | None:
    for line in stdout.splitlines():
        if line.startswith(marker):
            return line[len(marker) :].strip()
    return None


def _gap_block_payload(stdout: str, begin_marker: str, end_marker: str) -> str | None:
    begin = stdout.find(begin_marker)
    if begin < 0:
        return None
    begin += len(begin_marker)
    end = stdout.find(end_marker, begin)
    if end < 0:
        return None
    return stdout[begin:end].strip()


def build_triangle_perm_from_vp(vp, triangles, tri_idx):
    n_tri = len(triangles)
    perm = np.zeros(n_tri, dtype=int)
    signs = np.zeros(n_tri, dtype=int)

    for i, tri in enumerate(triangles):
        mapped = [vp[tri[0]], vp[tri[1]], vp[tri[2]]]
        sorted_mapped = tuple(sorted(mapped))
        j = tri_idx[sorted_mapped]
        perm[i] = j

        # orientation sign (parity of permutation that sorts `mapped`)
        inv = 0
        for a in range(3):
            for b in range(a + 1, 3):
                if mapped[a] > mapped[b]:
                    inv += 1
        signs[i] = -1 if (inv % 2) else 1

    return perm, signs


def build_signed_perm_matrix(perm, signs):
    n = len(perm)
    M = np.zeros((n, n), dtype=float)
    for i in range(n):
        M[perm[i], i] = signs[i]
    return M


def main():
    print("=== Match C2 triangle components to PSp(4,3) irreps (GAP) ===")

    # build W33 combinatorial complex (pure Python)
    n, vertices, adj, edges = build_w33()
    simplices = build_clique_complex(n, adj)
    triangles = simplices[2]
    n_tri = len(triangles)
    tri_idx = {t: i for i, t in enumerate(triangles)}

    print(f"W33: {n} vertices, {len(edges)} edges, {n_tri} triangles")

    # If libgap (Sage) is available use the original libgap path; otherwise
    # fall back to GAP CLI driven by the pure-Python Sp(4,3) generators.
    if _HAS_LIBGAP:
        # Build Sage Graph automorphism group (same partition used elsewhere)
        # Use the canonical W33 line data via the prebuilt Graph construction
        # Points are 1..40, lines are 41..80 (consistent with other scripts)
        G = Graph(multiedges=False, loops=False)
        G.add_vertices(range(1, 81))

        # add incidence edges (points 1..40 connect to 41..80)
        # triangles/tetrahedra are built from the point adjacency; build incidence
        for li, pts in enumerate(vertices):
            line_vertex = 41 + li
            for p in pts:
                G.add_edge(p + 1, line_vertex)

        A = G.automorphism_group(partition=[list(range(1, 41)), list(range(41, 81))])
        print(f"Automorphism group order (Sage A.order()): {int(A.order())}")

        gap_grp = libgap(A)

        # Precompute triangle-action matrices for the group's generators (on 40 points)
        gen_perm_elems = list(A.gens())
        gen_tri_mats = []
        for gen in gen_perm_elems:
            # build 0-based vp for the 40 point vertices
            vp = [int(gen(i + 1)) - 1 for i in range(40)]
            perm, signs = build_triangle_perm_from_vp(vp, triangles, tri_idx)
            M = build_signed_perm_matrix(perm, signs)
            gen_tri_mats.append(M)

        # Get conjugacy classes and GAP irreps via libgap
        cc_gap = gap_grp.ConjugacyClasses()
        char_table_gap = gap_grp.CharacterTable()
        irreps = char_table_gap.Irr()

        class_sizes = [int(cc_gap[i].Size()) for i in range(len(cc_gap))]
        G_order = int(gap_grp.Order())
        print(f"Group order (from GAP): {G_order}, conjugacy classes: {len(cc_gap)}")

    else:
        # --- FALLBACK: use pure-Python Sp(4,3) generators + GAP CLI ---
        print("libgap not available — using GAP CLI fallback")
        # Build Sp(4,3) generators as permutations on 40 points
        from e8_embedding_group_theoretic import build_sp43_generators

        gen_perms = build_sp43_generators(
            vertices, adj
        )  # tuples of length 40 (0-based)
        if not gen_perms:
            raise RuntimeError("No generators produced by build_sp43_generators()")

        # Prepare GAP script to compute conjugacy classes & representatives
        perm_strings = []
        for p in gen_perms:
            # GAP uses 1-based indexing
            ps = ",".join(str(x + 1) for x in p)
            perm_strings.append(f"PermList([{ps}])")

        gap_code = []
        gap_code.append(f"gens := [{','.join(perm_strings)}];;")
        gap_code.append("G := Group(gens);;")
        gap_code.append("CC := ConjugacyClasses(G);;")
        gap_code.append('Print("GAP:GORDER:", Size(G), "\\n");')
        gap_code.append('Print("GAP:NUM_CLASSES:", Length(CC), "\\n");')
        gap_code.append('Print("GAP:CLASS_SIZES_BEGIN\\n");')
        gap_code.append('Print(List(CC, c->Size(c)), "\\n");')
        gap_code.append('Print("GAP:CLASS_SIZES_END\\n");')
        # Print representatives as lists of images on [1..40]
        gap_code.append('Print("GAP:CLASS_REPS_BEGIN\\n");')
        gap_code.append(
            'Print(List(CC, c -> List([1..40], x -> x ^ Representative(c))), "\\n");'
        )
        gap_code.append('Print("GAP:CLASS_REPS_END\\n");')
        gap_code.append("quit;")
        gap_script = "\n".join(gap_code)

        try:
            proc = subprocess.run(
                ["gap", "-q"],
                input=gap_script,
                text=True,
                capture_output=True,
                check=True,
            )
        except FileNotFoundError as exc:
            raise RuntimeError(
                "GAP executable not found on PATH — please install GAP or use Sage/libgap"
            ) from exc
        # Parse GAP output by explicit markers; GAP wraps large lists across lines.
        stdout = proc.stdout
        g_order_payload = _gap_line_payload(stdout, "GAP:GORDER:")
        class_sizes_payload = _gap_block_payload(
            stdout, "GAP:CLASS_SIZES_BEGIN\n", "\nGAP:CLASS_SIZES_END"
        )
        class_reps_payload = _gap_block_payload(
            stdout, "GAP:CLASS_REPS_BEGIN\n", "\nGAP:CLASS_REPS_END"
        )
        G_order = int(g_order_payload) if g_order_payload is not None else None
        class_sizes = (
            ast.literal_eval(class_sizes_payload)
            if class_sizes_payload is not None
            else None
        )
        class_reps = (
            ast.literal_eval(class_reps_payload)
            if class_reps_payload is not None
            else None
        )

        if G_order is None or class_sizes is None or class_reps is None:
            raise RuntimeError(
                f"Failed to parse GAP output (stdout snippets): {stdout.splitlines()[:20]}"
            )

        print(f"Group order (from GAP CLI): {G_order}, classes: {len(class_sizes)}")

        # Build generator triangle matrices from the pure-Python permutations
        gen_tri_mats = []
        for p in gen_perms:
            vp = list(p)
            perm, signs = build_triangle_perm_from_vp(vp, triangles, tri_idx)
            M = build_signed_perm_matrix(perm, signs)
            gen_tri_mats.append(M)

        # Compute chi_C2 (character of triangle rep) for each conjugacy class
        chi_c2_by_class = []
        for rep in class_reps:
            # rep is 1-based images list for 40 points
            vp = [int(x) - 1 for x in rep]
            # compose generator words? simpler: factor representative in terms of gens in GAP
            # but we only have representative permutation; use GAP to factor it into gens.
            # Instead call GAP again to obtain factorization words for each rep (we'll do that below).

        # Compute traces directly from class representatives.
        chi_c2_by_class = []
        for rep in class_reps:
            vp = [int(x) - 1 for x in rep]
            perm, signs = build_triangle_perm_from_vp(vp, triangles, tri_idx)
            M = build_signed_perm_matrix(perm, signs)
            chi_c2_by_class.append(float(np.trace(M)))

        # Now call GAP to get irreducible characters and compute multiplicities by inner product
        # Prepare the chiC2 list string for GAP as exact integers.
        chi_list_str = ",".join(str(int(round(float(x)))) for x in chi_c2_by_class)
        rep_perm_strings = []
        for rep in class_reps:
            rep_perm_strings.append(f"PermList([{','.join(str(int(x)) for x in rep)}])")
        mult_gap_code = []
        mult_gap_code.append(f"gens := [{','.join(perm_strings)}];;")
        mult_gap_code.append("G := Group(gens);;")
        mult_gap_code.append("CC := ConjugacyClasses(G);;")
        mult_gap_code.append("classSizes := List(CC, c -> Size(c));;")
        mult_gap_code.append("tbl := CharacterTable(G);;")
        mult_gap_code.append("irr := Irr(tbl);;")
        mult_gap_code.append(f"firstReps := [{','.join(rep_perm_strings)}];;")
        mult_gap_code.append(f"chiInput := [{chi_list_str}];;")
        mult_gap_code.append(
            "chiC2 := List(CC, c -> chiInput[PositionProperty(firstReps, r -> r in c)]);;"
        )
        mult_gap_code.append(
            "mults := List(irr, chi -> Sum([1..Length(CC)], i -> classSizes[i] * chiC2[i] * chi[i]) / Size(G));;"
        )
        mult_gap_code.append('Print("GAP:IRR_MULTIPLICITIES_BEGIN\\n");')
        mult_gap_code.append('Print(List(mults, x->String(x)), "\\n");')
        mult_gap_code.append('Print("GAP:IRR_MULTIPLICITIES_END\\n");')
        mult_gap_code.append('Print("GAP:IRR_DEGREES_BEGIN\\n");')
        mult_gap_code.append('Print(List(irr, chi -> chi[1]), "\\n");')
        mult_gap_code.append('Print("GAP:IRR_DEGREES_END\\n");')
        mult_gap_code.append("quit;")
        mult_script = "\n".join(mult_gap_code)
        proc3 = subprocess.run(
            ["gap", "-q"], input=mult_script, text=True, capture_output=True, check=True
        )
        mults_payload = _gap_block_payload(
            proc3.stdout,
            "GAP:IRR_MULTIPLICITIES_BEGIN\n",
            "\nGAP:IRR_MULTIPLICITIES_END",
        )
        degrees_payload = _gap_block_payload(
            proc3.stdout, "GAP:IRR_DEGREES_BEGIN\n", "\nGAP:IRR_DEGREES_END"
        )
        mults_raw = (
            ast.literal_eval(mults_payload) if mults_payload is not None else None
        )
        mults = (
            [int(Fraction(str(value))) for value in mults_raw]
            if mults_raw is not None
            else None
        )
        degrees = (
            ast.literal_eval(degrees_payload) if degrees_payload is not None else None
        )

        if mults is None or degrees is None:
            raise RuntimeError(
                "Failed to obtain irreducible multiplicities from GAP CLI"
            )

        # Build final irrep matches list
        multiplicities = []
        for idx_ir, mval in enumerate(mults):
            mround = int(round(float(mval)))
            if mround > 0:
                multiplicities.append(
                    {
                        "gap_irrep_index": idx_ir,
                        "degree": int(degrees[idx_ir]),
                        "mult": mround,
                    }
                )

        # Save results to checks and finish
        out = {
            "G_order": G_order,
            "n_triangles": n_tri,
            "class_sizes": class_sizes,
            "chi_c2_by_class": [float(x) for x in chi_c2_by_class],
            "irrep_matches": multiplicities,
        }

        out_path = (
            Path.cwd()
            / "checks"
            / f"PART_CVII_triangle_irrep_match_gap_cli_{int(__import__('time').time())}.json"
        )
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2, default=str)

        print(f"Wrote: {out_path}")
        print("=== Done (GAP CLI path) ===")
        return

    # For each conjugacy class representative, factor and build triangle matrix
    chi_c2_by_class = []
    for i in range(len(cc_gap)):
        rep_gap = cc_gap[i].Representative()
        # Factorization in terms of the generators of A (libgap)
        word = gap_grp.Factorization(rep_gap)
        ext = word.ExtRepOfObj()
        ext_list = list(ext)

        # start with identity
        R = np.eye(n_tri, dtype=float)

        # ext_list is [g1, e1, g2, e2, ...] with generator indices 1-based
        for j in range(0, len(ext_list), 2):
            gen_idx = int(ext_list[j]) - 1
            power = int(ext_list[j + 1])
            M = gen_tri_mats[gen_idx]
            if power == 0:
                continue
            Mpow = np.linalg.matrix_power(M, power)
            R = Mpow @ R

        chi_val = float(np.trace(R))
        chi_c2_by_class.append(chi_val)

    # Convert GAP irreps to usable complex-valued lists
    def gap_val_to_complex(gap_val):
        try:
            if gap_val.IsInt():
                return int(gap_val)
            if gap_val.IsRat():
                return float(gap_val)
        except Exception:
            pass
        # fallback: convert via sage string -> complex
        return complex(str(gap_val.sage()))

    irrep_info = []
    multiplicities = []

    for idx_ir, ir in enumerate(irreps):
        # ir is a GAP row; index 0 is degree
        # build list of values for each conjugacy class
        ir_vals = [gap_val_to_complex(ir[j]) for j in range(len(cc_gap))]
        ir_deg = (
            int(ir_vals[0].real) if isinstance(ir_vals[0], complex) else int(ir_vals[0])
        )

        # inner product <chi_C2, chi_ir>
        inner_sum = 0
        for j, cls_size in enumerate(class_sizes):
            chi_c2 = chi_c2_by_class[j]
            chi_ir = ir_vals[j]
            inner_sum += (
                cls_size
                * chi_c2
                * (chi_ir.conjugate() if isinstance(chi_ir, complex) else chi_ir)
            )

        inner = inner_sum / G_order
        mult_approx = float(inner.real) if hasattr(inner, "real") else float(inner)
        mult = int(round(mult_approx)) if abs(mult_approx) > 0.01 else 0

        if mult > 0:
            multiplicities.append(
                {"gap_irrep_index": idx_ir, "degree": ir_deg, "mult": mult}
            )

        irrep_info.append({"idx": idx_ir, "degree": ir_deg, "mult_approx": mult_approx})

    # Save results to checks
    out = {
        "G_order": G_order,
        "n_triangles": n_tri,
        "class_sizes": class_sizes,
        "chi_c2_by_class": [float(x) for x in chi_c2_by_class],
        "irrep_matches": multiplicities,
        "irrep_info_sample": irrep_info[:20],
    }

    out_path = (
        Path.cwd()
        / "checks"
        / f"PART_CVII_triangle_irrep_match_{int(__import__('time').time())}.json"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, default=str)

    print(f"Wrote: {out_path}")
    print("=== Done ===")


if __name__ == "__main__":
    main()
