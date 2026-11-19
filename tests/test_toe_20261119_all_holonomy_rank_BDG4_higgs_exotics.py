"""Independent regressions: all Spin10 Wilson/Higgs, causal BDG4 and photonic gates."""
from pathlib import Path
import sys,unittest
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_all_holonomy_rank_BDG4_higgs_exotics as m

class EightPhysicalGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=m.spin10_all_holonomy_rank_no_go()
        cls.w=m.cyclic_W7_GUT_projection()
        cls.h0=m.vectorlike_spinor_Higgs_escape_and_exotics()
        cls.h1=m.vectorlike_spinor_Higgs_with_ten_completion()
        cls.b=m.causal_BDG4_quadratic_recovery()
        cls.o=m.orbifold_boundary_Robin_spectrum()
        cls.p=m.photon_single_qubit_gate_real_cost()
        cls.g=m.physics_first_dependency_gate()

    def test_all_D5_roots_restrict_nontrivially_to_SM_torus(self):
        self.assertEqual(self.r["D5_root_count"],40)
        self.assertEqual(self.r["D5_roots_vanishing_on_SM_torus"],[])
        self.assertEqual(self.r["SM_maximal_torus_rank"],4)

    def test_even_noncommuting_inner_flat_holonomy_cannot_lower_rank(self):
        self.assertEqual(self.r["centralizer_of_SM_torus_Lie_rank"],5)
        self.assertIn("noncommuting",self.r["exact_inner_holonomy_theorem"])
        self.assertIn("Outer",self.r["caveat"])

    def test_Z7_lowest_block_holonomy_reproduces_prior_work(self):
        self.assertEqual(self.w["minimal_cyclic_order_for_SM_plus_chi"],7)
        for p in range(2,7):
            self.assertTrue(all(x["Spin10_unbroken_dimension"]!=13
                                for x in self.w["cyclic_orders_2_through_13"][str(p)]))

    def test_Z7_component_projections_are_not_complete_families(self):
        self.assertEqual(self.w["Spin10_centralizer_dimension"],13)
        self.assertEqual(self.w["one_16_trivial_holonomy_component_count"],1)
        self.assertEqual(len(self.w["one_16_all_component_Wilson_Z7_exponents"]),16)
        self.assertIn("Only constant bulk",self.w["not_a_chirality_derivation"])

    def test_minimal_vectorlike_pair_vacuum_F_D_flat(self):
        self.assertEqual(self.h0["D_chi_residual"],"0")
        self.assertEqual(self.h0["Hessian_rank"],2)
        self.assertEqual(self.h0["total_chiral_multiplet_components"],33)

    def test_pair_and_driver_leave_ten_extra_chiral_modes(self):
        self.assertEqual(self.h0["broken_complex_gauge_dimension"],21)
        self.assertEqual(self.h0["physical_massless_complex_chiral_remainder"],10)
        self.assertEqual(self.h0["remainder_SU5_representation"],"5 + bar5")

    def test_added_10_gives_all_43_F_terms_and_Hessian_independently(self):
        self.assertTrue(self.h1["F_terms_all_zero_at_H10_X0"])
        self.assertTrue(self.h1["D_terms_all_zero"])
        self.assertTrue(self.h1["independent_43_field_symbolic_F_gradient_and_Hessian_match"])

    def test_added_10_lifts_all_fiveplet_exotics(self):
        self.assertEqual(self.h1["full_4D_chiral_component_count"],43)
        self.assertEqual(self.h1["superpotential_Hessian_exact_rank"],22)
        self.assertEqual(self.h1["Hessian_kernel_dimension"],21)
        self.assertEqual(self.h1["physical_4D_local_complex_moduli_after_gauge"],0)
        self.assertEqual(self.h1["residual_SU5_5_plus_bar5"],"fully massive at lambda*v and lambdabar*v")

    def test_source_E8_has_no_correct_neutral_GUT_Higgs_fields(self):
        self.assertTrue(self.h1["no_source_uncharged_spinor_or_10"])
        self.assertTrue(self.h1["no_source_10_has_plus_or_minus_twice_spinor_charge"])
        self.assertTrue(self.h1["simple_neutral_X_vectorlike_charge_selection_forces_zero_charge"])
        self.assertIn("DO NOT occur",self.h1["physical_obstruction"])

    def test_original_three_chiral_spinors_and_discrete_R_caveat(self):
        self.assertEqual(self.h1["three_original_16_net_chiral_index_unchanged"],3)
        self.assertEqual(self.h1["conditional_matter_gravitational_Z4R_parity_shift"],1)

    def test_four_layer_moment_matrix_exact_unique_kernel(self):
        mat=s.Matrix([[1,s.Rational(1,2),s.Rational(3,8),s.Rational(5,16)],
                      [1,1,1,1],
                      [s.Rational(1,2),s.Rational(3,4),s.Rational(15,16),s.Rational(35,32)]])
        w=s.Matrix(self.b["unique_primitive_four_layer_weights"])
        self.assertEqual(w,s.Matrix([1,-9,16,-8]))
        self.assertEqual(mat*w,s.zeros(3,1))
        self.assertEqual(len(mat.nullspace()),1)

    def test_BDG4_s_asymptotic_is_exact_minus8(self):
        self.assertEqual(self.b["asymptotic_Wave_box_s_exact"],-8)
        self.assertEqual(self.b["constant_renormalization_sum"],"1/3")
        self.assertIn("sqrt(pi)/3",self.b["digamma_s_sum"])

    def test_BDG4_constant_and_linear_recover_zero(self):
        q=self.b["numerical_density_benchmarks"][-1]["BDG4_normalized_wave_operator"]
        self.assertLess(abs(q["1"]),.03)
        self.assertLess(abs(q["t"]),.03)

    def test_BDG4_timelike_quadratic(self):
        q=self.b["numerical_density_benchmarks"][-1]["BDG4_normalized_wave_operator"]
        self.assertLess(abs(q["t²"]+2),.03)

    def test_BDG4_spacelike_quadratic(self):
        q=self.b["numerical_density_benchmarks"][-1]["BDG4_normalized_wave_operator"]
        self.assertLess(abs(q["r²"]-6),.03)
        self.assertLess(abs(q["x²"]-2),.03)

    def test_BDG4_Lorentzian_quadratic_s(self):
        q=self.b["numerical_density_benchmarks"][-1]["BDG4_normalized_wave_operator"]
        self.assertLess(abs(q["s"]+8),.03)

    def test_BDG4_boost_covariance_probe(self):
        q=self.b["numerical_density_benchmarks"][-1]["BDG4_normalized_wave_operator"]
        self.assertLess(abs(q["t'²"]+2),.03)
        self.assertLess(abs(q["x'²"]-2),.03)

    def test_BDG4_prior_art_and_limit_not_GR(self):
        self.assertIn("known benincasa-dowker",self.b["source"].lower())
        self.assertIn("No finite sprinkling",self.b["limitations"])

    def test_Robin_branemass_lifts_one_KK_mode(self):
        rows=self.o["roots"]
        self.assertEqual(rows[0]["first_three_kL"][0],0.)
        self.assertGreater(rows[-1]["first_three_kL"][0],1.55)
        self.assertLess(rows[-1]["first_three_kL"][0],1.571)

    def test_Robin_boundary_spectrum_not_Fermion_spectrum(self):
        self.assertIn("scalar",self.o["limits"].lower())
        self.assertGreater(self.o["one_heavy_octet_proxy_mass_GeV"],1e13)

    def test_one_photon_unary_X_gate_swaps_scale_exponentially(self):
        r=self.p["mode_swap_resource_table"]
        self.assertEqual([x["mode_swaps_for_one_logical_X"] for x in r],
                         [8,64,512,2048])
        self.assertEqual([x["generic_Ud_real_parameters"] for x in r],
                         [256,16384,1048576,16777216])

    def test_four_percent_acceptance_bias_mimics_one_percent_quantum_shift(self):
        self.assertAlmostEqual(
          self.p["success_detection_acceptance_bias_that_mimics_p0_0p5_as_pobs_0p51"],
          51/49,places=12)
        self.assertIn("not a universal",self.p["limits"].lower())

    def test_dependency_priority_preserves_two_independent_branches(self):
        self.assertIn("first",self.g["gravity_first"])
        self.assertIn("Higgs",self.g["specific_first_falsifier"])
        self.assertIn("missing q=0",self.g["specific_first_falsifier"])
        self.assertIn("anomaly",self.g["particle_first"])

if __name__=="__main__":unittest.main()
