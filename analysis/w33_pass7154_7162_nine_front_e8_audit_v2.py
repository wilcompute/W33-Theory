#!/usr/bin/env python3
"""Serialization-safe replay wrapper for Pass7154--7162.

The underlying producer exposes exact computation functions; this wrapper canonicalizes
non-JSON dictionary keys before freezing the certificate.
"""
from __future__ import annotations
import json
from pathlib import Path
import w33_pass7154_7162_nine_front_e8_audit as a

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7154_7162_NINE_FRONT_E8_AUDIT.json'

def canon(x):
    if isinstance(x,dict): return {str(k):canon(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [canon(v) for v in x]
    if isinstance(x,set): return sorted(canon(v) for v in x)
    return x

def main():
    p7154=a.anchor_rank_degree_data()
    p7155=a.pgl2_big_cell()
    p7156=a.hexad_cycle_obstruction()
    p7157=a.higher_rank_replay()
    p7158=a.homogeneous_hexagon_bundle()
    distinct,comp,cm,outer_set,p7159=a.code_column_geometry()
    p7159['natural_alternating_form_W33_audit']=a.natural_form_audit(comp)
    p7160=a.affine_hamming_flats(distinct,cm,outer_set)
    p7161=a.construction_A_firewall(cm,outer_set)
    p7162=a.e8_root_audit(p7160)
    out={
      'schema':'w33.pass7154_7162.nine_front_e8_audit.v2','status':'PASS',
      'boundary':'Exact finite algebra/code/geometry computations. The unresolved q=9 48-clique decision remains separate unless its own aggregate certificate is present. E8 statements are restricted to root counts, code-lattice interfaces, and explicit obstructions; no particle or physical identification.',
      'pass_7154_anchor_torus_rank_coherent_data':p7154,
      'pass_7155_gram_PGL2_big_cell_interface':p7155,
      'pass_7156_code_geometry_lifting_obstruction':p7156,
      'pass_7157_higher_rank_involution_pair_theorem':p7157,
      'pass_7158_witness_orbit_hexagon_bundle':p7158,
      'pass_7159_bonkers_23_plus_40_binary_projective_probe':p7159,
      'pass_7160_bonkers_local_Hamming_punctures':p7160,
      'pass_7161_bonkers_Construction_A_firewall':p7161,
      'pass_7162_E8_248_audit':p7162,
    }
    out=canon(out)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': main()
