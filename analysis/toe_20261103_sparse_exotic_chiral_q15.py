#!/usr/bin/env python3
"""Construct an ACTUAL sparse 4D Wilson/overlap Hermitian kernel including
large exotic Q=15 on a 10^4-site flux torus. No large dense sign/eigensolve.
Small L3 spectrum gets full index and a sparse-vs-dense check.
"""
from pathlib import Path
import json,math,time
import numpy as np
from scipy import sparse as sp
from scipy.sparse.linalg import eigsh
ROOT=Path(__file__).resolve().parents[1]
def grammas():
 I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1])
 g=[np.kron(X,I),np.kron(Y,I),np.kron(Z,X),np.kron(Z,Y)]
 g5=g[0]@g[1]@g[2]@g[3]
 return g,g5
def kernel(L,charge,twist=None):
 n=L**4
 coords=np.indices((L,L,L,L)).reshape(4,-1).T
 ii=np.arange(n)
 g,g5=grammas();I4=np.eye(4,dtype=complex)
 if twist is None:twist=np.ones(n,complex)
 H=3*sp.eye(4*n,format='csr',dtype=complex)
 G=sp.kron(sp.eye(n,format='csr'),sp.csr_matrix(g5),format='csr')
 ident=sp.eye(n,format='csr')
 for mu in range(4):
  neigh=coords.copy();neigh[:,mu]=(neigh[:,mu]+1)%L
  jj=np.ravel_multi_index(neigh.T,(L,L,L,L))
  U=np.ones(n,dtype=complex)
  # Gauge field matches preexisting uncommitted 4D overlap producer:
  # in planes (0,1),(2,3), U_a=exp(-2pi i q x_b/L²)
  # on seam x_b=L-1, U_b=exp(+2pi i q x_a/L).
  if mu in (0,2):
   U*=np.exp(-2j*np.pi*charge*coords[:,mu+1]/(L*L))
  else:
   a=mu-1
   U[coords[:,mu]==L-1]*=np.exp(2j*np.pi*charge*coords[coords[:,mu]==L-1,a]/L)
  U*=twist[ii]*np.conjugate(twist[jj])
  T=sp.coo_matrix((U,(ii,jj)),shape=(n,n)).tocsr()
  # Construct Wilson W - m0=3I - sum forward+backward, then H=G(W-m0).
  H-=.5*sp.kron(T,sp.csr_matrix(I4-g[mu]),format='csr')
  H-=.5*sp.kron(T.getH(),sp.csr_matrix(I4+g[mu]),format='csr')
 H=(G@H).tocsr();H.sum_duplicates();H.eliminate_zeros()
 return H,coords
def one(L,q,spectrum=False,gauge_check=False):
 t0=time.perf_counter();H,_=kernel(L,q)
 delta=H-H.getH()
 hermitian_defect=float(max(abs(delta.data))) if delta.nnz else 0.
 n=H.shape[0]
 assert hermitian_defect<1e-12
 rr=np.random.default_rng(20261103)
 v=rr.standard_normal(n)+1j*rr.standard_normal(n)
 Hv=H@v
 max_hermitian_bilinear=abs(np.vdot(v,Hv)-np.vdot(Hv,v))
 out={'L':L,'charge_Q':q,'matrix_dimension':n,'nonzeros':int(H.nnz),
   'sparse_memory_MiB':(H.data.nbytes+H.indices.nbytes+H.indptr.nbytes)/2**20,
   'compared_dense_GiB':n*n*16/2**30,
   'hermitian_max_entry_defect':hermitian_defect,
   'complex_bilinear_self_adj_defect':float(max_hermitian_bilinear),
   'construction_seconds':time.perf_counter()-t0}
 if spectrum:
  lam=np.linalg.eigvalsh(H.toarray())
  index=int(round(-.5*sum(np.sign(lam))))
  out.update({'exact_dense_L3_index':index,'exact_dense_min_abs_eigen':float(min(abs(lam))),
   'exact_dense_eigensolve_seconds':time.perf_counter()-t0})
  sm=eigsh(H,k=2,which='SM',tol=1e-8,return_eigenvectors=False)
  out['sparse_min_abs_eigen_estimate']=float(min(abs(sm)))
  assert abs(out['sparse_min_abs_eigen_estimate']-out['exact_dense_min_abs_eigen'])<1e-6
  assert abs(index)==1
 if gauge_check:
  twist=np.exp(1j*rr.uniform(-np.pi,np.pi,size=L**4))
  Ht,_=kernel(L,q,twist)
  tg=np.repeat(twist,4)
  lhs=Ht@(tg*v);rhs=tg*(H@v)
  out['gauge_covariance_probe_relative_residual']=float(np.linalg.norm(lhs-rhs)/np.linalg.norm(lhs))
  assert out['gauge_covariance_probe_relative_residual']<1e-12
 return out
def main():
 out=[one(3,1,True,True),one(4,1,False,True),one(10,15,False,True)]
 print('SPARSE_Q15',json.dumps(out),flush=True)
 assert out[-1]['matrix_dimension']==40000 and out[-1]['sparse_memory_MiB']<100
 result={'status':'PASS_REAL_SPARSE_L10_Q15_WILSON_KERNEL_AND_SMALL_L_INDEX_GAUGE_CONTROL',
  'rows':out,
  'mathematical_context':'W gamma5-hermitian Wilson kernel H=gamma5(W-m0), m0=1, 4D periodic torus with U1 unit flux in 12 and34 planes. Multiplied links U^q for integer Q=3(B-L).',
  'scope':'ACTUAL sparse q=15 L10 Wilson kernel and its Hermiticity, memory. It is a prerequisite, NOT the L10 overlap SIGN, not the L10 topological index, not a chiral measure and no gauge+fermion path integral. L3 q1 dense full spectrum and index used to verify sparse construction against prior local mechanism. Charge q=15 links are within conservative plaquette phase benchmark. Dimensions are externally supplied 4D geometry.',
  'prior_local_source':'uncommitted analysis/toe_20261103_mechanism_four_dimensional_overlap.py is an earlier independent exact small-L construction, not claimed as our new result.',
  'literature':['https://doi.org/10.1103/756m-stz5']}
 (ROOT/'data/toe_20261103_sparse_exotic_chiral_q15.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
