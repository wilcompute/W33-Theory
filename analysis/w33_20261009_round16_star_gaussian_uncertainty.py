"""Round16 Gaussian uncertainty audit of classical 80 star zero planes:
Every classical current vanishes at (q_star,p_star), yet a scalar
isotropic coherent Gaussian centered there has high expected quantum
energy. Analytic minimization over width sigma yields a reproducible
upper bound on E0, NOT an actual eigenvalue or LOWER bound.

|psi|^2 covariance sigma² I/2 and momentum covariance I/(2sigma²);
U_e.V_e=0, so the commuting quadratures factor in Wick calculus:
sum_e <J_e²> = A/sigma²+B sigma²+C, when center H_cl=0.
"""
from pathlib import Path
import json,sys,math
from fractions import Fraction as F
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11769_quantized_current_vacuum as H
def certificate():
 g=H.geometry()
 U=np.rint(40*g['u']).astype(np.int64)
 V=np.rint(40*g['v']).astype(np.int64)
 U2=[F(int(z@z),1600) for z in U];V2=[F(int(z@z),1600) for z in V]
 assert U2==V2==[F(39,20)]*160
 vals=[]
 for e in range(80):
  qi=np.zeros(80,dtype=np.int64)
  if e<40:qi[:40]=-1;qi[e]=39
  else:qi[40:]=1;qi[e]=-39
  X=V@qi+40
  active=np.flatnonzero(X)
  assert len(active)==4
  pnum=-40*U[active].sum(axis=0)
  Y=U@pnum+40*7680
  assert not np.any(X*Y)
  z2=[F(int(k*k),32000) for k in X]  # a²*(X/40)²
  y2=[F(int(k*k),20*40*40*7680*7680) for k in Y]
  A=sum((z2[i]*U2[i]/2 for i in range(160)),F(0))
  B=sum((y2[i]*V2[i]/2 for i in range(160)),F(0))
  C=sum((U2[i]*V2[i]/4+z2[i]*y2[i] for i in range(160)),F(0))
  vals.append((A,B,C))
 assert len(set(vals))==1
 A,B,C=vals[0]
 assert A==F(312) and B==F(1027,128) and C==F(1521,10)
 opt=float(C+2*math.sqrt(float(A*B)))
 origin=F(1681,10)
 assert opt>float(origin)
 return dict(status='PASS',classical_zero_stars=80,
   exact_energy_function=f'{A}/sigma² + {B}*sigma² + {C}',
   coefficient_A=str(A),coefficient_B=str(B),constant=str(C),
   optimum_sigma_squared=float(math.sqrt(float(A/B))),
   optimum_gaussian_energy=float(opt),
   exact_optimum='1521/10+sqrt(40053)/2',
   isotropic_centered_origin_gaussian_energy=str(origin),
   conclusion='The 80 exact CLASSICAL star zero planes are quantum-coherent localization costly within the specified isotropic Gaussian family, compared with the symmetric q=p=0 isotropic Gaussian. This is NOT a lower bound: squeezed, non-Gaussian and phase-correlated states may do better.',
   proof='For each e, X=40+V0*qi and Y=40*7680+U0*pnum give all classical J_e=0. U_e.V_e=0 implies independent centered position and momentum quadratures for isotropic Gaussian; Wick factor yields A/sigma²+B sigma²+C. Minimize by AM-GM; exact arithmetic repeated on all 80 anchors.')
if __name__=='__main__':
 z=certificate();(ROOT/'data/w33_20261009_round16_star_gaussian_uncertainty.json').write_text(json.dumps(z,indent=2)+'\n')
 print('GAUSSIAN',z['exact_energy_function'],z['optimum_gaussian_energy'])
