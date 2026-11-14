#!/usr/bin/env python3
"""Independent standard-library regression suite for five TOE fronts + three."""
from fractions import Fraction as F
from pathlib import Path
import importlib.util
import math
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "toe_20261114_fiveplus3_cloud_reproducer.py"
spec = importlib.util.spec_from_file_location("toe_20261114_verified_core", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class FivePlusThreeTests(unittest.TestCase):
    def test_GF8_is_a_field(self):
        for a in range(8):
            self.assertEqual(mod.mul(a, 1), a)
            if a:
                self.assertEqual({mod.mul(a, b) for b in range(8)}, set(range(8)))
            for b in range(8):
                self.assertEqual(mod.mul(a, b), mod.mul(b, a))

    def test_nine_MUB_Bell_spectrum(self):
        result = mod.f8_two_copy_spectrum()
        self.assertEqual(result["covered_Pauli_labels"], 567)
        self.assertEqual(result["full_Bell_spectrum"], {567: 1, 55: 567, -9: 3528})
        self.assertEqual(result["symmetric_Bell_spectrum"], {567: 1, 55: 567, -9: 1512})
        self.assertEqual(sum(result["symmetric_Bell_spectrum"].values()), 2080)

    def test_Einstein_Maxwell_tensor_equation(self):
        d = mod.einstein_maxwell_ads5_s2_s2()
        f2 = F(56,5)
        self.assertEqual(-f2/F(4*(9-2)), F(-2,5))
        self.assertEqual(F(14,5)/2 - f2/F(4*(9-2)), 1)
        self.assertEqual(d["AdS_radius_squared"], "10")
        self.assertEqual(d["homogeneous_radion_Hessian"], ["112/3","144/5"])

    def test_homogeneous_radion_stability(self):
        d = mod.einstein_maxwell_ads5_s2_s2()
        self.assertLess(F(d["V_at_critical"]), 0)
        self.assertTrue(all(F(v)>0 for v in d["homogeneous_radion_Hessian"]))

    def test_reversible_local_clock(self):
        self.assertEqual(mod.reversible_two_component_clock()["ticks_verified"],9)

    def test_edge_subdivision_exact_moment(self):
        items = mod.subdivided_w33_limit()["moments"]
        for item in items:
            L = item["path_length"]
            n = item["vertices"]
            self.assertEqual(F(item["second_moment"]),F(120*L-200,n))
        self.assertGreater(float(F(items[-1]["second_moment"])), .49)

    def test_photonic_GHZ_and_readout_losses(self):
        d = mod.photon_16_rail_ghz()
        self.assertEqual(d["photon_modes"],16)
        self.assertEqual(d["H_disjoint_coupler_count"],8)
        self.assertEqual(d["X4_analyzer_additional_couplers"],32)
        self.assertEqual(d["accepted_events_Hoeffding_95pct_error_0p05"],2952)
        self.assertEqual(d["preparation_only_raw_events_eta98"],3201)
        self.assertEqual(d["preparation_plus_X4_analyzer_raw_events_eta98"],3470)

    def test_flux_sign_isospectral(self):
        d = mod.flux_chirality_blind_spot()
        self.assertTrue(d["isospectral_plus_minus_flux"])
        self.assertAlmostEqual(d["oriented_current_plus_flux"],
                               -d["oriented_current_minus_flux"])

    def test_nonhomeomorphic_compactification_sectors(self):
        d = mod.flux_topology_guard()
        self.assertEqual(d["T4_Betti"],[1,4,6,4,1])
        self.assertEqual(d["S2xS2_Betti"],[1,0,2,0,1])
        self.assertEqual(d["third_form_ranks"],[4,0])

    def test_dimensionful_tick_speed_underdetermined(self):
        self.assertEqual(mod.speed_of_light_units_guard()["possible_hop_speeds"],
                         ["1","2","1/3","3/7"])


if __name__ == "__main__":
    unittest.main()
