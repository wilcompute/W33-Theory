"""Independent regression tests: causal exchanges -> relativistic propagator
and exact charged-field curvature failure, with no TOE overclaims."""
import math,pathlib,sys,unittest
import numpy as np
from scipy.special import j0,erfcx
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_causal_exchange_gauge_homerun as h


class CausalExchangeGaugeHomerun(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=h.run_all()
        cls.r=cls.data["results"]

    def test_ordered_pair_comparability_exact_dimensions(self):
        self.assertAlmostEqual(h.ordered_fraction(2),.5)
        self.assertAlmostEqual(h.ordered_fraction(3),8/35)
        self.assertAlmostEqual(h.ordered_fraction(4),.1)

    def test_dimensional_inverse_order_fraction(self):
        for d in [2,2.5,3,3.5,4]:
            self.assertAlmostEqual(h.dimension_from_fraction(
                h.ordered_fraction(d)),d,places=9)

    def test_dimension_sprinkling_recovers_2_3_4_with_input_dimensions(self):
        r=self.r["Myrheim_Meyer_dimension_control"]["data"]
        self.assertEqual([row["input_dimension"] for row in r],[2,3,4])
        for row in r:
            self.assertLess(abs(row["estimated_dimension"]-
                                row["input_dimension"]),.23)

    def test_chain_kernel_zero_mass_is_half_in_every_causet(self):
        rng=np.random.default_rng(7)
        for rho in [1,20,100]:
            u,v=h.sprinkle_1d_uv(2,rho,rng)
            self.assertAlmostEqual(h.chain_mass_kernel_1p1(u,v,rho,0),.5)

    def test_fast_chain_sum_agrees_with_independent_dense_inverse(self):
        rng=np.random.default_rng(11)
        for n in [0,1,3,9,17]:
            u=rng.random(n)*2;v=rng.random(n)*2
            self.assertAlmostEqual(h.chain_mass_kernel_1p1(u,v,12,.8),
                                   h.chain_exact_small(u,v,12,.8),places=12)

    def test_massive_chain_Poisson_averages_converge_to_Bessel(self):
        d=self.r["mass_and_proper_time_from_causal_chains"]
        self.assertAlmostEqual(d["continuum"],.5*j0(1.6),places=12)
        for row in d["density_trials"]:
            self.assertLess(abs(row["sample_mean_retarded_amplitude"]-
                       d["continuum"]),5*row["standard_error"]+.006)

    def test_proper_time_asymptotic_chain_height_scaling(self):
        for row in self.r["mass_and_proper_time_from_causal_chains"]["density_trials"]:
            self.assertGreater(row["asymptotic_chain_proper_time_estimator"],1.4)
            self.assertLess(row["asymptotic_chain_proper_time_estimator"],2.2)

    def test_free_scalar_limit_Bessel_J0(self):
        for m in [0,.3,.8,1.2]:
            s=4.
            self.assertAlmostEqual(h.radial_factor(s,m,0),j0(m*np.sqrt(s)),
                                   places=11)

    def test_charged_massless_limit_is_Bessel_J0_in_flux(self):
        for a in [0,.4,.9,1.2]:
            self.assertAlmostEqual(h.radial_factor(4,0,a),j0(a),
                                   places=11)

    def test_charged_massive_ODE_and_power_series_agree(self):
        for row in self.r["exact_constant_E_charged_KG_and_Poisson_count"]["radial_checks"]:
            self.assertLess(row["series_ODE_absolute_difference"],2e-9)

    def test_charged_KG_coefficient_recurrence(self):
        m=.8;a=.9;c=h.coeff_KG(m,a,15)
        self.assertEqual(c[0],1)
        self.assertAlmostEqual(c[1],-m*m/4)
        for n in range(1,15):
            self.assertAlmostEqual(
               4*(n+1)**2*c[n+1]+m*m*c[n]+a*a*c[n-1]/4,0,places=14)

    def test_Poisson_falling_factorial_estimator_agrees_with_manual_polynomial(self):
        N=5;rho=9.;m=.8;a=.9
        c=h.coeff_KG(m,a,N)
        explicit=0.
        for k in range(N+1):
            falling=math.factorial(N)/math.factorial(N-k)
            explicit+=c[k]*(2/rho)**k*falling
        self.assertAlmostEqual(explicit,
           h.poisson_factorial_KG_estimator(N,rho,m,a),places=13)

    def test_Poisson_event_count_estimator_zero_N_is_local_massless_green(self):
        for m,a in [(.8,0),(.8,.9),(0,.9)]:
            self.assertEqual(h.poisson_factorial_KG_estimator(0,20,m,a),1.)

    def test_Poisson_unbiased_electric_field_statistical_reconstruction(self):
        samples=self.r["exact_constant_E_charged_KG_and_Poisson_count"]["Poisson_unbiased_volume_estimator"]
        self.assertEqual(len(samples),4)
        for row in samples:
            self.assertLess(row["absolute_discrepancy"],5*row["standard_error"]+.003)

    def test_nonzero_gauge_field_has_a_true_loop_flux(self):
        g=self.r["gauge_covariance_vs_dynamical_failure"]
        self.assertGreater(abs(g["electric_field_two_path_holonomy_phase"]),.05)
        self.assertAlmostEqual(g["electric_field_two_path_holonomy_phase"],
                               g["loop_flux_analytic_qE_times_area"],places=12)

    def test_flat_connection_gauge_covariance(self):
        g=self.r["gauge_covariance_vs_dynamical_failure"]
        self.assertLess(g["flat_gauge_covariance_error"],1e-12)
        self.assertLess(g["constant_field_gauge_covariance_error"],1e-12)

    def test_simple_edge_Wilson_phase_is_dynamically_wrong_for_nonzero_F(self):
        g=self.r["gauge_covariance_vs_dynamical_failure"]
        self.assertAlmostEqual(g["naive_massless_Wilson_kernel_at_tau_2"],.5)
        self.assertAlmostEqual(g["exact_massless_charged_kernel_at_tau_2"],
                      .5*j0(.9),places=12)
        self.assertGreater(g["naive_minus_exact_amplitude"],.09)

    def test_corrected_charged_kernel_satisfies_covariant_wave_equation(self):
        g=self.r["gauge_covariance_vs_dynamical_failure"]
        self.assertGreater(g["naive_covariant_KG_PDE_residual_abs_at_event"],.05)
        self.assertLess(g["corrected_covariant_KG_numeric_PDE_residual_abs"],2e-6)

    def test_relativistic_boost_preserves_intrinsic_charged_amplitude(self):
        t=1.8;x=.3;z=.71
        tt=np.cosh(z)*t+np.sinh(z)*x
        xx=np.sinh(z)*t+np.cosh(z)*x
        s=t*t-x*x
        sp=tt*tt-xx*xx
        self.assertAlmostEqual(s,sp,places=12)
        self.assertAlmostEqual(h.radial_factor(s,.8,.9),
                               h.radial_factor(sp,.8,.9),places=11)

    def test_4D_null_link_normalization_and_delta_function_limit(self):
        d=self.r["four_dimensional_null_cone_link_distribution"]
        rows=d["rows"]
        self.assertEqual(len(rows),4)
        self.assertLess(rows[0]["integral_divided_by_distributional_limit"],.8)
        self.assertGreater(rows[-1]["integral_divided_by_distributional_limit"],.96)
        for row in rows:
            rho=row["rho"]
            z=1/(2*np.sqrt((np.pi/24)*rho))
            self.assertAlmostEqual(
              row["test_exp_minus_sigma_integral"]*2*np.pi,erfcx(z),places=13)

    def test_4D_null_shell_width_scales_inverse_sqrt_density(self):
        rows=self.r["four_dimensional_null_cone_link_distribution"]["rows"]
        for i in range(len(rows)-1):
            self.assertAlmostEqual(
               rows[i]["characteristic_null_shell_sigma_mean"]/
               rows[i+1]["characteristic_null_shell_sigma_mean"],4.,places=10)

    def test_no_unwarranted_unification_claims(self):
        self.assertFalse(self.data["TOE_solved"])
        self.assertFalse(self.data["four_dimensional_spacetime_derived"])
        self.assertFalse(self.data["mass_charge_or_gauge_dynamics_derived"])
        self.assertFalse(self.data["metric_dynamics_or_Einstein_equations_derived"])
        self.assertEqual(len(self.r),5)

if __name__=="__main__":
    unittest.main()
