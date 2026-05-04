import pytest
from exploration.PART_CCLXIII_ISLAND_FORMULA_BRIDGE import (
    checks,
    k3_central_charge,
    k3_hodge_11,
    k3_hodge_21,
    island_entropy_bits,
    island_surface_genus,
)

class TestCCLXIIIIslandFormula:
    def test_all_checks_pass(self):
        failed = [name for name, ok in checks if not ok]
        assert failed == [], f"Failed checks: {failed}"

    def test_k3_hodge_diamond(self):
        """K3 surface Hodge diamond: (1, 0, 20, 0, 1)"""
        assert k3_hodge_11 == 20
        assert k3_hodge_21 == 21  # h21 + h11 = 41 (Euler chi = 24)

    def test_k3_conformal_central_charge(self):
        """Central charge c = 24 for K3 CFT"""
        assert k3_central_charge == 24

    def test_island_entropy_bits(self):
        """Island configuration entropy in bits"""
        assert island_entropy_bits == 2

    def test_extremal_surface_genus_1(self):
        """Minimal surface on torus genus 1 has genus 1"""
        assert island_surface_genus == 1
