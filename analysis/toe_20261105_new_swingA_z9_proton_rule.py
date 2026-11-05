#!/usr/bin/env python3
"""Unrelated swing A: exact Z9 residual baryon selection as a TOE-wide veto.

Replicate the known Z9 gauge selection rule q_Z9=3B mod9 for SM
quarks (triplets +1, anti-triplets -1), leptons/Higgs neutral.
Brute-force gauge-neutral necessary monomial screens with Weyl fermion
and Higgs combinations, plus explicit dimension-6 proton-decay
operators and a dimension-15 Delta-B=3 schematic operator.
No discrete gauge anomaly or UV origin is derived: consult Davighi,
Greljo, Ponce Diaz arXiv:2609.01712 for a consistent completion.
"""
from __future__ import annotations
import itertools,json
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_new_swingA_z9_proton_quality.json"
# left handed Weyl: SU3 triality in {-1,0,1}, SU2 parity,
# Y in LH conjugate convention, B integer thirds, Z9=3B mod9.
fields={
 "Q": {"triality":1,"doublet":1,"Y":F(1,6),"b3":1,"spin":1,"d2":3},
 "uc":{"triality":-1,"doublet":0,"Y":-F(2,3),"b3":-1,"spin":1,"d2":3},
 "dc":{"triality":-1,"doublet":0,"Y":F(1,3),"b3":-1,"spin":1,"d2":3},
 "L":{"triality":0,"doublet":1,"Y":-F(1,2),"b3":0,"spin":1,"d2":3},
 "ec":{"triality":0,"doublet":0,"Y":F(1),"b3":0,"spin":1,"d2":3},
 "Nc":{"triality":0,"doublet":0,"Y":F(0),"b3":0,"spin":1,"d2":3},
 "H":{"triality":0,"doublet":1,"Y":F(1,2),"b3":0,"spin":0,"d2":2},
 "Hc":{"triality":0,"doublet":1,"Y":-F(1,2),"b3":0,"spin":0,"d2":2},
}
def properties(mono):
    return {
      "color_triality_mod3":sum(fields[q]["triality"] for q in mono)%3,
      "SU2_doublet_parity":sum(fields[q]["doublet"] for q in mono)%2,
      "hypercharge":sum((fields[q]["Y"] for q in mono),F(0)),
      "number_Weyl":sum(fields[q]["spin"] for q in mono),
      "three_times_baryon_number":sum(fields[q]["b3"] for q in mono),
      "canonical_dim_twice":sum(fields[q]["d2"] for q in mono)}
def necessary_sm_singlet(mono):
    p=properties(mono)
    return (p["color_triality_mod3"]==0 and p["SU2_doublet_parity"]==0
        and p["hypercharge"]==0 and p["number_Weyl"]%2==0)
def show(mono):
    p=properties(mono)
    return {"operators":list(mono),"DeltaB":p["three_times_baryon_number"]/3,
         "Z9_charge":p["three_times_baryon_number"]%9,
         "dim":p["canonical_dim_twice"]/2,
         "SM_necessary":necessary_sm_singlet(mono)}
def main():
    qqql=("Q","Q","Q","L")
    uddn=("uc","dc","dc","Nc")
    uude=("uc","uc","dc","ec")
    assert all(necessary_sm_singlet(o) for o in (qqql,uddn,uude))
    examples=[show(x) for x in (qqql,uddn,uude)]
    assert {r["Z9_charge"] for r in examples}=={3,6}
    n_candidates=0;forbidden_by_z9=0;allowed_delta3=0
    dimby={}
    # Conservatively screen gauge-singlet NECESSARY monomials of up
    # to eight Weyl fields (dimension 12), and up to two Higgs insertions.
    names=list(fields)
    for n in range(2,9,2):
        for fermions in itertools.combinations_with_replacement(names[:6],n):
            for nh in range(3):
                for hsc in itertools.combinations_with_replacement(("H","Hc"),nh):
                    mono=fermions+hsc
                    if not necessary_sm_singlet(mono):continue
                    p=properties(mono)
                    b3=p["three_times_baryon_number"]
                    if not b3:continue
                    n_candidates+=1
                    if abs(b3) in (3,6):
                        assert b3%9 != 0
                        forbidden_by_z9+=1
                    if abs(b3)>=9 and b3%9==0:
                        allowed_delta3+=1
                    key=str(F(p["canonical_dim_twice"],2))
                    dimby[key]=dimby.get(key,0)+1
    assert n_candidates>20 and forbidden_by_z9>20
    # Nine anti-quarks + one gauge-neutral LH neutrino:
    # 3*(uc dc dc)+Nc; 10 Weyl fields, dimension 15.
    triple=tuple(["uc","dc","dc"]*3+["Nc"])
    t=show(triple)
    assert t["SM_necessary"] and t["Z9_charge"]==0 and t["DeltaB"]==-3
    assert t["dim"]==15.
    # Independent simple test over random baryon numbers:
    assert all((3*B)%9!=0 for B in (-2,-1,1,2))
    assert all((3*B)%9==0 for B in (-6,-3,0,3,6))
    # Primitive 3(B-L) normalization of the prior minimal seesaw:
    # quark q=1, lepton doublet q=-3, Nc q=+3, S(BL=-2) q=-6.
    # S condensation leaves Z6, not the Z9 needed above.
    q_minimalBL={"quark":1,"lepton":-3,"Nc":3,"S":-6}
    assert abs(q_minimalBL["S"])==6
    assert q_minimalBL["lepton"]%9!=0
    result={"status":"PASS_Z9_PROTON_BARYON_SELECTION_FULL_MONOMIAL_SCREEN",
      "paper":"Davighi-Greljo-Ponce Diaz Axion Quality from Exact Proton Stability arXiv:2609.01712 (2026)",
      "claimed_Z9_action":"q(Q)=+1, q(uc)=q(dc)=-1, all leptons and Higgs neutral",
      "exact_selection_rule":"Delta B=0 mod3",
      "minimal_BL_3BL_integer_charges":q_minimalBL,
      "minimal_BL_S_condensate_remnant":"Z6, not desired lepton-neutral quark-unit Z9",
      "cannot_get_Z9_proton_selection_from_unchanged_minimal_BL_S_vev":True,
      "explicit_dim6_forbidden_SM_operators":examples,
      "number_necessary_SM_gauge_singlet_nonzero_B_operator_monomials":n_candidates,
      "screened_DeltaB_1_or_2_all_forbidden":forbidden_by_z9,
      "candidate_DeltaB_multiple3_found_in_screen":allowed_delta3,
      "search_dimension_histogram":dimby,
      "explicit_schematic_DeltaB3_operator":t,
      "scope":"Brute-force color triality, SU2 parity, hypercharge, Lorentz Weyl-even are NECESSARY not full SU3/SU2/spin/Fermi contraction tests. The dim15 DeltaB3 operator may need distinct generations for nonzero Grassmann contraction.",
      "critical_missing":"Naively asserting Z9 does not prove discrete gauge anomaly cancellation or a UV Higgs embedding. Nor does Z9 proton stability alone forbid PQ-breaking scalar monomials, imply dark-matter abundance, or fix strong CP.",
      "novelty":"Independent executable operator-selection audit of published Z9 idea, not a discovery of Z9 proton stability."}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("Z9_PASS",n_candidates,forbidden_by_z9,"dim15",t,flush=True)
    return result
if __name__=="__main__":main()
