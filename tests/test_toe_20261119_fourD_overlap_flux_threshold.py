"""Independent full 4D U1 overlap index versus regulator-smoothness tests."""
import pathlib,sys,unittest
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_fourD_overlap_flux_threshold as q

class FourDOverlapFluxIndex(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=q.run_all()
        cls.cases=cls.r["cases"]

    def test_fourD_Clifford_anticommutation(self):
        self.assertLess(cls_residual:=q.gamma_relations(),1e-12)

    def test_gamma5_anticommutes_all_four_gammas(self):
        for g in q.G:
            self.assertLess(np.linalg.norm(q.G5@g+g@q.G5),1e-12)

    def test_4D_flux_plaquette_orientations_all_six_planes(self):
        cases=self.cases
        self.assertEqual(len(cases),7)
        for r in cases:
            angles=r["mean_plaquette_flux_angles"]
            self.assertAlmostEqual(angles["12"],2*np.pi*r["Q12"]/r["L"]**2)
            self.assertAlmostEqual(angles["34"],2*np.pi*r["Q34"]/r["L"]**2)
            for plane in ("13","14","23","24"):
                self.assertAlmostEqual(angles[plane],0)

    def test_flat_T4_has_zero_overlap_index(self):
        a=next(c for c in self.cases if (c["L"],c["Q12"],c["Q34"])==(3,0,0))
        self.assertEqual(a["finite_overlap_index"],0)
        self.assertGreater(a["kernel_gap"],.9)

    def test_one_plane_flux_yields_zero_F_wedge_F_index(self):
        a=next(c for c in self.cases if (c["L"],c["Q12"],c["Q34"])==(3,1,0))
        self.assertEqual(a["finite_overlap_index"],0)

    def test_two_orthogonal_flux_planes_yield_unit_4D_index(self):
        a=next(c for c in self.cases if (c["L"],c["Q12"],c["Q34"])==(3,1,1))
        self.assertEqual(a["continuum_Chern_character_Q12_times_Q34"],1)
        self.assertEqual(a["finite_overlap_index"],1)
        self.assertGreaterEqual(a["overlap_zero_mode_count_when_full_operator"],1)

    def test_4D_overlap_Ginsparg_Wilson_relation(self):
        a=next(c for c in self.cases if (c["L"],c["Q12"],c["Q34"])==(3,1,1))
        self.assertLess(a["Ginsparg_Wilson_residual_when_full_operator"],1e-10)

    def test_orientation_reversal_reverses_4D_topological_index(self):
        pos=next(c for c in self.cases if (c["L"],c["Q12"],c["Q34"])==(3,1,1))
        neg=next(c for c in self.cases if (c["L"],c["Q12"],c["Q34"])==(3,1,-1))
        self.assertEqual(pos["finite_overlap_index"],-neg["finite_overlap_index"])

    def test_both_flux_orientations_reversed_keep_index_sign(self):
        a=next(c for c in self.cases if (c["L"],c["Q12"],c["Q34"])==(3,-1,-1))
        self.assertEqual(a["finite_overlap_index"],1)

    def test_coarse_L2_counterexample_to_unqualified_finite_index_claim(self):
        coarse=next(c for c in self.cases if (c["L"],c["Q12"],c["Q34"])==(2,1,1))
        self.assertEqual(coarse["continuum_Chern_character_Q12_times_Q34"],1)
        self.assertEqual(coarse["finite_overlap_index"],0)
        self.assertGreater(coarse["kernel_gap"],.1)

    def test_large_flux_on_L3_also_fails_naive_4D_index(self):
        coarse=next(c for c in self.cases if (c["L"],c["Q12"],c["Q34"])==(3,1,2))
        self.assertEqual(coarse["continuum_Chern_character_Q12_times_Q34"],2)
        self.assertEqual(coarse["finite_overlap_index"],1)

    def test_no_4D_gravity_or_SM_derivation(self):
        self.assertFalse(self.r["TOE_solved"])
        self.assertFalse(self.r["dynamical_4D_spacetime_derived"])
        self.assertFalse(self.r["physical_SM_chiral_gauge_theory_constructed"])
        self.assertTrue(self.r["field_and_fourD_torus_inserted_as_inputs"])

if __name__=="__main__":unittest.main()
