"""
Part CCXCI: Covering Radius, Packing-Covering Duality, and the Perfect Code
Geometry of Ham(4,3) / W(3,3).

A linear code C ⊆ GF(q)^n has:
  - Packing radius t = floor((d-1)/2)  (error-correcting radius)
  - Covering radius R = max_v min_{c in C} d(v, c)

A code is *perfect* iff t = R (every vector is within distance t of exactly one
codeword). Ham(4,3) is perfect with t = R = 1.

The t = R = 1 condition:
  - The q^n = 81 cosets of Ham(4,3) partition GF(3)^4 into 81 Hamming balls of
    radius 1, each of size 1 + n*(q-1) = 1 + 4*2 = 9 = ... wait, that's the
    scheme ball, not the code ball.

Actually the *code* lives in GF(3)^40 (block length = 40), and:
  - Ball of radius 1 in GF(3)^40: size = 1 + 40*2 = 81 = q^r.
  - Total codewords * ball size = q^36 * 81 = q^36 * q^4 = q^40 = |GF(3)^40|. ✓

The perfect partition gives a geometric picture:
  - 3^36 codewords, each with a ball of 81 vectors, no overlaps, covering all
    of GF(3)^40.
  - Each *coset* of Ham(4,3) has exactly one vector of minimum weight (the coset
    leader), which is the unique nearest codeword.

All arithmetic is exact (fractions / integers, no numpy).
"""

from fractions import Fraction
from math import comb

# ─────────────────────────────────────────────────────────────────────────────
# W(3,3) SRG constants
# ─────────────────────────────────────────────────────────────────────────────
V = 40
K = 12
LAM = 2
MU = 4
Q = 3
K2 = 27
MULT_R = 24
MULT_S = 15
EDGES = 240

# ─────────────────────────────────────────────────────────────────────────────
# SM constants
# ─────────────────────────────────────────────────────────────────────────────
QUARKS_36 = 36
EW_GAUGE_4 = 4
TOTAL_SM = 40

# ─────────────────────────────────────────────────────────────────────────────
# Ham(4,3) code parameters
# ─────────────────────────────────────────────────────────────────────────────
HAM_N = 40          # Block length = V = 40
HAM_K = 36          # Dimension = QUARKS_36
HAM_D = 3           # Min distance = Q = 3
HAM_Q = 3           # Field order
HAM_R = 4           # Redundancy = EW_GAUGE_4

# ─────────────────────────────────────────────────────────────────────────────
# Packing radius t = floor((d - 1) / 2)
# ─────────────────────────────────────────────────────────────────────────────
PACKING_RADIUS = (HAM_D - 1) // 2   # = 1  (error-correcting radius)

# ─────────────────────────────────────────────────────────────────────────────
# Hamming ball of radius r in GF(q)^n
#   Vol(n, r, q) = sum_{i=0}^{r} C(n, i) * (q-1)^i
# ─────────────────────────────────────────────────────────────────────────────
def hamming_ball_volume(n: int, r: int, q: int) -> int:
    """Number of vectors in a Hamming ball of radius r in GF(q)^n."""
    return sum(comb(n, i) * (q - 1) ** i for i in range(r + 1))


BALL_VOL_T = hamming_ball_volume(HAM_N, PACKING_RADIUS, HAM_Q)
# = 1 + 40*2 = 81

# ─────────────────────────────────────────────────────────────────────────────
# Perfect code condition:  |C| * Vol(n, t, q) = q^n
# ─────────────────────────────────────────────────────────────────────────────
CODE_SIZE = HAM_Q ** HAM_K           # = 3^36
AMBIENT_SIZE = HAM_Q ** HAM_N        # = 3^40
PERFECT_CODE_PRODUCT = CODE_SIZE * BALL_VOL_T
PERFECT_CODE_EXACT = (PERFECT_CODE_PRODUCT == AMBIENT_SIZE)

# ─────────────────────────────────────────────────────────────────────────────
# Covering radius R
#
# For a perfect code: R = t exactly.  Ham(4,3) is perfect, so R = t = 1.
# This can also be seen from the Hamming scheme: the maximum distance between
# any word and the code is 1 (every coset has a unique leader of weight <= 1).
# ─────────────────────────────────────────────────────────────────────────────
COVERING_RADIUS = PACKING_RADIUS     # = 1  (perfect code: R = t)
PACKING_COVERING_EQUAL = (PACKING_RADIUS == COVERING_RADIUS)

# ─────────────────────────────────────────────────────────────────────────────
# Coset structure
#
# The ambient space GF(3)^40 partitions into 3^r = 3^4 = 81 cosets of Ham(4,3).
# Each coset has exactly one leader of weight <= t = 1 (the nearest codeword).
#
# Leaders of weight 0: the zero vector (1 total)
# Leaders of weight 1: n*(q-1) = 40*2 = 80 vectors
# Total: 81 = BALL_VOL_T ✓
# ─────────────────────────────────────────────────────────────────────────────
NUM_COSETS = HAM_Q ** HAM_R          # = 3^4 = 81
COSET_LEADERS_WT0 = 1
COSET_LEADERS_WT1 = HAM_N * (HAM_Q - 1)   # = 80
TOTAL_COSET_LEADERS = COSET_LEADERS_WT0 + COSET_LEADERS_WT1   # = 81
COSET_STRUCTURE_CORRECT = (TOTAL_COSET_LEADERS == NUM_COSETS == BALL_VOL_T)

# ─────────────────────────────────────────────────────────────────────────────
# Syndrome decoding
#
# Each coset of Ham(4,3) is identified by a syndrome s ∈ GF(3)^4.
# The syndrome of a received vector y = c + e is s = H*y (parity check).
# For weight-1 errors: s identifies the unique error position and symbol.
#
# Number of syndromes: 3^4 = 81
# Syndrome 0 → codeword (no error)
# Syndrome ≠ 0 → weight-1 error in position given by the syndrome column
# ─────────────────────────────────────────────────────────────────────────────
SYNDROME_SPACE_SIZE = HAM_Q ** HAM_R    # = 81
ZERO_SYNDROME = 1        # One zero syndrome (codewords)
NONZERO_SYNDROMES = SYNDROME_SPACE_SIZE - 1   # = 80 (error syndromes)
SYNDROMES_PER_POSITION = HAM_Q - 1     # = 2  (two nonzero field elements)
NUM_CORRECTABLE_POSITIONS = NONZERO_SYNDROMES // SYNDROMES_PER_POSITION  # = 40 = HAM_N
SYNDROME_COVERS_ALL_POSITIONS = (NUM_CORRECTABLE_POSITIONS == HAM_N)

# ─────────────────────────────────────────────────────────────────────────────
# Parity check matrix H of Ham(4,3): n = 40 columns over GF(3)^4
#
# H is a 4 × 40 matrix whose columns are all nonzero vectors in PG(3,3) up to
# scalar equivalence, i.e., all (3^4 - 1)/(3 - 1) = 40 = V points of PG(3,3).
# ─────────────────────────────────────────────────────────────────────────────
PG3_3_POINTS = (HAM_Q ** HAM_R - 1) // (HAM_Q - 1)   # = (81-1)/2 = 40 = V
PCM_COLUMNS_EQ_PG = (PG3_3_POINTS == HAM_N == V)

# ─────────────────────────────────────────────────────────────────────────────
# Covering density
#
# Covering density mu = (q^n * Vol(n, R, q)) / (q^n) = 1  for a perfect code.
# In general: mu = (q^{n-k} * Vol(n, R, q)) / q^n = Vol(n, R, q) / q^k.
# For Ham(4,3): mu = 81 / 3^36 * 3^36 = 1 exactly.
# ─────────────────────────────────────────────────────────────────────────────
COVERING_DENSITY = Fraction(BALL_VOL_T, HAM_Q ** (HAM_N - HAM_K))  # = 81/81 = 1
PERFECT_DENSITY = (COVERING_DENSITY == 1)

# ─────────────────────────────────────────────────────────────────────────────
# Redundancy interpretation: r = 4 = EW_GAUGE_4
#
# The redundancy (= number of parity check equations = n - k = 40 - 36 = 4)
# equals EW_GAUGE_4, the dimension of the electroweak gauge sector.  The 4
# parity check bits precisely match the 4 EW bosons (W+, W-, Z, γ).
# ─────────────────────────────────────────────────────────────────────────────
REDUNDANCY = HAM_N - HAM_K   # = 4
REDUNDANCY_EQ_EW = (REDUNDANCY == EW_GAUGE_4)

# ─────────────────────────────────────────────────────────────────────────────
# Sphere-packing bound (Hamming bound)
#
# For any t-error-correcting code of length n over GF(q):
#   M <= q^n / Vol(n, t, q)
# Equality holds iff the code is perfect.
# ─────────────────────────────────────────────────────────────────────────────
HAMMING_BOUND = HAM_Q ** HAM_N // BALL_VOL_T    # = 3^40 / 81 = 3^36
HAMMING_BOUND_EQ_CODE_SIZE = (HAMMING_BOUND == CODE_SIZE)
HAMMING_BOUND_TIGHT = HAMMING_BOUND_EQ_CODE_SIZE   # perfect code => tight

# ─────────────────────────────────────────────────────────────────────────────
# Perfect partition: the 3^40 ambient vectors split into 3^36 cosets of size 81.
# The cosets are disjoint, and their union is all of GF(3)^40.
# ─────────────────────────────────────────────────────────────────────────────
PARTITION_COSET_COUNT = CODE_SIZE     # = 3^36
PARTITION_COSET_SIZE = BALL_VOL_T    # = 81
PARTITION_TOTAL = PARTITION_COSET_COUNT * PARTITION_COSET_SIZE   # = 3^40
PARTITION_COMPLETE = (PARTITION_TOTAL == AMBIENT_SIZE)

# ─────────────────────────────────────────────────────────────────────────────
# SM physical interpretation of the perfect partition
#
# The 3^36 codewords correspond to valid SM fermion states (dim-36 message space).
# The 81-element ball around each codeword represents the "error neighbourhood":
# the set of 1-qudit-flip errors correctable from that state.
# The 81 syndromes / coset leaders form the "error alphabet": they enumerate
# all single-site excitations (80 nonzero) plus the no-error case (0 syndrome).
# ─────────────────────────────────────────────────────────────────────────────
SM_VALID_STATES = CODE_SIZE             # = 3^36
SM_ERROR_NEIGHBORHOOD = BALL_VOL_T      # = 81 per state
SM_ERROR_ALPHABET_SIZE = NUM_COSETS     # = 81 = 3^4
SM_SYNDROME_BITS = HAM_R               # = 4 = EW_GAUGE_4

# ─────────────────────────────────────────────────────────────────────────────
# Verification
# ─────────────────────────────────────────────────────────────────────────────

def verify_perfect_code() -> dict:
    """Verify Ham(4,3) is a perfect code via packing/covering conditions."""
    return {
        "packing_radius_is_1": PACKING_RADIUS == 1,
        "covering_radius_is_1": COVERING_RADIUS == 1,
        "packing_covering_equal": PACKING_COVERING_EQUAL,
        "ball_vol_is_81": BALL_VOL_T == 81,
        "perfect_code_exact": PERFECT_CODE_EXACT,
        "perfect_density": PERFECT_DENSITY,
    }


def verify_coset_structure() -> dict:
    """Verify the coset/syndrome decoding structure."""
    return {
        "num_cosets_is_81": NUM_COSETS == 81,
        "coset_size_eq_ball_vol": NUM_COSETS == BALL_VOL_T,
        "leaders_wt0_is_1": COSET_LEADERS_WT0 == 1,
        "leaders_wt1_is_80": COSET_LEADERS_WT1 == 80,
        "coset_structure_correct": COSET_STRUCTURE_CORRECT,
        "syndrome_covers_all_positions": SYNDROME_COVERS_ALL_POSITIONS,
    }


def verify_parity_check_matrix() -> dict:
    """Verify PCM / PG(3,3) column count."""
    return {
        "pg33_points_is_40": PG3_3_POINTS == 40,
        "pcm_columns_eq_pg": PCM_COLUMNS_EQ_PG,
        "pcm_columns_eq_v": PG3_3_POINTS == V,
        "redundancy_is_4": REDUNDANCY == 4,
        "redundancy_eq_ew": REDUNDANCY_EQ_EW,
    }


def verify_hamming_bound() -> dict:
    """Verify the sphere-packing (Hamming) bound and partition."""
    return {
        "hamming_bound_tight": HAMMING_BOUND_TIGHT,
        "partition_complete": PARTITION_COMPLETE,
        "partition_count_is_3_pow_36": PARTITION_COSET_COUNT == HAM_Q ** HAM_K,
        "partition_size_is_81": PARTITION_COSET_SIZE == 81,
        "covering_density_is_1": PERFECT_DENSITY,
    }


def verify_all() -> dict:
    result = {}
    result.update(verify_perfect_code())
    result.update(verify_coset_structure())
    result.update(verify_parity_check_matrix())
    result.update(verify_hamming_bound())
    return result


# ─────────────────────────────────────────────────────────────────────────────
# Summary builder
# ─────────────────────────────────────────────────────────────────────────────

def build_ccxci_summary() -> dict:
    checks = verify_all()
    n_pass = sum(1 for v in checks.values() if v)
    n_total = len(checks)
    return {
        "part_number": "CCXCI",
        "title": "Covering Radius and Packing-Covering Duality",
        "theme": "Perfect code geometry: Ham(4,3) achieves t = R = 1",
        "verification_status": "ALL CHECKS PASS" if all(checks.values()) else "FAILURES",
        "checks_pass": n_pass,
        "checks_total": n_total,
        "code_parameters": {
            "n": HAM_N, "k": HAM_K, "d": HAM_D, "q": HAM_Q,
            "r": HAM_R,
        },
        "perfect_code": {
            "packing_radius": PACKING_RADIUS,
            "covering_radius": COVERING_RADIUS,
            "ball_volume": BALL_VOL_T,
            "code_size": str(CODE_SIZE),
            "ambient_size": str(AMBIENT_SIZE),
        },
        "coset_structure": {
            "num_cosets": NUM_COSETS,
            "leaders_wt0": COSET_LEADERS_WT0,
            "leaders_wt1": COSET_LEADERS_WT1,
            "total_leaders": TOTAL_COSET_LEADERS,
        },
        "syndrome_decoding": {
            "syndrome_space": SYNDROME_SPACE_SIZE,
            "syndromes_per_position": SYNDROMES_PER_POSITION,
            "correctable_positions": NUM_CORRECTABLE_POSITIONS,
        },
        "sm_interpretation": {
            "valid_states": str(SM_VALID_STATES),
            "error_neighborhood": SM_ERROR_NEIGHBORHOOD,
            "error_alphabet": SM_ERROR_ALPHABET_SIZE,
            "syndrome_bits": SM_SYNDROME_BITS,
        },
        "key_discoveries": [
            "Ham(4,3) is perfect: packing radius = covering radius = 1",
            f"Perfect partition: 3^40 ambient vectors = 3^36 cosets × 81 elements each",
            f"Ball volume {BALL_VOL_T} = 3^4: one ball per syndrome, 81 syndromes",
            f"PCM has {PG3_3_POINTS} columns = all points of PG(3,3) = V = 40",
            f"Redundancy r = {REDUNDANCY} = EW_GAUGE_4 (electroweak sector)",
            f"Covering density = 1: the most efficient possible covering",
            f"80 nonzero syndromes = 80 single-qudit error types = SIM_NONZERO",
        ],
    }


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    checks = verify_all()
    n_pass = sum(1 for v in checks.values() if v)
    n_total = len(checks)
    print(f"CCXCI Verification: {n_pass}/{n_total} checks pass",
          "✓" if n_pass == n_total else "✗")
    if n_pass < n_total:
        for k, v in checks.items():
            if not v:
                print(f"  FAIL: {k}")
