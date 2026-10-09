"""F20 quotient/orbifold of genus53 repaired chiral W33 surface.
Compute all 20 group elements on actual 240 vertices, all 136 faces,
the induced global orientation sign, cell orbit sizes and genus2
Riemann-Hurwitz if orientation action preserves surface orientation.
"""
from pathlib import Path
import json,sys,itertools,collections
import networkx as nx
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_twenty_apartment_binary_CSS_F20 import topology
from w33_20261008_F20_A5_600cell_antipodal_bridge import comp,power
OUT=ROOT/"data/w33_20261008_chiral_genus53_F20_orbifold_C5_branching.json"
def main():
 data=json.loads((ROOT/"data/w33_20261008_240chiral_surface_genus_orientability_F20_certificate.json").read_text())
 q=json.loads((ROOT/"data/w33_20261008_W33_to_H4_chiral_4regular_embedding.json").read_text())
 old=json.loads((ROOT/"data/w33_20261008_F20_A5_antipodal_60_bijection.json").read_text())
 V,E,fs,_,_,bx,bz=topology();ix={e:i for i,e in enumerate(E)}
 plus={tuple(sorted(x)) for x in q["selected_H4_plus_W33_edges"]}
 col={tuple(sorted(e)):(1 if tuple(sorted(e)) in plus else 2) for e in q["selected_H4_plus_W33_edges"]+q["selected_H4_minus_W33_edges"]}
 G=nx.Graph();G.add_nodes_from(range(240))
 for (u,v),c in col.items():
  for sh in range(4):G.add_edge(4*u+sh,4*v+(sh^c))
 ed=sorted(tuple(sorted(e)) for e in G.edges());eid={e:i for i,e in enumerate(ed)}
 def walk(seq,sh):
  now=sh;edges=[]
  for u,v in zip(seq,seq[1:]+seq[:1]):
   a=4*u+now;now^=col[tuple(sorted((u,v)))];b=4*v+now
   edges.append(eid[tuple(sorted((a,b)))])
  assert sh==now
  return tuple(edges)
 octs=[]
 for f in fs:
  seq=[ix[tuple(sorted((u,v)))] for u,v in zip(f,f[1:]+f[:1])]
  octs.extend(walk(seq,sh) for sh in range(4))
 hs=[];seen=set()
 for v in V:
  seq=sorted(i for i,e in enumerate(E) if v in e)
  for sh in range(4):
   p=walk(seq+seq,sh)
   if frozenset(p) not in seen:hs.append(p);seen.add(frozenset(p))
 assert len(hs)==80
 covered={i for f in octs for i in f}
 U=nx.Graph();U.add_edges_from(ed[i] for i in range(480) if i not in covered)
 ds=[]
 for c in nx.connected_components(U):
  cc=nx.cycle_basis(U.subgraph(c));assert len(cc)==1
  v=cc[0];ds.append(tuple(eid[tuple(sorted((a,b)))] for a,b in zip(v,v[1:]+v[:1])))
 assert len(ds)==16
 sel=data["selection_results"][0]["selected_octagon_indices"]
 faces=hs+[octs[i] for i in sel]+ds
 assert [len([f for f in faces if len(f)==q]) for q in (6,8,10)]==[80,40,16]
 # Face parity solve from edge direction; returns orientation bit t.
 face_ids={frozenset(f):i for i,f in enumerate(faces)}
 inc=collections.defaultdict(list)
 for i,f in enumerate(faces):
  verts=[]
  for j in range(len(f)):
   cc=set(ed[f[j-1]])&set(ed[f[j]])
   assert len(cc)==1
   verts.append(next(iter(cc)))
  for j,e in enumerate(f):
   direc=int((verts[j],verts[(j+1)%len(f)])!=ed[e])
   inc[e].append((i,direc))
 assert len(inc)==480 and all(len(x)==2 for x in inc.values())
 adj=collections.defaultdict(list)
 for pair in inc.values():
  (i,u),(j,v)=pair;rhs=1^u^v
  adj[i].append((j,rhs));adj[j].append((i,rhs))
 orient={0:0};todo=[0]
 while todo:
  i=todo.pop()
  for j,rhs in adj[i]:
   expect=orient[i]^rhs
   if j in orient:assert orient[j]==expect
   else:orient[j]=expect;todo.append(j)
 assert len(orient)==136
 r=tuple(old["F20_generators_W33_80point_r"]);s=tuple(old["F20_generators_W33_80point_s"])
 def swapbits(k):return ((k&1)<<1)|((k&2)>>1)
 actions={}
 for j in range(4):
  for i in range(5):
   a=comp(power(r,i),power(s,j))
   a60=[ix[tuple(sorted((a[u],a[v])))] for u,v in E]
   a240=[4*a60[v]+(swapbits(k) if j%2 else k) for v in range(60) for k in range(4)]
   perm_edge=[eid[tuple(sorted((a240[u],a240[v])))] for u,v in ed]
   faceperm=[face_ids[frozenset(perm_edge[e] for e in fc)] for fc in faces]
   assert len(set(faceperm))==136
   # For oriented face, transform edge cyclic order, compare with target:
   # same up to rotation versus reversed edge order up to rotation.
   orient_sign=set()
   for fi,fc in enumerate(faces):
    dest=faces[faceperm[fi]]
    x=[perm_edge[e] for e in fc]
    def cyclic_equal(a,b):
     return any(a==list(b[k:]+b[:k]) for k in range(len(b)))
    if cyclic_equal(x,list(dest)):sgn=0
    elif cyclic_equal(x,list(reversed(dest))):sgn=1
    else:raise AssertionError(("image face not cyclic",fi,j,i))
    orient_sign.add(sgn^orient[fi]^orient[faceperm[fi]])
   assert len(orient_sign)==1,orient_sign
   actions[f"r{i}s{j}"]={"faceperm":faceperm,"orientation_reversal":bool(next(iter(orient_sign))),
                            "vertexperm":a240,"edgeperm":perm_edge}
 # Cell orbit enumeration
 def orbits(n,lookup):
  unseen=set(range(n));rr=[]
  while unseen:
   root=min(unseen);o={lookup(a,root) for a in actions.values()}
   assert root in o and o<=unseen
   rr.append(sorted(o));unseen-=o
  return rr
 forc=orbits(136,lambda a,v:a["faceperm"][v])
 vorc=orbits(240,lambda a,v:a["vertexperm"][v])
 eorc=orbits(480,lambda a,v:a["edgeperm"][v])
 assert len(eorc)==24 and all(len(o)==20 for o in eorc)
 oric=collections.Counter(a["orientation_reversal"] for a in actions.values())
 fortype=collections.defaultdict(list)
 for orb in forc:
  fortype[len(faces[orb[0]])].append(len(orb))
 out={"base_surface_genus":53,"Euler_characteristic":-104,
   "F20_group_order":len(actions),
   "orientation_reversing_group_elements":oric.get(True,0),
   "orientation_preserving_group_elements":oric.get(False,0),
   "F20_preserves_orientation":oric.get(True,0)==0,
   "face_orbit_sizes_by_polygon_n":{str(k):sorted(v) for k,v in fortype.items()},
   "vertex_orbit_count":len(vorc),"vertex_orbit_sizes":dict(collections.Counter(len(x) for x in vorc)),
   "edge_orbit_count":len(eorc),"edge_orbit_sizes":dict(collections.Counter(len(x) for x in eorc)),
   "quotient_cell_orbit_f_vector":[len(vorc),len(eorc),len(forc)],
   "quotient_cell_Euler_characteristic":len(vorc)-len(eorc)+len(forc),
   "branch_orbits_faces_with_order5_stabilizer":[orb for orb in forc if len(orb)==4],
   "all_faces_automorphism_action_checked":True,
   "surface_orientation_from_exact_integer_face_boundary":True}
 if out["F20_preserves_orientation"]:
  branch=[20//len(o) for o in forc if len(o)<20]
  out["elliptic_branch_orders"]=sorted(branch)
  n=len(branch)
  fraction=sum((1-1/q) for q in branch)
  qeuler=-104/20+fraction
  out["underlying_orientable_quotient_surface_genus"]=(2-qeuler)/2
  assert abs(qeuler-round(qeuler))<1e-12
  assert out["underlying_orientable_quotient_surface_genus"]==0
  assert sorted(branch)==[2,2,4,4,4,4,5,5,5,5]
  assert out["quotient_cell_orbit_f_vector"]==[12,24,14]
 out["no_Riemann_surface_complex_structure_selected"]=True
 out["cannot_infer_universal_gravitational_or_fermion_coupling_from_orbifold"]=True
 return out
if __name__=="__main__":
 r=main();OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
 print({k:v for k,v in r.items() if k!="branch_orbits_faces_with_order5_stabilizer"},flush=True)
 print("GENUS53_F20_RIEMANN_HURWITZ_ORBIFOLD_PASS")
