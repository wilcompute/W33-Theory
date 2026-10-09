"""Native 600-cell no-go over ALL 120 perfect F20-equivariant selectors.

Enumerate original 48k F20-set bijections; among the 120 preserving all
W33 qubit adjacencies in the two-class H4 order-5 union, test whether
each W33 octagon travels entirely along actual 600-cell native + edges.
Count 0/8 and the full octagon plus-edge hist for all perfect selectors.
"""
import sys,json,itertools,collections
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_twenty_apartment_binary_CSS_F20 import topology
from w33_20261008_F20_A5_600cell_antipodal_bridge import comp,power,order
from w33_20261008_W33_H4_chiral_4regular_embedding import group_isomorphism
from w33_clifford_antipodal_a5_selector_group import clifford_antipodal_permutations,inverse
OUT=ROOT/"data/w33_20261008_all120_perfect_F20_selectors_native_H4_face_nogo.json"
def main():
 V,E,faces,stab,H,b1,b2=topology()
 old=json.loads((ROOT/"data/w33_20261008_F20_A5_antipodal_60_bijection.json").read_text())
 ch=json.loads((ROOT/"data/w33_20261008_H4_A5_chiral_5cycle_normal_Cayley.json").read_text())
 cos=[tuple(x) for x in old["S5_coset_representatives"]];even=[tuple(x) for x in old["S5_coset_even_A5_permutations"]]
 five=set(even);six=clifford_antipodal_permutations()
 iso=group_isomorphism(five,set(six.values()))
 pos={tuple(a) for a in ch["A5_neighbor_identity_permutations"]}
 P=np.zeros((60,60),dtype=np.uint8);S=np.zeros((60,60),dtype=np.uint8)
 for a in range(60):
  for b in range(a+1,60):
   rel=comp(inverse(iso[even[a]]),iso[even[b]])
   if order(rel)==5:
    S[a,b]=S[b,a]=1
    if rel in pos:P[a,b]=P[b,a]=1
 assert set(P.sum(axis=1))=={12} and set(S.sum(axis=1))=={24}
 r=tuple(old["F20_generators_W33_80point_r"]);s=tuple(old["F20_generators_W33_80point_s"])
 rs=tuple(old["F20_generator_S5_r"]);ss=tuple(old["F20_generator_S5_s"])
 group=[comp(power(r,i),power(s,j)) for j in range(4) for i in range(5)]
 embed={g:comp(power(rs,i),power(ss,j)) for j in range(4) for i in range(5) for g in [comp(power(r,i),power(s,j))]}
 index={c:i for i,c in enumerate(cos)}
 t=(1,0,2,3,4);normal=lambda p:min(p,comp(p,t))
 eidx={e:i for i,e in enumerate(E)}
 wact={g:[eidx[tuple(sorted((g[u],g[v])))] for u,v in E] for g in group}
 cact={g:[index[normal(comp(embed[g],c))] for c in cos] for g in group}
 def orb(act):
  rem=set(range(60));out=[]
  while rem:
   root=min(rem);o={act[g][root] for g in group}
   assert len(o)==20
   out.append(sorted(o));rem-=o
  return out
 W=orb(wact);C=orb(cact)
 anchors={}
 for k,wo in enumerate(W):
  for j,co in enumerate(C):
   arr=[]
   for c0 in co:
    m={wact[g][wo[0]]:cact[g][c0] for g in group}
    arr.append([m[u] for u in wo])
   anchors[k,j]=np.array(arr,dtype=np.int16)
 adj=set()
 for v in V:
  inc=[i for i,e in enumerate(E) if v in e]
  for a,b in itertools.combinations(inc,2):adj.add(tuple(sorted((a,b))))
 a,b=np.array(sorted(adj)).T
 farr=[]
 for f in faces:
  es=[eidx[tuple(sorted((u,v)))] for u,v in zip(f,f[1:]+f[:1])]
  farr.extend((u,v) for u,v in zip(es,es[1:]+es[:1]))
 fa,fb=np.array(farr).T
 assert len(farr)==160
 hists=collections.Counter();native_all=collections.Counter();perfect=0
 max_faces=0;all_face_counts=[];five_witness=None
 for targ in itertools.permutations(range(3)):
  for h in itertools.product(range(20),repeat=3):
   m=np.empty(60,dtype=np.int16)
   for k in range(3):m[W[k]]=anchors[k,targ[k]][h[k]]
   if int(S[m[a],m[b]].sum())!=120:continue
   perfect+=1
   native_counts=P[m[fa],m[fb]].reshape((20,8)).sum(axis=1)
   assert np.all(np.isin(native_counts,[0,2,4,6,8]))
   k=int((native_counts==8).sum())
   if k==5 and five_witness is None:
    five_witness={"coset_address_map_W33_60qubits":m.tolist(),"native_face_indices":[int(i) for i,c in enumerate(native_counts) if c==8],"native_face_plus_count_per_20faces":native_counts.tolist()}
   max_faces=max(max_faces,k);native_all[k]+=1
   hists[tuple(sorted(collections.Counter(native_counts.tolist()).items()))]+=1
   all_face_counts.append(native_counts.tolist())
 assert perfect==120
 return {"all_F20_bijections_examined":48000,
  "perfect_pair_union_embedding_selectors":perfect,
  "native_H4_plus_degree":12,
  "perfect_selectors_by_number_of_all_native_8edge_Z_octagons":dict(native_all),
  "maximum_native_octagonal_check_supports_for_any_perfect_selector":max_faces,
  "per_selector_face_pluscount_histogram_type":{str(k):v for k,v in hists.items()},
  "all_perfect_selectors_face_native_edge_counts":all_face_counts,
  "first_five_face_native_selector":five_witness,
  "all_20_octagon_CW_supports_realized_natively_simultaneously":False,
  "not_ruling_out_non_F20_or_different_chiral_H4_relations":True,
  "boundary":"The test addresses native original H4 + graph adjacency, not the synthetic mirror - relation; it rules out a native edgewise embedding for all perfect selectors in this fixed equivariant family only."}
if __name__=="__main__":
 x=main();OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
 print({k:v for k,v in x.items() if k!="all_perfect_selectors_face_native_edge_counts"},flush=True)
 print("ALL_120_PERFECT_NATIVE_H4_CW_SELECTOR_CENSUS_DONE")
