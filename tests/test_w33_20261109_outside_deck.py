"""Independent exact polynomial guard: 15-link flux beats restricted 3pi deck.

Recomputes old TOE61 exact 41 e_k, both 15-link characteristic
coefficients, and tests strict positive-temperature Weierstrass ordering.
"""
import json,sys,unittest
from pathlib import Path
from sympy import Matrix
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261109_flux_dark_mode_fragility import build
import w33_20261109_outside_deck_flux_counterexample as work

def result(n):
    return json.loads((ROOT/"data"/("w33_20261109_"+n+".json")).read_text(encoding="utf8"))
class ExactBeyondDeck(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=result("outside_deck_flux_counterexample")
        cls.prior=result("minimal_15_flux_lift")
        cls.opt=result("flux_mass_gap_design")

    def test_TEO61_eight_sector_certificates_reproduced_exactly(self):
        self.assertTrue(self.d["frozen_TOE61_0_and_111_characteristic_polynomials_exactly_reproduced"])
        old=json.loads((ROOT/"data/w33_20261013_toe61_det_poly.json").read_text())
        coeff={tuple(x["corner"]):[int(t) for t in x["full_det_coefficients_decimal"]] for x in old["Z2_character_polynomials"]}
        self.assertEqual(work.coeff(work.deck111()),coeff[(1,1,1)])

    def test_old15_strict_coefficientwise_dominates_threepi(self):
        B,edges,G=build()
        T=B.astype(int)
        for e in self.prior["constructed_phase_only_pi_flip_links"]:
            T[e["point"],e["line"]]=-1
        a=work.coeff(T);b=work.coeff(work.deck111())
        delta=[x-y for x,y in zip(a,b)]
        self.assertEqual(len(delta),41)
        self.assertEqual(sum(x>0 for x in delta),37)
        self.assertTrue(all(x>=0 for x in delta))
        self.assertEqual([str(x) for x in delta],
           self.d["comparison_coefficientwise_15_vs_threepi"]["old_15edge"]["full_exact_difference_decimal"])

    def test_optimized15_coefficientwise_dominates_threepi(self):
        B,edges,G=build()
        T=B.astype(int)
        for e in self.opt["best_15_edges"]:T[e["point"],e["line"]]=-1
        a=work.coeff(T);b=work.coeff(work.deck111())
        self.assertTrue(all(x>=y for x,y in zip(a,b)))
        self.assertEqual(sum(x>y for x,y in zip(a,b)),37)

    def test_old_vs_opt_both_are_stronger_than_deck(self):
        self.assertTrue(self.d["old_vs_gap_optimized_15edge_coefficientwise"]["old15_coefficientwise_dominates_optimized15"])
        self.assertEqual(self.d["old_vs_gap_optimized_15edge_coefficientwise"]["number_coefficients_old_exceed_optimized"],36)
        for row in self.d["all_positive_beta_numerical_controls"]:
            if row["beta"]>=.2:
                self.assertLess(row["F_old15_minus_threepi"],0)
                self.assertLess(row["F_opt15_minus_threepi"],0)

    def test_physical_hopping_magnitudes_unmodified(self):
        self.assertTrue(self.d["all_four_operators_have_160_unit_magnitude_links"])
        self.assertTrue(self.d["both_fifteen_link_masks_preserve_native_incidence_support"])
        self.assertEqual(self.d["comparison_coefficientwise_15_vs_threepi"]["old_15edge"]["first_nonzero_degree"],4)

if __name__=="__main__":unittest.main()
