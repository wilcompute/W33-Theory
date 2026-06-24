#!/usr/bin/env python3
"""BT1715 - objectwise 48-bus axis quotient theorem."""
from __future__ import annotations
import json
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1715_48_bus_axis_quotient.json'
def lat(i,j): return i^j
def side(kind,idx,cell):
 i,j=cell
 if kind=='R': return j%2
 if kind=='C': return i%2
 if kind=='S': return i%2
 raise ValueError(kind)
def build_certificate():
 cells=[(i,j) for i in range(4) for j in range(4)]
 axes=[('R',i) for i in range(4)]+[('C',j) for j in range(4)]+[('S',k) for k in range(4)]
 face_axes={c:[('R',c[0]),('C',c[1]),('S',lat(*c))] for c in cells}
 axis_faces=defaultdict(list)
 for c,axs in face_axes.items():
  for a in axs: axis_faces[a].append(c)
 face_obs={}; obs_faces=defaultdict(list)
 for c,axs in face_axes.items():
  os=[]
  for kind,idx in axs:
   o=(kind,idx,side(kind,idx,c)); os.append(o); obs_faces[o].append(c)
  face_obs[c]=os
 obs=sorted(obs_faces)
 quotient_ok=True
 for a in axes:
  q=sorted(obs_faces[(a[0],a[1],0)]+obs_faces[(a[0],a[1],1)])
  quotient_ok = quotient_ok and q==sorted(axis_faces[a])
 checks={'tomotope_12_axes':len(axes)==12,'tomotope_16_faces':len(cells)==16,'tomotope_48_incidences':sum(len(v) for v in face_axes.values())==48,'each_face_has_3_axes':all(len(v)==3 for v in face_axes.values()),'each_axis_has_4_faces':all(len(axis_faces[a])==4 for a in axes),'q2025_24_observations':len(obs)==24,'q2025_48_incidences':sum(len(v) for v in face_obs.values())==48,'each_observation_degree_2':all(len(obs_faces[o])==2 for o in obs),'axis_quotient_recovers_tomotope':quotient_ok,'holonet_16_by_3_ticks_48':16*3==48,'objectwise_cell_identity':set(face_axes)==set(face_obs)==set(cells)}
 return {'theorem':'BT1715 Objectwise 48-Bus Axis-Quotient Theorem','verified':all(checks.values()),'summary':'A concrete 4x4 Klein-Latin bus realizes the tomotope/Reye (12_4,16_3) layer and its q-2025-style oriented double cover (24_2,16_3). Pairing the two degree-2 observations over each axis quotients 24 observations back to 12 axes. The same 16 cells with three phase labels give the Holonet 16x3=48 tick body.','models':{'tomotope_reye':{'axes':[list(a) for a in axes],'faces':{f'{i},{j}':[list(a) for a in axs] for (i,j),axs in face_axes.items()}},'q2025_oriented_cover':{'observations':[list(o) for o in obs],'lines':{f'{i},{j}':[list(o) for o in os] for (i,j),os in face_obs.items()}},'holonet_ticks':{'cells':16,'phases':['R','C','S'],'ticks':48}},'axis_degrees':{str(a):len(axis_faces[a]) for a in axes},'observation_degrees':{str(o):len(obs_faces[o]) for o in obs},'claim_boundary':['This gives an explicit abstract incidence isomorphism/quotient between the bus types.','It does not claim the q-2025 red/blue domains use this exact Klein-Latin coordinatization before a paper-derived labeling is extracted.'],'checks':checks}
def main():
 cert=build_certificate(); OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(cert,indent=2,sort_keys=True)+'\n'); print(cert['theorem'],cert['verified']); return 0 if cert['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
