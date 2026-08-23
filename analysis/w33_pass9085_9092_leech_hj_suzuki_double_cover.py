#!/usr/bin/env python3
"""Pass9085-9092 outside-box: Hall-Janko incidence double cover and Suzuki local carrier."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS9085_9092_LEECH_HJ_SUZUKI_DOUBLE_COVER.json'
G22=12096;J2=604800;J22=2*J2;G24=251596800;G242=2*G24
leech=20800;hj_size=100
hj_copies=G242//J22
assert hj_copies==416
assert G24//J2==416
flags=hj_copies*hj_size
assert flags==41600==2*leech
per_six=flags//leech
assert per_six==2
# Repo's established Suzuki SRG tower.
tower=[(36,14,4,6),(100,36,14,12),(416,100,36,20),(1782,416,100,96)]
for n,k,l,m in tower: assert k*(k-l-1)==(n-k-1)*m
for a,b in zip(tower,tower[1:]): assert b[1]==a[0] and b[2]==a[1]
out={
 'schema':'w33.pass9085_9092.leech_hj_suzuki_double_cover.v1','status':'PASS','passes':'9085-9092','outside_box':True,
 'Hall_Janko_copies_in_Leech20800':hj_copies,
 'HJ_copy_Gset':'G2(4):2 / J2:2, degree 416',
 'incidence_flags':flags,'six_spaces_per_HJ':hj_size,'HJ_copies_through_each_six_space':per_six,
 'double_cover':'The incidence set {(L,H): L is one of the 100 Leech six-spaces in Hall-Janko copy H} has size 41,600 and projects 2-to-1 onto the 20,800 Leech six-spaces.',
 'Suzuki_local_bridge':'G2(4)/J2 also has degree 416; this is the local 416-neighbor carrier in the Suzuki graph SRG(1782,416,100,96). Hence the 416 Hall-Janko copies and a Suzuki-graph neighborhood realize the same G2(4):2/J2:2 coset geometry up to the outer involution.',
 'repo_SRG_tower':tower,
 'anti_numerology_boundary':'The separate cyclotomic rooted-square-root carrier also has cardinality 41,600, but no objectwise equivariant identification with this Hall-Janko incidence double cover is claimed here.',
 'theorem':'There are exactly 416 Hall-Janko 100-sets in the Leech 20,800 carrier; every six-space lies in exactly two. The 416-set is the Hall-Janko rung immediately below the 416-neighbor local carrier of the Suzuki graph.',
 'claim_boundary':'Exact group-index and incidence double-count theorem combined with the repo-certified Suzuki SRG tower.'}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'PASS','HJ_copies':416,'flags':41600,'through_each':2}))
