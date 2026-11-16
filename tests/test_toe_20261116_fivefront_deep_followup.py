"""Regression suite for five independent TOE follow-ups and arithmetic control."""
import importlib.util,math,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"analysis"

def load(name,file):
    sp=importlib.util.spec_from_file_location(name,ROOT/file)
    m=importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m

bf=load("bf2","toe_20261116_robust_torus_BF_nearequal.py")
kt=load("kt2","toe_20261116_twisted_K_Tduality_resolutions.py")
spin=load("spin2","toe_20261116_spin_winding_SL2_orbits.py")
e6=load("e6soft","toe_20261116_E6_soft_gauge_falsifier.py")
optic=load("optic2","toe_20261116_qutrit_eventready_loss_bound.py")
oldopt=load("opticold","toe_20261116_qutrit_four_MUB_experiment.py")

class PhysicalBF(unittest.TestCase):
    def test_equal_order_one_gap(self):
        for n in (1,10,100,1000):
            x=bf.equal_exact(n)
            self.assertAlmostEqual(x["BF_violation"],1.0169440813078374,places=11)
            self.assertLess(x["physical_odd_scalar_mass2_L2"],-5)
    def test_8derivative_required_coefficient_grows_quadratically(self):
        a,b=bf.equal_exact(10),bf.equal_exact(100)
        self.assertAlmostEqual(b["hypothetical_Ccrit_for_shift_C_lp_over_L_to_sixth"]/a["hypothetical_Ccrit_for_shift_C_lp_over_L_to_sixth"],100)
    def test_near_equal_torus_area_and_radius(self):
        a,b=bf.unequal_geometry(100),bf.unequal_geometry(1000)
        self.assertLess(abs(b["square_torus_first_lambda"]-3*math.pi),abs(a["square_torus_first_lambda"]-3*math.pi))
        self.assertGreater(b["L_over_lp"],a["L_over_lp"])
        self.assertTrue(b["NOT_A_PHYSICAL_UNEQUAL_FLUX_EIGENMASS"])
    def test_whole_verifier(self):self.assertTrue(bf.verify()["status"].startswith("PASS"))

class TopologicalTdual(unittest.TestCase):
    def test_unit_twist_resolves_extension(self):
        for p,q in [(3,3),(6,10),(-4,-4),(3,0),(0,7),(1,1)]:
            g=math.gcd(p,q)
            for k in (-1,1):
                r=kt.resolve(p,q,k)
                self.assertEqual(r["K0_exact"],f"Z_{g} + Z_{g}" if g>1 else "0")
                self.assertEqual(r["K1_exact"],"0")
    def test_tdual_pushforward(self):
        r=kt.resolve(6,10,1)
        self.assertEqual(r["dual_c1"],[3,-5])
        self.assertEqual(r["dual_twist"],2)
        self.assertEqual(r["dual_H3_pushforward"],[3,5])
    def test_lens_product_resolves_all_nonzero_twists(self):
        for k in (2,3,7):
            r=kt.resolve(6,0,k)
            self.assertEqual(r["K0_exact"],"Z_6 + Z_6")
            self.assertEqual(r["K1_exact"],f"Z_{k} + Z_{k}")
    def test_unresolved_cases_stay_unresolved(self):
        self.assertIsNone(kt.resolve(3,3,2)["K0_exact"])
        self.assertIsNone(kt.resolve(3,3,2)["K1_exact"])
    def test_full_verifier(self):self.assertTrue(kt.verify()["status"].startswith("PASS"))

class SL2TopologyVsSpin(unittest.TestCase):
    def test_six_orbits(self):
        a=spin.orbit_table(6)["orbits"]
        self.assertEqual([(v["gcd_divisor"],v["orbit_cardinality"]) for v in a],[(1,24),(2,8),(3,3),(6,1)])
    def test_prime_and_primepower(self):
        self.assertEqual([x["orbit_cardinality"] for x in spin.orbit_table(5)["orbits"]],[24,1])
        self.assertEqual([x["orbit_cardinality"] for x in spin.orbit_table(4)["orbits"]],[12,3,1])
    def test_spinor_not_arbitrary_winding(self):
        self.assertFalse(spin.compare_spin_and_species(3)["spinor_cover_modes_survive"])
        self.assertTrue(spin.compare_spin_and_species(2)["spinor_cover_modes_survive"])
        self.assertEqual(spin.totient_two(6),24)
    def test_equal_to_nearequal_global_topology_jump(self):
        for n in (2,3,10,100,1000):
            v=spin.quantized_flux_topology_jump(n)
            self.assertEqual(v["equal_pi1"],f"Z_{n}")
            self.assertEqual(v["near_equal_pi1"],"trivial")
            self.assertEqual(v["equal_complex_K0_torsion_order"],n*n)
            self.assertEqual(v["near_equal_complex_K0_torsion_order"],1)
    def test_full_verifier(self):self.assertTrue(spin.verify()["status"].startswith("PASS"))

class ExceptionalVacuum(unittest.TestCase):
    def test_soft_stationary_gauge_masses(self):
        r=e6.soft_branch(-1,1,1,1)
        self.assertEqual(r["VEV_abs_s"],1)
        self.assertEqual(r["gauge_vector_mass2_eigenvalues"],[0,3,3])
        self.assertEqual(r["radial_canonical_mass2"],4)
        self.assertEqual(r["phase_canonical_mass2"],0)
    def test_rank_obstruction(self):
        r=e6.soft_branch(-4,2,3,.7)
        self.assertLess(r["SU3_diagonal_rank"],r["Standard_Model_gauge_rank"])
        self.assertEqual(sum(r["gauge_multiplicities"].values()),24)
        self.assertFalse(r["full_scalar_stability_proven"])
    def test_supersymmetric_one_loop_supertrace_cancellation(self):
        for g,r in ((1.,1.),(.7,2.),(2.5,.2)):
            v=e6.supersymmetric_gauge_loop_control(g,r)
            self.assertEqual(v["supertrace_mass2"],0)
            self.assertEqual(v["supertrace_mass4"],0)
            self.assertEqual(v["per_multiplet_real_bosonic_dof"],v["per_multiplet_real_fermionic_dof"])
    def test_positive_mass_origin(self):
        self.assertFalse(e6.soft_branch(1,2,3,1)["nonzero_singlet_stationary_point"])
    def test_full_verifier(self):self.assertTrue(e6.verify()["status"].startswith("PASS"))

class QutritEventReady(unittest.TestCase):
    def test_reference_projector_identity(self):
        self.assertLess(oldopt.mubs_identity_error(),1e-12)
    def test_loss_threshold(self):
        self.assertFalse(optic.eventready_plan(.75,.5)["loss_robust_detectable_at_assumed_parameters"])
        self.assertTrue(optic.eventready_plan(.75,.7)["loss_robust_detectable_at_assumed_parameters"])
        self.assertAlmostEqual(optic.eventready_plan(.75,.7)["necessary_eta_threshold_with_zero_calibration_error"],.6)
    def test_gross_trials_and_calibration_penalty(self):
        a=optic.eventready_plan(.75,.7,0)
        b=optic.eventready_plan(.75,.7,.01)
        self.assertEqual(a["gross_attempts_per_basis"],242)
        self.assertEqual(b["gross_attempts_per_basis"],312)
        self.assertEqual(b["total_event_ready_heralded_attempts"],1248)
    def test_invalid_and_undetectable(self):
        self.assertIsNone(optic.eventready_plan(.25,1)["gross_attempts_per_basis"])
        with self.assertRaises(ValueError):optic.eventready_plan(.6,1.1)
    def test_full_verifier(self):self.assertTrue(optic.verify()["status"].startswith("PASS"))
if __name__=="__main__":unittest.main()
