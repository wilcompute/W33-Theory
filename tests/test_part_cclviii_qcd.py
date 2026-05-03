"""Tests for Part CCLVIII: Quantum Chromodynamics (QCD) — W(3,3) Bridge."""
import pytest
from PART_CCLVIII_QCD_BRIDGE import (
    su3_rank,
    su3_generators,
    gluons,
    gluons_lap_link,
    su3_weyl_order,
    quark_colors,
    quark_flavors,
    quark_flavor_edge_link,
    quark_generations,
    quark_per_generation,
    meson_quarks,
    baryon_quarks,
    lattice_qcd_dim,
    qcd_coupling_log_power,
    color_casimir_CA,
    eleven_Nc,
    eleven_Nc_link,
    af_nf_bound,
    qcd_fund_dim,
    qcd_adj_dim,
    m_lam_cubic,
    gluon_3vertex,
    gluon_4vertex,
    confinement_string_power,
    instanton_charge,
    w33_edges_qcd,
    aut_color_link,
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


class TestSU3GroupStructure:
    def test_su3_rank(self):
        # Cartan rank of SU(3) = LAM = 2
        assert su3_rank == LAM

    def test_su3_generators(self):
        # Gell-Mann matrices: Q^2 - 1 = 8
        assert su3_generators == Q**2 - 1
        assert su3_generators == 8

    def test_gluons(self):
        # Gluons = SU(3) generators = 8
        assert gluons == 8
        assert gluons == su3_generators

    def test_gluons_lap_link(self):
        # Spectral: gluons = LAP_MID - LAM = 10 - 2 = 8
        assert gluons_lap_link == LAP_MID - LAM
        assert gluons_lap_link == 8

    def test_su3_weyl_order(self):
        # Weyl group S_3: order 3! = 6 = K // LAM
        assert su3_weyl_order == 6
        assert su3_weyl_order == K // LAM


class TestQuarkStructure:
    def test_quark_colors(self):
        assert quark_colors == Q

    def test_quark_flavors(self):
        # 6 = 2*Q
        assert quark_flavors == 2 * Q
        assert quark_flavors == 6

    def test_quark_flavor_edge_link(self):
        # K // LAM = 12 // 2 = 6 = quark_flavors
        assert quark_flavor_edge_link == K // LAM
        assert quark_flavor_edge_link == quark_flavors

    def test_quark_generations(self):
        assert quark_generations == Q

    def test_quark_per_generation(self):
        # Up-type + down-type = LAM = 2
        assert quark_per_generation == LAM


class TestHadronStructure:
    def test_meson_quarks(self):
        # Meson = quark + antiquark = LAM = 2
        assert meson_quarks == LAM

    def test_baryon_quarks(self):
        # Baryon = 3 quarks = Q = 3
        assert baryon_quarks == Q


class TestQCDLagrangian:
    def test_lattice_qcd_dim(self):
        # 4D Euclidean lattice = MU = 4
        assert lattice_qcd_dim == MU

    def test_qcd_coupling_log_power(self):
        # alpha_s ~ 1/log(mu^2): power 2 = LAM
        assert qcd_coupling_log_power == LAM

    def test_color_casimir_CA(self):
        # C_A = N = 3 for SU(3) = Q
        assert color_casimir_CA == Q


class TestAsymptoticFreedom:
    def test_eleven_Nc(self):
        # 11 * N_c = 11 * Q = 33
        assert eleven_Nc == 11 * Q
        assert eleven_Nc == 33

    def test_eleven_Nc_link(self):
        # 33 = M_LAM + K // LAM = 27 + 6
        assert eleven_Nc_link == M_LAM + K // LAM
        assert eleven_Nc_link == 33

    def test_af_nf_bound(self):
        # Asymptotic freedom: N_f < 16.5 → 16 = LAP_TOP
        assert af_nf_bound == LAP_TOP
        assert af_nf_bound == 11 * Q // LAM


class TestRepresentations:
    def test_qcd_fund_dim(self):
        # Fundamental of SU(3): dim = Q = 3
        assert qcd_fund_dim == Q

    def test_qcd_adj_dim(self):
        # Adjoint of SU(3): dim = Q^2-1 = 8
        assert qcd_adj_dim == Q**2 - 1
        assert qcd_adj_dim == 8

    def test_m_lam_cubic(self):
        # M_LAM = Q^3 = 27 (27-plet in SU(3) flavour)
        assert m_lam_cubic == M_LAM
        assert m_lam_cubic == Q**3


class TestGluonVertices:
    def test_gluon_3vertex(self):
        # Triple-gluon vertex: Q = 3 legs
        assert gluon_3vertex == Q

    def test_gluon_4vertex(self):
        # Quartic-gluon vertex: MU = 4 legs
        assert gluon_4vertex == MU


class TestConfinement:
    def test_confinement_string_power(self):
        # String tension Lambda^2: power = LAM = 2
        assert confinement_string_power == LAM

    def test_instanton_charge(self):
        # Integer topological charge
        assert instanton_charge == 1


class TestW33SpectralEncoding:
    def test_w33_edges_qcd(self):
        # EDGES // (K * LAM) = 240 // 24 = 10 = LAP_MID
        assert w33_edges_qcd == LAP_MID
        assert EDGES // (K * LAM) == LAP_MID

    def test_aut_color_link(self):
        # AUT_ORDER // EDGES = 216 = 6^3 = (2*Q)^3
        assert aut_color_link == (2 * Q) ** 3
        assert aut_color_link == 216
        assert AUT_ORDER // EDGES == (2 * Q) ** 3
