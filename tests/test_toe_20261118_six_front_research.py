"""Regression tests for six independent TOE research probes, Nov 18 2026."""
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261118_susy_sic_uv_completion as uv
import toe_20261118_four_independent_bottleneck_probes as probes
import toe_20261118_h27_twisted_K_first_AHSS as twisted

class SixFrontResearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.uv=uv.numeric_certificate()
        cls.mod=uv.exact_mod7_certificate()
        cls.singular=probes.singular_orbifold_probe()
        cls.memory=probes.memory_probe()
        cls.bracket=probes.bracket_probe()
        cls.code=probes.qutrit_code_magic_probe()
        cls.twists=twisted.main()

    def test_susy_cubic_anomaly_free(self):
        a=self.uv
        self.assertEqual(a["total_fundamental_count"],a["total_antifundamental_count"])
        self.assertEqual(a["gauge_singlet_count"],46)
        self.assertEqual(a["one_loop_SU3_beta_coefficient_3Nc_minus_Nf"],-1)
        self.assertFalse(a["perturbatively_asymptotically_free"])
        self.assertLess(a["max_D_matrix_residual"],1e-12)

    def test_susy_full_physical_hessian(self):
        a=self.uv
        self.assertEqual(a["holomorphic_constraint_rank"],46)
        self.assertEqual(a["superpotential_hessian_rank"],98)
        self.assertEqual(a["complex_gauge_orbit_nullity"],8)
        self.assertGreater(a["smallest_nonzero_hessian_singular_value"],0.1)

    def test_susy_finite_field_independence(self):
        self.assertEqual(self.mod["meson_jacobian_rank"],45)
        self.assertEqual(self.mod["meson_plus_baryon_rank"],46)
        self.assertNotEqual(self.mod["meson_pivot_det_mod7"],0)

    def test_g2_orbifold_is_only_index_candidate(self):
        self.assertEqual(self.singular["torus_orbifold_fixed_points"],3)
        self.assertEqual(self.singular["H27_charge_fixed_line_mod3"][1],(1,2))
        self.assertEqual(self.singular["H27_dual_torsion_clock_fixed_line_mod3"][1],(1,1))
        self.assertTrue(self.singular["charge_dual_orthogonal_mod3"])
        self.assertEqual(self.singular["per_family_SU3_cubic_anomaly_coefficients"],[0,0,0])

    def test_qutrit_memory_intervention_and_witness(self):
        d=self.memory
        self.assertAlmostEqual(sum(d["arbitrary_instrument_example_conditional_probabilities"]),1)
        self.assertLess(d["max_conditional_input_output_error"],1e-10)
        self.assertGreater(d["hoeffding_99p9pct_lower"],1/3)
        self.assertAlmostEqual(d["noise_threshold_for_witness_violation"],.75)

    def test_continuum_low_band_vs_aliasing(self):
        t=self.bracket["discretization_comparison"]
        self.assertTrue(all(x["spectral_relative_defect"]<1e-10 for x in t))
        self.assertGreater(self.bracket["32_site_spectral_high_frequency_alias_defect"],1.0)
        self.assertTrue(all(x>3 for x in self.bracket["centered_defect_halving_ratios"]))

    def test_qutrit_stabilizer_decoding_and_magic(self):
        d=self.code
        self.assertEqual(d["stabilizer_elements"],81)
        self.assertEqual(d["distinct_weight_one_nonzero_syndromes"],40)
        self.assertEqual(d["weight_three_normalizer_nonstabilizer_count"],80)
        self.assertAlmostEqual(d["exact_decoded_logical_failure_probability"],0.0009080851374237062)
        self.assertAlmostEqual(min(d["SIC_Hesse_Wigner"]),-1/3)

    def test_twisted_K_rank_period_necessary(self):
        r=self.twists
        self.assertEqual(r["nontrivial_twists"],8)
        self.assertEqual(len(r["projective_rays"]),4)
        self.assertEqual(r["nine_twists"]["(0, 0)"]["necessary_rank_multiple"],1)
        for name,record in r["nine_twists"].items():
            if name!="(0, 0)":
                self.assertEqual(record["necessary_rank_multiple"],3)

if __name__=="__main__":
    unittest.main()
