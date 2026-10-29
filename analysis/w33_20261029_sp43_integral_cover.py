#!/usr/bin/env python3
"""Exact integral E8 lattice realization of the natural Sp(4,3) double cover.
Enumerate all 240 E8 roots, lift seven certified mod-2 generators,
and check the simultaneous 51,840-word natural/integral representation.
No physical Hamiltonian is asserted. Python standard library only.
"""
import json
from collections import Counter,deque
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRIOR=json.loads((ROOT/"data/w33_20261029_explicit_mod2_E8_isometry.json").read_text())
OUT=ROOT/"data/w33_20261029_sp43_integral_cover.json"
EDGES=[tuple(t) for t in PRIOR["E8_Dynkin_edges"]]
GENF=[tuple(x["E8_simple_root_mod2_columns"]) for x in PRIOR["checked_group_generators"]]
US=[tuple(x["transvection_u"]) for x in PRIOR["checked_group_generators"]]
def neg(x):return tuple(-t for t in x)
def dot(x,y):
 return 2*sum(a*b for a,b in zip(x,y))-sum(x[i]*y[j]+x[j]*y[i] for i,j in EDGES)
def roots240():
 roots=set()
 for j in range(8):
  v=tuple(int(i==j) for i in range(8));roots.update((v,neg(v)))
 queue=list(roots)
 for x in queue:
  for i in range(8):
   k=2*x[i]-sum(x[j] for u,j in EDGES if u==i)-sum(x[j] for j,u in EDGES if u==i)
   y=list(x);y[i]-=k;y=tuple(y)
   if y not in roots:roots.add(y);queue.append(y)
 assert len(roots)==240
 return sorted(roots)
def mat_image(cols,idx,roots):
 basis=[roots[i] for i in cols]
 v=[]
 for x in roots:
  y=tuple(sum(x[j]*basis[j][k] for j in range(8)) for k in range(8))
  v.append(idx[y])
 assert len(set(v))==240
 return tuple(v)
def lift(columns,roots,index):
 classes={}
 for v in roots:
  key=sum((v[i]&1)<<i for i in range(8))
  classes.setdefault(key,[]).append(v)
 assert all(len(v)==2 for v in classes.values())
 opts=[classes[t] for t in columns]
 solutions=[]
 for bits in range(256):
  chosen=[opts[i][(bits>>i)&1] for i in range(8)]
  if all(dot(chosen[i],chosen[j])==(2 if i==j else -1 if (i,j) in EDGES or (j,i) in EDGES else 0)
         for i in range(8) for j in range(i+1)):
   solutions.append(tuple(index[v] for v in chosen))
 assert len(solutions)==2
 return solutions
def integral_product(x,y,roots,idx):
 base=[roots[j] for j in x]
 return tuple(idx[tuple(sum(roots[y[j]][i]*base[i][k] for i in range(8)) for k in range(8))]
              for j in range(8))
def omega(x,y):
 return (x[0]*y[1]-x[1]*y[0]+x[2]*y[3]-x[3]*y[2])%3
def natural_product(x,y):
 return tuple(tuple(sum(y[j][i]*x[i][k] for i in range(4))%3 for k in range(4))
              for j in range(4))
def main():
 roots=roots240();index={r:i for i,r in enumerate(roots)}
 eye8=tuple(index[tuple(int(j==i) for j in range(8))] for i in range(8))
 neg8=tuple(index[neg(roots[j])] for j in eye8)
 gen=[]
 for f in GENF:
  for candidate in lift(f,roots,index):
   perm=mat_image(candidate,index,roots)
   if all(perm[perm[perm[j]]]==j for j in range(240)):
    gen.append(candidate);break
  else:raise AssertionError("No order-three integral lift")
 assert len(gen)==7
 eye4=tuple(tuple(int(j==i) for j in range(4)) for i in range(4))
 natgen=[]
 for u in US:
  natgen.append(tuple(tuple((x[k]+omega(x,u)*u[k])%3 for k in range(4)) for x in eye4))
 seen={eye4:eye8}
 reverse={eye8:eye4}
 queue=deque([eye4])
 while queue:
  n=queue.popleft();e=seen[n]
  for g,h in zip(natgen,gen):
   nn=natural_product(n,g)
   ee=integral_product(e,h,roots,index)
   if nn in seen:assert seen[nn]==ee
   else:
    assert ee not in reverse
    seen[nn]=ee;reverse[ee]=nn;queue.append(nn)
 assert len(seen)==len(reverse)==51840
 neg4=tuple(tuple((-v)%3 for v in column) for column in eye4)
 assert seen[neg4]==neg8
 classes=Counter()
 for e in seen.values():
  binary=tuple(sum((roots[e[i]][j]&1)<<j for j in range(8)) for i in range(8))
  classes[binary]+=1
 assert len(classes)==25920 and set(classes.values())=={2}
 invsq=Counter()
 for n,e in seen.items():
  if n in (eye4,neg4):continue
  e2=integral_product(e,e,roots,index)
  if e2 in (eye8,neg8):
   n2=natural_product(n,n)
   if n2==neg4:
    assert e2==neg8
    invsq["minus"]+=1
   elif n2==eye4:
    assert e2==eye8
    invsq["plus"]+=1
 assert invsq=={"minus":540,"plus":90},invsq
 output={"status":"PASS","integral_cover_order":len(seen),"natural_symplectic_group":"Sp(4,3)",
         "projective_image_order":len(classes),"kernel":"{+I,-I}",
         "central_minus_I4_corresponds_to_minus_I8":True,
         "integral_generator_columns":[[list(roots[k]) for k in g] for g in gen],
         "finite_involution_lift_counts":dict(invsq),
         "involution_classes":{"order_four_lifts":270,"order_two_lifts":45},
         "method":"complete parallel word BFS, natural 4x4 F3 and integral 8x8 E8 root action",
         "boundary":"Purely mathematical; no physical implementation or parameter prediction."}
 OUT.write_text(json.dumps(output,indent=2)+"\n",encoding="utf-8")
 print("PASS Sp(4,3) -> E8: 51840; projective 25920; involutions 270+45")
if __name__=="__main__":main()
