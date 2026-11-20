"""Focused independent gates for temporal-order / W33 / tensor-SIC proposal."""
from __future__ import annotations
import sys
import unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
from toe_20261120_symplectic_order_sic_switch import (
    OMEGA, normalize, points, symp, area_triangle, pauli, switch,
    geometry, operator_switch, hesse_sic, sic_operator_frame,
    statistics,quadratic_character_extension,failure_controls,main
)

class ProjectiveGeometryChecks(unittest.TestCase):
    def test_40_points_and_pair_orbits(self):
        g=geometry()
        self.assertEqual((g["points"],g["commuting_unordered_pairs"],
                          g["noncommuting_unordered_pairs"]),(40,240,540))
        self.assertEqual(g["partners_per_noncommuting_pair"],[20,9,9])
    def test_triangle_combinatorics(self):
        g=geometry()
        self.assertEqual((g["fully_noncommuting_triples"],
                          g["projectively_dependent_triples"],
                          g["projectively_independent_triples"]),(3240,360,2880))
        self.assertEqual(g["signed_independent_counts"],{"plus":1440,"minus":1440})
        self.assertEqual(g["signed_dependent_counts"],{"plus":180,"minus":180})
    def test_no_projective_pair_sign_but_projective_triple(self):
        P=points()
        u,v,w=next((a,b,c) for a,b,c in
                    ((P[i],P[j],P[k]) for i in range(40)
                     for j in range(i+1,40) for k in range(j+1,40))
                    if area_triangle(a,b,c))
        self.assertNotEqual(symp(u,v),symp(tuple(-x for x in u),v))
        self.assertEqual(area_triangle(u,v,w),
                         area_triangle(tuple(-x for x in u),v,w))
        self.assertEqual(area_triangle(u,v,w),
                         area_triangle(v,w,u))
        self.assertEqual(area_triangle(u,v,w),
                         (-area_triangle(v,u,w))%3)
    def test_quadratic_character_generalization(self):
        q=quadratic_character_extension()
        rows=q["odd_prime_samples"]
        self.assertEqual([t["prime_field"] for t in rows],[3,5,7,11])
        self.assertEqual([t["chi_of_minus_one"] for t in rows],[-1,1,-1,-1])
        self.assertTrue(all(t["random_nonorthogonal_triples_checked"]>=60 for t in rows))

class ControlledOrderChecks(unittest.TestCase):
    def test_all_780_switches(self):
        r=operator_switch()
        self.assertEqual(r["tested_projective_pair_switches"],780)
        self.assertLess(r["control_phase_residual_max"],2e-14)
        self.assertEqual(r["target_independent_control_x_for_noncommuting"],-.5)
    def test_two_qutrit_operator_order_and_sign(self):
        P=points()
        u,v=next((a,b) for a in P for b in P if symp(a,b)==1)
        rng=np.random.default_rng(4)
        psi=rng.normal(size=9)+1j*rng.normal(size=9)
        psi/=np.linalg.norm(psi)
        ph,_,_=switch(u,v,np.outer(psi,psi.conj()))
        self.assertAlmostEqual(ph.real,-.5)
        self.assertAlmostEqual(ph.imag,np.sqrt(3)/2)
        p_reverse,_,_=switch(v,u,np.outer(psi,psi.conj()))
        self.assertAlmostEqual(p_reverse.imag,-np.sqrt(3)/2)

class SICGateChecks(unittest.TestCase):
    def test_hesse_9_state_frame(self):
        P=hesse_sic()
        self.assertEqual(P.shape,(9,3,3))
        self.assertLess(np.linalg.norm(P.sum(axis=0)-3*np.eye(3)),1e-12)
    def test_81_probe_full_operator_certification(self):
        r=sic_operator_frame()
        self.assertEqual(r["tensor_product_informationally_complete_probes"],81)
        self.assertAlmostEqual(r["frame_Gram_condition_number"],16)
        self.assertLess(r["max_operator_reconstruction_error"],1e-12)
        self.assertAlmostEqual(r["SIC_Gram_inverse_quadratic_certificate"],
                               r["operator_noncentral_Frobenius_norm"]**2,places=10)
        self.assertLess(r["ideal_center_81_probe_deviation_max"],1e-12)
        self.assertTrue(r["simultaneous_gauge_covariance"])
    def test_conservative_finite_shot_scope(self):
        r=statistics()
        self.assertEqual(r["conservative_individual_accepted_shots_per_each_of_162_quadrature_settings"],95717)
        self.assertEqual(r["total_accepted_81_input_2_quadrature_shots"],15506154)
        self.assertEqual(r["accepted_shots_to_resolve_chirality_sign_with_calibrated_frame"],26)
    def test_coherent_order_and_spam_failure_controls(self):
        r=failure_controls()
        self.assertTrue(r['classical_mixture_cannot_reveal_center_phase'])
        self.assertLess(r['definite_order_target_output_difference_for_central_commutator'],1e-12)
        self.assertGreater(r['input_dependent_visibility_falsely_inferred_noncentral_norm'],.1)

    def test_full_producer_metadata_and_bounds(self):
        r=main(write=False)
        self.assertIn("not physical QCD colour",r["physics_boundary"])
        self.assertEqual(r["status"],"PASS_FINITE_SYMPLECTIC_SWITCH_SIC_RECONSTRUCTION")

if __name__=="__main__":unittest.main()
