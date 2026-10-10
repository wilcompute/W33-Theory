"""TOE37 track1. Native bipartite W33 fermion index versus artificial wall.
No unrequested Spin10 Weyl selection: compute singular spectrum/ranks
of native 40x40 Levi incidence and Euler index of 80x160 gradient.
"""
import json,sys,collections
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe26_css_matching_family import wilson
OUT=ROOT/'data/w33_20261010_toe37_native_chiral_index.json'
def rank3(A):
 a=np.asarray(A,dtype=np.int64).copy()%3;n,m=a.shape;rk=0
 for col in range(m):
  k=next((j for j in range(rk,n) if a[j,col]),None)
  if k is None:continue
  a[[rk,k]]=a[[k,rk]]
  a[rk]=a[rk]*pow(int(a[rk,col]),-1,3)%3
  for row in range(n):
   if row!=rk and a[row,col]:a[row]=(a[row]-a[row,col]*a[rk])%3
  rk+=1
 return rk
def run(write=True):
 edges,D,C=wilson()
 F=np.zeros((40,40),dtype=np.int64)
 for p,l in edges:F[p,l-40]=1
 assert int(np.sum(F))==160
 assert set(F.sum(axis=0))=={4} and set(F.sum(axis=1))=={4}
 s=np.linalg.svd(F.astype(float),compute_uv=False)
 sings=dict(four=int(np.sum(abs(s-4)<1e-8)),
  sqrt_six=int(np.sum(abs(s-np.sqrt(6))<1e-8)),
  zero=int(np.sum(s<1e-8)))
 assert sings==dict(four=1,sqrt_six=24,zero=15),sings
 rr=int(np.linalg.matrix_rank(F));r3=rank3(F)
 assert rr==25
 native_index=(40-rr)-(40-rr)
 assert native_index==0
 edge_grad=D.T
 real_grad_rank=int(np.linalg.matrix_rank(edge_grad.astype(float)))
 assert real_grad_rank==79
 H0=80-real_grad_rank;H1=160-real_grad_rank
 assert (H0,H1)==(1,81)
 # 3-fold and all other finite covers retain vertex-edge difference -80p.
 out=dict(status='PASS',W33_Levi_points=40,lines=40,incidence_edges=160,
   incidence_shape=[40,40],incidence_singular_values_multiplicity=sings,
   incidence_real_rank=rr,incidence_F3_rank=r3,
   left_hand_kernel_dimension=15,right_hand_kernel_dimension=15,
   native_point_line_chiral_Fredholm_index=native_index,
   levi_0_1_cochain_kernel_dimensions=dict(H0=H0,H1=H1),
   levi_Euler_characteristic=80-160,
   extra_W33_cover_Euler_char_formula='80p-160p=-80p for any degree-p covering of the Levi graph',
   contrast='The -80p vertex/edge de Rham index is an Euler-cochain count, NOT 80p Weyl fermions or 3 families. The native 40x40 bipartite fermionic point-line hopping has EXACTLY balanced 15+15 zero modes and index0. Round36 rectangular Q index+1 requires an externally unbalanced boundary.',
   no_go_scope='No net chirality from finite balanced point/line incidence hopping or finite native graph cochain index alone. Nontrivial chiral edge/bulk index with extra geometry, flux, nonlinear interactions and boundary conditions remains possible; those have not been derived from W33.')
 if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
 print('TOE37 index 0 singulars',sings,'F3 rank',r3,'Euler',(H0,H1),flush=True)
 return out
if __name__=='__main__':run()
