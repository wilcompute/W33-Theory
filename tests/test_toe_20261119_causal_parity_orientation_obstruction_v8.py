"""Exact parity/orientation obstruction in a reflection-symmetric causal order."""
import math,pathlib,sys,unittest
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_causal_parity_orientation_obstruction_v8 as p
import toe_20261119_causal_nerve_transfer_interference_flavor_v6 as v
import toe_20261119_order_to_wilson_dirac_critical_path_v7 as bridge

class CausalParityCriticalMissingInput(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=p.run()
        cls.items=cls.r["reflected_synthetic_causal_order_cases"]

    def test_three_symmetric_causal_cylinders_checked(self):
        self.assertEqual([(x["n"],x["shadow_radius"]) for x in self.items],[(12,1),(12,2),(20,1)])

    def test_reflection_is_an_exact_automorphism_of_causal_relation(self):
        for n,r in ((12,1),(12,2),(20,1)):
            R=v.causal_ring_order(n,r)
            q=p.reflection_permutation(n)
            P=np.r_[q,q+n]
            self.assertTrue(np.array_equal(R,R[np.ix_(P,P)]))

    def test_recovered_cycle_is_reflected_to_reverse_orientation(self):
        for x in self.items:
            self.assertTrue(x["mapped_oriented_cycle_edges_all_reversed"])
            self.assertEqual(x["integer_H1_generator_reflection_eigenvalue"],-1)

    def test_reflection_invariant_nonzero_integer_orientation_impossible(self):
        for x in self.items:
            self.assertFalse(x["nonzero_automorphism_invariant_integer_H1_orientation_possible"])
            self.assertEqual(x["reconstructed_nerve_H0_H1"],[1,1])

    def test_reflection_preserves_mod2_spin_twist_sectors(self):
        for x in self.items:
            self.assertEqual(x["spin_Z2_holonomies_survive_reflection"],[0,1])
            self.assertEqual((-1)%2,1)

    def test_twist_reverse_conjugates_wilson_determinant(self):
        for x in self.items:
            d=complex(*x["det_theta_real_imag"])
            d_rev=complex(*x["det_reverse_theta_real_imag"])
            self.assertLess(abs(d-d_rev.conjugate()),1e-11)
            self.assertGreater(abs(d.imag),.1)

    def test_wilson_det_magnitude_cannot_detect_orientation_sign(self):
        for x in self.items:
            d=complex(*x["det_theta_real_imag"])
            d_rev=complex(*x["det_reverse_theta_real_imag"])
            self.assertAlmostEqual(abs(d),abs(d_rev),places=12)

    def test_reflection_can_be_broken_by_a_distinct_causal_relation(self):
        n=12;R=v.causal_ring_order(n,1).copy()
        R[0,n+0]=0
        P=np.r_[p.reflection_permutation(n),p.reflection_permutation(n)+n]
        # To break reflection, remove a relation not fixed by the reflection.
        R=v.causal_ring_order(n,1).copy()
        R[0,n+1]=0
        self.assertFalse(np.array_equal(R,R[np.ix_(P,P)]))

    def test_orientation_parity_no_go_is_not_a_general_chiral_gravity_theorem(self):
        self.assertIn("reflection-symmetric",self.r["exact_proof"])
        self.assertIn("spontaneous parity breaking",self.r["does_not_falsify"])
        self.assertFalse(self.r["SM_weak_chirality_derived"])
        self.assertFalse(self.r["TOE_solved"])

    def test_orientation_recovery_not_automatically_supplied_by_betti_one(self):
        r=bridge.recover_circle_graph_from_order(v.causal_ring_order(12,1),12)
        self.assertEqual(r["nerve_homology"]["betti_H0_H1_mod2"],[1,1])
        self.assertEqual(p.reflection_certificate()["integer_H1_generator_reflection_eigenvalue"],-1)

if __name__=="__main__":unittest.main()
