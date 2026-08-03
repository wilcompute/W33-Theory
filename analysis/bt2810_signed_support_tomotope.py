#!/usr/bin/env python3
from __future__ import annotations
from collections import Counter
from itertools import combinations, permutations, product
import hashlib, json
from typing import Iterable
import networkx as nx

IndexSet=tuple[int,...]
SignFace=tuple[int,...]
Cell=tuple[str,tuple[int,...]]

def canon_sign(v:Iterable[int])->SignFace:
 v=tuple(int(x) for x in v)
 for x in v:
  if x:return v if x==1 else tuple(-y for y in v)
 raise ValueError('zero sign vector')

def support(v):return tuple(i for i,x in enumerate(v) if x)

def signed_faces(weight):
 out=set()
 for supp in combinations(range(4),weight):
  for signs in product((1,-1),repeat=weight):
   v=[0]*4
   for i,z in zip(supp,signs):v[i]=z
   out.add(canon_sign(v))
 return sorted(out)

def restrict(v,supp):return canon_sign(tuple(v[i] if i in supp else 0 for i in range(4)))
def even_full_signs():return [v for v in signed_faces(4) if __import__('math').prod(v)==1]

def build_poset():
 ranks={0:signed_faces(1),1:signed_faces(2),2:signed_faces(3)}
 H=[('H',s) for s in combinations(range(4),3)];T=[('T',v) for v in even_full_signs()];ranks[3]=H+T
 inc=set()
 for a_rank in range(3):
  for b_rank in range(a_rank+1,3):
   for a in ranks[a_rank]:
    for b in ranks[b_rank]:
     if set(support(a)).issubset(support(b)) and restrict(b,support(a))==a:inc.add(((a_rank,a),(b_rank,b)))
 for c in H:
  S=c[1]
  for r in range(3):
   for a in ranks[r]:
    if set(support(a)).issubset(S):inc.add(((r,a),(3,c)))
 for c in T:
  v=c[1]
  for r in range(3):
   for S in combinations(range(4),r+1):inc.add(((r,restrict(v,S)),(3,c)))
 return ranks,inc

def is_incident(a,b,inc):
 if a[0]==b[0]:return a==b
 lo,hi=(a,b) if a[0]<b[0] else (b,a)
 return (lo,hi) in inc

def flags_of(ranks,inc):
 return [(v,e,f,c) for v in ranks[0] for e in ranks[1] for f in ranks[2] for c in ranks[3] if is_incident((0,v),(1,e),inc) and is_incident((1,e),(2,f),inc) and is_incident((2,f),(3,c),inc)]

def flag_adjacencies(flags,ranks):
 index={f:i for i,f in enumerate(flags)};moves=[]
 for color in range(4):
  m=[]
  for flag in flags:
   cand=[]
   for x in ranks[color]:
    if x!=flag[color]:
     z=list(flag);z[color]=x;z=tuple(z)
     if z in index:cand.append(index[z])
   assert len(cand)==1;m.append(cand[0])
  moves.append(tuple(m))
 return moves

def perm_sign(v,p,eps):
 out=[0]*4
 for i,x in enumerate(v):out[p[i]]=x
 return canon_sign(tuple(eps[i]*out[i] for i in range(4)))

def explicit_automorphisms(ranks,inc):
 nodes=[(r,x) for r in range(4) for x in ranks[r]];maps=[]
 for p in permutations(range(4)):
  for eps in even_full_signs():
   phi={}
   for r,x in nodes:
    if r<3:y=perm_sign(x,p,eps)
    elif x[0]=='H':y=('H',tuple(sorted(p[i] for i in x[1])))
    else:y=('T',perm_sign(x[1],p,eps))
    assert y in ranks[r];phi[(r,x)]=(r,y)
   assert all((phi[lo],phi[hi]) in inc for lo,hi in inc)
   maps.append(phi)
 keys={tuple(phi[n] for n in nodes) for phi in maps}
 assert len(maps)==len(keys)==96
 return maps

def orbit_partition(n,perms):
 unseen=set(range(n));out=[]
 while unseen:
  x=min(unseen);o={p[x] for p in perms};unseen-=o;out.append(sorted(o))
 return sorted(out,key=lambda z:(len(z),z))

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def main():
 ranks,inc=build_poset();flags=flags_of(ranks,inc);moves=flag_adjacencies(flags,ranks);autos=explicit_automorphisms(ranks,inc)
 idx={f:i for i,f in enumerate(flags)};perms=[]
 for phi in autos:perms.append(tuple(idx[tuple(phi[(r,f[r])][1] for r in range(4))] for f in flags))
 orbits=orbit_partition(len(flags),perms);of={f:i for i,o in enumerate(orbits) for f in o}
 action={c:('preserves' if {of[moves[c][f]] for f in orbits[0]}=={0} else 'swaps') for c in range(4)}
 profiles={}
 for c in ranks[3]:profiles[repr(c)]=[sum(is_incident((r,a),(3,c),inc) for a in ranks[r]) for r in range(3)]
 co={repr(f):[c[0] for c in ranks[3] if is_incident((2,f),(3,c),inc)] for f in ranks[2]}
 G=nx.Graph();G.add_nodes_from(range(len(flags)))
 for c,m in enumerate(moves):
  for i,j in enumerate(m):G.add_edge(i,j,color=c)
 counts=[len(ranks[r]) for r in range(4)];tetra_flags=sum(f[3][0]=='T' for f in flags)
 checks={'f_vector_4_12_16_8':counts==[4,12,16,8],'rank_total_40':sum(counts)==40,'four_hemi_cells':sum(c[0]=='H' for c in ranks[3])==4,'four_tetra_cells':sum(c[0]=='T' for c in ranks[3])==4,'hemi_profiles_3_6_4':all(v==[3,6,4] for k,v in profiles.items() if k.startswith("('H'")),'tetra_profiles_4_6_4':all(v==[4,6,4] for k,v in profiles.items() if k.startswith("('T'")),'every_face_one_hemi_one_tetra':all(sorted(v)==['H','T'] for v in co.values()),'flags_192':len(flags)==192,'flag_moves_involutions':all(m[m[f]]==f for m in moves for f in range(len(flags))),'far_colors_commute':all(moves[i][moves[j][f]]==moves[j][moves[i][f]] for i,j in ((0,2),(0,3),(1,3)) for f in range(len(flags))),'flag_graph_connected':nx.is_connected(G),'four_unique_flag_neighbors':all(len({m[f] for m in moves})==4 for f in range(len(flags))),'automorphism_group_96':len(autos)==tetra_flags==96,'two_flag_orbits_96_96':[len(o) for o in orbits]==[96,96],'class_2_012':action=={0:'preserves',1:'preserves',2:'preserves',3:'swaps'},'flag_orbits_are_cell_types':{tuple(sorted({flags[f][3][0] for f in o})) for o in orbits}=={('H',),('T',)}}
 assert all(checks.values()),[k for k,v in checks.items() if not v]
 compact=[[repr(lo),repr(hi)] for lo,hi in sorted(inc,key=repr) if hi[0]==lo[0]+1]
 out={'schema':'w33.bt2810.signed_support_tomotope.v2','status':'COMPLETE_EXACT','theorem':'The tomotope is the parity-twisted signed-support incidence geometry on four coordinates.','f_vector':counts,'rank_total':sum(counts),'cell_types':{'hemioctahedra':4,'tetrahedra':4},'tetrahedral_cell_signs':[list(v) for k,v in ranks[3] if k=='T'],'cell_profile_distribution':{str(k):v for k,v in sorted(Counter(tuple(x) for x in profiles.values()).items())},'rank2_cofacet_type_distribution':{'/'.join(k):v for k,v in sorted(Counter(tuple(sorted(x)) for x in co.values()).items())},'flags':len(flags),'automorphism_group_order':len(autos),'automorphism_proof':'96 explicit even-signed coordinate permutations; an automorphism is determined by the image of one tetrahedral flag, of which there are 96.','flag_orbit_sizes':[len(o) for o in orbits],'color_action_on_flag_orbits':action,'incidence_sha256':digest(compact),'flag_moves_sha256':digest(moves),'checks':checks,'check_count':len(checks),'boundary':'Explicit abstract incidence realization; not a Euclidean realization or continuum-physics theorem.'}
 print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
