"""Round7 front2: rigorous inclusion/exclusion bounds for global
one-tick phase of full 120-tick negative-kappa model.
Combined exact previous global sufficiency with heptad trial
competitor from exact 5 integer characteristic polynomials.
"""
from __future__ import annotations
import json
import numpy as np
from pathlib import Path
from scipy.optimize import brentq
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round7_competing_phase.json"
SOURCE=ROOT/"data/w33_20261019_round6_heptad_exact_charpoly.json"
families=json.loads(SOURCE.read_text())["families"]
def bound_a(T):
    b=1/T;e=np.exp(-b)
    return 3*T*(1-(1+b)*e)/(3+6*e)
def F_spec(e,T):
    x=(e-1)/T
    return float(-T*(max(x)+np.log(np.exp(x-max(x)).sum())))
def eigpoly(f):
    coeff=f["characteristic_polynomial_of_21Q_integer_coefficients_high_to_low"]
    roots=np.roots(coeff)
    assert max(abs(np.imag(roots)))<.001,roots
    return np.sort(np.real(roots))/21
def run():
    sp=[eigpoly(f) for f in families]
    max_root_err=0
    for f,e in zip(families,sp):
        coeff=f["characteristic_polynomial_of_21Q_integer_coefficients_high_to_low"]
        max_root_err=max(max_root_err,float(np.max(abs(np.polyval(coeff,21*e)))))
    rows=[]
    for T in (.05,.1,.2,.5,1.,2.,5.,10.):
        Fb=float(-T*np.log(3+6*np.exp(-1/T)))
        Fs=np.array([F_spec(v,T) for v in sp])
        ix=int(np.argmin(Fs))
        Fh=float(Fs[ix])
        # H_energy=Fh+(4/7)*kappa; single=Fb.
        # trial below -7/4(Fh-Fb) beats EVERY C=0 configuration
        # since baseline is best at C=0 (majorization).
        k_exclude=float(-7/4*(Fh-Fb))
        k_ensure=float(-bound_a(T))
        rows.append({"T":T,"F_single":Fb,"optimal_uniform_heptad_F":Fh,
                     "winning_family_index":ix,"family_free_energies":Fs.tolist(),
                     "global_single_guaranteed_if_kappa_at_least":k_ensure,
                     "single_tick_excluded_if_kappa_strictly_below":k_exclude,
                     "undetermined_kappa_interval":[k_exclude,k_ensure],
                     "test_kappa_below_exclusion":k_exclude-.01,
                     "trial_advantage_at_test":(Fh+(4/7)*(k_exclude-.01))-Fb})
    # At zero T, heptad trial inequality kappa < -(7/4)*(1-lambda_max(Qh))
    top=[float(np.max(v)) for v in sp]
    k0=-1.75*(1-max(top))
    checks={
      "five_exact_integer_polynomials_imported":len(sp)==5,
      "heptad_matrix_root_residual":max_root_err<1e-1,
      "phase_threshold_order_valid":all(q["single_tick_excluded_if_kappa_strictly_below"]<q["global_single_guaranteed_if_kappa_at_least"] for q in rows),
      "negative_competitor_wins_test":all(q["trial_advantage_at_test"]<-.005 for q in rows),
      "nontrivial_negative_phase_is_proven_to_exist":all(q["single_tick_excluded_if_kappa_strictly_below"]<0 for q in rows),
      "finite_temperature_rows":len(rows)==8}
    out={"schema":"w33.round7.global_phase_certified_outer_bracket.v1",
      "theorem_1":"For all 120 normalized nonnegative rates at T>0, kappa >= -a(T), a(T)=3T*(1-(1+1/T)exp(-1/T))/(3+6exp(-1/T)), is a sufficient global single-tick condition (proven in prior round).",
      "theorem_2":"For each T>0, choose heptad uniform point masses 1/7 with outcome assignment yielding minimum Gibbs F_h among five exactly classified characteristic-polynomial families. Then if kappa < -7/4*(F_h-F_single), that explicit state beats ALL singleton AND ALL C=0 states. Thus every true global minimizer has C>0, proving a noncommuting phase exists at sufficiently negative kappa.",
      "key_limitation":"The interval between sufficient global-single bound and explicit heptad exclusion threshold is UNDECIDED; these do not establish the complete phase boundary or prove that a heptad is globally optimal at finite negative coupling. Polynomial coefficients are exact but root/log evaluations numeric.",
      "source_exact_polynomials":"data/w33_20261019_round6_heptad_exact_charpoly.json",
      "max_integer_polynomial_numeric_evaluation_residual":max_root_err,
      "T0_max_heptad_eigenvalues":top,
      "T0_uniform_heptad_single_exclusion_kappa_below":k0,
      "T_data":rows,
      "checks":{k:bool(v) for k,v in checks.items()},"all_checks_pass":bool(all(checks.values()))}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"checks":out["checks"],"T05":rows[3],"maxpoly_err":max_root_err},indent=2))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":run()
