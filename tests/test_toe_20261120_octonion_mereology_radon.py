"""Focused repeatable checks for five-front Witting/G2 finite research."""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261120_octonion_mereology_radon as F

class IndependentFiveFrontGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=F.run()
        cls.a=cls.result["quantum_mereology"]
        cls.b=cls.result["G2_hexagon"]
        cls.c=cls.result["Radon_tomography"]
        cls.d=cls.result["E8_and_symmetric_action"]
    def test_01_exact_45_frames(self):self.assertEqual(self.a["charts"],45)
    def test_02_exact_1800_state_frame_cases(self):self.assertEqual(self.a["state_chart_checks"],1800)
    def test_03_per_frame_product_vs_entangled(self):self.assertEqual((self.a["local_states_per_chart"],self.a["entangled_states_per_chart"]),(8,32))
    def test_04_nine_vs_thirtysix_frame_view(self):self.assertEqual((self.a["product_charts_per_state"],self.a["entangled_charts_per_state"]),(9,36))
    def test_05_purity_from_actual_Pauli_traces(self):self.assertLess(self.a["maximal_quantum_purity_error"],1e-10)
    def test_06_noncommuting_pair_selects_unique_frame(self):self.assertEqual(self.a["noncommuting_pair_frame_multiplicity"],1)
    def test_07_commuting_pair_leaves_three_frames(self):self.assertEqual(self.a["commuting_pair_frame_multiplicity"],3)
    def test_08_counts_of_both_pair_types(self):self.assertEqual(self.a["commuting_pair_count"]+self.a["noncommuting_pair_count"],780)
    def test_09_split_octonion_null_projective_count(self):self.assertEqual(self.b["points"],364)
    def test_10_split_octonion_hexagon_lines(self):self.assertEqual(self.b["lines"],364)
    def test_11_G2_girth_twelve(self):self.assertEqual(self.b["incidence_girth"],12)
    def test_12_G2_spectrum_exact_multiplicities(self):self.assertEqual(self.b["point_graph_eigenvalues"],{12:1,5:104,-1:168,-4:91})
    def test_13_G2_729_cycle_Steinberg_degree(self):self.assertEqual(self.b["betti_1"],self.b["known_Steinberg_dimension"])
    def test_14_full_Radon_81_state_operator_span(self):self.assertEqual(self.c["phase_space_operator_span_rank"],81)
    def test_15_Radon_random_positive_states(self):self.assertEqual(self.c["probabilities_tested"],1620)
    def test_16_Radon_numerical_agreement(self):self.assertLess(self.c["max_Radon_Wigner_error"],1e-11)
    def test_17_Radon_operator_calibration(self):self.assertLess(self.c["max_operator_identity_error"],1e-11)
    def test_18_40_reflection_commutant(self):self.assertEqual(self.d["full_matrix_commutant_dimension"],2)
    def test_19_symmetric_Hamiltonian_cannot_choose_one_ray(self):self.assertTrue(self.d["Witting_ray_selection_requires_symmetry_breaking"])
    def test_20_prior_E8_root_fibers(self):self.assertEqual((self.d["E8_prior_root_count"],self.d["E8_prior_projective_ray_count"],self.d["root_phase_lifts_per_ray"]),(240,40,6))

if __name__=="__main__":unittest.main()
