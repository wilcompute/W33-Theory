"""Finite-time continuous-time single-photon W33 return *probability*
measurement at physical selected-site basis. Complement to exact 8th
Taylor-coefficient modular witness. Fully numerical and externally phased.
"""
from pathlib import Path
import sys,json
import numpy as np
from scipy.linalg import expm
from itertools import combinations
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261008_5state_ritz import geometry
def complex_adjacency(edges,rep,ph):
 A=np.zeros((80,80),dtype=complex)
 phases=dict(zip(rep,ph))
 for i,(p,l) in enumerate(edges):
  z=np.exp(1j*phases[i]) if i in phases else 1.
  A[p,l]=z;A[l,p]=np.conj(z)
 return A
def experiment():
 edges,*_=geometry()
 reps=json.loads((ROOT/'data/w33_20261009_PSp_orbits_isotropic_triplets.json').read_text())['orbits']
 rational=[float(np.arctan2(b,a)) for a,b,d in [(15,8,17),(4,-3,5),(5,12,13)]]
 output={}
 for label,ph in [('rational_unimodular',rational),('original_round16_angles',[.49,-.74,1.22])]:
  A=[complex_adjacency(edges,r['representative'],ph) for r in reps]
  for a in A:assert np.linalg.norm(a-a.conj().T)<1e-14
  times={}
  for t in (.25,.5,1.,2.):
   hist=[];errors=[]
   for a in A:
    u=expm(-1j*t*a)
    errors.append(float(np.linalg.norm(u.conj().T@u-np.eye(80))))
    hist.append(np.sort(np.abs(np.diag(u))**2))
   margins=[float(np.max(np.abs(hist[i]-hist[j]))) for i,j in combinations(range(5),2)]
   times[str(t)]=dict(max_probability_gap_among_pairwise_histograms=float(max(margins)),
    minimum_pairwise_histogram_linf_distance=float(min(margins)),
    maximum_unitarity_residual=max(errors))
  output[label]=times
 print('FINITE-TIME',output,flush=True)
 return dict(status='PASS',phase_conventions=output,
  protocol='Single-photon preparation at each one of 80 physical sites; evolve for t under engineered 80-mode Peierls adjacency; read survival probability and sort across sites, allowing relabeling. Compare the full 80-dimensional histogram.',
  caveat='All differences at finite time are floating-point numerical calculations, not exact certified lower bounds. In particular, minute short-time differences may be experimentally impractical. No gate fidelity, source/detector statistics, or photon-chip implementation has been measured.')
def main():
 d=experiment()
 (ROOT/'data/w33_20261009_round19_finite_time_onephoton_readout.json').write_text(json.dumps(d,indent=2)+'\n')
if __name__=='__main__':main()
