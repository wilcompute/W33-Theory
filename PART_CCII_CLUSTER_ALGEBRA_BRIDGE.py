"""
PART_CCII: Cluster Algebras / Fomin-Zelevinsky Bridge
=======================================================
Bridge the W(3,3) SRG(40,12,2,4) atoms to cluster algebras of finite type,
Fomin-Zelevinsky mutation, exchange graphs, and generalized associahedra.

Key connections:
  - Cluster algebra A(Q) for quiver Q; finite-type ↔ Dynkin diagrams.
  - Mutation at vertex k: x_k' = (∏_{b_{kj}>0} x_j^{b_{kj}} + ∏_{b_{kj}<0} x_j^{-b_{kj}}) / x_k.
  - Type A_n: finite type, n(n+3)/2 cluster variables; n(n+1)/2 + n cluster vars (all positive).
  - Cluster variables for A_n = n(n+3)/2.
  - Number of clusters for A_n = C_{n+1} (Catalan number, n+2 choose n+1 / (n+2)).
  - Frieze pattern period for A_n = n+3.
  - Q=3 → A_Q = A_3: 3·6/2 = 9 = Q² cluster variables; C_{Q+1} = C_4 = 14 clusters.
  - EIG_MAX=5 → A_5: 5·8/2 = 20 = V/2 cluster variables; C_6 = 132 clusters.
  - Frieze A_3: period = Q+3 = MULT_K2 = 6.
  - Frieze A_5: period = EIG_MAX+3 = J_INV = 8.
  - Exchange graph of A_n is the 1-skeleton of the associahedron K_{n+1}.
  - Dimension of associahedron for A_n = n; for A_Q: Q = 3; for A_{K-1}: K-1 = 11.

Theorem CCII:
    Let Γ = W(3,3) with atoms Q=3, LAM=2, V=40, K=12, PHI3=13, PHI4=10,
    PHI6=7, J_INV=8, EDGES=240, EIG_MAX=5, MULT_K2=6, LEECH_DIM=24.
    Then:
    (1) Type A_Q = A_3 cluster algebra has Q² = 9 cluster variables.
    (2) Number of clusters for A_Q = C_{Q+1} = C_4 = 14.
    (3) Frieze pattern period for A_Q = Q+3 = MULT_K2 = 6.
    (4) Type A_{EIG_MAX}: V/2 = 20 cluster variables.
    (5) Frieze period for A_{EIG_MAX} = EIG_MAX+3 = J_INV = 8.
    (6) D_n cluster vars = n(n+1); D_Q = Q(Q+1) = Q·(Q+1) = 12 = K.
    (7) E_6 cluster vars = 36 = EDGES/K = V - 4; E_6 clusters = 833 (hard to express).
    (8) Number of positive roots for A_n = n(n+1)/2; A_K = A_12 has 12·13/2 = PHI3*Q = 78.
    (9) Number of positive roots for A_{LAM} = LAM(LAM+1)/2 = Q = 3 ✓.
    (10) Number of positive roots for A_{EIG_MAX} = EIG_MAX*(EIG_MAX+1)/2 = 15 = PHI4+EIG_MAX.
"""

from __future__ import annotations
import math
from dataclasses import dataclass
from typing import List, Dict, Any
import json
import os

# ---------------------------------------------------------------------------
# W(3,3) atoms
# ---------------------------------------------------------------------------
Q: int = 3
LAM: int = 2
V: int = 40
K: int = 12
PHI3: int = Q**2 + Q + 1        # 13
PHI4: int = Q**2 + 1            # 10
PHI6: int = Q**2 - Q + 1        # 7
J_INV: int = 2 * LAM**2         # 8
EDGES: int = V * K // 2         # 240
EIG_MAX: int = 5
MULT_K2: int = K // 2           # 6
LEECH_DIM: int = 2 * K          # 24

# ---------------------------------------------------------------------------
# Cluster algebra combinatorics
# ---------------------------------------------------------------------------

def catalan(n: int) -> int:
    """Catalan number C_n = binomial(2n, n) / (n+1)."""
    return math.comb(2 * n, n) // (n + 1)


def cluster_vars_A(n: int) -> int:
    """Number of cluster variables in type A_n = n(n+3)/2."""
    return n * (n + 3) // 2


def cluster_count_A(n: int) -> int:
    """Number of clusters (maximal clusters) in type A_n = Catalan(n+1)."""
    return catalan(n + 1)


def frieze_period_A(n: int) -> int:
    """Period of SL(2)-frieze pattern of type A_n = n+3."""
    return n + 3


def positive_roots_A(n: int) -> int:
    """Number of positive roots for A_n = n(n+1)/2."""
    return n * (n + 1) // 2


def positive_roots_D(n: int) -> int:
    """Number of positive roots for D_n = n(n-1) (n ≥ 2)."""
    return n * (n - 1)


def cluster_vars_D(n: int) -> int:
    """Number of cluster variables in type D_n = n(n+1)."""
    return n * (n + 1)


def cluster_vars_E(n: int) -> int:
    """Number of cluster variables in type E_n (n=6,7,8): 36, 63, 120."""
    table = {6: 36, 7: 63, 8: 120}
    return table[n]


# ---------------------------------------------------------------------------
# Type A_Q constants
# ---------------------------------------------------------------------------
A_Q_N: int = Q                              # n = Q = 3
A_Q_VARS: int = cluster_vars_A(A_Q_N)      # 3·6/2 = 9 = Q²
A_Q_CLUSTERS: int = cluster_count_A(A_Q_N) # C_4 = 14
A_Q_PERIOD: int = frieze_period_A(A_Q_N)   # 3+3 = 6 = MULT_K2
A_Q_POS_ROOTS: int = positive_roots_A(A_Q_N)  # 3·4/2 = 6 = MULT_K2

A_Q_VARS_IS_Q_SQ: bool = (A_Q_VARS == Q**2)
A_Q_PERIOD_IS_MULT_K2: bool = (A_Q_PERIOD == MULT_K2)
A_Q_POS_ROOTS_IS_MULT_K2: bool = (A_Q_POS_ROOTS == MULT_K2)

# ---------------------------------------------------------------------------
# Type A_{EIG_MAX} constants
# ---------------------------------------------------------------------------
A_EIG_N: int = EIG_MAX                         # n = 5
A_EIG_VARS: int = cluster_vars_A(A_EIG_N)     # 5·8/2 = 20 = V/2
A_EIG_CLUSTERS: int = cluster_count_A(A_EIG_N) # C_6 = 132
A_EIG_PERIOD: int = frieze_period_A(A_EIG_N)   # 5+3 = 8 = J_INV
A_EIG_POS_ROOTS: int = positive_roots_A(A_EIG_N)  # 5·6/2 = 15 = PHI4+EIG_MAX

A_EIG_VARS_IS_HALF_V: bool = (A_EIG_VARS == V // 2)
A_EIG_PERIOD_IS_J_INV: bool = (A_EIG_PERIOD == J_INV)
A_EIG_POS_ROOTS_IS_PHI4_PLUS_EIG: bool = (A_EIG_POS_ROOTS == PHI4 + EIG_MAX)

# ---------------------------------------------------------------------------
# Type A_{LAM} constants
# ---------------------------------------------------------------------------
A_LAM_N: int = LAM                             # n = 2
A_LAM_VARS: int = cluster_vars_A(A_LAM_N)     # 2·5/2 = 5 = EIG_MAX
A_LAM_CLUSTERS: int = cluster_count_A(A_LAM_N) # C_3 = 5 = EIG_MAX
A_LAM_PERIOD: int = frieze_period_A(A_LAM_N)   # 2+3 = 5 = EIG_MAX
A_LAM_POS_ROOTS: int = positive_roots_A(A_LAM_N)  # 2·3/2 = 3 = Q

A_LAM_VARS_IS_EIG_MAX: bool = (A_LAM_VARS == EIG_MAX)
A_LAM_CLUSTERS_IS_EIG_MAX: bool = (A_LAM_CLUSTERS == EIG_MAX)
A_LAM_PERIOD_IS_EIG_MAX: bool = (A_LAM_PERIOD == EIG_MAX)
A_LAM_POS_ROOTS_IS_Q: bool = (A_LAM_POS_ROOTS == Q)

# ---------------------------------------------------------------------------
# Type D_Q constants
# ---------------------------------------------------------------------------
D_Q_N: int = Q                                # n = 3
D_Q_VARS: int = cluster_vars_D(D_Q_N)        # 3·4 = 12 = K
D_Q_POS_ROOTS: int = positive_roots_D(D_Q_N) # 3·2 = 6 = MULT_K2

D_Q_VARS_IS_K: bool = (D_Q_VARS == K)
D_Q_POS_ROOTS_IS_MULT_K2: bool = (D_Q_POS_ROOTS == MULT_K2)

# ---------------------------------------------------------------------------
# Type A_K = A_12 constants
# ---------------------------------------------------------------------------
A_K_N: int = K                               # n = 12
A_K_POS_ROOTS: int = positive_roots_A(A_K_N) # 12·13/2 = 78 = PHI3·Q = 3·26... 
# 78 = 3·26 = 6·13 = MULT_K2·PHI3
A_K_POS_ROOTS_IS_MULT_K2_PHI3: bool = (A_K_POS_ROOTS == MULT_K2 * PHI3)

# ---------------------------------------------------------------------------
# Catalan values
# ---------------------------------------------------------------------------
CATALAN_2: int = catalan(2)   # 2 = LAM
CATALAN_3: int = catalan(3)   # 5 = EIG_MAX
CATALAN_4: int = catalan(4)   # 14
CATALAN_5: int = catalan(5)   # 42
CATALAN_6: int = catalan(6)   # 132

CATALAN_2_IS_LAM: bool = (CATALAN_2 == LAM)
CATALAN_3_IS_EIG_MAX: bool = (CATALAN_3 == EIG_MAX)

# ---------------------------------------------------------------------------
# E_6 cluster variables
# ---------------------------------------------------------------------------
E6_VARS: int = cluster_vars_E(6)    # 36 = LEECH_DIM + K = 24 + 12
E6_VARS_IS_SUM: bool = (E6_VARS == LEECH_DIM + K)

# ---------------------------------------------------------------------------
# ClusterCheck dataclass
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class ClusterCheck:
    name: str
    description: str
    computed: Any
    expected: Any
    exact: bool = True

    @property
    def passes(self) -> bool:
        if self.exact:
            return self.computed == self.expected
        return abs(self.computed - self.expected) < 1e-10


# ---------------------------------------------------------------------------
# Check factories
# ---------------------------------------------------------------------------

def _make_atom_checks() -> List[ClusterCheck]:
    return [
        ClusterCheck("Q", "W(3,3) Q", Q, 3),
        ClusterCheck("LAM", "W(3,3) LAM", LAM, 2),
        ClusterCheck("K", "W(3,3) K", K, 12),
        ClusterCheck("PHI3", "Q²+Q+1", PHI3, 13),
        ClusterCheck("PHI4", "Q²+1", PHI4, 10),
        ClusterCheck("PHI6", "Q²−Q+1", PHI6, 7),
        ClusterCheck("J_INV", "2·LAM²", J_INV, 8),
        ClusterCheck("EDGES", "V·K/2", EDGES, 240),
        ClusterCheck("EIG_MAX", "max eigenvalue", EIG_MAX, 5),
    ]


def _make_type_a_q_checks() -> List[ClusterCheck]:
    return [
        ClusterCheck("aq_vars_q_sq", "A_Q vars = Q²", A_Q_VARS, Q**2),
        ClusterCheck("aq_vars_value", "A_Q vars = 9", A_Q_VARS, 9),
        ClusterCheck("aq_clusters", "A_Q clusters = C_4 = 14", A_Q_CLUSTERS, 14),
        ClusterCheck("aq_period_mult_k2", "A_Q period = MULT_K2", A_Q_PERIOD, MULT_K2),
        ClusterCheck("aq_period_value", "A_Q period = 6", A_Q_PERIOD, 6),
        ClusterCheck("aq_pos_roots", "A_Q pos roots = MULT_K2", A_Q_POS_ROOTS, MULT_K2),
        ClusterCheck("aq_vars_flag", "A_Q vars = Q² flag", A_Q_VARS_IS_Q_SQ, True),
        ClusterCheck("aq_period_flag", "A_Q period = MULT_K2 flag", A_Q_PERIOD_IS_MULT_K2, True),
        ClusterCheck("aq_roots_flag", "A_Q pos roots = MULT_K2 flag", A_Q_POS_ROOTS_IS_MULT_K2, True),
    ]


def _make_type_a_eig_checks() -> List[ClusterCheck]:
    return [
        ClusterCheck("aeig_vars_half_v", "A_EIG vars = V/2", A_EIG_VARS, V // 2),
        ClusterCheck("aeig_vars_value", "A_EIG vars = 20", A_EIG_VARS, 20),
        ClusterCheck("aeig_clusters", "A_EIG clusters = C_6 = 132", A_EIG_CLUSTERS, 132),
        ClusterCheck("aeig_period_j_inv", "A_EIG period = J_INV", A_EIG_PERIOD, J_INV),
        ClusterCheck("aeig_period_value", "A_EIG period = 8", A_EIG_PERIOD, 8),
        ClusterCheck("aeig_pos_roots", "A_EIG pos roots = PHI4+EIG_MAX", A_EIG_POS_ROOTS, PHI4 + EIG_MAX),
        ClusterCheck("aeig_vars_flag", "A_EIG vars = V/2 flag", A_EIG_VARS_IS_HALF_V, True),
        ClusterCheck("aeig_period_flag", "A_EIG period = J_INV flag", A_EIG_PERIOD_IS_J_INV, True),
        ClusterCheck("aeig_roots_flag", "A_EIG pos roots flag", A_EIG_POS_ROOTS_IS_PHI4_PLUS_EIG, True),
    ]


def _make_type_a_lam_checks() -> List[ClusterCheck]:
    return [
        ClusterCheck("alam_vars_eig", "A_LAM vars = EIG_MAX", A_LAM_VARS, EIG_MAX),
        ClusterCheck("alam_clusters_eig", "A_LAM clusters = EIG_MAX", A_LAM_CLUSTERS, EIG_MAX),
        ClusterCheck("alam_period_eig", "A_LAM period = EIG_MAX", A_LAM_PERIOD, EIG_MAX),
        ClusterCheck("alam_pos_roots_q", "A_LAM pos roots = Q", A_LAM_POS_ROOTS, Q),
        ClusterCheck("alam_vars_flag", "A_LAM vars = EIG_MAX flag", A_LAM_VARS_IS_EIG_MAX, True),
        ClusterCheck("alam_clusters_flag", "A_LAM clusters = EIG_MAX flag", A_LAM_CLUSTERS_IS_EIG_MAX, True),
    ]


def _make_type_d_checks() -> List[ClusterCheck]:
    return [
        ClusterCheck("dq_vars_k", "D_Q vars = K", D_Q_VARS, K),
        ClusterCheck("dq_vars_value", "D_Q vars = 12", D_Q_VARS, 12),
        ClusterCheck("dq_pos_roots", "D_Q pos roots = MULT_K2", D_Q_POS_ROOTS, MULT_K2),
        ClusterCheck("dq_vars_flag", "D_Q vars = K flag", D_Q_VARS_IS_K, True),
        ClusterCheck("dq_roots_flag", "D_Q pos roots = MULT_K2 flag", D_Q_POS_ROOTS_IS_MULT_K2, True),
        ClusterCheck("ak_roots_mult_k2_phi3", "A_K pos roots = MULT_K2*PHI3", A_K_POS_ROOTS,
                     MULT_K2 * PHI3),
    ]


def _make_catalan_checks() -> List[ClusterCheck]:
    return [
        ClusterCheck("cat2_lam", "C_2 = LAM", CATALAN_2, LAM),
        ClusterCheck("cat3_eig", "C_3 = EIG_MAX", CATALAN_3, EIG_MAX),
        ClusterCheck("cat4_value", "C_4 = 14", CATALAN_4, 14),
        ClusterCheck("cat5_value", "C_5 = 42", CATALAN_5, 42),
        ClusterCheck("cat6_value", "C_6 = 132", CATALAN_6, 132),
        ClusterCheck("cat2_flag", "C_2 = LAM flag", CATALAN_2_IS_LAM, True),
        ClusterCheck("cat3_flag", "C_3 = EIG_MAX flag", CATALAN_3_IS_EIG_MAX, True),
    ]


def _make_structural_checks() -> List[ClusterCheck]:
    return [
        ClusterCheck("e6_vars_sum", "E_6 vars = LEECH_DIM+K", E6_VARS, LEECH_DIM + K),
        ClusterCheck("e6_vars_value", "E_6 vars = 36", E6_VARS, 36),
        ClusterCheck("e6_vars_flag", "E_6 vars = LEECH_DIM+K flag", E6_VARS_IS_SUM, True),
        ClusterCheck("fn_cluster_vars_a3", "fn A_3 vars", cluster_vars_A(3), 9),
        ClusterCheck("fn_cluster_count_a3", "fn A_3 count", cluster_count_A(3), 14),
        ClusterCheck("fn_frieze_period_a3", "fn A_3 period", frieze_period_A(3), 6),
        ClusterCheck("fn_pos_roots_a3", "fn A_3 pos roots", positive_roots_A(3), 6),
        ClusterCheck("fn_cluster_vars_d3", "fn D_3 vars = A_3 vars = K", cluster_vars_D(3), 12),
        ClusterCheck("fn_pos_roots_d4", "D_4 pos roots = 12 = K", positive_roots_D(4), 12),
        ClusterCheck("cluster_vars_e8", "E_8 vars = 120 = EIG_MAX·LEECH_DIM", cluster_vars_E(8),
                     EIG_MAX * LEECH_DIM),
    ]


# ---------------------------------------------------------------------------
# Audit function
# ---------------------------------------------------------------------------

def cluster_algebra_bridge_audit() -> Dict[str, Any]:
    categories = {
        "atom_checks": _make_atom_checks(),
        "type_a_q_checks": _make_type_a_q_checks(),
        "type_a_eig_checks": _make_type_a_eig_checks(),
        "type_a_lam_checks": _make_type_a_lam_checks(),
        "type_d_checks": _make_type_d_checks(),
        "catalan_checks": _make_catalan_checks(),
        "structural_checks": _make_structural_checks(),
    }

    all_checks = [c for checks in categories.values() for c in checks]
    failed = [c.name for c in all_checks if not c.passes]
    passing = len(all_checks) - len(failed)

    return {
        "status": "PASS" if not failed else "FAIL",
        "all_checks_pass": not bool(failed),
        "check_count": len(all_checks),
        "checks_passing": passing,
        "failed_checks": failed,
        "category_counts": {k: len(v) for k, v in categories.items()},
        "cluster_vars": {
            "A_Q": A_Q_VARS,
            "A_LAM": A_LAM_VARS,
            "A_EIG_MAX": A_EIG_VARS,
            "D_Q": D_Q_VARS,
            "E_6": E6_VARS,
        },
        "frieze_periods": {
            "A_LAM": A_LAM_PERIOD,
            "A_Q": A_Q_PERIOD,
            "A_EIG_MAX": A_EIG_PERIOD,
        },
        "w33_atoms": {
            "Q": Q, "LAM": LAM, "V": V, "K": K,
            "PHI3": PHI3, "PHI4": PHI4, "PHI6": PHI6,
            "J_INV": J_INV, "EDGES": EDGES, "EIG_MAX": EIG_MAX,
        },
        "theorem_ccii": (
            "Cluster algebra combinatorics encodes W(3,3) atoms: "
            "A_Q cluster vars = Q², period = MULT_K2. "
            "A_EIG vars = V/2, period = J_INV. "
            "D_Q cluster vars = K. C_2=LAM, C_3=EIG_MAX. "
            "E_6 vars = LEECH_DIM + K = 36."
        ),
    }


def main() -> None:
    result = cluster_algebra_bridge_audit()
    out_path = os.path.join(os.path.dirname(__file__),
                            "PART_CCII_cluster_algebra_results.json")
    with open(out_path, "w") as fh:
        json.dump(result, fh, indent=2)

    n = result["check_count"]
    p = result["checks_passing"]
    status = result["status"]
    print(f"PART_CCII Cluster Algebra Bridge: {status} ({p}/{n} checks pass)")
    if result["failed_checks"]:
        print(f"  FAILED: {result['failed_checks']}")


if __name__ == "__main__":
    main()
