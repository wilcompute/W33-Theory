#!/usr/bin/env python3
"""Pass 1855: verify literal simultaneous conjugacy of the official ATLAS 40a GAP pair."""
from __future__ import annotations
import argparse,collections,hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OFFICIAL_C='z1 := (1,2)(3,4)(5,7)(6,9)(8,13)(10,17)(11,18)(12,19)(14,21)(15,22)(16,23)(20,27)(24,32)(25,33)(26,34)(28,36)(29,37)(30,35)(31,38)(39,40);\n'
OFFICIAL_D='z1 := (1,3,6,10,14,8,5,2,4)(7,11,17,13,16,9,15,20,12)(18,24,23)(19,25,31,22,30,29,21,28,26)(27,35,34)(32,33,38)(36,39,37);\n'
URLS=['https://brauer.maths.qmul.ac.uk/Atlas/clas/U42/gap/U42d2G1-p40aB0.g1','https://brauer.maths.qmul.ac.uk/Atlas/clas/U42/gap/U42d2G1-p40aB0.g2']
def parse(text,n=40):
 p=list(range(n))
 for cyc in re.findall(r'\(([^()]*)\)',text):
  a=[int(x)-1 for x in re.findall(r'\d+',cyc)]
  for x,y in zip(a,a[1:]+a[:1]):p[x]=y
 return tuple(p)
def comp(p,q):return tuple(p[q[i]] for i in range(len(p)))
def inv(p):
 r=[0]*len(p)
 for i,j in enumerate(p):r[j]=i
 return tuple(r)
def order(p):
 e=tuple(range(len(p)));x=e
 for n in range(1,1000):
  x=comp(p,x)
  if x==e:return n
 raise AssertionError('order overflow')
def conjugators(c0,d0,c,d):
 n=len(c);sol=[]
 for image0 in range(n):
  h={0:image0};q=[0];ok=True
  while q and ok:
   x=q.pop()
   for a,b in ((c0,c),(d0,d)):
    y=a[x];z=b[h[x]]
    if y in h and h[y]!=z:ok=False;break
    if y not in h:h[y]=z;q.append(y)
  if ok and len(h)==n and len(set(h.values()))==n:
   H=tuple(h[i] for i in range(n))
   if all(H[c0[i]]==c[H[i]] and H[d0[i]]==d[H[i]] for i in range(n)):sol.append(H)
 return sol
def generated_group(gens):
 gens=list(gens)+[inv(g) for g in gens];e=tuple(range(len(gens[0])));seen={e};q=collections.deque([e])
 while q:
  x=q.popleft()
  for g in gens:
   y=comp(g,x)
   if y not in seen:seen.add(y);q.append(y)
 return seen
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output');args=ap.parse_args()
 c=(23,16,39,11,9,21,34,32,14,4,30,3,25,19,8,36,1,29,26,13,33,5,24,0,22,12,18,37,38,17,10,35,7,20,6,31,15,27,28,2);d=(27,1,24,30,22,29,3,28,23,2,25,26,0,10,21,33,4,18,36,7,15,39,16,35,6,13,38,9,19,32,12,37,8,14,31,11,20,34,5,17);assert hashlib.sha256(bytes(c)+bytes(d)).hexdigest()=='28a50053c1e9f870165e7a0da88a482f64ce35fc5a27f7e18442a574aeb0b7cf'
 C=parse(OFFICIAL_C);D=parse(OFFICIAL_D);sol=conjugators(C,D,c,d);assert len(sol)==1;h=sol[0]
 G=generated_group([C,D]);stab=[g for g in G if g[0]==0];unused=set(range(40));subs=[]
 while unused:
  x=min(unused);O={g[x] for g in stab};subs.append(sorted(O));unused-=O
 checks={'official_orders':order(C)==2 and order(D)==9 and order(comp(C,D))==10,'official_group_order_51840':len(G)==51840,'rank3_suborbits_1_12_27':sorted(map(len,subs))==[1,12,27],'unique_simultaneous_conjugator':len(sol)==1,'literal_c_conjugacy':all(h[C[i]]==c[h[i]] for i in range(40)),'literal_d_conjugacy':all(h[D[i]]==d[h[i]] for i in range(40))};assert all(checks.values())
 out={'schema':'w33.pass1855.literal_official_atlas_tuple.v1','status':'PASS','official_representation_page':'https://brauer.maths.qmul.ac.uk/Atlas/v3/permrep/U42d2G1-p40aB0','official_payload_urls':URLS,'official_payload_text':[OFFICIAL_C.strip(),OFFICIAL_D.strip()],'official_payload_sha256':[hashlib.sha256(OFFICIAL_C.encode()).hexdigest(),hashlib.sha256(OFFICIAL_D.encode()).hexdigest()],'official_generator_permutations':[list(C),list(D)],'project_pair_permutations':[list(c),list(d)],'unique_conjugator_official_to_project':list(h),'conjugator_sha256':hashlib.sha256(bytes(h)).hexdigest(),'group_order':len(G),'standard_orders':{'c':order(C),'d':order(D),'cd':order(comp(C,D))},'suborbit_lengths_at_point1':sorted(map(len,subs)),'checks':checks,'boundary':'This is a literal byte-level simultaneous-conjugacy certificate for the official ATLAS 40a GAP pair and the project standard pair. It does not identify unrelated ATLAS representations or alternative standard pairs.'}
 out['certificate_sha256']=hashlib.sha256(json.dumps(out,sort_keys=True,separators=(',',':')).encode()).hexdigest();text=json.dumps(out,sort_keys=True,separators=(',',':'))+'\n';print(text,end='')
 if args.output:Path(args.output).write_text(text)
if __name__=='__main__':main()
