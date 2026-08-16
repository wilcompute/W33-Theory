#!/usr/bin/env python3
"""Pass5606: compose the GAP cover12->Latin witness with the F4->Latin witness.

This script intentionally fails closed until the GAP certificate exists and says
conjugate_in_S12=true.  When it does, the output is an explicit table from the
selected 13-cover's twelve moving vertices to scaled coordinates for the twelve
antipodal short-root pairs of F4.
"""
from __future__ import annotations
import importlib, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
f4=importlib.import_module('w33_pass5596_f4_rootpair_latin_action')
GAP=ROOT/'data/PART_W33_PASS5606_COVER12_EXPLICIT_CONJUGATOR.json'
OLD=ROOT/'data/PART_W33_PASS5596_F4_ROOTPAIR_LATIN_ACTION.json'
OUT=ROOT/'data/PART_W33_PASS5606_COVER_TO_F4_ROOTPAIR_MAP.json'

def neg(v): return tuple(-x for x in v)

def main():
    if not GAP.exists(): raise SystemExit('GAP Pass5606 certificate missing: run w33_pass5606_cover12_explicit_conjugator.g')
    g=json.loads(GAP.read_text())
    if not g.get('conjugate_in_S12'): raise SystemExit('cover12 is not conjugate to Latin12; no F4 map may be emitted')
    if not OLD.exists():
        f4.main()
    a=json.loads(OLD.read_text())
    phi=tuple(int(x) for x in a['conjugating_permutation_F4pair_to_Latin'])
    iphi=f4.inverse_perm(phi)
    c=tuple(int(x)-1 for x in g['conjugator_cover12_to_latin12_one_based'])
    roots=f4.f4_roots(); short=[r for r in roots if sum(x*x for x in r)==4]
    pairs=sorted({min(r,neg(r)) for r in short})
    assert len(pairs)==12
    mov=list(map(int,g['cover13_moving_orbit_original_positions']))
    assert len(mov)==12
    rows=[]
    for cover_idx in range(12):
        latin_idx=c[cover_idx]
        f4_idx=iphi[latin_idx]
        rows.append({
          'cover_action_position_one_based':cover_idx+1,
          'cover13_original_position_one_based':mov[cover_idx],
          'latin_symbol_zero_based':latin_idx,
          'F4_short_rootpair_index_zero_based':f4_idx,
          'F4_scaled_root_representative':list(pairs[f4_idx]),
        })
    out={
      'pass':5606,'status':'EXPLICIT_COVER12_TO_F4_SHORT_ROOTPAIR_BIJECTION',
      'map':rows,
      'theorem':'The selected 13-cover moving 12-orbit is permutation-isomorphic to the Reye/Klein-V4 Latin/W(F4)/+-1 short-root-pair action, with the displayed object-level bijection.',
      'boundary':'Emitted only after the exact GAP S12 conjugacy gate returns true.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': main()
