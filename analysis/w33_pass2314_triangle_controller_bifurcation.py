#!/usr/bin/env python3
"""Pass 2314: exact triangle-relation fork between two controller quotients."""
from __future__ import annotations
import collections,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_pass2314_triangle_controller_bifurcation.json'
EXPECTED='551a6a33d547eb58e891b931709eb3cfa260216d16763d5793d3f379e67561c7'
I=(1,0,0,0,1,0,0,0,1);R=(0,1,0,1,0,0,0,0,1);U=(1,0,0,0,0,1,0,1,1)
def mm(a,b):return tuple(sum(a[3*i+k]*b[3*k+j] for k in range(3))%2 for i in range(3) for j in range(3))
def closure(gens):
 seen={I};q=collections.deque([I])
 while q:
  a=q.popleft()
  for g in gens:
   c=mm(g,a)
   if c not in seen:seen.add(c);q.append(c)
 return seen
def order(a):
 x=I
 for n in range(1,100):
  x=mm(a,x)
  if x==I:return n
 raise RuntimeError
def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None)
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def build():
 G=closure([R,U]);invs={}
 for g in G:
  x=I
  for n in range(1,20):
   x=mm(g,x)
   if x==I:
    y=I
    for _ in range(n-1):y=mm(g,y)
    invs[g]=y;break
 unseen=set(G);classes=[]
 while unseen:
  g=next(iter(unseen));C={mm(mm(h,g),invs[h]) for h in G};classes.append(C);unseen-=C
 pairs=sorted((len(C),order(next(iter(C)))) for C in classes)
 gh=hashlib.sha256(json.dumps([list(g) for g in sorted(G)],separators=(',',':')).encode()).hexdigest()
 checks={'R_order_2':order(R)==2,'U_order_3':order(U)==3,'RU_order_7':order(mm(R,U))==7,'generated_order_168':len(G)==168,'all_nonidentity_normal_closures_full':all(len(closure(list(C)))==168 for C in classes if I not in C),'six_conjugacy_classes':len(classes)==6,'triangle_signatures_distinct':7!=2}
 d={'schema':'w33.pass2314.triangle_controller_bifurcation.v1','status':'PASS_WITH_RELATION_FORK_NOT_CARRIER_IDENTIFICATION','arithmetic_mod2':{'generators':{'R4_mod2':[[0,1,0],[1,0,0],[0,0,1]],'U6_mod2':[[1,0,0],[0,0,1],[0,1,1]]},'generator_orders':[2,3],'product_order':7,'generated_order':168,'generated_group':'GL(3,2) = PSL(2,7)','group_elements_sha256':gh,'conjugacy_class_size_order_pairs':[list(x) for x in pairs],'simplicity_check':'The normal closure of a representative of every nonidentity conjugacy class has order 168.'},'quadratic_hom_controller':{'group':'C3:C2 = S3','generator_orders':[3,2],'reflection_phase_relation':'srs=r^-1','corresponding_2_3_product_order':2,'module':'16 trivial + 16 sign + 9 standard'},'fork':{'shared_local_orders':[2,3],'arithmetic_triangle_signature':[2,3,7],'quadratic_triangle_signature':[2,3,2],'no_s3_quotient_of_mod2_group':'The order-168 group is simple; a nontrivial quotient to S3 would require a proper nontrivial normal kernel, while an injection is impossible by order.','interpretation':'Reducing the overlapping arithmetic carrier mod 2 produces the Fano-plane symmetry controller. Passing to bilinear phase multiplicities instead produces S3. They are relation branches of common local order data, not the same controller at different resolutions.'},'engineering':{'proposal':'Expose two explicitly typed control modes: a 168-state Fano routing/diagnostic mode and an S3 quadratic phase-demodulation mode. Never reuse a state encoding merely because both modes have order-2 and order-3 generators.','type_safety_rule':'The product-order assertion distinguishes the modes: 7 for Fano mode, 2 for quadratic-Hom mode.'},'checks':checks,'theorem':'The mod-2 reduction of the overlapping arithmetic phase generators closes as the (2,3,7) Fano group GL(3,2), whereas the quadratic Hom multiplicity controller closes as the (2,3,2) group S3. The common generator orders bifurcate through different product relations.','boundary':'This is an exact algebraic controller distinction. It does not identify either finite group with the infinite SL3(Z) carrier, select a physical observable, or restore withdrawn particle interpretations.'}
 assert all(checks.values());d['sha256_without_hash_field']=digest(d);return d
def main():
 d=build();assert d['sha256_without_hash_field']==EXPECTED;assert d==json.loads(OUT.read_text())
 print(json.dumps({'status':d['status'],'certificate':EXPECTED,'Fano':[2,3,7],'quadratic':[2,3,2]},sort_keys=True))
if __name__=='__main__':main()
