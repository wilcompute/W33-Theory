#!/usr/bin/env python3
"""Pass 164: the rank-10 quadratic form of the incidence tower.

The adjacency mod-2 tower of W(3,3) produced the rank-8 quotient
ker(A)/im(A) with a plus-type form -- the E8 shadow.  Pass 159 showed the
INCIDENCE tower has its own pair: the trade code C = ker_F2(N) is a
doubly-even [40,15,8] code, hence self-orthogonal, and its dual is the
context code C^perp = rowspace_F2(N) of dimension 25.  This witness
computes the incidence analogue of the E8 shadow:

1. THE QUOTIENT FORM.  H = C^perp / C = F2^10 carries the well-defined
   quadratic form q(x+C) = wt(x)/2 mod 2 (doubly-even C) with
   nondegenerate polar form b(x,y) = |x cap y| mod 2.  Its type (number
   of isotropic vectors: 528 = plus / 496 = minus) is computed by exact
   enumeration of all 1024 cosets.

2. THE GROUP ACTION.  PSp(4,3) permutes coordinates, preserves C and
   C^perp, hence acts on H preserving q: an embedding into O(10,2).
   Faithfulness and F2-irreducibility of the action are decided exactly
   (fixed subspaces of the generators; orbit-span test on every nonzero
   vector).

3. THE READING.  Rank 10 = Theta is the string dimension; the isotropic
   count decides whether the incidence shadow is the D5 = SO(10) GUT
   surface (plus type) or the 496-object (minus type; 496 = dim SO(32) =
   dim E8 x E8, the Green-Schwarz anomaly-free dimension).
"""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass158_chiral_trade_lattice_two_480s import (
    build_group,
    build_w33,
    saturated_kernel,
    w33_lines,
)
from analysis.w33_pass161_gq42_ihara_inheritance import small_generating_set

OUT = ROOT / "data" / "w33_pass164_so10_shadow_quotient_form.json"


def rref_f2(matrix):
    """Reduced row echelon form over F2; returns (rref_rows, pivot_cols)."""
    work = [row.copy() for row in matrix]
    pivots = []
    row = 0
    for col in range(work[0].shape[0] if work else 0):
        pivot = next((r for r in range(row, len(work)) if work[r][col]), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        for r in range(len(work)):
            if r != row and work[r][col]:
                work[r] = work[r] ^ work[row]
        pivots.append(col)
        row += 1
    return [work[r] for r in range(row)], pivots


def main():
    points, adjacency, symplectic = build_w33()
    lines = w33_lines(adjacency)
    checks = {}

    incidence = np.zeros((40, 40), dtype=np.uint8)
    for row, line in enumerate(lines):
        for point in line:
            incidence[row, point] = 1

    # trade code C = ker_F2(N) via the saturated integer kernel mod 2
    dark = saturated_kernel((incidence.astype(np.int64)))
    c_rows, c_pivots = rref_f2([r.astype(np.uint8) % 2 for r in dark.T])
    checks["trade_code_dim_15"] = len(c_rows) == 15

    d_rows, d_pivots = rref_f2([incidence[r] for r in range(40)])
    checks["context_code_dim_25"] = len(d_rows) == 25

    c_matrix = np.array(c_rows, dtype=np.uint8)
    d_matrix = np.array(d_rows, dtype=np.uint8)

    checks["trade_code_doubly_even"] = bool(
        all(int(w) % 4 == 0 for w in c_matrix.sum(axis=1))
        and all(
            int((c_matrix[i] & c_matrix[j]).sum()) % 2 == 0
            for i in range(15)
            for j in range(i + 1, 15)
        )
    )
    # C subset C^perp: every trade word orthogonal to every context word
    checks["trade_inside_context_dual"] = bool(
        ((c_matrix @ incidence.T) % 2 == 0).all()
    )
    # C^perp of the trade code IS the context code: dims 15 + 25 = 40 and
    # orthogonality, so it suffices that C^perp contains D and dims match
    checks["dual_dimensions_match"] = len(c_rows) + len(d_rows) == 40

    # C inside D (as codes): each trade word is a sum of context rows?
    # No -- the containment is C subset C^perp = D' where D' is the DUAL
    # of C; the context code equals that dual by dimension + orthogonality.
    # The quotient H = C^perp / C is computed inside the context code
    # coordinates only if C subset context code; verify directly:
    def in_code(word, code_rref, code_pivots):
        residual = word.copy()
        for r, p in zip(code_rref, code_pivots):
            if residual[p]:
                residual = residual ^ r
        return not residual.any()

    checks["trade_words_in_context_code"] = all(
        in_code(c_matrix[i], d_rows, d_pivots) for i in range(15)
    )

    # quotient coordinates: express D-codewords by their pivot values,
    # reduce modulo the image of C, keep the 10 free coordinates
    def d_coords(word):
        return word[d_pivots]

    c_in_d = np.array([d_coords(c_matrix[i]) for i in range(15)], dtype=np.uint8)
    u_rows, u_pivots = rref_f2([r for r in c_in_d])
    checks["c_image_dim_15"] = len(u_rows) == 15
    free_positions = [i for i in range(25) if i not in u_pivots]
    checks["quotient_dim_10"] = len(free_positions) == 10

    def quotient_coords(word25):
        residual = word25.copy()
        for r, p in zip(u_rows, u_pivots):
            if residual[p]:
                residual = residual ^ r
        return residual[free_positions]

    # section: quotient coords -> a codeword of D
    basis_h = []
    for k in range(10):
        coords25 = np.zeros(25, dtype=np.uint8)
        coords25[free_positions[k]] = 1
        word = (coords25 @ d_matrix) % 2
        basis_h.append(word.astype(np.uint8))
    basis_h = np.array(basis_h, dtype=np.uint8)

    # q(x) = wt(x)/2 mod 2 on all 1024 quotient classes
    coeffs = np.array(
        [[(m >> b) & 1 for b in range(10)] for m in range(1024)], dtype=np.uint8
    )
    words = (coeffs @ basis_h) % 2
    weights = words.sum(axis=1)
    checks["all_context_weights_even"] = bool((weights % 2 == 0).all())
    q_values = (weights // 2) % 2
    zeros = int((q_values == 0).sum())
    form_type = "plus" if zeros == 528 else ("minus" if zeros == 496 else "??")
    checks["form_type_decided"] = form_type in ("plus", "minus")

    # nondegeneracy of the polar form b(x,y) = |x cap y| mod 2 on H
    gram_b = np.zeros((10, 10), dtype=np.uint8)
    for i in range(10):
        for j in range(10):
            gram_b[i, j] = int((basis_h[i] & basis_h[j]).sum()) % 2
    rank_b = len(rref_f2([gram_b[i] for i in range(10)])[0])
    checks["polar_form_nondegenerate"] = rank_b == 10

    # q(x+y) = q(x) + q(y) + b(x,y) sanity on the basis
    quad_ok = True
    for i in range(10):
        for j in range(10):
            x, y = basis_h[i], basis_h[j]
            s = (x ^ y).sum()
            lhs = (int(s) // 2) % 2
            rhs = (
                (int(x.sum()) // 2) % 2
                + (int(y.sum()) // 2) % 2
                + int((x & y).sum()) % 2
            ) % 2
            if lhs != rhs:
                quad_ok = False
    checks["quadratic_refinement_law"] = bool(quad_ok)

    # ------------------------------------------------------------------
    # the group action on H
    # ------------------------------------------------------------------
    generators, group = build_group(points, symplectic)
    checks["group_order_25920"] = len(group) == 25920
    two_gens = small_generating_set(group)

    def act_on_h(perm):
        """10x10 F2 matrix of the action of perm on H."""
        rows = []
        for k in range(10):
            image = np.zeros(40, dtype=np.uint8)
            for src in range(40):
                image[perm[src]] = basis_h[k][src]
            rows.append(quotient_coords(d_coords(image)))
        return np.array(rows, dtype=np.uint8)

    action_matrices = [act_on_h(g) for g in two_gens]

    # weight preservation implies q-preservation; verify explicitly on H
    q_preserved = True
    for matrix in action_matrices:
        images = (coeffs @ matrix) % 2
        image_words = (images @ basis_h) % 2
        image_q = (image_words.sum(axis=1) // 2) % 2
        if not (image_q == q_values).all():
            q_preserved = False
    checks["action_preserves_q"] = bool(q_preserved)

    # faithfulness: BFS closure of the two 10x10 matrices over F2
    def mat_key(m):
        return tuple(int(v) for v in m.reshape(-1))

    seen = {mat_key(np.eye(10, dtype=np.uint8))}
    frontier = [np.eye(10, dtype=np.uint8)]
    while frontier:
        new_frontier = []
        for element in frontier:
            for gen in action_matrices:
                composed = (element @ gen) % 2
                key = mat_key(composed)
                if key not in seen:
                    seen.add(key)
                    new_frontier.append(composed)
        frontier = new_frontier
    checks["action_faithful_25920"] = len(seen) == 25920

    # submodule structure over F2: cyclic-submodule dimension of every
    # nonzero vector, the distinct proper invariant submodules, and the
    # restriction of q to each
    def cyclic_submodule(start_vec):
        orbit = {tuple(int(v) for v in start_vec)}
        stack = [start_vec]
        basis_rows = []
        while stack:
            current = stack.pop()
            candidate = basis_rows + [current]
            if len(rref_f2(candidate)[0]) == len(candidate):
                basis_rows.append(current)
            for gen in action_matrices:
                image = (current @ gen) % 2
                key = tuple(int(v) for v in image)
                if key not in orbit:
                    orbit.add(key)
                    stack.append(image)
        reduced, _ = rref_f2(basis_rows)
        return reduced

    dim_profile = Counter()
    proper_submodules = {}
    for m in range(1, 1024):
        sub = cyclic_submodule(coeffs[m].copy())
        dim_profile[len(sub)] += 1
        if len(sub) < 10:
            key = tuple(sorted(tuple(int(v) for v in row) for row in sub))
            proper_submodules[key] = sub
    irreducible = len(proper_submodules) == 0
    checks["module_structure_recorded"] = len(dim_profile) > 0

    submodule_reports = []
    for key, sub in proper_submodules.items():
        sub_matrix = np.array(sub, dtype=np.uint8)
        n_sub = len(sub)
        sub_coeffs = np.array(
            [[(m >> b) & 1 for b in range(n_sub)] for m in range(2**n_sub)],
            dtype=np.uint8,
        )
        sub_vectors = (sub_coeffs @ sub_matrix) % 2
        sub_words = (sub_vectors @ basis_h) % 2
        sub_q = (sub_words.sum(axis=1) // 2) % 2
        submodule_reports.append(
            {
                "dimension": n_sub,
                "q_zero_count": int((sub_q == 0).sum()),
                "totally_isotropic": bool((sub_q == 0).all()),
            }
        )
    submodule_reports.sort(key=lambda r: r["dimension"])

    all_pass = all(checks.values())
    payload = {
        "schema": "w33.pass164.so10_shadow_quotient_form.v1",
        "status": "PASS" if all_pass else "FAIL",
        "tower": {
            "adjacency_tower": "ker(A)/im(A) = F2^8, plus type -> E8 (known)",
            "incidence_tower": "C^perp/C = F2^10 with q = wt/2 mod 2",
            "trade_code": "[40,15,8] doubly even",
            "context_code": "[40,25] = dual of the trade code",
        },
        "quotient_form": {
            "dimension": 10,
            "isotropic_vectors": zeros,
            "anisotropic_vectors": 1024 - zeros,
            "type": form_type,
            "reading": (
                "plus type (528 zeros) is O+(10,2), the D5 = SO(10) GUT "
                "shadow; minus type (496 zeros) is O-(10,2), with 496 = "
                "dim SO(32) = dim E8xE8 the anomaly-free dimension"
            ),
        },
        "group_action": {
            "embedding": f"PSp(4,3) -> O_{form_type}(10,2)",
            "faithful": bool(checks["action_faithful_25920"]),
            "irreducible_over_F2": bool(irreducible),
            "cyclic_submodule_dimension_profile": {
                str(k): int(v) for k, v in sorted(dim_profile.items())
            },
            "proper_invariant_submodules": submodule_reports,
        },
        "checks": {name: bool(value) for name, value in checks.items()},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
