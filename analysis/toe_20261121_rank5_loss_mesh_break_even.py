"""Insertion-loss tradeoff for two exact ten-mode Witting decoders.

No lossless quantum hardware is claimed: an ideal Reck 10-mode decomposition
has 45 adjacent two-mode gates. This model adds uniform intensity attenuation
on each *active* pair after every gate; idle modes are not attenuated.
A lost photon is an unconditional decoder failure, not a successful output.

Run: python analysis/toe_20261121_rank5_loss_mesh_break_even.py
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np
from scipy.linalg import null_space
from scipy.optimize import brentq
sys.path.insert(0,str(Path(__file__).resolve().parent))
import toe_20261121_fivefront_rank5_optical_noise as new
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261121_rank5_loss_mesh_break_even.json"

def triangular_mesh(U):
    n=len(U)
    X=U.copy()
    gates=[]
    for col in range(n-1):
        for i in range(n-1,col,-1):
            a,b=X[i-1,col],X[i,col]
            scale=np.hypot(abs(a),abs(b))
            if scale<1e-13:continue
            c,s=np.conj(a)/scale,np.conj(b)/scale
            G=np.array([[c,s],[-np.conj(s),np.conj(c)]])
            X[[i-1,i]]=G@X[[i-1,i]]
            gates.append((i-1,i,G))
    phases=np.diag(X)
    assert np.max(abs(X-np.diag(phases)))<1e-11
    result=np.diag(phases)
    for i,j,G in reversed(gates):
        result[[i,j]]=G.conj().T@result[[i,j]]
    assert np.max(abs(result-U))<1e-10
    return gates,phases

def simulated_recovery(U,T,loss):
    gates,phases=triangular_mesh(U)
    W=np.diag(phases)[:,:9].copy()
    for i,j,G in reversed(gates):
        W[[i,j]]=np.sqrt(1-loss)*G.conj().T@W[[i,j]]
    R=W.reshape(5,2,9)
    L=np.array([r@T[:,j,:]for r in R for j in range(5)])
    e_f=float(sum(abs(np.trace(x))**2 for x in L)/4)
    e=sum(x.conj().T@x for x in L)
    avg=float(np.trace(e).real/2)
    ee=np.linalg.eigvalsh(e)
    assert ee.min()>=-1e-12 and ee.max()<=1+1e-9
    assert e_f<=avg+1e-9
    return {"loss_per_active_gate":loss,"mesh_gate_count":len(gates),
            "survival_average":avg,"survival_worst_logical":float(ee.min()),
            "unconditional_fidelity":e_f,
            "survival_normalized_entanglement_overlap":e_f/avg}

def main():
    rays,_,_,_=new.prior.geometry()
    d,Ropt,Rpetz,T,Uopt,V=new.optimize_decoder(rays)
    Wpetz=Rpetz.reshape(10,9)
    Upetz=np.column_stack((Wpetz,null_space(Wpetz.conj().T)))
    assert Upetz.shape==(10,10)
    Udict={"Petz":Upetz,"SDP_rank5":Uopt}
    result={}
    for name,U in Udict.items():
        result[name]=[simulated_recovery(U,T,loss)
                       for loss in (0,.001,.005,.01,.02)]
        assert result[name][0]["mesh_gate_count"]==45
    assert abs(result["Petz"][0]["unconditional_fidelity"]-d["petz_entanglement_fidelity"])<1e-9
    assert abs(result["SDP_rank5"][0]["unconditional_fidelity"]-d["rank5_CPTP_fidelity"])<1e-9
    def gap(loss):
        return simulated_recovery(Uopt,T,loss)["unconditional_fidelity"]-simulated_recovery(Upetz,T,loss)["unconditional_fidelity"]
    cross=float(brentq(gap,.01,.02,xtol=1e-13))
    assert .016<cross<.019
    assert result["Petz"][-1]["unconditional_fidelity"]>result["SDP_rank5"][-1]["unconditional_fidelity"]
    record={
       "status":"PASS","date":"2026-11-21",
       "loss_model":"Each active two-mode gate followed by uniform power attenuation on those two rails, no idle-mode loss or detector effects",
       "different_45_gate_mesh_loss_paths":True,
       "numerical_crossing_per_active_gate_intensity_loss":cross,
       "conditional_advantage_SDP_in_sampled_grid":all(
           s["survival_normalized_entanglement_overlap"]>
           p["survival_normalized_entanglement_overlap"]
           for s,p in zip(result["SDP_rank5"],result["Petz"])),
       "cases":result,
       "interpretation":"Architecture-specific insertion-loss crossover. Optimizing mesh layout/gauge can move the crossover; no universal 1.706% hardware threshold or measured chip."
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(record,indent=2,sort_keys=True)+"\n")
    print("PASS two decoder optical meshes; loss crossing",cross)
    return record
if __name__=="__main__":main()
