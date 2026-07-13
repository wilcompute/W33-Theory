#!/usr/bin/env python3
"""Pass 204: the orthogonal action on one sentinel logical-label copy.

Pass 201 showed PSp(4,3) permutes the 40 physical coordinates of the CSS
code [[40,10,4]], acting on H=C^perp/C through O+(10,2).  H is one
10-dimensional X/Z label copy, not the full logical Pauli space.  This
witness certifies only that label action:

1. THE ORTHOGONAL LABEL ACTION.  Each physical permutation induces a
   10x10 matrix M on H that preserves q(x)=wt/2 mod 2 and its polar form.
   The image lies in O+(10,2) subset Sp(10,2) and has order 25920, hence
   is the PSp(4,3) image.  Sp(10,2) here is an ambient group for H, not
   the full logical Clifford quotient.

2. THE AMBIENT LABEL GROUPS.  |Sp(10,2)| and |O+(10,2)| and the image
   index are computed exactly.  These counts do not establish a gate
   inventory, universality boundary, or an E6 implementation.

3. THE CORRECTED CLIFFORD LIFT.  After choosing the dot-product dual Z
   basis, the full action is diag(M,M^(-T)) in Sp(20,2), as certified by
   GAP in Pass 211.  The order distribution below is only the abstract
   PSp image census; its 315 involutions are not a CZ census.
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
from analysis.w33_pass201_sentinel_css_logical_shadow import (
    in_span,
    rref_f2,
)

OUT = ROOT / "data" / "w33_pass204_transversal_clifford.json"


def sp_order(m):
    """|Sp(2m, 2)| = 2^{m^2} prod_{i=1}^m (2^{2i} - 1)."""
    order = 2 ** (m * m)
    for i in range(1, m + 1):
        order *= (2 ** (2 * i)) - 1
    return order


def o_plus_order(m):
    """|O^+(2m, 2)| = 2 * 2^{m(m-1)} (2^m - 1) prod_{i=1}^{m-1}(2^{2i}-1)."""
    order = 2 * 2 ** (m * (m - 1)) * ((2**m) - 1)
    for i in range(1, m):
        order *= (2 ** (2 * i)) - 1
    return order


def main():
    points, adjacency, symplectic = build_w33()
    lines = w33_lines(adjacency)
    checks = {}

    incidence = np.zeros((40, 40), dtype=np.uint8)
    for row, line in enumerate(lines):
        for p in line:
            incidence[row, p] = 1
    dark = saturated_kernel(incidence.astype(np.int64))
    C = rref_f2([(dark[:, j] % 2).astype(np.uint8) for j in range(15)])
    Cperp = rref_f2([incidence[r] for r in range(40)])

    def reduce_mod_C(vec):
        r = vec.copy()
        for b in C:
            piv = int(np.flatnonzero(b)[0])
            if r[piv]:
                r = r ^ b
        return r

    Cperp_mat = np.array(Cperp, dtype=np.uint8)
    H = rref_f2([reduce_mod_C(Cperp_mat[i]) for i in range(25)])
    dim = len(H)
    checks["logical_dim_10"] = dim == 10
    Hmat = np.array(H, dtype=np.uint8)
    pivots = [int(np.flatnonzero(b)[0]) for b in H]

    # quadratic form q and polar form B on the logical space
    qvec = np.array([(int(H[i].sum()) // 2) % 2 for i in range(dim)], dtype=np.uint8)
    B = np.zeros((dim, dim), dtype=np.uint8)
    for i in range(dim):
        for k in range(dim):
            B[i, k] = int((H[i] & H[k]).sum()) % 2

    def logical_coords(vec):
        r = reduce_mod_C(vec)
        out = np.zeros(dim, dtype=np.uint8)
        for k in range(dim):
            if r[pivots[k]]:
                out[k] = 1
                r = r ^ H[k]
        return out

    generators, group = build_group(points, symplectic)
    checks["group_25920"] = len(group) == 25920
    two_gens = small_generating_set(group)

    def logical_action(perm):
        cols = []
        for b in H:
            image = np.zeros(40, dtype=np.uint8)
            for src in range(40):
                image[perm[src]] = b[src]
            cols.append(logical_coords(image))
        return np.array(cols, dtype=np.uint8).T % 2

    Lgens = [logical_action(g) for g in two_gens]

    # --- verify the one-copy label action is polar-preserving and orthogonal ---
    def preserves_B(M):
        return np.array_equal((M.T @ B @ M) % 2, B % 2)

    def preserves_q(M):
        # q(Mx) = q(x) for all x: check on basis + cross terms via
        # q(Mx) = qvec . (coords of Mx in H-weight) -- use weight parity
        for i in range(dim):
            col = M[:, i]
            # weight of the H-combination given by col
            w = int((col @ Hmat % 2).sum())
            if (w // 2) % 2 != int(qvec[i]):
                return False
        return True

    checks["generators_preserve_polar_form"] = all(preserves_B(M) for M in Lgens)
    checks["generators_in_O_plus_10_2"] = all(
        preserves_B(M) and preserves_q(M) for M in Lgens
    )

    # --- closure and image order ---
    def key(M):
        return tuple(int(v) for v in M.reshape(-1))

    identity = np.eye(dim, dtype=np.uint8)
    seen = {key(identity): identity}
    frontier = [identity]
    while frontier:
        nf = []
        for e in frontier:
            for g in Lgens:
                comp = (e @ g) % 2
                k = key(comp)
                if k not in seen:
                    seen[k] = comp
                    nf.append(comp)
        frontier = nf
    image = list(seen.values())
    checks["transversal_image_25920"] = len(image) == 25920

    # every image element is in O+(10,2)
    checks["whole_image_in_O_plus"] = all(
        preserves_B(M) and preserves_q(M) for M in image
    )

    # --- ambient groups for the one-copy polar form ---
    sp10 = sp_order(5)
    op10 = o_plus_order(5)
    checks["image_divides_O_plus"] = op10 % 25920 == 0
    checks["O_plus_subset_Sp"] = sp10 % op10 == 0
    index_in_O = op10 // 25920

    # --- abstract order census of the PSp image (not a gate inventory) ---
    def mat_order(M):
        o = 1
        cur = M.copy()
        while not np.array_equal(cur, identity):
            cur = (cur @ M) % 2
            o += 1
        return o

    order_dist = Counter(mat_order(M) for M in image)
    involutions = order_dist.get(2, 0)
    checks["order_census_recorded"] = sum(order_dist.values()) == 25920

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass204.transversal_clifford.v2",
        "status": "PASS" if all_pass else "FAIL",
        "label_action": {
            "group": "PSp(4,3) -> O+(10,2) subset Sp(10,2)",
            "image_order": 25920,
            "is_orthogonal": True,
            "full_logical_pauli_dimension": 20,
            "corrected_clifford_lift": "diag(M,M^(-T)) in Sp(20,2) (Pass 211)",
            "reading": (
                "the 10x10 matrices act on one logical-label copy only; "
                "they are not by themselves full Clifford matrices"
            ),
        },
        "ambient_label_groups": {
            "Sp_10_2_order_on_H": sp10,
            "O_plus_10_2_order_on_H": op10,
            "PSp_image_order": 25920,
            "index_in_O_plus": index_in_O,
            "reading": (
                "these are ambient counts for the one-copy label form; "
                "they do not establish a gate inventory or universality claim"
            ),
        },
        "image_order_census": {
            "element_order_distribution": {
                str(k): int(v) for k, v in sorted(order_dist.items())
            },
            "involutions_not_CZ_gates": involutions,
        },
        "checks": {name: bool(v) for name, v in checks.items() if isinstance(v, bool)},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
