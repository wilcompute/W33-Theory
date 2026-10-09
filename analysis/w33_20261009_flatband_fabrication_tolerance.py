"""W33 two-critical-point photonic coupler: Weyl-toleranced isolated
cluster certificates and generic independent onsite detuning.

For A(t)=(1-t)A6+t A30, Eflat=-2 and H1 has multiplicity81
for all t. At t1=1/2: 96-way cluster, at
t2=(2+sqrt10)/6: 105-way cluster.
For Hermitian perturbation D with ||D||_op<=epsilon,
every ordered eigenvalue shifts <=epsilon (Weyl).
If the unperturbed nonzero gap to flat band delta>2epsilon,
the corresponding cluster is isolated (but may split internally).
At a critical t, crossing multiplicity splits under GENERIC onsite
detuning, even though protected correlation-specific weights retain H1.
"""
import sys,json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_correlated_disorder_dual_couplers import construct
def certificate():
 B,A6,A30,M,D,P=construct()
 I=np.eye(160)
 t1=.5;t2=(2+math.sqrt(10))/6
 samples=[]
 rng=np.random.default_rng(551)
 eps=.01
 for t in (0,.35,.45,.49,t1,.51,.55,.8,.85,t2,.87,.95,1):
  H=(1-t)*A6+t*A30+2*I
  ev=np.linalg.eigvalsh(H)
  zeros=int(sum(abs(ev)<1e-8))
  assert zeros==(96 if abs(t-t1)<1e-12 else 105 if abs(t-t2)<1e-12 else 81)
  others=[abs(v) for v in ev if abs(v)>1e-8]
  delta=min(others)
  kneg=int(sum(ev< -1e-8))
  hpert=H+np.diag(rng.uniform(-eps,eps,size=160))
  ep=np.linalg.eigvalsh(hpert)
  assert max(abs(ev-ep))<=eps+1e-10
  separated=bool(delta>2*eps)
  # Exactly zeros' spectral descendants must remain in +-eps.
  zero_idx=np.flatnonzero(abs(ev)<1e-8)
  assert max(abs(ep[zero_idx]))<=eps+1e-10
  if separated:
   assert int(sum(abs(ep)<=eps+1e-9))==zeros
  samples.append(dict(t=t,unperturbed_minus2_multiplicity=zeros,
      n_modes_below_minus2=kneg,
      unperturbed_min_distance_other_eigenvalues=delta,
      perturbation_norm_max=eps,
      Weyl_max_indexed_eigenvalue_shift=float(max(abs(ep-ev))),
      guaranteed_isolated_cluster_by_delta_gt_2epsilon=separated,
      perturbed_cluster_width=float(np.ptp(ep[zero_idx]))))
 # For 0<=t<1/2, rigorous gap from Gram positivity.
 r=(4-math.sqrt(6))*(1-2*.45)
 measured=next(x for x in samples if abs(x['t']-.45)<1e-10)
 assert measured['unperturbed_min_distance_other_eigenvalues']>=r-1e-9
 # Correlated vertex weights preserve exact 81-way cycle eigenspace.
 w=rng.uniform(.5,1.5,size=80)
 Hcorr=(B.T*w)@B
 ec=np.linalg.eigvalsh(Hcorr)
 assert max(abs(ec[:81]))<1e-9
 assert ec[81]>=(4-math.sqrt(6))*min(w)-1e-9
 return dict(status='PASS',eps_independent_onsite=.01,
  critical_points={'first_t':'1/2','first_kernel_dimension':96,
                   'second_t':'(2+sqrt10)/6','second_kernel_dimension':105},
  exact_offcritical_band_dimension=81,
  analytic_lower_gap_first_phase='For 0<=t<1/2, distance of 81 flat eigenvalues to all other energies >= (1-2t)*(4-sqrt6); at t=0.45 this is 0.15505102572...',
  Weyl_stability_theorem='For any Hermitian perturbation V of norm<=eps, every eigenvalue moves at most eps. If the unperturbed gap delta to a flat eigenvalue cluster exceeds 2eps, the perturbed cluster is isolated with its original total spectral count, although generic disorder splits exact degeneracy.',
  negative_consequence='At exact t1/t2, no gap between 81 core modes and extra 15/24 crossing states exists. Generic independent onsite detuning removes exact 96/105 degeneracy; it cannot be called topologically protected against arbitrary perturbations.',
  correlated_vertex_weights_exact_81_band=True,
  correlated_min_positive_gap_numerical=float(ec[81]),
  correlated_rigorous_gap_lower=float(min(w)*(4-math.sqrt(6))),
  samples=samples,
  hardware_boundary='Dimensionless Hermitian 160-port hopping model only; no physical coupler calibration, photon statistics, dispersion relation or gravitational dynamics inferred.')
if __name__=='__main__':
 d=certificate();(ROOT/'data/w33_20261009_flatband_fabrication_tolerance.json').write_text(json.dumps(d,indent=2)+'\n')
 print('TOLERANCE',[(round(r['t'],6),r['unperturbed_minus2_multiplicity'],r['n_modes_below_minus2'],round(r['unperturbed_min_distance_other_eigenvalues'],6),r['guaranteed_isolated_cluster_by_delta_gt_2epsilon']) for r in d['samples']])
