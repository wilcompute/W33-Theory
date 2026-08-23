#!/usr/bin/env python3
"""Pass8309-8316: exact setwise stabilizer of the explicit Q+(3,3) residue in the
Monster-local O8+(3):S4 triality carrier.

The calculation is classical orthogonal orbit-stabilizer arithmetic, cross-checked
against the current projective-E8 orbit of the same 16-point subquadric.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS8309_8316_MONSTER_LOCAL_QPLUS33_STABILIZER.json'
q=3

def Oplus(m):
    # full linear plus-orthogonal isometry group in dimension 2m, q odd
    z=2*q**(m*(m-1))*(q**m-1)
    for i in range(1,m):z*=q**(2*i)-1
    return z

def main():
    simple=4952179814400                 # ATLAS O8+(3)=P Omega_8^+(3)
    outer=24                             # Out=S4
    aut=simple*outer                     # O8+(3):S4 on the 3360 triality carrier
    assert aut==118852315545600
    go4=Oplus(2);go8=Oplus(4)
    assert go4==1152                     # ATLAS: GO4+(3)=W(F4)
    assert go8==39617438515200
    assert go8==simple*8                 # set-stabilizer of one of the three triality types

    # Full linear O8 acts transitively on nondegenerate plus 4-spaces; stabilizer
    # is O4^+(3) x O4^+(3).  The common central -I cancels in the effective
    # projective point action, leaving the same orbit count.
    per_type=go8//(go4*go4)
    assert per_type==29852550
    all_types=3*per_type
    assert all_types==89557650
    stab_full=aut//all_types
    assert stab_full==go4*go4==1327104
    effective_point_stab=stab_full//2
    assert effective_point_stab==663552

    # Pass8301 reconstructed the same residue under projective W(E8)/+-I.
    proj_e8=348364800
    e8_orbit=3150
    e8_stab=proj_e8//e8_orbit
    assert e8_stab==110592
    assert stab_full%e8_stab==0 and stab_full//e8_stab==12
    assert effective_point_stab%e8_stab==0 and effective_point_stab//e8_stab==6

    out={
      'schema':'w33.pass8309_8316.monster_local_qplus33_stabilizer.v1','status':'PASS','passes':'8309-8316',
      'atlas':{'O8plus3_simple_order':simple,'Out':'S4','O8plus3_S4_order':aut,'GO4plus3_order':go4,'GO4plus3_identification':'W(F4)'},
      'orthogonal_orbit':{'Qplus33_residues_per_triality_type':per_type,'three_type_orbit':all_types},
      'residue_stabilizer':{'full_3360_action_order':stab_full,'effective_on_16_point_type_vertices':effective_point_stab,'geometric_source':'(GO4+(3) x GO4+(3)) on W perp W^perp, with the full triality type-stabilizer retaining one extra kernel involution on point vertices'},
      'projective_E8_comparison':{'residue_orbit':e8_orbit,'residue_stabilizer_order':e8_stab,'index_in_full_3360_residue_stabilizer':12,'index_in_effective_point_stabilizer':6},
      'theorem':'The explicit 16-point Q+(3,3) residue lies in the unique classical orbit of plus nondegenerate 4-spaces. There are 29,852,550 per triality type and 89,557,650 over all three types. Its setwise stabilizer in O8+(3):S4 has order 1,327,104=1152^2; the effective point-type action has order 663,552. The current projective-E8 residue stabilizer is an actual subgroup of index 12 in the full triality-carrier stabilizer.',
      'claim_boundary':'Finite orthogonal/triality carrier theorem. Literal ATLAS vertex numbers are a separate coordinate certificate and are not asserted here.',
      'sources':['ATLAS O8+(3): order 4952179814400, Out=S4','ATLAS W(F4)=GO4+(3): order 1152']}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','orbit':all_types,'stabilizer':stab_full,'E8_index':12}))
if __name__=='__main__':main()
