"""Exhaust all 3!*(20!)? NO: 3! * 20^3 = 48,000 F20-equivariant
60-address bijections between W33 edge-qubit and S5/C2 Clifford-A5 torsor.

Ask whether *every* degree4 W33 edge-line adjacency can land in the
natural degree24 A5 order-five union of the two actual 600cell H4
chiral Cayley graphs. Testing 48k valid equivariant maps, not 60!.
"""
import sys,json,itertools,collections,numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_twenty_apartment_binary_CSS_F20 import topology
from w33_20261008_F20_A5_600cell_antipodal_bridge import comp,power,order
OUT=ROOT/"data/w33_20261008_F20_48000_selectors_chiral_union_census.json"
def main():
 V,E,F,stab,H,b1,b2=topology()
 old=json.loads((ROOT/"data/w33_20261008_F20_A5_antipodal_60_bijection.json").read_text())
 init=np.array(old["W33_edge_index_to_S5_coset_index"])
 cos=[tuple(x) for x in old["S5_coset_representatives"]]
 evens=[tuple(x) for x in old["S5_coset_even_A5_permutations"]]
 ix={e:i for i,e in enumerate(E)}
 wact={g:[ix[tuple(sorted((g[u],g[v])))] for u,v in E] for g in stab}
 # S5 action: F20 generator normal form from previous certificate.
 r=tuple(old["F20_generators_W33_80point_r"])
 s=tuple(old["F20_generators_W33_80point_s"])
 rs=tuple(old["F20_generator_S5_r"]);ss=tuple(old["F20_generator_S5_s"])
 group=[comp(power(r,i),power(s,j)) for j in range(4) for i in range(5)]
 embed={g:comp(power(rs,i),power(ss,j)) for j in range(4) for i in range(5) for g in [comp(power(r,i),power(s,j))]}
 cosix={a:i for i,a in enumerate(cos)}
 t=(1,0,2,3,4)
 normal=lambda p:min(p,comp(p,t))
 cact={g:[cosix[normal(comp(embed[g],a))] for a in cos] for g in group}
 def orbits(act):
  rest=set(range(60));out=[]
  while rest:
   root=min(rest);oo={act[g][root] for g in group}
   assert len(oo)==20
   out.append(sorted(oo));rest-=oo
  return out
 W=orbits(wact);C=orbits(cact)
 assert len(W)==len(C)==3 and sorted(sum(W,[]))==list(range(60))
 assert sorted(sum(C,[]))==list(range(60))
 anchors={}
 for k,w in enumerate(W):
  src=w[0]
  for j,targ in enumerate(C):
   imgs=[]
   for c0 in targ:
    m={wact[g][src]:cact[g][c0] for g in group}
    assert len(m)==20
    imgs.append([m[u] for u in w])
   anchors[k,j]=np.array(imgs,dtype=np.int16)
 # Order-five relation on coset labels: a^-1 b has order5.
 S=np.zeros((60,60),dtype=np.uint8)
 def inverse(p):
  inv=[0]*len(p)
  for i,v in enumerate(p):inv[v]=i
  return tuple(inv)
 for u in range(60):
  for v in range(u+1,60):
   if order(comp(inverse(evens[u]),evens[v]))==5:
    S[u,v]=S[v,u]=1
 assert all(S.sum(axis=1)==24)
 # This 24-degree class union is preserved by F20 on coset action:
 assert all(S[np.ix_(cact[g],cact[g])].tolist()==S.tolist() for g in group)
 edges=set()
 for star in range(40):
  points=[i for i,row in enumerate(b1) if i==star]
  inc=[j for j,e in enumerate(E) if V[star] in e]
  assert len(inc)==3
  for x,y in itertools.combinations(inc,2):edges.add(tuple(sorted((x,y))))
 assert len(edges)==120
 a,b=np.array(sorted(edges),dtype=int).T
 peak=-1;best=None;hist=collections.Counter()
 for targets in itertools.permutations(range(3)):
  for h0,h1,h2 in itertools.product(range(20),repeat=3):
   mapped=np.empty(60,dtype=np.int16)
   for k,h in enumerate((h0,h1,h2)):
    mapped[W[k]]=anchors[k,targets[k]][h]
   matched=int(S[mapped[a],mapped[b]].sum())
   hist[matched]+=1
   if matched>peak:
    peak=matched;best=(targets,(h0,h1,h2),mapped.tolist())
 assert sum(hist.values())==48000
 return {"F20_equivariant_60_address_bijections_exhausted":48000,
   "H4_chiral_pair_union_A5_order5_degree":24,
   "W33_edge_qubit_line_adjacency_degree":4,
   "W33_edge_line_adjacency_edge_count":120,
   "highest_W33_edges_respecting_H4_chiral_pair_union":peak,
   "full_edge_containment_achieved":peak==120,
   "best_orbit_permutation":list(best[0]),
   "best_three_anchor_translation_indices":list(best[1]),
   "best_map_W33_to_A5_coset_index":best[2],
   "intersection_size_histogram":dict(sorted(hist.items())),
   "boundary":"All 48,000 F20-equivariant bijections for one fixed F20 identification tested; other non-equivariant maps and different H4 relations are not excluded. The H4 union adjacency is an order-five relation, not a physical chiral gate."}
if __name__=="__main__":
 x=main();OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
 print({k:v for k,v in x.items() if k not in ("best_map_W33_to_A5_coset_index","intersection_size_histogram")},flush=True)
 print("F20_48000_CHIRAL_SELECTOR_CENSUS_PASS")
