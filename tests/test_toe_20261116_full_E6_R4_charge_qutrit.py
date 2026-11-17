"""Independently cross-check new five-front M/IIB/E6/qutrit results."""
from pathlib import Path
from fractions import Fraction as F
import importlib.util,math,unittest
ROOT=Path(__file__).resolve().parents[1]/"analysis"
def load(name,filename):
    spec=importlib.util.spec_from_file_location(name,ROOT/filename)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module
flux=load("nearfirst","toe_20261116_nearequal_KK_firstorder_exchange.py")
control=load("r4control","toe_20261116_8derivative_shape_control.py")
tri=load("twohiggs","toe_20261116_E6_two_Higgs_SM_stabilizer.py")
full=load("fulle6","toe_20261116_E6_full_cubic_SM_stabilizer.py")
charges=load("fluxheis","toe_20261116_M_IIB_flux_Heisenberg_CRT.py")
qutrit=load("temporaldrift","toe_20261116_qutrit_randomized_memory_drift.py")

class GeometricStability(unittest.TestCase):
    def test_initial_equal_mass(self):
        self.assertAlmostEqual(flux.MASS0,-5.016944081307837,places=11)
    def test_firstorder_torus_geometry(self):
        for N in (100,1000,10000):
            rec=flux.near(N)
            self.assertLess(rec["lambda_from_exact_period_geometry"],flux.LAMBDA0)
            self.assertTrue(rec["equal_flux_formula_at_unequal_geometry_PROXY_NOT_EIGENMASS"]<flux.MASS0)
        self.assertAlmostEqual(flux.near(100000)["N_times_proxy_mass_minus_mass0"],flux.PREDICTION_COEFFICIENT,delta=.0005)
    def test_conditional_not_full_KK_mass(self):
        rec=flux.verify()
        self.assertIn("Requires exact",rec["assumptions"])
        self.assertIn("O(N^-2)",rec["assumptions"])
    def test_shape_radii(self):
        a=control.geometry(1000000,100j,5)
        b=control.geometry(1000000,1000j,5)
        self.assertTrue(a["all_internal_cycles_above_cutoff"])
        self.assertFalse(b["all_internal_cycles_above_cutoff"])
    def test_eightderivative_threshold(self):
        self.assertAlmostEqual(control.DELTA*(9*math.pi/2)**2,92.64323741139292)
        self.assertFalse(control.correction_bound(1,1000)["BF_instability_certified_under_assumed_operator_norm"])
        self.assertTrue(control.correction_bound(1000,1000)["BF_instability_certified_under_assumed_operator_norm"])
    def test_r4_does_not_claim_coeff(self):
        note=control.correction_bound(100,1000)["physics_condition"]
        self.assertIn("NOT an M-theory R4 coefficient determination",note)

class E6Symmetry(unittest.TestCase):
    def test_full_rational_ranks(self):
        r=full.verify()
        self.assertEqual([r["E6_Lie_dim"],r["surviving_SU5_Lie_dim"],r["SM_Lie_dim"]],[78,24,12])
        self.assertEqual([r["cubic_derivation_rank"],r["two_Higgs_dual_vev_rank"],r["after_adjoint_rank"]],[651,705,717])
    def test_20_surviving_roots_then_8(self):
        r=full.verify()["root_data"]
        self.assertEqual([r["original_nonzero_roots"],r["Higgs_surviving_nonzero_roots"],r["adjoint_Y_neutral_nonzero_roots"]],[72,20,8])
    def test_27_anomaly_cancellation(self):
        x=full.anomaly_table()
        self.assertEqual(sum(v["dimension"]*v["copies"] for v in x["multiplets"]),27)
        self.assertEqual(x["anomaly_checks_exact"]["U1_cubed"],"0")
        self.assertEqual(x["anomaly_checks_exact"]["SU3_squared_U1"],"0")
        self.assertEqual(x["anomaly_checks_exact"]["Witten_SU2_doublets"],6)
    def test_manifest_mass_multiplicities(self):
        p=tri.exact_certificate()
        self.assertEqual(p["manifest_stabilizer_dimension"],4)
        self.assertEqual(p["mass2_spectrum_equal_couplings_with_two_conjugate_pairs"],
                         [("0",4),("g^2*v^2",4),("2*g^2*v^2",7),("10*g^2*v^2/3",1)])
    def test_each_cubic_Higgs_polarization_F_flat(self):
        V,W=tri.fields()
        t,u=tri.S.symbols("t u")
        self.assertEqual((t*V+u*W).det(),0)
        self.assertTrue(all(x==0 for x in (t*V+u*W).adjugate()))

class HeisenbergTopologicalBoundary(unittest.TestCase):
    def test_cocycle_and_27(self):
        p,q=(1,0,0),(0,1,0)
        self.assertEqual(charges.comm(p,q,3),(0,0,2))
        self.assertEqual(charges.group_certificate(3)["group_order"],27)
        self.assertTrue(charges.verify_qutrit()["Fourier_and_phase_Clifford_checks"])
    def test_CRT_six(self):
        self.assertTrue(charges.crt_certificate(2,3)["qutrit_factor_appears"])
        self.assertEqual(charges.group_certificate(9)["center_order"],9)
    def test_gcd_collapse(self):
        for N in (3,9,100):
            x=charges.topology_sequence(N)
            self.assertEqual(x["equal_candidate_H_group_order"],N**3)
            self.assertEqual(x["near_equal_candidate_H_group_order"],1)
    def test_candidate_not_physical_assumption(self):
        self.assertTrue(charges.verify()["mathematical_model_only"])

class RandomizedQutrit(unittest.TestCase):
    def test_nonIID_exact_bound(self):
        self.assertEqual(qutrit.null_p_value(1,10,.01),1.)
        self.assertAlmostEqual(qutrit.null_p_value(10,10,0.),math.exp(-5))
    def test_power_matches_earlier_binned_plan(self):
        self.assertEqual(qutrit.power_plan(.75,.7,.01)["required_heralded_trials"],1248)
        self.assertIsNone(qutrit.power_plan(.75,.5,.01)["required_heralded_trials"])
    def test_synthetic_randomized_models(self):
        r=qutrit.verify()["synthetic_samples"]
        self.assertTrue(r[0]["reject_separability_at_one_percent"])
        self.assertFalse(r[1]["reject_separability_at_one_percent"])
        self.assertEqual(r[0]["trials"],r[1]["trials"])
    def test_adaptive_null_near_detection_limit(self):
        r=qutrit.simulate(2500,seed=999,kind="adaptive_separable",eta=1.,eps=.01)
        self.assertGreater(r["separable_null_supermartingale_p_bound"],.01)
    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):qutrit.power_plan(.7,1.4)
        with self.assertRaises(ValueError):control.geometry(100,.8+.3j)
if __name__=="__main__":unittest.main()
