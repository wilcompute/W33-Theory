#!/usr/bin/env python3
"""Pass5632 bonkers: ask whether the signed deck16 supports a spinful BdG/Pin symmetry.

Pass5630 constructs the 96-element real signed carrier representation R and the
purely imaginary Hermitian H=iS with K H K^{-1}=-H, K^2=+1.  If there were an
additional stabilizer-equivariant time-reversal antiunitary T=U K satisfying
T H T^{-1}=H, then U would have to satisfy simultaneously
  U R_g = R_g U  for every carrier symmetry g,
  U H + H U = 0.
The joint linear system has nullity zero.  Thus no nonzero equivariant U exists;
in particular no T with T^2=-1 and no Kramers doubling follows from this carrier.

In the standard tenfold-way vocabulary this is algebraically class-D-like if H is
second-quantized as a Majorana/BdG Hamiltonian: particle-hole/real-Majorana
structure without an equivariant time-reversal symmetry.  That vocabulary is a
comparison, not a claim that the finite carrier is already a physical fermion.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import w33_pass5630_deck_bdg_commutant_mass_ratio_unprotected as p5630
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5632_PIN_BDG_SPIN_STATISTICS_NO_GO.json'

def main():
    pairs,Rs,H=p5630.build()
    # A small generating set is enough for the commutant equations.
    gens=[];cur={(tuple(range(16)),tuple([1]*16))}
    for c in pairs:
        if c not in cur:
            test=p5630.pair_closure(gens+[c])
            if len(test)>len(cur):gens.append(c);cur=test
            if len(cur)==96:break
    GR=[p5630.signed_matrix(x) for x in gens]; assert len(cur)==96
    C=np.vstack([np.kron(R.T,np.eye(16))-np.kron(np.eye(16),R) for R in GR]).astype(complex)
    Anti=np.kron(H.T,np.eye(16))+np.kron(np.eye(16),H)
    A=np.vstack([C,Anti])
    s=np.linalg.svd(A,compute_uv=False); nullity=int(np.sum(s<1e-9)); assert nullity==0
    assert np.max(abs(H.conj()+H))<1e-9 # KHK^-1=-H
    out={
      'pass':5632,'status':'NO_STABILIZER_EQUIVARIANT_TIME_REVERSAL__CLASS_D_LIKE_FINITE_BDG',
      'particle_hole_antiunitary':'K=complex conjugation','K_squared':1,'K_action':'K H K^{-1}=-H',
      'time_reversal_ansatz':'T=U K with U commuting with the 96-element carrier stabilizer',
      'required_linear_system':['U R_g = R_g U','U H + H U = 0'],
      'joint_nullity':nullity,
      'theorem':'There is no nonzero stabilizer-equivariant U that converts K into an antiunitary commuting with H. Therefore the carrier supplies no equivariant T, no T^2=-1 Kramers structure, and no DIII shortcut.',
      'tenfold_way_reading':'If second-quantized as a free Majorana/BdG Hamiltonian, the algebraic symmetry content is class-D-like: a real skew Majorana generator / PHS-type K symmetry without equivariant TRS.',
      'spin_statistics_firewall':'A central sign and a BdG-like symmetry class are not the relativistic spin-statistics theorem. Lorentz covariance, locality, a Fock representation and exchange statistics remain unconstructed.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
