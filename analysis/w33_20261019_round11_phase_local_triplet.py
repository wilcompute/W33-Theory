"""Adversarial three-tick near-singleton census AT exact two-tick threshold.
Unlike prior random sampling, hold a singleton and scan all two
extra projectors across multiple epsilons. A numerical falsification,
not interval/SDP certificate or global 120-variable theorem.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
from w33_20261019_tick_operator_frame_majorization import points,build_projectors,symp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round11_phase_local_triplet.json"
pts=points();P=build_projectors(pts)
def free(Q,T):
    eig=np.linalg.eigvalsh(Q).real
    z=(eig-1)/T
    mx=z.max(axis=-1,keepdims=True)
    return (-T*(mx[:,0]+np.log(np.exp(z-mx).sum(axis=1)))) if z.ndim==2 else -T*np.log(np.exp(z).sum())
def run():
    T=.5;v=np.exp(-1/T)
    kc=-1.5*(1-v)/(3+6*v)
    F0=-T*np.log(3+6*v)
    Cmat=np.array([[int(i//3!=j//3 and symp(pts[i//3],pts[j//3])!=0)
           for j in range(120)] for i in range(120)],dtype=float)
    others=np.arange(1,120)
    ab=np.array(list(itertools.combinations(others,2)),dtype=int)
    wdict={}
    for t in (.25,.5,.75):
      for eps in (.01,.025,.05,.10,.20):
        wa,wb=eps*t,eps*(1-t);w0=1-eps
        Q=w0*P[0]+wa*P[ab[:,0]]+wb*P[ab[:,1]]
        C=4/3*(w0*wa*Cmat[0,ab[:,0]]+w0*wb*Cmat[0,ab[:,1]]+wa*wb*Cmat[ab[:,0],ab[:,1]])
        gaps=free(Q,T)+kc*C-F0
        arg=int(np.argmin(gaps))
        wdict[f"t={t},epsilon={eps}"]={"gap":float(gaps[arg]),
             "indices":[0,int(ab[arg,0]),int(ab[arg,1])],
             "weights":[float(w0),float(wa),float(wb)],
             "C":float(C[arg]),"candidate_count":len(ab)}
    best=min(wdict.values(),key=lambda z:z["gap"])
    check={"all_explicit_triple_weights_positive":min(best["weights"])>0,
      "full_119_choose2_scan_each_trial":all(x["candidate_count"]==7021 for x in wdict.values()),
      "all_tests_have_real_finite_free_energy":all(np.isfinite(x["gap"]) for x in wdict.values()),
      "fifteen_parameter_slices":len(wdict)==15}
    out={"schema":"w33.round11.triple_near_singleton_explicit_sweep.v1",
      "T":T,"exact_two_tick_threshold_evaluated":float(kc),
      "slices":wdict,"best":best,
      "adversarial_counterexample_at_two_tick_kcrit":bool(best["gap"]<-1e-7),
      "interpretation":"A gap<-1e-7 at kappa=kappa_2 is a feasible 3-tick numerical counterexample to extrapolating the support-two stability boundary to all 120 rates. If gap nonnegative, this scan still cannot prove the global theorem. Numerical 9x9 Hermitian eigensolver, NOT certified interval bounds.",
      "checks":check,"all_checks_pass":bool(all(check.values()))}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"pass":out["all_checks_pass"],"best":best,"counterexample":out["adversarial_counterexample_at_two_tick_kcrit"]},indent=2))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":run()
