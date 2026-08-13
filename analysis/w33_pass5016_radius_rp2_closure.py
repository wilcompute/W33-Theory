#!/usr/bin/env python3
"""Pass5016: factor the low-shell character closure into tetrahedral, RP2, octahedral, and residual pieces."""
from __future__ import annotations
import itertools,json,sys
from collections import Counter,deque
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from analysis.w33_pass4992_4999_common import build_base,build_group,gf2_rank_int
OUT=ROOT/'data/PART_W33_PASS5016_RADIUS_RP2_SYMMETRY_CLOSURE.json'
RP2=[(0,1,6),(0,1,17),(0,6,10),(0,10,34),(0,17,25),(0,25,34),(1,6,13),(1,13,34),(1,17,22),(1,22,34),(5,6,10),(5,6,13),(5,10,22),(5,13,25),(5,17,22),(5,17,25),(10,22,34),(13,25,34)]

def piv(rows):
 p={}
 for r0 in rows:
  x=int(r0)
  while x:
   q=x.bit_length()-1
   if q in p:x^=p[q]
   else:p[q]=x;break
 return p

def reduce(x,p):
 for q in sorted(p,reverse=True):
  if x>>q&1:x^=p[q]
 return x

def main():
 b=build_base();H=b['H36'];tri=b['tri_masks'];res=[m for m,_ in b['residual']]
 tri_t=[tuple(b['tri_by_mask'][m]) for m in tri];ti={frozenset(t):i for i,t in enumerate(tri_t)}
 obs=tri+res
 assert (len(obs),gf2_rank_int(obs))==(1890,324)
 relation_dim=len(obs)-324
 # Every K4 has four sigma-even triangle faces; their tetrahedral boundaries form rank755.
 K4=[c for c in itertools.combinations(range(36),4) if all(H.has_edge(*e) for e in itertools.combinations(c,2))]
 assert len(K4)==1080
 krel=[]
 for c in K4:
  r=0
  for t in itertools.combinations(c,3):r^=1<<ti[frozenset(t)]
  krel.append(r)
 assert gf2_rank_int(krel)==755
 tri_rel_dim=1080-gf2_rank_int(tri);assert tri_rel_dim==756
 # Explicit non-tetrahedral closed surface.
 r=0;edge=Counter();verts=set()
 for t in RP2:
  assert frozenset(t) in ti;r^=1<<ti[frozenset(t)];verts.update(t)
  for e in itertools.combinations(t,2):edge[tuple(sorted(e))]+=1
 assert all(v==2 for v in edge.values()) and len(verts)==10 and len(edge)==27
 # XOR of the eighteen triangle boundaries vanishes.
 z=0
 for i in range(1080):
  if r>>i&1:z^=tri[i]
 assert z==0 and reduce(r,piv(krel))!=0
 # Each vertex link is a cycle, so this is a closed triangulated surface; chi=1 => RP2.
 for v in verts:
  L=[]
  for t in RP2:
   if v in t:L.append(tuple(x for x in t if x!=v))
  deg=Counter(x for e in L for x in e)
  assert set(deg.values())=={2}
 assert len(verts)-len(edge)+len(RP2)==1
 # The 270 local octahedron equations have disjoint residual triples, hence rank270.
 local=[];tri_index={m:i for i,m in enumerate(tri)};res_index={m:i for i,m in enumerate(res)}
 for (a,q),items in sorted(b['pair_to_res'].items()):
  U=[d for d in range(36) if b['M'][a,d]==b['M'][q,d]==0];faces=[]
  for t in itertools.combinations(U,3):
   if all(H.has_edge(*e) for e in itertools.combinations(t,2)):
    es=[b['ei'][tuple(sorted(e))] for e in itertools.combinations(t,2)];m=sum(1<<x for x in es)
    if m in tri_index:faces.append(m)
  assert (len(faces),len(items))==(4,3)
  rr=0
  for m in faces:rr^=1<<tri_index[m]
  for m,_ in items:rr^=1<<(1080+res_index[m])
  local.append(rr)
 assert gf2_rank_int(local)==270
 # The K4 family is one PGSp orbit.
 G=build_group(b);ki={frozenset(c):i for i,c in enumerate(K4)};seen={0};D=deque([0])
 while D:
  i=D.popleft();c=K4[i]
  for gp in G['DPf']:
   j=ki[frozenset(gp[x] for x in c)]
   if j not in seen:seen.add(j);D.append(j)
 assert len(seen)==1080
 missing=relation_dim-270;attachments=relation_dim-tri_rel_dim-270
 assert (relation_dim,missing,attachments)==(1566,1296,540)
 out={'pass':5016,'status':'PASS','observables':1890,'character_rank':324,'all_relations':1566,
  'triangle_internal_relations':756,'K4_tetrahedral_boundaries':{'count':1080,'PGSp_orbits':1,'rank':755},
  'global_mod2_class':{'dimension':1,'representative_faces':RP2,'V':10,'E':27,'F':18,'euler_characteristic':1,'closed_surface':'RP2','not_in_K4_boundary_span':True},
  'octahedron_local_relations':270,'residual_attachment_quotient':540,'missing_beyond_oct_local':1296,
  'factorization':'1566 = 755 tetrahedral + 1 RP2 + 270 octahedral + 540 residual attachments',
  'covering_radius':[134,173],'radius_improved':False,
  'theorem':'The full low-shell character closure admits an exact symmetry/topology factorization. The 756 triangle-only relations are 755 independent boundaries from a single PGSp orbit of 1080 H36 K4 tetrahedra plus one global mod-2 RP2 class. After the 270 local octahedral equations, the remaining closure deficit is exactly 756+540=1296. Thus the difficult global radius model is localized to one RP2 parity class, the tetrahedral orbit, and 540 residual attachment degrees rather than an undifferentiated 1296 constraints.',
  'boundary':'This reorganizes the exact distance-173 SAT closure but does not provide a complete UNSAT certificate; 134<=rho(K)<=173 remains the theorem.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
