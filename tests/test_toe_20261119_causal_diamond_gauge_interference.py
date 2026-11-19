"""Gauge-covariant causal diamond with strictly forward-directed paths."""
import math,pathlib,sys,unittest
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_causal_diamond_gauge_interference as m

class DiamondGaugeInterference(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=m.study()

    def test_diamond_is_a_directed_acyclic_graph(self):
        T=m.diamond_operator([.1,.2,.3,.4])
        np.testing.assert_allclose(np.linalg.matrix_power(T,3),np.zeros((4,4)),atol=1e-15)

    def test_retarded_determinant_is_graph_and_flux_blind(self):
        for t in np.linspace(0,2*math.pi,17):
            T=m.diamond_operator([t,.3,.7,-.8])
            self.assertAlmostEqual(np.linalg.det(1.3*np.eye(4)-.6*T).real,1.3**4,places=12)

    def test_two_forward_paths_interfere(self):
        x=m.observables([0.,0.,0.,0.])
        self.assertGreater(x["retarded_probability_like_intensity"],.1)

    def test_destructive_interference_zero_at_pi(self):
        x=m.observables([0.,0.,0.,math.pi])
        self.assertLess(x["retarded_probability_like_intensity"],1e-25)

    def test_intermediate_phase_has_half_of_constructive_intensity(self):
        x=m.observables([0.,0.,0.,0.])["retarded_probability_like_intensity"]
        y=m.observables([0.,0.,0.,math.pi/2])["retarded_probability_like_intensity"]
        self.assertAlmostEqual(x,2*y,places=12)

    def test_directly_computed_green_matches_two_path_sum(self):
        theta=.7
        T=m.diamond_operator([.2,-.5,.9,theta])
        g=np.linalg.inv(1.3*np.eye(4)-.6*T)
        predicted=(.6**2/1.3**3)*(np.exp(1j*(.2+.9))+np.exp(1j*(-.5+theta)))
        self.assertLess(abs(g[0,3]-predicted),1e-12)

    def test_forty_random_gauge_transformations_preserve_intensity(self):
        self.assertEqual(self.data["random_local_gauge_frame_trials"],40)
        self.assertLess(self.data["largest_gauge_invariant_holonomy_error"],1e-11)

    def test_relative_holonomy_phase_is_gauge_invariant(self):
        x=m.observables([.5,.1,.8,-.3])
        expected=np.exp(1j*(.5+.8-.1+.3))
        self.assertLess(abs(complex(*x["gauge_invariant_relative_holonomy_real_imag"])-expected),1e-12)

    def test_retarded_green_transforms_bifundamentally_at_endpoints(self):
        angles=[.5,.1,.8,-.3];local=np.array([.2,.7,-.4,1.1])
        original=m.diamond_operator(angles)
        U=np.diag(np.exp(1j*local))
        transformed=U@original@U.conj().T
        G=np.linalg.inv(1.3*np.eye(4)-.6*original)
        Gprime=np.linalg.inv(1.3*np.eye(4)-.6*transformed)
        self.assertLess(abs(Gprime[0,3]-np.exp(1j*(local[0]-local[3]))*G[0,3]),1e-12)

    def test_nonzero_forward_path_phase_does_not_require_timing_loop(self):
        x=m.observables([.4,-.1,.7,.5])
        self.assertEqual(x["causal_directed_cycles"],0)
        self.assertNotAlmostEqual(x["gauge_invariant_relative_holonomy_real_imag"][1],0,places=7)

    def test_independent_changed_holonomy_changes_interference_intensity(self):
        left=m.observables([0,0,0,0])["retarded_probability_like_intensity"]
        right=m.observables([0,0,0,math.pi])["retarded_probability_like_intensity"]
        self.assertGreater(left-right,.10)

    def test_phases_are_inputs_not_dynamically_derived(self):
        self.assertFalse(self.data["TOE_solved"])
        self.assertIn("supplied inputs",self.data["physical_limit"])

if __name__=="__main__":unittest.main()
