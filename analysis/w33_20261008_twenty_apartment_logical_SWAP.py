"""Permutation-only Clifford logical SWAP from the actual F20 CW automorphisms.

A group symmetry acts as an edge permutation preserving both CSS check
rowspaces. The induced mod2 H1 representation is C2; choose a compatible
dual basis of X/Z logical operators and verify logical SWAP.
"""
import json,collections,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_twenty_apartment_binary_CSS_F20 import topology,add,reduce,nullspace
OUT=ROOT/"data/w33_20261008_20apartment_logical_swap_gate.json"
def basis(span):
 B={}
 for v in span:add(v,B)
 return B
def transform(word,p):
 t=0
 for i in range(len(p)):
  if (word>>i)&1:t^=1<<p[i]
 return t
def coord(x,classes,check_basis):
 for c in range(1<<len(classes)):
  y=x
  for j,h in enumerate(classes):
   if c>>j&1:y^=h
  if reduce(y,check_basis)==0:return c
 raise ValueError("outside")
def main():
 V,E,faces,stab,C5,b1,b2=topology()
 cob=basis(b1);bound=basis(b2)
 Xh=[];Zh=[]
 B=cob.copy()
 for h in nullspace(b2,60):
  if add(h,B):Xh.append(h)
 B=bound.copy()
 for z in nullspace(b1,60):
  if add(z,B):Zh.append(z)
 assert len(Xh)==len(Zh)==2
 # Choose Z logical basis dual to the X logical basis.
 Zdual=[]
 for logical in (1,2):
  v=next(Zh[0]*(t&1)^Zh[1]*((t>>1)&1) for t in (1,2,3)
      if all(( (Xh[j]&(Zh[0]*(t&1)^Zh[1]*((t>>1)&1))).bit_count()%2)==((logical>>j)&1) for j in range(2)))
  Zdual.append(v)
 assert [[(a&b).bit_count()%2 for b in Zdual] for a in Xh]==[[1,0],[0,1]]
 idx={e:i for i,e in enumerate(E)}
 orders=collections.Counter();images=collections.Counter();witness=None
 I=tuple(range(80))
 for g in stab:
  perm=[idx[tuple(sorted((g[u],g[v])))] for u,v in E]
  assert sorted(perm)==list(range(60))
  assert all(reduce(transform(v,perm),cob)==0 for v in b1)
  assert all(reduce(transform(v,perm),bound)==0 for v in b2)
  nx=tuple(coord(transform(v,perm),Xh,cob) for v in Xh)
  nz=tuple(coord(transform(v,perm),Zdual,bound) for v in Zdual)
  assert nx==nz
  t=I;n=0
  while True:
   t=tuple(t[g[i]] for i in range(80));n+=1
   if t==I:break
  orders[n]+=1;images[(n,nx)]+=1
  if n==4 and witness is None:
   witness={"automorphism_order":4,"edge_permutation":perm,
     "logical_X_image":list(nx),"logical_Z_image":list(nz),
     "X_logical_supports":[[i for i in range(60) if h>>i&1] for h in Xh],
     "Z_logical_supports":[[i for i in range(60) if h>>i&1] for h in Zdual]}
 assert orders=={1:1,2:5,4:10,5:4}
 assert all(image==(2,1) if order==4 else image==(1,2) for order,image in images)
 return {"code":"[[60,2,6]]_2","F20_element_order_counts":dict(orders),
  "F20_logical_action_by_element_order":{str(k):("SWAP" if k==4 else "identity") for k in orders},
  "logical_SWAP_implemented_by_edge_permutation":True,
  "physical_wire_permutation_witness":witness,
  "all_vertex_X_and_face_Z_stabilizers_preserved":True,
  "X_Z_dual_basis_pairing":[[1,0],[0,1]],
  "not_an_entangling_gate":True,
  "hardware_cost_and_fault_tolerance_unknown":True,
  "representation_boundary":"Induced Pauli symplectic action is logical SWAP in chosen dual basis, up to phases/Pauli-frame choices; no implemented photonic hardware or logical universal gate set inferred."}
if __name__=="__main__":
 x=main();OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
 print(json.dumps({k:v for k,v in x.items() if k!="physical_wire_permutation_witness"},indent=2),flush=True)
 print("LOGICAL_SWAP_PASS")
