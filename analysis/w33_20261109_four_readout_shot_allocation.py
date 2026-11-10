#!/usr/bin/env python3
"""Oracle source-shot allocation optimization across W33 four readouts.

Minimizes h'F(w)^-1h with nonnegative per-context shot shares summing
to one for fixed known Horodecki a=.236, using ideal and one seeded
full noncommuting-loss POVM from prior code. Local A-optimal witness
criterion only, not robust unknown-state or finite-shot certificate.
"""
import json,sys,math
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from w33_20261109_four_architectures_full_loss_povm import all_physical,cz_factors
from w33_20261109_optical_fisher_competition import designs
from w33_20261109_q8_five_extensions import horodecki_state
from w33_20261109_q8_horodecki_ccnr_exact import realign

def components(Ks,rho,ops):
    Fs=[]
    for K in Ks:
        A=np.einsum("ji,kil,jl->jk",K,ops,K.conj()).real
        p=np.diag(K@rho@K.conj().T).real
        lost=float(max(0,1-sum(p)))
        if lost>1e-11:
            A=np.vstack([A,-A.sum(axis=0)])
            p=np.r_[p,lost]
        assert min(p)>1e-13
        Fs.append((A.T/p)@A)
    return np.array(Fs)

def solve_optimal(Fs,h,floor=.01):
    K=len(Fs);uniform=np.ones(K)/K
    def fun(w):
        F=np.einsum('i,ijk->jk',w,Fs)
        x=np.linalg.solve(F,h)
        return float(h@x),-np.array([x@Z@x for Z in Fs])
    res=minimize(fun,uniform,jac=True,method="SLSQP",
        bounds=[(floor,1)]*K,
        constraints=[{"type":"eq","fun":lambda w:float(sum(w)-1),
                      "jac":lambda w:np.ones(len(w))}],
        options={"maxiter":500,"ftol":1e-12})
    assert np.all(res.x>=floor-1e-8)
    assert abs(sum(res.x)-1)<1e-8
    baseline=fun(uniform)[0];optimal=fun(res.x)[0]
    assert optimal<=baseline+1e-7,(baseline,optimal)
    return {"uniform_per_launch_CCNR_CRLB":baseline,
        "optimized_per_launch_CCNR_CRLB":optimal,
        "fractional_variance_reduction":float(1-optimal/baseline),
        "shot_fractions_by_setting":[float(v) for v in res.x],
        "min_per_setting_shot_fraction":floor,
        "optimization_success":bool(res.success),
        "optimization_message":str(res.message)[:120],
        "iterations":int(res.nit)}

def main(path=None):
    designs_,ops=designs()
    fac=cz_factors()
    rho=horodecki_state(.236)
    R=realign(rho);u,_,vh=np.linalg.svd(R);W=u@vh
    h=np.array([float(np.vdot(W,realign(x)).real) for x in ops])
    outcases={}
    for scenario,t in {"ideal":(1.,1.,1.,0.),"moderate":(.995,.99,.999,.003)}.items():
        rng=np.random.default_rng(202611092221)
        K,_=all_physical(designs_,*t,rng,fac)
        outcases[scenario]={}
        for name,mat in K.items():
            Fs=components(mat,rho,ops)
            outcases[scenario][name]=solve_optimal(Fs,h,floor=.01)
    result={"status":"PASS_FOUR_OPTICAL_POVM_ORACLE_SOURCE_SHOT_ALLOCATION",
       "benchmark_state":"known Horodecki a=0.236 PPT entangled, CCNR fixed polar dual",
       "loss_scenarios":{
         "ideal":{"gate_intensity":1,"crossing_intensity":1,"mask_intensity":1,"phase_rms":0},
         "moderate":{"gate_intensity":.995,"crossing_intensity":.99,"mask_intensity":.999,"phase_rms":.003}},
       "per_launched_source_photon_optimization":outcases,
       "optimization_constraints":"All settings keep at least 1% of launched source photon budget (floor=.01 absolute). Total launched photons identical before and after allocation.",
       "model_limitations":"Oracle source state and its witness known in advance; optimization can bias adaptive state estimators and must use separate pilot data. Full fixed synthetic POVMs known exactly, real hardware losses, calibration uncertainty, crosstalk and clock overhead are not validated. CRLB is asymptotic and not a finite-shot statistical certificate. Optimizing variance for one chosen state is not universal tomography optimality.",
       "prior_art":"Classical optimal experimental design and convex inverse Fisher objectives are standard; W33 experimental geometry supplies the numeric matrices."}
    if path:Path(path).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("SHOT_ALLOC",json.dumps({scenario:{name:round(v["fractional_variance_reduction"],4)
         for name,v in case.items()} for scenario,case in outcases.items()}))
    return result
if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
