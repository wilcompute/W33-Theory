"""Independent tests for the n-copy single-photon SSR/CHSH Pascal-Lucas gate.

Every result is under ideal operational assumptions, not a new TOE.
"""
from __future__ import annotations
import math,pathlib,sys,unittest
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_multicopy_particle_ssr_pascal_chsh as m

class PascalSSRManyCopyBell(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=m.calculate()

    def test_status_and_no_universality_claim(self):
        self.assertFalse(self.r["TOE_solved"])
        self.assertFalse(self.r["physical_photonic_universality_derived"])
        self.assertEqual(len(self.r["explicit_local_number_preserving_matrix_checks"]),9)

    def test_pascal_sector_dimensions_sum_to_total_hilbert_dimension(self):
        for n in range(0,15):
            rows=m.sector_table(n)
            self.assertEqual(sum(x["sector_dim"] for x in rows),2**n)
            self.assertAlmostEqual(sum(x["sector_probability"] for x in rows),1.)

    def test_each_local_number_sector_is_maximally_entangled_schmidt_rank(self):
        for n in range(1,10):
            for row in m.sector_table(n):
                k=row["local_A_photons"]
                self.assertEqual(row["sector_dim"],math.comb(n,k))
                self.assertEqual(row["local_B_photons"],n-k)

    def test_lucas_odd_row_count_independently_calculated(self):
        for n in range(0,60):
            num=sum(math.comb(n,k)%2 for k in range(n+1))
            self.assertEqual(num,2**n.bit_count())

    def test_lucas_odd_iff_bit_subset(self):
        for n in range(0,50):
            for k in range(n+1):
                parity=math.comb(n,k)%2
                subset=int((k&n)==k)
                self.assertEqual(parity,subset)

    def test_maximally_entangled_even_sector_touches_tsirelson(self):
        for d in (2,4,6,8,10):
            s=(2*math.sqrt(2)*(d-d%2)+2*(d%2))/d
            self.assertAlmostEqual(s,2*math.sqrt(2))

    def test_odd_sector_has_one_unpaired_classical_basis_vector(self):
        for d in (1,3,5,7,9):
            val=(2*math.sqrt(2)*(d-1)+2)/d
            self.assertGreaterEqual(val,2)
            self.assertLess(val,2*math.sqrt(2))
            self.assertEqual(d-2*(d//2),1)

    def test_exact_formula_matches_independent_sector_weighting(self):
        for n in range(0,15):
            data=m.formula(n)
            self.assertAlmostEqual(data["SSR_CHSH_supremum"],
                                   data["independent_sector_weighted_sum"],places=12)

    def test_one_copy_cannot_violate_strict_number_ssr(self):
        self.assertAlmostEqual(m.formula(1)["SSR_CHSH_supremum"],2)

    def test_two_copies_reproduce_previous_project_Bell_gate(self):
        self.assertAlmostEqual(m.formula(2)["SSR_CHSH_supremum"],1+math.sqrt(2),places=13)

    def test_odd_copy_after_even_copy_no_ideal_gain(self):
        for t in range(0,12):
            a=m.formula(2*t)["SSR_CHSH_supremum"]
            b=m.formula(2*t+1)["SSR_CHSH_supremum"]
            self.assertAlmostEqual(a,b,places=12)

    def test_ideal_CHSH_is_monotonic_non_decreasing_in_copy_number(self):
        vals=[m.formula(n)["SSR_CHSH_supremum"] for n in range(0,50)]
        self.assertTrue(all(a<=b+1e-12 for a,b in zip(vals,vals[1:])))

    def test_nearly_tsirelson_for_power_of_two_photon_counts(self):
        for n in (2,4,8,16,32):
            gap=2*math.sqrt(2)-m.formula(n)["SSR_CHSH_supremum"]
            expected=(2*math.sqrt(2)-2)*(2./(2**n))
            self.assertAlmostEqual(gap,expected,places=12)

    def test_explicit_observables_each_have_binary_eigenvalues(self):
        for n in (0,1,2,3,4,5):
            eye=np.eye(2**n)
            for O in m.explicit_observables(n):
                np.testing.assert_allclose(O@O,eye,atol=1e-12)
                np.testing.assert_allclose(O.T,O,atol=1e-12)

    def test_observables_commute_with_local_photon_number(self):
        for n in (1,2,3,4,5):
            number=np.diag([a.bit_count() for a in range(2**n)])
            for O in m.explicit_observables(n):
                np.testing.assert_allclose(number@O,O@number,atol=1e-12)

    def test_direct_dense_bipartite_state_reproduces_small_copy_CHSH(self):
        for n in range(0,4):
            D=2**n
            psi=np.zeros(D*D,complex)
            for a in range(D): psi[D*a+(D-1)^a]=1/math.sqrt(D)
            A0,A1,B0,B1=m.explicit_observables(n)
            def full(A,B):return float(np.vdot(psi,np.kron(A,B)@psi).real)
            observed=full(A0,B0)+full(A0,B1)+full(A1,B0)-full(A1,B1)
            self.assertAlmostEqual(observed,m.formula(n)["SSR_CHSH_supremum"],places=12)

    def test_explicit_matrix_construction_n8_reaches_formula(self):
        self.assertAlmostEqual(m.explicit_chsh(8)["explicit_number_conserving_CHSH"],
                               2.821955037834111,places=11)

    def test_every_unpaired_sector_is_classical_not_hidden_violator(self):
        for n in range(0,9):
            odd=sum(row["number_1d_classical_blocks"] for row in m.sector_table(n))
            self.assertEqual(odd,2**n.bit_count())

    def test_no_loss_two_copy_exact_previous_ideal(self):
        self.assertAlmostEqual(m.chsh_with_independent_copy_loss(2,1.),1+math.sqrt(2))

    def test_vacuum_with_all_photons_lost_is_classically_2(self):
        for n in range(2,7):
            self.assertAlmostEqual(m.chsh_with_independent_copy_loss(n,0.),2)

    def test_independent_two_copy_loss_exact_polynomial_from_previous_pass(self):
        for eta in (0.,.1,.4,.75,.9,.95,1.):
            actual=m.chsh_with_independent_copy_loss(2,eta)
            earlier=2-4*eta+(3+math.sqrt(2))*eta*eta
            self.assertAlmostEqual(actual,earlier,places=12)

    def test_fixed_setting_two_copy_survival_threshold_reproduces_prior_gate(self):
        data=self.r["fixed_setting_independent_photon_loss"]["survival_efficiency_records"][0]
        self.assertEqual(data["n"],2)
        self.assertAlmostEqual(data["fixed_settings_positive_thresholds"][0],
                               4/(3+math.sqrt(2)),places=11)

    def test_n4_ideal_gain_does_not_imply_better_threshold_than_n2(self):
        data=self.r["fixed_setting_independent_photon_loss"]["survival_efficiency_records"]
        row={x["n"]:x for x in data}
        self.assertGreater(row[4]["unconditional_zero_loss_CHSH"],
                           row[2]["unconditional_zero_loss_CHSH"])
        self.assertGreater(row[4]["fixed_settings_positive_thresholds"][0],
                           row[2]["fixed_settings_positive_thresholds"][0])

    def test_fixed_settings_thresholds_strictly_between_0_and_1(self):
        for row in self.r["fixed_setting_independent_photon_loss"]["survival_efficiency_records"]:
            t=row["fixed_settings_positive_thresholds"]
            self.assertEqual(len(t),1)
            self.assertGreater(t[0],0.8)
            self.assertLess(t[0],1.)

    def test_no_postselection_probabilities_sum(self):
        n=4
        for eta in (0.,.2,.5,.9,1.):
            val=sum(eta**mask.bit_count()*(1-eta)**(n-mask.bit_count())
                    for mask in range(2**n))
            self.assertAlmostEqual(val,1.,places=13)

    def test_equal_ideal_score_n2_n3_but_unequal_loss_thresholds(self):
        row={x["n"]:x for x in self.r["fixed_setting_independent_photon_loss"]["survival_efficiency_records"]}
        self.assertAlmostEqual(row[2]["unconditional_zero_loss_CHSH"],
                               row[3]["unconditional_zero_loss_CHSH"])
        self.assertGreater(row[3]["fixed_settings_positive_thresholds"][0],
                           row[2]["fixed_settings_positive_thresholds"][0])

    def test_missing_Born_and_gate_synthesis_explicitly_not_claimed(self):
        scope=self.r["proof_and_scope"]["limitations"]
        self.assertIn("does not derive the Born rule",scope)
        self.assertIn("no loss",scope)

if __name__=="__main__": unittest.main()
