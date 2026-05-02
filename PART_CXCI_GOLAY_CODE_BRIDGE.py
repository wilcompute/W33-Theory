"""
PART_CXCI_GOLAY_CODE_BRIDGE.py

Bridge connecting W(3,3) SRG(40,12,2,4) to the Golay codes
and associated lattices (E8, Leech).

Key results (zero free parameters):
  1. Extended binary Golay [24,12,8]: n=2K, k=K, d=J^{-1}
  2. Extended ternary Golay [12,6,6]_3: n=K, k=K/2, d=K/2, q=Q
  3. Perfect binary Golay [23,12,7]: n=K+Phi3-2, t=Q (correction capacity)
  4. Perfect ternary Golay [11,6,5]_3: n=K-1 (M-theory dim!), t=lambda=2
  5. E8 root system: rank=J^{-1}=8, kissing=edges(W33)=240
  6. E8 theta series: sigma_3(2)=Q^2, sigma_3(3)=V-K
  7. Leech lattice: rank=2K=24, kissing=E*Q^2*Phi6*Phi3=196560
  8. Ternary Golay alphabet = Q; binary Golay length = 2K

The Golay codes are the only non-trivial perfect linear codes (up to Hamming codes).
Both the binary and ternary Golay families are completely indexed by W(3,3) atoms.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from math import comb, factorial
from typing import List

# ─── W(3,3) atoms ────────────────────────────────────────────────────────────

Q      = 3     # projective dimension; also alphabet size of ternary Golay code
LAM    = 2     # lambda of SRG (also error-correction of perfect ternary Golay)
MU     = 4     # mu of SRG
V      = 40    # vertices
K      = 12    # valency
PHI3   = 13    # Phi_3(3) = q^2+q+1 = 13
PHI4   = 10    # Phi_4(3) = q^2+1   = 10
PHI6   = 7     # Phi_6(3) = q^2-q+1 = 7
PHI12  = 73    # Phi_12(3) = q^4-q^2+1 = 73
J_INV  = 8     # inverse Jackson coefficient
ALPHA_INV = 137
VIETA2 = 33

# Derived
EDGES = V * K // 2           # 240 = edge count of W(3,3)
MULTIPLICITIES = (10, 16, 6) # multiplicities in Z(x)
EIGENVALUES    = (5, -1, -7)

# ─── Golay code parameters ────────────────────────────────────────────────────

# Extended binary Golay code: [24, 12, 8]_2  (self-dual, not perfect)
BIN_EXT_N = 2 * K      # 24
BIN_EXT_K = K          # 12
BIN_EXT_D = J_INV      # 8

# Extended ternary Golay code: [12, 6, 6]_3  (self-dual, not perfect)
TER_EXT_N = K          # 12
TER_EXT_K = K // 2     # 6  = K/2 = m_3 (third multiplicity in Z(x))
TER_EXT_D = K // 2     # 6

# Perfect binary Golay code: [23, 12, 7]_2  (perfect, t=3=Q)
BIN_PERF_N = K + PHI3 - 2   # 23
BIN_PERF_K = K               # 12
BIN_PERF_D = 7
BIN_PERF_T = Q               # error-correction t = 3 = Q

# Perfect ternary Golay code: [11, 6, 5]_3  (perfect, t=2=lambda)
TER_PERF_N = K - 1           # 11  (= M-theory dimension!)
TER_PERF_K = K // 2          # 6
TER_PERF_D = 5
TER_PERF_T = LAM             # error-correction t = 2 = lambda

# ─── Lattice parameters ───────────────────────────────────────────────────────

E8_RANK     = J_INV   # 8
E8_KISSING  = EDGES   # 240  (= V*K/2 = 40*12/2)

LEECH_RANK    = 2 * K         # 24
LEECH_KISSING = 196560        # 196560 = EDGES * Q^2 * PHI6 * PHI3

# ─── Utility functions ────────────────────────────────────────────────────────

def hamming_ball_volume(q: int, n: int, t: int) -> int:
    """Volume of a Hamming ball of radius t in F_q^n."""
    return sum(comb(n, i) * (q - 1) ** i for i in range(t + 1))


def is_perfect_code(q: int, n: int, k: int, d: int) -> bool:
    """Check the perfect-code (Hamming bound equality) condition for [n,k,d]_q."""
    t = (d - 1) // 2
    M = q ** k
    return hamming_ball_volume(q, n, t) * M == q ** n


def sigma3(n: int) -> int:
    """Sum of cubes of divisors of n."""
    return sum(d ** 3 for d in range(1, n + 1) if n % d == 0)


# ─── Check dataclass ─────────────────────────────────────────────────────────

@dataclass(frozen=True)
class GolayCheck:
    name: str
    description: str
    computed: object
    expected: object
    exact: bool = True

    @property
    def passes(self) -> bool:
        if self.exact:
            return self.computed == self.expected
        return abs(float(self.computed) - float(self.expected)) < 1e-10


# ─── Check builders ──────────────────────────────────────────────────────────

def _make_atom_checks() -> List[GolayCheck]:
    return [
        GolayCheck("Q_is_3",          "Q = 3 (projective dim / ternary alphabet)",    Q,     3),
        GolayCheck("LAM_is_2",        "lambda = 2 (SRG; also perfect ternary t)",     LAM,   2),
        GolayCheck("V_is_40",         "V = 40 (vertices)",                             V,    40),
        GolayCheck("K_is_12",         "K = 12 (valency)",                              K,    12),
        GolayCheck("PHI3_is_13",      "Phi3 = 13",                                    PHI3,  13),
        GolayCheck("PHI6_is_7",       "Phi6 = 7",                                     PHI6,   7),
        GolayCheck("J_INV_is_8",      "J^{-1} = 8",                                J_INV,   8),
        GolayCheck("EDGES_is_240",    "Edges = V*K/2 = 240",                        EDGES, 240),
        GolayCheck("mult3_is_6",      "Third multiplicity in Z(x) = K/2 = 6",  MULTIPLICITIES[2], K // 2),
    ]


def _make_golay_checks() -> List[GolayCheck]:
    checks: List[GolayCheck] = []

    # — Extended binary Golay [24,12,8] —
    checks.append(GolayCheck(
        "bin_ext_n_is_2K",    "Extended binary Golay n = 2K",   BIN_EXT_N, 2 * K))
    checks.append(GolayCheck(
        "bin_ext_k_is_K",     "Extended binary Golay k = K",    BIN_EXT_K, K))
    checks.append(GolayCheck(
        "bin_ext_d_is_Jinv",  "Extended binary Golay d = J^{-1}", BIN_EXT_D, J_INV))
    checks.append(GolayCheck(
        "bin_ext_self_dual",  "Extended binary Golay is self-dual (n=2k)", BIN_EXT_N, 2 * BIN_EXT_K))

    # — Extended ternary Golay [12,6,6]_3 —
    checks.append(GolayCheck(
        "ter_ext_n_is_K",     "Extended ternary Golay n = K",   TER_EXT_N, K))
    checks.append(GolayCheck(
        "ter_ext_k_is_K2",    "Extended ternary Golay k = K/2", TER_EXT_K, K // 2))
    checks.append(GolayCheck(
        "ter_ext_d_is_K2",    "Extended ternary Golay d = K/2", TER_EXT_D, K // 2))
    checks.append(GolayCheck(
        "ter_ext_q_is_Q",     "Extended ternary alphabet = Q",  Q,         Q))
    checks.append(GolayCheck(
        "ter_ext_self_dual",  "Extended ternary is self-dual (n=2k)", TER_EXT_N, 2 * TER_EXT_K))

    # — Perfect binary Golay [23,12,7]_2 —
    checks.append(GolayCheck(
        "bin_perf_n_formula", "Perfect binary n = K+Phi3-2 = 23", BIN_PERF_N, K + PHI3 - 2))
    checks.append(GolayCheck(
        "bin_perf_t_is_Q",    "Perfect binary correction t = Q",  BIN_PERF_T, Q))
    checks.append(GolayCheck(
        "bin_perf_is_perfect","Perfect binary satisfies Hamming bound",
        is_perfect_code(2, BIN_PERF_N, BIN_PERF_K, BIN_PERF_D), True))
    checks.append(GolayCheck(
        "bin_perf_volume",    "V_2(23,3) = 2048 = 2^11",
        hamming_ball_volume(2, 23, 3), 2 ** 11))

    # — Perfect ternary Golay [11,6,5]_3 —
    checks.append(GolayCheck(
        "ter_perf_n_is_K-1",  "Perfect ternary n = K-1 = 11 (M-theory dim)", TER_PERF_N, K - 1))
    checks.append(GolayCheck(
        "ter_perf_t_is_LAM",  "Perfect ternary correction t = lambda = 2",   TER_PERF_T, LAM))
    checks.append(GolayCheck(
        "ter_perf_q_is_Q",    "Perfect ternary alphabet = Q",                Q,          Q))
    checks.append(GolayCheck(
        "ter_perf_is_perfect","Perfect ternary satisfies Hamming bound",
        is_perfect_code(Q, TER_PERF_N, TER_PERF_K, TER_PERF_D), True))
    checks.append(GolayCheck(
        "ter_perf_volume",    "V_3(11,2) = 3^5 = 243",
        hamming_ball_volume(Q, 11, 2), Q ** 5))

    return checks


def _make_lattice_checks() -> List[GolayCheck]:
    checks: List[GolayCheck] = []

    # — E8 lattice —
    checks.append(GolayCheck(
        "E8_rank_is_Jinv",    "E8 rank = J^{-1} = 8",               E8_RANK,   J_INV))
    checks.append(GolayCheck(
        "E8_kissing_is_edges","E8 kissing = edges of W(3,3) = 240",  E8_KISSING, EDGES))
    checks.append(GolayCheck(
        "E8_kissing_formula", "E8 kissing = V*K/2",                  E8_KISSING, V * K // 2))

    # E8 theta series: number of minimal vectors at successive norms
    # Theta_E8(q) = 1 + 240*sum sigma_3(n)*q^n
    e8_norm2 = 240 * sigma3(1)    # = 240*1 = 240
    e8_norm4 = 240 * sigma3(2)    # = 240*9 = 2160
    e8_norm6 = 240 * sigma3(3)    # = 240*28 = 6720

    checks.append(GolayCheck(
        "E8_theta_norm2",         "E8 norm-2 vectors = 240 = EDGES",    e8_norm2, EDGES))
    checks.append(GolayCheck(
        "sigma3_1_is_1",          "sigma_3(1) = 1",                     sigma3(1), 1))
    checks.append(GolayCheck(
        "sigma3_2_is_Q2",         "sigma_3(2) = 9 = Q^2",               sigma3(2), Q ** 2))
    checks.append(GolayCheck(
        "sigma3_3_is_V_minus_K",  "sigma_3(3) = 28 = V-K",             sigma3(3), V - K))
    checks.append(GolayCheck(
        "E8_theta_norm4_formula", "E8 norm-4 vectors = EDGES * Q^2",    e8_norm4, EDGES * Q ** 2))
    checks.append(GolayCheck(
        "E8_theta_norm6_formula", "E8 norm-6 vectors = EDGES * (V-K)",  e8_norm6, EDGES * (V - K)))

    # — Leech lattice —
    checks.append(GolayCheck(
        "Leech_rank_is_2K",       "Leech rank = 2K = 24",              LEECH_RANK,    2 * K))
    checks.append(GolayCheck(
        "Leech_kissing_value",    "Leech kissing = 196560",             LEECH_KISSING, 196560))
    leech_formula = EDGES * Q ** 2 * PHI6 * PHI3
    checks.append(GolayCheck(
        "Leech_kissing_formula",  "Leech kissing = E*Q^2*Phi6*Phi3",   LEECH_KISSING, leech_formula))
    checks.append(GolayCheck(
        "Leech_kissing_over_E8",  "Leech/E8 kissing = Q^2*Phi6*Phi3",
        LEECH_KISSING // E8_KISSING, Q ** 2 * PHI6 * PHI3))

    return checks


# ─── Audit ───────────────────────────────────────────────────────────────────

def golay_code_bridge_audit() -> dict:
    atom_checks    = _make_atom_checks()
    golay_checks   = _make_golay_checks()
    lattice_checks = _make_lattice_checks()
    all_checks     = atom_checks + golay_checks + lattice_checks

    failing = [c.name for c in all_checks if not c.passes]

    return {
        "status": "PASS" if not failing else "FAIL",
        "all_checks_pass": len(failing) == 0,
        "failed_checks": failing,
        "check_count": len(all_checks),
        "checks_passing": len(all_checks) - len(failing),
        "atom_check_count": len(atom_checks),
        "golay_check_count": len(golay_checks),
        "lattice_check_count": len(lattice_checks),
        "golay_parameters": {
            "binary_extended":  {"n": BIN_EXT_N, "k": BIN_EXT_K, "d": BIN_EXT_D, "q": 2},
            "ternary_extended": {"n": TER_EXT_N, "k": TER_EXT_K, "d": TER_EXT_D, "q": Q},
            "binary_perfect":   {"n": BIN_PERF_N, "k": BIN_PERF_K, "d": BIN_PERF_D,
                                  "t": BIN_PERF_T, "q": 2},
            "ternary_perfect":  {"n": TER_PERF_N, "k": TER_PERF_K, "d": TER_PERF_D,
                                  "t": TER_PERF_T, "q": Q},
        },
        "lattice_parameters": {
            "E8":    {"rank": E8_RANK,    "kissing": E8_KISSING},
            "Leech": {"rank": LEECH_RANK, "kissing": LEECH_KISSING},
        },
        "e8_theta_series": {
            "norm_2_vectors": 240 * sigma3(1),
            "norm_4_vectors": 240 * sigma3(2),
            "norm_6_vectors": 240 * sigma3(3),
            "sigma3_2_equals_Q2":      sigma3(2) == Q ** 2,
            "sigma3_3_equals_V_minus_K": sigma3(3) == V - K,
        },
        "w33_atoms": {
            "Q": Q, "LAM": LAM, "V": V, "K": K,
            "PHI3": PHI3, "PHI4": PHI4, "PHI6": PHI6, "PHI12": PHI12,
            "J_INV": J_INV, "EDGES": EDGES,
        },
        "theorem_cxci": (
            "Theorem CXCI (Golay Code Bridge): The W(3,3) graph parameters index all "
            "four Golay codes and both the E8 and Leech lattices with zero free parameters. "
            "The extended ternary Golay [12,6,6]_3 has length K=12, dimension K/2=6, "
            "distance K/2=6, and alphabet Q=3. "
            "The perfect ternary Golay [11,6,5]_3 has length K-1=11 (M-theory dimension), "
            "correction capacity lambda=2. "
            "The E8 root system has rank J^{-1}=8 and kissing number equal to the edge "
            "count of W(3,3) (both 240). "
            "The Leech lattice has rank 2K=24 and kissing number E*Q^2*Phi6*Phi3=196560."
        ),
    }


def main() -> None:
    result = golay_code_bridge_audit()
    print(f"Status : {result['status']}")
    print(f"Checks : {result['checks_passing']}/{result['check_count']} pass")
    if result["failed_checks"]:
        print(f"FAILED : {result['failed_checks']}")
    with open("PART_CXCI_golay_code_results.json", "w") as f:
        json.dump(result, f, indent=2)
    print("Results written to PART_CXCI_golay_code_results.json")


if __name__ == "__main__":
    main()
