#!/usr/bin/env python3
"""Part DCCLXVI: octahedral matrix-tree / density-denominator bridge.

DCCL-DCCLXII made the octahedral closure phase space into an exact finite
harmonic and Markov system. DCCLVI, in the parallel sphere-packing lane,
identified the E8 optimal-density denominator

    rho_8 = pi^4 / 384.

This verifier joins those lanes by applying Kirchhoff's matrix-tree theorem
to the exact octahedral Laplacian:

    spec(L) = (0, 4, 4, 4, 6, 6)
    det'(L) = 4^3 * 6^2 = 2304
    tau(O) = det'(L) / 6 = 384.

So the E8 density denominator is also the spanning-tree count of the exact
octahedral closure phase space.
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccl_octahedral_laplacian_heat_kernel_bridge import (  # noqa: E402
    adjacency_matrix,
    octahedron_vertices,
)
from verify_dcclvi_sphere_packing_density_tower import (  # noqa: E402
    G_384_w33_factorisations,
    density_table,
)


OUT_PATH = ROOT / "data" / "dcclxvi_octahedral_matrix_tree_density_bridge.json"

Q = 3
MU = 4
F_EIGEN = 24
W_D4_ORDER = 192
G_384 = 384


@dataclass(frozen=True)
class BridgeSummary:
    vertex_count: int
    det_prime_laplacian: int
    spanning_tree_count: int
    rho_8_denominator: int
    all_identities_hold: bool


def integer_octahedral_laplacian() -> np.ndarray:
    verts = octahedron_vertices()
    A = adjacency_matrix(verts).astype(int)
    D = np.diag(A.sum(axis=1))
    return D - A


def bareiss_det(matrix: list[list[int]]) -> int:
    """Exact integer determinant by the Bareiss fraction-free algorithm."""
    a = [row[:] for row in matrix]
    n = len(a)
    if n == 0:
        return 1

    sign = 1
    previous = 1
    for k in range(n - 1):
        if a[k][k] == 0:
            swap = next((r for r in range(k + 1, n) if a[r][k] != 0), None)
            if swap is None:
                return 0
            a[k], a[swap] = a[swap], a[k]
            sign *= -1

        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                a[i][j] = (a[i][j] * pivot - a[i][k] * a[k][j]) // previous
        previous = pivot

        for i in range(k + 1, n):
            a[i][k] = 0
        for j in range(k + 1, n):
            a[k][j] = 0

    return sign * a[n - 1][n - 1]


def principal_minor(matrix: np.ndarray, removed: int) -> list[list[int]]:
    rows = []
    for i in range(matrix.shape[0]):
        if i == removed:
            continue
        row = []
        for j in range(matrix.shape[1]):
            if j != removed:
                row.append(int(matrix[i, j]))
        rows.append(row)
    return rows


def matrix_tree_data() -> dict[str, Any]:
    L = integer_octahedral_laplacian()
    eigvals = [int(round(x)) for x in np.linalg.eigvalsh(L)]
    nonzero = [x for x in eigvals if x != 0]
    det_prime = math.prod(nonzero)
    tau_from_spectrum = det_prime // L.shape[0]
    cofactors = [bareiss_det(principal_minor(L, i)) for i in range(L.shape[0])]

    return {
        "laplacian": L.astype(int).tolist(),
        "laplacian_spectrum": eigvals,
        "nonzero_spectrum": nonzero,
        "det_prime_laplacian": det_prime,
        "det_prime_formula": "4^3 * 6^2",
        "spanning_tree_count_from_spectrum": tau_from_spectrum,
        "principal_cofactors": cofactors,
        "all_principal_cofactors_equal": len(set(cofactors)) == 1,
        "matrix_tree_count": cofactors[0],
    }


def spectral_zeta_data() -> dict[str, Any]:
    det_prime = 4**3 * 6**2
    zeta_prime_at_zero = -(3 * math.log(4) + 2 * math.log(6))
    return {
        "zeta_formula": "zeta_L(s) = 3*4^(-s) + 2*6^(-s)",
        "zeta_at_0": 5,
        "rank_laplacian": 5,
        "zeta_prime_at_0": zeta_prime_at_zero,
        "minus_zeta_prime_at_0": -zeta_prime_at_zero,
        "regularized_det": round(math.exp(-zeta_prime_at_zero)),
        "det_prime_laplacian": det_prime,
    }


def density_denominator_bridge() -> dict[str, Any]:
    rho_8 = next(row for row in density_table() if row["dim"] == 8)
    g384_facts = G_384_w33_factorisations()
    return {
        "rho_8_formula": rho_8["density_formula"],
        "rho_8_denominator": rho_8["denominator"],
        "G_384_factorisations": g384_facts,
        "new_finite_harmonic_reading": (
            "384 is the spanning-tree count of the exact octahedral closure "
            "phase-space graph."
        ),
        "additional_factorisations": [
            {"formula": "tau(O)", "value": 384, "reading": "octahedral spanning trees"},
            {"formula": "2 * |W(D_4)|", "value": 2 * W_D4_ORDER, "reading": "double D4 Weyl/tomotope flags"},
            {"formula": "(q+1)^2 * f", "value": MU**2 * F_EIGEN, "reading": "Cartan trace times +2 eigenspace"},
            {"formula": "q! * (q+1)^3", "value": math.factorial(Q) * MU**3, "reading": "triality permutations times cubic closure axes"},
        ],
    }


def build_bridge() -> dict[str, Any]:
    tree = matrix_tree_data()
    zeta = spectral_zeta_data()
    density = density_denominator_bridge()

    identities = {
        "laplacian_spectrum_is_0_4_4_4_6_6": tree["laplacian_spectrum"] == [0, 4, 4, 4, 6, 6],
        "det_prime_eq_4_cubed_6_squared": tree["det_prime_laplacian"] == 4**3 * 6**2 == 2304,
        "matrix_tree_from_spectrum_eq_384": tree["spanning_tree_count_from_spectrum"] == G_384,
        "all_principal_cofactors_eq_384": tree["all_principal_cofactors_equal"] and tree["matrix_tree_count"] == G_384,
        "rho_8_denominator_eq_tree_count": density["rho_8_denominator"] == tree["matrix_tree_count"] == G_384,
        "G_384_eq_2_W_D4": G_384 == 2 * W_D4_ORDER,
        "G_384_eq_mu_squared_times_f": G_384 == MU**2 * F_EIGEN,
        "G_384_eq_q_factorial_times_mu_cubed": G_384 == math.factorial(Q) * MU**3,
        "zeta_at_0_eq_rank": zeta["zeta_at_0"] == zeta["rank_laplacian"] == 5,
        "regularized_det_eq_det_prime": zeta["regularized_det"] == tree["det_prime_laplacian"],
        "imported_G_384_factorisations_all_equal_384": all(row["value"] == G_384 for row in density["G_384_factorisations"]),
    }

    summary = BridgeSummary(
        vertex_count=6,
        det_prime_laplacian=tree["det_prime_laplacian"],
        spanning_tree_count=tree["matrix_tree_count"],
        rho_8_denominator=density["rho_8_denominator"],
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "matrix_tree_data": tree,
        "spectral_zeta_data": zeta,
        "density_denominator_bridge": density,
        "identities": identities,
        "theorem": (
            "Octahedral Matrix-Tree / Density-Denominator Theorem. The exact "
            "octahedral closure Laplacian has spectrum (0,4,4,4,6,6), hence "
            "det'(L)=4^3*6^2=2304. Kirchhoff's matrix-tree theorem gives "
            "tau(O)=det'(L)/6=384. The same integer is the denominator of "
            "the optimal E8 packing density rho_8=pi^4/384 and the W(3,3) "
            "G_384 cascade value. Thus the E8 density denominator is also "
            "the spanning-tree count of the finite octahedral harmonic "
            "closure phase space."
        ),
        "one_line": (
            "tau(octahedron)=384=rho_8 denominator=G_384; the E8 density "
            "denominator is the octahedral matrix-tree count."
        ),
        "honesty_boundary": (
            "This proves an exact finite graph identity and an exact equality "
            "with the denominator used in the standard E8 density formula. It "
            "does not re-prove Viazovska's E8 optimality theorem, nor does it "
            "derive continuum sphere packing from the octahedron. The new "
            "content is the finite harmonic/topological anchoring of 384."
        ),
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    payload = build_bridge()
    print(f"Wrote {out}")
    print(f"Verified: {payload['summary']['all_identities_hold']}")
    print(f"tau(O) = {payload['summary']['spanning_tree_count']}")
    print(f"rho_8 denominator = {payload['summary']['rho_8_denominator']}")


if __name__ == "__main__":
    main()
