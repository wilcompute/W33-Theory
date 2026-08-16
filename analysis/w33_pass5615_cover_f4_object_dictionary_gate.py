#!/usr/bin/env python3
"""Pass5615: fail-closed 13-cover -> Latin -> F4 short-root-pair object dictionary.

The expensive GAP producer is analysis/w33_pass5606_cover12_explicit_conjugator.g.
This consumer refuses to synthesize an object map unless that producer has emitted
a direct S12 conjugator. Once present it composes the cover->Latin permutation
with the already frozen F4pair->Latin conjugator from Pass5596.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5615_COVER_F4_OBJECT_DICTIONARY.json'

def inv(p):
    q=[0]*len(p)
    for i,j in enumerate(p): q[j]=i
    return q

def main():
    cover_cert=ROOT/'data/PART_W33_PASS5606_COVER12_EXPLICIT_CONJUGATOR.json'
    f4_cert=ROOT/'data/PART_W33_PASS5596_F4_ROOTPAIR_LATIN_ACTION.json'
    selected_cover=[7,31,74,112,129,141,158,190,194,227,255,278,321]
    if not cover_cert.exists() or not f4_cert.exists():
        out={'pass':5615,'status':'FAIL_CLOSED_PENDING_DIRECT_GAP_OBJECT_MAP',
             'selected_13_cover':selected_cover,
             'known_exact_structure':{'setwise_stabilizer_order':1152,'S13_image_order':576,'pointwise_kernel_order':2,'orbit_sizes':[1,12]},
             'missing':[str(p.relative_to(ROOT)) for p in (cover_cert,f4_cert) if not p.exists()],
             'boundary':'No cover-to-F4 vertex dictionary is asserted without the direct S12 conjugator.'}
    else:
        c=json.loads(cover_cert.read_text());f=json.loads(f4_cert.read_text())
        assert c.get('conjugate_in_S12') is True
        mov_pos=list(map(int,c['cover13_moving_orbit_original_positions'])) # one-based positions in sorted selected cover
        fixed_pos=next(i for i in range(1,14) if i not in set(mov_pos))
        moving=[selected_cover[i-1] for i in mov_pos]
        fixed=selected_cover[fixed_pos-1]
        # GAP witness is one-based images cover12 -> Latin12.
        cl=[int(x)-1 for x in c['conjugator_cover12_to_latin12_one_based']]
        fl=list(map(int,f['conjugating_permutation_F4pair_to_Latin']))
        assert sorted(cl)==list(range(12)) and sorted(fl)==list(range(12))
        # F4 -> Latin = fl, hence Latin -> F4 = fl^{-1}; cover -> F4 = fl^{-1} o cl.
        lif=inv(fl);cf=[lif[x] for x in cl]
        assert len(moving)==len(cf)==12
        out={'pass':5615,'status':'EXPLICIT_COVER_TO_F4_OBJECT_DICTIONARY',
             'selected_13_cover':selected_cover,'fixed_cover_position_one_based':fixed_pos,
             'fixed_cover_vertex':fixed,'moving_cover_positions_one_based':mov_pos,'moving_cover_vertices':moving,
             'cover_vertex_to_F4_short_root_pair_index':{str(v):int(cf[i]) for i,v in enumerate(moving)},
             'cover12_to_latin_zero_based':cl,'F4pair_to_latin_zero_based':fl,
             'boundary':'This is an action-level object dictionary, not a physical identification of the twelve objects.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
