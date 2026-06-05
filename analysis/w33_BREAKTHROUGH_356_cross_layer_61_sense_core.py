#!/usr/bin/env python3
"""BT356: the cross-layer 61-core theorem.

BT354/355 separated two edge-carrier Hamiltonian layers on W(3,3):

  * canonical oriented clique-chain CSS: [[240,81,3]]_3
  * all-plus vertex/line Hamiltonian:    [[240,160,2]]_3

This verifier computes their shared Z-logical carrier:

    K = ker(d1) ∩ ker(Hx_plus)  inside F_3^240.

The surprise is that this shared carrier is not the full 81-dimensional
homology sector.  After quotienting by the stabilizers from both layers that
remain in K, the common core has dimension

    61 = 165 - 104 = 81 - 20 = 64 - 3.

So the same finite calculation links three previously separate dictionaries:

  * QEC/spacetime: common code core of the two Hamiltonian layers;
  * W33 homology: 81 protected H_1 modes minus a 20-state readout alphabet;
  * genetic code: 64 codons minus q=3 stop codons = 61 sense codons.

This is an exact finite-structure result.  It does not claim that biology is
derived from the code by itself; it identifies the same rank that the later
biology bridge must explain.
"""
from __future__ import annotations

import json
import sys
from itertools import combinations
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_css_exact_audit import P, boundary_matrices, build_w33, gf_nullspace, gf_rank


Q = 3
LAMBDA = 2
MU = 4
F5 = 5
PHI3 = Q * Q + Q + 1      # 13
PHI4 = Q * Q + 1          # 10
PHI6 = Q * Q - Q + 1      # 7
P_IH = 11
G_NEG = 15
H1 = Q ** MU              # 81
AMINO = LAMBDA * PHI4     # 20
CODONS = MU ** Q          # 64
SENSE = CODONS - Q        # 61


def all_plus_line_matrices(points, edges, edge_index, lines) -> tuple[np.ndarray, np.ndarray]:
    hx = np.zeros((len(points), len(edges)), dtype=int)
    for col, (i, j) in enumerate(edges):
        hx[i, col] = 1
        hx[j, col] = 1

    hz = np.zeros((len(lines), len(edges)), dtype=int)
    for row, line in enumerate(lines):
        for i, j in combinations(line, 2):
            hz[row, edge_index[tuple(sorted((i, j)))]] = 1

    return hx % P, hz % P


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def subspace_in_kernel_rank(generator_columns: np.ndarray, constraint_rows: np.ndarray) -> int:
    """Dimension of im(generator_columns) ∩ ker(constraint_rows)."""

    return gf_rank(generator_columns) - gf_rank((constraint_rows @ generator_columns) % P)


def basis_in_kernel(generator_columns: np.ndarray, constraint_rows: np.ndarray) -> np.ndarray:
    """Return row vectors spanning im(generator_columns) ∩ ker(constraint_rows)."""

    coeff_basis = gf_nullspace((constraint_rows @ generator_columns) % P)
    if coeff_basis.size == 0:
        return np.zeros((0, generator_columns.shape[0]), dtype=int)
    return (coeff_basis @ generator_columns.T) % P


def build_payload() -> dict[str, Any]:
    points, edges, edge_index, lines, triangles = build_w33()
    d1, d2 = boundary_matrices(points, edges, edge_index, triangles)
    hx_plus, hz_line = all_plus_line_matrices(points, edges, edge_index, lines)

    common_constraints = np.vstack([d1, hx_plus]) % P
    common_kernel_dim = len(edges) - gf_rank(common_constraints)

    canonical_boundary_cols = d2 % P
    line_stabilizer_cols = hz_line.T % P
    shared_stabilizer_cols = np.column_stack([canonical_boundary_cols, line_stabilizer_cols]) % P

    canonical_boundary_in_common = subspace_in_kernel_rank(canonical_boundary_cols, common_constraints)
    line_stabilizer_in_common = subspace_in_kernel_rank(line_stabilizer_cols, common_constraints)
    shared_stabilizers_in_common = subspace_in_kernel_rank(shared_stabilizer_cols, common_constraints)
    shared_core = common_kernel_dim - shared_stabilizers_in_common

    # Independent basis-rank check for the same stabilizer dimensions.
    b_can = basis_in_kernel(canonical_boundary_cols, common_constraints)
    b_line = basis_in_kernel(line_stabilizer_cols, common_constraints)
    b_shared = basis_in_kernel(shared_stabilizer_cols, common_constraints)

    canonical_only_common_quotient = common_kernel_dim - canonical_boundary_in_common
    line_only_common_quotient = common_kernel_dim - line_stabilizer_in_common

    identities = {
        "w33_counts": len(points) == 40 and len(edges) == 240 and len(lines) == 40 and len(triangles) == 160,
        "common_kernel_rank": gf_rank(common_constraints) == 75,
        "common_kernel_dim": common_kernel_dim == 165 == G_NEG * P_IH,
        "canonical_boundary_in_common": canonical_boundary_in_common == 88 == (2 ** Q) * P_IH,
        "line_stabilizer_in_common": line_stabilizer_in_common == 16 == 2 ** MU,
        "shared_stabilizers_in_common": shared_stabilizers_in_common == 104 == (2 ** Q) * PHI3,
        "basis_rank_cross_check": (
            gf_rank(b_can) == canonical_boundary_in_common
            and gf_rank(b_line) == line_stabilizer_in_common
            and gf_rank(b_shared) == shared_stabilizers_in_common
        ),
        "canonical_only_common_quotient": canonical_only_common_quotient == 77 == PHI6 * P_IH,
        "shared_core_61": shared_core == 61,
        "shared_core_prime": is_prime(shared_core),
        "shared_core_as_H1_minus_amino": shared_core == H1 - AMINO,
        "shared_core_as_sense_codons": shared_core == CODONS - Q == SENSE,
        "shared_core_as_substrate_indexed_prime": shared_core == 40 + P_IH + PHI4,
        "shared_core_as_centered_hexagonal_H5": shared_core == 3 * 4 * 5 + 1,
    }

    theorem = (
        "Cross-layer 61-Core Theorem.  Let K=ker(d1)∩ker(Hx_plus) in the "
        "240-edge F_3 carrier.  Then dim K=165=15*11.  The triangle-boundary "
        "stabilizers contribute 88=2^3*11 dimensions inside K, the line "
        "stabilizers contribute 16=2^4, and together they contribute "
        "104=2^3*13.  The shared logical quotient therefore has dimension "
        "61.  Equivalently, 61=q^mu-lambda*Phi4=81-20 and also "
        "61=mu^q-q=64-3, the sense-codon count.  Thus the overlap of the "
        "homological physics layer and the all-plus line/readout layer is a "
        "prime core whose size is the same finite rank used by the genetic-code "
        "dictionary."
    )

    return {
        "summary": {
            "common_kernel_dim": common_kernel_dim,
            "shared_stabilizers_in_common": shared_stabilizers_in_common,
            "shared_core": shared_core,
            "shared_core_formulas": [
                "165 - 104",
                "81 - 20",
                "64 - 3",
                "40 + 11 + 10",
            ],
            "all_identities_hold": all(identities.values()),
        },
        "input_layers": {
            "canonical": {
                "constraints": "d1 cycles modulo d2 triangle boundaries",
                "code": "[[240,81,3]]_3",
                "H1": H1,
            },
            "line_hamiltonian": {
                "constraints": "all-plus vertex stars modulo all-plus K4 line checks",
                "code": "[[240,160,2]]_3",
            },
        },
        "rank_ledger": {
            "rank_common_constraints": gf_rank(common_constraints),
            "common_kernel_dim": common_kernel_dim,
            "canonical_boundary_in_common": canonical_boundary_in_common,
            "line_stabilizer_in_common": line_stabilizer_in_common,
            "shared_stabilizers_in_common": shared_stabilizers_in_common,
            "canonical_only_common_quotient": canonical_only_common_quotient,
            "line_only_common_quotient": line_only_common_quotient,
            "shared_core": shared_core,
        },
        "closed_forms": {
            "common_kernel_dim": "165 = g_neg * p_Ih = 15 * 11",
            "canonical_boundary_in_common": "88 = 2^q * p_Ih = 8 * 11",
            "line_stabilizer_in_common": "16 = 2^mu",
            "shared_stabilizers_in_common": "104 = 2^q * Phi3 = 8 * 13",
            "canonical_only_common_quotient": "77 = Phi6 * p_Ih = 7 * 11",
            "shared_core": "61 = q^mu - lambda*Phi4 = mu^q - q",
        },
        "biology_bridge": {
            "codons": CODONS,
            "stop_codons": Q,
            "sense_codons": SENSE,
            "amino_readout_alphabet": AMINO,
            "formula": "shared_core = 64 - 3 = 81 - 20",
            "interpretation": (
                "The common Hamiltonian core has the same count as sense codons. "
                "The 20-dimensional complement to H1 is the amino/dodecahedral "
                "readout alphabet used elsewhere in the repo."
            ),
        },
        "identities": identities,
        "theorem": theorem,
        "honesty_boundary": (
            "This proves finite F_3 rank identities for the two W33 edge "
            "Hamiltonian layers.  The genetic-code interpretation is a finite "
            "dictionary bridge, not a biochemical derivation."
        ),
    }


def main() -> int:
    payload = build_payload()
    out = Path("data/w33_BREAKTHROUGH_356_cross_layer_61_sense_core.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"wrote {out}")
    return 0 if payload["summary"]["all_identities_hold"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
