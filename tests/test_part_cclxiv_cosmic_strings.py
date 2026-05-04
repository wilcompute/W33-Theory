import pytest
from exploration.PART_CCLXIV_COSMIC_STRINGS_BRIDGE import (
    checks,
    su3_tooft_order,
    monopole_loops_genus_6,
    chern_simons_level,
    consistent_monopole_charge_pairs,
)

class TestCCLXIVCosmicStrings:
    def test_all_checks_pass(self):
        failed = [name for name, ok in checks if not ok]
        assert failed == [], f"Failed checks: {failed}"

    def test_su3_tooft_operator(self):
        """'t Hooft order parameter for SU(3): order = 3 = Q"""
        assert su3_tooft_order == 3

    def test_monopole_loops_genus_6(self):
        """Independent monopole loops on genus 6 surface: k = 12"""
        assert monopole_loops_genus_6 == 12

    def test_chern_simons_level(self):
        """Chern-Simons level = LAP_TOP = 16"""
        assert chern_simons_level == 16

    def test_dirac_quantization(self):
        """Dirac quantization: consistent monopole charge pairs = K = 12"""
        assert consistent_monopole_charge_pairs == 12

    def test_topological_defect_consistency(self):
        """Higher-genus configuration supports all W(3,3) defect types"""
        assert su3_tooft_order * monopole_loops_genus_6 == 36
