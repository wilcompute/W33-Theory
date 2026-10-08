"""Explicit F20-equivariant bijection: W33 60 edge qubits <-> A5 60 torsor.

The Clifford antipodal 600-cell catalogue independently identifies its
60 addresses with A5. This constructs an ABSTRACT F20-set equivalence to
S5/<odd transposition> ~= A5; the coset model realizes F20=AGL(1,5)
inside S5, which acts freely on the 60 cosets in three 20-orbits.
No geometric 600-cell edge/BC-helix incidence is transported.
"""
import itertools,collections,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_twenty_apartment_binary_CSS_F20 import topology
OUT=ROOT/"data/w33_20261008_F20_A5_antipodal_60_bijection.json"
def comp(a,b):return tuple(a[b[i]] for i in range(len(a)))
def power(a,k):
 p=tuple(range(len(a)))
 for _ in range(k):p=comp(a,p)
 return p
def parity(p):return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2
def order(p):
 I=tuple(range(len(p)));q=I
 for n in range(1,33):
  q=comp(p,q)
  if q==I:return n
 raise ValueError
def main():
 V,E,F,stab,H,b1,b2=topology()
 I80=tuple(range(80));r=H[1]
 assert order(r)==5
 r2=power(r,2)
 s=next(g for g in stab if order(g)==4 and comp(comp(g,r),power(g,3))==r2)
 G={}
 for j in range(4):
  for i in range(5):
   p=comp(power(r,i),power(s,j));G[p]=(i,j)
 assert len(G)==20 and set(G)==set(stab)
 # Canonical AGL_1(F5) group embedded as affine permutations in S5.
 rs=tuple((i+1)%5 for i in range(5))
 ss=tuple((2*i)%5 for i in range(5))
 assert order(rs)==5 and order(ss)==4 and comp(comp(ss,rs),power(ss,3))==power(rs,2)
 emap={g:comp(power(rs,i),power(ss,j)) for g,(i,j) in G.items()}
 assert len(set(emap.values()))==20
 # S5/<t> right cosets; left S5 action.
 t=(1,0,2,3,4)
 allp=list(itertools.permutations(range(5)))
 co=lambda p:min(p,comp(p,t))
 cos=sorted({co(p) for p in allp})
 assert len(cos)==60
 cindex={p:i for i,p in enumerate(cos)}
 cact={g:[cindex[co(comp(emap[g],p))] for p in cos] for g in stab}
 eidx={e:i for i,e in enumerate(E)}
 wact={g:[eidx[tuple(sorted((g[u],g[v])))] for u,v in E] for g in stab}
 def orbits(points,action):
  rem=set(points);out=[]
  while rem:
   seed=min(rem);o={action[g][seed] for g in stab}
   assert o<=rem
   out.append(sorted(o));rem-=o
  return out
 ow=orbits(range(60),wact);oc=orbits(range(60),cact)
 assert [len(o) for o in ow]==[20]*3
 assert [len(o) for o in oc]==[20]*3
 mapping=[None]*60
 for wc,cc in zip(ow,oc):
  for g in stab:
   i=wact[g][wc[0]];j=cact[g][cc[0]]
   if mapping[i] is not None:assert mapping[i]==j
   mapping[i]=j
 assert len(set(mapping))==60
 for g in stab:
  for i in range(60):assert mapping[wact[g][i]]==cact[g][mapping[i]]
 # Pick the even member of each coset as the A5 group address.
 A5=[]
 for u in cos:
  c=(u,comp(u,t))
  even=next(p for p in c if parity(p)==0)
  A5.append(even)
 assert len(set(A5))==60
 orders=collections.Counter(order(p) for p in A5)
 assert orders=={1:1,2:15,3:20,5:24}
 # Read the actual 60 Clifford addresses and verify they form same A5
 # abstract order spectrum, without selecting a canonical geometry.
 from w33_clifford_antipodal_a5_selector_group import clifford_antipodal_permutations,permutation_order
 sample=clifford_antipodal_permutations()
 assert len(sample)==60
 orders_cl=collections.Counter(permutation_order(p) for p in sample.values())
 assert orders_cl==orders
 return {
  "W33_CSS_edge_qubits":60,"W33_F20_edge_orbit_sizes":[len(o) for o in ow],
  "S5_order":120,"S5_odd_transposition_cosets":60,
  "F20_normalizer_of_C5_in_S5":True,
  "S5_coset_F20_orbit_sizes":[len(o) for o in oc],
  "S5_coset_stabilizer_is_odd_transposition":True,
  "S5_coset_A5_even_member_unique":True,
  "abstract_A5_order_hist":dict(orders),
  "600cell_Clifford_A5_order_hist_from_actual_repo":dict(orders_cl),
  "F20_equivariant_bijection_verified_for_all_1200_edge_group_pairs":True,
  "W33_edge_index_to_S5_coset_index":mapping,
  "S5_coset_even_A5_permutations":[list(p) for p in A5],
  "S5_coset_representatives":[list(p) for p in cos],
  "F20_generators_W33_80point_r":list(r),
  "F20_generators_W33_80point_s":list(s),
  "F20_generator_S5_r":list(rs),"F20_generator_S5_s":list(ss),
  "noncanonical_choices":3,
  "canonical_geometry_proven":False,
  "invariant_boundary":"Equivalence of abstract permutation F20-sets only; not an incidence/code/H4 geometry isomorphism. The A5 torsor in the prior Clifford analysis is a separate concrete 600-cell object."}
if __name__=="__main__":
 x=main();OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
 print(json.dumps({k:v for k,v in x.items() if k not in ("W33_edge_index_to_S5_coset_index","S5_coset_even_A5_permutations","S5_coset_representatives","F20_generators_W33_80point_r","F20_generators_W33_80point_s")},indent=2),flush=True)
 print("F20_A5_ABSTRACT_EQUIVARIANT_PASS")
