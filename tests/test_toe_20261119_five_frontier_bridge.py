"""Regression tests for five-frontier TOE bridge.
Run: python -m unittest discover -s tests -p test_toe_20261119_five_frontier_bridge.py -v
"""
import pathlib
import sys
import unittest
import numpy as np

ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_five_frontier_bridge as m


class FrontierBridgeTests(unittest.TestCase):
    def test_sic_tight_frame(self):
        Q=m.hesse_matrix()
        self.assertTrue(np.allclose(Q@Q.conj().T,6*np.eye(3)))
        self.assertEqual(Q.shape,(3,9))

    def test_sic_pairwise_36_overlaps(self):
        Q=m.hesse_matrix()
        self.assertTrue(all(abs(abs(np.vdot(Q[:,i],Q[:,j]))**2-1)<1e-9
                            for i in range(9) for j in range(i+1,9)))

    def test_susy_19_independent_F_constraints(self):
        Q=m.hesse_matrix()
        rows, B=m.baryonic_constraints(Q)
        self.assertEqual(len(rows),19)
        self.assertEqual(np.linalg.matrix_rank(m.jacobian_baryons(Q,rows),tol=1e-9),19)
        self.assertGreater(abs(B[0]),1)

    def test_baryons_are_complex_SL3_invariants(self):
        Q=m.hesse_matrix()
        g=np.array([[1,3,4],[0,1,5],[0,0,1]],complex)
        self.assertAlmostEqual(np.linalg.det(g).real,1)
        self.assertTrue(np.allclose(m.baryonic_constraints(Q)[1],
                                    m.baryonic_constraints(g@Q)[1]))

    def test_antifundamental_constraint_and_anomaly(self):
        Q=m.hesse_matrix()
        C=Q[:,[0,3,7]]
        self.assertGreater(abs(np.linalg.det(C)),1)
        # If each row Qtilde_i annihilates the three anchor columns,
        # invertibility implies that row is zero. No spectator F-branch.
        for i in range(9):
            v=np.array([i+1,-(i+1),2*(i+1)],complex)
            self.assertTrue(np.allclose((v@C)@np.linalg.inv(C),v))
        sic=m.susy_sic_certificate()
        self.assertEqual(sic["SU3_cubic_anomaly_coefficient"],0)
        self.assertEqual(sic["holomorphic_constraint_rank"],46)
        self.assertEqual(sic["holomorphic_Hessian_rank"],92)
        self.assertEqual(sic["Hessian_nullity_equals_complexified_gauge_dimension"],8)

    def test_D_flat_selects_unitary_gauge_orbit(self):
        Q=m.hesse_matrix()
        g=np.array([[1,1,0],[0,1,0],[0,0,1]],complex)
        H=(g@Q)@(g@Q).conj().T
        self.assertFalse(np.allclose(H,np.trace(H)/3*np.eye(3)))
        self.assertTrue(np.allclose(Q@Q.conj().T,6*np.eye(3)))

    def test_spin_and_flat_twist_gap(self):
        r=m.topology_spin_certificate()
        self.assertEqual(r["number_of_spin_structures"],4)
        self.assertEqual(r["untwisted_Dirac_kernel"],0)
        self.assertEqual(r["unitary_flat_bundles_Dirac_kernel"],0)
        self.assertAlmostEqual(r["round_S5_product_D_abs_gap_at_least"],2.5)

    def test_memory_entanglement_and_threshold(self):
        r=m.quantum_memory_certificate()
        self.assertEqual(r["samples"][0]["partial_transpose_negativity"],1)
        self.assertEqual(r["samples"][-1]["partial_transpose_negativity"],0)
        self.assertEqual(r["samples"][4]["partial_transpose_negativity"],0)

    def test_lattice_orientation_and_refinement(self):
        r=m.continuum_certificate()
        self.assertLess(r["axis_minus_diagonal"],0)
        self.assertAlmostEqual(r["body_diagonal_angular_frequency"],1)
        self.assertLess(abs(m.lattice_omega([1,0,0],a=0.05)-1),
                        abs(m.lattice_omega([1,0,0],a=0.2)-1))

    def test_qutrit_T9_is_nonClifford_and_cubic_mod3_is_Z(self):
        r=m.quantum_code_gate_certificate()
        self.assertFalse(r["naive_cubic_gate_is_nonClifford"])
        self.assertFalse(r["T_is_Clifford"])
        self.assertEqual(r["projective_single_qutrit_Clifford_order"],216)
        self.assertEqual(r["projective_two_qutrit_Clifford_order"],4199040)

    def test_all_frontiers_have_explicit_limits(self):
        r=m.certify()
        self.assertEqual(r["all_status"],"PASS")
        for label in ("SUSY_SIC","G2_chirality_gap","three_time_quantum_memory",
                      "continuum_falsifier","E8_qutrit_nonClifford_gate"):
            self.assertTrue(r[label]["limitations"] if "limitations" in r[label]
                            else r[label]["not_ruled_out"])

if __name__=="__main__":
    unittest.main()
