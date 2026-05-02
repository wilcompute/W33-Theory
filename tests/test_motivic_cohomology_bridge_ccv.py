"""
Regression tests for Part CCV: Motivic Cohomology Bridge (W(3,3)).

All constants are derived from the zero-parameter W(3,3) atoms:
  Q=3, V=40, K=12, LAM=2, MU=4, PHI3=13, EDGES=240,
  EIG_MAX=5, LEECH_DIM=24.

Run:  pytest tests/test_motivic_cohomology_bridge_ccv.py -v
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).parent.parent
if str(_ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(_ROOT / "exploration"))

from PART_CCV_MOTIVIC_COHOMOLOGY_BRIDGE import (
    Q, V, K, LAM, MU, PHI3, EDGES, EIG_MAX, LEECH_DIM, WEIGHT_DEPTH,
    EIGENVALUES,
    MotivicCohomologyBridge,
    build_motivic_cohomology_bridge_summary,
    _verify_invariants,
)


# ──────────────────────────────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def bridge() -> MotivicCohomologyBridge:
    return MotivicCohomologyBridge()


@pytest.fixture(scope="module")
def summary() -> dict:
    return build_motivic_cohomology_bridge_summary()


# ──────────────────────────────────────────────────────────────────────
# Atoms
# ──────────────────────────────────────────────────────────────────────

class TestAtoms:
    def test_q(self):
        assert Q == 3

    def test_v(self):
        assert V == 40

    def test_k(self):
        assert K == 12

    def test_lam(self):
        assert LAM == 2

    def test_mu(self):
        assert MU == 4

    def test_phi3(self):
        assert PHI3 == 13

    def test_edges(self):
        assert EDGES == 240

    def test_eig_max(self):
        assert EIG_MAX == 5

    def test_leech_dim(self):
        assert LEECH_DIM == 24

    def test_weight_depth(self):
        assert WEIGHT_DEPTH == Q + LAM

    def test_weight_depth_value(self):
        assert WEIGHT_DEPTH == 5

    def test_eigenvalue_multiplicities(self):
        assert sum(m for _, m in EIGENVALUES) == V


# ──────────────────────────────────────────────────────────────────────
# Weight filtration
# ──────────────────────────────────────────────────────────────────────

class TestWeightFiltration:
    def test_weight_depth(self, bridge):
        assert bridge.weight_filtration_depth == EIG_MAX

    def test_weight_depth_value(self, bridge):
        assert bridge.weight_filtration_depth == 5

    def test_weight_depth_formula(self, bridge):
        assert bridge.weight_filtration_depth == Q + LAM


# ──────────────────────────────────────────────────────────────────────
# Chow groups
# ──────────────────────────────────────────────────────────────────────

class TestChowGroups:
    def test_chow_codim1_rank(self, bridge):
        assert bridge.chow_rank_codim1 == K

    def test_chow_codim1_value(self, bridge):
        assert bridge.chow_rank_codim1 == 12

    def test_chow_codim2_rank(self, bridge):
        assert bridge.chow_rank_codim2 == LAM

    def test_chow_codim2_value(self, bridge):
        assert bridge.chow_rank_codim2 == 2

    def test_chow_codim1_gt_codim2(self, bridge):
        assert bridge.chow_rank_codim1 > bridge.chow_rank_codim2


# ──────────────────────────────────────────────────────────────────────
# Motivic Euler characteristic
# ──────────────────────────────────────────────────────────────────────

class TestMotivicEuler:
    def test_euler_char(self, bridge):
        assert bridge.motivic_euler_char == V - EDGES

    def test_euler_char_value(self, bridge):
        assert bridge.motivic_euler_char == -200

    def test_euler_char_negative(self, bridge):
        assert bridge.motivic_euler_char < 0


# ──────────────────────────────────────────────────────────────────────
# K-theory
# ──────────────────────────────────────────────────────────────────────

class TestKTheory:
    def test_k0_virtual_rank(self, bridge):
        pos = sum(m for lam, m in EIGENVALUES if lam > 0)
        neg = sum(m for lam, m in EIGENVALUES if lam < 0)
        assert bridge.k0_virtual_rank == pos - neg

    def test_k0_virtual_rank_value(self, bridge):
        assert bridge.k0_virtual_rank == 16

    def test_k0_grothendieck_class(self, bridge):
        assert bridge.k0_grothendieck_class == V - EDGES + 1

    def test_k0_grothendieck_value(self, bridge):
        assert bridge.k0_grothendieck_class == -199

    def test_k0_virtual_positive(self, bridge):
        assert bridge.k0_virtual_rank > 0

    def test_k0_grothendieck_negative(self, bridge):
        assert bridge.k0_grothendieck_class < 0


# ──────────────────────────────────────────────────────────────────────
# Mixed Hodge numbers
# ──────────────────────────────────────────────────────────────────────

class TestMixedHodge:
    def test_hodge_11(self, bridge):
        assert bridge.hodge_11 == K

    def test_hodge_11_value(self, bridge):
        assert bridge.hodge_11 == 12

    def test_hodge_00(self, bridge):
        assert bridge.hodge_pq[(0, 0)] == 1

    def test_hodge_11_dict(self, bridge):
        assert bridge.hodge_pq[(1, 1)] == K

    def test_hodge_22(self, bridge):
        assert bridge.hodge_pq[(2, 2)] == LAM

    def test_hodge_22_value(self, bridge):
        assert bridge.hodge_pq[(2, 2)] == 2

    def test_hodge_symmetry(self, bridge):
        # h^{p,q} = h^{q,p} for pure Hodge structures (diagonal here)
        for (p, q), v in bridge.hodge_pq.items():
            assert p == q  # all entries are diagonal (pure type)

    def test_hodge_keys(self, bridge):
        keys = set(bridge.hodge_pq.keys())
        assert (0, 0) in keys
        assert (1, 1) in keys
        assert (2, 2) in keys


# ──────────────────────────────────────────────────────────────────────
# Motivic zeta function
# ──────────────────────────────────────────────────────────────────────

class TestMotivicZeta:
    def test_zeta_degree(self, bridge):
        assert bridge.motivic_zeta_degree == EDGES

    def test_zeta_degree_value(self, bridge):
        assert bridge.motivic_zeta_degree == 240


# ──────────────────────────────────────────────────────────────────────
# Chow motive decomposition
# ──────────────────────────────────────────────────────────────────────

class TestChowMotive:
    def test_chow_factors(self, bridge):
        assert bridge.chow_motive_factors == PHI3 + 1

    def test_chow_factors_value(self, bridge):
        assert bridge.chow_motive_factors == 14

    def test_chow_factors_exceeds_phi3(self, bridge):
        assert bridge.chow_motive_factors == PHI3 + 1


# ──────────────────────────────────────────────────────────────────────
# Tate twist
# ──────────────────────────────────────────────────────────────────────

class TestTateTwist:
    def test_tate_twist_dim(self, bridge):
        assert bridge.tate_twist_dim == LEECH_DIM

    def test_tate_twist_value(self, bridge):
        assert bridge.tate_twist_dim == 24


# ──────────────────────────────────────────────────────────────────────
# Motivic bidegrees
# ──────────────────────────────────────────────────────────────────────

class TestMotivicBidegrees:
    def test_top_p(self, bridge):
        assert bridge.motivic_cohom_top_p == 2 * K

    def test_top_p_value(self, bridge):
        assert bridge.motivic_cohom_top_p == 24

    def test_top_q(self, bridge):
        assert bridge.motivic_cohom_top_q == K

    def test_top_q_value(self, bridge):
        assert bridge.motivic_cohom_top_q == 12

    def test_top_p_equals_leech_dim(self, bridge):
        # 2K = 24 = LEECH_DIM
        assert bridge.motivic_cohom_top_p == LEECH_DIM

    def test_top_p_twice_top_q(self, bridge):
        assert bridge.motivic_cohom_top_p == 2 * bridge.motivic_cohom_top_q


# ──────────────────────────────────────────────────────────────────────
# Adams operations
# ──────────────────────────────────────────────────────────────────────

class TestAdamsOperations:
    def test_adams_eigenvalue(self, bridge):
        assert bridge.adams_psi_k_eigenvalue == Q ** LAM

    def test_adams_eigenvalue_value(self, bridge):
        assert bridge.adams_psi_k_eigenvalue == 9

    def test_adams_eigenvalue_formula(self, bridge):
        assert bridge.adams_psi_k_eigenvalue == 3 ** 2


# ──────────────────────────────────────────────────────────────────────
# Bloch-Kato regulators
# ──────────────────────────────────────────────────────────────────────

class TestBlochKato:
    def test_bloch_kato_rank(self, bridge):
        assert bridge.bloch_kato_rank == EIG_MAX

    def test_bloch_kato_rank_value(self, bridge):
        assert bridge.bloch_kato_rank == 5


# ──────────────────────────────────────────────────────────────────────
# Full summary / integration
# ──────────────────────────────────────────────────────────────────────

class TestFullSummary:
    def test_verified(self, summary):
        assert summary["verified"] is True

    def test_no_failures(self, summary):
        assert summary["failures"] == []

    def test_keys_present(self, summary):
        required = [
            "weight_filtration_depth", "chow_rank_codim1", "chow_rank_codim2",
            "motivic_euler_char", "k0_virtual_rank", "k0_grothendieck_class",
            "hodge_11", "hodge_pq", "motivic_zeta_degree",
            "chow_motive_factors", "tate_twist_dim",
            "motivic_cohom_top_p", "motivic_cohom_top_q",
            "adams_psi_k_eigenvalue", "bloch_kato_rank",
            "verified", "failures", "w33_atoms",
        ]
        for key in required:
            assert key in summary, f"Missing: {key}"

    def test_summary_weight_depth(self, summary):
        assert summary["weight_filtration_depth"] == 5

    def test_summary_chow1(self, summary):
        assert summary["chow_rank_codim1"] == 12

    def test_summary_euler_char(self, summary):
        assert summary["motivic_euler_char"] == -200

    def test_summary_k0(self, summary):
        assert summary["k0_virtual_rank"] == 16

    def test_summary_hodge_11(self, summary):
        assert summary["hodge_11"] == 12

    def test_summary_zeta_degree(self, summary):
        assert summary["motivic_zeta_degree"] == 240

    def test_summary_chow_factors(self, summary):
        assert summary["chow_motive_factors"] == 14

    def test_summary_tate_dim(self, summary):
        assert summary["tate_twist_dim"] == 24

    def test_summary_top_p(self, summary):
        assert summary["motivic_cohom_top_p"] == 24

    def test_summary_adams(self, summary):
        assert summary["adams_psi_k_eigenvalue"] == 9

    def test_summary_bloch_kato(self, summary):
        assert summary["bloch_kato_rank"] == 5

    def test_summary_w33_atoms(self, summary):
        atoms = summary["w33_atoms"]
        assert atoms["Q"] == 3
        assert atoms["V"] == 40
        assert atoms["K"] == 12

    def test_verify_invariants_clean(self):
        b = MotivicCohomologyBridge()
        assert _verify_invariants(b) == []
