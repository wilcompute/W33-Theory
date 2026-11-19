"""Exhaustive E8 source charge-dressed SO10 Higgs repair regressions."""
import sys,unittest
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_E8_source_dressed_GUT_Higgs_bridge as m

class SourceDressedSO10Bridge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=m.source_dressed_rank_breaking()

    def test_three_source_chiral_spinors_only(self):
        self.assertEqual(self.a["source_spinor_H1"],["16_1","16_2","16_3"])

    def test_five_source_spin10_tens_only(self):
        self.assertEqual(self.a["source_ten_H1"],
                         ["10_12","10_13","10_14","10_24","10_34"])

    def test_all_fifteen_pairings_have_holomorphic_spurions(self):
        self.assertEqual(len(self.a["candidate_all_15_charge_combinations"]),15)
        self.assertTrue(all(x["total_spurion_insertions"]>=3
                            for x in self.a["candidate_all_15_charge_combinations"]))

    def test_minimum_total_holomorphic_degree_is_three(self):
        self.assertEqual(self.a["minimal_total_nonnegative_singlet_spurion_degree"],3)
        self.assertEqual(min(v["total_spurion_insertions"] for v in
                         self.a["candidate_all_15_charge_combinations"]),3)

    def test_explicit_source_H10_34_solution_reuses_B_C_D(self):
        x=self.a["selected_higgs_pair_source_charge_and_10"]
        self.assertEqual(x["pair_vectorlike_16_charge"],"16_1")
        self.assertEqual(x["source_10_H"],"10_34")
        self.assertEqual(x["16H_squared_S"],["B"])
        self.assertEqual(x["bar16H_squared_S"],["C","D"])
        self.assertEqual(x["degrees"],[1,2])

    def test_both_exact_three_component_U1_charges_cancel(self):
        self.assertTrue(self.a["all_Spin10_and_U1cubed_operator_charges_zero"])
        self.assertEqual(self.a["selected_higgs_pair_source_charge_and_10"]["source_16_charge"],[1,0,0])
        self.assertEqual(self.a["selected_higgs_pair_source_charge_and_10"]["source_10_charge"],[-1,-1,0])

    def test_all_three_original_singlet_spurions_have_nonzero_VEV(self):
        B,C,D=self.a["source_spurion_VEVs_B_C_D"]
        self.assertAlmostEqual(B,1.,places=12)
        self.assertAlmostEqual(C,np.sqrt(2.08),places=12)
        self.assertAlmostEqual(D,1.,places=12)

    def test_effective_mass_couplings_from_existing_condensates(self):
        u,v=self.a["dimensionless_effective_couplings_for_unit_UV_coefficients"]
        self.assertAlmostEqual(u,.1,places=12)
        self.assertAlmostEqual(v,np.sqrt(2.08)/100,places=12)
        self.assertGreater(u,0.)
        self.assertGreater(v,0.)

    def test_source_dressed_superpotential_F_terms_vanish(self):
        self.assertTrue(self.a["SU5_component_exact_F_terms_zero"])
        self.assertEqual(self.a["SU5_component_exact_hessian_rank"],6)

    def test_no_cross_Hessian_singlet_to_GUT_masses_at_vacuum(self):
        self.assertTrue(self.a["new_cross_Hessian_to_preexisting_singlet_spurions_zero"])

    def test_combined_19_plus_43_local_Hessian_is_isolated_modulo_gauge(self):
        self.assertEqual(self.a["combined_active_chiral_components"],62)
        self.assertEqual(self.a["combined_hessian_rank"],38)
        self.assertEqual(self.a["combined_hessian_nullity"],24)
        self.assertEqual(self.a["broken_Abelian_plus_Spin10_gauge_complex_dimension"],24)
        self.assertEqual(self.a["combined_local_physical_complex_moduli_count"],0)

    def test_uses_one_new_vectorlike_spinor_pair_not_neutral_H10(self):
        self.assertIn("one extra vectorlike",self.a["new_fields_beyond_original_spectrum"])
        self.assertIn("source 10_34",self.a["new_fields_beyond_original_spectrum"])

    def test_UV_overlap_quantized_anomaly_and_chirality_are_not_claimed(self):
        self.assertIn("no UV messenger",self.a["remaining_anomaly_and_origin_gates"])
        self.assertIn("mirror 16bar Higgs zero mode",self.a["remaining_anomaly_and_origin_gates"])
        self.assertIn("NOT physical",self.a["scientific_interpretation"])
        self.assertIn("compact G2",self.a["remaining_anomaly_and_origin_gates"])

if __name__=="__main__":unittest.main()
