#!/usr/bin/env python3
"""Nonlinear 4D Euclidean Regge action on the boundary of the 5-simplex.

Twenty triangle hinges, fifteen edges and six 4-simplices triangulate S^4.
Checks the Schlaefli/Regge gradient identity, solves the symmetric
cosmological-term stationarity condition and computes its 15x15 Hessian.
This is established Regge calculus, not an emergent Lorentzian spacetime.
"""
from __future__ import annotations
from itertools import combinations
import json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_nonlinear_4d_regge_curved_hessian.json"
V=tuple(range(6))
EDGES=list(combinations(V,2))
TRI=list(combinations(V,3))
FOUR=list(combinations(V,5))

def simplex_geometry(vertices, lengths):
    vs=list(vertices)
    ds=np.zeros((5,5))
    for i,j in combinations(range(5),2):
        ds[i,j]=ds[j,i]=lengths[tuple(sorted((vs[i],vs[j])))]**2
    G=np.array([[(ds[0,i]+ds[0,j]-ds[i,j])/2
                for j in range(1,5)]for i in range(1,5)])
    sign,logdet=np.linalg.slogdet(G)
    assert sign>0
    volume=math.exp(logdet/2)/24
    CM=np.ones((6,6));CM[0,0]=0;CM[1:,1:]=ds
    Q=np.linalg.inv(CM)[1:,1:]
    dihed={}
    for i,j in combinations(range(5),2):
        cos=Q[i,j]/math.sqrt(Q[i,i]*Q[j,j])
        theta=math.acos(float(np.clip(cos,-1,1)))
        hinge=tuple(sorted(set(vs)-{vs[i],vs[j]}))
        dihed[hinge]=theta
    return volume,dihed

def evaluate(x):
    lengths=dict(zip(EDGES,x))
    deficit={f:2*math.pi for f in TRI};total_volume=0
    for four in FOUR:
        vol,angles=simplex_geometry(four,lengths)
        total_volume+=vol
        for t,theta in angles.items():deficit[t]-=theta
    areas=[]
    for i,j,k in TRI:
        a=lengths[(i,j)];b=lengths[(i,k)];c=lengths[(j,k)]
        semi=(a+b+c)/2
        assert semi>max(a,b,c)
        areas.append(math.sqrt(semi*(semi-a)*(semi-b)*(semi-c)))
    aa=np.array(areas)
    dd=np.array([deficit[t] for t in TRI])
    return float(aa@dd),float(total_volume),aa,dd

def main():
    x=np.ones(len(EDGES))
    S,V4,areas,deficits=evaluate(x)
    theta=math.acos(.25)
    expected_deficit=2*math.pi-3*theta
    assert abs(deficits[0]-expected_deficit)<1e-13
    assert np.max(abs(deficits-deficits[0]))<1e-13
    assert abs(V4-6*math.sqrt(5)/96)<1e-12
    Lambda=S/(4*V4)
    h=1e-5
    schlaefli=[]
    stationarity=[]
    for i,e in enumerate(EDGES):
        dx=np.eye(15)[i]*h
        Sp,Vp,_,_=evaluate(x+dx)
        Sm,Vm,_,_=evaluate(x-dx)
        dS=(Sp-Sm)/(2*h)
        predicted=expected_deficit*4*(math.sqrt(3)/6)
        assert abs(dS-predicted)<1e-7
        schlaefli.append(abs(dS-predicted))
        stationary=dS-2*Lambda*(Vp-Vm)/(2*h)
        stationarity.append(abs(stationary))
    assert max(stationarity)<2e-7
    def action(y):
        s,v,_,_=evaluate(y)
        return s-2*Lambda*v
    step=2e-4
    basis=np.eye(15)
    hessian=np.zeros((15,15))
    for i in range(15):
        for j in range(i,15):
            a=step*basis[i];b=step*basis[j]
            hessian[i,j]=hessian[j,i]=(
               action(x+a+b)-action(x+a-b)-action(x-a+b)+action(x-a-b)
            )/(4*step*step)
    vals=np.linalg.eigvalsh(hessian)
    assert vals[0]<-5 and np.all(vals[1:]>5)
    assert max(abs(vals[1:6]-np.mean(vals[1:6])))<1e-3
    assert max(abs(vals[6:]-np.mean(vals[6:])))<1e-3
    assert abs(np.mean(vals[1:6])-5.106393)<1e-2
    assert abs(np.mean(vals[6:])-13.00222)<1e-2
    # Constant edge-length scaling mode is the unique negative direction.
    uniform=np.ones(15)/math.sqrt(15)
    eval0=float(uniform@hessian@uniform)
    assert abs(eval0-vals[0])<1e-4
    result={
       "status":"PASS_CURVED_4D_REGGE_S4_SCHLAEFLI_HESSIAN_1_5_9",
       "triangulation":"boundary of six-vertex 5-simplex, topological 4-sphere",
       "edges":15,"triangle_hinges":20,"four_simplices":6,
       "unit_edge_triangle_area":math.sqrt(3)/4,
       "regular_simplex_interior_dihedral":theta,
       "regular_hinge_deficit":expected_deficit,
       "regge_action_S":S,"total_4_volume":V4,
       "symmetric_cosmological_lambda":Lambda,
       "max_schlaefli_gradient_mismatch":max(schlaefli),
       "max_full_action_gradient_at_stationarity":max(stationarity),
       "hessian_eigenvalues":vals.tolist(),
       "S6_edge_rep_irrep_multiplicities":[1,5,9],
       "negative_uniform_scale_mode":eval0,
       "hessian_min_abs_eigenvalue":float(min(abs(vals))),
       "nonzero_linearized_gauge_modes":0,
       "interpretation":"The curved, finite Euclidean Regge+volume stationary point has no exact edge-Hessian zero modes and one negative scale mode. The continuum four linearized gauge zero directions from the previously supplied flat-symbol calculation do not automatically survive this nonlinear curved triangulation.",
       "boundary":"No Lorentzian signature, continuum limit, discrete canonical constraint algebra, matter coupling, or derived Newton constant. The symmetry and Schlaefli identities are standard Regge-calculus mathematics."}
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS Regge 4D: Hessian sign (1 negative,14 positive), 1+5+9",float(vals[0]),float(vals[1]),float(vals[6]),flush=True)
    print("CERTIFICATE",OUT)
    return result
if __name__=="__main__":main()
