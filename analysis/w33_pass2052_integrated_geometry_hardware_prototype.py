#!/usr/bin/env python3
"""Executable reference model for the Pass-2052 geometry pipeline."""
from __future__ import annotations
import itertools,json,hashlib
from collections import Counter,deque
from pathlib import Path
import numpy as np
from w33_pass1060_1064_core import build_w33

ROOT=Path(__file__).resolve().parents[1]
WIT=ROOT/'data/w33_pass2012_d8_orbit_parallel_class_witness.json'
CERT=ROOT/'data/w33_pass2052_integrated_geometry_hardware_prototype.json'
EXPECTED='975e159ffaca69b2c4ad488f5b3552fe7780c3b017fc29c94194013956bd5e42'

def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None)
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def compose(a,b):return tuple(a[b[i]] for i in range(len(a)))
def closure(gens):
 n=len(gens[0]);e=tuple(range(n));seen={e};q=deque([e])
 while q:
  a=q.popleft()
  for g in gens:
   c=compose(g,a)
   if c not in seen:seen.add(c);q.append(c)
 return sorted(seen)
def all_spreads(lines,npts=40):
 onpt=[[i for i,L in enumerate(lines) if p in L] for p in range(npts)];out=[]
 def rec(ch,used):
  if len(used)==npts:out.append(tuple(sorted(ch)));return
  p=next(x for x in range(npts) if x not in used)
  for li in onpt[p]:
   if set(lines[li])&used:continue
   rec(ch+[li],used|set(lines[li]))
 rec([],set());return sorted(set(out))
def frame_data(w):
 edges=[(a,b) for a in range(40) for b in range(a+1,40) if w.adj[a,b]]
 eidx={e:i for i,e in enumerate(edges)};frames=[];masks=[]
 for a,b in itertools.combinations(range(40),2):
  if set(w.lines[a])&set(w.lines[b]):continue
  es=[]
  for p in w.lines[a]:
   qs=[q for q in w.lines[b] if w.adj[p,q]];assert len(qs)==1
   es.append(tuple(sorted((p,qs[0]))))
  mask=sum(1<<eidx[e] for e in es);frames.append((a,b));masks.append(mask)
 assert len(edges)==240 and len(frames)==540
 return edges,frames,masks
def induced_line_perm(w,p):
 li={L:i for i,L in enumerate(w.lines)}
 return tuple(li[tuple(sorted(p[x] for x in L))] for L in w.lines)
def induced_frame_perm(frames,lp):
 fi={f:i for i,f in enumerate(frames)}
 return tuple(fi[tuple(sorted((lp[a],lp[b])))] for a,b in frames)
def orbit(start,group):return sorted({g[start] for g in group})

def main():
 w=build_w33();edges,frames,masks=frame_data(w);spreads=all_spreads(w.lines)
 wit=json.loads(WIT.read_text());cert=json.loads(CERT.read_text())
 assert cert['sha256_without_hash_field']==EXPECTED==digest(cert)
 selected=sorted(wit['selected_frame_indices']);assert len(selected)==60
 r=tuple(wit['subgroup']['r_point_permutation']);s=tuple(wit['subgroup']['s_point_permutation'])
 pg=closure([r,s]);assert len(pg)==8
 fg=[induced_frame_perm(frames,induced_line_perm(w,p)) for p in pg]
 remaining=set(selected);selected_orbits=[]
 while remaining:
  o=orbit(min(remaining),fg);assert set(o)<=remaining
  selected_orbits.append(o);remaining-=set(o)
 assert sorted(map(len,selected_orbits))==sorted(wit['selected_orbit_sizes'])
 union=0;overlap=0
 for i in selected:
  overlap|=union&masks[i];union|=masks[i]
 assert overlap==0 and union.bit_count()==240
 # Rank-three spread mixer.
 A=np.zeros((36,36),dtype=np.int64)
 for i,j in itertools.combinations(range(36),2):
  if len(set(spreads[i])&set(spreads[j]))==4:A[i,j]=A[j,i]=1
 assert set(map(int,A.sum(1)))=={15}
 assert np.array_equal(A@A,9*np.eye(36,dtype=np.int64)+6*np.ones((36,36),dtype=np.int64))
 x=np.arange(36,dtype=np.int64);x=x*36-int(x.sum())
 assert int(x.sum())==0 and np.array_equal(A@(A@x),9*x)
 # Rook-double crossbar: two 3x3 banks, cross-bank row/column links.
 V=[(b,r,c) for b in range(2) for r in range(3) for c in range(3)]
 links=[]
 for u in V:
  for v in V:
   if u<v and u[0]!=v[0] and (u[1]==v[1] or u[2]==v[2]):links.append((u,v))
 deg=Counter(x for e in links for x in e)
 assert len(V)==18 and len(links)==36 and set(deg.values())=={4}
 out={'status':'PASS','counts':{'points':40,'lines':40,'edges':240,'frames':540,'spreads':36},
      'd8':{'order':8,'orbits':len(selected_orbits),'orbit_sizes':sorted(map(len,selected_orbits)),
            'frames':len(selected),'edge_profile':{'1':union.bit_count()}},
      'spread_mixer':{'lanes':36,'degree':15,'A2':'9I+6J','mean_zero_R2':'I'},
      'rook_double':{'vertices':18,'edges':36,'degree':4},'certificate':EXPECTED}
 print(json.dumps(out,indent=2,sort_keys=True));return out
if __name__=='__main__':main()
