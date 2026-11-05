#!/usr/bin/env python3
"""Integrative TOE consistency check: gauged B-L plus vectorlike GUT matter.

One anomaly-free classical action can combine B-L seesaw and vectorlike
SU3xSU2xU1 Dirac quark, but its U1_Y x U1_(B-L) charge mixed trace
is NONZERO, so loop-generated kinetic mixing must be included. Earlier
diagonal-gauge 2loop fit and B-L seesaw CANNOT simply be pasted
together into a radiatively closed full action.
"""
from __future__ import annotations
import json,math,sys
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261105_anomalyfree_bl_seesaw_degeneracy import FIELDS,anomalies
OUT=ROOT/"data/toe_20261105_bl_sm_threshold_kinetic_mixing_no_go.json"
def trace(fs,func):
    return sum(n*func(y,x) for n,y,x in fs)
def wfields():
    return [(v["mult"],v["Y"],v["BL"]) for v in FIELDS.values()]
def extra_vectorlike_Q():
    # One LH (3,2)Q and its conjugate LH multiplet; mass allowed.
    return [(6,F(1,6),F(1,3)),(6,-F(1,6),-F(1,3))]
def checks():
    gen=wfields()
    vl=extra_vectorlike_Q()
    fermions=gen*3+vl
    scalars=[(2,F(1,2),F(0)),(1,F(0),F(-2))]
    zero_tests={
      "gravY":trace(fermions,lambda y,x:y),
      "gravBL":trace(fermions,lambda y,x:x),
      "Y3":trace(fermions,lambda y,x:y**3),
      "BL3":trace(fermions,lambda y,x:x**3),
      "Y2BL":trace(fermions,lambda y,x:y*y*x),
      "YBL2":trace(fermions,lambda y,x:y*x*x)}
    assert all(z==0 for z in zero_tests.values())
    assert all(z=="0" for z in anomalies().values())
    mixed_SM=trace(gen*3,lambda y,x:y*x)
    mixed_VL=trace(vl,lambda y,x:y*x)
    assert mixed_SM==F(8) and mixed_VL==F(2,3)
    bmix_sm=F(2,3)*mixed_SM
    bmix_vl=F(2,3)*(mixed_SM+mixed_VL)
    assert bmix_sm==F(16,3)
    assert bmix_vl==F(52,9)
    b_BL=F(2,3)*trace(fermions,lambda y,x:x*x)+F(1,3)*trace(scalars,lambda y,x:x*x)
    assert b_BL==F(116,9)
    # Leading log for fixed diagonal gY,gBL and chi(vBL)=0.
    scale=1e10
    unif=1.3163003690605982e15
    gY=math.sqrt(4*math.pi/127.955)/math.sqrt(1-.23122)
    gBL=.2
    delta=(gY*gBL/(16*math.pi**2))*float(bmix_vl)*math.log(unif/scale)
    assert .02<delta<.04
    return {"status":"PASS_U1_MIXED_TRACE_NONZERO",
       "model":"SM*3 + (Nc)*3 + S(BL=-2) + one vectorlike quark doublet (3,2,Y=1/6,BL=1/3)",
       "all_local_polynomial_U1_gauge_anomalies":{k:str(x) for k,x in zero_tests.items()},
       "trace_Y_BL_SM_three_families":str(mixed_SM),
       "trace_Y_BL_added_vectorlike_pair":str(mixed_VL),
       "mixed_beta_b_Y_BL_without_vectorlike":str(bmix_sm),
       "mixed_beta_b_Y_BL_with_vectorlike":str(bmix_vl),
       "one_loop_BL_diagonal_b_with_vectorlike_and_scalar":str(b_BL),
       "leading_log_boundary_zero_kinetic_mix_at_GeV":scale,
       "reference_energy_GeV":unif,
       "benchmark_fixed_gY":gY,"benchmark_fixed_gBL":gBL,
       "loop_generated_kinetic_mixing_estimate":delta,
       "nonzero_radiative_kinetic_mixing":True,
       "consequence":"Two-loop diagonal SM gauge RG plus separately anomaly-free gauged BL seesaw do not form a radiatively closed joint model: U1xU1 mixing and BL beta function must be included.",
       "boundary":"Leading-log illustrative bare chi convention, constant couplings, mass thresholds approximated. No full kinetic-mixing matrix RGE, no generated UV completion and no empirical Zprime prediction.",
       "prior_art":"One-loop U1xU1 kinetic mixing proportional to trace of product of charges is standard."}
def main():
    out=checks()
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("JOINT_ACTION_NO_GO_PASS",out["mixed_beta_b_Y_BL_with_vectorlike"],
       out["loop_generated_kinetic_mixing_estimate"],flush=True)
    print("CERTIFICATE",OUT,flush=True)
    return out
if __name__=="__main__":main()
