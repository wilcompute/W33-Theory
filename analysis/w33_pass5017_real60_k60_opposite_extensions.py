#!/usr/bin/env python3
"""Pass5017: reduce the canonical real octahedron V60 lattice mod2 and compare it equivariantly with binary K60."""
from __future__ import annotations
import itertools,json,math,sys
from pathlib import Path
import numpy as np
import sympy as sy
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from analysis.w33_pass4992_4999_common import build_base,build_group,gf2_rank_int
OUT=ROOT/'data/PART_W33_PASS5017_REAL60_K60_OPPOSITE_EXTENSIONS.json'

def rankp(A,p):
 A=np.array(A,dtype=int)%p;m,n=A.shape;r=0
 for c in range(n):
  k=next((i for i in range(r,m) if A[i,c]),None)
  if k is None:continue
  if k!=r:A[[r,k]]=A[[k,r]]
  A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
  for i in range(m):
   if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%p
  r+=1
  if r==m:break
 return r

def nullp(A,p):
 A=np.array(A,dtype=int)%p;m,n=A.shape;r=0;piv=[]
 for c in range(n):
  k=next((i for i in range(r,m) if A[i,c]),None)
  if k is None:continue
  if k!=r:A[[r,k]]=A[[k,r]]
  A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
  for i in range(m):
   if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%p
  piv.append(c);r+=1
 free=[c for c in range(n) if c not in piv];out=[]
 for f in free:
  x=np.zeros(n,dtype=np.uint8);x[f]=1
  for rr,c in enumerate(piv):x[c]=(-A[rr,f])%p
  out.append(x)
 return np.array(out,dtype=np.uint8)

def indep_rows(M):
 piv={};out=[]
 for i,row in enumerate(np.asarray(M,dtype=np.uint8)%2):
  x=sum(int(v)<<j for j,v in enumerate(row) if v)
  while x:
   q=x.bit_length()-1
   if q in piv:x^=piv[q]
   else:piv[q]=x;out.append(i);break
 return out

def solver(rows):
 piv={}
 for i,row in enumerate(np.asarray(rows,dtype=np.uint8)%2):
  x=sum(int(v)<<j for j,v in enumerate(row) if v);c=1<<i
  while x:
   q=x.bit_length()-1
   if q in piv:x^=piv[q][0];c^=piv[q][1]
   else:piv[q]=(x,c);break
 def ex(row):
  x=sum(int(v)<<j for j,v in enumerate(np.asarray(row,dtype=np.uint8)%2) if v);c=0
  for q in sorted(piv,reverse=True):
   if x>>q&1:x^=piv[q][0];c^=piv[q][1]
  return x,c
 return ex

def permrow(row,p):
 z=np.zeros_like(row)
 for i,j in enumerate(p):z[j]=row[i]
 return z

def actions(rows,perms):
 ex=solver(rows);k=len(rows);out=[]
 for p in perms:
  A=np.zeros((k,k),dtype=np.uint8)
  for j,row in enumerate(rows):
   rem,c=ex(permrow(row,p));assert rem==0
   for i in range(k):A[i,j]=(c>>i)&1
  out.append(A)
 return out

def hom_piv(Aacts,Bacts):
 n=Aacts[0].shape[0];m=Bacts[0].shape[0];N=m*n;piv={}
 for A,B in zip(Aacts,Bacts):
  for i in range(m):
   nz=np.flatnonzero(B[i])
   for j in range(n):
    row=0
    for a in nz:row^=1<<(int(a)*n+j)
    for bb in np.flatnonzero(A[:,j]):row^=1<<(i*n+int(bb))
    x=row
    while x:
     q=x.bit_length()-1
     if q in piv:x^=piv[q]
     else:piv[q]=x;break
 return piv,N

def one_null(piv,N):
 free=[i for i in range(N) if i not in piv];assert len(free)==1;x=1<<free[0]
 for q in sorted(piv):
  if ((piv[q]^(1<<q))&x).bit_count()&1:x|=1<<q
 return x

def hom(Aacts,Bacts):
 piv,N=hom_piv(Aacts,Bacts);d=N-len(piv);assert d==1;x=one_null(piv,N)
 n=Aacts[0].shape[0];m=Bacts[0].shape[0];X=np.zeros((m,n),dtype=np.uint8)
 for i in range(m):
  for j in range(n):X[i,j]=(x>>(i*n+j))&1
 return d,X

def main():
 b=build_base();g=build_group(b);E=b['E'];ei=b['ei'];pairs=sorted(b['pair_to_res'].items())
 O=np.zeros((270,360),dtype=np.uint8);B=np.zeros((270,45),dtype=int)
 for r,(ab,items) in enumerate(pairs):
  a,q=ab;B[r,a]=B[r,q]=1;z=0
  for m,_ in items:z^=m
  while z:
   lb=z&-z;O[r,lb.bit_length()-1]=1;z^=lb
 G=O.astype(int)@O.astype(int).T;X=(G==3).astype(int);np.fill_diagonal(X,0)
 Aint=np.vstack([X-2*np.eye(270,dtype=int),B.T]);assert 270-np.linalg.matrix_rank(Aint.astype(float))==60
 nullities={'F2':270-rankp(Aint,2),'F3':270-rankp(Aint,3),'F5':270-rankp(Aint,5)}
 assert nullities=={'F2':174,'F3':130,'F5':60}
 ns=sy.Matrix(Aint).nullspace();assert len(ns)==60;rows=[];dens=[]
 for v in ns:
  den=sy.ilcm(*[z.q for z in v]);a=[int(z*den) for z in v];gg=0
  for z in a:gg=math.gcd(gg,abs(z))
  rows.append([z//gg for z in a]);dens.append(int(den))
 L=np.array(rows,dtype=object);assert set(dens)=={3}
 redr={'F2':rankp(L,2),'F3':rankp(L,3),'F5':rankp(L,5)};assert redr=={'F2':60,'F3':14,'F5':60}
 L2=np.array(L,dtype=np.uint8)%2
 # Octahedron and H36-edge permutations.
 tri_index={frozenset(t):i for i,t in enumerate(b['tritangents'])};pi={frozenset(ab):i for i,(ab,_) in enumerate(pairs)}
 def tp(linep):return tuple(tri_index[frozenset(linep[x] for x in t)] for t in b['tritangents'])
 TPs=[tp(x) for x in g['gp']+[g['trans'][0]]]
 OP=[tuple(pi[frozenset((p[a],p[q]))] for a,q in [ab for ab,_ in pairs]) for p in TPs]
 LA=actions(L2,OP)
 # Binary K60 = kernel of shared-line projection on the rank90 octahedron row space.
 oi=indep_rows(O);OR=O[oi]%2;P=np.zeros((360,40),dtype=np.uint8)
 for e,(a,c) in enumerate(E):
  z=b['spreads'][b['iso_ds_sp'][a]]&b['spreads'][b['iso_ds_sp'][c]];assert len(z)==1;P[e,next(iter(z))]=1
 proj=(OR@P)%2;lam=nullp(proj.T,2);assert lam.shape==(60,90);K=(lam@OR)%2;assert rankp(K,2)==60
 EP=[]
 for dp in g['DPf']:
  EP.append(tuple(ei[tuple(sorted((dp[a],dp[c])))] for a,c in E))
 KA=actions(K,EP)
 dLK,fLK=hom(LA,KA);dKL,fKL=hom(KA,LA);rLK=rankp(fLK,2);rKL=rankp(fKL,2)
 assert (rLK,rKL)==(14,46) and not np.any((fLK@fKL)%2) and not np.any((fKL@fLK)%2)
 dLL,_=hom(LA,LA);dKK,_=hom(KA,KA);assert (dLL,dKK)==(1,1)
 # Pass5010 S14 check: the unique V20->K image equals im(L->K).
 vi=indep_rows(b['M']%2);V=(b['M'][vi]%2).astype(np.uint8);VA=actions(V,g['DPf']);_,fVK=hom(VA,KA)
 sameS=rankp(np.concatenate([fVK,fLK],axis=1),2)==14;assert sameS
 out={'pass':5017,'status':'PASS','real_V60_equations':'ker(X-2I) intersect ker(B_end^T)','rational_dimension':60,
  'equation_kernel_nullities':nullities,'primitive_integer_basis':{'vectors':60,'common_rational_denominator':3,'reduction_ranks':redr},
  'PGSp_Hom':{'L60_to_K60':{'dimension':dLK,'rank':rLK},'K60_to_L60':{'dimension':dKL,'rank':rKL},'End_L60':dLL,'End_K60':dKK,'both_compositions_zero':True},
  'S14_matches_Pass5010_V20_image':sameS,
  'exact_pair':'K60 has 0->S14->K60->Q46->0 while the mod2 real-lattice reduction L60 has the opposite 0->Q46->L60->S14->0',
  'theorem':'The canonical integral lattice inside the real octahedron V60 does not reduce to the binary K60 module. Instead the two full-PGSp modules are opposite nonsplit extensions of the same 14- and 46-dimensional factors. The unique L60->K60 map has rank14, the unique K60->L60 map has rank46, their compositions vanish, and both endomorphism rings are scalar. The rank14 image is exactly the Pass5010 S14 coming from V20.',
  'boundary':'Characteristic2 is singular for the defining eigen-equations (kernel174), so the 60-dimensional reduction is the primitive integral lattice reduction, not the full mod2 equation kernel. This is an explicit non-isomorphism/cross-extension theorem, not an identification of real and binary V60.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
