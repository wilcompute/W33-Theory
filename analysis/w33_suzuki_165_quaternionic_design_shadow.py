#!/usr/bin/env python3
"""Quaternionic design shadow of the Suzuki local-165 W33 carrier.

The exact local carrier certified in w33_suzuki_local_165_gq48_spectral_bridge
is the U5(2) rank-three graph SRG(165,36,3,9), i.e. GQ(4,8).  This verifier
reconstructs its 297 generalized-quadrangle lines directly from the 165 graph:
for every adjacent pair u,v, lambda=3 says the line is
    {u,v} union (N(u) intersect N(v)),
and the resulting five-set is a K5.  Deduplication gives 297 lines, with nine
through each point.

External classical representation theory gives another realization of the same
U5(2) degree-165/297 incidence G-set: the quaternion reflection group
2 x PSU5(2) has a 165-ray tight projective 3-design in HP^4, with angle set
{0,1/4}; its 297 Jordan frames are precisely the GQ(4,8) lines and nine pass
through each ray (Hoggar; modern summary in Nasmith's thesis, Example A.16).
ATLAS independently lists primitive U5(2) permutation actions of degrees 165
and 297.

The theorem here is the finite G-set/incidence identification.  Interpreting the
quaternionic realization as physical quantum states is optional and is NOT
assumed; ordinary complex quantum mechanics would require an explicit complex
or fusion-frame realization and measurement protocol.
"""
from __future__ import annotations
import importlib.util,itertools,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_suzuki_165_quaternionic_design_shadow.json'

def load(name):
 p=ROOT/'analysis'/(name+'.py');s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def main(write=True):
 t=load('w33_suzuki_w33_e6_incidence_tower');A=t.parse_meataxe(ROOT/'data/atlas/2SuzG1-f3r12B0.m1');B=t.parse_meataxe(ROOT/'data/atlas/2SuzG1-f3r12B0.m2')
 orb=t.subspace_orbit(t.U1,[A,B]);P=sorted(t.projective_points(t.U1));p=np.array(P[0],dtype=np.int64)
 V=[U for U in orb.values() if t.rankp(np.vstack([U,p]))==4];assert len(V)==165
 G=np.zeros((165,165),dtype=bool)
 for i,j in itertools.combinations(range(165),2):
  if t.intersection_dim(V[i],V[j])==2:G[i,j]=G[j,i]=True
 assert set(map(int,G.sum(1)))=={36}
 lines=set()
 for i,j in itertools.combinations(range(165),2):
  if not G[i,j]:continue
  C=tuple([i,j]+[k for k in range(165) if G[i,k] and G[j,k]])
  C=tuple(sorted(set(C)));assert len(C)==5
  assert all(G[a,b] for a,b in itertools.combinations(C,2))
  lines.add(C)
 assert len(lines)==297
 inc=[0]*165
 edge_mult={}
 for L in lines:
  for x in L:inc[x]+=1
  for e in itertools.combinations(L,2):edge_mult[e]=edge_mult.get(e,0)+1
 assert set(inc)=={9} and len(edge_mult)==165*36//2 and set(edge_mult.values())=={1}
 out={
  'schema':'w33.suzuki_165_quaternionic_design_shadow.v1','status':'PASS',
  'headline':'The local 165 Suzuki/Leech W33 encodings reconstruct all 297 lines of GQ(4,8) as unique K5 Jordan-frame candidates: five W33 encodings per line, nine lines per encoding, and every graph edge lies on one line. This is the same U5(2) degree-165/297 incidence G-set that has a classical quaternionic tight-projective-3-design realization in HP^4.',
  'finite_incidence':{'points':165,'lines':297,'points_per_line':5,'lines_per_point':9,'identity':'165*9=297*5','collinearity_srg':[165,36,3,9],'edge_in_unique_line':True},
  'quaternionic_external_realization':{'group':'2 x PSU5(2)','space':'HP^4','rays':165,'design':'tight projective 3-design','angle_set':['0','1/4'],'Jordan_frames':297,'frames_per_ray':9},
  'physics_probe':'The abstract carrier supplies an exact highly symmetric ensemble/frame schedule. A useful next experiment is to construct a complex/fusion-frame image and test whether it gives a unitary-design or randomized-benchmarking ensemble for the six-qutrit register.',
  'falsifier':'If no physically natural complex/fusion-frame intertwiner preserves the U5(2) incidence/overlap algebra, the quaternionic design remains a beautiful alternative realization with no direct quantum-hardware meaning.',
  'boundary':'This certificate identifies finite U5(2) incidence. It does not assume quaternionic quantum mechanics or identify a Leech/W33 subspace with a quaternionic ray without an explicit intertwiner.',
  'checks':{'165_points':True,'297_lines':True,'five_per_line':True,'nine_per_point':True,'edge_unique_line':True}}
 if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
