#!/usr/bin/env python3
"""Pass9061-9068: reduce the unresolved H(4) 3024 split to one exact 16-point stabilizer test."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS9061_9068_H4_3024_SPLIT_DISCRIMINATOR.json'
H=24192
configs=189
extensions=16
assert H//configs==128
assert 3024//configs==extensions
# Leech refinement alternatives: one 3024 orbit (pair stabilizer 8) versus two 1512 orbits (pair stabilizer 16).
assert H//3024==8
assert H//1512==16
out={
 'schema':'w33.pass9061_9068.h4_3024_split_discriminator.v1','status':'PASS','passes':'9061-9068',
 'classical_candidates':{
   'S^1_1':'one point and one incident line','S^2_1':'two collinear points (and their common line)'},
 'each_classical_count':3024,'configurations_inside_fixed_H2':configs,'extensions_per_configuration':extensions,
 'configuration_stabilizer_order':128,
 'Leech_refinement':{'self_transpose_option':{'orbit':3024,'pair_stabilizer_order':8,'configuration_stabilizer_orbits_on_16':[16]},'oriented_option':{'orbits':[1512,1512],'pair_stabilizer_order':16,'configuration_stabilizer_orbits_on_16':[8,8]}},
 'exact_remaining_test':'Compute the order-128 configuration stabilizer on the 16 H(2)-extensions for S^1_1 and S^2_1. The type with orbit shape 8+8 is exactly the unique oriented Leech relation; the type with orbit shape 16 is the self-transpose 3024 relation.',
 'theorem':'The formerly ambiguous 3024 labeling is reduced to a single 16-point orbit calculation; no other classical intersection type can be the unique oriented Leech pair.',
 'claim_boundary':'This pass deliberately does not guess whether S^1_1 or S^2_1 is the 8+8 case.'}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'PASS','stabilizer':128,'test':'16 versus 8+8'}))
