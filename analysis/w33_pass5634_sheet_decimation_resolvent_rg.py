#!/usr/bin/env python3
"""Pass5634 bonkers: real-space/sheet decimation of the intrinsic 32-state magnetic lift.

The intrinsic q=3 vector lift commutes with sheet swap, so in the raw + / - sheet
basis its Hamiltonian has exact block form
    H32 = [[A,B],[B,A]],
while in deck parity basis
    H_even=A+B,  H_odd=A-B.

A is precisely (up to complex conjugation convention) the old section-dependent
16-point magnetic Hamiltonian corrected at Pass5613.  Thus that operator was not
meaningless: it is the BARE ONE-SHEET block of the intrinsic two-sheet theory.

Eliminating the opposite sheet gives the exact Feshbach/Schur effective operator
    H_eff(E)=A + B (E-A)^(-1) B.
This is an energy-dependent finite resolvent flow.  Since [A,B] != 0, the self
energy is not a scalar renormalization of A.  Its poles occur at the 15 distinct
one-sheet energies.  This is a genuine finite decimation structure, but not yet a
Wilsonian spacetime RG or an emergent light cone.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import w33_pass5627_deck_stabilizer_spinor_no_go as core
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5634_SHEET_DECIMATION_RESOLVENT_RG.json'

def build32():
    P=core.p1(); S=[core.segre(u,v) for u in P for v in P]
    vecs=[];base=[]
    for i,v in enumerate(S):
        for a in (1,2):vecs.append(tuple(a*x%3 for x in v));base.append(i)
    w=np.exp(2j*np.pi/3);L=np.zeros((32,32),complex)
    for i in range(32):
        ri,ci=divmod(base[i],4)
        for j in range(i+1,32):
            rj,cj=divmod(base[j],4)
            if ri!=rj and ci!=cj:
                z=w**((2*core.B(vecs[i],vecs[j]))%3);L[i,j]=z;L[j,i]=np.conj(z)
    # reorder interleaved (+,-) to all + then all -
    idx=[2*i for i in range(16)]+[2*i+1 for i in range(16)]
    return L[np.ix_(idx,idx)]

def main():
    H=build32();A=H[:16,:16];B=H[:16,16:]
    assert np.max(abs(H[16:,16:]-A))<1e-10 and np.max(abs(H[16:,:16]-B))<1e-10
    assert np.max(abs(A-A.conj().T))<1e-10 and np.max(abs(B-B.conj().T))<1e-10
    He=A+B;Ho=A-B
    assert np.allclose(np.sort(np.linalg.eigvalsh(H)),np.sort(np.r_[np.linalg.eigvalsh(He),np.linalg.eigvalsh(Ho)]),atol=1e-9)
    old=np.linalg.eigvalsh(A); distinct=[]
    for x in old:
        if not distinct or abs(x-distinct[-1])>1e-7:distinct.append(float(x))
    assert len(distinct)==15
    comm=A@B-B@A; commmax=float(np.max(abs(comm))); assert commmax>1
    # Exact sheet elimination at E=0 is safe because A has no zero eigenvalue.
    E=0.0; Heff=A+B@np.linalg.inv(E*np.eye(16)-A)@B
    ee=np.linalg.eigvalsh(Heff); de=[]
    for x in ee:
        if not de or abs(x-de[-1])>1e-7:de.append(float(x))
    assert len(de)==16
    out={
      'pass':5634,'status':'EXACT_TWO_SHEET_FESHBACH_FLOW__NOT_YET_SPACETIME_RG',
      'block_identity':'H32=[[A,B],[B,A]], H_even=A+B, H_odd=A-B',
      'old_pass5609_reinterpretation':'A is the canonical one-sheet section Hamiltonian up to the omega <-> omega^2 complex-conjugation convention; its spectrum has the same 15 distinct levels. The old operator is a bare sheet block, not the intrinsic full observable.',
      'one_sheet_distinct_energies':distinct,
      'A_B_commutator_max_abs':commmax,
      'effective_operator':'H_eff(E)=A+B(E-A)^(-1)B',
      'self_energy_poles':'the 15 distinct eigenvalues of A',
      'E0_effective_distinct_levels':de,
      'UV_expansion':'Sigma(E)=B(E-A)^(-1)B = B^2/E + B A B/E^2 + ... for large |E|',
      'no_go':'Because A and B do not commute, sheet elimination does not close onto an energy-independent rescaling of A. The natural decimation therefore produces a nonlocal-in-energy self-energy rather than a one-parameter RG fixed point.',
      'physics_boundary':'This is an exact finite Feshbach/resolvent flow. It is not a Wilsonian continuum RG, does not determine spacetime dimension, and does not derive the physical speed of light.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
