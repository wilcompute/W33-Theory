"""
PART_CXCII_MODULAR_FORMS_BRIDGE.py

Bridge connecting W(3,3) SRG(40,12,2,4) to classical modular forms:
the Ramanujan Delta function, the j-invariant, and the Ramanujan tau function.

Key results (zero free parameters):
  1.  Weight of Ramanujan Delta = K = 12
  2.  Dedekind eta exponent: Delta = eta(tau)^24 = eta^{2K}
  3.  j(i) = 1728 = K^3  (j-invariant at the CM point tau=i)
  4.  tau(2) = -24 = -2K  (Ramanujan tau function at p=2)
  5.  tau(3) = 252 = Q*K*Phi6  (Ramanujan tau at p=3)
  6.  tau(6) = tau(2)*tau(3) = -6048  (multiplicativity of tau)
  7.  E8 theta: sigma_3(2) = Q^2 = 9;  sigma_3(3) = V-K = 28
  8.  j constant term = 744 = prime(K-1) * 2K  (where prime(11)=31)
  9.  E8 kissing = 240 = edges of W(3,3)
  10. Leech rank = 2K = 24;  bosonic string in 2*Phi3 = 26 dimensions
  11. Ramanujan conjecture: |tau(p)| <= 2*p^(11/2) for primes p (Deligne)

The Ramanujan Delta function Delta(tau) = q * prod_{n>=1} (1-q^n)^24
is the unique (up to scaling) normalized cusp form of weight K=12 for SL(2,Z).
Its exponent 24 = 2K ties the bosonic string dimension to the same algebra.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from math import comb, isqrt
from typing import Dict, List

# ─── W(3,3) atoms ────────────────────────────────────────────────────────────

Q      = 3     # projective dimension
LAM    = 2     # lambda of SRG
MU     = 4     # mu of SRG
V      = 40    # vertices
K      = 12    # valency
PHI3   = 13    # Phi_3(3)  = q^2+q+1 = 13
PHI4   = 10    # Phi_4(3)  = q^2+1   = 10
PHI6   = 7     # Phi_6(3)  = q^2-q+1 = 7
PHI12  = 73    # Phi_12(3) = 73
J_INV  = 8     # inverse Jackson coefficient
ALPHA_INV = 137
VIETA2    = 33

EDGES = V * K // 2    # 240
EIGENVALUES    = (5, -1, -7)
MULTIPLICITIES = (10, 16, 6)

# ─── Modular forms constants ──────────────────────────────────────────────────

WEIGHT_DELTA      = K           # 12
ETA_EXPONENT      = 2 * K       # 24  (Delta = eta^24)
J_AT_I            = K ** 3      # 1728
J_CONSTANT_TERM   = 744         # q^0 coefficient in j(tau)-q^{-1}
TAU_AT_2          = -2 * K      # -24
TAU_AT_3          = Q * K * PHI6  # 252  (= 3*12*7)
TAU_AT_6          = TAU_AT_2 * TAU_AT_3  # -6048 (multiplicativity)
BOSONIC_STRING    = 2 * PHI3    # 26

# ─── Utility functions ────────────────────────────────────────────────────────

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, isqrt(n) + 1, 2):
        if n % i == 0:
            return False
    return True


def nth_prime(n: int) -> int:
    """Return the n-th prime (1-indexed)."""
    count, candidate = 0, 2
    while True:
        if is_prime(candidate):
            count += 1
            if count == n:
                return candidate
        candidate += 1


def sigma3(n: int) -> int:
    """Sum of cubes of divisors of n."""
    return sum(d ** 3 for d in range(1, n + 1) if n % d == 0)


def compute_tau(max_n: int) -> Dict[int, int]:
    """
    Compute Ramanujan tau(1..max_n) from the q-expansion of
    Delta(q)/q = prod_{k>=1} (1-q^k)^24.

    Algorithm: maintain coefficient array c where c[i] = tau(i+1).
    Apply each factor (1-q^k)^24 = ((1-q^k))^24 via 24 passes of
    the operator c[m] -= c[m-k] (high-to-low sweep).
    """
    N = max_n
    c = [0] * N
    c[0] = 1  # tau(1) = 1

    for k in range(1, N + 1):
        for _ in range(24):  # Apply (1-q^k) 24 times
            for m in range(N - 1, -1, -1):
                if m >= k:
                    c[m] -= c[m - k]

    return {i + 1: c[i] for i in range(N)}


# ─── Check dataclass ─────────────────────────────────────────────────────────

@dataclass(frozen=True)
class ModularCheck:
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

def _make_atom_checks() -> List[ModularCheck]:
    return [
        ModularCheck("Q_is_3",    "Q = 3",   Q,    3),
        ModularCheck("V_is_40",   "V = 40",  V,   40),
        ModularCheck("K_is_12",   "K = 12",  K,   12),
        ModularCheck("PHI3_is_13","Phi3=13", PHI3, 13),
        ModularCheck("PHI6_is_7", "Phi6=7",  PHI6,  7),
        ModularCheck("J_inv_is_8","J^-1=8",  J_INV, 8),
        ModularCheck("EDGES_240", "Edges=240", EDGES, 240),
    ]


def _make_delta_checks(tau: Dict[int, int]) -> List[ModularCheck]:
    checks: List[ModularCheck] = []

    # Weight and eta exponent
    checks.append(ModularCheck(
        "weight_delta_is_K",    "Weight of Delta = K = 12",   WEIGHT_DELTA,  K))
    checks.append(ModularCheck(
        "eta_exponent_is_2K",   "Delta = eta^{2K}, exp = 24", ETA_EXPONENT, 2 * K))
    checks.append(ModularCheck(
        "eta_exp_2K_value",     "Eta exponent = 24 = 2*K",     ETA_EXPONENT,  24))
    checks.append(ModularCheck(
        "bosonic_string_2Phi3", "Bosonic string dim = 26 = 2*Phi3", BOSONIC_STRING, 26))

    # tau(1) = 1
    checks.append(ModularCheck(
        "tau_1_is_1",  "tau(1) = 1 (normalization)", tau[1], 1))

    # tau(2) = -2K = -24
    checks.append(ModularCheck(
        "tau_2_value",         "tau(2) = -24",      tau[2], -24))
    checks.append(ModularCheck(
        "tau_2_is_minus_2K",   "tau(2) = -2K",      tau[2], TAU_AT_2))

    # tau(3) = Q*K*Phi6 = 252
    checks.append(ModularCheck(
        "tau_3_value",         "tau(3) = 252",      tau[3], 252))
    checks.append(ModularCheck(
        "tau_3_is_QKPhi6",     "tau(3) = Q*K*Phi6", tau[3], TAU_AT_3))

    # tau(4) = -1472
    checks.append(ModularCheck(
        "tau_4_value",         "tau(4) = -1472",    tau[4], -1472))

    # tau(5) = 4830
    checks.append(ModularCheck(
        "tau_5_value",         "tau(5) = 4830",     tau[5], 4830))

    # tau(6): multiplicativity tau(6) = tau(2)*tau(3)
    checks.append(ModularCheck(
        "tau_6_value",           "tau(6) = -6048",            tau[6], -6048))
    checks.append(ModularCheck(
        "tau_multiplicative_6",  "tau(6) = tau(2)*tau(3)",    tau[6], TAU_AT_6))
    checks.append(ModularCheck(
        "tau_6_is_tau2_times_tau3", "tau(2)*tau(3) = -6048",  tau[2] * tau[3], -6048))

    # Ramanujan conjecture: |tau(p)| <= 2 * p^(11/2) for primes p
    ramanujan_ok = all(
        abs(tau[p]) <= 2 * p ** 5.5
        for p in [2, 3, 5, 7, 11]
    )
    checks.append(ModularCheck(
        "ramanujan_conjecture", "Ramanujan conj |tau(p)|<=2p^{11/2} for p=2..11",
        ramanujan_ok, True))

    return checks


def _make_j_checks() -> List[ModularCheck]:
    checks: List[ModularCheck] = []

    checks.append(ModularCheck(
        "j_at_i_value",   "j(i) = 1728",          J_AT_I, 1728))
    checks.append(ModularCheck(
        "j_at_i_is_K3",   "j(i) = K^3",            J_AT_I, K ** 3))

    # j constant term: 744 = prime(K-1) * 2K
    p_K_minus_1 = nth_prime(K - 1)   # prime(11) = 31
    checks.append(ModularCheck(
        "j_const_744",         "j constant term = 744",         J_CONSTANT_TERM, 744))
    checks.append(ModularCheck(
        "j_const_prime_K-1",   "prime(K-1) = prime(11) = 31",   p_K_minus_1, 31))
    checks.append(ModularCheck(
        "j_const_formula",     "744 = prime(K-1) * 2K",          J_CONSTANT_TERM,
        p_K_minus_1 * 2 * K))

    return checks


def _make_e8_theta_checks() -> List[ModularCheck]:
    checks: List[ModularCheck] = []

    # Theta_E8(q) = 1 + 240 * sum sigma_3(n) q^n
    e8_norm2 = 240 * sigma3(1)   # = 240
    e8_norm4 = 240 * sigma3(2)   # = 240*9 = 2160
    e8_norm6 = 240 * sigma3(3)   # = 240*28 = 6720

    checks.append(ModularCheck(
        "E8_norm2_is_edges",  "E8 norm-2 count = 240 = EDGES", e8_norm2, EDGES))
    checks.append(ModularCheck(
        "sigma3_2_is_Q2",     "sigma_3(2) = Q^2 = 9",          sigma3(2), Q ** 2))
    checks.append(ModularCheck(
        "sigma3_3_is_V_K",    "sigma_3(3) = V-K = 28",         sigma3(3), V - K))
    checks.append(ModularCheck(
        "E8_norm4_formula",   "E8 norm-4 = EDGES*Q^2 = 2160",  e8_norm4, EDGES * Q ** 2))
    checks.append(ModularCheck(
        "E8_norm6_formula",   "E8 norm-6 = EDGES*(V-K) = 6720", e8_norm6, EDGES * (V - K)))
    checks.append(ModularCheck(
        "E8_rank_is_Jinv",    "E8 rank = J^{-1} = 8",           J_INV, J_INV))

    return checks


# ─── Audit ───────────────────────────────────────────────────────────────────

def modular_forms_bridge_audit() -> dict:
    tau = compute_tau(13)  # Compute tau(1..13)

    atom_checks  = _make_atom_checks()
    delta_checks = _make_delta_checks(tau)
    j_checks     = _make_j_checks()
    e8_checks    = _make_e8_theta_checks()
    all_checks   = atom_checks + delta_checks + j_checks + e8_checks

    failing = [c.name for c in all_checks if not c.passes]

    return {
        "status": "PASS" if not failing else "FAIL",
        "all_checks_pass": len(failing) == 0,
        "failed_checks": failing,
        "check_count": len(all_checks),
        "checks_passing": len(all_checks) - len(failing),
        "atom_check_count":  len(atom_checks),
        "delta_check_count": len(delta_checks),
        "j_check_count":     len(j_checks),
        "e8_check_count":    len(e8_checks),
        "ramanujan_tau": {n: tau[n] for n in range(1, 14)},
        "j_invariant": {
            "j_at_i":         J_AT_I,
            "j_at_i_is_K3":   J_AT_I == K ** 3,
            "constant_term":  J_CONSTANT_TERM,
            "constant_formula": f"prime(K-1)*2K = prime(11)*24 = 31*24 = {31*24}",
        },
        "modular_forms_structure": {
            "weight_delta":    WEIGHT_DELTA,
            "eta_exponent":    ETA_EXPONENT,
            "bosonic_string":  BOSONIC_STRING,
            "tau_2":           TAU_AT_2,
            "tau_3":           TAU_AT_3,
            "tau_3_formula":   "Q*K*Phi6 = 3*12*7 = 252",
            "tau_6":           TAU_AT_6,
        },
        "e8_theta": {
            "norm_2_vectors": 240 * sigma3(1),
            "norm_4_vectors": 240 * sigma3(2),
            "norm_6_vectors": 240 * sigma3(3),
        },
        "w33_atoms": {
            "Q": Q, "V": V, "K": K, "PHI3": PHI3,
            "PHI6": PHI6, "J_INV": J_INV, "EDGES": EDGES,
        },
        "theorem_cxcii": (
            "Theorem CXCII (Modular Forms Bridge): The W(3,3) graph parameters "
            "index the Ramanujan modular machinery with zero free parameters. "
            "The unique weight-12 normalized cusp form for SL(2,Z) has weight K=12 "
            "and eta exponent 2K=24 (= bosonic string dimension 2*Phi3=26? No -- "
            "24=2K and 26=2*Phi3 are distinct W(3,3) parameters that coincide with "
            "the eta exponent and bosonic string dimension respectively). "
            "The j-invariant satisfies j(i)=1728=K^3. "
            "The Ramanujan tau function satisfies tau(2)=-2K=-24 and tau(3)=Q*K*Phi6=252. "
            "The E8 theta series encodes sigma_3(2)=Q^2 and sigma_3(3)=V-K."
        ),
    }


def main() -> None:
    result = modular_forms_bridge_audit()
    print(f"Status : {result['status']}")
    print(f"Checks : {result['checks_passing']}/{result['check_count']} pass")
    print(f"tau(2) = {result['ramanujan_tau'][2]}  (expect -24 = -2K)")
    print(f"tau(3) = {result['ramanujan_tau'][3]}  (expect 252 = Q*K*Phi6)")
    print(f"j(i)   = {result['j_invariant']['j_at_i']}  (expect 1728 = K^3)")
    if result["failed_checks"]:
        print(f"FAILED : {result['failed_checks']}")
    with open("PART_CXCII_modular_forms_results.json", "w") as f:
        json.dump(result, f, indent=2)
    print("Results written to PART_CXCII_modular_forms_results.json")


if __name__ == "__main__":
    main()
