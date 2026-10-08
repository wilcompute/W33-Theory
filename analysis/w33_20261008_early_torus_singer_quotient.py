"""Early-torus crosswalk: quotient chosen 20 W33 octagons by its actual Singer C5.

Prior owners: Mar 9 torus heat-trace (EXTERNAL 4D), May Csaszar/Szilassi,
June BT790 5400 seven-skew-line cells. This C5 CW quotient is NEW, not a
claim that those older objects and the 20 W33 apartments are identical.
"""
import itertools,json,collections,sys
from pathlib import Path
import networkx as nx
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
from w33_20261008_five_physics_frontiers import projective_points_and_lines
from w33_20261008_dual_27_electrical_transport import normalize,pairing
from w33_20261008_global_cycle_center_census import cycles
from w33_pass607_johnson_clique_pi1 import tietze_eliminate,free_reduce
D=R/"data";OUT=D/"w33_20261008_early_torus_singer_quotient.json"

def objects():
 pts,lines=projective_points_and_lines();pi={v:i for i,v in enumerate(pts)}
 lin={frozenset(L):i for i,L in enumerate(lines)}
 vs=[(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,1,0,0),(1,0,1,0),(1,1,1,1)]
 gg=[tuple(pi[normalize(tuple((x[i]+pairing(x,v)*v[i])%3 for i in range(4)))] for x in pts) for v in vs]
 I=tuple(range(40));G={I};queue=[I]
 def prod(a,b):return tuple(a[b[i]] for i in range(40))
 for a in queue:
  for b in gg:
   c=prod(a,b)
   if c not in G:G.add(c);queue.append(c)
 assert len(G)==25920
 C=cycles();a=json.loads((D/"w33_20261008_cycle_center_atlas_constructive.json").read_text());b=json.loads((D/"w33_20261008_cycle_atlas_homology_rank.json").read_text())
 selected=[tuple(C[c]) for c,k in zip(a["largest_found_cycle_indices"],b["primitive_integral_relation_coefficients"]) if k]
 face_set=set(map(frozenset,selected));assert len(face_set)==20
 def induced(g):
  lperm=[lin[frozenset(pts[g[pi[x]]] for x in line)] for line in lines]
  return g+tuple(40+x for x in lperm)
 stabilizer=[]
 for g in G:
  h=induced(g)
  if all(frozenset(h[x] for x in face) in face_set for face in face_set):stabilizer.append(h)
 assert len(stabilizer)==20
 def order(g):
  p=tuple(range(80));n=0
  while True:
   p=tuple(p[g[i]] for i in range(80));n+=1
   if all(i==p[i] for i in range(80)):return n
 generator=next(g for g in stabilizer if order(g)==5)
 powers=[tuple(range(80))]
 for i in range(4):
  x=powers[-1];powers.append(tuple(x[generator[t]] for t in range(80)))
 assert len(set(powers))==5
 return C, selected,stabilizer,powers

def orbit_partition(items, group, act):
 universe=set(items);orbits=[]
 while universe:
  seed=next(iter(universe));orb={act(g,seed) for g in group}
  assert orb<=universe
  orbits.append(orb);universe-=orb
 return orbits

def main():
 C,faces,stabilizer,H=objects()
 V=set(v for f in faces for v in f)
 E=set(tuple(sorted((u,v))) for f in faces for u,v in zip(f,f[1:]+f[:1]))
 F=set(map(frozenset,faces));assert (len(V),len(E),len(F))==(40,60,20)
 orbV=orbit_partition(V,H,lambda g,v:g[v])
 orbE=orbit_partition(E,H,lambda g,e:tuple(sorted((g[e[0]],g[e[1]]))))
 orbF=orbit_partition(F,H,lambda g,f:frozenset(g[v] for v in f))
 assert len(orbV)==8 and len(orbE)==12 and len(orbF)==4
 assert all(len(o)==5 for o in orbV+orbE+orbF)
 vmap={v:i for i,o in enumerate(orbV) for v in o}
 emap={e:i for i,o in enumerate(orbE) for e in o}
 Fseq=[next(tuple(f) for f in faces if frozenset(f) in orbit) for orbit in orbF]
 # Compute integral quotient boundaries with orientation by point -> line.
 vrep=[next(iter(o)) for o in orbV]
 erep=[next(iter(o)) for o in orbE]
 B1=sp.zeros(8,12);B2=sp.zeros(12,4)
 for j,(u,v) in enumerate(erep):
  assert (u<40)!=(v<40)
  B1[vmap[u],j]+=1 if u>=40 else -1
  B1[vmap[v],j]+=1 if v>=40 else -1
 for k,f in enumerate(Fseq):
  for u,v in zip(f,f[1:]+f[:1]):
   B2[emap[tuple(sorted((u,v)))],k]+=1 if u<40 else -1
 assert B1*B2==sp.zeros(8,4)
 sv1=smith_normal_form(B1,domain=ZZ);sv2=smith_normal_form(B2,domain=ZZ)
 ds1=[abs(int(sv1[i,i])) for i in range(min(sv1.shape)) if sv1[i,i]]
 ds2=[abs(int(sv2[i,i])) for i in range(min(sv2.shape)) if sv2[i,i]]
 ranks=[len(ds1),len(ds2)];betti=[8-ranks[0],12-sum(ranks),4-ranks[1]]
 # Actual pi1 from quotient CW cellular edge/face attaching words.
 adj={i:[] for i in range(8)}
 for j,(u,v) in enumerate(erep):
  x,y=vmap[u],vmap[v]
  adj[x].append((y,j));adj[y].append((x,j))
 tree=set();queue=[0];seen={0}
 for x in queue:
  for y,j in sorted(adj[x]):
   if y not in seen:seen.add(y);queue.append(y);tree.add(j)
 assert len(tree)==7
 non=[j for j in range(12) if j not in tree]; eid={j:i+1 for i,j in enumerate(non)}
 words=[]
 for f in Fseq:
  letters=[]
  for x,y in zip(f,f[1:]+f[:1]):
   e=tuple(sorted((x,y)));j=emap[e]
   if j in eid:letters.append(eid[j] if x<40 else -eid[j])
  words.append(free_reduce(letters))
 active,rels,steps,digest,_=tietze_eliminate(words,len(non))
 Q=nx.Graph()
 Q.add_nodes_from(range(8))
 Q.add_edges_from((vmap[u],vmap[v]) for u,v in erep)
 simple_edges=Q.number_of_edges()
 cube_isomorphism=nx.is_isomorphic(Q,nx.hypercube_graph(3))
 c8_isomorphism=nx.is_isomorphic(Q,nx.cycle_graph(8))
 parallel=collections.Counter(tuple(sorted((vmap[u],vmap[v]))) for u,v in erep)
 doubled={x for x,m in parallel.items() if m==2}
 assert c8_isomorphism and len(doubled)==4 and len({v for edge in doubled for v in edge})==8
 print("QUOTIENT_SIMPLE_EDGES",simple_edges,"CUBE",cube_isomorphism,"MULTIEDGE_HIST",dict(collections.Counter(parallel.values())),flush=True)
 face_cycles=[tuple(vmap[x] for x in f) for f in Fseq]
 print("QUOTIENT_FACE_DISTINCT_VERTEX_COUNTS",[len(set(f)) for f in face_cycles],flush=True)
 # Quotient face walks need not be simple Hamiltonian cube cycles.
 edge_face=collections.Counter()
 for f in face_cycles:
  for x,y in zip(f,f[1:]+f[:1]):edge_face[tuple(sorted((x,y)))]+=1
 print("QUOTIENT_FACE_EDGE_MULT",dict(collections.Counter(edge_face.values())),flush=True)
 # Orientation action on full 20-face homology fundamental signed relation:
 # some order4 symmetries may flip orientation.
 weights=json.loads((D/"w33_20261008_cycle_atlas_homology_rank.json").read_text())["primitive_integral_relation_coefficients"]
 full=json.loads((D/"w33_20261008_cycle_center_atlas_constructive.json").read_text())["largest_found_cycle_indices"]
 signs={frozenset(C[c]):k for c,k in zip(full,weights) if k}
 orientation=collections.Counter()
 for g in stabilizer:
  s=None
  for f in F:
   t=frozenset(g[x] for x in f)
   sign=signs[t]*signs[f]
   if s is None:s=sign
   # orientation caveat: each face's fixed stored cycle orientation may
   # have its boundary reversed under g, so do not assert support-sign alone.
  orientation[s]+=1
 out={"context":{"earliest_external_torus_refinement_commit":"589d3069f (2026-03-09)",
     "Csaszar_Szilassi_edge_parser":"a2c43a398 (2026-05-18)",
     "BT796_June_2026_5400_skew_line_cells":"different carrier: seven mutually skew W33 lines, not Levi 20-apartment CW complex"},
      "singer_C5_free_cell_action":True,
      "original_CW_cells":[40,60,20],
      "C5_quotient_cells":[len(orbV),len(orbE),len(orbF)],
      "C5_quotient_euler":len(orbV)-len(orbE)+len(orbF),
      "C5_quotient_1_skeleton_is_three_cube_Q3":cube_isomorphism,
      "C5_quotient_simple_underlying_graph_is_C8":c8_isomorphism,
      "C5_quotient_double_edges_form_perfect_matching_on_C8":True,
      "C5_quotient_simple_graph_edges":simple_edges,
      "C5_quotient_parallel_edge_multiplicity_histogram":dict(collections.Counter(parallel.values())),
      "C5_quotient_four_octagon_attaching_cycles_are_Hamiltonian_on_Q3":cube_isomorphism and all(len(set(f))==8 for f in face_cycles),
      "C5_quotient_octagon_edge_face_multiplicities":dict(collections.Counter(edge_face.values())),
      "C5_quotient_C8_face_vertex_walks":[list(f) for f in face_cycles],
      "quotient_smith_d1":ds1,"quotient_smith_d2":ds2,
      "quotient_integral_betti":betti,
      "quotient_H1_torsion_invariants":[x for x in ds2 if x!=1],
      "quotient_pi1_presentation_initial_generators":len(non),
      "quotient_pi1_presentation_initial_relators":len(words),
      "quotient_pi1_post_elimination_generators":len(active),
      "quotient_pi1_post_elimination_relators":[list(x) for x in rels],
      "quotient_pi1_remaining_generator_ids":sorted(active),
      "quotient_tietze_eliminations":len(steps),
      "quotient_tietze_sha256":digest,
      "C5_orbit_representative_vertices":vrep,
      "C5_orbit_representative_edges":[list(x) for x in erep],
      "C5_quotient_attaching_words":[list(x) for x in words],
      "quotient_is_Csaszar_or_Szilassi":False,
      "CW_physical_geometry_claim":"Finite topological quotient, no length metric, no explicit geometric embedding or spacetime action"}
 return out
if __name__=="__main__":
 d=main();OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
 print({k:v for k,v in d.items() if k not in ("C5_orbit_representative_vertices","C5_orbit_representative_edges","C5_quotient_attaching_words")},flush=True)
 print("SINGER_QUOTIENT_PASS",flush=True)
