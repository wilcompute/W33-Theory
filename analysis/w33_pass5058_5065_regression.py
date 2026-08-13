#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def J(n): return json.loads((R/'data'/n).read_text())
assert J('PART_W33_PASS5058_Q3_MINIMUM_SHELL.json')['minimum_words']==160
x=J('PART_W33_PASS5059_JACOBIAN_BICYCLE_BRIDGE.json'); assert x['hom_dimension']==1 and x['nonzero_map_rank']==15 and not x['isomorphic']
x=J('PART_W33_PASS5060_STEINBERG_ORIENTATION_CHANNELS.json'); assert x['fixed']==5 and x['twisted']==5
assert J('PART_W33_PASS5062_CODE_BUILDING_RECONSTRUCTION.json')['panel_graph']['W33_Levi']
x=J('PART_W33_PASS5061_5065_AUXILIARY.json'); assert x['5061']['new_den']==3120 and x['5064']['q4'][3]==108800 and x['5065']['code_perm_aut_order']==51840
print('PASS')
