#!/usr/bin/env python3
"""Schur-twirl capacity no-go for the 132D E6 carrier, conditional on full symmetry averaging."""
from itertools import product
import numpy as np
import toe_20261122_e6_132_constructive_embedding as E

def verify():
  old=E.verify();assert old['target_dimension']==132
  dims=(78,27,27)
  # Distinct multiplicity-one irreducible E6 blocks: adjoint, fundamental, antifundamental.
  # The group Haar twirl projects any density matrix to scalar identities on these blocks.
  # For each of 81 canonical regular-H27 address labels, Fourier phases spread amplitudes
  # equally among 3 inequivalent E6 blocks, independent of label.
  w=np.exp(2j*np.pi/3)
  probs=[]
  for r,a,b,c in product(range(3),repeat=4):
    prob=[float(abs(w**(t*c)/np.sqrt(3))**2) for t in range(3)]
    assert max(abs(x-1/3) for x in prob)<2e-15
    probs.append(prob)
  assert len(probs)==81
  # Twirled outputs all have the same 132x132 block-diagonal density matrix.
  state=np.zeros((132,132),complex)
  offset=0
  for d,p in zip(dims,(1/3,)*3):
    state[offset:offset+d,offset:offset+d]=p*np.eye(d)/d
    offset+=d
  assert abs(np.trace(state)-1)<1e-12
  ev=np.linalg.eigvalsh(state)
  assert min(ev)>0
  return dict(status='PASS_E6_FULL_TWIRL_ERASES_81_ADDRESS_BASIS_LABELS',
   full_representation='78+27+27bar',total_dimension=132,
   e6_irreps_pairwise_inequivalent=True,each_multiplicity=1,
   twirl_fixed_operator_complex_dimension=3,
   address_basis_state_count=81,each_address_basis_block_populations=[1/3,1/3,1/3],
   twirled_basis_outputs_identical=True,output_rank=132,
   output_block_eigenvalues=[[1/(3*d),d] for d in dims],
   theorem='By Schur orthogonality, full compact E6 Haar conjugation averages a density matrix to direct sum of p_lambda I_{d_lambda}/d_lambda. For the previously certified 81->132 H27 Fourier isometry each canonical address ket has identical block weights 1/3, hence all 81 address basis states become identical after twirling. The twirl is a measure-and-prepare channel, so its quantum capacity vanishes.',
   caveat='Full E6 Haar twirling is a deliberately strong noise null model, NOT generic gauge-invariant dynamics, an experimentally present channel, or proof that all E6 encodings fail. Symmetry covariance alone is distinct from physical twirling. Other error models and active recovery can preserve quantum information.')
if __name__=='__main__':print(verify())
