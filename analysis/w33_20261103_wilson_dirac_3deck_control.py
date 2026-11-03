#!/usr/bin/env python3
"""A strictly local Wilson-Dirac control coupled to W33 three-voltage Bloch cells.
Exposes naive high-momentum doublers, Wilson-mass lifting, and the necessary
chiral-symmetry breaking. NOT an emergent physical fermion model.
"""
from pathlib import Path
import itertools,sys,json
import numpy as np
from scipy.linalg import eigvalsh
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261102_route_216_cubic_tomography import geometry
def main():
 pts,lines,N,idx,norm,omega=geometry()
 A=N@N.T-4*np.eye(40,dtype=int)
 edges=[(i,j) for i in range(40) for j in range(i+1,40) if A[i,j]]
 selected=[]
 for e in edges:
  if all(set(e).isdisjoint(set(x)) for x in selected):selected.append(e)
  if len(selected)==3:break
 assert selected==[(0,1),(2,3),(4,7)]
 def cell(k):
  B=A.astype(complex)
  for t,(i,j) in zip(k,selected):
   B[i,j]=np.exp(1j*t);B[j,i]=np.exp(-1j*t)
  L=np.eye(40)-B/12
  return eigvalsh(L,check_finite=False)
 I=np.eye(2,dtype=complex);zero=np.zeros((2,2),complex)
 sx=np.array([[0,1],[1,0]],complex)
 sy=np.array([[0,-1j],[1j,0]],complex)
 sz=np.diag([1.,-1.]).astype(complex)
 alpha=[np.block([[zero,s],[s,zero]]) for s in (sx,sy,sz)]
 beta=np.block([[I,zero],[zero,-I]])
 gamma5=np.block([[zero,I],[I,zero]])
 assert all(np.max(abs(a@b+b@a-2*(i==j)*np.eye(4)))<1e-12 for i,a in enumerate(alpha) for j,b in enumerate(alpha))
 assert all(np.max(abs(a@beta+beta@a))<1e-12 for a in alpha)
 def dirac(k,wilson):
  m=float(1.5*sum(1-np.cos(t) for t in k)) if wilson else 0.
  D=m*beta
  for t,a in zip(k,alpha):D=D+np.sin(t)*a
  return D,m
 lambda_=0.1
 # Since the cell Laplacian and Dirac symbol act on tensor factors,
 # full 160-mode spectrum is λ*eig(cell)+eig(Dirac), exactly.
 corners=[]
 for p in itertools.product((0,np.pi),repeat=3):
  l=cell(p)
  dn,m0=dirac(p,False);dw,m=dirac(p,True)
  x=np.ravel(lambda_*l[:,None]+eigvalsh(dn)[None,:])
  y=np.ravel(lambda_*l[:,None]+eigvalsh(dw)[None,:])
  corners.append({'pi_axes':int(sum(t>0 for t in p)),
      'bare_dirac_min_abs':float(min(abs(eigvalsh(dn)))),
      'native_40mode_naive_min_abs':float(min(abs(x))),
      'native_40mode_wilson_min_abs':float(min(abs(y))),
      'wilson_mass':m,
      'chirality_commutator_norm':float(np.linalg.norm(dw@gamma5-gamma5@dw))})
 assert all(c['bare_dirac_min_abs']<1e-12 for c in corners)
 assert corners[0]['native_40mode_wilson_min_abs']<1e-12
 assert all(c['native_40mode_wilson_min_abs']>2.7 for c in corners[1:])
 assert all(c['chirality_commutator_norm']>1 for c in corners[1:])
 branches=[]
 for eps in (0.003,0.01,0.03):
  k=np.array([eps,2*eps,-eps])/np.sqrt(6)
  l=cell(k)
  H,m=dirac(k,True)
  E=np.ravel(lambda_*l[:,None]+eigvalsh(H)[None,:])
  nearest=np.sort(E[np.argsort(abs(E))[:4]])
  branches.append({'k_norm':float(np.linalg.norm(k)), 'four_near_zero_energies':nearest.tolist(),
   'positive_speed_ratio':float(nearest[-1]/np.linalg.norm(k)),
   'negative_speed_ratio':float(-nearest[0]/np.linalg.norm(k))})
 assert all(abs(x['positive_speed_ratio']-1)<.02 for x in branches)
 out={'status':'PASS_W33_SYNTHETIC_3D_WILSON_DIRAC_BENCHMARK',
  'base_graph_modes':40,'Dirac_internal_modes':4,'Bloch_cell_modes':160,'voltage_edges':selected,
  'W33_laplacian_amplitude':lambda_,'Wilson_r':1.5,'mass_at_k0':0,
  'BZ_corner_doubler_controls':corners,'small_k_branches':branches,
  'locality':'Exactly 3 real deck hoppings + on-site 40-mode adjacency + finite nearest-neighbor Wilson spinor terms; 160-mode cell before deck replication',
  'limitation':'Wilson mass is manually supplied and breaks exact chiral conservation; the resulting cone is engineered, not emergent, and no SM chirality, interactions, c or gravity derived. Known Wilson fermion technique, not novel physical principle.',
  'reference':'Gupta & Short PRA 114 012208 (2026); Wilson fermions topolectrical Communications Physics 2023'}
 (ROOT/'data/w33_20261103_wilson_dirac_3deck_control.json').write_text(json.dumps(out,indent=2)+'\n')
 print('WILSON_NATIVE',json.dumps(out)[:4600],flush=True)
 return out
if __name__=='__main__':main()
