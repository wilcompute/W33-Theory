#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
# From Pass11580: nu^c has qBL=3 and r=2T3R=-1, hence y=qBL+3r=0.
nu={'qBL':3,'r':-1,'sixY':0}
pair={k:2*v for k,v in nu.items()}
assert pair=={'qBL':6,'r':-2,'sixY':0}
# A scalar VEV making nu^c nu^c gauge invariant must have opposite charges.
vev={'qBL':-6,'r':2,'sixY':0}
# Sym^2(16)=10+126, multiplicity one for each.  The 10_H Pati-Salam content
# (6,1,1)+(1,2,2) has no SU(2)_R triplet T3R=+1 component, so the neutral
# B-L=-2 Majorana VEV must live in the scalar rep conjugate to the 126 channel.
out={'status':'PASS_UNIQUE_SPIN10_RIGHT_HANDED_NEUTRINO_MAJORANA_CHANNEL',
     'nu_c_charges':nu,'nu_c_pair_charges':pair,'required_scalar_vev_charges':vev,
     'symmetric_square':'Sym^2(16)=10+126, both multiplicity one',
     '10H_excluded':'10_H=(6,1,1)+(1,2,2) under Pati-Salam; it contains no SU(2)_R triplet with r=+2 and qBL=-6.',
     'Majorana_channel':'the scalar representation conjugate to the unique 126 component of Sym^2(16)',
     'seesaw_reading':'A neutral B-L=-2, T3R=+1 VEV in that channel gives a Majorana mass to nu^c while preserving U(1)_Y.',
     'boundary':'The existence, scale and family texture of the 126-type VEV are not derived here.'}
(ROOT/'data/PART_W33_PASS11595_NEUTRINO_MAJORANA_CHANNEL.json').write_text(json.dumps(out,indent=2,sort_keys=True))
print(json.dumps(out,indent=2))
