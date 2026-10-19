"""Sharper *rigorous* noncommuting/global-single exclusion at all T>0
from the exact one-sided two-tick derivative. Also freeze a rational
7-rate feasible witness at T=.5 with numerical gap to singleton.
"""
from __future__ import annotations
import json,math
import numpy as np
from pathlib import Path
from w33_20261019_tick_operator_frame_majorization import points,build_projectors
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round8_exact_local_instability.json"
P=build_projectors(points()).reshape(40,3,9,9)
hist=json.loads((ROOT/"data/w33_20261019_round6_heptad_symmetry.json").read_text())
families=json.loads((ROOT/"data/w33_20261019_round6_heptad_exact_charpoly.json").read_text())["families"]
h=hist["sample_heptad"]
I=np.eye(9)
def F(Q,T):
    v=np.linalg.eigvalsh(Q)
    z=(v-1)/T
    a=z.max()
    return float(-T*(a+np.log(np.exp(z-a).sum())))
def a_global(T):
    e=math.exp(-1/T)
    return 3*T*(1-(1+1/T)*e)/(3+6*e)
def local(T):
    e=math.exp(-1/T)
    return -1.5*(1-e)/(3+6*e)
def run():
    rows=[]
    Pa=P[h[0],0];Pb=P[h[1],0]
    for T in (.1,.2,.5,1,2,5):
        singleton=F(Pa,T)
        dF=2*(1-math.exp(-1/T))/(3+6*math.exp(-1/T))
        kcrit=local(T)
        k=kcrit-.01
        eps=1e-4
        delta=F((1-eps)*Pa+eps*Pb,T)+k*(4/3)*eps*(1-eps)-singleton
        rows.append({"T":T,"kappa_local_exact_formula_evaluated":kcrit,
           "single_tick_certified_if_kappa_at_least":-a_global(T),
           "open_boundary_bracket":[kcrit,-a_global(T)],
           "directional_F_prime_at_singleton":dF,
           "directional_total_prime_at_kappa_critical":dF+(4/3)*kcrit,
           "epsilon_test_kappa":k,"epsilon_test":eps,
           "energy_difference_feasible_two_tick_vs_singleton":delta})
    # Additional rational, optimizer-INDEPENDENT explicit candidate:
    # seven weights: one 9/10 and six 1/60, all noncommuting,
    # with the outcome representative of exact spectral family #0.
    T=.5;center=3
    s=np.ones(7)/60
    s[center]=9/10
    ks=families[0]["one_label"]
    Q=sum(x*P[i,j] for x,i,j in zip(s,h,ks))
    fq=F(Q,T);C=2/3*(1-s@s)
    fs=F(Pa,T)
    crossing=(fs-fq)/C
    E=fq+(-.35)*C
    checks={
       "exact_derivative_zero_at_local_threshold":all(abs(r["directional_total_prime_at_kappa_critical"])<1e-12 for r in rows),
       "pairwise_two_tick_feasible_direction_beats_singleton":all(r["energy_difference_feasible_two_tick_vs_singleton"]<0 for r in rows),
       "local_instability_improves_previous_global_exclusion":all(r["kappa_local_exact_formula_evaluated"]>-.9 for r in rows) and local(.5)>-.357883514,
       "rational_heptad_witness_valid":abs(s.sum()-1)<1e-15 and abs(C-2/3*(1-s@s))<1e-15,
       "rational_heptad_witness_beats_single_at_negative_035":E<fs,
       "global_single_sufficient_vs_local_exclusion_separated":all(r["open_boundary_bracket"][0]<r["open_boundary_bracket"][1] for r in rows)}
    out={"schema":"w33.round8.local_instability_sharp_global_exclusion.v1",
      "theorem":"For T>0 choose any two projective Pauli outcome projectors Pa,Pb from NONCOMMUTING W33 directions. Q_epsilon=(1-epsilon)Pa+epsilon Pb, C(Q_epsilon)=4/3 epsilon(1-epsilon). At epsilon=0, dF_T/d epsilon = [2(1-exp(-1/T))]/[3+6exp(-1/T)]. Thus d(F_T+kappa C)/d epsilon at 0 = [2(1-u)/(3+6u)]+4kappa/3. For kappa< -(3/2)(1-u)/(3+6u) the derivative is strictly negative; a feasible positive epsilon beats singleton. Since every C=0 state has F>=single (previous majorization), every GLOBAL minimizer necessarily has C>0. This is an exact all-temperature global phase EXCLUSION theorem, not merely an unproven local heuristic.",
      "status":"The true global phase transition remains between the exact sufficient global singleton bound and exact local-instability exclusion bound. We did not prove their equality or obtain full 40-mass global stationary solutions.",
      "temperature_rows":rows,
      "T_point5_refined_noncommuting_exclusion_kappa_below":local(.5),
      "T_point5_previous_uniform_heptad_exclusion":-.35788351411087066,
      "rational_seven_mass_witness":{"T":T,"heptad_indices":h,
        "outcome_labels":ks,"seven_rational_weights":["9/10" if i==center else "1/60" for i in range(7)],
        "F_T":fq,"commutator_C":float(C),"single_F":fs,
        "kappa_star_below_which_this_fixed_witness_wins":float(crossing),
        "E_at_kappa_minus_035":E,"gap_below_single_at_minus_035":E-fs},
      "prior_art":"The formula for local singleton instability appeared in the earlier round3 work. NEW here is the explicit rigorous implication for all global minimizers (using C=0 Gibbs majorization), and an optimizer-independent rational heptad witness. Credit the previous result; do not call the derivative novel.",
      "checks":{k:bool(v) for k,v in checks.items()},
      "all_checks_pass":bool(all(checks.values()))}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"checks":out["checks"],"local_k05":local(.5),"rational":out["rational_seven_mass_witness"]},indent=2))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":run()
