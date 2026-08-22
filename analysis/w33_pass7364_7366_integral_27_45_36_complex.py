#!/usr/bin/env python3
"""Pass7364-7366: integral 27-lines -> 45-tritangents -> 36-double-sixes incidence prism."""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
import numpy as np
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from w33_pass4992_4999_common import build_base
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7364_7366_INTEGRAL_27_45_36_COMPLEX.json'

def rankp(A,p):
 A=np.asarray(A,dtype=np.int64).copy()%p;m,n=A.shape;r=0
 for c in range(n):
  z=next((i for i in range(r,m) if A[i,c]),None)
  if z is None:continue
  A[[r,z]]=A[[z,r]];A[r]=A[r]*pow(int(A[r,c]),-1,p)%p
  for i in range(m):
   if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%p
  r+=1
  if r==m:break
 return r

def snf(A):
 D=smith_normal_form(sp.Matrix(A),domain=sp.ZZ)
 return Counter(abs(int(D[i,i])) for i in range(min(D.shape)) if D[i,i])

def enum2(rows):
 B=[]
 for row in np.asarray(rows,dtype=np.uint8):
  x=sum((int(v)&1)<<i for i,v in enumerate(row))
  y=x
  for p,b in B:
   if (y>>p)&1:y^=b
  if y:
   p=y.bit_length()-1;B.append((p,y));B.sort(reverse=True)
 assert len(B)==7
 basis=[b for _,b in B];C=Counter()
 for m in range(1<<7):
  x=0
  for i,b in enumerate(basis):
   if (m>>i)&1:x^=b
  C[x.bit_count()]+=1
 return dict(sorted(C.items()))

def main():
 b=build_base();T=b['tritangents'];DS=b['DS']
 R=np.zeros((27,45),dtype=int)
 for j,t in enumerate(T):R[list(t),j]=1
 N=1-np.asarray(b['M'],dtype=int)
 Q=np.zeros((27,36),dtype=int)
 for i in range(27):
  for j,D in enumerate(DS):Q[i,j]=int(i not in D)
 assert np.array_equal(R@N,3*Q)
 sR,sN,sQ=snf(R),snf(N),snf(Q)
 assert sR==Counter({1:21});assert sN==Counter({1:14,3:7});assert sQ==Counter({2:13,1:7,10:1})
 ranks={str(p):{'R':rankp(R,p),'N':rankp(N,p),'Q':rankp(Q,p)} for p in (2,3,5,7)}
 assert ranks['3']=={'R':21,'N':14,'Q':21}
 # Mod 3 this is a genuine chain complex C2=F3^36 -> C1=F3^45 -> C0=F3^27.
 h2=36-ranks['3']['N'];h1=(45-ranks['3']['R'])-ranks['3']['N'];h0=27-ranks['3']['R']
 assert (h2,h1,h0)==(22,10,6)
 # Characteristic-2 projection of the line/double-six complement matrix.
 w=enum2(Q.T);assert w=={0:1,11:27,12:36,15:36,16:27,27:1}
 out={'schema':'w33.pass7364_7366.integral_27_45_36_complex.v1','status':'PASS','matrices':{'R':'27x45 line-tritangent incidence','N':'45x36 tritangent/doily-slice incidence','Q':'27x36 complement of line-in-double-six incidence'},'integral_curvature_identity':'R N = 3 Q','smith':{'R':{'1':21},'N':{'1':14,'3':7},'Q':{'1':7,'2':13,'10':1}},'modular_ranks':ranks,'F3_chain_homology':{'H2':h2,'H1':h1,'H0':h0,'euler_check':'22-10+6 = 36-45+27 = 18'},'binary_Q_code':{'parameters':'[27,7,11]_2','weight_enumerator':{str(k):v for k,v in w.items()},'minimum_words':27},'interpretation':'The 27/45/36 cubic-surface incidence system is an integral curved complex whose curvature is exactly 3Q; reducing mod 3 makes it flat and produces homology dimensions 22,10,6. Different prime reductions of the same integral matrices yield the ternary doily code and the binary 27-line code.','boundary':'Exact integral/incidence statement; RN=3Q is not an ordinary Z-chain complex because the integral composite is nonzero.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','F3_homology':[h2,h1,h0],'binary_Q':'[27,7,11]'}))
if __name__=='__main__':main()
