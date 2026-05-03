"""Tests for Part CCLVI: Maxwell Field Tensor — W(3,3) Bridge."""
import pytest
from PART_CCLVI_MAXWELL_FIELD_TENSOR_BRIDGE import (
    field_tensor_components,
    field_tensor_rank,
    spacetime_dim,
    e_field_components,
    b_field_components,
    eb_total,
    poynting_dim,
    a_mu_components,
    physical_dof,
    gauge_redundancy,
    u1_gauge_rank,
    inhomogeneous_maxwell,
    homogeneous_maxwell,
    total_maxwell,
    maxwell_groups,
    lorentz_invariants,
    action_coeff_denom,
    maxwell_action_power,
    dual_coeff_denom,
    levi_civita_nonzero,
    em_duality_angle_denom,
    self_dual_components,
    anti_self_dual_components,
    t_munu_sym_components,
    t_munu_trace,
    t_munu_independent,
    photon_propagator_power,
    photon_helicity_states,
    w33_lap_mid_link,
    spectral_gap_link,
    edges_formula,
    conformal_group_dim,
    conformal_weight_F,
    checks,
    Verified,
)

Q, V, K, LAM, MU = 3, 40, 12, 2, 4
M_LAM, M_NEG, LAP_MID, LAP_TOP, EDGES = 27, 12, 10, 16, 240


class TestFieldTensorStructure:
    def test_all_checks_pass(self):
        failed = [name for name, ok in checks if not ok]
        assert failed == [], f"Failed checks: {failed}"

    def test_verified(self):
        assert Verified is True

    def test_field_tensor_components(self):
        # F_mu_nu: 4x4 antisymmetric → MU*(MU-1)//2 = 6 = K//LAM
        assert field_tensor_components == 6
        assert field_tensor_components == K // LAM

    def test_field_tensor_rank(self):
        assert field_tensor_rank == LAM  # rank-2 tensor

    def test_spacetime_dim(self):
        assert spacetime_dim == MU  # 4D spacetime


class TestEBDecomposition:
    def test_e_field_components(self):
        # F_{0i} for i=1,2,3 → Q=3 components
        assert e_field_components == Q

    def test_b_field_components(self):
        # epsilon_{ijk} F^{jk}/2 → Q=3 components
        assert b_field_components == Q

    def test_eb_total(self):
        # 3 + 3 = 6 = field_tensor_components
        assert eb_total == field_tensor_components
        assert eb_total == e_field_components + b_field_components

    def test_poynting_dim(self):
        # Poynting vector S = E × B: Q=3 spatial components
        assert poynting_dim == Q


class TestGaugePotential:
    def test_a_mu_components(self):
        # A_mu: MU=4 covariant components
        assert a_mu_components == MU

    def test_physical_dof(self):
        # 2 transverse polarizations after gauge fixing
        assert physical_dof == LAM

    def test_gauge_redundancy(self):
        # 2 removed DOF (temporal + longitudinal)
        assert gauge_redundancy == LAM

    def test_gauge_dof_balance(self):
        # physical + gauge = total A_mu components
        assert physical_dof + gauge_redundancy == a_mu_components

    def test_u1_gauge_rank(self):
        assert u1_gauge_rank == 1


class TestMaxwellEquations:
    def test_inhomogeneous_maxwell(self):
        # d_mu F^{mu nu} = J^nu: MU=4 equations
        assert inhomogeneous_maxwell == MU

    def test_homogeneous_maxwell(self):
        # d_mu F~^{mu nu} = 0: MU=4 equations
        assert homogeneous_maxwell == MU

    def test_total_maxwell(self):
        # 8 = K - MU = 12 - 4
        assert total_maxwell == 8
        assert total_maxwell == K - MU

    def test_maxwell_groups(self):
        # Two groups (homogeneous + inhomogeneous) = LAM=2
        assert maxwell_groups == LAM


class TestLorentzInvariantsAndAction:
    def test_lorentz_invariants(self):
        # F·F and F·F~: two independent quadratic invariants
        assert lorentz_invariants == LAM

    def test_action_coeff_denom(self):
        # S = -(1/4) ∫ F^2: denominator = MU=4
        assert action_coeff_denom == MU

    def test_maxwell_action_power(self):
        # F^2 → power = LAM=2
        assert maxwell_action_power == LAM


class TestDualTensor:
    def test_dual_coeff_denom(self):
        # F~ = (1/2) eps F: denom = LAM=2
        assert dual_coeff_denom == LAM

    def test_levi_civita_nonzero(self):
        # 4D Levi-Civita: 4! = 24 = K * LAM nonzero components
        import math
        assert levi_civita_nonzero == math.factorial(MU)
        assert levi_civita_nonzero == K * LAM
        assert levi_civita_nonzero == 24

    def test_em_duality_angle_denom(self):
        # EM duality rotation angle = pi/LAM = pi/2
        assert em_duality_angle_denom == LAM

    def test_self_dual_components(self):
        assert self_dual_components == Q

    def test_anti_self_dual_components(self):
        assert anti_self_dual_components == Q

    def test_self_dual_total(self):
        assert self_dual_components + anti_self_dual_components == field_tensor_components


class TestStressEnergyTensor:
    def test_t_munu_sym_components(self):
        # Symmetric T^{mu nu}: MU*(MU+1)//2 = 10 = LAP_MID
        assert t_munu_sym_components == LAP_MID
        assert t_munu_sym_components == MU * (MU + 1) // LAM

    def test_t_munu_trace(self):
        # EM T^{mu nu} traceless (conformal invariance)
        assert t_munu_trace == 0

    def test_t_munu_independent(self):
        # Traceless symmetric: LAP_MID - 1 = 9 = Q^2
        assert t_munu_independent == 9
        assert t_munu_independent == Q * Q


class TestPhotonPropagator:
    def test_photon_propagator_power(self):
        # Feynman propagator ~ 1/k^2: power = LAM=2
        assert photon_propagator_power == LAM

    def test_photon_helicity_states(self):
        # Helicity +1 and -1 → LAM=2 states
        assert photon_helicity_states == LAM


class TestW33SpectralEncoding:
    def test_w33_lap_mid_link(self):
        # W(3,3) Laplacian mid eigenvalue = T^{mu nu} components
        assert w33_lap_mid_link == t_munu_sym_components
        assert w33_lap_mid_link == LAP_MID

    def test_spectral_gap_link(self):
        # LAP_MID - field_tensor_components = 10 - 6 = 4 = MU
        assert spectral_gap_link == MU

    def test_edges_formula(self):
        # EDGES = V*K//LAM = 240
        assert edges_formula == EDGES


class TestConformalStructure:
    def test_conformal_group_dim(self):
        # SO(2,4) dimension: 6*5//2 = 15 = M_LAM - K = 27-12
        assert conformal_group_dim == 15
        assert conformal_group_dim == M_LAM - K

    def test_conformal_weight_F(self):
        # Conformal weight of F_{mu nu} in 4D = LAM=2
        assert conformal_weight_F == LAM
