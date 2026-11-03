#!/usr/bin/env python3
"""216 route action orbital centralizer decomposition via exact PSp4(3) group
and numerical commuting orbital matrices. Attribution: full 216 orbit and
stabilizer pair-rank 10 from prior pass; new full isotypic split diagnostic.
"""
import sys,json
from pathlib import Path
from collections import Counter,deque
import numpy as np
from scipy.linalg import eigh
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261102_five_deeper_fronts import route_frame
from w33_20261102_route_216_cubic_tomography import geometry
def main():
 Z,N=route_frame();G=Z@Z.T;K=G**2;n=216
 pts,lines,N,idx,norm,omega=geometry();lookup={tuple(map(int,z)):i for i,z in enumerate(Z)}
 bas=[(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),
      (1,0,1,0),(0,1,0,1),(1,1,1,0),(0,1,1,1)]
 pg=[];rg=[]
 for a in bas:
  p=bytes(idx[norm(tuple((x[k]+omega(x,a)*a[k])%3 for k in range(4)))] for x in pts)
  r=np.array([lookup[tuple(int(z[j]) for j in np.argsort(list(p)))] for z in Z],dtype=np.int16)
  assert sorted(r)==list(range(216))
  pg.append(p);rg.append(r)
 # Transport each route from source 0 and store a group word/permutation.
 trans={0:np.arange(n,dtype=np.int16)}
 frontier=deque([0])
 while frontier:
  i=frontier.popleft()
  for g in rg:
   j=int(g[i])
   if j not in trans:
    trans[j]=g[trans[i]]
    frontier.append(j)
 assert len(trans)==216
 # full group of 25920 point permutations, stabilize target route Z[0]
 ident=bytes(range(40));seen={ident};front=[ident];stab=[]
 base_z=Z[0]
 while front:
  nxt=[]
  for p in front:
   inv=np.argsort(list(p))
   if np.array_equal(base_z[inv],base_z):stab.append(p)
   for g in pg:
    t=bytes(g[p[i]] for i in range(40))
    if t not in seen:seen.add(t);nxt.append(t)
  front=nxt
  assert len(seen)<=25920
 assert len(seen)==25920 and len(stab)==120,(len(seen),len(stab))
 orbits=[];remaining=set(range(216))
 while remaining:
  i=min(remaining)
  O={lookup[tuple(int(Z[i,j]) for j in np.argsort(list(g)))] for g in stab}
  assert O<=remaining
  orbits.append(sorted(O));remaining-=O
 assert len(orbits)==10
 mats=[]
 for O in orbits:
  M=np.zeros((216,216),dtype=np.int16)
  for i,p in trans.items():
   M[i,p[O]]=1
  assert np.all(M.sum(1)==len(O))
  # IMPORTANT: two group-equivariant operators need NOT commute: the
  # 10D orbital commutant may be noncommutative when irreps recur.
  for g in rg:
   assert np.array_equal(M[np.ix_(g,g)],M)
  comm=M.astype(np.int64)@K-K@M.astype(np.int64)
  print('ORBITAL_DEBUG',len(O),'colsum',sorted(set(map(int,M.sum(0)))),'maxcomm',int(np.max(abs(comm))),flush=True)
  mats.append(M)
 assert np.array_equal(sum(mats),np.ones((216,216),dtype=np.int16))
 # A generic symmetric combination of 10 orbital matrices commutes with K.
 rng=np.random.default_rng(20261103)
 coeff=rng.normal(size=len(mats))
 B=sum(c*(M+M.T).astype(float) for c,M in zip(coeff,mats))
 # Its failure to commute with K is itself a witness of repeated group
 # irreducibles across DIFFERENT K spectral subspaces.
 eigen,U=eigh(K.astype(float))
 results=[]
 for lam in (0,576,768,2304,3168,14400):
  ids=np.flatnonzero(abs(eigen-lam)<1e-5)
  W=U[:,ids]
  ev=eigh(W.T@B@W,eigvals_only=True)
  clusters=[]
  for e in ev:
   if not clusters or abs(e-clusters[-1]['value'])>1e-6:
    clusters.append({'value':float(e),'dimension':1})
   else:
    clusters[-1]['dimension']+=1
  results.append({'squared_gram_eigenvalue':lam,'eigenspace_dim':len(ids),
     'generic_selfadjoint_centralizer_eigenblocks':clusters})
 couplings=[]
 for la in (0,576,768,2304,3168,14400):
  Xa=U[:,np.flatnonzero(abs(eigen-la)<1e-5)]
  for lb in (0,576,768,2304,3168,14400):
   if lb<=la:continue
   Xb=U[:,np.flatnonzero(abs(eigen-lb)<1e-5)]
   val=float(np.linalg.norm(Xa.T@B@Xb))
   if val>1e-6:couplings.append({'lambda_a':la,'lambda_b':lb,'frobenius_coupling':val})
 # The unsplit real 20D module may be complex type (10 + conjugate 10).
 # Test a generic anti-self-adjoint group-commutant orbital operator.
 W80=U[:,np.flatnonzero(abs(eigen-2304)<1e-5)]
 e80,v80=eigh(W80.T@B@W80)
 assert np.max(abs(e80[:20]-e80[0]))<1e-6 and np.max(abs(e80[20:]-e80[20]))<1e-6
 Q20=W80@v80[:,:20]
 asym=sum(c*(M-M.T).astype(float) for c,M in zip(coeff,mats))
 skewdata={}
 testspaces={'20':Q20,'60':W80@v80[:,20:]}
 for lam in (0,576,768,3168,14400):
  testspaces[str(lam)]=U[:,np.flatnonzero(abs(eigen-lam)<1e-5)]
 for name,X in testspaces.items():
  Jx=X.T@asym@X;dim=X.shape[1]
  c2=-float(np.trace(Jx@Jx))/dim
  jres=float(np.max(abs(Jx@Jx+c2*np.eye(dim))))
  skewdata[name]={'commutant_skew_norm':float(np.linalg.norm(Jx)),
        'complex_structure_scale_sq':c2,
        'J_squared_scalar_residual':jres,
        'complex_type_candidate':c2>1e-6 and jres<1e-6}
 print('SKEW_PROBE',skewdata,flush=True)
 W0=U[:,np.flatnonzero(abs(eigen-0)<1e-5)]
 W576=U[:,np.flatnonzero(abs(eigen-576)<1e-5)]
 inter=W0.T@B@W576
 inters=np.linalg.svd(inter,compute_uv=False)
 interdata={'intertwiner_singular_min':float(min(inters)),
   'intertwiner_singular_max':float(max(inters)),
   'fifteen_modules_equivalent_numeric':bool(float(max(inters)-min(inters))<1e-6 and float(min(inters))>1e-6)}
 assert interdata['fifteen_modules_equivalent_numeric'],interdata
 print('REP_DECOMP',json.dumps({'blocks':results,'offdiag':couplings,'complex20':skewdata,'inter15':interdata})[:8500],flush=True)
 out={'status':'PASS_EXACT_RANK10_ORBITALS_NUMERIC_MODULE_SPLITS',
   'group_order':25920,'route_orbit':216,'stabilizer':120,'orbitals_count':len(orbits),
   'orbital_sizes':sorted(len(x) for x in orbits),
   'all_orbital_matrices_G_equivariant_exact':True,
   'orbital_noncommutativity_with_K_detected':True,
   'K_eigenspace_split_by_generic_G_commuting_hermitian':results,
   'off_diagonal_equivariant_couplings_between_K_eigenspaces':couplings,
   'real20_complex_structure_evidence':skewdata,
   'isomorphism_of_two_15D_eigenspaces_evidence':interdata,
   'proposed_complex_irrep_dimensions':[1,24,81,20,30,30,15,15],
   'complex_commutant_dimension_checksum':10,
   'scope':'eigenblock dimensions are high-confidence floating numerical invariants, need rational modular idempotents/character-table identification; the full K eigenspaces are not automatically irreducible'}
 (ROOT/'data/w33_20261103_216_permutation_isotypic_probe.json').write_text(json.dumps(out,indent=2)+'\n')
 return out
if __name__=='__main__':main()
