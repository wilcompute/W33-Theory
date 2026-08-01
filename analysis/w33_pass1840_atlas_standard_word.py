#!/usr/bin/env python3
"""Pass 1840: an ATLAS-standard (c,d) pair and a word for the canonical 2D outer element.

Official ATLAS conditions for U4(2):2: c is class 2C, |d|=9, and |cd|=10.
"""
from __future__ import annotations
import collections,hashlib,json,math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_pass1801_1805_common import build_geometry
D=build_geometry();igs=[tuple(a[0]) for a in D['acts']];s=tuple(D['outer'][0]);I=tuple(range(40))
def comp(p,q):return tuple(p[q[i]] for i in range(40))
def inv(p):
 r=[0]*40
 for i,j in enumerate(p):r[j]=i
 return tuple(r)
def eval_inner(word):
 p=I
 for ch in reversed(word):p=comp(igs[int(ch)],p)
 return p
def order(p):
 seen=[False]*40;o=1
 for i in range(40):
  if seen[i]:continue
  j=i;n=0
  while not seen[j]:seen[j]=True;n+=1;j=p[j]
  o=math.lcm(o,n)
 return o
def generated(gens):
 S={I};Q=collections.deque([I])
 while Q:
  x=Q.popleft()
  for g in gens:
   y=comp(g,x)
   if y not in S:S.add(y);Q.append(y)
 return S
c=comp(s,eval_inner('3423144210'));d=eval_inner('1410');di=inv(d)
assert order(c)==2 and order(d)==9 and order(comp(c,d))==10
G=generated((c,d,di));assert len(G)==51840
assert sum(comp(g,c)==comp(c,g) for g in G)==1440
assert sum(comp(g,s)==comp(s,g) for g in G)==96
parent={I:(None,None)};Q=collections.deque([I]);gens=(c,d,di);letters=('c','d','D')
while s not in parent:
 x=Q.popleft()
 for g,L in zip(gens,letters):
  y=comp(g,x)
  if y not in parent:parent[y]=(x,L);Q.append(y)
word=[];y=s
while parent[y][0] is not None:y,L0=parent[y];word.append(L0)
word=word[::-1];z=I
for L in word:z=comp({'c':c,'d':d,'D':di}[L],z)
assert z==s
print(json.dumps({'status':'PASS','group_order':len(G),'orders':{'c':2,'d':9,'cd':10},'centralizers':{'2C':1440,'2D':96},'canonical_2D_word':word,'word_length':len(word)},indent=2))
