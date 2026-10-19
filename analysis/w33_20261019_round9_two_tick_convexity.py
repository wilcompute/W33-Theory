"""Front2: exact analytical TWO-TICK phase threshold for all T>0,
via convexity of Pauli pair free energy in u=w(1-w).

Scope limited to support on two NONCOMMUTING Pauli directions;
does not prove full 120-rate global threshold.
"""
from __future__ import annotations
import math,json,itertools
from pathlib import Path
import numpy as np
from w33_20261019_tick_operator_frame_majorization import points,build_projectors,symp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round9_two_tick_convexity.json"
pts=points()
P=build_projectors(pts).reshape(40,3,9,9)
def free_pair(w,T):
    u=w*(1-w)
    r=math.sqrt(1-8*u/3)
    a=math.exp((1+r)/(2*T))
    b=math.exp((1-r)/(2*T))
    Z=3*(a+b+1)
    return 1-T*math.log(Z)
def threshold(T):
    v=math.exp(-1/T)
    return -1.5*(1-v)/(3+6*v)
def gprime_num(z,c):
    # minus the derivative numerator of g(z)=sinh(z)/[z(cosh(z)+c)]
    return math.sinh(z)*math.cosh(z)-z+c*(math.sinh(z)-z*math.cosh(z))
def run():
    count=0; maximal=0.
    for i,j in itertools.combinations(range(40),2):
        if symp(pts[i],pts[j])==0:continue
        for a,b in itertools.product(range(3),repeat=2):
            Pa,Pb=P[i,a],P[j,b]
            maximal=max(maximal,float(np.linalg.norm(Pa@Pb@Pa-Pa/3)))
            count+=1
    rows=[]
    for T in (.1,.2,.5,1,2,5):
        F0=free_pair(0,T)
        rat=[]
        for w in (.00001,.001,.01,.05,.1,.2,.3,.5):
            u=w*(1-w)
            C=4*u/3
            ratio=(free_pair(w,T)-F0)/C
            rat.append({"w":w,"ratio_Gibbs_cost_per_commutator":ratio})
        rows.append({"T":T,"two_tick_exact_critical_kappa":threshold(T),
                     "secant_ratios":rat,
                     "ratios_increase_with_u":bool(all(rat[i]["ratio_Gibbs_cost_per_commutator"]<=rat[i+1]["ratio_Gibbs_cost_per_commutator"]+1e-9 for i in range(7)))})
    # Proof: let u=w(1-w), a=8/3, x=sqrt(1-au), z=x/(2T),
    # B=e^(1/(2T)), c=1/(2B) in (0,1/2).
    # Z=3(1+2B cosh z), F'(u)=(a/(8T))*g(z), where
    # g(z)=sinh(z)/(z(cosh(z)+c)).
    # g'(z) numerator= z(1+c cosh z) -sinh z(cosh z+c)
    # = -[(1-c)(sinh z cosh z-z)+c(cosh z+1)(sinh z-z)] <=0.
    # z decreases in u, so F'(u) increases: F''(u)>=0.
    # Thus (F(u)-F(0))/u >=F'(0), and the exact singleton
    # boundary within all 2-tick supports is kappa_local(T).
    samples=[]
    for c in (0,.01,.1,.3,.5,1):
        for z in (.01,.1,1,3,8):
            samples.append(gprime_num(z,c))
    checks={"all_4860_noncommuting_Pauli_outcome_pairs_isoclinic":count==4860 and maximal<1e-11,
            "numerical_all_T_secant_ratios_monotone":all(r["ratios_increase_with_u"] for r in rows),
            "hyperbolic_monotonicity_numerator_positive":min(samples)>-1e-10,
            "two_tick_Tpoint5_boundary_matches_old_local":abs(threshold(.5)+.3402395316211989)<1e-13}
    out={"schema":"w33.round9.exact_2tick_free_energy_convexity.v1",
      "theorem":"For any TWO Pauli rank-three outcome projectors from distinct noncommuting W33 points, P Q P=(1/3)P, so Q_w=(1-w)P+wQ has eigenvalues lambda±=[1±sqrt(1-(8/3)w(1-w))]/2 each multiplicity3 and 0 multiplicity3. F_T(w)=1-T log[3+6 exp(1/(2T)) cosh(sqrt(1-(8/3)w(1-w))/(2T))]. As function u=w(1-w), F_T(u) is STRICTLY convex on [0,1/4] for T>0, hence secant >= F'_T(0), and singleton minimizes F_T+kappa(4/3)u among ALL two-tick mixtures iff kappa>=-3/2(1-exp(-1/T))/(3+6 exp(-1/T)). For kappa below threshold an infinitesimal two-tick mixture improves.",
      "analytic_convexity_proof":"Write a=8/3, x=sqrt(1-a u), z=x/(2T), c=(1/2)exp(-1/(2T)) in (0,1/2). Then F'_T(u)=(a/(8T))*g(z), g(z)=sinh(z)/[z(cosh(z)+c)]. Since z decreases as u increases, and -z²(cosh(z)+c)² g'(z)=(1-c)(sinh(z)cosh(z)-z)+c(cosh(z)+1)(sinh(z)-z)>=0, g'(z)<=0. Hence F''_T(u)>=0. The inequality uses only sinh(2z)>=2z and sinh(z)>=z for z>=0.",
      "noncommuting_pauli_outcome_pairs_tested":count,
      "PQP_equals_Pover3_max_frobenius_residual":maximal,
      "temperatures":rows,
      "scope":"This is an exact TWO-TICK result on all 4860 noncommuting tick pairs. It does not sharpen the certified global 120-variable sufficient bound; three-or-more-support states might intervene and must be checked.",
      "checks":{k:bool(v) for k,v in checks.items()},"all_checks_pass":bool(all(checks.values()))}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"checks":out["checks"],"maxres":maximal},indent=2))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":run()
