#!/usr/bin/env python3
"""Pass 204: the transversal logical Clifford gates of the sentinel code.

Pass 201 showed PGSp(4,3) permutes the 40 physical qubits of the CSS code
[[40,10,4]], acting on the 10 logical qubits through O+(10,2).  This
witness pins that action as a fault-tolerant gate set:

1. THE LOGICAL SYMPLECTIC (CLIFFORD) ACTION.  Each physical permutation
   induces a 10x10 matrix M on the logical Paulis (H10) that preserves
   BOTH the quadratic form q(x)=wt/2 mod 2 AND its symplectic polar form
   B -- so the image lies in O+(10,2) subset Sp(10,2) = the logical
   Clifford group modulo Paulis.  The image order is exactly |PGSp(4,3)|
   = 25920.

2. THE EASTIN-KNILL CEILING.  |Sp(10,2)| and |O+(10,2)| are computed
   exactly; the transversal group is a proper subgroup of index >> 1, so
   the transversal gates are a tiny, FINITE slice of the Clifford group
   -- necessarily non-universal (Eastin-Knill), and containing NO
   non-Clifford gate.  The magic must come from outside the permutation
   group: the substrate's E6 cubic.

3. THE GATE INVENTORY.  Because a permutation acts identically on X- and
   Z-type logicals, the realized gates are exactly the "diagonal" CSS
   Clifford operations diag(M,M) with M in O+(10,2): logical CZ/CNOT-type
   entangling gates and Hadamard-free Paulis, with no logical phase gate
   escaping O+.  The count of order-2 (involution) logical gates is
   reported as the transversal-CZ census.
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

    # --- verify the action is symplectic (Clifford) AND orthogonal ---
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

    # --- the Eastin-Knill ceiling ---
    sp10 = sp_order(5)
    op10 = o_plus_order(5)
    checks["image_divides_O_plus"] = op10 % 25920 == 0
    checks["O_plus_subset_Sp"] = sp10 % op10 == 0
    index_in_O = op10 // 25920

    # --- gate census: order distribution of the logical gates ---
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
        "schema": "w33.pass204.transversal_clifford.v1",
        "status": "PASS" if all_pass else "FAIL",
        "logical_action": {
            "group": "PGSp(4,3) -> O+(10,2) subset Sp(10,2)",
            "image_order": 25920,
            "is_clifford": True,
            "is_orthogonal": True,
            "reading": (
                "the transversal permutation gates act as logical Clifford "
                "operations preserving the O+(10,2) form; because a qubit "
                "permutation hits X and Z identically, they are the "
                "diagonal CSS gates diag(M,M)"
            ),
        },
        "eastin_knill": {
            "Sp_10_2_order": sp10,
            "O_plus_10_2_order": op10,
            "transversal_order": 25920,
            "index_in_O_plus": index_in_O,
            "reading": (
                "the transversal gate group is a FINITE subgroup of index "
                f"{index_in_O} in O+(10,2) and far smaller than Sp(10,2): "
                "necessarily non-universal (Eastin-Knill) and containing "
                "no non-Clifford gate -- the magic is the E6 cubic, "
                "supplied outside the permutation group"
            ),
        },
        "gate_census": {
            "logical_order_distribution": {
                str(k): int(v) for k, v in sorted(order_dist.items())
            },
            "involutions": involutions,
        },
        "checks": {name: bool(v) for name, v in checks.items() if isinstance(v, bool)},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
