"""Experimental finite-shot blueprint for Witting third-order spectral moments.

The 40-ray 3-design reproduces the third Haar moment; five ququart MUBs
are a genuine 2-design but not a 3-design. Collision tests use independent
identically prepared sources. No physical experiment or security guarantee.
"""
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np
from scipy.stats import binom
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261121_relational_reference_pareto as base
import toe_20261122_witting_3design_collision_moments as design
OUT=ROOT/"data/toe_20261122_witting_triple_collision_finite_shots.json"

def probs(x,rays):
    p=np.abs(rays.conj()@x)**2 * 4/len(rays)
    assert abs(p.sum()-1)<1e-10
    return p
def finite_test(p0,p1,alpha=2.866515718791933e-7,power=.9):
    assert p1>p0
    def eval(N):
        k=int(binom.isf(alpha,N,p0))+1
        return binom.sf(k-1,N,p1)>=power,k
    hi=1
    while not eval(hi)[0]:hi*=2
    lo=1
    while lo<hi:
        mid=(lo+hi)//2
        if eval(mid)[0]:hi=mid
        else:lo=mid+1
    _,critical=eval(lo)
    return {"iid_triplets_N":lo,"independent_photon_launches":3*lo,
      "critical_triple_label_matches":critical,
      "null_size":float(binom.sf(critical-1,lo,p0)),
      "alternative_power":float(binom.sf(critical-1,lo,p1))}
def main():
    wr,_,_,_=base.geometry()
    mub=design.get_MUB()
    states={"Witting_ray":wr[5],"fiveMUB_ray":mub[0],
            "nonstabilizer_pure":np.array([1,1,1,np.exp(1j*math.pi/5)])/2}
    rows=[]
    for name,x in states.items():
        pw=probs(x,wr);pm=probs(x,mub)
        c2w=float((pw**2).sum());c3w=float((pw**3).sum())
        assert abs(c2w-.04)<1e-12 and abs(c3w-.002)<1e-12
        rows.append({"input":name,"Witting40_pair_collision":c2w,
          "Witting40_triple_collision":c3w,
          "fiveMUB20_pair_collision":float((pm**2).sum()),
          "fiveMUB20_triple_collision":float((pm**3).sum())})
    assert abs(rows[0]["fiveMUB20_triple_collision"]-7/900)<1e-11
    assert abs(rows[1]["fiveMUB20_triple_collision"]-.01)<1e-11
    test=finite_test(rows[0]["fiveMUB20_triple_collision"],
                     rows[1]["fiveMUB20_triple_collision"])
    assert test["iid_triplets_N"]==68886
    # Explicit random mixed input moment reconstruction.
    rng=np.random.default_rng(20261122)
    Z=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4))
    rho=Z@Z.conj().T;rho/=np.trace(rho)
    P=np.einsum("ai,aj->aij",wr,wr.conj())
    pm=np.einsum("aij,ji->a",P,rho).real/10
    C2=float(sum(pm**2));C3=float(sum(pm**3))
    purity=float(np.trace(rho@rho).real);third=float(np.trace(rho@rho@rho).real)
    assert abs(C2-(1+purity)/50)<1e-12
    assert abs(C3-(1+3*purity+2*third)/3000)<1e-12
    N=450000
    sigma3=float(1500*math.sqrt(.002*(1-.002)/N))
    assert .099<sigma3<.101
    result={"status":"PASS","date":"2026-11-22",
        "pure_state_controls":rows,
        "fiveMUB20_distinguish_input_ray_5sigma_90percent_power":test,
        "mixed_input_purity":purity,"mixed_input_third_moment":third,
        "mixed_input_pair_collision_probability":C2,
        "mixed_input_triple_collision_probability":C3,
        "pure_ququart_Tr_rho3_one_sigma_from_450000_iid_triplets_if_purity_exact":sigma3,
        "operational_identity":"Tr(rho^2)=50 C2 -1; Tr(rho^3)=(3000 C3-1-3Tr(rho^2))/2",
        "boundary":"The known 3-design identity supplies these moments; 5-MUB is a 2-design control. Triplet sample count assumes iid independent states, stable alignment and no detector loss, source multiphoton errors or temporal drift."}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print("PASS Witting triple collision finite shots and MUB negative control")
    return result
if __name__=="__main__":main()
