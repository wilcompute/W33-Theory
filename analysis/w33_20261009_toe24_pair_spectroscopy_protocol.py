"""Experimental falsification certificate for W33 strong-attraction
two-boson pair spectroscopy: exact FIVE bands and local spectral weights,
plus reproducible noisy on-site synthetic-array tolerance.
"""
import json,sys,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe_integral_clique_levi_bridge import chain
OUT=ROOT/'data/w33_20261009_toe24_pair_spectroscopy_protocol.json'
def run():
 pts,ix,lines,li,edges,tris,flags,fi,E,T,D,M,R=chain()
 A=np.zeros((80,80))
 for p,l in flags:A[p,40+l]=A[40+l,p]=1
 eigen,U=np.linalg.eigh(A)
 lam=[4,np.sqrt(6),0,-np.sqrt(6),-4]
 multiplicity=[1,24,30,24,1]
 for l,m in zip(lam,multiplicity):
  mask=(abs(eigen-l)<1e-7)
  assert sum(mask)==m
  weights=(U[:,mask]**2).sum(axis=1)
  assert np.max(abs(weights-m/80))<1e-11,(l,np.max(abs(weights-m/80)))
 ref=4-np.sqrt(6)
 bands=[dict(adjacency_eigenvalue=float(l),multiplicity=int(m),
   weight_from_one_localized_doublon=m/80,
   gap_over_2t_squared_over_U=float(4-l),
   energy_over_first_nonzero_gap=float((4-l)/ref))
  for l,m in zip(lam,multiplicity)]
 assert abs(sum(b['weight_from_one_localized_doublon'] for b in bands)-1)<1e-12
 # Exact local weights follow bipartite singular-pairing and separate
 # point/line transitivity; no point/line swapping automorphism is assumed.
 rng=np.random.default_rng(20261009)
 noise={}
 for sigma in (0,.01,.03,.05,.1):
  ratios=[];band_spreads=[]
  for trial in range(50):
   delta=rng.uniform(-sigma,sigma,size=80)
   ev=np.linalg.eigvalsh(A+np.diag(delta))
   top=ev[-1];high=ev[-25:-1];middle=ev[-55:-25]
   R=(top-middle.mean())/(top-high.mean())
   ratios.append(float(R))
   band_spreads.append(float(high[-1]-high[0]))
  R0=4/ref
  analytic=2*sigma*(1+R0)/(ref-2*sigma) if 2*sigma<ref else None
  assert max(abs(v-R0) for v in ratios)<analytic+1e-10 if sigma>0 else all(abs(v-R0)<1e-9 for v in ratios)
  noise[str(sigma)]=dict(trials=50,mean_second_over_first_gap=float(np.mean(ratios)),
   max_abs_ratio_shift=float(np.max(abs(np.array(ratios)-R0))),
   mean_first_band_broadening=float(np.mean(band_spreads)),
   rigorous_Weyl_ratio_error_upper_bound=float(analytic) if analytic is not None else None)
 old=json.loads((ROOT/'data/w33_20261009_toe23_universal_pair_ratios.json').read_text())
 err={k:float(v['relative_error']) for k,v in old['finite_U_numeric'].items()}
 out=dict(status='PASS',n_graph_sites=80,n_links=160,
  physical_model='Attractive U>>t Bose-Hubbard model of two bosons on an engineered W33 80-site 160-link synthetic lattice; NOT actual elementary particles.',
  effective_pair_H='-U I -(t^2/U)(8I+2A) +O(t^4/U^3)',
  band_spectroscopy=bands,
  nontrivial_gap_ratio_second_over_first=float(R0),
  measurements='Prepare doublon |i,i> by local on-site two-boson injection, spectroscopically probe return amplitude / two-photon coincidence vs delay, Fourier resolve four nonzero internal band splittings. At a single incidence site, predicted FIVE band weights are {1,24,30,24,1}/80. Compare measured frequencies after removing overall t²/U; calibrate t independently using single-boson hopping and U via onsite interaction spectroscopy.',
  synthetic_on_site_noise_A_units=noise,
  finite_U_relative_error_in_first_gap=err,
  exclusion_criteria='Reject native W33 simulator if five predicted band centers, multiplicities, and parameter-free relative ratios disagree beyond measured loss/inhomogeneity/model corrections in the controlled U/t extrapolation. This is a falsification of a specified quantum-simulator Hamiltonian, not a falsification of fundamental physical laws or a TOE.',
  confounders=['site-dependent hopping disorder','pair leakage into separated-particle continuum','loss and dephasing broadening','finite-U corrections','nonuniform address/readout calibration','graph implementation error'],
  caution='All 80 native projector diagonals were independently verified equal rank/80 by numerical diagonalization. The proof uses bipartite +/- spectral pairing and PSp transitivity separately on points/lines; the 0 eigenspace has equal 15D point and line kernels. No vertex-transitive point/line swapping automorphism is assumed. Single-source individual mode amplitudes depend on imperfections. Band projectors, rather than isolated eigenvector overlaps, are invariant data.')
 OUT.write_text(json.dumps(out,indent=2)+'\n')
 print('SPECTROSCOPY',[(b['multiplicity'],round(b['energy_over_first_nonzero_gap'],6)) for b in bands],
    'noise .05',noise['0.05'],flush=True)
 return out
if __name__=='__main__':run()
