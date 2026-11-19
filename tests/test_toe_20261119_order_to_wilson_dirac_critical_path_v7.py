"""Independent critical path: causal order -> nerve topology -> transport cycle -> Wilson determinant."""
import math,pathlib,sys,unittest
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_order_to_wilson_dirac_critical_path_v7 as c
import toe_20261119_causal_nerve_transfer_interference_flavor_v6 as v6

class FromCausalOrderToConditionalFermionDeterminant(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.res=c.run()

    def test_complete_dependency_gate_ran(self):
        self.assertEqual(self.res["status"],"PASS constructive one-dimensional order-to-Wilson bridge")

    def test_no_unsupported_emergent_4D_claims(self):
        self.assertFalse(self.res["TOE_solved"])
        self.assertFalse(self.res["emergent_3plus1_spin_Dirac_derived"])
        self.assertTrue(self.res["metric_and_antichain_supplied"])
        self.assertTrue(self.res["Wilson_mass_and_spin_lift_supplied"])

    def test_causal_shadow_overlap_max_graph_recovers_exact_12_cycle(self):
        R=v6.causal_ring_order(12,1)
        g=c.recover_circle_graph_from_order(R,12)
        self.assertEqual(len(g["edges"]),12)
        self.assertEqual(len(g["cycle_order"]),12)
        self.assertEqual(len(set(g["cycle_order"])),12)

    def test_maximal_overlap_picks_only_neighbors_not_triangle_diagonals(self):
        R=v6.causal_ring_order(12,1)
        g=c.recover_circle_graph_from_order(R,12)
        C=g["common_past_witness_matrix"]
        self.assertEqual(C.shape,(12,12))
        for i in range(12):
            self.assertEqual(C[i,i],3)
            self.assertEqual(C[i,(i+1)%12],2)
            self.assertEqual(C[i,(i+2)%12],1)
            self.assertEqual(C[i,(i+4)%12],0)

    def test_each_recovered_vertex_has_degree_two(self):
        g=c.recover_circle_graph_from_order(v6.causal_ring_order(12,1),12)
        degrees=[0]*12
        for a,b in g["edges"]:
            degrees[a]+=1;degrees[b]+=1
        self.assertEqual(degrees,[2]*12)

    def test_recovered_circle_has_same_topology_as_nerve(self):
        for r in (1,2):
            g=c.recover_circle_graph_from_order(v6.causal_ring_order(12,r),12)
            self.assertEqual(g["nerve_homology"]["betti_H0_H1_mod2"],[1,1])

    def test_overly_small_shadow_has_no_topological_circle(self):
        with self.assertRaises(ValueError):
            c.recover_circle_graph_from_order(v6.causal_ring_order(12,0),12)

    def test_oversmoothed_nerve_rejected_before_Dirac_operator(self):
        for r in (3,4,5):
            with self.assertRaises(ValueError):
                c.recover_circle_graph_from_order(v6.causal_ring_order(12,r),12)

    def test_oversmoothing_can_leave_spurious_ring_if_no_homology_filter(self):
        g=c.recover_circle_graph_from_order(v6.causal_ring_order(12,3),12,require_H1=False)
        self.assertEqual(len(g["edges"]),12)
        self.assertEqual(g["nerve_homology"]["betti_H0_H1_mod2"],[1,0])

    def test_no_spurious_circle_for_disconnected_radius_zero_even_if_unfiltered(self):
        with self.assertRaises(ValueError):
            c.recover_circle_graph_from_order(v6.causal_ring_order(12,0),12,require_H1=False)

    def test_wilson_operator_uses_only_order_recovered_cycle_edges(self):
        rec=c.recover_circle_graph_from_order(v6.causal_ring_order(12,1),12)
        D=c.wilson_operator_on_recovered_cycle(rec,0.,0.)
        edges={frozenset(x) for x in rec["edges"]}
        for i in range(12):
            for j in range(12):
                if i!=j and abs(D[i,j])>1e-10:
                    self.assertIn(frozenset((i,j)),edges)

    def test_reconstructed_circle_massless_periodic_has_one_zero_mode(self):
        g=c.recover_circle_graph_from_order(v6.causal_ring_order(12,2),12)
        D=c.wilson_operator_on_recovered_cycle(g,0.,0.)
        self.assertEqual(sum(np.linalg.svd(D,compute_uv=False)<1e-9),1)
        self.assertAlmostEqual(np.linalg.det(D),0)

    def test_reconstructed_circle_massless_antiperiodic_has_no_zero_modes(self):
        g=c.recover_circle_graph_from_order(v6.causal_ring_order(12,1),12)
        D=c.wilson_operator_on_recovered_cycle(g,0.,np.pi)
        self.assertEqual(sum(np.linalg.svd(D,compute_uv=False)<1e-9),0)
        self.assertAlmostEqual(np.linalg.det(D).real,2,places=12)

    def test_recovered_order_Dirac_determinant_has_exact_Wilson_product(self):
        for n,r in ((12,1),(12,2),(20,1)):
            g=c.recover_circle_graph_from_order(v6.causal_ring_order(n,r),n)
            for mass in (0.,.01,.1):
                for twist in (0.,np.pi):
                    det=np.linalg.det(c.wilson_operator_on_recovered_cycle(g,mass,twist))
                    expected=(1+mass)**n-np.exp(-1j*twist)
                    self.assertLess(abs(det-expected),1e-8)

    def test_independent_antichain_witness_relabelings_preserve_spectrum_det(self):
        e=c.label_covariance_gate(n=12,r=1)
        self.assertEqual(e["status"],"PASS")
        for r in e["fermion_det_invariant_under_event_relabeling"]:
            self.assertLess(r["abs_determinant_difference"],1e-8)

    def test_graph_has_20_edges_for_n20_not_special_n12(self):
        r=self.res["N20_stable_shadow_case"]
        self.assertEqual(r["edges_recovered"],20)
        self.assertEqual(r["H0_H1"],[1,1])

    def test_dependency_Dirac_is_first_unsettled_high_leverage_bottleneck(self):
        dep=self.res["critical_path"]
        self.assertEqual(dep["first_open_minimum_depth_front"],["F"])
        req={a["id"]:a for a in dep["dependencies"]}
        self.assertEqual(req["F"]["prerequisites"],["B"])
        self.assertIn("F",req["G"]["prerequisites"])
        self.assertIn("F",req["H"]["prerequisites"])

    def test_dependency_DAG_is_acyclic_and_sorted(self):
        deps=self.res["critical_path"]["dependencies"]
        i={x["id"]:j for j,x in enumerate(deps)}
        self.assertTrue(all(i[p]<i[x["id"]] for x in deps for p in x["prerequisites"]))

    def test_dependency_graph_does_not_claim_Born_rule_or_full_QG(self):
        d=self.res["critical_path"]["dependencies"]
        self.assertTrue(any("OPEN" in x["status"] for x in d))
        self.assertIn("4D Lorentzian",d[-1]["name"])

if __name__=="__main__":unittest.main()
