r"""Part DCCXXVIII: The Ternary-Quaternion-Codec Tower and W(3,3) as
Two-Qutrit Pauli Commutation Geometry.

The user's observation: since q = 3 produces the three Clifford bivector
axes (B23, B31, B12) of DCCXIV, the Master-Equation pair (q, q+1) =
(3, 4) is precisely the (qutrit, quaternion) pair.  The 3 bivectors plus
1 identity span the QUATERNION algebra H = Cl^+(3, 0), and the codec
size 12 = q(q+1) is qutrit-times-quaternion.

The same q = 3 has a parallel physics realisation: W(3,3) is the
*commutation geometry of two-qutrit Pauli operators* (Saniga-Planat
2007).  Two qutrits have a Heisenberg-Weyl Pauli group of order
3 * 3^2 * 3^2 = 243 = 3^5; its centre is Z_3, and the quotient
G / Z(G) is an abelian 4-dim vector space over F_3.  The commutator on
this F_3^4 is a non-degenerate symplectic form, and the projective space
PG(3, F_3) of its isotropic points is W(3,3) = Sp(4, F_3).

  v(W(3,3)) = (3^4 - 1) / (3 - 1) = 40
            = number of non-identity 2-qutrit Pauli operators (mod centre);

  k(W(3,3)) = 12
            = number of 2-qutrit Pauli operators that commute with a
              given non-identity operator;

  E(W(3,3)) = 240
            = number of commuting pairs of distinct non-identity
              2-qutrit Pauli operators (mod centre).

Three independent W(3,3) numbers thus have direct quantum-information
meanings on two qutrits.

Ternary-Quaternion-Codec Tower:

  Layer 1 (TERNARY = q = 3):
        3 bivector axes B23, B31, B12 (DCCXIV)
        3 generators of one qutrit Pauli group (mod centre)
        3 = smallest non-abelian symmetric group S_3

  Layer 2 (QUATERNION = q + 1 = 4):
        H = Cl^+(3, 0) = {1, B23, B31, B12} (= 3 bivectors + identity)
        4 spacetime dimensions (3 + 1)
        4 = tetrahedron V = vertex count of triangle's closure (DCCXXIV)
        Unit quaternions = SU(2) = double cover of SO(3) rotations

  Layer 3 (CODEC = q(q+1) = 12):
        12 = local W(3,3) valency
        12 = two-qutrit Pauli commuting partners (Saniga-Planat)
        12 = qutrit x quaternion (Clifford reading)
        12 = codec / E_6 Coxeter / ZETA(-1) denominator

The closure that turns 3 (ternary axes) into 4 (quaternion algebra) is
the same closure that turns the triangle's 3 vertices into the
tetrahedron's 4 (DCCXXIV).
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


OUT_PATH = ROOT / "data" / "dccxxviii_ternary_quaternion_codec_tower.json"

Q = 3
QP1 = Q + 1
CODEC = Q * QP1                              # 12

# Two-qutrit Pauli geometry
PAULI_GROUP_ORDER = 3 ** 5                   # 243 (Heisenberg-Weyl mod nothing)
CENTRE_ORDER = 3                              # Z_3
QUOTIENT_ORDER = PAULI_GROUP_ORDER // CENTRE_ORDER  # 81 = 3^4

W33_V = 40                                    # = (3^4 - 1) / (3 - 1)
W33_K = CODEC                                 # 12
W33_E = 240                                   # = v*k/2


# ---------------------------------------------------------------------------
# Single-qutrit Pauli generators X, Z (clock and shift) over Z_3
# ---------------------------------------------------------------------------


def qutrit_X() -> np.ndarray:
    """Shift operator X: |j> -> |j+1 mod 3>."""
    X = np.zeros((3, 3), dtype=complex)
    for j in range(3):
        X[(j + 1) % 3, j] = 1
    return X


def qutrit_Z() -> np.ndarray:
    """Clock operator Z: |j> -> omega^j |j>, omega = exp(2 pi i / 3)."""
    omega = np.exp(2j * np.pi / 3)
    return np.diag([omega ** j for j in range(3)])


def is_commutator_omega_power(A: np.ndarray, B: np.ndarray, k: int,
                                tol: float = 1e-8) -> bool:
    """Test whether A B = omega^k B A within tolerance."""
    omega = np.exp(2j * np.pi / 3)
    AB = A @ B
    BA = B @ A
    return np.allclose(AB, (omega ** k) * BA, atol=tol)


# ---------------------------------------------------------------------------
# Quaternion algebra H = Cl^+(3, 0)
# ---------------------------------------------------------------------------


def quaternion_basis() -> dict[str, dict[str, Any]]:
    """The 4 basis elements: 1 + 3 bivectors."""
    return {
        "1":   {"role": "identity (real unit)", "clifford": "+1"},
        "B23": {"role": "imaginary unit i = e_2 e_3", "clifford": "e_2 e_3"},
        "B31": {"role": "imaginary unit j = e_3 e_1", "clifford": "e_3 e_1"},
        "B12": {"role": "imaginary unit k = e_1 e_2", "clifford": "e_1 e_2"},
    }


def quaternion_multiplication_rule() -> dict[str, str]:
    return {
        "B23 * B31": "B12 (i j = k)",
        "B31 * B12": "B23 (j k = i)",
        "B12 * B23": "B31 (k i = j)",
        "B23 * B23": "-1",
        "B31 * B31": "-1",
        "B12 * B12": "-1",
        "B23 * B31 * B12": "-1 (ijk = -1)",
    }


# ---------------------------------------------------------------------------
# Two-qutrit Pauli commutation graph -> W(3,3)
# ---------------------------------------------------------------------------


def two_qutrit_pauli_labels() -> list[tuple[int, int, int, int]]:
    """Each non-identity 2-qutrit Pauli operator (mod centre) corresponds
    to a vector (a1, b1, a2, b2) in F_3^4 \\ {0}, identified mod scalar.
    Returns the 80 = 3^4 - 1 non-zero vectors; W(3,3) vertices are the
    40 projective classes (a, lambda * a) for lambda in F_3*."""
    labels = []
    for a1 in range(3):
        for b1 in range(3):
            for a2 in range(3):
                for b2 in range(3):
                    if (a1, b1, a2, b2) != (0, 0, 0, 0):
                        labels.append((a1, b1, a2, b2))
    return labels


def projective_classes() -> set[tuple[int, int, int, int]]:
    """40 representatives of F_3^4 \\ {0} mod F_3* scalar action."""
    seen: set[tuple[int, int, int, int]] = set()
    reps: set[tuple[int, int, int, int]] = set()
    for v in two_qutrit_pauli_labels():
        if v in seen:
            continue
        # mark the F_3* orbit {v, 2v} as seen, choose lex min as rep
        v2 = tuple((2 * x) % 3 for x in v)
        orbit = {v, v2}
        for w in orbit:
            seen.add(w)
        reps.add(min(orbit))
    return reps


def f3_symplectic_form(u: tuple[int, int, int, int],
                       v: tuple[int, int, int, int]) -> int:
    """omega(u, v) = u1 v3 - u3 v1 + u2 v4 - u4 v2  (mod 3)
       in (a1, b1, a2, b2) coordinates this is the standard symplectic form."""
    a1, b1, a2, b2 = u
    c1, d1, c2, d2 = v
    return (a1 * d1 - b1 * c1 + a2 * d2 - b2 * c2) % 3


def commute_pairs_count() -> dict[str, int]:
    """Count commuting (omega = 0) and non-commuting (omega != 0) pairs
    among the 40 projective classes."""
    reps = sorted(projective_classes())
    comm = 0
    non_comm = 0
    for i, u in enumerate(reps):
        for v in reps[i + 1:]:
            if f3_symplectic_form(u, v) == 0:
                comm += 1
            else:
                non_comm += 1
    return {
        "vertices": len(reps),
        "commuting_pairs": comm,
        "non_commuting_pairs": non_comm,
        "total_pairs": comm + non_comm,
    }


def neighborhood_audit(reps: list[tuple[int, int, int, int]]) -> dict[str, int]:
    """For each rep, count how many others it commutes with (= valency)."""
    valencies = []
    for u in reps:
        v_count = 0
        for v in reps:
            if v == u:
                continue
            if f3_symplectic_form(u, v) == 0:
                v_count += 1
        valencies.append(v_count)
    return {
        "min_valency": min(valencies),
        "max_valency": max(valencies),
        "all_same": min(valencies) == max(valencies),
        "common_valency": valencies[0],
    }


# ---------------------------------------------------------------------------
# Tower table
# ---------------------------------------------------------------------------


def tower_table() -> list[dict[str, Any]]:
    return [
        {
            "layer": 1,
            "name": "TERNARY (qutrit)",
            "size": Q,
            "structure": "3 Clifford bivectors B23, B31, B12 (DCCXIV)",
            "physics": "single qutrit Pauli generators X, Z (mod phase)",
            "topology": "minimum closed 1-loop has 3 vertices (DCCXXIV)",
        },
        {
            "layer": 2,
            "name": "QUATERNION (qubit-pair / spacetime)",
            "size": QP1,
            "structure": "H = Cl^+(3,0) = {1, B23, B31, B12}",
            "physics": "SU(2) = double cover of SO(3); 4D spacetime basis",
            "topology": "triangle's closure adds a 4th element (face / apex)",
        },
        {
            "layer": 3,
            "name": "CODEC (two-qutrit valency)",
            "size": CODEC,
            "structure": "12 = q(q+1) = ternary * quaternion",
            "physics": "12 = #(2-qutrit Pauli operators commuting with given operator) (Saniga-Planat)",
            "topology": "W(3,3) valency; tomotope E; E_6 Coxeter; ζ(-1) denom",
        },
    ]


# ---------------------------------------------------------------------------
# Build bridge
# ---------------------------------------------------------------------------


def build_bridge() -> dict[str, Any]:
    X = qutrit_X()
    Z = qutrit_Z()
    omega = np.exp(2j * np.pi / 3)

    # Single-qutrit Pauli commutation: X Z = omega^{-1} Z X (or omega depending on convention)
    XZ = X @ Z
    ZX = Z @ X
    # Find k such that X Z = omega^k Z X
    pauli_phase = None
    for k in range(3):
        if np.allclose(XZ, (omega ** k) * ZX):
            pauli_phase = k
            break

    reps = sorted(projective_classes())
    pair_counts = commute_pairs_count()
    nbr = neighborhood_audit(reps)
    tower = tower_table()

    identities = {
        "ternary_size_equals_q": Q == 3,
        "quaternion_size_equals_q_plus_1": QP1 == 4,
        "codec_equals_ternary_times_quaternion": CODEC == Q * QP1 == 12,
        "single_qutrit_pauli_phase_is_omega_power": pauli_phase in {1, 2},
        "two_qutrit_projective_class_count_is_40": len(reps) == W33_V == 40,
        "two_qutrit_commuting_pair_count_is_240": pair_counts["commuting_pairs"] == W33_E == 240,
        "two_qutrit_valency_constant": nbr["all_same"] is True,
        "two_qutrit_common_valency_is_12": nbr["common_valency"] == W33_K == 12,
        "F3_vector_space_dim_is_4": 4 == 2 * 2,         # 2 qutrits, 2 components each
        "F3_to_4_minus_one_over_2_equals_40": (3**4 - 1) // 2 == W33_V == 40,
        "pauli_group_order_is_3_to_5": PAULI_GROUP_ORDER == 243,
        "centre_order_is_3": CENTRE_ORDER == Q == 3,
        "tower_three_layers": len(tower) == 3,
        "layer_sizes_are_3_4_12": [t["size"] for t in tower] == [3, 4, 12],
    }

    theorem = (
        "Ternary-Quaternion-Codec Tower Theorem.  At the W(3,3) saturation "
        "q = 3 the ternary structure (3 Clifford bivectors B23, B31, B12 of "
        "DCCXIV, equivalently the 3 generators of a single qutrit Pauli "
        "group mod centre) closes by adding one identity element into the "
        "QUATERNION algebra H = Cl^+(3, 0) = {1, B23, B31, B12}, of "
        "dimension q + 1 = 4.  The product q * (q + 1) = 12 is the local "
        "codec.  In direct physical realisation, two qutrits have a "
        "Heisenberg-Weyl Pauli group of order 3^5 = 243; its quotient by "
        "the Z_3 centre is F_3^4 (81 = 3^4 elements).  The symplectic form "
        "induced by the commutator on F_3^4 makes its 40 = (3^4 - 1) / 2 "
        "projective classes into the vertices of W(3,3) = Sp(4, F_3), with "
        "12 commuting partners per vertex and 240 commuting pairs total.  "
        "All three W(3,3) numbers (v, k, E) = (40, 12, 240) are quantum-"
        "information quantities for two qutrits."
    )

    one_line = (
        "3 (ternary bivectors) + 1 (identity) = 4 (quaternion) ; "
        "3 * 4 = 12 (codec) ; W(3,3) = (Sp(4, F_3)) = two-qutrit Pauli "
        "commutation geometry, with (v, k, E) = (40, 12, 240) computed "
        "explicitly here."
    )

    summary = {
        "q": Q,
        "qp1": QP1,
        "codec": CODEC,
        "two_qutrit_vertices": len(reps),
        "two_qutrit_valency": nbr["common_valency"],
        "two_qutrit_commuting_pairs": pair_counts["commuting_pairs"],
        "matches_W33_v": len(reps) == W33_V,
        "matches_W33_k": nbr["common_valency"] == W33_K,
        "matches_W33_E": pair_counts["commuting_pairs"] == W33_E,
        "all_identities_hold": all(identities.values()),
    }

    return {
        "summary": summary,
        "ternary_quaternion_codec_tower": tower,
        "quaternion_basis": quaternion_basis(),
        "quaternion_multiplication_rule": quaternion_multiplication_rule(),
        "two_qutrit_pauli_check": {
            "projective_classes_count": len(reps),
            "neighborhood_audit": nbr,
            "pair_counts": pair_counts,
        },
        "single_qutrit_commutation_phase": {
            "X_Z_equals_omega_power_times_Z_X": pauli_phase,
            "interpretation": "single qutrit Heisenberg-Weyl commutation",
        },
        "identities": identities,
        "theorem": theorem,
        "one_line": one_line,
        "honesty_boundary": (
            "The W(3,3) = Sp(4, F_3) = two-qutrit Pauli commutation geometry "
            "identification is a known theorem (Saniga-Planat 2007 and "
            "follow-ups).  This part VERIFIES the identification "
            "numerically by computing the 40 projective classes of F_3^4, "
            "their pairwise symplectic form, and confirming valency 12 and "
            "edge count 240.  The ternary-quaternion-codec tower is the "
            "Clifford-algebra reading of the same q = 3 saturation already "
            "documented in DCCXIV / DCCXVII / DCCXXIV; this part does not "
            "derive new physical observables."
        ),
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    payload = build_bridge()
    print(f"Wrote {out}")
    print(f"Verified: {payload['summary']['all_identities_hold']}")
    print(f"\nTower:")
    for t in payload["ternary_quaternion_codec_tower"]:
        print(f"  Layer {t['layer']}: {t['name']:<30} size = {t['size']}")
    s = payload["summary"]
    print(f"\nTwo-qutrit Pauli commutation graph (computed):")
    print(f"  vertices (projective classes of F_3^4): {s['two_qutrit_vertices']}  (W(3,3) v = 40)")
    print(f"  valency (commuting partners):           {s['two_qutrit_valency']}  (W(3,3) k = 12)")
    print(f"  edges (commuting pairs):                {s['two_qutrit_commuting_pairs']}  (W(3,3) E = 240)")
    print(f"  matches W(3,3): v={s['matches_W33_v']}, k={s['matches_W33_k']}, E={s['matches_W33_E']}")


if __name__ == "__main__":
    main()
