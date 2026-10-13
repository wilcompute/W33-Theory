"""TOE62 front2: 4-regular vertex link capacity vs 8-gon spatial CW cells.

Tests a stronger *conditional* no-go with simple vertex links and a
GF2 rank-compatible 81-face subset; not a general manifold obstruction.
"""
from pathlib import Path
from collections import Counter
import sys,json,numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'analysis'))
from w33_20261010_toe38_local_maxwell_2complex import prep,cycle_row
ed,v,lk,octs,comm,*_=prep();E=np.asarray(ed,int)
P=np.rint(np.asarray([cycle_row(x,ed,v,lk,np.zeros(3)).real for x in octs])).astype(int)
assert P.shape==(1382,160)
degree=np.bincount(E.ravel(),minlength=80)
assert np.all(degree==4)
pair_counter=Counter()
per_vertex=Counter()
for row in P:
 support=np.flatnonzero(row)
 assert len(support)==8
 incident=Counter()
 for e in support:
  incident[int(E[e,0])]+=1;incident[int(E[e,1])]+=1
 assert len(incident)==8 and set(incident.values())=={2}
 for z in incident:
  a,b=(int(e) for e in support if z in E[e])
  pair_counter[(z,min(a,b),max(a,b))]+=1
  per_vertex[z]+=1
assert sum(pair_counter.values())==8*1382
# Simple vertex links: at most C(degree(v),2)=6 unique edge pairs at each vertex.
max_total_distinct=int(sum(x*(x-1)//2 for x in degree))
assert max_total_distinct==480
# Each of selected F=8-gons has eight distinct corner positions. If
# link edges cannot repeat at a vertex, 8F<=480 -> F<=60.
max_faces_with_simple_vertex_links=max_total_distinct//8
assert max_faces_with_simple_vertex_links==60
# Euler of closed 3manifold requires C3=80-160+F=F-80, and C3>=1 -> F>=81.
assert 81>max_faces_with_simple_vertex_links
# GF2 row-rank and explicit independent face basis.
basis={};picked=[]
for idx,row in enumerate(P):
 x=0
 for e in np.flatnonzero(row):x^=1<<int(e)
 while x:
  j=x.bit_length()-1
  if j in basis:x^=basis[j]
  else:basis[j]=x;picked.append(idx);break
rank2=len(picked)
assert rank2==78,(rank2,picked[:4])
seed=picked+next([i for i in range(len(P)) if i not in set(picked)][s:s+3] for s in [0])
assert len(seed)==81
subset_pairs=Counter()
for idx in seed:
 row=P[idx];sup=np.flatnonzero(row)
 for z in set(map(int,E[sup].ravel())):
  incident=[int(e) for e in sup if z in E[e]]
  assert len(incident)==2
  subset_pairs[(z,*sorted(incident))]+=1
repeats=sum(v-1 for v in subset_pairs.values())
assert repeats>=8*81-480 # at least 168 pair repeats
out={'status':'PASS_TOE62_SIMPLE_VERTEX_LINK_W33_NO_GO',
'native_graph':{'vertices':80,'edges':160,'all_degree':4,'octagon_faces':1382,
                'each_face_length':8,'GF2_boundary_rank':rank2},
'unique_possible_edge_pairs_across_vertices':max_total_distinct,
'max_faces_if_simple_vertex_link':max_faces_with_simple_vertex_links,
'closed_manifold_min_faces_from_Euler_and_nonempty_3cells':81,
'eight_one_face_independent_subset':{'indices':seed,'face_count':len(seed),
                                    'GF2_boundary_rank':rank2,
                                    'repeated_vertex_edge_pairs':repeats},
'native_all_octagon_pair_multiplicities':dict(Counter(pair_counter.values())),
'theorem':"With unaltered native simple 4-regular 80-vertex/160-edge graph, an embedded regular CW 3-manifold in which each vertex link has at most one link edge per unordered pair of incident graph edges admits at most 80*C(4,2)/8=60 regular eight-sided 2-faces. But closed-manifold Euler chi=0 and at least one 3-cell require F>=E-V+1=81. Contradiction for ANY selected subset of existing regular octagons. This strengthens TOE61's keeping-all-faces obstruction but depends crucially on SIMPLE vertex links. An explicit 81-face GF2-rank78 subset already repeats edge pairs.",
'limitations':"A regular CW manifold's vertex link need NOT be a simple graph: it may have parallel edges, e.g. non-simplicial/curved cellulations. Thus this is NOT an unconditional no-go for ALL regular CW manifolds; subdivision, dual 1-skeleton, non-simple links and additional vertices/edges remain possible. GF2 rank78 does not prove correct integral homology, cup products, local sphere links, manifold orientation or a built 3-cell."}
(R/'data/w33_20261013_toe62_vertex_links.json').write_text(json.dumps(out,indent=2)+'\n')
print('TOE62 topological',rank2,len(seed),repeats,'maxfaces',max_faces_with_simple_vertex_links)
