"""Tests for Part CCLIX: Supersymmetry (SUSY) — W(3,3) Bridge."""
import pytest
from PART_CCLIX_SUSY_BRIDGE import (
    n_susy_min,
    susy_generators,
    susy_grassmann,
    superspace_bosonic,
    superspace_fermionic,
    superspace_total,
    mssm_higgs_doublets,
    mssm_gauge_ranks,
    r_parity_order,
    susy_breaking_mech,
    sm_su3_gen,
    sm_su2_gen,
    sm_u1_gen,
    sm_gauge_total,
    sm_gauge_group_factors,
    gravitino_2spin,
    sugra_fields,
    chiral_onshell,
    vector_physical,
    n4_sym_supercharges,
    w33_edges_susy,
    aut_mssm_link,
    m_lam_q3_link,
    lap_top_susy,
    m_neg_susy,
    checks,
    Verified,
)

Q, V, K, LAM, MU = 3, 40, 12, 2, 4
M_LAM, M_NEG, LAP_MID, LAP_TOP, EDGES, AUT_ORDER = 27, 12, 10, 16, 240, 51840


class TestAllChecks:
    def test_all_checks_pass(self):
        failed = [name for name, ok in checks if not ok]
        assert failed == [], f"Failed checks: {failed}"

    def test_verified(self):
        assert Verified is True


class TestSUSYSuperalgebra:
    def test_n_susy_min(self):
        assert n_susy_min == 1

    def test_susy_generators(self):
        # 4 real supercharges Q_α, Q̄_α̇ = MU = 4
        assert susy_generators == MU

    def test_susy_grassmann(self):
        # θ^α: LAM = 2 complex Grassmann coordinates
        assert susy_grassmann == LAM


class TestSuperspaceGeometry:
    def test_superspace_bosonic(self):
        # x^μ: MU = 4 bosonic coords
        assert superspace_bosonic == MU

    def test_superspace_fermionic(self):
        # θ^α + θ̄_α̇: MU = 4 fermionic real DOF (2+2)
        assert superspace_fermionic == MU

    def test_superspace_total(self):
        # 4 + 4 = 8 = 2*MU = K - MU
        assert superspace_total == 2 * MU
        assert superspace_total == K - MU
        assert superspace_total == 8


class TestMSSMStructure:
    def test_mssm_higgs_doublets(self):
        # Hu and Hd: LAM = 2 doublets
        assert mssm_higgs_doublets == LAM

    def test_mssm_gauge_ranks(self):
        # SU(3)(2) + SU(2)(1) + U(1)(1) = 4 = MU
        assert mssm_gauge_ranks == MU

    def test_r_parity_order(self):
        # Z_2 R-parity: order = LAM = 2
        assert r_parity_order == LAM

    def test_susy_breaking_mech(self):
        # F-term or D-term: LAM = 2 mechanisms
        assert susy_breaking_mech == LAM


class TestSMGaugeGenerators:
    def test_sm_su3_gen(self):
        # 8 = Q^2 - 1 gluons
        assert sm_su3_gen == Q**2 - 1
        assert sm_su3_gen == 8

    def test_sm_su2_gen(self):
        # W^1, W^2, W^3: Q = 3 generators
        assert sm_su2_gen == Q

    def test_sm_u1_gen(self):
        # B boson: 1 generator
        assert sm_u1_gen == 1

    def test_sm_gauge_total(self):
        # 8 + 3 + 1 = 12 = K — the valency of W(3,3) is the SM gauge generator count
        assert sm_gauge_total == K
        assert (Q**2 - 1) + Q + 1 == K

    def test_sm_gauge_group_factors(self):
        # SU(3) x SU(2) x U(1): Q = 3 factors
        assert sm_gauge_group_factors == Q


class TestGravitinoAndSUGRA:
    def test_gravitino_2spin(self):
        # Spin-3/2: 2J = 3 = Q
        assert gravitino_2spin == Q

    def test_sugra_fields(self):
        # Graviton (spin-2) + gravitino (spin-3/2) = LAM = 2
        assert sugra_fields == LAM


class TestMultipletStructure:
    def test_chiral_onshell(self):
        # On-shell chiral: (scalar, Weyl fermion) = LAM = 2 DOF
        assert chiral_onshell == LAM

    def test_vector_physical(self):
        # Physical vector: 2 transverse polarizations = LAM = 2
        assert vector_physical == LAM


class TestN4SYM:
    def test_n4_sym_supercharges(self):
        # N=4 SYM: 4*MU = 16 = LAP_TOP supercharges
        assert n4_sym_supercharges == LAP_TOP
        assert n4_sym_supercharges == 4 * MU


class TestW33SpectralEncoding:
    def test_w33_edges_susy(self):
        # EDGES // (K * LAM) = 240 // 24 = 10 = LAP_MID
        assert w33_edges_susy == LAP_MID

    def test_aut_mssm_link(self):
        # AUT_ORDER // (M_LAM * K * LAM) = 51840 // 648 = 80 = 2*V
        assert aut_mssm_link == 2 * V
        assert AUT_ORDER // (M_LAM * K * LAM) == 80

    def test_m_lam_q3_link(self):
        # M_LAM = Q^3 = 27
        assert m_lam_q3_link == M_LAM
        assert m_lam_q3_link == Q**3

    def test_lap_top_susy(self):
        # LAP_TOP = K + MU = 16
        assert lap_top_susy == LAP_TOP
        assert lap_top_susy == K + MU

    def test_m_neg_susy(self):
        # M_NEG = LAP_MID + LAM = 12
        assert m_neg_susy == M_NEG
        assert m_neg_susy == LAP_MID + LAM
