"""Finite-cone continuum bias and variance tradeoff for 4D BDG4 smearing.

Uses exact expected constant-field response by scalar quadrature (not fitted
to stochastic trials). Compares MSE for eps=1,.5,.2 and rho=100,200.
"""
from pathlib import Path
from math import pi,sqrt,log,exp
import json
from scipy.integrate import quad
ROOT=Path(__file__).resolve().parents[1]
IN=ROOT/"data/toe_20261119_BDG4_conditional_thinning_variance.json"
OUT=ROOT/"data/toe_20261119_BDG4_bias_variance_continuum_gate.json"

def expectation_constant(rho):
    kappa=pi/24
    zmax=rho*kappa
    def integrand(z):
        s=sqrt(z/(rho*kappa))
        if s<1e-15:g=1.
        elif s>=1:g=0.
        else:
            w=sqrt(1-s)
            g=w-s*log((1+w)/sqrt(s))
        P=1-9*z+8*z*z-4*z*z*z/3
        return exp(-z)*P*.5*g
    I=quad(integrand,0,zmax,weight="alg",wvar=(-.5,0),
           epsabs=1e-10,epsrel=1e-11,limit=600)[0]
    K=pi*sqrt(rho/kappa)*I
    return (4*sqrt(rho)/sqrt(6))*(K-1)

def run():
    previous=json.loads(IN.read_text(encoding="utf8"))
    rows=[]
    for r in previous["sample_results"]:
        expected=expectation_constant(r["effective_density"])
        se=r["smoothed_sd"]/sqrt(r["trials"])
        disagreement=abs(r["smoothed_mean"]-expected)
        # fixed deterministic Monte Carlo, sample means are noisy.
        assert disagreement<5*se+1e-9,(r,expected,se)
        mse=(r["smoothed_sd"]**2)+expected**2
        rows.append({"parent_rho":r["parent_sprinkling_density"],
                     "eps":r["retention_eps"],"effective_rho":r["effective_density"],
                     "analytic_continuum_Box_on_1":0,
                     "exact_finite_volume_mean_bias_from_quadrature":expected,
                     "MonteCarlo_mean":r["smoothed_mean"],
                     "MonteCarlo_mean_SE":se,
                     "absolute_mean_disagreement_in_SE":disagreement/se,
                     "observed_sample_variance":r["smoothed_sd"]**2,
                     "estimated_MSE_using_exact_bias_plus_sample_variance":mse})
    best={}
    for rho in (100.,200.):
        cohort=[r for r in rows if r["parent_rho"]==rho]
        b=min(cohort,key=lambda r:r["estimated_MSE_using_exact_bias_plus_sample_variance"])
        best[str(rho)]={"epsilon_best_of_tested_three":b["eps"],
                        "MSE_estimate":b["estimated_MSE_using_exact_bias_plus_sample_variance"],
                        "sharp_eps1_MSE_estimate":cohort[0]["estimated_MSE_using_exact_bias_plus_sample_variance"],
                        "MSE_ratio_best_over_sharp":b["estimated_MSE_using_exact_bias_plus_sample_variance"]/cohort[0]["estimated_MSE_using_exact_bias_plus_sample_variance"]}
    out={"rows":rows,"best_per_parent_density":best,
         "known_BDG4_mean_integral":"Exact 4D Minkowski future-cone integral 0<t<1, Poisson interval volume kappa*tau^4 (kappa=pi/24) with Poisson polynomial 1-9z+8z²-4z³/3, integrated with t/r radial Jacobian.",
         "limits":"MSE for constant field at origin in fixed finite domain, not generic smooth fields, curved spacetime, stable Lorentzian tensor operator, or physical quantum state. Estimated variance only 300 independent sprinklings, epsilon optimized among 3 fixed choices. Lower epsilon sacrifices locality and changes effective density."}
    OUT.write_text(json.dumps(out,indent=2)+"\n",encoding="utf8")
    for r in rows:print("BIAS",r["parent_rho"],r["eps"],round(r["exact_finite_volume_mean_bias_from_quadrature"],4),"SD MC",round(sqrt(r["observed_sample_variance"]),2),"z",round(r["absolute_mean_disagreement_in_SE"],2))
    for k,b in best.items():print("BEST",k,b)
    print(OUT)
    return out
if __name__=="__main__":run()
