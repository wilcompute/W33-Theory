#!/usr/bin/env python3
"""Compile the exact 54D W33 reciprocal pulse into parallel real 3-mode interferometers.

Input: the certified plus factor 7 and minus factor 6 (Pass 11062).
Output: each 3-mode block's integer axis and a signed-permutation Givens schedule.
No physical hardware, fault threshold or phase calibration is claimed.
"""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import numpy as np
from analysis.w33_pass11062_single_foliation_finite54_transducer import factorize

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261031_54d_beamsplitter_compiler.json"

def canonical():
    c=2/math.sqrt(14);s=math.sqrt(10)/math.sqrt(14)
    d=3/math.sqrt(10);e=1/math.sqrt(10)
    R12=np.array([[c,-s,0],[s,c,0],[0,0,1]],float)
    R23=np.array([[1,0,0],[0,d,-e],[0,e,d]],float)
    V=R23@R12
    D=np.diag([1.,-1.,-1.])
    U=V@D@V.T
    v=np.array([2.,3.,1.])/math.sqrt(14)
    assert np.max(abs(V[:,0]-v))<1e-14
    assert np.max(abs(U-(2*np.outer(v,v)-np.eye(3))))<1e-14
    F=np.array([[0,1,-3],[-1,0,2],[3,-2,0]],np.int64)
    assert np.max(abs(U-(np.eye(3)+F@F/7)))<1e-14
    return U,{"theta_cos":"2/sqrt(14)","theta_sin":"sqrt(10)/sqrt(14)",
        "phi_cos":"3/sqrt(10)","phi_sin":"1/sqrt(10)",
        "chronological_layers":["BS23(-phi)","BS12(-theta)",
            "phase_pi_on_canonical_2_and_3","BS12(+theta)","BS23(+phi)"],
        "axis":"(2,3,1)/sqrt(14)","target":"2vv^T-I (pi rotation about v)"}

def blocks(which,ix,Ucanon):
    coords,pairs,factors=factorize(which)
    F=factors[ix].astype(np.int64)
    done=set(); schedule=[]; max_err=0.
    for x in range(81):
        if x in done:continue
        trio=sorted({x}|{j for j in range(81) if F[x,j]!=0})
        assert len(trio)==3 and not(done&set(trio))
        done.update(trio)
        f=F[np.ix_(trio,trio)]
        a,b,c=int(f[0,1]),int(f[0,2]),int(f[1,2])
        axis=np.array([c,-b,a],dtype=np.int64)
        assert sorted(abs(int(z)) for z in axis)==[1,2,3]
        assert np.array_equal(f@axis,np.zeros(3,dtype=np.int64))
        assert np.array_equal(f@f,np.outer(axis,axis)-14*np.eye(3,dtype=np.int64))
        U=np.eye(3)+f@f/7
        local_order=[int(np.where(abs(axis)==weight)[0][0]) for weight in (2,3,1)]
        signs=[1 if int(axis[k])>0 else -1 for k in local_order]
        S=np.zeros((3,3),dtype=np.int64)
        for j,k in enumerate(local_order):S[k,j]=signs[j]
        assert np.array_equal(S@S.T,np.eye(3,dtype=np.int64))
        computed=S@Ucanon@S.T
        err=float(np.max(abs(U-computed)))
        max_err=max(max_err,err)
        assert err<2e-14
        schedule.append({"modes":trio,"axis_integer":axis.tolist(),
            "canonical_to_local_order":local_order,"canonical_sign_gauge":signs,
            "compiled_max_abs_error":err})
    assert len(schedule)==27 and len(done)==81 and max_err<2e-14
    return {"factor":ix,"orientation":which,"mode_triangles":27,"schedule":schedule,
        "rank_of_exact_retyping":54,"max_abs_matrix_error":max_err}

def payload():
    U,rotations=canonical()
    return {"schema":"w33.20261031.54d_beamsplitter_compiler.v1",
      "status":"PASS",
      "plus":blocks("plus",7,U),"minus":blocks("minus",6,U),
      "canonical":rotations,
      "resource_upper_bound_per_triangle":{"real_two_mode_rotations":4,"parallel_phase_stage":1,
          "pi_phase_shifters":2,"additional_local_sign_gauges":"compiled into signed mode calibration",
          "parallel_triangles":27},
      "exact_ideal_relation":"U=2vv^T-I=I+F^2/7, v in ker F, F^3=-14F",
      "scientific_boundary":"An exact lossless real linear-optical unitary/circuit construction. Does not prove physical realization, phase fidelity, noise resilience, fault tolerance, a local Lorentzian continuum, or the direction of time.",
      "prior_art":"Pass 11062 perfect factors and October 1 cocycle blindness; present work supplies explicit real-symmetric pi pulse and two-Givens prepare/unprepare compiler."}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,default=OUT)
    a=p.parse_args()
    result=payload()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(json.dumps({"status":"PASS","modes":81,"blocks_each":27,
      "plus_max_error":result["plus"]["max_abs_matrix_error"],
      "minus_max_error":result["minus"]["max_abs_matrix_error"],
      "output":str(a.output)}))
if __name__=="__main__":
    main()
