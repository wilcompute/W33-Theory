"""Adversarial full-simplex 120-tick PHASE test at exact support-two
threshold, using active 40-outcome slices chosen across all 3 labels.

Numerical SLSQP feasible witnesses, NOT an interval global proof.
"""
import json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from w33_20261019_tick_operator_frame_majorization import build_projectors,points,symp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round12_global_phase_multistart.json"
rng=np.random.default_rng(120120)
P=build_projectors(points()).reshape(40,3,9,9)
pts=points()
A=np.array([[int(i!=j and symp(pts[i],pts[j])!=0) for j in range(40)] for i in range(40)],float)
def exactsingle(T):return -T*np.log(3+6*np.exp(-1/T))
def crit(T):
    y=np.exp(-1/T);return -1.5*(1-y)/(3+6*y)
def E_grad(w,ps,T,k):
    Q=np.einsum("p,pij->ij",w,ps)
    ev,U=np.linalg.eigh(Q)
    a=(ev-1)/T
    mx=a.max();z=np.exp(a-mx)
    F=-T*(mx+np.log(z.sum()))
    rho=(U*(z/z.sum())[None,:])@U.conj().T
    grads=-np.einsum("ij,pji->p",rho,ps).real
    aw=A@w
    C=2/3*(w@aw)
    g=grads+k*4/3*aw
    return float(F+k*C),g,float(F),float(C)
def run():
    entries=[]
    for T in (.2,.5,1.):
      for delta in (0.,.005):
        k=crit(T)+delta
        single=exactsingle(T)
        best={"E_gap":float("inf")}
        for trial in range(8):
            labels=rng.integers(0,3,size=40)
            ps=P[np.arange(40),labels]
            if trial==0:w0=np.eye(40)[0]
            elif trial==1:w0=np.ones(40)/40
            elif trial==2:w0=rng.dirichlet(np.full(40,.05))
            elif trial==3:w0=rng.dirichlet(np.full(40,2.))
            elif trial==4:w0=np.eye(40)[rng.integers(40)]*.9+np.ones(40)*(.1/40)
            else:w0=rng.dirichlet(np.full(40,.3))
            cache={}
            def f(w):
                key=w.tobytes()
                if cache.get("key")!=key:
                    e,g,F,C=E_grad(w,ps,T,k)
                    cache.update(key=key,e=e,g=g,F=F,C=C)
                return cache["e"]
            def jac(w):
                f(w)
                return cache["g"]
            op=minimize(f,w0,method="SLSQP",jac=jac,
               constraints=[{"type":"eq","fun":lambda w:sum(w)-1,"jac":lambda w:np.ones(40)}],
               bounds=[(0,1)]*40,
               options={"maxiter":250,"ftol":1e-12})
            feasible_w=np.maximum(op.x,0.0)
            feasible_w/=feasible_w.sum()
            ene,_,F,C=E_grad(feasible_w,ps,T,k)
            gap=ene-single
            if gap<best["E_gap"]:
                best={"E_gap":float(gap),"F":F,"C":C,"trial":trial,
                   "success":bool(op.success),"iterations":int(op.nit),
                   "labels":labels.tolist(),"weights":feasible_w.tolist(),
                   "sum_residual":float(abs(feasible_w.sum()-1)),
                   "min_weight":float(feasible_w.min()),
                   "support_gt1e_5":int(np.sum(feasible_w>1e-5))}
        entries.append({"T":T,"kappa":k,"offset_above_local":delta,"single_E":single,
            "best_feasible":best,"counterexample_below_single":bool(best["E_gap"]<-1e-7)})
    checks={"18_or_more_trial_minimizations":len(entries)==6,
        "all_feasible_weights":all(r["best_feasible"]["min_weight"]>=-1e-8 and r["best_feasible"]["sum_residual"]<1e-7 for r in entries),
        "all_finite_energies":all(np.isfinite(r["best_feasible"]["E_gap"]) for r in entries)}
    out={"schema":"w33.round12.full120_symmetry_slice_multistart_numerical.v1",
       "method":"Six (T,kappa) conditions, eight SLSQP feasible optimizations each, 40 active projective Pauli directions with independently randomized labels among three outcomes. These are embedded feasible 40-dimensional faces of the full 120-rate simplex. Jacobian uses rho=exp((Q-I)/T)/Tr and complement Pauli incidence C=(2/3)w^T A_noncomm w. A negative feasible E_gap is a numerical falsification candidate, NOT certified, requiring high-precision reevaluation. Nonnegative optimization minima do NOT prove global stability.",
       "cases":entries,"checks":checks,"all_checks_pass":all(checks.values()),
       "global_phase_boundary_proved":False}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"pass":out["all_checks_pass"],"cases":[(r["T"],r["offset_above_local"],r["best_feasible"]["E_gap"],r["best_feasible"]["support_gt1e_5"]) for r in entries]},indent=2))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":run()
