#!/usr/bin/env python3
"""Exact Helstrom optical readout and robust measurement control for 54D W33 triangles.

Classical injections, real 3-mode interferometric eigenbasis, IID controls.
No lab data or intrinsic CPT/chirality claim.
"""
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261031_helstrom_optical_braid_readout.json"

def angle_rotation(i,j,t,n=3):
    m=np.eye(n);c=math.cos(t);s=math.sin(t)
    m[i,i]=m[j,j]=c;m[i,j]=-s;m[j,i]=s
    return m

def givens_decomposition(Q):
    work=Q.copy();left=[]
    for i,j in ((0,1),(0,2),(1,2)):
        a,b=work[i,i],work[j,i]
        angle=math.atan2(float(b),float(a))
        G=angle_rotation(i,j,-angle)
        work=G@work;left.append((i,j,angle))
    assert np.max(abs(work-np.diag(np.diag(work))))<1e-12
    reconstruction=np.eye(3)
    for i,j,angle in left:
        reconstruction=reconstruction@angle_rotation(i,j,angle)
    reconstruction=reconstruction@np.diag(np.diag(work))
    assert np.max(abs(reconstruction-Q))<1e-12
    return left,work,reconstruction

def counts(pe,n):
    wrong=sum(math.comb(n,k)*pe**k*(1-pe)**(n-k)
             for k in range(n//2+1,n+1))
    if n%2==0:wrong+=.5*math.comb(n,n//2)*pe**(n//2)*(1-pe)**(n//2)
    return wrong

def build():
    F=np.array([[0,1,-3],[-1,0,2],[3,-2,0]],float)
    I=np.eye(3);v=(I+F@F/14+F/math.sqrt(14))[:,0]
    w=(I+F@F/14-F/math.sqrt(14))[:,0]
    assert max(abs(np.linalg.norm(v)-1),abs(np.linalg.norm(w)-1))<1e-14
    ov=float(v@w);d=math.sqrt(1-ov*ov)
    assert abs(ov+3/7)<1e-14 and abs(d-2*math.sqrt(10)/7)<1e-14
    Delta=np.outer(v,v)-np.outer(w,w)
    eig,vec=np.linalg.eigh(Delta)
    assert np.max(abs(eig-[-d,0,d]))<1e-13
    # Plus, minus, null outcome rows; real orthogonal mixing!
    Q=np.stack([vec[:,2],vec[:,0],vec[:,1]])
    assert abs(abs(np.linalg.det(Q))-1)<1e-13
    pplus=abs(Q@v)**2;pminus=abs(Q@w)**2
    assert pplus[0]>.9 and pminus[1]>.9
    one=.5*(pplus[1]+pminus[0])+.25*(pplus[2]+pminus[2])
    assert abs(one-(1-d)/2)<1e-13
    steps,diag,rebuild=givens_decomposition(Q)
    basetv=.5*sum(abs(abs(v)**2-abs(w)**2))
    assert abs(basetv-12/(7*math.sqrt(14)))<1e-13
    # Collective optimal Helstrom, versus independent shots followed by
    # majority-vote classical postprocessing. These differ operationally.
    probes={}
    for target in (.001,.000001):
        ncol=next(n for n in range(1,50)
                  if .5*(1-math.sqrt(1-(ov*ov)**n))<target)
        nmaj=next(n for n in range(1,100) if counts(one,n)<target)
        probes[str(target)]={"collective_ideal_copies":ncol,
                            "local_interferometer_IID_shots":nmaj,
                            "collective_error":.5*(1-math.sqrt(1-(ov*ov)**ncol)),
                            "local_error":counts(one,nmaj)}
    assert probes["0.001"]["collective_ideal_copies"]==4
    assert probes["0.001"]["local_interferometer_IID_shots"]==7
    assert probes["1e-06"]["collective_ideal_copies"]==8
    assert probes["1e-06"]["local_interferometer_IID_shots"]==13
    # Miscalibration of the analyzer (same fixed orientation for both).
    drift=[]
    for t in (0,.01,.03,.10):
        M=angle_rotation(0,2,t)@angle_rotation(1,2,-t)@Q
        pa=abs(M@v)**2;pb=abs(M@w)**2
        error=.5*(pa[1]+pb[0])+.25*(pa[2]+pb[2])
        drift.append({"drift_radians":t,"one_shot_error":float(error)})
    assert abs(drift[0]["one_shot_error"]-one)<1e-13
    return {"status":"PASS_REAL_THREE_MODE_HELSTROM_AND_BRAID_GATE_SENSING",
        "source_pair_overlap":"-3/7","trace_distance":"2sqrt(10)/7",
        "baseline_fixed_port_TV":basetv,
        "real_mode_analyzer":Q.tolist(),
        "analyzer_two_mode_Givens_angles":[{"ports":[i,j],"radians":angle}for i,j,angle in steps],
        "diagonal_phase_signs":[float(x) for x in np.diag(diag)],
        "one_photon_Helstrom_optimal_error":one,
        "one_photon_fixed_port_error":(1-basetv)/2,
        "per_orientation_analyzer_click_probabilities":{"plus":pplus.tolist(),"minus":pminus.tolist()},
        "IID_local_vs_collective_test":probes,"analyzer_drift_control":drift,
        "scope":"Ideal state discrimination; loss and crosstalk must be separately modeled. Collective Helstrom test requires entangled joint measurements across multiple photons; local IID majority can be implemented by repeated single-photon three-mode detectors. Neither is a physical CP/time-arrow test."}

if __name__=="__main__":
    d=build();OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":d["status"],"one_error":d["one_photon_Helstrom_optimal_error"],
       "thresholds":d["IID_local_vs_collective_test"]},sort_keys=True))
