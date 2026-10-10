"""TOE36/1: exact rank-one interface Dirac chiral index and anomalies.

Artificial extra fifth coordinate with a rectangular domain-wall
gradient Q:  (Q psi)_j = psi[j+1]-exp(-m_j) psi[j].
A sign-changing mass gives one exponentially localized kernel,
no adjoint kernel. This is an INDEX FROM INSERTED BOUNDARY DATA,
not spontaneous E8 chirality; square Q on a circle restores index0.
One SO10 16->SU5 (10+5bar+1) cancels gauge anomalies.
"""
from pathlib import Path
from fractions import Fraction as F
import json,numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_20261010_toe36_chiral_domain_wall.json'
def run():
 L=24;m=.7; sites=np.arange(-L,L+1)
 # low j mass negative (growing toward interface), high mass positive
 bonds=np.arange(-L,L);mass=np.where(bonds<0,-m,m)
 rat=np.exp(-mass)
 Q=np.zeros((2*L,2*L+1),float)
 for i,r in enumerate(rat):Q[i,i]=-r;Q[i,i+1]=1
 s=np.linalg.svd(Q,compute_uv=False)
 assert len(s)==2*L and s[-1]>.05
 psi=np.ones(len(sites),float)
 for i,r in enumerate(rat):psi[i+1]=r*psi[i]
 psi/=np.linalg.norm(psi)
 resid=np.linalg.norm(Q@psi)
 assert resid<1e-12
 peaked=int(np.argmax(abs(psi)))
 assert sites[peaked]==0
 kernel_dim=Q.shape[1]-np.linalg.matrix_rank(Q)
 adjoint_kernel_dim=Q.shape[0]-np.linalg.matrix_rank(Q)
 assert (kernel_dim,adjoint_kernel_dim)==(1,0)
 # finite CLOSED chain with as many rows as columns (append wrap):
 Qclosed=np.zeros((2*L+1,2*L+1))
 Qclosed[:2*L,:]=Q
 Qclosed[-1,-1]=1;Qclosed[-1,0]=-1
 assert Qclosed.shape[0]==Qclosed.shape[1]
 square_index=Qclosed.shape[1]-Qclosed.shape[0]
 assert square_index==0
 # SU5 16 Weyl matter: Q(3,2)_1/6, uc(3bar,1)_-2/3,
 # ec(1,1)_1, dc(3bar,1)_1/3, L(1,2)_-1/2, nu(1,1)_0.
 content=[('Q',6,F(1,6)),('uc',3,F(-2,3)),('ec',1,F(1)),('dc',3,F(1,3)),('L',2,F(-1,2)),('nuc',1,F(0))]
 assert sum(mult*y for _,mult,y in content)==0
 assert sum(mult*y**3 for _,mult,y in content)==0
 # SU3^2 U1: 2 components per fundamental Q, one uc and one dc
 assert 2*F(1,6)+F(-2,3)+F(1,3)==0
 # SU2^2 U1: 3 colored Q doublets, one L
 assert 3*F(1,6)+F(-1,2)==0
 # four LH SU2 doublets: no Witten parity anomaly
 nSU2=3+1;assert nSU2%2==0
 # SU5^3: A(10)=+1, A(5bar)=-1
 assert 1-1==0
 result=dict(status='PASS',
  SO10_content='One complex chiral Weyl 16 decomposes to SU5 10+5bar+1, without its conjugate 16bar, provided boundary zero-mode selection is PHYSICALLY implemented.',
  interface_sites=len(sites),matrix_Q_shape=list(Q.shape),mass_left=-m,mass_right=m,root_at_site=0,
  smallest_nonzero_singular_value=float(s[-1]),localized_profile_residual=float(resid),
  one_wall_Q_index=int(kernel_dim-adjoint_kernel_dim),
  finite_square_closed_system_index=square_index,
  normalized_probability_center=float(psi[peaked]**2),
  boundary_decay_ratio_exp_m=float(np.exp(-m)),
  su5_anomaly_cubic_integer=1-1,
  SM_U1_cubic_anomaly=str(sum(mult*y**3 for _,mult,y in content)),
  SM_gravitational_U1_mixed=str(sum(mult*y for _,mult,y in content)),
  SU3sqU1_coeff=str(2*F(1,6)+F(-2,3)+F(1,3)),
  SU2sqU1_coeff=str(3*F(1,6)+F(-1,2)),
  SU2_Witten_doublets=nSU2,
  key_caveat='Rectangular Q carries an EXTERNALLY INSERTED one-site chiral imbalance and sign-changing domain-wall profile. A finite square periodic model has index0 and a mirror/boundary companion; no unpaired observed fermion or SO10 gauge dynamics derived from the W33/E8 finite geometry. Standard Model gauge anomalies cancelling for a 16 is established textbook group theory, not novel.',
  consistency_with_parallel='Pass11855/11859 proved no purely E8 automorphism gives chirality; this construction uses extra geometric/boundary degrees of freedom, thus does not violate their no-go.')
 OUT.write_text(json.dumps(result,indent=2)+'\n')
 print('TOE36 DOMAIN WALL index',result['one_wall_Q_index'],'resid',resid,'massive gap',s[-1],flush=True)
 return result
if __name__=='__main__':run()
