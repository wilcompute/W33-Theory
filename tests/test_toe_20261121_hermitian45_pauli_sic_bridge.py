"""Regression for exact Hermitian 45 <-> Witting/Pauli tensor-chart bridge."""
import importlib.util
from pathlib import Path
import unittest

FILE = Path(__file__).resolve().parents[1]/"analysis/toe_20261121_hermitian45_pauli_sic_bridge.py"
spec=importlib.util.spec_from_file_location("toe_20261121_hermitian45_pauli_sic_bridge",FILE)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class TestHermitian45PauliSIC(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=module.analyze()

    def test_all_85_and_complex_reduction(self):
        self.assertEqual((self.d["PG34_points"],self.d["Hermitian_isotropic_points"],
                          self.d["Hermitian_anisotropic_Witting_points"]),(85,45,40))
        self.assertTrue(self.d["GF4_complex_orthogonality_exact_match"])

    def test_all_45_tensor_decompositions(self):
        self.assertEqual(self.d["Pauli_tensor_charts"],45)
        self.assertEqual(self.d["two_qutrit_nondegenerate_planes"],90)
        self.assertTrue(self.d["isotropic_polar_supports_identical_to_all_45_Pauli_charts"])
        self.assertEqual(len(self.d["isotropic_GF4_point_to_Pauli_chart_support"]),45)

    def test_qubit_SIC_and_normalization(self):
        self.assertEqual(self.d["qubit_SIC_subspace_rank_counter"],{2:90})
        self.assertLess(self.d["max_SIC_overlap_residual"],1e-11)
        self.assertLess(self.d["max_8ray_sum_minus_2I_residual"],1e-11)

    def test_integer_incidence_smith(self):
        self.assertEqual(self.d["W33_point_line_incidence_smith_normal_form"],{1:25,0:15})
        self.assertEqual(self.d["chart_incidence_spectrum"],{72:1,12:24,0:15})
        self.assertEqual(self.d["chart_pair_intersections"],{2:720,0:270})

    def test_dual_measurement_marginal(self):
        self.assertLess(self.d["max_dual_POVM_marginal_residual"],1e-12)
        self.assertEqual(self.d["Witting_projector_Gram_spectrum"],{10:1,2:15,0:24})

if __name__ == "__main__":
    unittest.main()
