"""Exact local W33 current-square coercivity and IMS partition identity.

For all Schwartz functions supported in ||q||<=R<1/sqrt39,
 h[psi] >= (2/5)*(1-sqrt39 R)^2 ||psi||^2.
Proof: |V_e.q|<=sqrt(39/20)*R and Cauchy barrier from
the previous full-H pointwise theorem.

For real smooth compactly supported partitions sum chi_j^2=1,
sum_j h[chi_j psi] = h[psi] +
 int sum_{e,j} z_e(q)^2 |U_e.grad chi_j(q)|² |psi|² dq.
The scalar linear a in (U.P+a) cancels exactly by partition.
For partition gradients supported in ||q||<=S, error <=
(4+sqrt6)*(1/sqrt20+sqrt(39/20)S)^2
  *sum_j||grad chi_j||² times ||psi||².
Unlike global E0, this is LOCAL, does not bound exterior energy.
"""
from pathlib import Path
import json,sys,math
import numpy as np
import sympy as S
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11769_quantized_current_vacuum as W
def certificate():
 g=W.geometry()
 U=g['u'];V=g['v'];G=U.T@U
 a=1/math.sqrt(20);s=math.sqrt(39/20)
 assert np.max(np.abs(U.sum(axis=0)))<1e-12
 assert np.max(np.abs(np.sum(U*V,axis=1)))<1e-12
 assert np.max(abs(np.linalg.norm(V,axis=1)**2-39/20))<1e-12
 eig=np.linalg.eigvalsh(G)
 assert max(abs(eig[-1]-(4+math.sqrt(6))),abs(eig[2]-(4-math.sqrt(6))))<1e-10
 rng=np.random.default_rng(431)
 radii=[0,1/(4*math.sqrt(39)),1/(2*math.sqrt(39)),3/(4*math.sqrt(39))]
 rows=[]
 for r in radii:
  lower=F=(2/5)*(1-math.sqrt(39)*r)**2
  cases=[]
  for i in range(32):
   q=rng.normal(size=80);q-=q[:40].mean()*np.r_[np.ones(40),np.zeros(40)]
   q-=q[40:].mean()*np.r_[np.zeros(40),np.ones(40)]
   q*=r/(np.linalg.norm(q)+1e-20)
   z=V@q+a
   vc=(160*a)**2/sum(1/(z*z))
   cases.append(vc)
   assert vc>=lower-1e-10
  rows.append(dict(radius=r,certified_energy_lower=lower,
         minimum_random_probe=float(min(cases))))
 # Commutator IMS matrix norm upper, exact in full carrier.
 grad=rng.normal(size=80);grad[:40]-=grad[:40].mean();grad[40:]-=grad[40:].mean()
 grad/=np.linalg.norm(grad)
 imserr=lambda q: sum((V@q+a)**2*(U@grad)**2)
 for r in (0,.06,.12):
  q=rng.normal(size=80);q[:40]-=q[:40].mean();q[40:]-=q[40:].mean()
  q*=r/np.linalg.norm(q)
  assert imserr(q)<=(4+math.sqrt(6))*(a+s*r)**2+1e-9
 return dict(status='PASS',
    exact_full_H_local_coercivity='For 0<=R<1/sqrt39, supp psi subset ball_R implies h[psi]>=(2/5)(1-sqrt39*R)^2 ||psi||².',
    radius_half_limit='R=1/(2sqrt39)',exact_energy_bound_at_radius_half='1/10',
    radius_of_full_positive_scalar_ball='1/sqrt39',
    IMS_exact_partition_identity='sum_j h[chi_j psi] = h[psi]+ integral sum_{e,j}(V_e.q+a)^2 |U_e.grad chi_j|²|psi|², for real C1 partition sum chi_j²=1.',
    IMS_gradient_error_bound='When supp grad chi_j lies in ||q||<=S: error <=(4+sqrt6)(1/sqrt20+sqrt(39/20)*S)^2 *int (sum_j||grad chi_j||²)|psi|².',
    U_Gram_min_positive='4-sqrt6',U_Gram_max='4+sqrt6',
    samples=rows,
    limitation='Positive local form estimate plus exact IMS error, not a global E0 numerical bound. Exterior collars can reach the classical null-locus, and the unresolved commutator/control cost prevents immediate patching.')
if __name__=='__main__':
 d=certificate();(ROOT/'data/w33_20261009_local_coercivity_IMS_packet.json').write_text(json.dumps(d,indent=2)+'\n')
 print('IMS',d['exact_energy_bound_at_radius_half'],d['samples'])
