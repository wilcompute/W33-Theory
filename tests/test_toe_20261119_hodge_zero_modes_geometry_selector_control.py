"""Independent finite-complex Hodge zero-mode control tests (not spinor physics)."""
from __future__ import annotations
import pathlib,sys,unittest
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_hodge_zero_modes_geometry_selector_control as m

class HodgeTopologyZeroModes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=m.test()

    def test_torus_betti_exactly_121(self):
        for n in (3,4,5):
            self.assertEqual(self.result["topological_torus_complexes"][str(n)]["cellular_Betti_H0_H1_H2"],[1,2,1])

    def test_filled_square_disk_betti_exactly_100(self):
        self.assertEqual(self.result["contractible_filled_square_disk_complex"]["cellular_Betti_H0_H1_H2"],[1,0,0])

    def test_torus_boundaries_compose_to_zero(self):
        for n in (3,4,5):
            B1,B2=m.torus_cellular_operators(n)
            np.testing.assert_array_equal(B1@B2,np.zeros_like(B1@B2))

    def test_disk_boundaries_compose_to_zero(self):
        B1,B2=m.filled_square_cellular_operators()
        np.testing.assert_array_equal(B1@B2,np.zeros_like(B1@B2))

    def test_torus_two_Hodge_one_form_zero_modes(self):
        for n in (3,4,5):
            B1,B2=m.torus_cellular_operators(n)
            L=B1.T@B1+B2@B2.T
            eigen=np.linalg.eigvalsh(L.astype(float))
            self.assertEqual(int(np.sum(abs(eigen)<1e-8)),2)

    def test_disk_has_no_Hodge_one_form_zero_modes(self):
        B1,B2=m.filled_square_cellular_operators()
        L=B1.T@B1+B2@B2.T
        self.assertGreater(np.min(np.linalg.eigvalsh(L.astype(float))),1.)

    def test_disk_Laplacian_eigenvalues_are_2_2_4_4(self):
        B1,B2=m.filled_square_cellular_operators()
        eig=np.linalg.eigvalsh((B1.T@B1+B2@B2.T).astype(float))
        np.testing.assert_allclose(eig,[2,2,4,4],atol=1e-13)

    def test_torus_n3_smallest_nonzero_Hodge_eigenvalue_is_3(self):
        e=self.result["topological_torus_complexes"]["3"]["Hodge_L1_eigenvalues"]
        nonzero=[x for x in e if x>1e-8]
        self.assertAlmostEqual(min(nonzero),3.)

    def test_torus_zero_mode_determinant_factor_mu_squared(self):
        for row in self.result["finite_mass_regulator_zero_mode_factors"]:
            self.assertAlmostEqual(row["torus_normalized_determinant_zero_mode_factor"],
                                   row["expected_mu_squared"],delta=1e-8*row["expected_mu_squared"])

    def test_disk_normalized_topological_zero_factor_is_one(self):
        for row in self.result["finite_mass_regulator_zero_mode_factors"]:
            self.assertEqual(row["disk_normalized_zero_mode_factor"],1.)

    def test_naive_massless_determinant_can_suppress_good_torus(self):
        rows=self.result["finite_mass_regulator_zero_mode_factors"]
        factors=[r["torus_normalized_determinant_zero_mode_factor"] for r in rows]
        self.assertGreater(factors[0],factors[1])
        self.assertGreater(factors[1],factors[2])

    def test_different_cell_counts_preclude_full_uncontrolled_weight_comparison(self):
        self.assertNotEqual(self.result["topological_torus_complexes"]["3"]["V_E_F"],
                            self.result["contractible_filled_square_disk_complex"]["V_E_F"])
        self.assertIn("unequal numbers of cells",self.result["physical_caution"])

    def test_Hodge_laplacian_not_asserted_as_Lorentzian_chiral_Dirac(self):
        self.assertIn("not a valid comparison",self.result["physical_caution"])
        self.assertFalse(self.result["TOE_solved"])

if __name__=="__main__": unittest.main()
