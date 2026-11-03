#!/usr/bin/env python3
"""Finite-field exact certificate: 15D blind W33 POVM module is absolutely
irreducible. Uses two primes with char not dividing |PSp4(3)|=25920.
"""
import sys,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261102_five_deeper_fronts import route_frame
from w33_20261102_route_216_cubic_tomography import geometry
def reduce_mod(A,p,full=False):
 A=(np.array(A,dtype=np.int64)%p).copy()
 m,n=A.shape;r=0;piv=[]
 for j in range(n):
  ii=np.flatnonzero(A[r:,j])
  if not len(ii):continue
  k=r+int(ii[0]);A[[r,k]]=A[[k,r]]
  inv=pow(int(A[r,j]),-1,p)
  A[r,j:]=(A[r,j:]*inv)%p
  if full:ids=np.array([i for i in range(m) if i!=r and A[i,j]],dtype=np.int64)
  else:ids=np.flatnonzero(A[r+1:,j])+r+1
  if len(ids):
   f=A[ids,j].copy()
   A[ids,j:]=(A[ids,j:]-f[:,None]*A[r,j:][None,:])%p
  piv.append(j);r+=1
  if r==min(m,n):break
 return A,piv
def run(p,Z,perms):
 K=(Z@Z.T)**2
 A,piv=reduce_mod(K,p,True)
 assert len(piv)==201
 free=[j for j in range(216) if j not in set(piv)]
 assert len(free)==15
 B=np.zeros((216,15),dtype=np.int64)
 B[free,np.arange(15)]=1
 B[piv,:]=(-A[np.arange(len(piv))[:,None],np.array(free)[None,:]])%p
 assert np.array_equal((K@B)%p,np.zeros((216,15),dtype=np.int64))
 I=np.eye(15,dtype=np.int64)
 # centralizer constraints, exactly over GF(p)
 D=[]
 for pi in perms:
  acted=B[pi]
  R=acted[free]
  assert np.array_equal((B@R-acted)%p,np.zeros_like(B))
  D.append((np.kron(I,R)-np.kron(R.T,I))%p)
 D=np.vstack(D)
 _,cols=reduce_mod(D,p,False)
 rank=len(cols)
 assert rank<=224 # identity always lies in commutant
 return dict(prime=p,modular_nullity_of_K=15,commutant_matrix_shape=list(D.shape),
   centralizer_rank_mod_prime=rank,centralizer_dimension_mod_prime=225-rank,
   absolutely_irreducible_certified=rank==224)
def main():
 Z,_=route_frame();pts,lines,N,idx,norm,omega=geometry()
 lookup={tuple(int(v) for v in z):i for i,z in enumerate(Z)}
 bas=[(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),
      (1,0,1,0),(0,1,0,1),(1,1,1,0),(0,1,1,1)]
 perm=[]
 for a in bas:
  g=np.array([idx[norm(tuple((x[k]+omega(x,a)*a[k])%3 for k in range(4)))] for x in pts])
  pi=np.array([lookup[tuple(int(z[j]) for j in np.argsort(g))] for z in Z],dtype=np.int64)
  assert len(set(pi))==216
  perm.append(pi)
 reports=[run(p,Z,perm) for p in (101,103)]
 out={"status":"PASS_EXACT_ABSOLUTE_IRREDUCIBILITY" if all(r["absolutely_irreducible_certified"] for r in reports) else "FAIL",
     "group_order":25920,"module_dimension":15,
     "field_checks":reports,
     "logic":"Kernel of exact K (rank201), induced transvection permutations; solve X R_g=R_g X over F_p. Rank224 of 225 constraints leaves scalars only. Because p does not divide |G| and rational kernel dimension agrees, a 1D modular commutant bounds complex commutant dimension by 1.",
     "scope":"irreducible outcome-kernel PSp(4,3) representation; does not imply POVM informational completeness or physical protection"}
 print(json.dumps(out,indent=2),flush=True)
 (ROOT/"data/w33_20261102_exact_blind_irreducibility.json").write_text(json.dumps(out,indent=2)+"\n")
 return out
if __name__=="__main__":main()
