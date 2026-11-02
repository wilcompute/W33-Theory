"""Five targeted exact regressions for the 216-route POVM continuation."""
import importlib.util
import json
import pathlib
import unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis"/"w33_20261102_povm_spectrum_and_duality.py"
SPEC=importlib.util.spec_from_file_location("w33_route_povm", SCRIPT)
MODULE=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

class RoutePovmFiveFronts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=MODULE.main()
    def test_abstract_povm_is_normalized(self):
        p=self.data["povm"]
        self.assertEqual(p["dimension"],24)
        self.assertEqual(p["outcomes"],216)
        self.assertEqual(p["sum_effects"],"I_24")
    def test_exact_non_ic_operator_spectrum(self):
        self.assertEqual(self.data["effect_squared_gram"]["integer_eigenvalues"],
          {"0":15,"576":15,"768":81,"2304":80,"3168":24,"14400":1})
        self.assertEqual(self.data["povm"]["operator_span_exact_rank"],201)
        self.assertFalse(self.data["povm"]["informationally_complete"])
    def test_address_route_cross_incidence(self):
        self.assertEqual(self.data["cross_point_overlap_distribution"],
                         {0:1080,4:6480,6:2160})
        self.assertEqual(self.data["address_minimum_words"],45)
        self.assertEqual(self.data["route_minimum_words"],216)
    def test_full_generator_covariance(self):
        self.assertEqual(self.data["clifford_transvections_checked"],40)
        self.assertEqual(self.data["point_stabilizer_108_split_first_moments"],
                         {-12:27,18:12,108:1})
    def test_invariant_cubic_and_unital_obstruction(self):
        self.assertEqual(self.data["invariant_cubic_frobenius_norm_squared"],27371520)
        self.assertFalse(self.data["equivariant_unital_Jordan_on_24d"])
if __name__=="__main__":unittest.main()
