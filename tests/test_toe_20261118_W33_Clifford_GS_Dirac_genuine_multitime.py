"""Native Sp4(3) two-qutrit Siegel cross-check and physical falsifier tests."""
import sys,math,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261118_native_W33_dual27_twoqutrit_siegel_crosscheck as W
import toe_20261118_TOE_phys_falsifiers_anomaly_winding_multitime as P

class TOEFiveFrontFurther(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.w=W.run()
        cls.p=P.run()

    def test_native_27_regular_shell(self):
        x=self.w
        self.assertEqual(sorted(t["size"] for t in x["native_W33_point_orbits"]),
                         [1,3,3,3,3,27])
        self.assertEqual(x["point_H27_regular_noncollinear_shell"],27)

    def test_regular_center_three_characters(self):
        x=self.w
        self.assertEqual(x["point_H27_central_cycles"],9)
        self.assertEqual(x["regular_center_character_multiplicities"],
                         {"1":9,"omega":9,"omega2":9})
        self.assertTrue(x["no_invertible_intertwiner"])
        self.assertEqual(x["maximal_linear_equivariant_rank_address_to_E6_operator"],9)

    def test_exact_Siegel_27_symplectic_shears(self):
        self.assertTrue(self.w["native_line_radical_matches_all_27_F3_symmetric_shears"])
        self.assertTrue(self.w["all_27_diagonal_Clifford_operators_distinct"])
        self.assertTrue(self.w["group_law_exact_all_729_pairs"])

    def test_two_qutrit_entangling_CZ_phase(self):
        v=self.w["exact_CZ_01_phase_exponents"]
        self.assertEqual(v,[0,0,0,0,1,2,0,2,1])
        self.assertEqual(self.w["two_qutrit_CZ_entangling_generators"],1)
        self.assertEqual(self.w["local_quadratic_generators"],2)

    def test_radical_intersection_tracks_incidence(self):
        a=self.w["native_point_line_radical_intersection_samples"]
        self.assertEqual({x["incidence"]:x["intersect_radical_size"]
                          for x in a.values()},{0:1,1:9})

    def test_boundary_finite_spinor_index_varies(self):
        z=self.p["Dirac_domain"]["interval_boundary_sensitivity"]
        self.assertEqual([z[x]["chiral_index"] for x in
                          ("free_both","left_Dirichlet","both_Dirichlet")],
                         [1,0,-1])
        self.assertEqual([z[x]["actual_SUSY_D_kernel"] for x in
                          ("free_both","left_Dirichlet","both_Dirichlet")],
                         [1,0,1])

    def test_closed_circle_nonunitary_resonance_not_chiral(self):
        z=self.p["Dirac_domain"]
        self.assertEqual(z["ring_resonance"]["index"],0)
        self.assertEqual(z["ring_resonance"]["kernel_Q"],1)
        self.assertEqual(z["ring_resonance"]["kernel_Q_adj"],1)
        self.assertEqual(z["ring_off_resonance"]["kernel_Q"],0)

    def test_conditional_GS24_requires_level_three(self):
        z=self.p["E6_anomaly"]
        self.assertEqual(z["A_grav_over_24"],-6)
        self.assertEqual(z["U1_Psi_SU3_SU2_GUT_normalized_Y2"],-18)
        self.assertEqual(z["required_k_if_universal_GS24"],3)
        self.assertTrue(z["ratio_independent_of_number_of_complete_spinor_families"])

    def test_winding_lattice_square_hex_degeneracies(self):
        rows=self.p["winding"]["counts"]
        x={(r["flux_ratio"],r["shape"]):r["oriented_winding_modes"] for r in rows}
        self.assertEqual((x[1.,"square"],x[1.,"hex"]),(4,6))
        self.assertEqual((x[.5,"square"],x[.5,"hex"]),(8,6))
        self.assertEqual((x[1.2,"square"],x[1.2,"hex"]),(4,0))
        self.assertEqual((x[1.3,"square"],x[1.3,"hex"]),(0,0))

    def test_three_time_pairwise_CPTP_decompositions(self):
        x=self.p["quantum_three_time"]
        self.assertEqual(len(x["independently_reproduced_four_analytic_pairwise_models"]),4)
        for z in x["independently_reproduced_four_analytic_pairwise_models"]:
            self.assertGreaterEqual(z["p"],z["pairwise_classical_p_threshold"])
            self.assertLess(max(z["pairwise_CPTP_choi_max_errors"]),1e-12)
            self.assertAlmostEqual(z["proven_three_time_witness_upper_bound"],-z["gamma"])

    def test_three_time_genuine_violation(self):
        x=self.p["quantum_three_time"]
        self.assertLess(x["nonclassical_triple_witness_W3"],0)
        self.assertIn("2611.17268",x["paper"])

    def test_witness_visibility_threshold(self):
        z=self.p["quantum_three_time"]
        thr=z["gamma_036_later_depolarizing_visibility_threshold"]
        self.assertAlmostEqual(thr,math.sqrt(1-(.36/2)**2))
        m={r["later_channel_bloch_visibility"]:
           r["this_analytic_axes_witness_negative"] for r in
           z["late_channel_visibility_sweep"]}
        self.assertTrue(m[.985])
        self.assertFalse(m[.98])

if __name__=="__main__":unittest.main()
