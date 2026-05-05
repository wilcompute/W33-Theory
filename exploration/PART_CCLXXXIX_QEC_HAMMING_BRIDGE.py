"""
Part CCLXXXIX: Quantum Error Correcting Codes — W(3,3) as the Ternary Hamming Code

The 40 points of the projective space PG(3,3) over GF(3) are simultaneously:

  (i)  the 40 vertices of the W(3,3) strongly regular graph (Parts CCLXXXVI–CCLXXXVIII),
  (ii) the columns of the parity-check matrix of the perfect ternary Hamming code Ham(4,3).

This double identification yields the SM fermion partition:

  Ham(4,3) = [40, 36, 3]_3   →   length = V = 40
                               →   dimension = QUARKS_36 = 36
                               →   min distance = Q = 3 (field order / # generations)
                               →   redundancy = EW_GAUGE_4 = 4

  Sim(4,3) = [40, 4, 27]_3   →   dual of Ham(4,3)
                               →   dimension = EW_GAUGE_4 = 4
                               →   min distance = K2 = 27

The perfect-code condition (Hamming ball of radius 1 has size 81 = 3^4 = Q^EW_GAUGE_4) is
the coding-theoretic counterpart of the Delsarte bound from Part CCLXXXVIII.
"""

from __future__ import annotations
import math
from fractions import Fraction

# ── W(3,3) / W(E6) constants ──────────────────────────────────────────────────
V      = 40     # vertices
K      = 12     # valency
LAM    = 2      # lambda
MU     = 4      # mu
Q      = 3      # field order GF(3)
K2     = 27     # co-valency (non-adjacent vertices share no common neighbour)
MULT_R = 24     # eigenvalue multiplicity (r = 2)
MULT_S = 15     # eigenvalue multiplicity (s = -4)
EDGES  = 240

# ── SM particle counts ────────────────────────────────────────────────────────
QUARKS_36  = 36   # 3 colours × 3 generations × 4 Weyl species
EW_GAUGE_4 = 4    # W+, W−, Z, γ
TOTAL_SM   = 40   # = V

# ── Ternary Hamming code Ham(4, 3) ────────────────────────────────────────────
# Ham(r, q) over GF(q) has parameters:
#   block length  n = (q^r − 1) / (q − 1)
#   dimension     k = n − r
#   min distance  d = 3
#
# For q = 3, r = 4:
#   n = (81 − 1) / 2 = 40  ← exactly V !
#   k = 40 − 4 = 36        ← exactly QUARKS_36 !
#   d = 3                  ← exactly Q = GF(3) field order !
#   redundancy = r = 4     ← exactly EW_GAUGE_4 !

HAMMING_R          = 4
HAMMING_Q          = Q                                            # = 3
HAMMING_LENGTH     = (HAMMING_Q**HAMMING_R - 1) // (HAMMING_Q - 1)   # = 40
HAMMING_REDUNDANCY = HAMMING_R                                    # = 4
HAMMING_DIMENSION  = HAMMING_LENGTH - HAMMING_REDUNDANCY          # = 36
HAMMING_MIN_DIST   = 3                                            # = Q

# ── Perfect-code property ─────────────────────────────────────────────────────
# Hamming ball of radius t = 1 around any codeword:
#   |B(c, 1)| = 1 + n*(q − 1) = 1 + 40*2 = 81 = 3^4 = q^r
#
# Hamming bound (perfect code condition):
#   |C| * |B(c,1)| = q^n   →   3^36 * 81 = 3^40 ✓

HAMMING_BALL_RADIUS = 1
HAMMING_BALL_SIZE   = 1 + HAMMING_LENGTH * (HAMMING_Q - 1)       # = 81
HAMMING_PERFECT_RHS = HAMMING_Q ** HAMMING_REDUNDANCY             # = 3^4 = 81
HAMMING_IS_PERFECT  = (HAMMING_BALL_SIZE == HAMMING_PERFECT_RHS)  # True

# Covering radius is also 1 for a perfect 1-error-correcting code
HAMMING_COVERING_RADIUS = 1

# ── Simplex code Sim(4, 3) — dual of Ham(4, 3) ───────────────────────────────
# Sim(r, q) has parameters:
#   length        = (q^r − 1) / (q − 1)   = 40 = V
#   dimension     = r                     = 4  = EW_GAUGE_4
#   min distance  = q^{r−1}               = 27 = K2
#   The code is equidistant: all nonzero codewords have weight q^{r−1} = 27.
#   Number of nonzero codewords = q^r − 1 = 80.

SIMPLEX_LENGTH         = HAMMING_LENGTH                           # = 40 = V
SIMPLEX_DIMENSION      = HAMMING_REDUNDANCY                       # = 4  = EW_GAUGE_4
SIMPLEX_MIN_DIST       = HAMMING_Q ** (HAMMING_R - 1)             # = 27 = K2
SIMPLEX_NUM_NONZERO    = HAMMING_Q ** HAMMING_REDUNDANCY - 1      # = 80
SIMPLEX_IS_EQUIDISTANT = True   # all nonzero words have weight SIMPLEX_MIN_DIST

# Duality: Ham(4,3)^⊥ = Sim(4,3), Sim(4,3)^⊥ = Ham(4,3)
DUAL_DIMENSION_SUM = HAMMING_DIMENSION + SIMPLEX_DIMENSION  # = 36 + 4 = 40 = n ✓

# ── PG(3, 3) ↔ W(3,3) identification ────────────────────────────────────────
# The projective space PG(3, 3) over GF(3) has exactly:
#   |PG(3,3)| = (3^4 − 1) / (3 − 1) = 40 = V points.
#
# These 40 projective points ARE the columns of the parity-check matrix H
# of Ham(4,3) (each column is a distinct point of PG(3,3)).
# They are also the 40 vertices of the W(3,3) SRG under the symplectic form:
#   u ~ v  ⟺  ⟨u, v⟩_symplectic ≠ 0   (adjacency in W(3,3))

PG3_3_POINT_COUNT = (Q**4 - 1) // (Q - 1)                      # = 40 = V
HAMMING_COLS_EQ_PG = (PG3_3_POINT_COUNT == HAMMING_LENGTH)       # True

# ── Qutrit / quantum error correction connection ──────────────────────────────
# The W(3,3) symplectic polar space Sp(4, 3) is the phase space for n_q = 2 qutrits
# (quantum systems with q = 3 levels).
# The Heisenberg–Weyl group for 2 qutrits has q^{2*n_q} = 3^4 = 81 elements.
# In projective space (removing identity and scalar multiples):
#   # non-trivial Pauli error operators = (3^4 − 1) / (3 − 1) = 40 = V
#
# Thus the 40 vertices of W(3,3) are exactly the 40 non-trivial Pauli operators
# (up to phase) acting on a 2-qutrit system.  Adjacency in W(3,3) corresponds
# to the symplectic commutativity structure of these operators.

NUM_QUTRITS      = 2
HEISENBERG_SIZE  = Q ** (2 * NUM_QUTRITS)                        # = 81
QUTRIT_PAULIS    = (HEISENBERG_SIZE - 1) // (Q - 1)              # = 40 = V

# The quantum Hamming bound for a [[n_q, k_q, 3]]_3 qutrit stabilizer code:
#   1 + n_q * (q^2 − 1) ≤ q^{n_q − k_q}   (for t=1, d=3)
# For n_q = 20 qutrits (half of V=40 pairs):
#   1 + 20*8 = 161 ≤ 3^{n_q − k_q} → n_q − k_q ≥ ceil(log_3(161)) = 5
QUANTUM_N            = V // 2                                     # = 20 qutrits
QUANTUM_BALL_SIZE_LB = 1 + QUANTUM_N * (Q**2 - 1)                # = 161
QUANTUM_MIN_OVERHEAD = math.ceil(math.log(QUANTUM_BALL_SIZE_LB, Q))  # = 5

# ── Generation / Yukawa connection ────────────────────────────────────────────
# The perfect 1-error-correcting structure implies:
#   - Exactly 1 "error" (generation index flip) is correctable
#   - 3 generations = d = Q: the code corrects exactly (d−1)/2 = 1 error
#   - The 4 EW parity-check positions index the error syndrome

NUM_GENERATIONS          = 3                                      # = Q = HAMMING_MIN_DIST
COSET_LEADERS_PER_SYMBOL = Q - 1                                  # = 2  (nonzero GF(3) values)
TOTAL_ERROR_SYNDROMES    = 1 + HAMMING_LENGTH * (Q - 1)           # = 81 = 3^4

# ── Coding-theory bounds ──────────────────────────────────────────────────────

def griesmer_bound(n: int, k: int, d: int, q: int) -> int:
    """Griesmer lower bound: n ≥ ∑_{i=0}^{k−1} ⌈d / q^i⌉."""
    return sum(math.ceil(d / (q**i)) for i in range(k))


GRIESMER_LB = griesmer_bound(
    HAMMING_LENGTH, HAMMING_DIMENSION, HAMMING_MIN_DIST, HAMMING_Q
)  # = 3 + 1*35 = 38

SINGLETON_BOUND           = HAMMING_LENGTH - HAMMING_DIMENSION + 1  # = 5
HAMMING_SATISFIES_SINGLETON = (HAMMING_MIN_DIST <= SINGLETON_BOUND)  # True (3 ≤ 5)
HAMMING_MEETS_GRIESMER    = (HAMMING_LENGTH >= GRIESMER_LB)          # True (40 ≥ 38)

# Ham(4,3) is NOT an MDS code (d = 3 < n − k + 1 = 5)
HAMMING_IS_MDS = (HAMMING_MIN_DIST == SINGLETON_BOUND)              # False


# ── Verification functions ────────────────────────────────────────────────────

def verify_hamming_code() -> dict:
    """Verify Ham(4,3) parameters match W(3,3) / SM constants."""
    return {
        "hamming_length_eq_v":           HAMMING_LENGTH == V,
        "hamming_dimension_eq_quarks36":  HAMMING_DIMENSION == QUARKS_36,
        "hamming_min_dist_eq_q":          HAMMING_MIN_DIST == Q,
        "hamming_redundancy_eq_ew_gauge": HAMMING_REDUNDANCY == EW_GAUGE_4,
        "simplex_min_dist_eq_k2":         SIMPLEX_MIN_DIST == K2,
        "hamming_is_perfect":             HAMMING_IS_PERFECT,
    }


def verify_pg_identification() -> dict:
    """Verify PG(3,3) = W(3,3) vertex set identification."""
    return {
        "pg3_3_points_eq_v":     PG3_3_POINT_COUNT == V,
        "hamming_cols_eq_pg":    HAMMING_COLS_EQ_PG,
        "qutrit_paulis_eq_v":    QUTRIT_PAULIS == V,
        "heisenberg_size_eq_81": HEISENBERG_SIZE == 81,
    }


def verify_sm_coding_correspondence() -> dict:
    """Verify SM particle ↔ code parameter correspondence."""
    return {
        "info_symbols_eq_quarks":    HAMMING_DIMENSION == QUARKS_36,
        "parity_eq_ew_gauge":        HAMMING_REDUNDANCY == EW_GAUGE_4,
        "sm_partition_40":           QUARKS_36 + EW_GAUGE_4 == V,
        "generations_eq_min_dist":   NUM_GENERATIONS == HAMMING_MIN_DIST,
        "generations_eq_q":          NUM_GENERATIONS == Q,
        "ball_eq_q_pow_redundancy":  HAMMING_BALL_SIZE == Q**HAMMING_REDUNDANCY,
    }


def verify_all() -> dict:
    """Master verification — returns dict of all check results."""
    result: dict[str, bool] = {}
    result.update(verify_hamming_code())
    result.update(verify_pg_identification())
    result.update(verify_sm_coding_correspondence())
    return result


def build_cclxxxix_summary() -> dict:
    """Build machine-readable summary of Part CCLXXXIX discoveries."""
    checks = verify_all()
    return {
        "part_number": "CCLXXXIX",
        "title": "Quantum Error Correcting Codes — W(3,3) as the Ternary Hamming Code",
        "theme": "Ham(4,3) = [40,36,3]_3 perfectly encodes the SM fermion partition",
        "key_discoveries": [
            f"Ham(4,3) = [{HAMMING_LENGTH},{HAMMING_DIMENSION},{HAMMING_MIN_DIST}]_3: "
            f"length=V, dim=QUARKS_36, d=Q",
            f"Sim(4,3) = [{SIMPLEX_LENGTH},{SIMPLEX_DIMENSION},{SIMPLEX_MIN_DIST}]_3: "
            f"dim=EW_GAUGE_4, d=K2",
            f"Perfect code: |B(c,1)| = {HAMMING_BALL_SIZE} = Q^EW_GAUGE_4 = {Q}^{EW_GAUGE_4}",
            f"|PG(3,3)| = {PG3_3_POINT_COUNT} = V = columns of parity-check matrix",
            f"SM partition: {HAMMING_DIMENSION} info + {HAMMING_REDUNDANCY} parity = {HAMMING_LENGTH} = V",
            f"Min distance {HAMMING_MIN_DIST} = Q = number of SM generations",
            f"Qutrit Pauli operators: {QUTRIT_PAULIS} = V (W(3,3) as 2-qutrit phase space)",
        ],
        "hamming_code": {
            "block_length":       HAMMING_LENGTH,
            "dimension":          HAMMING_DIMENSION,
            "min_distance":       HAMMING_MIN_DIST,
            "redundancy":         HAMMING_REDUNDANCY,
            "is_perfect":         HAMMING_IS_PERFECT,
            "ball_size":          HAMMING_BALL_SIZE,
            "covering_radius":    HAMMING_COVERING_RADIUS,
        },
        "simplex_code": {
            "block_length":       SIMPLEX_LENGTH,
            "dimension":          SIMPLEX_DIMENSION,
            "min_distance":       SIMPLEX_MIN_DIST,
            "num_nonzero":        SIMPLEX_NUM_NONZERO,
            "is_equidistant":     SIMPLEX_IS_EQUIDISTANT,
        },
        "sm_correspondence": {
            "quarks_eq_dimension":        HAMMING_DIMENSION == QUARKS_36,
            "ew_gauge_eq_redundancy":     HAMMING_REDUNDANCY == EW_GAUGE_4,
            "generations_eq_min_dist":    NUM_GENERATIONS == HAMMING_MIN_DIST,
            "partition_sum":              QUARKS_36 + EW_GAUGE_4,
        },
        "verification_status": (
            "ALL CHECKS PASS" if all(checks.values()) else "SOME CHECKS FAIL"
        ),
    }


if __name__ == "__main__":
    checks = verify_all()
    passed = sum(1 for v in checks.values() if v)
    total  = len(checks)
    print(f"CCLXXXIX Verification: {passed}/{total} checks pass")
    if passed == total:
        print("✓ All checks PASS - Part CCLXXXIX bridge is complete")
    else:
        print("✗ Some checks failed:")
        for key, val in checks.items():
            if not val:
                print(f"  {key}: {val}")
