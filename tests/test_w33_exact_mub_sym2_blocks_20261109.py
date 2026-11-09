"""Regression: exhaustive integer-cyclotomic 5x5 UMUB certificate."""
import importlib.util
from pathlib import Path
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "analysis" / "w33_exact_mub_sym2_blocks_20261109.py"
spec = importlib.util.spec_from_file_location("w33_exact_mub_sym2_blocks_20261109", SOURCE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class ExactMUBCertificate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = module.compute()

    def test_census_and_projectors(self):
        self.assertEqual(self.certificate["geometry"]["maximal_partial_spreads"],
                         {"5": 432, "8": 135, "10": 36})
        self.assertEqual(self.certificate["geometry"]["disjoint_context_pairs"], 540)
        self.assertEqual(self.certificate["exact_checks"]["individual_projector_identities"], 40)

    def test_all_spreads_integer_polynomials(self):
        self.assertEqual(self.certificate["exact_checks"]["all_spread_polynomials"], 603)
        self.assertEqual(self.certificate["exact_checks"]["pentad_positive_triple_traces"], 4320)

    def test_positive_bounds(self):
        s = self.certificate["spectra_of_H_on_Sym2"]
        self.assertEqual(s["5"]["eigenvalue_ninths"], {"1": 36, "16": 9})
        self.assertEqual(s["8"]["eigenvalue_ninths"], {"4": 36, "16": 9})
        self.assertEqual(s["10"]["eigenvalue_ninths"], {"8": 45})

    def test_negative_controls(self):
        _, _, _, neighbors = module.construct_geometry()
        pentads = [s for s in module.maximal_cliques(neighbors) if len(s) == 5]
        for subset in pentads:
            for omitted in subset:
                self.assertTrue(all(omitted in neighbors[i] for i in subset if i != omitted))
        self.assertEqual(sum(5 for _ in pentads), 2160)
        self.assertEqual(module.mul(module.OMEGA, module.OMEGA), module.OMEGA2)
        self.assertEqual(module.add(module.add(module.ONE, module.OMEGA), module.OMEGA2),
                         module.ZERO)

if __name__ == "__main__":
    unittest.main()
