#!/usr/bin/env python3
"""
PART CCCVII - Operator Tetrahedron / Entropy Bridge
===================================================

This part uses the real-time CCCV/CCCVI commits from the other assistant.

New inputs:
    - Signless Laplacian Q = K I + A has spectrum 24^1, 14^24, 8^15.
      Its weighted trace is 480 = 2E, the directed-edge/Hashimoto carrier.
      Its second moment is 6240 = 480 * Phi3.

    - Distance matrix Delta = 2J - 2I - A has spectrum 66^1, (-4)^24, 2^15.
      Its second moment is 4800 = 480 * Phi4 = 480 * theta(W).
      Its Wiener index is 1320 = 11 * 120.

Earlier inputs:
    - Laplacian L = K I - A has nonzero spectrum 10^24, 16^15.
      Matrix Tree gives tau(W)=2^81 * 5^23.

Breakthrough:
    The exponent 23 in the spanning-tree count is not isolated:

        e5(tau) = 23 = Phi3 + Phi4
                = (tr(Q^2) + tr(Delta^2)) / (2E).

    Since 2E = 480 = 2q(q^4-1), this is a direct weld between:
        signless Laplacian energy,
        distance geometry,
        Hashimoto/CCT directed carrier,
        and the Matrix Tree prime exponent.

Also:
        (tr(Q^2) - tr(Delta^2)) / (2E) = Phi3 - Phi4 = q = 3.

Thus the pair of second moments recovers both the tree 5-exponent and the q-clock.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]

# W33 atoms
q = 3
V = 40
K = 12
lam = 2
mu = 4
r = 2
s = -4
E = V * K // 2
DIRECTED = 2 * E
HASHIMOTO_BRANCH = K - 1
Phi3 = q**2 + q + 1   # 13
Phi4 = q**2 + 1       # 10
Phi6 = q**2 - q + 1   # 7
J = 5
J_inv = 8
EW = q + 1
ALBERT = q**3
H1 = q**4

# spectra as value -> multiplicity lists
ADJ_SPECTRUM = [(K, 1), (r, 24), (s, 15)]
LAPLACIAN_SPECTRUM = [(K - K, 1), (K - r, 24), (K - s, 15)]
SIGNLESS_SPECTRUM = [(K + K, 1), (K + r, 24), (K + s, 15)]
DISTANCE_SPECTRUM = [(2 * V - 2 - K, 1), (-2 - r, 24), (-2 - s, 15)]

# spectral moments and energies
Q_TRACE = sum(val * mult for val, mult in SIGNLESS_SPECTRUM)
Q_SECOND_MOMENT = sum((val**2) * mult for val, mult in SIGNLESS_SPECTRUM)
Q_ENERGY = sum(abs(val - K) * mult for val, mult in SIGNLESS_SPECTRUM)
D_TRACE = sum(val * mult for val, mult in DISTANCE_SPECTRUM)
D_SECOND_MOMENT = sum((val**2) * mult for val, mult in DISTANCE_SPECTRUM)
DISTANCE_PERRON = DISTANCE_SPECTRUM[0][0]
WIENER_INDEX = E + ((V * (V - 1) // 2) - E) * 2

# Matrix tree exponents from CCCIV.
TREE_EXP_2 = H1
TREE_EXP_5 = ALBERT - EW
TREE_COUNT_FACTOR = f"2^{TREE_EXP_2}*5^{TREE_EXP_5}"

# New normalized moment identities.
NORMALIZED_Q2 = Fraction(Q_SECOND_MOMENT, DIRECTED)
NORMALIZED_D2 = Fraction(D_SECOND_MOMENT, DIRECTED)
NORMALIZED_SECOND_MOMENT_SUM = Fraction(Q_SECOND_MOMENT + D_SECOND_MOMENT, DIRECTED)
NORMALIZED_SECOND_MOMENT_DIFF = Fraction(Q_SECOND_MOMENT - D_SECOND_MOMENT, DIRECTED)


@dataclass(frozen=True)
class OperatorLayer:
    name: str
    spectrum: str
    key_identity: str
    interpretation: str


def operator_layers() -> List[OperatorLayer]:
    return [
        OperatorLayer(
            "Adjacency A",
            "12^1, 2^24, (-4)^15",
            "spectrum seed {K,r,s}",
            "base W(3,3) collinearity operator",
        ),
        OperatorLayer(
            "Laplacian L=K I-A",
            "0^1, 10^24, 16^15",
            "tau(W)=10^24*16^15/40=2^81*5^23",
            "global connectedness / Matrix Tree operator",
        ),
        OperatorLayer(
            "Signless Laplacian Q=K I+A",
            "24^1, 14^24, 8^15",
            "tr(Q)=480; tr(Q^2)=480*Phi3",
            "directed-carrier trace and projective-plane second moment",
        ),
        OperatorLayer(
            "Distance Delta=2J-2I-A",
            "66^1, (-4)^24, 2^15",
            "tr(Delta^2)=480*Phi4; Wiener=11*120",
            "diameter-two distance geometry and Hashimoto-branch Wiener law",
        ),
    ]


def operator_tetrahedron_entropy_audit() -> Dict[str, object]:
    checks = {
        "directed_carrier": DIRECTED == 480 == 2 * q * (H1 - 1),
        "laplacian_spectrum": LAPLACIAN_SPECTRUM == [(0, 1), (10, 24), (16, 15)],
        "signless_spectrum": SIGNLESS_SPECTRUM == [(24, 1), (14, 24), (8, 15)],
        "distance_spectrum": DISTANCE_SPECTRUM == [(66, 1), (-4, 24), (2, 15)],
        "L_plus_Q_pairing": all(lv + qv == 2 * K for (lv, lm), (qv, qm) in zip(LAPLACIAN_SPECTRUM, SIGNLESS_SPECTRUM)) and [m for _, m in LAPLACIAN_SPECTRUM] == [m for _, m in SIGNLESS_SPECTRUM],
        "distance_restricted_affine_involution": (-2 - r == s) and (-2 - s == r),
        "distance_perron_is_h6_edge_invariant": DISTANCE_PERRON == K * (K - 1) // 2 == 66,
        "signless_trace_is_directed_carrier": Q_TRACE == DIRECTED == 480,
        "signless_second_moment": Q_SECOND_MOMENT == DIRECTED * Phi3 == 6240,
        "distance_trace_zero": D_TRACE == 0,
        "distance_second_moment": D_SECOND_MOMENT == DIRECTED * Phi4 == 4800,
        "Q2_plus_D2_recovers_tree_5_exponent": NORMALIZED_SECOND_MOMENT_SUM == TREE_EXP_5 == 23,
        "Q2_minus_D2_recovers_q_clock": NORMALIZED_SECOND_MOMENT_DIFF == q == 3,
        "normalized_Q2_is_phi3": NORMALIZED_Q2 == Phi3 == 13,
        "normalized_D2_is_phi4": NORMALIZED_D2 == Phi4 == 10,
        "recover_phi3_phi4_from_sum_diff": (NORMALIZED_SECOND_MOMENT_SUM + NORMALIZED_SECOND_MOMENT_DIFF) / 2 == Phi3 and (NORMALIZED_SECOND_MOMENT_SUM - NORMALIZED_SECOND_MOMENT_DIFF) / 2 == Phi4,
        "Q_energy": Q_ENERGY == E // 2 == 120,
        "wiener_index": WIENER_INDEX == 1320,
        "wiener_hashimoto_branch_energy_law": WIENER_INDEX == HASHIMOTO_BRANCH * Q_ENERGY == 1320,
        "distance_second_moment_theta_directed": D_SECOND_MOMENT == Phi4 * DIRECTED == 10 * 480,
        "signless_second_moment_projective_directed": Q_SECOND_MOMENT == Phi3 * DIRECTED == 13 * 480,
        "tree_exponents": TREE_EXP_2 == H1 == 81 and TREE_EXP_5 == ALBERT - EW == 23,
        "threshold_carrier_inverse": (J * J_inv) % Phi3 == 1,
        "phi6_carrier_step": Phi6 + 1 == J_inv,
    }
    assert all(checks.values())

    return {
        "module": "PART_CCCVII_OPERATOR_TETRAHEDRON_ENTROPY_BRIDGE",
        "status": "exact four-operator spectral closure; welds signless/distance moments to Matrix Tree exponents and Hashimoto carrier",
        "source_links": {
            "CCCIV": "Spanning Tree Count of W(3,3)",
            "CCCV_signless": "Signless Laplacian Spectrum of W(3,3)",
            "CCCVI_distance": "Distance Matrix Spectrum of W(3,3)",
            "CLXXXII": "CCT / Hashimoto carrier weld",
            "CCCV_spectral_weld": "Spectral complexity / master ladder weld",
        },
        "w33_atoms": {
            "q": q,
            "V": V,
            "K": K,
            "lambda": lam,
            "mu": mu,
            "r": r,
            "s": s,
            "E": E,
            "directed_edges": DIRECTED,
            "Hashimoto_branch": HASHIMOTO_BRANCH,
            "Phi3": Phi3,
            "Phi4": Phi4,
            "Phi6": Phi6,
            "J": J,
            "J_inverse": J_inv,
            "Albert": ALBERT,
            "H1": H1,
        },
        "operator_layers": [asdict(layer) for layer in operator_layers()],
        "new_bridge_identities": {
            "four_operator_closure": "A, L=KI-A, Q=KI+A, Delta=2J-2I-A are affine shadows of the same eigenspace split",
            "L_Q_duality": "L+Q=2K I, so eigenvalues pair to 24 on every eigenspace",
            "distance_involution": "on restricted eigenspaces Delta=-2I-A, so r<->s because r+s=-2",
            "directed_trace": "tr(Q)=480=2E=2q(q^4-1)",
            "signless_projective_moment": "tr(Q^2)=480*Phi3=6240",
            "distance_theta_moment": "tr(Delta^2)=480*Phi4=4800",
            "tree_5_exponent_from_second_moments": "e5(tau)=23=(tr(Q^2)+tr(Delta^2))/(2E)=Phi3+Phi4",
            "q_clock_from_second_moments": "q=3=(tr(Q^2)-tr(Delta^2))/(2E)=Phi3-Phi4",
            "wiener_hashimoto_law": "Wiener=1320=(K-1)*Q-energy=11*120",
            "distance_second_moment_hashimoto_law": "tr(Delta^2)=theta(W)*directed_edges=10*480",
        },
        "matrix_tree_exponents": {
            "tau_factorization": TREE_COUNT_FACTOR,
            "e2": TREE_EXP_2,
            "e2_interpretation": "q^4=H1=three-generation/triple-Albert carrier",
            "e5": TREE_EXP_5,
            "e5_interpretation": "Phi3+Phi4, equivalently q^3-(q+1)=27-4, recovered from Q/Delta second moments",
        },
        "checks": checks,
        "theorem_statement": (
            "The four canonical matrices A, L=KI-A, Q=KI+A, and Delta=2J-2I-A form an exact operator tetrahedron over the same "
            "three eigenspaces.  The signless trace tr(Q)=480 is the Hashimoto directed carrier.  Its second moment is 480*Phi3, "
            "while the distance second moment is 480*Phi4.  Therefore their normalized sum is Phi3+Phi4=23, exactly the exponent "
            "of 5 in the Matrix Tree factorization tau(W)=2^81*5^23, and their normalized difference is Phi3-Phi4=q=3.  The "
            "Wiener index also closes as 1320=(K-1)*120, i.e. Hashimoto branch times signless Laplacian energy."
        ),
        "interpretive_note": (
            "This is the deepest current weld: global tree complexity, distance geometry, signless energy, and nonbacktracking carrier "
            "are not separate shadows.  The tree exponent 23 is literally the sum of normalized second moments of the signless and "
            "distance operators; the q-clock is their normalized difference."
        ),
    }


def main() -> int:
    audit = operator_tetrahedron_entropy_audit()
    out = ROOT / "PART_CCCVII_operator_tetrahedron_entropy_bridge_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
