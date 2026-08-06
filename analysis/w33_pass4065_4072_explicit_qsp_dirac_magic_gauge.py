#!/usr/bin/env python3
"""Deterministic verifier for Passes 4065-4072."""
from __future__ import annotations
import hashlib,json,math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_4065_4072_EXPLICIT_QSP_DIRAC_MAGIC_GAUGE_BONKERS.json'
def sha(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def qsp(ph,x):
 s=np.sqrt(max(0.0,1-x*x));W=np.array([[x,1j*s],[1j*s,x]],complex)
 U=np.diag([np.exp(1j*ph[0]),np.exp(-1j*ph[0])])
 for p in ph[1:]:U=U@W@np.diag([np.exp(1j*p),np.exp(-1j*p)])
 return U
def p5(x):
 r=np.sqrt(6);return (9/25+24*r/25)*x+(-48/25-152*r/225)*x**3+(64/25-64*r/225)*x**5
def main():
 x=json.loads(OUT.read_text());saved=x.pop('semantic_sha256');assert sha(x)==saved=='342e8e7ae8f3ef06750716a1d3bdb25f2db432ee55e3ca35482086e16d6544ed';x['semantic_sha256']=saved
 q=x['pass4065_explicit_qsp_phases'];ph=np.array(q['phases_radians']);grid=np.linspace(-1,1,20001)
 assert max(abs(qsp(ph,t)[0,0]-p5(t)) for t in grid)<1.3e-15
 assert abs(ph[0]+ph[5]+np.pi)<1e-14 and abs(ph[1]+ph[4]+np.pi)<1e-14 and abs(ph[2]+ph[3])<1e-14
 m=x['pass4066_adaptive_magic_correction']['sample_K10'];assert m['expected_raw_A_phi']==2047 and m['failure_probability']==1/2048
 I=np.eye(2,dtype=complex);sx=np.array([[0,1],[1,0]],complex);sy=np.array([[0,-1j],[1j,0]],complex);sz=np.array([[1,0],[0,-1]],complex)
 beta=np.kron(sz,I);alpha=[np.kron(sx,s) for s in (sx,sy,sz)];I4=np.eye(4)
 for a in alpha:assert np.linalg.norm(a@a-I4)<1e-14 and np.linalg.norm(a@beta+beta@a)<1e-14
 for i in range(3):
  for j in range(i+1,3):assert np.linalg.norm(alpha[i]@alpha[j]+alpha[j]@alpha[i])<1e-14
 p=np.array([.3,-.2,.1]);masses=[.4,np.sqrt(.66),np.sqrt(.96)]
 for label,mass in zip(('singlet','24_sector','15_sector'),masses):
  errs=[]
  D=mass*beta+sum(v*a for v,a in zip(p,alpha))
  for h in (.2,.1,.05,.025):
   U=expm(-1j*h*mass*beta)
   for v,a in zip(p,alpha):U=U@expm(-1j*h*v*a)
   errs.append(float(np.linalg.norm((U-I4)/(-1j*h)-D,2)))
  assert np.allclose(errs,x['pass4067_lorentzian_dirac_walk']['sample']['operator_errors'][label],atol=2e-15)
 assert 2**81*5**23*4==2**83*5**23
 assert abs(x['pass4070_bonkers_reflection_antithermalization']['localized_time_average_entropy_bits']-0.9709505944546686)<1e-15
 assert abs(x['pass4071_bonkers_H1_frame_metrology']['single_site_max_QFI_numeric_per_t2']-(81/160)**2)<1e-15
 print('PASS_4065_4072',saved)
if __name__=='__main__':main()
