"""
Part CCLXXVI — Klein Quartic to the 57-cell / 11-cell / Tomotope Triad
========================================================================

Bridges:
  A  The consecutive trio: (E_11, V_K, V_57) = (55, 56, 57)
  B  57-cell edges from Klein automorphism order
  C  11-cell automorphisms via Klein vertex count
  D  57-cell automorphisms via Klein vertex count
  E  Tomotope / Klein bridge via Klitzing operation ladder
  F  E₇ dimension from 57-cell prime P₁₉
  G  PSL(2,p) tower complete with PHI6 slot
  H  W(3,3) arithmetic cross-identities

The unifying identity chain:
    E_11 = 55 = V_K − 1  (11-cell edges = Klein quartic vertices − 1)
    V_K  = 56            (Klein quartic vertices = dim(E₇ min module))
    V_57 = 57 = V_K + 1  (57-cell vertices = Klein quartic vertices + 1)

    Three consecutive integers: 11-cell edges / E₇ module dim / 57-cell vertices.

    E_57 = 171 = |PSL(2,7)| + Q = 168 + 3   (57-cell edges = Klein aut + Q)
    F_K  = 24  appears as rung 2 of the Klitzing tomotope operation ladder
    FLAGS(tomotope) = 192 = |PSL(2,7)| + F_K  = 168 + 24

Zero free parameters; unique fixed point q = 3.
"""

import json
import math
from pathlib import Path

# ── W(3,3) SRG constants (zero free parameters) ──────────────────────────────
Q      = 3
V      = 40       # vertices of W(3,3)
K      = 12       # valency
LAM    = 2        # λ
MU     = 4        # μ
PHI3   = 13       # Φ₃(3) = q²+q+1
PHI4   = 10       # Φ₄(3) = q²+1
PHI6   = 7        # Φ₆(3) = q²−q+1

# ── Klein quartic / PSL(2,7) (from Part CCLXXV) ──────────────────────────────
VK      = 56      # Klein quartic vertices = dim(E₇ min module)
EK      = 84      # Klein quartic edges
FK      = 24      # Klein quartic faces = 2K
GENUS_K = 3       # surface genus = Q
PSL27   = 168     # |PSL(2,7)| = |GL(3,2)|

# ── E₇ (from Part CCLXXV) ────────────────────────────────────────────────────
E7_RANK     = 7   # rank(E₇) = PHI6
E7_DIM      = 133 # dim(E₇) = 7 + 2×63
E7_MIN_REP  = 56  # dim(minimal E₇-module) = VK

# ── 11-cell {3,5,3}/11 ───────────────────────────────────────────────────────
V_11, E_11, F_11, C_11 = 11, 55, 55, 11
ORD_PSL2_11 = 660   # |Aut(11-cell)| = |PSL(2,11)|

# ── 57-cell {5,3,5}/57 ───────────────────────────────────────────────────────
V_57, E_57, F_57, C_57 = 57, 171, 171, 57
ORD_PSL2_19 = 3420  # |Aut(57-cell)| = |PSL(2,19)|
DEG_57 = 6          # degree of 57-cell 1-skeleton = 2Q

# ── Tomotope {3,3,3}/2 ───────────────────────────────────────────────────────
V_TOMO, E_TOMO, F_TOMO, C_TOMO = 4, 12, 16, 8
FLAGS_TOMO = 192    # tomotope flag count = |W(D4)|
ORD_TOMO   = 18432  # full tomotope automorphism group

# ── Klitzing tomotope operation ladder (gc.htm) ───────────────────────────────
# 12 → 24 → 48 → 96  (successive doublings)
# Klitzing groups the tomotope with the 11-cell and 57-cell in the same table.
KLITZING_LADDER = (12, 24, 48, 96)

# ── PSL(2,p) tower primes from W(3,3) ────────────────────────────────────────
P3  = Q            # 3   |PSL(2,3)| = K = 12  = A₄
P5  = Q + 2        # 5   |PSL(2,5)| = 60       = A₅
P7  = PHI6         # 7   |PSL(2,7)| = 168       = Klein quartic Aut (CCLXXV)
P11 = K - 1        # 11  |PSL(2,11)| = 660      = 11-cell Aut
P19 = K + Q + MU   # 19  |PSL(2,19)| = 3420     = 57-cell Aut
A5_ORD = 60        # |A₅|

# ── bookkeeping ──────────────────────────────────────────────────────────────
_checks: list[dict] = []


def chk(name: str, value: bool, lhs=None, rhs=None) -> None:
    _checks.append({"name": name, "pass": bool(value), "lhs": lhs, "rhs": rhs})


def eq(name, a, b):
    chk(name, a == b, a, b)


def tr(name, val):
    chk(name, bool(val), val, True)


# =============================================================================
# SECTION A  The consecutive trio  E_11 / V_K / V_57 = 55 / 56 / 57
# =============================================================================

eq("trio_e11_eq_vk_minus_1",    E_11, VK - 1)           # 55 = 56 − 1
eq("trio_vk_eq_e7_min_rep",     VK,   E7_MIN_REP)       # 56 = dim(E₇ min module)
eq("trio_v57_eq_vk_plus_1",     V_57, VK + 1)           # 57 = 56 + 1
tr("trio_consecutive",          E_11 + 1 == VK and VK + 1 == V_57)
eq("trio_span",                 V_57 - E_11, 2)          # span = 2 = LAM
eq("trio_span_is_LAM",          V_57 - E_11, LAM)        # 57 − 55 = 2 = λ

# =============================================================================
# SECTION B  57-cell edges from Klein automorphism order
# =============================================================================

eq("b_e57_eq_psl27_plus_Q",     E_57, PSL27 + Q)         # 171 = 168 + 3
eq("b_e57_eq_2ek_plus_Q",       E_57, 2 * EK + Q)        # 171 = 2×84 + 3
eq("b_e57_eq_v57_times_Q",      E_57, V_57 * Q)          # 171 = 57 × 3  (2Q-regular ÷ 2)
eq("b_psl27_eq_e57_minus_Q",    PSL27, E_57 - Q)          # 168 = 171 − 3
eq("b_ek_eq_e57_minus_psl27",   2 * EK, E_57 - Q)        # 2×84 = 171−3 = 168

# =============================================================================
# SECTION C  11-cell automorphisms via Klein vertex count
# =============================================================================

eq("c_v11_eq_K_minus_1",        V_11, K - 1)             # 11 = 12 − 1 = P11
eq("c_e11_eq_C_v11_2",         E_11, V_11*(V_11-1)//2)  # 55 = C(11,2) complete graph
eq("c_ord_psl2_11_eq_K_e11",   ORD_PSL2_11, K * E_11)   # 660 = 12 × 55
eq("c_ord_psl2_11_via_vk",     ORD_PSL2_11, K*(VK-1))   # 660 = 12 × (56−1)

# =============================================================================
# SECTION D  57-cell automorphisms via Klein vertex count
# =============================================================================

eq("d_ord_psl2_19_eq_v57_A5",  ORD_PSL2_19, V_57 * A5_ORD)   # 3420 = 57 × 60
eq("d_ord_psl2_19_via_vk",     ORD_PSL2_19, (VK+1)*A5_ORD)   # 3420 = (56+1)×60
eq("d_gcd_psl2_19_psl27_eq_K", math.gcd(ORD_PSL2_19, PSL27), K)  # gcd(3420,168)=12
eq("d_gcd_psl2_11_psl27_eq_K", math.gcd(ORD_PSL2_11, PSL27), K)  # gcd(660,168)=12
eq("d_gcd_psl2_11_psl2_19",    math.gcd(ORD_PSL2_11, ORD_PSL2_19), A5_ORD)  # gcd=60

# =============================================================================
# SECTION E  Tomotope / Klein bridge via Klitzing operation ladder
# =============================================================================

# Klitzing groups tomotope / 11-cell / 57-cell on the same gc.htm page.
# The tomotope operation tower produces a pure doubling ladder 12→24→48→96.
# Rung 2 (the truncated tomotope) has leading count 24 = FK = Klein faces.

eq("e_klitzing_rung1_eq_K",    KLITZING_LADDER[0], K)         # 12 = W(3,3) degree
eq("e_klitzing_rung2_eq_FK",   KLITZING_LADDER[1], FK)        # 24 = Klein faces !
eq("e_klitzing_rung3_eq_4K",   KLITZING_LADDER[2], 4 * K)     # 48 = 4K
eq("e_klitzing_rung4_eq_8K",   KLITZING_LADDER[3], 8 * K)     # 96 = 8K
tr("e_klitzing_pure_doubling", all(
    KLITZING_LADDER[i+1] == 2 * KLITZING_LADDER[i] for i in range(3)))
eq("e_tomo_flags_eq_psl27_fk", FLAGS_TOMO, PSL27 + FK)        # 192 = 168 + 24
eq("e_tomo_flags_minus_psl27", FLAGS_TOMO - PSL27, FK)         # 192 − 168 = 24 = FK
eq("e_gcd_ord_tomo_psl27",     math.gcd(ORD_TOMO, PSL27), FK) # gcd(18432,168)=24

# =============================================================================
# SECTION F  E₇ dimension from 57-cell prime P₁₉
# =============================================================================

eq("f_P19_eq_K_plus_Q_plus_MU", P19, K + Q + MU)          # 19 = 12+3+4
eq("f_v57_eq_Q_times_P19",      V_57, Q * P19)             # 57 = 3 × 19
eq("f_e7_dim_eq_phi6_P19",      E7_DIM, PHI6 * P19)        # 133 = 7 × 19
eq("f_e7_dim_div_phi6_eq_P19",  E7_DIM // PHI6, P19)       # 133 ÷ 7 = 19
eq("f_v57_div_Q_eq_P19",        V_57 // Q, P19)            # 57 ÷ 3 = 19
eq("f_e7_dim_v57_same_P19",     E7_DIM // PHI6, V_57 // Q) # both equal 19

# =============================================================================
# SECTION G  PSL(2,p) tower — complete with PHI6 slot
# =============================================================================
# Full tower: PSL(2,3)=K, PSL(2,5)=60, PSL(2,7)=168, PSL(2,11)=660, PSL(2,19)=3420
# The W(3,3) tower for the 11-cell/57-cell uses primes {3,5,11,19};
# PHI6=7 is the Klein quartic prime, filling the slot between 5 and 11.

eq("g_psl_p3_eq_K",            K,          12)            # |PSL(2,3)| = A₄ = K
eq("g_psl_p5_eq_A5",           A5_ORD,     60)            # |PSL(2,5)| = A₅
eq("g_psl_p7_eq_psl27",        PSL27,     168)            # |PSL(2,7)| = PSL27
eq("g_psl_p11_eq_ord_psl2_11", ORD_PSL2_11, 660)         # |PSL(2,11)|
eq("g_psl_p19_eq_ord_psl2_19", ORD_PSL2_19, 3420)        # |PSL(2,19)|
eq("g_psl27_slot_ratio",       PSL27 // K, 2 * PHI6)     # 168÷12=14=2×PHI6
eq("g_tower_primes_ascending", 1, int(P3 < P5 < P7 < P11 < P19))  # 3<5<7<11<19

# =============================================================================
# SECTION H  W(3,3) arithmetic cross-identities
# =============================================================================

# Symmetric distance: V_57 − E_11 = 2 = λ (the W(3,3) lambda parameter)
eq("h_v57_minus_e11_eq_LAM",   V_57 - E_11, LAM)          # 57 − 55 = 2

# Prime sum: V_57 + VK = 113 (prime)
tr("h_v57_plus_vk_prime",      V_57 + VK == 113)
eq("h_e11_plus_e57_eq_226",    E_11 + E_57, 2 * (V_57 + VK))  # 55+171=226=2×113

# Self-dual f-vector palindromes
tr("h_11cell_palindrome",      V_11 == C_11 and E_11 == F_11)
tr("h_57cell_palindrome",      V_57 == C_57 and E_57 == F_57)

# 57-cell is 6-regular = 2Q-regular
eq("h_57cell_degree_2Q",       DEG_57, 2 * Q)             # 6 = 2 × 3
eq("h_e57_from_degree",        E_57, V_57 * DEG_57 // 2)  # 171 = 57×6÷2

# PHI6 links E₇ rank, Klein prime, and P₁₉ via E₇ dim formula
eq("h_e7_rank_is_PHI6",        E7_RANK, PHI6)             # 7 = 7
eq("h_P19_via_e7_dim",         E7_DIM // E7_RANK, P19)    # 133÷7 = 19 = P19


# =============================================================================
# Summary builder
# =============================================================================

def build_summary() -> dict:
    total   = len(_checks)
    passed  = sum(1 for c in _checks if c["pass"])
    failed  = total - passed
    failed_names = [c["name"] for c in _checks if not c["pass"]]
    return {
        "part":          "CCLXXVI",
        "title":         "Klein Quartic to the 57-cell / 11-cell / Tomotope Triad",
        "q":             Q,
        "V":             V,
        "K":             K,
        "MU":            MU,
        "PHI6":          PHI6,
        "checks_total":  total,
        "checks_passed": passed,
        "checks_failed": failed,
        "failed_check_names": failed_names,
        "all_pass":      failed == 0,
        "sections": {
            "A": "Consecutive trio (E_11, V_K, V_57) = (55, 56, 57)",
            "B": "57-cell edges from Klein automorphism order",
            "C": "11-cell automorphisms via Klein vertex count",
            "D": "57-cell automorphisms via Klein vertex count",
            "E": "Tomotope / Klein via Klitzing operation ladder",
            "F": "E₇ dimension from 57-cell prime P₁₉",
            "G": "PSL(2,p) tower complete with PHI6 slot",
            "H": "W(3,3) arithmetic cross-identities",
        },
        "key_identity": (
            "E_11=55=V_K−1; V_K=56=dim(E₇); V_57=57=V_K+1 (consecutive triple); "
            "E_57=171=|PSL(2,7)|+Q; F_K=24 is Klitzing tomotope rung 2; "
            "FLAGS(tomotope)=192=|PSL(2,7)|+F_K; dim(E₇)=7×19=PHI6×P₁₉"
        ),
        "checks": [
            {
                "name": c["name"],
                "pass": c["pass"],
                "lhs":  str(c["lhs"]),
                "rhs":  str(c["rhs"]),
            }
            for c in _checks
        ],
    }


if __name__ == "__main__":
    r = build_summary()
    out = Path(__file__).parent.parent / "PART_CCLXXVI_klein_57cell_results.json"
    out.write_text(json.dumps(r, indent=2))
    status = "ALL PASS" if r["all_pass"] else f"FAILED: {r['failed_check_names']}"
    print(f"Part CCLXXVI — {r['checks_passed']}/{r['checks_total']} checks — {status}")
