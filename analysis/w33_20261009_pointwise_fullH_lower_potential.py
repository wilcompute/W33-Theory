"""A pointwise (position-dependent) lower-form bound for the actual
160-current W33 Hamiltonian, independent of quantum trial truncations.

For psi smooth, J_e psi=(V_e.q+a)*(U_e.P+a)psi and U_e.V_e=0.
Writing z_e=(V_e.q+a), p=Ppsi/psi, the quadratic polynomial in p
is minimized at each q. This is valid also where psi=0 by continuity.

The exact simpler scalar barrier follows from sum_e U_e=0:
 V_C(q)=(160a)^2 / sum_e |z_e|^{-2}; set zero at any z_e=0.
For all Schwartz psi: <psi,H psi> >= int V_C(q)|psi|².
It is not a uniform positive E0 bound since V_C(q0)=0.
"""
from pathlib import Path
import json,sys
import numpy as np
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11769_quantized_current_vacuum as W
def certificate():
 g=W.geometry();U=np.rint(40*g['u']).astype('int64');V=np.rint(40*g['v']).astype('int64')
 assert np.max(abs(U.sum(axis=0)))==0
 assert np.max(abs(np.sum(U*V,axis=1)))==0
 assert all(int(r@r)==3120 for r in U)
 a=1/np.sqrt(20)
 qzero=np.zeros(80)
 qclass=np.r_[np.array([39]+[-1]*39,dtype=float),np.zeros(40)]*a
 points=[('origin',qzero),('principal_symbol_zero',qclass)]
 rng=np.random.default_rng(31)
 points.extend([('sample_'+str(i),rng.normal(size=80)*s) for i,s in enumerate((.1,.5,1.,2.))])
 output=[]
 for name,q in points:
  z=V@q/40+a
  inactive=int(np.sum(abs(z)<1e-9))
  if inactive:
   naive=0.
  else:
   naive=(160*a)**2 /np.sum(z**-2)
  weighted=z[:,None]*U/40
  v=z*a
  # the exact optimized pointwise quadratic minimum:
  coeff,res,rank,singular=np.linalg.lstsq(weighted,-v,rcond=1e-12)
  opt=float(np.linalg.norm(weighted@coeff+v)**2)
  assert opt>=naive-1e-7*max(1,opt),(name,opt,naive)
  if name=='origin':
   assert abs(opt-.4)<1e-10 and abs(naive-.4)<1e-10
  if name=='principal_symbol_zero':
   assert inactive==156 and opt<1e-9
  output.append(dict(point=name,inactive_currents=inactive,naive_barrier=naive,
    optimal_barrier_numerical=opt,transport_weighted_rank=int(rank),
    norm_q=float(np.linalg.norm(q))))
 return dict(status='PASS',current_count=160,parameter_a_square='1/20',
    exact_at_q_origin='V_C(0)=V_opt(0)=160*a^4=2/5',
    no_positive_uniform_bound_from_position_barrier='V_C(q0)=V_opt(q0)=0 on known classical zero, so inf_q V=0',
    exact_scalar_barrier='V_C(q)=(160*a)^2/(sum_e (V_e.q+a)^(-2)); define V_C=0 on affine-factor hyperplanes',
    sharp_scalar_barrier='V_opt(q)=a² min_{p in R^78}sum_e (V_e.q+a)²*(U_e.p+1)²',
    theorem='For every Schwartz psi, sum_e ||(V_e.q+a)(U_e.P+a)psi||² >= integral V_opt(q)|psi(q)|² dq >= integral V_C(q)|psi(q)|² dq, exactly by a pointwise real least-squares completion and Cauchy using sum U_e=0. The bound is independent of PSp ground representation and does not imply global E0>0 numerically.',
    provenance='Prior Pass11778 already proves compact resolvent and qualitative strict E0>0; this pass adds a position-dependent constructive lower-form estimate, not that global theorem.',
    samples=output)
if __name__=='__main__':
 d=certificate()
 (ROOT/'data/w33_20261009_pointwise_fullH_lower_potential.json').write_text(json.dumps(d,indent=2)+'\n')
 print('LOCAL LOWER',[(x['point'],round(x['naive_barrier'],8),round(x['optimal_barrier_numerical'],8)) for x in d['samples']])
