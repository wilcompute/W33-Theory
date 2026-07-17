#!/usr/bin/env python3
"""Pass 403: semilinear voltage classification of the Heisenberg DRACKN."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from sympy.combinatorics import Permutation,PermutationGroup
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/"data"/"w33_pass403_drackn_semilinear_classification.json"
class PrimeField:
 def __init__(self,p):self.q=self.p=p;self.f=1
 def add(self,a,b):return(a+b)%self.p
 def neg(self,a):return(-a)%self.p
 def sub(self,a,b):return(a-b)%self.p
 def mul(self,a,b):return(a*b)%self.p
 def pow(self,a,n):return pow(a,n,self.p)
 def frob(self,a):return a
 @property
 def one(self):return 1
 @property
 def zero(self):return 0
class GF9:
 q=9;p=3;f=2
 @staticmethod
 def pair(x):return x%3,x//3
 @staticmethod
 def enc(a,b):return(a%3)+3*(b%3)
 def add(self,x,y):a,b=self.pair(x);c,d=self.pair(y);return self.enc(a+c,b+d)
 def neg(self,x):a,b=self.pair(x);return self.enc(-a,-b)
 def sub(self,x,y):return self.add(x,self.neg(y))
 def mul(self,x,y):a,b=self.pair(x);c,d=self.pair(y);return self.enc(a*c+2*b*d,a*d+b*c)
 def pow(self,x,n):
  r=1
  while n:
   if n&1:r=self.mul(r,x)
   x=self.mul(x,x);n//=2
  return r
 def frob(self,x):return self.pow(x,3)
 @property
 def one(self):return 1
 @property
 def zero(self):return 0
def omega(F,u,v):x,y=u;xp,yp=v;return F.sub(F.mul(y,xp),F.mul(x,yp))
def vertices(F):return[(x,y,z) for x in range(F.q) for y in range(F.q) for z in range(F.q)]
def adjacent(F,a,b):x,y,z=a;xp,yp,zp=b;return(x,y)!=(xp,yp) and F.sub(zp,z)==omega(F,(x,y),(xp,yp))
def left_translation(F,a,b,c):
 def act(v):x,y,z=v;return(F.add(a,x),F.add(b,y),F.add(F.add(c,z),omega(F,(a,b),(x,y))))
 return act
def linear_action(F,M):
 a,b,c,d=M;det=F.sub(F.mul(a,d),F.mul(b,c))
 if det==0:raise ValueError("singular")
 def act(v):x,y,z=v;return(F.add(F.mul(a,x),F.mul(b,y)),F.add(F.mul(c,x),F.mul(d,y)),F.mul(det,z))
 return act
def frobenius_action(F):return lambda v:(F.frob(v[0]),F.frob(v[1]),F.frob(v[2]))
def primitive(F):
 for x in range(2,F.q):
  if len({F.pow(x,k) for k in range(1,F.q)})==F.q-1 and F.pow(x,F.q-1)==1:return x
 raise AssertionError("no primitive")
def as_perm(F,act):V=vertices(F);idx={v:i for i,v in enumerate(V)};return Permutation([idx[act(v)] for v in V])
def preserves_all_edges(F,act):
 V=vertices(F)
 for i,u in enumerate(V):
  for v in V[i+1:]:
   if adjacent(F,u,v)!=adjacent(F,act(u),act(v)):return False
 return True
def certificate(F):
 one,zero,g=F.one,F.zero,primitive(F);basis=[one] if F.f==1 else[one,3];actions=[];names=[]
 for t in basis:actions.extend([left_translation(F,t,zero,zero),left_translation(F,zero,t,zero),left_translation(F,zero,zero,t)]);names.extend([f"Tx_{t}",f"Ty_{t}",f"Tz_{t}"])
 actions.extend([linear_action(F,(one,one,zero,one)),linear_action(F,(zero,F.neg(one),one,zero)),linear_action(F,(g,zero,zero,one))]);names.extend(["shear","symplectic_rotation","primitive_dilation"])
 if F.f>1:actions.append(frobenius_action(F));names.append("frobenius")
 edge={n:preserves_all_edges(F,a) for n,a in zip(names,actions)};G=PermutationGroup([as_perm(F,a) for a in actions]);obs=int(G.order());gl=(F.q*F.q-1)*(F.q*F.q-F.q);exp=F.q**3*gl*F.f
 return{"q":F.q,"field_degree":F.f,"primitive_element_encoding":g,"generators":names,"all_generators_preserve_adjacency":all(edge.values()),"generator_edge_checks":edge,"permutation_group_order":obs,"predicted_H_semidirect_GammaL_order":exp,"order_matches":obs==exp,"vertex_transitive":len(G.orbit(0))==F.q**3,"point_stabilizer_order":obs//F.q**3}
def build_payload():
 cases=[certificate(PrimeField(3)),certificate(PrimeField(5)),certificate(GF9())];checks={f"q{c['q']}_order":c["order_matches"] for c in cases};checks.update({f"q{c['q']}_edge_preservation":c["all_generators_preserve_adjacency"] for c in cases});checks.update({f"q{c['q']}_vertex_transitive":c["vertex_transitive"] for c in cases});p={"schema":"w33.pass403.drackn_semilinear.v1","status":"PASS" if all(checks.values()) else "FAIL","oriented_automorphism_group":"H_q semidirect GammaL(2,q)","order_formula":"q^3 (q^2-1)(q^2-q) f for q=p^f","action":"(a,c):(u,z)->(a+u,c+z+omega(a,u)); g:(u,z)->(gu,det(g)z); Frobenius coordinatewise","classification_boundary":{"spectrum_and_intersection_array":"not unique in the DRACKN category","extra_data_needed":"a regular Heisenberg action plus an oriented section whose triangle voltage is a nondegenerate alternating form","uniqueness":"in dimension two all nondegenerate alternating forms differ by a scalar, absorbed by det(g); hence the oriented Heisenberg voltage cover is unique up to semilinear isomorphism","full_unoriented_group":"not asserted beyond the orientation-preserving voltage group without an independent graph-automorphism census"},"cases":cases,"checks":checks};canonical=json.dumps(p,sort_keys=True,separators=(",",":")).encode();p["certificate_sha256"]=hashlib.sha256(canonical).hexdigest();return p
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--check",action="store_true");ap.add_argument("--output",type=Path,default=OUT);a=ap.parse_args();p=build_payload();text=json.dumps(p,indent=2,sort_keys=True)+"\n"
 if a.check:
  if not a.output.exists() or a.output.read_text()!=text:raise SystemExit("Pass 403 frozen certificate is stale")
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
 print(json.dumps({"status":p["status"],"checks":sum(p["checks"].values()),"total":len(p["checks"])}));return 0 if p["status"]=="PASS" else 1
if __name__=="__main__":raise SystemExit(main())
