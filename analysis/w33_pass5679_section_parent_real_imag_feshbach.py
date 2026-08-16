#!/usr/bin/env python3
"""Pass5679: the old section Hamiltonian is the complex parent of deck even/odd physics.

Pass5634 found the intrinsic 32-state lift in sheet basis

    H32 = [[A,B],[B,A]]

with A equal (up to the omega convention) to the old Pass5609 one-section operator.
The stronger identity is

    B = conj(A).

Therefore the entire intrinsic lift is reconstructed from one complex Hermitian
section matrix:

    H32 = [[A,conj A],[conj A,A]],
    H_even = A+conj A = 2 Re(A),
    H_odd  = A-conj A = 2 i Im(A).

Because A is Hermitian, Re(A) is real symmetric and Im(A) is real skew-symmetric.
Thus the finite class-D-like odd block is literally the imaginary/antisymmetric part
of the old coordinate-section Hamiltonian, while the deck-even block is its real/
symmetric part.  The section matrix was not an intrinsic observable by itself, but it
contains both intrinsic parity sectors once its conjugate sheet is restored.

The one-sheet Feshbach operator becomes

    H_eff(E)=A+conj(A)(E-A)^(-1)conj(A).

Its poles are eigenvalues of the bare section A.  They are not physical eigenvalues
of H32; in the full Schur determinant they are cancelled by det(E-A).  Physical
energies are zeros of the complete determinant.  The verifier checks this separation.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import w33_pass5634_sheet_decimation_resolvent_rg as prev

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5679_SECTION_PARENT_REAL_IMAG_FESHBACH.json'


def clusters(vals,tol=1e-7):
    out=[]
    for x in np.sort(vals):
        if not out or abs(x-out[-1][0])>tol: out.append([float(x),1])
        else: out[-1][1]+=1
    return out


def main():
    H=prev.build32(); A=H[:16,:16]; B=H[:16,16:]
    assert np.max(abs(B-np.conj(A)))<1e-10
    He=A+B; Ho=A-B
    assert np.max(abs(He-2*np.real(A)))<1e-10
    assert np.max(abs(Ho-2j*np.imag(A)))<1e-10
    assert np.max(abs(np.real(A)-np.real(A).T))<1e-10
    assert np.max(abs(np.imag(A)+np.imag(A).T))<1e-10
    assert np.max(abs(He.conj()-He))<1e-10
    assert np.max(abs(Ho.conj()+Ho))<1e-10

    even=clusters(np.linalg.eigvalsh(He)); odd=clusters(np.linalg.eigvalsh(Ho))
    assert odd==[[-6.0,4],[-3.0,4],[3.0,4],[6.0,4]]
    # floating-safe checks on the known even spectrum
    expected_even=[(-6,2),(-3,3),(-1,3),(2,6),(3,1),(9,1)]
    assert len(even)==len(expected_even)
    for (x,m),(y,n) in zip(even,expected_even):
        assert abs(x-y)<1e-7 and m==n

    bare=np.linalg.eigvalsh(A)
    # There are 15 distinct bare poles because -2 occurs twice.
    bare_cl=clusters(bare); assert len(bare_cl)==15
    full=np.linalg.eigvalsh(H)
    assert all(np.min(abs(full-a))>1e-6 for a in bare)

    # Schur determinant identity at regular probe energies.
    probes=[-7.0,-5.5,0.25,4.25,10.0]
    max_rel=0.0
    I16=np.eye(16); I32=np.eye(32)
    for E in probes:
        assert np.min(abs(bare-E))>1e-4
        Heff=A+np.conj(A)@np.linalg.inv(E*I16-A)@np.conj(A)
        lhs=np.linalg.det(E*I32-H)
        rhs=np.linalg.det(E*I16-A)*np.linalg.det(E*I16-Heff)
        rel=abs(lhs-rhs)/max(1.0,abs(lhs),abs(rhs)); max_rel=max(max_rel,float(rel))
    assert max_rel<1e-7

    out={
      'pass':5679,
      'status':'ONE_SECTION_COMPLEX_PARENT_SPLITS_EXACTLY_INTO_REAL_EVEN_AND_IMAGINARY_CLASSD_ODD_SECTORS',
      'reconstruction':'H32=[[A,conj(A)],[conj(A),A]]',
      'deck_even':'H_+=2 Re(A), real symmetric',
      'deck_odd':'H_-=2 i Im(A), purely imaginary Hermitian with real skew generator',
      'even_spectrum':even,
      'odd_spectrum':odd,
      'bare_section_poles':bare_cl,
      'bare_distinct_poles':15,
      'bare_poles_coincide_with_full_physical_energies':False,
      'feshbach':'H_eff(E)=A+conj(A)(E-A)^(-1)conj(A)',
      'schur_identity':'det(E-H32)=det(E-A) det(E-H_eff(E))',
      'schur_probe_max_relative_error':max_rel,
      'interpretation':'The old section-dependent operator is a complex parent coordinate. Restoring the conjugate sheet converts its real and imaginary parts into the two intrinsic deck-parity sectors.',
      'physics_boundary':'Bare-section poles are coordinate/decimation poles, not particles. Only the deck-odd block has the K particle-hole symmetry used in the finite class-D analogy; the full 32-state matrix is not asserted to be a relativistic BdG theory.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()
