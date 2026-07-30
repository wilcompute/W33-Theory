#!/usr/bin/env python3
"""Independent exact p-adic idempotent-lifting verifier for Pass 1343."""
from pathlib import Path
import hashlib,json,sys
import sympy as sp
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data';sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass1330_1334_modular_triality_cycle_atlas as a
P=a.P;ONE=[1]+[0]*25;BASIS=[[int(i==j) for i in range(26)] for j in range(26)]
FROZEN=json.loads((DATA/'w33_pass1340_1344_cartan_atlas_selector_padic.json').read_text())['pass1343_padic_lifting']['records']
def mul(x,y,m):
 z=[0]*26
 for i,u in enumerate(x):
  if u%m:
   for j,v in enumerate(y):
    if v%m:
     for k,c in enumerate(P[i,j]):z[k]=(z[k]+u*v*int(c))%m
 return z
def sub(x,y,m):return [(u-v)%m for u,v in zip(x,y)]
def scale(c,x,m):return [(c*u)%m for u in x]
def solve(A,b,p):
 M=[[x%p for x in row]+[bb%p] for row,bb in zip(A,b)];r=0;piv=[];n=len(M[0])-1
 for c in range(n):
  q=next((i for i in range(r,len(M)) if M[i][c]),None)
  if q is None:continue
  M[r],M[q]=M[q],M[r];iv=pow(M[r][c],-1,p);M[r]=[(iv*x)%p for x in M[r]]
  for i in range(len(M)):
   if i!=r and M[i][c]:
    z=M[i][c];M[i]=[(M[i][j]-z*M[r][j])%p for j in range(n+1)]
  piv.append(c);r+=1
 x=[0]*n
 for i,c in enumerate(piv):x[c]=M[i][n]
 return x
def inverse(x,m):
 L=sp.Matrix.hstack(*[sp.Matrix(mul(x,e,m)) for e in BASIS])
 return [int(v)%m for v in L.inv_mod(m)*sp.Matrix(ONE)]
def lift(x,m):
 for step in range(20):
  err=sub(mul(x,x,m),x,m)
  if not any(err):return x,step
  x=sub(x,mul(err,inverse(sub(scale(2,x,m),ONE,m),m),m),m)
 raise RuntimeError
def qdata(p):
 rec=json.loads((DATA/'w33_pass1330_modular_quotient_maps.json').read_text())['records'][str(p)];images=[]
 for i in range(26):
  row=[]
  for b in rec['matrix_blocks']:row+=b['images'][i]
  row += [c[i] for c in rec['scalar_characters']];images.append([x%p for x in row])
 targets=[];off=0;qdim=len(images[0])
 for bi,b in enumerate(rec['matrix_blocks']):
  n=b['size']
  for r in range(n):
   t=[0]*qdim;t[off+r*n+r]=1;targets.append((f'M{n}_{bi}:{r}',t,bi))
  off+=n*n
 for si in range(len(rec['scalar_characters'])):
  t=[0]*qdim;t[off+si]=1;targets.append((f'F_{si}',t,len(rec['matrix_blocks'])+si))
 return images,targets
def modular_system(p):
 images,targets=qdata(p);rem=ONE[:];out=[]
 for label,target,component in targets:
  x=solve(list(map(list,zip(*images))),target,p);x=mul(mul(rem,x,p),rem,p);x,s=lift(x,p);out.append((label,x,component,s));rem=sub(rem,x,p)
 assert not any(rem);return out
def sha(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 for p in (2,3,5):
  m=p**6;rem=ONE[:];out=[]
  for label,e,component,_ in modular_system(p):
   x=mul(mul(rem,e,m),rem,m);x,s=lift(x,m)
   for _,f,_,_ in out:assert not any(mul(x,f,m)) and not any(mul(f,x,m))
   out.append((label,x,component,s));rem=sub(rem,x,m)
  assert not any(rem)
  serial=[{'label':lab,'component':c,'newton_steps':s,'coordinates':e} for lab,e,c,s in out]
  rec=FROZEN[str(p)];assert len(out)==rec['primitive_idempotent_count'];assert [x[3] for x in out]==rec['newton_steps'];assert sha(serial)==rec['lift_sha256']
 print('PASS 1343 p-adic lifting verifier')
if __name__=='__main__':main()
