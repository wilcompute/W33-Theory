"""Regression checks for the Klein seven-link ordinary Dirac bound."""
from pathlib import Path
import importlib.util
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "analysis" / "toe_20261117_klein_dirac_flat_twist_gap.py"
SPEC = importlib.util.spec_from_file_location("klein_dirac_check", PATH)
assert SPEC and SPEC.loader
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


class KleinDiracFlatTwistTest(unittest.TestCase):
    def test_full_group_and_commutator(self):
        self.assertEqual(len(mod.GROUP), 55)
        self.assertEqual({mod.commutator(x, y) for x in mod.GROUP
                          for y in mod.GROUP},
                         {(a, 0) for a in range(11)})

    def test_cubic_and_freeness(self):
        d = mod.verify()
        self.assertTrue(d["free_action_on_smooth_cubic_link"])
        self.assertTrue(d["Klein_cubic_invariant_under_D_and_P"])

    def test_character_census(self):
        d = mod.verify()
        self.assertEqual(d["irreducible_complex_representation_dimensions"],
                         [1, 1, 1, 1, 1, 5, 5])
        self.assertEqual(d["flat_complex_line_characters"], 5)
        self.assertEqual(d["spin_structure_count_if_spin"], 1)

    def test_dirac_gap_and_limits(self):
        d = mod.verify()
        self.assertEqual(d["scalar_curvature"], 42)
        self.assertEqual(d["Dirac_eigenvalue_squared_lower_bound"], "49/4")
        self.assertEqual(d["Dirac_absolute_eigenvalue_lower_bound"], "7/2")
        self.assertEqual(
            d["zero_modes_of_ordinary_Dirac_for_any_unitary_flat_twist"], 0)
        self.assertTrue(any("flux-shifted" in x for x in d["scope"]))


if __name__ == "__main__":
    unittest.main()
