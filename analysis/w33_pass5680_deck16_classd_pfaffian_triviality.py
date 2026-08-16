#!/usr/bin/env python3
"""Pass5680 bonkers: the deck-odd 16 has a *trivial* equivariant 0D class-D Pfaffian index.

For a purely imaginary Hermitian BdG/Majorana block H=iS with S real skew, the
zero-dimensional class-D invariant can be represented by the sign of Pf(S) once an
orientation convention is fixed.  Pass5675 gives the full stabilizer-equivariant cone:

    spec(H) = {+/-lambda_1 each x4, +/-lambda_2 each x4}.

Therefore

    |Pf(S)| = |lambda_1 lambda_2|^4.

A level crossing changes four Majorana pairs at once, so the usual Z2 Pfaffian sign is
not forced to flip.  This verifier checks something stronger in the canonical deck
coordinate orientation: all three signature components of the gapped Hermitian-2x2
moduli space have the SAME Pfaffian sign.

Representatives are:
  * X positive definite:  J = Hmag/2 - Hmag^3/54, with spectrum +/-1 each x8;
  * X negative definite: -J;
  * X indefinite:         Hmag, with levels 3 and 6.

All have negative Pfaffian in the fixed repo ordering.  Hence the entire gapped
G-equivariant cone is one class-D Z2 phase even though it has disconnected signature
components before forgetting the fourfold degeneracy.  No nontrivial topological bit
protects the mass ratio or chooses a Standard Model sector.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import w33_pass5630_deck_bdg_commutant_mass_ratio_unprotected as prev

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5680_DECK16_CLASSD_PFAFFIAN_TRIVIALITY.json'


def pfaffian(A,tol=1e-12):
    A=np.array(A,dtype=float).copy(); n=A.shape[0]
    assert n%2==0 and np.max(abs(A+A.T))<1e-8
    pf=1.0
    for k in range(0,n,2):
        j=max(range(k+1,n),key=lambda q:abs(A[k,q]))
        if abs(A[k,j])<tol:return 0.0
        if j!=k+1:
            A[[k+1,j],:]=A[[j,k+1],:]
            A[:,[k+1,j]]=A[:,[j,k+1]]
            pf*=-1
        piv=A[k,k+1];pf*=piv
        if k+2<n:
            a=A[k,k+2:].copy();b=A[k+1,k+2:].copy()
            A[k+2:,k+2:]+=(np.outer(b,a)-np.outer(a,b))/piv
    return float(pf)


def abs_levels(H):
    ev=np.linalg.eigvalsh(H);vals=[]
    for x in ev[ev>1e-8]:
        if not vals or abs(x-vals[-1])>1e-7:vals.append(float(x))
    return vals


def row(name,H):
    S=(-1j*H).real
    assert np.max(abs(S+S.T))<1e-9
    vals=abs_levels(H)
    pf=pfaffian(S)
    mag=float(np.prod(vals)**4) if len(vals)==2 else 1.0
    # For the +/-1^8 representative there is one distinct positive level but
    # eight canonical pairs, so |Pf|=1.
    assert abs(abs(pf)-mag)<1e-7
    return {'representative':name,'positive_distinct_levels':vals,
            'pfaffian':pf,'pfaffian_sign':int(np.sign(pf))}


def main():
    _,Rs,H=prev.build()
    J=H/2-(H@H@H)/54
    assert np.allclose(np.sort(np.linalg.eigvalsh(J)),[-1]*8+[1]*8,atol=1e-8)
    assert max(np.max(abs(R@J-J@R)) for R in Rs)<1e-8
    assert np.max(abs(J.conj()+J))<1e-8

    reps=[row('X positive definite (J)',J),
          row('X negative definite (-J)',-J),
          row('X indefinite (Hmag)',H)]
    assert {r['pfaffian_sign'] for r in reps}=={-1}
    # Exact magnitude at the magnetic point: (3*6)^4=104976.
    assert abs(reps[2]['pfaffian']+104976)<1e-5

    out={
      'pass':5680,
      'status':'EQUIVARIANT_DECK16_CLASSD_PFAFFIAN_INDEX_IS_TRIVIAL_ACROSS_ALL_GAPPED_SIGNATURE_COMPONENTS',
      'classD_setup':'H=iS, S real skew; use sign Pf(S) in the fixed deck basis orientation',
      'general_magnitude':'|Pf(S)|=|lambda1 lambda2|^4 because each positive level occurs with multiplicity four',
      'signature_component_representatives':reps,
      'magnetic_pfaffian_exact':'-104976 = -(3*6)^4 in the canonical repo ordering',
      'topological_conclusion':'positive-definite, indefinite, and negative-definite multiplicity matrices all have the same Pfaffian sign; the fourfold carrier degeneracy makes the 0D class-D Z2 index trivial on the full symmetry-allowed gapped cone',
      'mass_consequence':'the class-D Pfaffian bit cannot protect the ratio 6/3=2 or distinguish one allowed mass-ratio component from another',
      'prior_art_boundary':'The class-D/Pfaffian classification is standard free-fermion topology (e.g. Kitaev arXiv:0901.2686). The new statement here is only the finite W33 carrier calculation.',
      'physics_boundary':'No relativistic spin-statistics theorem, physical fermion parity assignment, or interacting topological classification is claimed.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()
