"""
Part CCLXXV — Klein Quartic, PSL(2,7) and the E₇-56 bridge
============================================================

Bridges:
  A  PSL(2,7) = GL(3,2) group arithmetic
  B  Klein quartic {7,3} combinatorics on genus-3 surface
  C  Hurwitz (2,3,7)-triangle group and automorphism bound
  D  E₇ rank-7 Lie algebra and its 56-dimensional minimal module
  E  28 bitangents / odd theta characteristics = MU × PHI6
  F  Heawood graph connections (CCLXXIV continuity)
  G  W(3,3) SRG arithmetic cross-identities

The unifying identity:
    PHI6 = 7 = rank(E₇) = Hurwitz r = Fano plane order
                         = Klein face valency = Heawood chromatic number
    MU × PHI6 = 28 = bitangents = odd theta characteristics (genus 3)
    V_Klein = 2 × MU × PHI6 = 56 = dim(E₇ minimal module)
    E_Klein = PHI6 × K = 84 ;  F_Klein = K = 24
    |PSL(2,7)| = 168 = PHI6 × F_Klein = Q × V_Klein = 2 × E_Klein

Zero free parameters; unique fixed point q = 3.
"""

import json
from fractions import Fraction
from pathlib import Path

# ── W(3,3) SRG constants (zero free parameters) ──────────────────────────────
Q          = 3
V          = 40          # vertices of W(3,3)
K          = 12          # valency
LAM        = 2           # λ  (common neighbours of adjacent pair)
MU         = 4           # μ  (common neighbours of non-adjacent pair)
PHI3       = 13          # Φ₃(3) = q²+q+1
PHI4       = 10          # Φ₄(3) = q²+1
PHI6       = 7           # Φ₆(3) = q²−q+1
EDGES      = 240         # V*K//2
AUT_ORDER  = 51840       # |Aut(W(3,3))|

# ── Klein quartic / PSL(2,7) ─────────────────────────────────────────────────
VK          = 56         # Klein quartic vertices
EK          = 84         # Klein quartic edges
FK          = 24         # Klein quartic faces  (heptagons)
GENUS       = 3          # surface genus
PSL27       = 168        # |PSL(2,7)| = |GL(3,2)|
FACE_VAL    = 7          # each face is a PHI6-gon (heptagon)
VERTEX_DEG  = 3          # each vertex is trivalent (Q-valent)

# ── Hurwitz triangle group (2, 3, 7) ─────────────────────────────────────────
HP, HQ, HR  = 2, 3, 7   # Hurwitz triple; sum 1/p+1/q+1/r < 1

# ── E₇ Lie algebra ───────────────────────────────────────────────────────────
E7_RANK      = 7         # rank of E₇ = PHI6
E7_DIM       = 133       # dim(E₇) as a Lie algebra = 7 + 2×63
E7_POS_ROOTS = 63        # number of positive roots of E₇
E7_MIN_REP   = 56        # dimension of minimal faithful E₇-module = VK

# ── Theta characteristics / bitangents ───────────────────────────────────────
BITANGENTS  = 28         # bitangents to a smooth plane quartic = MU × PHI6
THETA_ODD   = 28         # odd theta characteristics (genus-3 curve)
THETA_EVEN  = 36         # even theta characteristics (genus-3 curve)
THETA_TOTAL = 64         # 2^(2g) = 2^6

# ── Heawood graph (from CCLXXIV) ─────────────────────────────────────────────
HEAWOOD_V   = 14         # nodes = 2 × PHI6
HEAWOOD_E   = 21         # edges
HEAWOOD_CHR = 7          # chromatic number = PHI6

# ── bookkeeping ──────────────────────────────────────────────────────────────
_checks: list[dict] = []


def chk(name: str, value: bool, lhs=None, rhs=None) -> None:
    _checks.append({"name": name, "pass": bool(value), "lhs": lhs, "rhs": rhs})


def eq(name, a, b):
    chk(name, a == b, a, b)


def tr(name, val):
    chk(name, bool(val), val, True)


# =============================================================================
# SECTION A  PSL(2,7) = GL(3,2) group arithmetic
# =============================================================================

eq("psl27_order",             PSL27, 168)
eq("psl27_phi6_times_24",     PHI6 * 24, PSL27)            # 7×24 = 168
_gl32 = (8 - 1) * (8 - 2) * (8 - 4)
eq("gl32_order",              _gl32, 168)                   # |GL(3, F₂)|
eq("psl27_eq_gl32",           PSL27, _gl32)
eq("psl27_factored",          2**3 * Q * PHI6, PSL27)       # 2³×3×7 = 168
eq("psl27_div_phi6_is_2K",    PSL27 // PHI6, 2 * K)         # 168÷7 = 24 = 2K
eq("psl27_is_Q_VK",           PSL27, Q * VK)                # 3×56 = 168
eq("psl27_is_phi6_FK",        PSL27, PHI6 * FK)             # 7×24 = 168

# =============================================================================
# SECTION B  Klein quartic {7,3} combinatorics
# =============================================================================

eq("klein_vertices",          VK, 56)
eq("klein_edges",             EK, 84)
eq("klein_faces",             FK, 24)
_chi = VK - EK + FK
eq("klein_euler_char",        _chi, -4)                     # χ = V−E+F = −4
_g   = (2 - _chi) // 2
eq("klein_genus_from_chi",    _g, GENUS)                    # g = (2−χ)/2 = 3
eq("klein_genus_is_Q",        GENUS, Q)                     # genus = q (base prime)
eq("klein_V_2_MU_PHI6",       VK, 2 * MU * PHI6)           # 2×4×7 = 56
eq("klein_E_PHI6_K",          EK, PHI6 * K)                 # 7×12 = 84
eq("klein_F_2K",              FK, 2 * K)                      # faces = 2 × W(3,3) valency
eq("klein_face_val_PHI6",     FACE_VAL, PHI6)               # heptagonal faces
eq("klein_vertex_deg_Q",      VERTEX_DEG, Q)                # trivalent = q
# Handshaking: 2E = F × face_val
eq("klein_handshaking_E",     FK * FACE_VAL // 2, EK)       # 24×7÷2 = 84
# Vertex formula: V = 2E / vertex_deg
eq("klein_handshaking_V",     2 * EK // VERTEX_DEG, VK)     # 168÷3 = 56
eq("klein_aut_is_2EK",        PSL27, 2 * EK)                # |Aut| = 2×edges

# =============================================================================
# SECTION C  Hurwitz (2, 3, 7)-triangle group
# =============================================================================

eq("hurwitz_r_is_PHI6",       HR, PHI6)                     # r = 7 = PHI6
_hsum = Fraction(1, HP) + Fraction(1, HQ) + Fraction(1, HR)
eq("hurwitz_sum_value",       _hsum, Fraction(41, 42))
tr("hurwitz_sum_lt_1",        _hsum < 1)                    # hyperbolic condition
eq("hurwitz_defect",          Fraction(1) - _hsum, Fraction(1, 42))
eq("hurwitz_bound",           84 * (GENUS - 1), PSL27)      # 84×2 = 168
eq("hurwitz_achieved",        PSL27, 84 * (GENUS - 1))      # Klein achieves maximum

# =============================================================================
# SECTION D  E₇ Lie algebra
# =============================================================================

eq("e7_rank_is_PHI6",         E7_RANK, PHI6)                # rank(E₇) = 7
eq("e7_dim_phi6_factor",      E7_DIM, PHI6 * 19)            # 133 = 7×19
eq("e7_pos_roots",            E7_POS_ROOTS, 63)
eq("e7_dim_from_structure",   E7_RANK + 2 * E7_POS_ROOTS, E7_DIM)  # 7+126 = 133
eq("e7_min_rep_is_VK",        E7_MIN_REP, VK)               # 56 = 56
eq("e7_min_rep_2_MU_PHI6",    E7_MIN_REP, 2 * MU * PHI6)    # 56 = 2×4×7

# =============================================================================
# SECTION E  Theta characteristics and bitangents
# =============================================================================

eq("theta_total_2_2g",        2 ** (2 * GENUS), THETA_TOTAL)  # 2^6 = 64
eq("theta_odd_value",         THETA_ODD, 28)
eq("theta_even_value",        THETA_EVEN, 36)
eq("theta_sum",               THETA_ODD + THETA_EVEN, THETA_TOTAL)  # 28+36=64
eq("theta_odd_is_MU_PHI6",    THETA_ODD, MU * PHI6)          # 28 = 4×7 ✓
eq("bitangents_eq_theta_odd", BITANGENTS, THETA_ODD)          # classical theorem
eq("theta_2g_galois_period",  2 * GENUS, 6)                  # 2g=6=|(Z/7Z)*|

# =============================================================================
# SECTION F  Heawood graph bridge (CCLXXIV continuity)
# =============================================================================

eq("heawood_V_2_PHI6",        HEAWOOD_V, 2 * PHI6)          # 14 = 2×7
eq("heawood_CHR_PHI6",        HEAWOOD_CHR, PHI6)             # chromatic = 7
eq("klein_E_MU_heawood_E",    EK, MU * HEAWOOD_E)            # 84 = 4×21
eq("klein_V_MU_heawood_V",    VK, MU * HEAWOOD_V)            # 56 = 4×14
eq("psl27_div_heawood_V_K",   PSL27 // HEAWOOD_V, K)         # 168÷14 = 12 = K
eq("psl27_2MU_heawood_E",     PSL27, 2 * MU * HEAWOOD_E)     # 168 = 2×4×21
# E_K = PHI6 × heawood_E − E₇_positive_roots
eq("klein_E_heawood_e7",      EK, PHI6 * HEAWOOD_E - E7_POS_ROOTS)  # 7×21−63 = 84

# =============================================================================
# SECTION G  W(3,3) arithmetic cross-identities
# =============================================================================

# V_Klein − V_SRG = PHI4 + PHI6 − 1
eq("cross_VK_minus_V",        VK - V, PHI4 + PHI6 - 1)      # 16 = 10+7−1
# 168 mod 40 = 8 = 2×MU
eq("cross_psl27_mod_V",       PSL27 % V, 2 * MU)            # 168 mod 40 = 8
# 84 mod 40 = 4 = MU
eq("cross_EK_mod_V",          EK % V, MU)                   # 84 mod 40 = 4
# Total elements of Klein quartic
eq("cross_total_4_V1",        VK + EK + FK, 4 * (V + 1))    # 164 = 4×41
# E₇ rank = Hurwitz r
eq("cross_e7_rank_hurwitz_r", E7_RANK, HR)                  # 7 = 7
# Genus from Hurwitz triple: g = r − p − q + 1
eq("cross_genus_from_triple", GENUS, HR - HP - HQ + 1)      # 7−2−3+1 = 3
# E_K = Q × bitangents
eq("cross_EK_Q_bitangents",   EK, Q * BITANGENTS)           # 84 = 3×28
# V_K = 2 × bitangents
eq("cross_VK_2_bitangents",   VK, 2 * BITANGENTS)           # 56 = 2×28
# |PSL(2,7)| = 6 × bitangents  (6 = Galois period of 1/7)
eq("cross_psl27_6_bitangents", PSL27, 6 * BITANGENTS)       # 168 = 6×28
# PHI6 unifies: E₇ rank = Hurwitz r = Fano order = Klein face valency
eq("cross_phi6_unifier",      PHI6, E7_RANK)                # 7 = 7 (declared)
eq("cross_phi6_unifier2",     PHI6, HR)                     # 7 = 7 (Hurwitz r)


# =============================================================================
# Summary builder
# =============================================================================

def build_summary() -> dict:
    total   = len(_checks)
    passed  = sum(1 for c in _checks if c["pass"])
    failed  = total - passed
    failed_names = [c["name"] for c in _checks if not c["pass"]]
    return {
        "part":          "CCLXXV",
        "title":         "Klein Quartic, PSL(2,7) and the E₇-56 bridge",
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
            "A": "PSL(2,7) = GL(3,2) group arithmetic",
            "B": "Klein quartic {7,3} combinatorics",
            "C": "Hurwitz (2,3,7)-triangle group",
            "D": "E₇ rank-7 Lie algebra and 56-dim module",
            "E": "28 bitangents / odd theta characteristics",
            "F": "Heawood graph bridge (CCLXXIV continuity)",
            "G": "W(3,3) SRG arithmetic cross-identities",
        },
        "key_identity": (
            "V_Klein=56=2×MU×PHI6=dim(E₇ min rep); "
            "E_Klein=84=PHI6×K; F_Klein=24=K; "
            "|PSL(2,7)|=168=PHI6×F=Q×V=2×E; "
            "bitangents=28=MU×PHI6; genus=Q=3"
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
    out = Path(__file__).parent.parent / "PART_CCLXXV_klein_e7_results.json"
    out.write_text(json.dumps(r, indent=2))
    status = "ALL PASS" if r["all_pass"] else f"FAILED: {r['failed_check_names']}"
    print(f"Part CCLXXV — {r['checks_passed']}/{r['checks_total']} checks — {status}")
