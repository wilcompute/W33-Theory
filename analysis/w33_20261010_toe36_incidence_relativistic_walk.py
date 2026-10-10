"""TOE36/4: local W33 incidence Dirac square-root of Laplacian.

On the 3-deck W33 Levi graph define the LOCAL edge-vertex
gradient B(k) [160x80]; Q(k)=[[0,B†],[B,0]] [240x240].
Q² diag(B†B, BB†), B†B = W33 voltage Laplacian.
Low mode of Q has E=±sqrt(kᵀDk)+... (z=1). BUT
80 flat zero modes at generic momentum due to 160-80 edges,
and 81 at k0, no true spinorial 3+1D Dirac gamma structure.
"""
from pathlib import Path
import sys,json
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe26_css_matching_family import wilson
from w33_20261010_toe35_three_deck_kinematic_construction import spanning_chords,matrix
OUT=ROOT/'data/w33_20261010_toe36_incidence_relativistic_walk.json'
def gradient(edges,flux,k):
 B=np.zeros((160,80),dtype=complex)
 for j,((a,b),f) in enumerate(zip(edges,flux)):
  phase=np.exp(1j*np.dot(k,f))
  B[j,a]=-1
  B[j,b]=phase
 return B
def run():
 ed,D,C=wilson();ch=spanning_chords(ed)
 selected=[ch[i] for i in (5,30,65)]
 flux=np.zeros((160,3),int)
 for a,j in enumerate(selected):flux[j,a]=1
 eps=.008
 def lam(k):return float(np.linalg.eigvalsh(matrix(ed,flux,k))[0])
 d3=np.zeros((3,3))
 for i in range(3):
  k=np.zeros(3);k[i]=eps;d3[i,i]=lam(k)/eps**2
 for i in range(3):
  for j in range(i+1,3):
   k=np.zeros(3);k[i]=eps;k[j]=eps
   d3[i,j]=d3[j,i]=(lam(k)/eps**2-d3[i,i]-d3[j,j])/2
 eig=np.linalg.eigvalsh(d3);assert eig.min()>0
 outputs=[]
 for unit in ([1,0,0],[0,1,0],[0,0,1],[1,1,1],[1,2,-1]):
  direction=np.array(unit,dtype=float);direction/=np.linalg.norm(direction)
  k=direction*.02
  B=gradient(ed,flux,k)
  LL=B.conj().T@B
  resid=float(np.linalg.norm(LL-matrix(ed,flux,k)))
  assert resid<1e-12
  sval=np.linalg.svd(B,compute_uv=False)
  lowest=float(sval[-1])
  pred=float(np.sqrt(k@d3@k))
  ratio=lowest/pred
  assert abs(ratio-1)<.02,(unit,ratio)
  outputs.append(dict(k_direction=unit,k_norm=.02,
    E_positive_nearest_zero=lowest,linear_E_predicted=pred,
    measured_over_acoustic_prediction=ratio,
    adjoint_matrix_identity_residual=resid,
    zero_flat_edge_band_dimension=160-80))
 # Check exceptional k0 rank 79 and cycle null 81
 B0=gradient(ed,flux,np.zeros(3))
 sv0=np.linalg.svd(B0,compute_uv=False)
 assert sv0[-1]<1e-12 and sv0[-2]>.1
 # at nonzero k, B full rank => H has 80 zero modes
 # at k=0 B rank79 => H has82 total zero modes
 E=np.linalg.eigvalsh(np.block([[np.zeros((80,80)),B.conj().T],[B,np.zeros((160,160))]]))
 assert np.count_nonzero(abs(E)<1e-9)==80
 result=dict(status='PASS',carrier='same 3-generator W33 Levi cover from Round35; 80 base vertices 160 base edges',
  local_B='For each oriented base incidence edge e=(a→b) with deck flux f_e, B_ea=-1 and B_eb=e^{i k·f_e}, zero elsewhere.',
  local_chiral_H='H=[[0,B†],[B,0]] Hermitian 240×240 per Bloch cell, 4-neighbor vertex coupling to incident edges, 2-neighbor edge coupling to endpoints.',
  exact_H_squared='H²=diag(B†B,BB†), B†B=W33 voltage Laplacian L(k).',
  diffusion_tensor=d3.tolist(),squared_acoustic_velocity_eigenvalues=eig.tolist(),
  acoustic_velocity_eigenvalues=np.sqrt(eig).tolist(),
  directional_verified_dispersion=outputs,
  generic_flat_zero_modes=80,zero_modes_at_k0=82,
  spectral_dimension_isotropic_warning='Three imposed deck axes produce 3D low-energy dispersion E±∝|k| but with nonidentical velocities; anisotropy not dynamically eliminated.',
  conceptual_achievement='A LOCAL first-order-in-time, nearest-incidence linear square-root gives z=1 (wave-like) low-energy branch on W33-derived cover. It is a mathematical propagator candidate, not actual light or a Lorentzian quantum field.',
  physical_obstructions='H has 80 exactly flat zero bands for generic k and 82 at k=0, owing to edge-cycle kernel. No physical fermionic antisymmetry, four Dirac gamma matrices, helicity/Weyl chirality, gauge constraint to remove zero bands, photons, Einstein equations or universal c derived. Proving a smooth 3D long-wavelength cone requires dealing with degeneracies and anisotropy.')
 OUT.write_text(json.dumps(result,indent=2)+'\n')
 print('TOE36 DIRAC sqrtL sound velocities',np.sqrt(eig),'zero flat',result['generic_flat_zero_modes'],flush=True)
 return result
if __name__=='__main__':run()
