#!/usr/bin/env python3
"""Parses GAP's TWO S5 216-coset permutation characters, selects W33 route class
from its known nonzero 24D point map, freezes exact multiplicity table.
"""
from pathlib import Path
import re,json
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'data/w33_20261103_gap_216_irreducibles.txt').read_text()
assert 'Group=25920' in s and 'MaximalS5=2' in s
pattern=r'S5 IdGroup=\[\s*120,\s*34\s*\].*?Degrees=\[([^]]+)\].*?Multiplicities=\[([^]]+)\].*?Dimension=(\d+)'
matches=re.findall(pattern,s,re.S)
assert len(matches)==2
L=[]
for deg,mult,dim in matches:
 d=[int(t) for t in re.findall(r'\d+',deg)]
 m=[int(t) for t in re.findall(r'\d+',mult)]
 assert len(d)==len(m)==20 and sum(a*b for a,b in zip(d,m))==int(dim)==216
 L.append({'degrees':d,'multiplicities':m,'constituent_degrees':sum(([a]*b for a,b in zip(d,m)),[]),
   'commutant_dimension':sum(v*v for v in m)})
target=[i for i,r in enumerate(L) if r['multiplicities'][9]==1 and r['multiplicities'][19]==1]
assert target==[1],target
t=L[target[0]]
assert sorted(t['constituent_degrees'])==[1,15,15,20,24,30,30,81]
assert t['commutant_dimension']==10
assert L[0]['commutant_dimension']==10 # both actions have rank10? check might differ
out={'status':'PASS_EXACT_GAP_216_COSSET_CHARACTERS',
 'group':'PSp4(3)','group_order':25920,
 'two_nonconjugate_S5_stabilizers':True,
 'class_characters':L,'selected_route_class_index_0based':target[0],
 'selected_route_complex_degrees':sorted(t['constituent_degrees']),
 'route_commutant_dimension':10,
 'selection_logic':'Nonzero G-intertwiner from 216 route module to positive 24D point-graph module via sign-frame Z. Only the second S5 coset character contains 24, so that is the route class.',
 'scope':'GAP exact character decomposition; 30D complex conjugacy independently supported by numeric antisymmetric complex structure, not yet checked by a class-function conjugation identity.'}
(ROOT/'data/w33_20261103_gap_216_exact_character_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
print('GAP216',json.dumps(out)[:4400],flush=True)
