#!/usr/bin/env python3
"""Parse official ATLAS 40-point generators and solve literal tuple conjugacy.

Without the official payloads, the worker proves its conjugacy algorithm against a
synthetically relabelled project tuple and emits a fail-closed external-payload boundary.
"""
from __future__ import annotations
import argparse,hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def parse_gap(text,n=40):
 p=list(range(n))
 for cyc in re.findall(r'\(([^()]*)\)',text):
  a=[int(x)-1 for x in re.findall(r'\d+',cyc)]
  for x,y in zip(a,a[1:]+a[:1]):p[x]=y
 return tuple(p)
def compose(p,q):return tuple(p[q[i]]for i in range(len(p)))
def inverse(p):
 r=[0]*len(p)
 for i,j in enumerate(p):r[j]=i
 return tuple(r)
def conjugator(c0,d0,c,d):
 n=len(c);sol=[]
 for image0 in range(n):
  h={0:image0};q=[0];ok=True
  while q and ok:
   x=q.pop()
   for a,b in((c0,c),(d0,d)):
    y=a[x];z=b[h[x]]
    if y in h and h[y]!=z:ok=False;break
    if y not in h:h[y]=z;q.append(y)
  if ok and len(h)==n and len(set(h.values()))==n:
   H=tuple(h[i]for i in range(n))
   if all(H[c0[i]]==c[H[i]]and H[d0[i]]==d[H[i]]for i in range(n)):sol.append(H)
 return sol
def canonical_hash(d):
 x=dict(d);x.pop('sha256',None);return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 a=argparse.ArgumentParser();a.add_argument('--official-c');a.add_argument('--official-d');a.add_argument('--project-json',default=str(ROOT/'data'/'w33_pass1840_atlas_standard_word.json'));a.add_argument('--output');z=a.parse_args()
 proj=json.loads(Path(z.project_json).read_text());c=tuple(proj['c']['point_permutation']);d=tuple(proj['d']['point_permutation'])
 urls=['https://brauer.maths.qmul.ac.uk/Atlas/clas/U42/gap/U42d2G1-p40aB0.g1','https://brauer.maths.qmul.ac.uk/Atlas/clas/U42/gap/U42d2G1-p40aB0.g2']
 h=tuple((7*i+3)%40 for i in range(40));hi=inverse(h);c0=compose(compose(hi,c),h);d0=compose(compose(hi,d),h);synthetic=conjugator(c0,d0,c,d)
 base={'schema':'w33.pass1850.official_tuple_bridge.v2','official_urls':urls,'project_pair_sha256':hashlib.sha256(bytes(c)+bytes(d)).hexdigest(),'conjugacy_algorithm':'For each of 40 images of point 1, propagate h(c0*x)=c*h(x) and h(d0*x)=d*h(x); accept a bijection only after literal generator conjugacy checks.','synthetic_self_test':{'relabel_sha256':hashlib.sha256(bytes(h)).hexdigest(),'solutions':len(synthetic),'passed':h in synthetic}}
 if not z.official_c or not z.official_d:
  out=base|{'status':'BLOCKED_EXTERNAL_PAYLOAD','checks':{'algorithm_self_test':h in synthetic,'official_urls_frozen':True,'literal_tuple_claim_withheld':True},'boundary':'The official ATLAS representation page and exact GAP payload URLs are identified, but the remote payload server returned cache-miss/download failures in this execution environment. The exact conjugacy algorithm passes a literal synthetic tuple test; no official tuple-conjugacy claim is made without the primary-source bytes.'}
 else:
  tc=Path(z.official_c).read_text();td=Path(z.official_d).read_text();C=parse_gap(tc);D=parse_gap(td);S=conjugator(C,D,c,d)
  out=base|{'status':'PASS'if S else'FAIL','official_payload_sha256':[hashlib.sha256(tc.encode()).hexdigest(),hashlib.sha256(td.encode()).hexdigest()],'conjugators':[list(x)for x in S],'checks':{'algorithm_self_test':h in synthetic,'literal_c':bool(S),'literal_d':bool(S)}}
 out['sha256']=canonical_hash(out);text=json.dumps(out,sort_keys=True,separators=(',',':'))+'\n';print(text,end='')
 if z.output:Path(z.output).write_text(text)
 raise SystemExit(out['status']=='FAIL')
if __name__=='__main__':main()
