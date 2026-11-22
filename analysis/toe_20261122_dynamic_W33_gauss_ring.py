"""An exact 8D Gauss-constrained dynamical Z2 gauge loop inside W(3,3).

From a physical four-cycle (0,36,9,37), model one mobile matter quantum,
four quantum link variables, and one fixed odd background charge.
The 64D unconstrained 4x2**4 space becomes an eight-dimensional sector.
Electric-field dynamics changes flux and removes static AB cancellation.
It is NOT a 2+1D continuum gauge theory or measured quantum hardware.
"""
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261122_experiment_driven_five_fronts as prev
OUT=ROOT/"data/toe_20261122_dynamic_W33_gauss_ring.json"
EDGES=[(0,1),(1,2),(2,3),(3,0)]
LABELS=[0,36,9,37]
BACKGROUND=[1,0,0,0]

def gauss(m,bits,bg=BACKGROUND):
    x=[1-2*((bits>>e)&1) for e in range(4)]
    return tuple((-1)**(int(m==v)+bg[v])*
      math.prod(x[e] for e,(u,w) in enumerate(EDGES) if u==v or w==v)
      for v in range(4))

def build():
    graph=prev.W33()
    assert all(graph[LABELS[i],LABELS[(i+1)%4]]==1 for i in range(4))
    assert graph[LABELS[0],LABELS[2]]==0
    assert graph[LABELS[1],LABELS[3]]==0
    allstates=[(m,bits)for m in range(4)for bits in range(16)]
    assert all(math.prod(gauss(m,bits,[0]*4))==-1 for m,bits in allstates)
    states=[s for s in allstates if gauss(*s)==(1,1,1,1)]
    assert len(states)==8
    index={s:i for i,s in enumerate(states)}
    hop=np.zeros((8,8));electric=np.zeros((8,8));W=np.zeros((8,8))
    for i,(m,bits) in enumerate(states):
        electric[i,i]=-sum(1-2*((bits>>e)&1) for e in range(4))
        for e,(u,v) in enumerate(EDGES):
            if m in (u,v):
                newm=v if m==u else u
                newbits=bits^(1<<e)
                assert gauss(newm,newbits)==gauss(m,bits)
                hop[i,index[(newm,newbits)]]=-1
        assert gauss(m,bits^15)==gauss(m,bits)
        W[i,index[(m,bits^15)]]=1
    assert np.max(abs(hop-hop.T))<1e-12
    assert np.max(abs(W@W-np.eye(8)))<1e-12
    assert np.max(abs(W@hop-hop@W))<1e-12
    assert np.linalg.norm(W@electric-electric@W)>1
    return states,index,hop,electric,W

def observe(H,p,t,states,W):
    val,U=eigh(H)
    wave=U@(np.exp(-1j*val*t)*(U.conj().T@p))
    prob=float(sum(abs(wave[i])**2 for i,(m,_) in enumerate(states) if m==2))
    return prob,float(np.vdot(wave,W@wave).real)

def run():
    states,idx,hop,electric,W=build()
    sweep=[]
    for sign in (1,-1):
        p=np.zeros(8,complex)
        p[idx[(0,0)]]=1/math.sqrt(2)
        p[idx[(0,15)]]=sign/math.sqrt(2)
        assert np.max(abs(W@p-sign*p))<1e-12
        for h,B in ((0,0),(.3,0),(.3,.25),(1,0)):
            H=hop+h*electric-B*W
            for t in (.5,1,1.5,2,3):
                prob,wexp=observe(H,p,t,states,W)
                if h==0:
                    assert abs(prob-(math.sin(t)**4 if sign==1 else 0))<1e-11
                    assert abs(wexp-sign)<1e-11
                sweep.append({"initial_flux":sign,"electric_h":h,"plaquette_B":B,
                    "t":t,"opposite_vertex_probability":prob,
                    "Wilson_expectation":wexp})
    select=lambda sign,h,t:next(q for q in sweep if q["initial_flux"]==sign
                          and q["electric_h"]==h and q["plaquette_B"]==0 and q["t"]==t)
    negative_dynamic=select(-1,.3,1.5)
    assert abs(negative_dynamic["opposite_vertex_probability"]-.596141772894)<1e-9
    result={"status":"PASS","date":"2026-11-22","W33_cycle":LABELS,
      "total_unconstrained_dimension":64,"Gauss_positive_physical_dimension":8,
      "Gauss_definition":"G_v=(-1)^(matter_at_v+background_v) product X_incident",
      "odd_background_required":"On a closed loop, one matter quantum and all Gv=+1 require odd background charge",
      "Hamiltonian":"H=-sum_e(matter_hop_e Z_e + h.c.)-h sum_e X_e-B prod_e Z_e",
      "Gauss_constraints_preserved":True,"electric_field_does_not_commute_with_W":True,
      "static_flux_plus_arrival_probability":"sin(t)^4",
      "static_flux_minus_arrival_probability":0,
      "negative_flux_dynamic_t1p5_h0p3":negative_dynamic,
      "sweep":sweep,
      "boundary":"Exact finite Gauss-law Z2 quantum model on one W33 cycle. Not a real 2+1D gauge-theory experiment, local continuum, QCD or TOΕ."}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("PASS W33 dynamic gauge AB, 64 to 8 dimensions, flux negative no longer dark.")
    return result
if __name__=="__main__":run()
