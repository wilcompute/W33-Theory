"""Round 4 frontiers 1+2: exact fermion-statistics sign reversal and
global 120-rate -> 40-rate + discrete three-outcome selection reduction.
All mathematical claims restricted to a specified nine-mode fermion model.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
from w33_20261019_tick_operator_frame_majorization import points,symp,build_projectors

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"w33_20261019_round4_fermions_global.json"
pts=points(); P=build_projectors(pts)
U=np.eye(9); A=P[0]
co=next(j for j in range(1,40) if symp(pts[0],pts[j])==0)
nc=next(j for j in range(1,40) if symp(pts[0],pts[j])!=0)
B=P[3*co]; C=P[3*nc]
rng=np.random.default_rng(20261019)
def spectra(x): return np.linalg.eigvalsh((A+x)/2)
specC=spectra(B);specN=spectra(C)
analyticC=np.array([0]*4+[.5]*4+[1])
r=1/np.sqrt(3)
analyticN=np.array([0]*3+[(1-r)/2]*3+[(1+r)/2]*3)
def omega(spec,T,mu):
    # 9 independent stable spinless fermionic one-particle modes,
    # energies epsilon_i=1-q_i; grand canonical free energy.
    return float(-T*np.logaddexp(0,(spec-1+mu)/T).sum())
def sign_delta(T,mu):return omega(specN,T,mu)-omega(specC,T,mu)
def analytic_stable(T):
    x=1/(4*T)
    f=lambda z:float(np.logaddexp(z,-z)-np.log(2))
    return -2*T*(3*f(x/np.sqrt(3))-f(x))
def bound(T):
    e=np.exp(-1/T)
    return 3*T*(1-(1+1/T)*e)/(3+6*e)
def free(w,T):
    ev=np.linalg.eigvalsh(np.eye(9)-np.tensordot(w,P,axes=1))
    z=-ev/T;return float(-T*(z.max()+np.log(np.exp(z-z.max()).sum())))
def interaction(w):
    s=w.reshape(40,3).sum(axis=1)
    return float((2/3)*sum(s[i]*s[j] for i in range(40) for j in range(40)
                   if i!=j and symp(pts[i],pts[j])!=0))
def lower_bound_checks():
    u=np.zeros(120);u[0]=1
    randoms=[rng.dirichlet(np.ones(120)) for _ in range(80)]
    rows=[]
    for T in (.15,.3,.5,1,2):
        a=bound(T);slacks=[free(w,T)-free(u,T)-a*interaction(w) for w in randoms]
        rows.append({"T":T,"a_T_exact_sufficient_positive":a,
            "tested_smallest_slack":min(slacks),"all_slacks_positive":bool(min(slacks)>-1e-10)})
    # Concavity in outcome redistribution for fixed direction weights:
    # choose p with s_p fixed, mix between outcomes k0 and k1.
    out=[]
    for _ in range(40):
        weights=rng.dirichlet(np.ones(40))
        p=int(rng.integers(40))
        j0=rng.integers(0,3,size=40)
        u=np.zeros(120)
        for j in range(40):u[3*j+j0[j]]=weights[j]
        v=u.copy()
        active=3*p+j0[p]
        other=3*p+((j0[p]+1)%3)
        v[other]=v[active];v[active]=0
        alpha=rng.uniform(.03,.97)
        mid=alpha*u+(1-alpha)*v
        T=float(rng.uniform(.15,1.5))
        gap=free(mid,T)-alpha*free(u,T)-(1-alpha)*free(v,T)
        out.append(gap)
        assert abs(interaction(u)-interaction(mid))<1e-12
    return {"global_bound_rows":rows,
      "conditional_p_vertex_strict_concavity_min_test_gap":min(out),
      "conditional_reduction":"At any fixed 40 point masses s_p, the Gibbs free energy is strictly concave along each nontrivial redistribution of the 3 projector outcomes. C depends only on s_p. Thus a global minimum of F_T+kappa*C may be chosen with at most 1 occupied outcome per point; at T>0 every global minimum has this property.",
      "reduced_global_search":"40 continuous nonnegative masses plus up to 3^40 discrete Pauli-outcome labels; k=0 for all 40 is NOT justified by this theorem."}
def run():
    assert np.max(abs(np.sort(specC)-analyticC))<1e-12
    assert np.max(abs(np.sort(specN)-analyticN))<1e-12
    half=[]
    for T in (.01,.05,.1,.2,.3,.5,1,2,5,10):
        observed=sign_delta(T,.5)
        expected=analytic_stable(T)
        densityC=float(np.sum(1/(1+np.exp(-(specC-.5)/T))))
        densityN=float(np.sum(1/(1+np.exp(-(specN-.5)/T))))
        exact_density=3+3/(1+np.exp(.5/T))
        half.append({"T":T,"mean_fermion_count_commuting":densityC,
                     "mean_fermion_count_noncommuting":densityN,
                     "mean_fermion_count_closed_form":exact_density,
                     "fermion_nonminus_comm_grand_potential":observed,
                     "exact_formula":expected,"residual":abs(observed-expected),
                     "ratio_to_high_T_leading":observed*(-2304*T**3)})
    # Preference reversals as chemical potential changes:
    bands=[]
    for T in (.08,.2,.5,1.):
        ms=np.linspace(-2,3,501)
        fs=np.array([sign_delta(T,m) for m in ms])
        roots=[]
        for i in range(len(ms)-1):
            if fs[i]*fs[i+1]<0:roots.append(float(brentq(lambda m:sign_delta(T,m),
                        ms[i],ms[i+1])))
        bands.append({"T":T,"roots_mu":roots,
            "mu05_negative":float(sign_delta(T,.5)),
            "mu_minus1_positive":float(sign_delta(T,-1)),
            "mu_2_positive":float(sign_delta(T,2))})
    red=lower_bound_checks()
    checks={
      "closed_form_pair_spectra":True,
      "mu_equal_density_negative_all_temperatures":all(x["fermion_nonminus_comm_grand_potential"]<0 for x in half),
      "mu_point_five_formula_numeric":all(x["residual"]<3e-11 for x in half),
      "both_competing_spectra_same_mean_occupancy":all(abs(x["mean_fermion_count_commuting"]-x["mean_fermion_count_noncommuting"])<1e-11 and abs(x["mean_fermion_count_commuting"]-x["mean_fermion_count_closed_form"])<1e-11 for x in half),
      "fermionic_reversal_far_from_half":all(x["mu_minus1_positive"]>0 and x["mu_2_positive"]>0 for x in bands),
      "global_stability_bound_random_checks":all(x["all_slacks_positive"] for x in red["global_bound_rows"]),
      "outcome_vertex_reduction":red["conditional_p_vertex_strict_concavity_min_test_gap"]>0}
    checks={k:bool(v) for k,v in checks.items()}
    result={"schema":"w33.round4.fermion_reversal_and_rate_reduction.v1",
      "model":"Nine free spinless fermion Fock modes with single-particle H=I-(P+Q)/2. Finite-dimensional stable Fock space. Chemical potential mu and identification with physical matter are supplied, not derived from W33.",
      "grand_potential":"Omega_f(T,mu;Q) = -T * Tr log(1+exp((Q-I+mu)/T))",
      "commuting_eigenvalues":"Qcomm spectrum: 1^1, (1/2)^4, 0^4",
      "noncommuting_eigenvalues":"Qnon spectrum: ((1+1/sqrt3)/2)^3, ((1-1/sqrt3)/2)^3, 0^3",
      "exact_mu_half_formula":"At the equal-density chemical potential mu=1/2 let x=1/(4T); Omega_non-Omega_comm= -2T [3 log cosh(x/sqrt(3)) - log cosh(x)] < 0 for every T>0. Mean particle number for BOTH competitors =3+3/(1+exp(1/(2T))), approaching 3 not 4.5 as T->0.",
      "proof_of_all_T_sign":"h(x)=log cosh(x)/x^2 decreases strictly on x>0 since derivative numerator x tanh(x)-2logcosh(x) has derivative x sech^2(x)-tanh(x)<0. Hence 3logcosh(x/sqrt3)>logcosh x.",
      "high_T_asymptotic":"Omega_non-Omega_comm= -1/(2304 T^3)+O(T^-5), mu=1/2",
      "zero_T_limit":"Omega_non-Omega_comm -> -(sqrt3-1)/2 (mu=1/2)",
      "physical_scope":"Fermionic occupation can reverse the pair preference without unstable bosons, but the chemical potential, fermionic bath and coupling H=I-Q are external assumptions. No constant universal negative kappa derived for arbitrary multi-tick states.",
      "mu_equal_density_samples":half,"chemical_potential_crossovers":bands,
      "full_120_dimensional_reduction":red,
      "checks":checks,"all_checks_pass":all(checks.values())}
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"checks":checks,"half_T0_2":half[3],"bands":bands,
          "global_reduction":red},indent=2))
    assert result["all_checks_pass"]
    return result
if __name__=="__main__":run()
