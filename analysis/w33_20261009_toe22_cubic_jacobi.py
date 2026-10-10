import json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_pass1081_1086_core import build_w33,transvection_perm,outer_similitude_perm,enumerate_group,compose,line_perm
from w33_20261009_toe_integral_clique_levi_bridge import chain,integer_cycle_basis
OUT=ROOT/'data/w33_20261009_toe22_cubic_jacobi.json'
P=101
def inverse_mod(A,p):
 A=np.asarray(A,dtype=np.int64)%p;n=len(A)
 B=np.concatenate((A,np.eye(n,dtype=np.int64)),axis=1)
 for k in range(n):
  i=next(i for i in range(k,n) if B[i,k])
  B[[k,i]]=B[[i,k]]
  B[k]=B[k]*pow(int(B[k,k]),-1,p)%p
  for j in range(n):
   if j!=k and B[j,k]:B[j]=(B[j]-B[j,k]*B[k])%p
 assert np.array_equal(A@B[:,n:]%p,np.eye(n,dtype=np.int64))
 return B[:,n:]
def actions():
 pts,idx,lines,lidx,pl,frames,fidx,flags,fi=build_w33()
 gs=[transvection_perm(pts[i],pts,idx) for i in (0,1,4,5,13)]
 G,_=enumerate_group(gs);outer=outer_similitude_perm(pts,idx)
 acts=np.empty((51840,160),dtype=np.uint8)
 for k,g in enumerate(G):
  for shift,h in enumerate((g,compose(outer,g))):
   lp=line_perm(h,lines,lidx)
   acts[k+shift*len(G)]=[fi[(h[p],lp[l])] for p,l in flags]
 return acts
def orbit_form(act,seed):
 vals=act[:,seed].astype(np.int32);ordered=np.sort(vals,axis=1)
 signs=1-2*(((vals[:,0]>vals[:,1]).astype(int)+(vals[:,0]>vals[:,2]).astype(int)+(vals[:,1]>vals[:,2]).astype(int))%2)
 keys=(ordered[:,0].astype(np.int64)*160+ordered[:,1])*160+ordered[:,2]
 u,inv=np.unique(keys,return_inverse=True)
 weights=np.bincount(inv,weights=signs).astype(np.int64)
 nz=weights!=0
 abc=np.column_stack((u[nz]//25600,(u[nz]//160)%160,u[nz]%160))
 return abc,weights[nz]
def value(abc,wt,u,v,w):
 a,b,c=abc.T
 return int(np.dot(wt,
 u[a]*(v[b]*w[c]-v[c]*w[b])
 -u[b]*(v[a]*w[c]-v[c]*w[a])
 +u[c]*(v[a]*w[b]-v[b]*w[a])))
def contract(abc,wt,u,v):
 a,b,c=abc.T
 out=np.zeros(160,dtype=np.int64)
 np.add.at(out,a,wt*(u[b]*v[c]-u[c]*v[b]))
 np.add.at(out,b,wt*(u[c]*v[a]-u[a]*v[c]))
 np.add.at(out,c,wt*(u[a]*v[b]-u[b]*v[a]))
 return out
def run():
 _,_,_,_,_,_,flags,_,_,_,D,M,R=chain()
 Z,chords=integer_cycle_basis(flags)
 act=actions()
 rng=np.random.default_rng(2209)
 probes=[tuple(Z@rng.integers(-2,3,size=81,dtype=np.int64) for j in range(3)) for i in range(3)]
 chosen=None
 for step in range(180):
  seed=rng.choice(160,3,replace=False)
  abc,wt=orbit_form(act,seed)
  if not len(wt):continue
  vals=[value(abc,wt,*u) for u in probes]
  if any(vals):
   chosen=(seed,abc,wt,vals);break
 assert chosen is not None
 seed,abc,wt,vals=chosen
 print('CUBIC NONZERO',seed,'terms',len(wt),'sample',vals,flush=True)
 # Independent exact invariance under representative generating permutations
 u,v,z=probes[0]
 original=value(abc,wt,u,v,z)
 for row in (1,2,4,7,25920):
  perm=act[row].astype(int)
  uu=np.empty(160,dtype=np.int64);vv=uu.copy();zz=uu.copy()
  uu[perm]=u;vv[perm]=v;zz[perm]=z
  assert value(abc,wt,uu,vv,zz)==original
 G=Z.T@Z;Inv=inverse_mod(G,P)
 ZZ=Z%P;w=wt%P
 def bracket(x,y):
  co=contract(abc,w,(ZZ@x)%P,(ZZ@y)%P)%P
  return (Inv@(ZZ.T@co%P))%P
 out=[]
 for i in range(8):
  x,y,z=[rng.integers(0,P,size=81,dtype=np.int64) for t in range(3)]
  jac=(bracket(bracket(x,y),z)+bracket(bracket(y,z),x)+bracket(bracket(z,x),y))%P
  out.append({'case':i,'nonzero':int(np.count_nonzero(jac)),'first8':jac[:8].tolist()})
  print('JACOBI',i,out[-1]['nonzero'],flush=True)
 assert out[0]['nonzero']>0
 # Supply a tiny, explicit coordinate-basis triple with exact nonzero Jacobi
 basis=np.eye(81,dtype=np.int64)
 simple=None
 for case in range(80):
  i,j,k=sorted(rng.choice(81,3,replace=False))
  q=(bracket(bracket(basis[i],basis[j]),basis[k])+bracket(bracket(basis[j],basis[k]),basis[i])+bracket(bracket(basis[k],basis[i]),basis[j]))%P
  if np.any(q):
   simple={'cycle_basis_indices':[int(i),int(j),int(k)],'jacobi_first16':q[:16].tolist(),'nonzero_entries':int(np.count_nonzero(q))};break
 assert simple is not None
 rec={'status':'PASS_JACOBI_OBSTRUCTION','group_order':51840,
 'unique_alternating_cubic_prior_dimension':1,
 'seed_triple':[int(v) for v in seed],
 'orbit_nonzero_flag_triples':len(wt),'evaluations':vals,
 'jacobi_mod_prime':P,'jacobi_witnesses':out,'elementary_cycle_Jacobi_witness':simple,
 'independent_full_form_symmetry_checks':5,
 'proof':'The unique (by prior character census) PGSp-invariant alternating cubic is constructed as a signed Reynolds orbit of a flag triple. Restriction to the 81 cycle lattice is nonzero, as witnessed by integer evaluations. Raising one index using integral cycle Gram defines an equivariant antisymmetric bracket on 81 modes. Exact nonzero Jacobi vector modulo101 disproves the rational Jacobi identity (Gram invertible mod101).',
 'boundary':'This excludes the 81-only Gram-dual bracket, NOT the larger E8 Z3-graded algebra with extra E6+A2 adjoint channels. More mixed interaction tensors remain necessary.'}
 OUT.write_text(json.dumps(rec,indent=2)+'\n')
 return rec
if __name__=='__main__':run()
