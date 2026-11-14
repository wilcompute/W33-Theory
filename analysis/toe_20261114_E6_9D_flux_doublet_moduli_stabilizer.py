#!/usr/bin/env python3
"""Exact SL(2,Z)-covariant common-four flux toy potential.

In the 9D common M(T2) / IIB(S1) frame, a doublet of 3-form
fluxes F,H has four components each on the shared T4 directions.
The standard *three-form kinetic term at fixed base metric and
volume*, not the full ExFT scalar potential, is
    E(x+iy) = ||F-(x+iy)H||²/y, y>0.
D=||F||²||H||²-(F.H)² = sum_{i<j}(F_i H_j-F_j H_i)².
If D>0 then tau*=(F.H+i sqrt(D))/||H||², E_min=2sqrt(D).
If D=0 it has a runaway to the modular boundary, no finite min.
This constrains torus shape/axiodilaton *conditional on flux*, not
physical 5-vs-6 section selection; ignores Einstein/tadpole terms.

Under A in SL2Z, (F,H)->(aF+bH,cF+dH) and
tau->(a tau+b)/(c tau+d), E is exactly invariant.
"""
from pathlib import Path
from itertools import combinations,product
from fractions import Fraction
import json,sys,math
import sympy as sp
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261114_E6_9D_flux_doublet_moduli_stabilization.json"

def det_invariant(F,H):
    FF=sum(int(x)**2 for x in F)
    HH=sum(int(y)**2 for y in H)
    FH=sum(int(x)*int(y) for x,y in zip(F,H))
    D=FF*HH-FH*FH
    minors=sum((F[i]*H[j]-F[j]*H[i])**2 for i,j in combinations(range(len(F)),2))
    assert D==minors and D>=0
    return FF,HH,FH,D

def energy(F,H,x,y):
    assert y>0
    FF,HH,FH,_=det_invariant(F,H)
    return (FF-2*x*FH+x*x*HH)/y+y*HH

def main():
    i=sp.I
    rng=np.random.default_rng(20261114)
    SL=[sp.Matrix([[1,0],[0,1]]),
        sp.Matrix([[0,-1],[1,0]]),sp.Matrix([[1,1],[0,1]]),
        sp.Matrix([[1,1],[1,2]]),sp.Matrix([[2,1],[1,1]]),
        sp.Matrix([[-1,0],[0,-1]])]
    assert all(A.det()==1 for A in SL)
    checked=0
    ranks={0:0,1:0,2:0}
    minima=[]
    for _ in range(75):
        F=list(map(int,rng.integers(-3,4,4)))
        H=list(map(int,rng.integers(-3,4,4)))
        FF,HH,FH,D=det_invariant(F,H)
        rank=0 if not any(F+H) else (2 if D>0 else 1)
        ranks[rank]+=1
        assert rank in (0,1,2)
        x=sp.Rational(int(rng.integers(-4,5)),int(rng.integers(1,7)))
        y=sp.Rational(int(rng.integers(1,8)),int(rng.integers(1,6)))
        tau=x+i*y
        e0=energy(F,H,x,y)
        for A in SL:
            a,b,c,d=map(int,(A[0,0],A[0,1],A[1,0],A[1,1]))
            Fp=[a*f+b*h for f,h in zip(F,H)]
            Hp=[c*f+d*h for f,h in zip(F,H)]
            tp=(a*tau+b)/(c*tau+d)
            xp=sp.simplify(sp.re(sp.expand_complex(tp)))
            yp=sp.simplify(sp.im(sp.expand_complex(tp)))
            assert yp>0
            ep=energy(Fp,Hp,xp,yp)
            assert sp.simplify(e0-ep)==0,(F,H,A,e0,ep)
            assert det_invariant(Fp,Hp)[-1]==D
            checked+=1
        if D>0 and HH>0:
            xs=sp.Rational(FH,HH)
            ys=sp.sqrt(D)/HH
            minE=2*sp.sqrt(D)
            assert sp.simplify(energy(F,H,xs,ys)-minE)==0
            assert sp.simplify(sp.diff((FF-2*sp.Symbol("x")*FH+sp.Symbol("x")**2*HH)/sp.Symbol("y")+sp.Symbol("y")*HH,sp.Symbol("x")).subs({"x":xs,"y":ys}))==0
            if len(minima)<5:
                minima.append(dict(F=F,H=H,D=D,tau_star=str(xs+i*ys),
                                   energy_min=str(minE)))
    # Square and hexagonal torus examples. They arise from CHOSEN
    # integer fluxes, not from the cubic or from E6 alone.
    examples={}
    for label,F,H in [
        ("square",[1,0,0,0],[0,1,0,0]),
        ("hexagonal",[1,1,0,0],[0,1,1,0]),
        ("rank_one_runaway",[2,0,0,0],[1,0,0,0]),
        ("pure_F_runaway",[1,1,0,0],[0,0,0,0])]:
        FF,HH,FH,D=det_invariant(F,H)
        if D:
            xs=sp.Rational(FH,HH)
            ys=sp.sqrt(D)/HH
            assert sp.simplify(energy(F,H,xs,ys)-2*sp.sqrt(D))==0
            examples[label]=dict(F=F,H=H,rank=2,D=D,
               tau_star=str(xs+i*ys),energy_min=str(2*sp.sqrt(D)))
        else:
            # No stable finite shape for rank <2:
            # if H=0 take y -> infinity; if H !=0 and F proportional H,
            # choose x=FH/HH and y->0.
            examples[label]=dict(F=F,H=H,rank=0 if FF+HH==0 else 1,
                 D=0,has_finite_minimum=False,infimum_energy=0)
    assert examples["square"]["tau_star"]=="I"
    assert examples["hexagonal"]["tau_star"]=="1/2 + sqrt(3)*I/2"
    assert checked==75*len(SL)
    result=dict(status="PASS_EXACT_9D_M_IIB_FLUX_SHAPE_MINIMUM_SL2Z_DUALITY",
       common_four_3form_slots=4,flux_doublet_integer_components=8,
       flux_energy="E(tau) = ||F - tau H||² / Im(tau), at fixed base metric and volume",
       integer_discriminant="D=||F||² ||H||² - (F.H)²=sum_{i<j}(Fi Hj-Fj Hi)²",
       isolated_interior_shape_minimum_iff_flux_doublet_rank_two=True,
       zero_flux_has_flat_moduli_no_isolated_minimum=True,
       rank_two_tau_star="(F.H + i sqrt(D))/||H||²",
       rank_two_minimal_energy="2 sqrt(D)",
       normalized_shape_flux_Hessian_at_min="2 ||H||^4 / sqrt(D) times identity in (Re tau, Im tau) coordinates",
       rank_one_zero_energy_infimum_at_moduli_boundary=True,
       exact_SL2Z_duality_invariance_checks=checked,
       arbitrary_integer_flux_rank_census=ranks,
       square_hex_and_runaway_examples=examples,
       sample_rank_two_minima=minima,
       physical_interpretation="An actual kinetic term for an axiodilaton/torus shape doublet can conditionally stabilize shape while preserving M(T2)-IIB(S1) duality.",
       exclusions="NOT the full ExFT action or a validated compactification: fixes base metric and volume, ignores flux Bianchi/tadpoles, warping, sources, Einstein eqns and other moduli; does NOT select five vs six spacetime dimensions.",
       references=["https://academic.oup.com/ptep/article/2017/4/043B05/3605261",
                   "https://jaxvacua.readthedocs.io/en/latest/intro/sugra.html"])
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({k:result[k] for k in (
        "status","exact_SL2Z_duality_invariance_checks",
        "isolated_interior_shape_minimum_iff_flux_doublet_rank_two",
        "square_hex_and_runaway_examples")},indent=2),flush=True)
    return result
if __name__=="__main__":main()
