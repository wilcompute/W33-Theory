"""Seeded constrained Witting detector design search over 24 resolved rays.

Simultaneously considers a 40-chart privacy MI target, 24D detector-drift
linear amplification, and ideal maximally-entangled fidelity-estimator
variance for the Moore-Penrose dual. A feasible constructive comparison,
not a global optimum or a proof of adversarial detector security.
"""
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261121_relational_reference_pareto as base
OUT=ROOT/"data/toe_20261122_witting_multicriteria_dualframe_search.json"
OLD=[31,7,21,28,22,30,3,15,4,23,26,25,8,1,32,20,19,29,14,38,16,39,11,37]
NEW=[0,1,2,9,6,8,14,11,12,13,15,16,19,21,23,18,27,28,30,32,34,35,37,39]

class Evaluator:
    def __init__(self):
        rays,H,A,P=base.geometry()
        I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1])
        B=np.array([np.kron(a,b)/2 for a in (I,X,Y,Z)for b in (I,X,Y,Z)])
        Pi=np.einsum("ai,aj->aij",rays,rays.conj())
        self.A=np.einsum("aij,kji->ak",Pi,B).real/10
        phi=np.eye(4).reshape(16)/2
        self.T=np.array([[np.vdot(phi,np.kron(a,b.conj())@phi).real
                         for b in B]for a in B])
        self.p40=abs(rays.conj()@rays.T)**2/400
        self.H=H
        _,U=np.linalg.eigh(P[2])
        self.D=H.T@U[:,-24:]/8
    def eval(self,labels):
        labels=np.asarray(labels,dtype=int)
        assert len(labels)==24 and len(set(labels))==24
        mask=np.ones(40,bool);mask[labels]=False
        A=np.vstack([self.A[labels],self.A[mask].sum(0)])
        sv=np.linalg.svd(A,compute_uv=False)
        if sv[-1]<1e-11:return None
        p=np.empty((25,25))
        p[:24,:24]=self.p40[np.ix_(labels,labels)]
        p[24,:24]=self.p40[np.ix_(np.flatnonzero(mask),labels)].sum(0)
        p[:24,24]=p[24,:24]
        p[24,24]=self.p40[np.ix_(mask,mask)].sum()
        Q=np.linalg.pinv(A)
        C=Q.T@self.T@Q
        mean=np.sum(C*p)
        var=np.sum(C*C*p)-mean*mean
        assert abs(mean-1)<1e-8 and var>=-1e-8
        rates=np.column_stack([self.H[:,labels],self.H[:,mask].sum(1)])/8
        marginal=rates.mean(0)
        nz=rates>0
        MI=float(np.sum(rates[nz]/45*np.log2(rates[nz]/np.broadcast_to(marginal,rates.shape)[nz])))
        gain=math.sqrt(24)/(40*np.linalg.svd(self.D[labels],compute_uv=False)[-1])
        return {"single_shot_fidelity_SD":float(math.sqrt(max(0,var))),
                "chart_leakage_MI_bits":MI,"worst_drift_gain_per_RMS":float(gain),
                "local_POVM_rank":int(np.sum(sv>1e-10))}

def obj(v):
    return (v["single_shot_fidelity_SD"]+.4*v["worst_drift_gain_per_RMS"]+
            .4*v["chart_leakage_MI_bits"]+
            20*max(0,v["worst_drift_gain_per_RMS"]-1.65)+
            20*max(0,v["chart_leakage_MI_bits"]-1.46))
def feasible(v):
    return v["worst_drift_gain_per_RMS"]<=1.65 and v["chart_leakage_MI_bits"]<=1.46

def main():
    model=Evaluator();rng=np.random.default_rng(444)
    initial=model.eval(NEW);old=model.eval(OLD)
    current=np.array(NEW);cm=initial
    best=current.copy();bm=initial;accepted=0
    for step in range(50000):
        cand=current.copy()
        count=1 if step%6==0 else (2 if step%6<=4 else 3)
        choices=rng.choice(24,size=count,replace=False)
        pool=np.setdiff1d(np.arange(40),cand)
        cand[choices]=rng.choice(pool,size=count,replace=False)
        value=model.eval(cand)
        if value is None:continue
        delta=obj(cm)-obj(value)
        if delta>=0 or rng.random()<math.exp(min(0,delta/.15)):
            current,cm=cand,value;accepted+=1
        if feasible(value) and obj(value)<obj(bm)-1e-12:
            best,bm=cand.copy(),value
    assert feasible(bm) and bm["local_POVM_rank"]==16
    assert bm["single_shot_fidelity_SD"] < initial["single_shot_fidelity_SD"]
    assert bm["chart_leakage_MI_bits"]<=1.46 and bm["worst_drift_gain_per_RMS"]<=1.65
    r={"status":"PASS","date":"2026-11-22","initial_new25":initial,"prior_old25":old,
       "best_seeded_candidate_labels_zero_based":best.tolist(),
       "best_seeded_candidate_metrics":bm,
       "candidate_attempts":50000,"accepted_moves":accepted,"seed":444,
       "objective":"min SD +.4 drift +.4 MI + hard-ish 20x penalties outside max drift 1.65 / chart MI 1.46",
       "privacy_cap_MI_bits":1.46,"drift_gain_cap":1.65,
       "compromise":"Variance reduced while keeping chart privacy near old/new levels, but worse robustness to unknown drift than new25.",
       "limits":"Constructive stochastic search, not a global optimum; one-shot ideal target-state Moore-Penrose fidelity variance, not weighted efficient estimator nor full detector hardware."}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
    print("PASS robust detector search",bm)
    return r
if __name__=="__main__":main()
