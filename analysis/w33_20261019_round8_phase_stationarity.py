"""Front2: first-order stationary tests of all five heptad spectral
representatives and feasible improved negative-kappa phase witnesses.
These are feasible witnesses, NOT a global continuous 40-rate proof.
"""
from __future__ import annotations
import json
import numpy as np
from pathlib import Path
from scipy.optimize import minimize
from w33_20261019_tick_operator_frame_majorization import points,build_projectors
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round8_phase_stationarity.json"
hept=json.loads((ROOT/"data/w33_20261019_round6_heptad_symmetry.json").read_text())["sample_heptad"]
families=json.loads((ROOT/"data/w33_20261019_round6_heptad_exact_charpoly.json").read_text())["families"]
P=build_projectors(points()).reshape(40,3,9,9)
I9=np.eye(9)
def terms(s,projectors,T,k):
    Q=np.einsum('i,ijk->jk',s,projectors)
    eig,U=np.linalg.eigh(Q)
    e=np.exp((eig-eig.max())/T)
    den=e.sum()
    rho=(U*e[np.newaxis,:])@U.conj().T/den
    F=1-eig.max()-T*np.log(den)
    C=2/3*(1-s@s) # all seven projective directions pairwise noncommuting
    gradients=np.array([-np.trace(rho@Pi).real-(4*k/3)*sj for sj,Pi in zip(s,projectors)])
    return float(F+k*C),float(F),float(C),gradients
def run():
    T=.5
    s0=np.ones(7)/7
    single=float(-T*np.log(3+6*np.exp(-1/T)))
    fam=[]
    for i,f in enumerate(families):
        projectors=np.array([P[p,k] for p,k in zip(hept,f["one_label"])])
        E,F,C,g=terms(s0,projectors,T,0)
        fam.append({"family":i,"counts":f["count"],"F_at_equal_weights":F,
            "analytic_7_mass_gradient_range":float(g.max()-g.min()),
            "analytic_gradient":g.tolist(),
            "equal_weights_stationary_inside_seven_simplex":bool(g.max()-g.min()<1e-11)})
    viable=[]
    for kappa in (-.36,-.358,-.357,-.35,-.34,-.3):
        solutions=[]
        for i,f in enumerate(families):
            qs=np.array([P[p,k] for p,k in zip(hept,f["one_label"])])
            f_and_jac=lambda s: (terms(s,qs,T,kappa)[0],terms(s,qs,T,kappa)[3])
            opt=minimize(f_and_jac,s0,method="SLSQP",jac=True,
              constraints=[{"type":"eq","fun":lambda s:s.sum()-1,
                "jac":lambda s:np.ones_like(s)}],
              bounds=[(0,1)]*7,options={"ftol":1e-13,"maxiter":400})
            E,F,C,g=terms(opt.x,qs,T,kappa)
            solutions.append((E,i,opt.x,F,C,bool(opt.success),float(abs(opt.x.sum()-1))))
        E,i,s,F,C,ok,res=min(solutions,key=lambda x:x[0])
        equal_F=min(fam,key=lambda x:x["F_at_equal_weights"])["F_at_equal_weights"]
        E_equal=equal_F+(4/7)*kappa
        viable.append({"kappa":kappa,"lowest_feasible_E":E,
           "family":i,"optimized_weights":s.tolist(),
           "Gibbs_F":F,"C":C,"optimizer_success":ok,
           "simplex_sum_residual":res,
           "singleton_E":single,"improvement_over_uniform_heptad":E_equal-E,
           "beats_single_tick":bool(E<single),"feasible_gap_below_singleton":E-single})
    checks={"all_five_gradient_computed":len(fam)==5,
        "nonstationary_heptad_family_exists":any(not q["equal_weights_stationary_inside_seven_simplex"] for q in fam),
        "all_feasible_simplexes_valid":all(r["simplex_sum_residual"]<1e-8 and min(r["optimized_weights"])>=-1e-9 for r in viable),
        "numerical_heptad_improves_equal_weight_trial":any(q["improvement_over_uniform_heptad"]>1e-6 for q in viable),
        "noncommuting_feasible_witness_below_known_bound":any(q["beats_single_tick"] and q["kappa"]<-.357884 for q in viable)}
    out={"schema":"w33.round8.heptad_continuous_mass_stationarity.v1",
       "method":"Strictly feasible 7-simplex states using exact 9x9 Pauli projectors. F_T=1-T log Tr exp(Q/T); dF/ds_i=-Tr[rho P_i]. For a 7-clique C=(2/3)(1-s·s), derivative d(kappa C)/ds_i=-(4/3)kappa s_i. At equal weights, interaction derivatives are identical, so equality of Gibbs gradients is NECESSARY for finite-kappa stationarity.",
       "temperature":T,"single_tick_F":single,
       "five_family_stationarity":fam,"seven_mass_SLSQP_witnesses":viable,
       "claim_boundary":"Feasible seven-support candidate energies refute singleton whenever below F_single. Optimizer output is numerical, not interval-certified or a global 40-point phase boundary; no conclusion about unique heptad phase at intermediate kappa.",
       "checks":{k:bool(v) for k,v in checks.items()},
       "all_checks_pass":bool(all(checks.values()))}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"checks":out["checks"],"stationary":[r["equal_weights_stationary_inside_seven_simplex"] for r in fam],"results":[[r["kappa"],r["feasible_gap_below_singleton"],r["improvement_over_uniform_heptad"]] for r in viable]},indent=2))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":run()
