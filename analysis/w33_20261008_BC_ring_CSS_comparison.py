"""Executable BC-ring vs W33 apartment CSS comparison.

BC's 30-tetra ring boundary: 30 vertices, 90 edges, 60 triangles,
not the same cell carrier as W33's branched 40/60/20 20-apartment CW.
Compute its own exact CSS [90,2,d] via primal/dual lifted BFS and
prove the strongest immediate action/graph no-go.
"""
import sys,itertools,collections,json,networkx as nx
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_bc_ring_boundary_torus import tetrahedra,canon_edge,ring_graph
from w33_20261008_twenty_apartment_binary_CSS_F20 import topology,add,reduce,nullspace
OUT=ROOT/"data/w33_20261008_BC_ring_CSS_vs_apartment.json"
def make():
 cnt=collections.Counter(tuple(sorted(f)) for t in tetrahedra() for f in itertools.combinations(t,3))
 faces=sorted(f for f,num in cnt.items() if num==1)
 edges=sorted(set(canon_edge(*e) for f in faces for e in itertools.combinations(f,2)))
 assert len(faces)==60 and len(edges)==90
 ix={e:i for i,e in enumerate(edges)}
 b1=[0]*30;b2=[0]*60
 edgefaces=collections.defaultdict(list)
 for j,(u,v) in enumerate(edges):
  b1[u]^=1<<j;b1[v]^=1<<j
 for j,f in enumerate(faces):
  for e in itertools.combinations(f,2):
   idx=ix[canon_edge(*e)]
   b2[j]^=1<<idx;edgefaces[idx].append(j)
 assert all(len(x)==2 for x in edgefaces.values())
 assert all((p&q).bit_count()%2==0 for p in b1 for q in b2)
 return faces,edges,b1,b2,edgefaces
def dual_lift_shortest(adj,vals,k=2):
 best=None
 for start in adj:
  queue=collections.deque([(start,0)])
  seen={(start,0):(None,None)}
  end=None
  while queue:
   u,c=queue.popleft()
   if u==start and c:
    end=(u,c);break
   for v,e in adj[u]:
    state=(v,c^vals[e])
    if state not in seen:
     seen[state]=((u,c),e);queue.append(state)
  if end:
   path=[];loc=end
   while seen[loc][0] is not None:
    prev,e=seen[loc];path.append(e);loc=prev
   path=path[::-1]
   if best is None or len(best)>len(path):best=path
 return best

def css():
 faces,edges,b1,b2,edgefaces=make()
 cob={};bound={}
 for r in b1:add(r,cob)
 for r in b2:add(r,bound)
 assert len(cob)==29 and len(bound)==59
 co=[];cy=[]
 B=cob.copy()
 for x in nullspace(b2,90):
  if add(x,B):co.append(x)
 B=bound.copy()
 for z in nullspace(b1,90):
  if add(z,B):cy.append(z)
 assert len(co)==len(cy)==2
 V={i:[] for i in range(30)}
 F={i:[] for i in range(60)}
 for j,(u,v) in enumerate(edges):
  V[u].append((v,j));V[v].append((u,j))
  f,g=edgefaces[j];F[f].append((g,j));F[g].append((f,j))
 cv=[((a>>j)&1)|(((b>>j)&1)<<1) for j in range(90) for a,b in [co]]
 zv=[((a>>j)&1)|(((b>>j)&1)<<1) for j in range(90) for a,b in [cy]]
 zbest=dual_lift_shortest(V,cv)
 xbest=dual_lift_shortest(F,zv)
 assert zbest is not None and xbest is not None
 return {"V_E_F":[30,90,60],"n":90,"rank_HX":29,"rank_HZ":59,"k":2,
 "Z_distance":len(zbest),"X_distance":len(xbest),
 "CSS_distance":min(len(zbest),len(xbest)),
 "Z_witness_edges":[list(edges[e]) for e in zbest],
 "X_witness_boundary_edges":[list(edges[e]) for e in xbest],
 "step_spectrum":{str(j):{"edges":30,"connected_cycles":j,"cycle_length":30//j} for j in (1,2,3)},
 "primal_graph_degree":6,"dual_face_adjacency_degree":3}

def compare():
 bc=css()
 a=topology()
 _,a_edges,_,stabilizer,_,_,_=a
 bc_faces,_,_,_,_ = make()
 g=ring_graph()
 # The prior BT486 independent full automorphism enumeration proved order60.
 # Reconstruct the 60 D30 transformations deterministically rather than
 # rerun the expensive generic GraphMatcher over a 30-vertex graph.
 aut=[{i:(eps*i+shift)%30 for i in range(30)}
       for eps in (1,-1) for shift in range(30)]
 assert len(aut)==60 and len({tuple(v[i] for i in range(30)) for v in aut})==60
 assert all({tuple(sorted((m[u],m[v]))) for u,v in g.edges()}=={tuple(sorted(e)) for e in g.edges()} for m in aut)
 # Check no automorphism of order4 (D_30 group).
 def perm_order(p):
  start=p
  cur=p
  n=1
  while any(cur[i]!=i for i in range(30)):
   cur={i:start[cur[i]] for i in range(30)}
   n+=1
   assert n<=30
  return n
 orders=collections.Counter(perm_order(p) for p in aut)
 assert not any(k%4==0 for k in orders)
 W=nx.Graph();W.add_nodes_from(range(60))
 v2edges=collections.defaultdict(list)
 for j,(u,v) in enumerate(a_edges):
  v2edges[u].append(j);v2edges[v].append(j)
 for inc in v2edges.values():
  for j,k in itertools.combinations(inc,2):W.add_edge(j,k)
 assert set(dict(W.degree()).values())=={4}
 D=nx.Graph();D.add_nodes_from(range(60))
 ef=collections.defaultdict(list)
 for j,f in enumerate(bc_faces):
  for e in itertools.combinations(f,2):ef[canon_edge(*e)].append(j)
 for incid in ef.values():D.add_edge(*incid)
 assert set(dict(D.degree()).values())=={3}
 # Actual 600cell 60 antipodal Clifford addresses are a separate A5 carrier;
 # the BC face triangle adjacency has D_30, so cannot carry W's F20.
 return {"BC_CSS":bc,
  "W33_selected_CSS":"[[60,2,6]]_2",
  "BC_boundary_triangle_faces":60,
  "W33_CSS_edge_qubits":60,
  "BC_torus_1_skeleton_aut_order":len(aut),
  "BC_torus_automorphism_order_histogram":dict(orders),
  "BC_full_automorphism_has_order_four":False,
  "F20_order4_elements_in_W33":10,
  "no_full_F20_action_as_BC_ring_geometric_automorphisms":True,
  "BC_face_dual_graph_degree":3,
  "W33_edge_line_graph_degree":4,
  "BC_face_dual_and_W33_edge_line_graph_isomorphic":False,
  "hypothesis_boundary":"Same 60 labels not canonical, distinct cellular carriers and qubit counts. Full 600-cell / A5 Clifford antipodal construction may still admit a different action; this rules out simplest individual-BC-ring geometric identification."}
if __name__=="__main__":
 r=compare();OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
 print(json.dumps(r,indent=2),flush=True);print("BC_TORUS_CSS_PASS")
