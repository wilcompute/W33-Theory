"""Round35: construct a THREE-generator abelian W33 Levi cover.

Pick 3 independent fundamental graph cycles after tree gauge, put
Z^3 unit flux on 3 chord edges. The connected infinite regular cover
has deck group Z^3, effective positive-definite quadratic Bloch
diffusion and asymptotic ds=3. Finite Z_p^3 quotients tested by
p^3 Hermitian 80x80 Bloch diagonalizations.
Important: dimensionality is INSERTED through a rank-3 deck choice,
not spontaneously selected by W33 or a physical Lorentzian metric.
"""
from pathlib import Path
import sys,json,math,itertools
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe26_css_matching_family import wilson
from w33_20261010_toe33_bloch_spectral_spacetime import heat_record,longest_plateau
OUT=ROOT/'data/w33_20261010_toe35_three_deck_kinematic_construction.json'
def spanning_chords(edges,n=80):
 p=list(range(n))
 def root(k):
  while p[k]!=k:p[k]=p[p[k]];k=p[k]
  return k
 tree=[]
 for j,(a,b) in enumerate(edges):
  ra,rb=root(a),root(b)
  if ra!=rb:p[ra]=rb;tree.append(j)
 assert len(tree)==79
 return [j for j in range(len(edges)) if j not in set(tree)]
def matrix(edges,flux,vec):
 A=np.eye(80,dtype=np.complex128)*4
 for (a,b),v in zip(edges,flux):
  angle=np.dot(v,vec)
  z=np.exp(1j*angle)
  A[a,b]-=z;A[b,a]-=z.conjugate()
 return A
def lowest(edges,flux,vec):
 return float(np.linalg.eigvalsh(matrix(edges,flux,np.asarray(vec)))[0])
def run():
 edges,D,C=wilson()
 chord=spanning_chords(edges)
 # 3 far-spaced independent homological graph cycles
 selected=[chord[5],chord[30],chord[65]]
 flux=np.zeros((160,3),dtype=np.int16)
 for i,j in enumerate(selected):flux[j,i]=1
 # for every fundamental cycle, its flux is the specified chord vector
 assert np.linalg.matrix_rank(flux[selected])==3
 eps=.01;D3=np.zeros((3,3))
 for i in range(3):
  v=np.zeros(3);v[i]=eps
  D3[i,i]=lowest(edges,flux,v)/eps**2
 for i in range(3):
  for j in range(i+1,3):
   v=np.zeros(3);v[i]=eps;v[j]=eps
   D3[i,j]=D3[j,i]=(lowest(edges,flux,v)/eps**2-D3[i,i]-D3[j,j])/2
 eigen=np.linalg.eigvalsh(D3)
 assert min(eigen)>0,(D3,eigen)
 print('THREE DECK diffusion D eigen',eigen,flush=True)
 runs=[]
 for p in (3,5,7,9):
  vals=[]
  for k in itertools.product(range(p),repeat=3):
   theta=np.asarray(k)*(2*np.pi/p)
   vals.extend(np.linalg.eigvalsh(matrix(edges,flux,theta)))
  vals=np.sort(np.asarray(vals))
  assert len(vals)==80*p**3 and abs(vals[0])<1e-8
  assert sum(abs(vals)<1e-7)==1
  grid=np.geomspace(.05,1e6,270)
  samples=[heat_record(vals,float(t)) for t in grid]
  one=longest_plateau(samples,.75,1.25)
  three=longest_plateau(samples,2.75,3.25)
  rec=dict(degree_per_axis=p,vertices=len(vals),spectral_gap=float(vals[1]),
    near3_diffusion_plateau=three,near1_diffusion_plateau=one,
    dimension_samples=[heat_record(vals,t) for t in (3,10,30,100,300,1000,3000,10000)])
  runs.append(rec)
  print('W33 3DECK',p,'gap',round(vals[1],6),'plateau3',round(three['span_ratio'],2),flush=True)
 result=dict(status='PASS',
  three_selected_fundamental_chord_edge_indices=selected,
  edge_flux_map='All 160 edges carry 0∈Z³ except 3 selected spanning-tree chords carrying +e1,+e2,+e3. Fundamental cycle winding vectors span Z³ integrally; all finite Z_p³ quotients connected.',
  positive_diffusion_tensor_D3=D3.tolist(),diffusion_tensor_eigenvalues=eigen.tolist(),
  asymptotic_theorem='An infinite connected finite-range Z³-periodic graph whose fundamental deck winding spans Z³ integrally has a simple zero bottom Bloch band λ0(k)=kᵀDk+O(|k|4), with D positive definite. The integrated low-energy density scales E^(3/2) and per-cell heat trace scales t^(-3/2), hence diffusion spectral dimension asymptotically 3. Finite Z_p³ quotients return to d_s=0 at t≫p²/D.',
  tested_finite_quotients=runs,
  physical_boundary='This constructs 3D kinematic DIFFUSION, not physical emergent 3+1D spacetime. Three independent macroscopic deck coordinates and port assignments are imposed from outside; no dynamical selector, local Lorentz symmetry, Einstein field equations or massless E=c|k| photon dispersion. The same k² Bloch band yields z=2 nonrelativistic hopping.',
  group_contrast='Round35 connected one-generator Z tower has d_s→1, illustrating that the asymptotic dimension follows chosen abelian deck RANK, not uniquely native finite W33 geometry.')
 OUT.write_text(json.dumps(result,indent=2)+'\n')
 return result
if __name__=='__main__':run()
