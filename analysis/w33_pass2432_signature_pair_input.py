#!/usr/bin/env python3
from __future__ import annotations
import argparse, collections, itertools
from pathlib import Path
import numpy as np
Q=3
SIGNATURES=['111111141024111111111240111402111111111111024','111111402141111111112011141110411121114211101','111113121211311111113112111121131111111111411','111141111111024111111402111111111024240111111','112211121211112211211112112141111111112211211','113110113311110131141111111113011311311113110','141111111111111222111222111111222111111222111','211311111111311211111111411113111121111131112','311113101101131113311011113110113311111111141']
def normalize(v):
 w=tuple(int(x)%Q for x in v)
 for x in w:
  if x:return tuple(pow(x,-1,Q)*y%Q for y in w)
 raise ValueError
def symp(u,v):return (u[0]*v[3]-u[3]*v[0]+u[1]*v[2]-u[2]*v[1])%Q
def compose(p,q):return tuple(p[q[i]] for i in range(len(q)))
def build():
 points=sorted({normalize(v) for v in itertools.product(range(Q),repeat=4) if any(v)});pidx={p:i for i,p in enumerate(points)}
 A=np.zeros((40,40),dtype=np.int8)
 for i,u in enumerate(points):
  for j in range(i+1,40):
   if symp(u,points[j])==0:A[i,j]=A[j,i]=1
 line_sets=set()
 for i in range(40):
  for j in range(i+1,40):
   if not A[i,j]:continue
   u,v=points[i],points[j];span=set()
   for a,b in itertools.product(range(3),repeat=2):
    w=tuple((a*u[k]+b*v[k])%3 for k in range(4))
    if any(w):span.add(pidx[normalize(w)])
   line_sets.add(tuple(sorted(span)))
 lines=sorted(line_sets);lidx={L:i for i,L in enumerate(lines)}
 edges=[(i,j) for i in range(40) for j in range(i+1,40) if A[i,j]];eidx={e:i for i,e in enumerate(edges)}
 frames=[];match=[]
 for a,La in enumerate(lines):
  sa=set(La)
  for b in range(a+1,40):
   Lb=lines[b]
   if not sa.isdisjoint(Lb):continue
   m=[]
   for x in La:
    ys=[y for y in Lb if A[x,y]];assert len(ys)==1;m.append(eidx[tuple(sorted((x,ys[0])))])
   frames.append((a,b));match.append(tuple(sorted(m)))
 fidx={f:i for i,f in enumerate(frames)};octets=[];seen=set()
 for left in itertools.combinations(range(40),4):
  if any(A[a,b] for a,b in itertools.combinations(left,2)):continue
  right=tuple(v for v in range(40) if all(A[v,u] for u in left))
  if len(right)!=4 or any(A[a,b] for a,b in itertools.combinations(right,2)):continue
  key=tuple(sorted((tuple(left),tuple(right))))
  if key not in seen:seen.add(key);octets.append((tuple(left),tuple(right)))
 oidx={tuple(sorted(o)):i for i,o in enumerate(octets)}
 def trans(v):
  v=normalize(v);out=[]
  for x in points:
   c=symp(x,v);out.append(pidx[normalize(tuple((x[i]+c*v[i])%3 for i in range(4)))])
  return tuple(out)
 def induced(p):
  lp=tuple(lidx[tuple(sorted(p[x] for x in L))] for L in lines);fp=tuple(fidx[tuple(sorted((lp[a],lp[b])))] for a,b in frames);op=[]
  for left,right in octets:
   key=tuple(sorted((tuple(sorted(p[x] for x in left)),tuple(sorted(p[x] for x in right)))))
   op.append(oidx[key])
  return fp,tuple(op)
 gens=[induced(trans(v)) for v in ((1,0,0,0),(0,1,0,0),(0,0,0,1),(1,0,1,0))]
 unseen=set(range(540*45));orbits=[]
 while unseen:
  z=next(iter(unseen));O={z};q=collections.deque([z])
  while q:
   w=q.popleft();f,o=divmod(w,45)
   for fg,og in gens:
    zz=fg[f]*45+og[o]
    if zz not in O:O.add(zz);q.append(zz)
  unseen-=O;orbits.append(O)
 O=next(O for O in orbits if len(O)==540);key=[None]*540
 for z in O:f,o=divmod(z,45);key[f]=o
 assert collections.Counter(key)=={o:12 for o in range(45)}
 return match,key
def main():
 ap=argparse.ArgumentParser();ap.add_argument('output',type=Path);a=ap.parse_args();match,key=build()
 with a.output.open('w') as f:
  f.write('540 240 45 9\n')
  for r,m in enumerate(match):f.write(' '.join(map(str,m))+f' {key[r]}\n')
  for s in SIGNATURES:f.write(' '.join(s)+'\n')
if __name__=='__main__':main()
