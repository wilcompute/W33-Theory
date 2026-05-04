import pytest
from exploration.PART_CCLX_TOPOLOGICAL_QC_BRIDGE import (
    checks,
    gsd_torus,
    chern_number,
    ising_topological_spin,
    edge_modes_count,
    honeycomb_jx,
    honeycomb_jy,
    honeycomb_jz,
    topological_sectors,
)

Q, V, K, LAM, MU = 3, 40, 12, 2, 4


class TestCCLXTopologicalQC:
    def test_all_checks_pass(self):
        failed = [name for name, ok in checks if not ok]
        assert failed == [], f"Failed checks: {failed}"

    def test_gsd_torus_is_9(self):
        assert gsd_torus == 9

    def test_chern_number_is_5(self):
        assert chern_number == 5

    def test_ising_spin(self):
        assert ising_topological_spin == 5 / 80

    def test_edge_modes(self):
        assert edge_modes_count == 5

    def test_honeycomb_couplings(self):
        assert honeycomb_jx == 2
        assert honeycomb_jy == 4
        assert honeycomb_jz == 12

    def test_topological_sectors(self):
        assert topological_sectors == 4

    def test_kitaev_toric_code_phase(self):
        """W(3,3) lies in gapped B-phase of Kitaev honeycomb model"""
        assert honeycomb_jx * 6 == honeycomb_jy * 3 == honeycomb_jz
