#!/usr/bin/env python3
"""Native W33 three-voltage Bloch tower: exact incidence and low-k diffusion
metric vs Lorentzian cone. Avoids 40*m^3 explicit graph and tests 3D cover.
"""
from pathlib import Path
import sys, json, itertools
import numpy as np
from scipy.linalg import eigh
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261102_route_216_cubic_tomography import geometry
def main():
 pts,lines,N,idx,norm,omega=geometry()
 A=N@N.T-4*np.eye(40,dtype=int)
 k=12
 edges=[(a,b) for a in range(40) for b in range(a+1,40) if A[a,b]]
 # Choose a triangle-free set of edges on 6 distinct vertices.
 chosen=[]
 for a,b in edges:
  if a not in [e for pair in chosen for e in pair] and b not in [e for pair in chosen for e in pair]:
   chosen.append((a,b))
  if len(chosen)==3:break
 assert len(chosen)==3
 def lowest(t):
  M=A.astype(complex)
  for j,(a,b) in enumerate(chosen):
   M[a,b]=np.exp(1j*t[j]);M[b,a]=np.exp(-1j*t[j])
  H=np.eye(40)-M/12
  eig=eigh(H,subset_by_index=[0,2],eigvals_only=True)
  return eig
 zero=lowest(np.zeros(3))
 assert abs(zero[0])<1e-12 and zero[1]>.8
 h=0.003
 D=np.zeros((3,3))
 for i in range(3):
  t=np.zeros(3);t[i]=h
  D[i,i]=(lowest(t)[0]+lowest(-t)[0]-2*zero[0])/(2*h*h)
 for i in range(3):
  for j in range(i+1,3):
   pp=np.zeros(3);pp[i]=h;pp[j]=h
   pm=np.zeros(3);pm[i]=h;pm[j]=-h
   mp=-pm;mm=-pp
   D[i,j]=D[j,i]=(lowest(pp)[0]+lowest(mm)[0]-lowest(pm)[0]-lowest(mp)[0])/(8*h*h)
 vals=np.linalg.eigvalsh(D)
 assert vals[0]>0,vals
 # Bloch for Z_m^3 covers: low bands for wavevectors near zero.
 bands={}
 for m in (5,9,17):
  z=2*np.pi/m
  b1=[lowest(z*np.eye(3)[j])[0] for j in range(3)]
  mixed=[lowest(z*(np.eye(3)[i]+np.eye(3)[j]))[0] for i,j in ((0,1),(0,2),(1,2))]
  bands[str(m)]={'axis_first_band':list(map(float,b1)),
   'axis_mean_gap':float(np.mean(b1)),
   'mixed_first_band':list(map(float,mixed)),
   'axis_rescaled_m2':list(map(float,np.array(b1)*m*m))}
 # Controlled second-derivative scale check.
 rng=np.random.default_rng(20261103)
 errors=[]
 for _ in range(12):
  t=rng.normal(size=3);t=t/np.linalg.norm(t)*0.01
  est=float(t@D@t);exact=float(lowest(t)[0])
  errors.append(abs(est-exact)/exact)
 assert max(errors)<0.01,max(errors)
 out={'status':'PASS_NATIVE_ZM3_BLOCH_DIFFUSION_TENSOR','edge_voltages':chosen,
      'base_vertex_count':40,'cover_layers_dims':3,
      'low_momentum_quadratic_tensor':D.tolist(),'diffusion_eigenvalues':vals.tolist(),
      'metric_condition_number':float(vals[-1]/vals[0]),
      'small_k_max_relative_quadratic_error':float(max(errors)),
      'cover_bloch_examples':bands,
      'low_k_modes_directions':3,'acoustic_quadratic':'lambda0(k)=k.T D k + O(|k|^4) for conjugation-symmetric spectrum',
      'scope':'three independent voltage directions on same 40-vertex W33 cell; quadratic nonrelativistic/Laplacian dispersion, no Minkowski signature or physical speed and time'}
 (ROOT/'data/w33_20261103_native_three_voltage_bloch.json').write_text(json.dumps(out,indent=2)+'\n')
 print('BLOCH',json.dumps(out)[:4000],flush=True)
 return out
if __name__=='__main__':main()
