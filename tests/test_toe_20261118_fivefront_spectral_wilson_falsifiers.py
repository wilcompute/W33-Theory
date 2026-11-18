"""Focused independent regression for November-18 six-front research."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
import toe_20261118_fivefront_spectral_wilson_falsifiers as t


class SixFrontTests(unittest.TestCase):
    def test_F55_holomorphic_character_split(self):
        data=t.holomorphic_character_towers()
        self.assertEqual(data["full_F55_C5_character_coefficients"][3], [0,1,1,1,1])
        self.assertEqual(data["full_F55_C5_character_coefficients"][4], [1,1,1,1,1])
        self.assertEqual([s["first_degree"] for s in data["F55_first_modes"]], [4,3,3,3,3])
        self.assertEqual([s["scalar_laplacian"] for s in data["F55_first_modes"]], [112,72,72,72,72])

    def test_C11_character_and_f_quotient(self):
        data=t.holomorphic_character_towers()
        rows=data["C11_character_coefficients"]
        self.assertEqual(rows[0], [1]+[0]*10)
        self.assertEqual(rows[3][0], 4)
        self.assertEqual(sum(rows[3]), 34)
        self.assertEqual([s["first_degree"] for s in data["C11_first_modes"]][0], 3)
        self.assertEqual(sum(s["first_degree"]==1 for s in data["C11_first_modes"]), 5)
        self.assertEqual(sum(s["first_degree"]==2 for s in data["C11_first_modes"]), 5)

    def test_SU5_branching_gauge_and_matter(self):
        d=t.su5_wilson_ledger()
        self.assertEqual(d["exact_order"], 11)
        self.assertEqual(d["unbroken_SU5_dimension"], 12)
        self.assertEqual(d["broken_SU5_dimension"], 12)
        self.assertEqual(sum(d["matter_27_phase_multiplicities"].values()), 27)
        self.assertEqual(d["phase_zero_matter_components"], 2)
        self.assertEqual(d["C5_compatible_3plus2_holonomies"], [(x,x) for x in range(5)])

    def test_GQ_spectral_multiplicities_and_nonconvergence(self):
        d=t.gq_continuum_obstruction()
        q3=d["rows"][1]
        self.assertEqual((q3["v"],q3["degree"],q3["diameter"]),(40,12,2))
        self.assertEqual(q3["adjacency_eigenvalues"],[12,2,-4])
        self.assertEqual(q3["multiplicities"],[1,24,15])
        self.assertAlmostEqual(q3["normalized_laplacian_nonzero"][0],5/6)
        self.assertAlmostEqual(q3["normalized_laplacian_nonzero"][1],4/3)
        self.assertLess(d["rows"][-1]["spectral_ratio"], q3["spectral_ratio"])

    def test_photonic_exact_errors_and_finite_sample(self):
        d=t.photonic_budget()
        a=d["one_sided_exact_Neyman_Pearson"]
        b=d["efficiency_envelope_robust"]
        self.assertEqual((a["accepted_events"],a["decision_threshold_plus_clicks"]),(235,136))
        self.assertEqual((b["accepted_events"],b["decision_threshold_plus_clicks"]),(490,283))
        for row in (a,b):
            self.assertLessEqual(row["type_I"],.01)
            self.assertLessEqual(row["type_II"],.01)
        with self.assertRaises(ValueError):
            t.min_binomial_test(.5,.65,max_n=234)

    def test_T11_modular_lattice_winding_instability(self):
        d=t.t11_winding_modular_bound()
        self.assertTrue(d["square_modulus_ratio1"]["BF_violated"])
        self.assertTrue(d["hexagonal_modulus_ratio1"]["BF_violated"])
        self.assertLess(1.0,d["critical_ratio_all_axiodilatons"])
        self.assertLess(d["critical_ratio_all_axiodilatons"],d["critical_ratio_square"])
        self.assertAlmostEqual(d["critical_ratio_all_axiodilatons"],1.1026577908435842)

    def test_torsion_CRT_and_scope(self):
        d=t.torsion_and_local_flux()
        self.assertEqual(d["flat_degree4_Cfield_holonomy_classes"],"Z15")
        sectors=d["sector_CRT"]
        self.assertEqual(len(sectors),15)
        self.assertEqual(len({(s["crt_mod3"],s["crt_mod5"]) for s in sectors}),15)


if __name__=="__main__":
    unittest.main()
