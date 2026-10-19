"""Follow-up frontiers 1+2: stable auxiliary-induced negative coupling and
rigorous global one-tick domain in the full 120-variable Gibbs simplex.
No claim that the auxiliary modes exist in nature. Run standalone.
"""
from __future__ import annotations
import json
import numpy as np
from pathlib import Path
from scipy.optimize import minimize
from scipy.linalg import eigh
from w33_20261019_tick_operator_frame_majorization import points, symp, build_projectors
from w33_20261019_tick_commutator_extremum import maximal_cliques

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"w33_20261019_nextfive_gaussian_phase.json"
pts=points()
P=build_projectors(pts)
I=np.eye(9)
B=np.array([[int(i!=j and symp(a,b)!=0) for j,b in enumerate(pts)] for i,a in enumerate(pts)],dtype=float)
edges=np.array([(i,j) for i in range(40) for j in range(i+1,40) if B[i,j]],dtype=int)
cl=maximal_cliques([sum(int(B[i,j])<<j for j in range(40)) for i in range(40)])
hept=next(c for c in cl if len(c)==7)
rng=np.random.default_rng(20261019)
assert len(edges)==540

def C(w):
    s=w.reshape(40,3).sum(axis=1)
    return float((2/3)*s@B@s)

def F(w,T):
    ev=eigh(I-np.tensordot(w,P,axes=1),eigvals_only=True)
    x=-ev/T
    u=x.max()
    return float(-T*(u+np.log(np.exp(x-u).sum())))

def gauss_model(w,g=1.,m=2.):
    """540 real stable oscillator modes, source proportional sqrt(s_p s_q).
    E_e = 0.5*m^2*x_e^2 - g sqrt(4/3)*sqrt(s_p s_q)*x_e.
    Eliminating x exactly produces -g^2/(2 m^2)*C(w).
    """
    s=w.reshape(40,3).sum(axis=1)
    j=np.sqrt(4/3)*np.sqrt(s[edges[:,0]]*s[edges[:,1]])
    xmin=(g/(m*m))*j
    min_energy=float(np.sum(.5*m*m*xmin*xmin-g*j*xmin))
    return {"auxiliary_modes":len(edges),"source_norm_squared":float(j@j),
        "integrated_energy":min_energy,
        "exact_target":-g*g/(2*m*m)*C(w),
        "kappa":-g*g/(2*m*m),
        "max_stationarity_residual":float(np.max(np.abs(m*m*xmin-g*j)))}

def safe_bound(T):
    """Exact full-simplex global lower bound on F-Fvertex >= a(T)*C."""
    beta=1/T
    em=np.exp(-beta)
    zmax=3+6*em
    # e^(beta*x) <= 1+(e^beta-1)*x -
    #    (e^beta-1-beta)*x*(1-x), via power series x-x^n>=x(1-x).
    # hence Zmax-Z >= (1-(1+beta)*exp(-beta))*(3-Tr Q^2).
    # And 3-Tr Q^2 >= 3*C(w) for all 120-coordinate w.
    return 3*T*(1-(1+beta)*em)/zmax

def local_threshold(T):
    em=np.exp(-1/T)
    return -1.5*(1-em)/(3+6*em)

def objective(w,T,k):
    H=I-np.tensordot(w,P,axes=1)
    ev,U=eigh(H)
    prob=np.exp(-(ev-ev.min())/T)
    prob/=prob.sum()
    rho=(U*prob)@U.conj().T
    val=float(ev.min()-T*np.log(np.exp(-(ev-ev.min())/T).sum()))
    gradF=-np.einsum("ij,pji->p",rho,P).real
    s=w.reshape(40,3).sum(axis=1)
    c=(2/3)*s@B@s
    gradC=np.repeat((4/3)*B@s,3)
    return float(val+k*c), gradF+k*gradC

def test():
    one=np.zeros(120);one[0]=1
    heptw=np.zeros(120)
    heptw[3*np.array(hept,dtype=int)]=1/7
    samples=[one,heptw,np.ones(120)/120]+[rng.dirichlet(np.ones(120)) for _ in range(30)]
    stable_checks=[gauss_model(w,g=.7,m=1.3) for w in samples]
    stable_error=max(abs(x["integrated_energy"]-x["exact_target"]) for x in stable_checks)
    records=[]
    for T in (.2,.5,1.,2.):
        b=safe_bound(T)
        gaps=[]
        for w in samples:
            gaps.append(F(w,T)-F(one,T)-b*C(w))
        records.append({"T":T,"global_singleton_sufficient_kappa_min":-b,
            "local_vertex_noncommuting_instability_kappa":local_threshold(T),
            "tested_min_bound_slack":min(gaps),
            "heptad_energy_above_single":F(heptw,T)-F(one,T),
            "heptad_C":C(heptw)})
    # Exact 120-dimensional variation with 4 starts, 3 temperatures/couplings
    num=[]
    for T,k in ((.5,-.6),(1.,-.3),(1.,-.15)):
        starts=[one,heptw,np.ones(120)/120,rng.dirichlet(np.ones(120))]
        solves=[]
        for start in starts:
            sol=minimize(objective,start,args=(T,k),jac=True,method="SLSQP",
                constraints=[{"type":"eq","fun":lambda w:np.sum(w)-1,
                    "jac":lambda w:np.ones_like(w)}],
                bounds=[(0,1)]*120,options={"maxiter":120,"ftol":1e-9})
            solves.append(sol)
        winner=min(solves,key=lambda v:v.fun)
        num.append({"T":T,"kappa":k,"best_energy":float(winner.fun),
          "support_gt_1e_3":int(np.sum(winner.x>1e-3)),
          "interaction":C(winner.x),
          "best_passed_solver":bool(winner.success),
          "all_solvers_converged":bool(all(v.success for v in solves)),
          "note":"restricted to four numerical starts but optimization spans all 120 tick coordinates"})
    checks={
      "540_genuine_noncommutation_edges":len(edges)==540,
      "stable_gaussian_exact_elimination":stable_error<1e-12,
      "nonnegative_mass_oscillators":all(x["max_stationarity_residual"]<1e-12 for x in stable_checks),
      "global_Gibbs_bound_full_120_coordinates":all(x["tested_min_bound_slack"]>=-1e-11 for x in records),
      "safe_domain_strictly_below_zero":all(x["global_singleton_sufficient_kappa_min"]<0 for x in records),
      "global_heptad_C_four_sevenths":abs(C(heptw)-4/7)<1e-12,
      "numeric_simplex_search_has_finite_objectives":all(np.isfinite(z["best_energy"]) for z in num)}
    out={"schema":"w33.nextfive.gaussian_phase.v1",
      "physical_model":"540 stable massive real auxiliary modes coupled linearly to sqrt(4/3)*sqrt(s_p*s_q) for W33 noncollinear p,q. Classical Gaussian functional integration/minimization exactly produces negative coupling. Auxiliary sector POSTULATED, not derived from photon or SM.",
      "auxiliary_energy":"sum_e [(m^2/2)x_e^2 - g sqrt(4/3)*sqrt(s_p*s_q)*x_e], m^2>0",
      "induced_kappa":"-g^2/(2m^2) <0",
      "canonical_Gaussian_derivation":"Complete squares in each stable x_e; finite-T partition integrates to w-independent determinant times exp(+beta*g^2*C/(2m^2))",
      "global_bound":"F_T(w)-F_T(one tick) >= a(T) C(w); a(T) = 3*T*[1-(1+1/T)*exp(-1/T)]/[3+6 exp(-1/T)], all 120 weights >=0 sum 1.",
      "proof_hint":"For eigenvalues 0<=q<=1, exp(beta q)<=1+(exp(beta)-1)q-[exp(beta)-1-beta]q(1-q); sum and use 3-Tr(Q^2)>=3*C and -log(1-x)>=x.",
      "exact_global_single_tick_certified_if":"kappa>=-a(T), including negative coupling above a temperature-specific boundary",
      "local_noncommutation_threshold":"kappa_local=-(3/2)*(1-exp(-1/T))/(3+6exp(-1/T))",
      "temperatures":records,"numerical_all_120_search":num,
      "Gaussian_max_abs_energy_residual":stable_error,
      "scope":"The global domain bound is rigorous but not sharp. Negative-kappa search is heuristic, not global certification. Source of auxiliary bosons is NOT physically established.",
      "checks":checks,"all_checks_pass":all(checks.values())}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"checks":checks,"temperatures":records,"numerics":num},indent=2))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":test()
