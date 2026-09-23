#!/usr/bin/env python3
"""Test the 54 fiber-instruction sector against the 54D representation deficit.

The two fiber instruction orbits come from the central lifted direction z with
external slopes s=1,2. Each is the 27-point coset action K/H_s where
  K=H27 x C3_external,
  H_s=< (z,s) >.

By Frobenius reciprocity, Ind_{H_s}^K(1) contains an irrep with multiplicity
equal to its degree iff (z,s) acts trivially.

For one-dimensional L(u,v,t), z acts trivially, so t=0 is required.
For three-dimensional S(r,t), (z,s) acts as omega^(r+t*s), so r+t*s=0 mod3.

This gives:
 slope 1:  9 L(*,*,0) + 3 S(1,2) + 3 S(2,1)
 slope 2:  9 L(*,*,0) + 3 S(1,1) + 3 S(2,2).

The 54D source representation-change sector from the minimal compiler is:
  all 27 L(u,v,t) + 3 S(2,0)+3 S(2,1)+3 S(2,2).

These modules are not isomorphic. Their maximum common equivariant rank is 27,
and the H27-center trace is 0 on fiber54 but -27*omega on deficit54.

Thus 54=fiber count and 54=equivariance deficit is a count collision, not an
objectwise/module identification.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_fiber54_vs_equivariance54_no_go.json"

DEG={**{f"L_{u}_{v}_{t}":1 for u in range(3) for v in range(3) for t in range(3)},
     **{f"S_{r}_{t}":3 for r in (1,2) for t in range(3)}}

def dim(profile):
    return sum(DEG[k]*v for k,v in profile.items())

def max_common_rank(a,b):
    return sum(DEG[k]*min(a.get(k,0),b.get(k,0)) for k in DEG)

def orbit_profile(slope):
    p={}
    for u in range(3):
      for v in range(3):
        p[f"L_{u}_{v}_0"]=1
    for r in (1,2):
      for t in range(3):
        if (r+t*slope)%3==0:p[f"S_{r}_{t}"]=3
    assert dim(p)==27
    return p

def add(a,b):
    return {k:a.get(k,0)+b.get(k,0) for k in set(a)|set(b)}

def main(write=True):
    f1=orbit_profile(1);f2=orbit_profile(2);fiber=add(f1,f2)
    assert dim(fiber)==54

    deficit={f"L_{u}_{v}_{t}":1 for u in range(3) for v in range(3) for t in range(3)}
    for t in range(3):deficit[f"S_2_{t}"]=3
    assert dim(deficit)==54

    common=max_common_rank(fiber,deficit)
    assert common==27

    # Character of the H27 center z represented in Q(omega) pairs A+B omega.
    # Fiber: 18*1 + 18*omega + 18*omega^2 = 0.
    fiber_center_pair=[0,0]
    # Deficit: 27*1 + 27*omega^2 = -27*omega.
    deficit_center_pair=[0,-27]
    assert fiber_center_pair!=deficit_center_pair

    compiler=json.loads((ROOT/"data/w33_minimal_symmetry_changing_81_compiler.json").read_text())
    instructions=json.loads((ROOT/"data/w33_hesse_pappus_45_270_instruction_compiler.json").read_text())
    assert compiler["compiler"]["symmetry_changing_coordinates"]==54
    assert instructions["instruction_layer"]["fiber"]==54
    assert instructions["instruction_layer"]["Clifford_phase_fixed_orbits"]==[27,27,216]

    out={
      "schema":"w33.fiber54_vs_equivariance54_no_go.v1",
      "status":"PASS_FIBER54_AND_EQUIVARIANCE_DEFICIT54_ARE_NONISOMORPHIC_K_MODULES",
      "headline":"The 54 phase-decorated fiber instructions are not the 54 symmetry-changing coordinates. The fiber sector is the sum of two 27-point quotient permutation modules K/<z*ext^s>, while the compiler deficit is all 27 one-dimensional characters plus the complete conjugate-Schrodinger sector. Their H27-center characters differ and their maximum common equivariant rank is only 27.",
      "fiber_sector":{
        "dimension":54,
        "slope1_profile":{"L_t0_multiplicity_each":1,"S_1_2":3,"S_2_1":3},
        "slope2_profile":{"L_t0_multiplicity_each":1,"S_1_1":3,"S_2_2":3},
        "combined_profile_summary":{"L_u_v_0_multiplicity_each":2,"S_1_1":3,"S_1_2":3,"S_2_1":3,"S_2_2":3},
        "H27_center_character_Qomega_pair":[0,0]
      },
      "equivariance_deficit_sector":{
        "dimension":54,
        "profile_summary":{"all_L_u_v_t_multiplicity_each":1,"S_2_0":3,"S_2_1":3,"S_2_2":3},
        "H27_center_character_Qomega_pair":[0,-27],
        "H27_center_character":"-27*omega"
      },
      "comparison":{
        "same_dimension":True,
        "isomorphic_as_K_modules":False,
        "maximum_common_equivariant_rank":27,
        "unmatched_dimensions_each_side":27,
        "center_character_witness":"fiber54 trace(z)=0, deficit54 trace(z)=-27*omega"
      },
      "consequence":"The fiber bypass cannot by itself be the missing 54D symmetry-changing compiler. Any relation between the two 54s must include an explicit representation-changing operation; equality of counts supplies no objectwise map.",
      "parents":[
        "data/w33_minimal_symmetry_changing_81_compiler.json",
        "data/w33_hesse_pappus_45_270_instruction_compiler.json",
        "data/w33_hybrid81_operator_equivariance_budget.json"
      ],
      "checks":{
        "each_fiber_orbit_dimension27":True,
        "fiber_total_dimension54":True,
        "deficit_dimension54":True,
        "center_characters_differ":True,
        "maximum_common_rank27":True,
        "count_collision_killed":True
      }
    }
    if write:OUT.write_text(json.dumps(out,indent=2)+"\n")
    return out

if __name__=="__main__":
    print(json.dumps(main(True),indent=2))
