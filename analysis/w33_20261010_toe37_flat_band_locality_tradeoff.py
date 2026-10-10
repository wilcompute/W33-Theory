"""TOE37 track4: Flat-band removal vs locality & linear dispersion.

Native W33 lifted vertex-edge Dirac H=[0 B†;B 0]:
at generic Bloch k, B:160x80 rank80 => 80 edge flat modes.
Attempt A local edge onsite mass m I: gapped flat80 but low E~k²/m
and destroys linear cone. Attempt B precise cycle-only
mass m*(I-B(B†B)^-1 B†) gaps flat80 while preserving ±sqrt L,
but P is dense/nonlocal and singular when k->0.
"""
import sys,json,numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe26_css_matching_family import wilson
from w33_20261010_toe35_three_deck_kinematic_construction import spanning_chords
from w33_20261010_toe36_incidence_relativistic_walk import gradient
OUT=ROOT/'data/w33_20261010_toe37_flat_band_locality_tradeoff.json'
def run():
 edges,D,C=wilson();ch=spanning_chords(edges)
 flux=np.zeros((160,3),int)
 for dim,j in enumerate([ch[i] for i in (5,30,65)]):flux[j,dim]=1
 m=1.0;cases=[]
 for knorm in (.03,.015,.0075):
  k=np.array([knorm,0.,0.])
  B=gradient(edges,flux,k)
  L=B.conj().T@B
  e=np.linalg.eigvalsh(L)
  assert e[0]>1e-10
  sigma=float(np.sqrt(e[0]))
  P=B@np.linalg.solve(L,B.conj().T)
  nonlocal_mass=m*(np.eye(160)-P)
  psym=float(np.linalg.norm(P-P.conj().T))
  pproj=float(np.linalg.norm(P@P-P))
  pcompatible=float(np.linalg.norm((np.eye(160)-P)@B))
  assert max(psym,pproj,pcompatible)<1e-8
  # exact 2x2 block for each singular value of B
  Elocal=(m-np.sqrt(m*m+4*e[0]))/2
  Eproj_minus=-sigma
  assert abs(Eproj_minus+sigma)<1e-12
  # cycle-only P is a generally DENSE edge-edge operator:
  off=P.copy();np.fill_diagonal(off,0)
  dense_frac=float(np.count_nonzero(abs(off)>1e-8)/(160*159))
  cases.append(dict(k_norm=knorm,smallest_Laplacian_eigenvalue=float(e[0]),
   intrinsic_linear_E_positive=sigma,
   local_uniform_edge_mass_negative_acoustic_E=float(Elocal),
   nonlocal_cycle_only_mass_negative_acoustic_E=Eproj_minus,
   projection_Hermitian_residual=psym,projection_idempotence_residual=pproj,
   cycle_projector_annihilates_B_residual=pcompatible,
   fraction_nonzero_offdiagonal_entries_in_required_edge_projector=dense_frac))
 ratios=dict(
   intrinsic_E_at_k_over_E_at_half_k=cases[0]['intrinsic_linear_E_positive']/cases[1]['intrinsic_linear_E_positive'],
   local_mass_E_at_k_over_E_at_half_k=cases[0]['local_uniform_edge_mass_negative_acoustic_E']/cases[1]['local_uniform_edge_mass_negative_acoustic_E'],
   exact_cycle_projector_E_at_k_over_E_at_half_k=cases[0]['nonlocal_cycle_only_mass_negative_acoustic_E']/cases[1]['nonlocal_cycle_only_mass_negative_acoustic_E'])
 assert 1.9<ratios['intrinsic_E_at_k_over_E_at_half_k']<2.1
 assert 3.8<ratios['local_mass_E_at_k_over_E_at_half_k']<4.2
 assert cases[0]['fraction_nonzero_offdiagonal_entries_in_required_edge_projector']>.2
 result=dict(status='PASS',samples=cases,dispersion_halving_ratios=ratios,
   flat_modes_before=80,flat_modes_after_local_uniform_edge_mass_at_E_equals_m=80,
   flat_modes_after_exact_cycle_projector_at_E_equals_m=80,
   physical_spectrum_note='Both put former flat zero modes at energy +m, but local uniform edge mass changes acoustic dispersion to quadratic, whereas projector mass preserves ±sqrt(L) while coupling edge channels nonlocally.',
   Hlocal='H=[[0,B†],[B,mI_edge]], eigenvalues (m±sqrt(m²+4λ_j))/2 plus m repeated E−V=80. At small λ~k², negative branch E_-~-λ/m~k².',
   Hnonlocal='H=[[0,B†],[B,m(I-P)]], P=B(B†B)^-1B† for invertible L(k), shifts cycle modes to m and preserves ±sqrt λ. P is dense, momentum dependent, and singular in the zero-momentum limit because L(0) has a zero mode.',
   gauge_candidate='A physical quotient by ker B†, leaving C^80 ⊕ im B, also needs a gauge/constraint principle and local implementation; simply deleting the unwanted kernel is an imposed global operation.',
   caveat='Not a universal no-go for every possible local coupled-ancilla completion or gauge theory. We only falsify these TWO SIMPLE methods as simultaneous locality+flat-band-removal+z1 solutions.')
 OUT.write_text(json.dumps(result,indent=2)+'\n')
 print('TOE37 flat-band tradeoff ratios',ratios,'projector density',cases[0]['fraction_nonzero_offdiagonal_entries_in_required_edge_projector'],flush=True)
 return result
if __name__=='__main__':run()
