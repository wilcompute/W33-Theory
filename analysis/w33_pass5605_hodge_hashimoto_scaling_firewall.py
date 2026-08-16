#!/usr/bin/env python3
"""Pass5605: all-q spectral-scaling firewall for Hodge and Hashimoto operators.

The current projectivity Gram was already ruled out as a spacetime Laplacian.
This pass tests the two strongest pre-existing dynamical candidates against an
all-q continuum criterion.  The result is also negative in the maximally
symmetric family: both have finite atomic scaling limits.
"""
from __future__ import annotations
import json, math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5605_HODGE_HASHIMOTO_SCALING_FIREWALL.json'


def hodge(q:int):
    # D^T D = 2I+A_X from Pass5388-5392.
    a=q*(q+1)**2//2
    b=q*(q*q+1)
    N=(q+1)**2*(q*q+1)
    vals=[0.0, q+1-math.sqrt(2*q), q+1.0, q+1+math.sqrt(2*q), 2*q+2.0]
    mult=[q**4,a,b,a,1]
    assert sum(mult)==N
    nonzero=N-q**4
    return {
      'q':q,'dimension':N,
      'spectrum':[{'eigenvalue':vals[i],'multiplicity':mult[i]} for i in range(5)],
      'cycle_fraction':q**4/N,
      'nonzero_scaled_by_q_plus_1':[
        {'value':vals[i]/(q+1),'fraction_within_nonzero':mult[i]/nonzero}
        for i in range(1,5)
      ],
    }


def hashimoto(q:int):
    # W(3,q) point graph parameters.
    v=(q+1)*(q*q+1); k=q*(q+1); m=v*k//2
    directed=v*k
    # Exact singular values of B: order rows by head, cols by tail. Each local
    # block is J_k-I_k.
    sing=[{'singular_value':k-1,'multiplicity':v},
          {'singular_value':1,'multiplicity':v*(k-1)}]
    assert sum(x['multiplicity'] for x in sing)==directed
    # Bass nontrivial roots normalized by sqrt(k-1).  Record angles where
    # roots are asymptotically on the unit circle.
    def roots(lam):
      disc=complex(lam*lam-4*(k-1),0)**0.5
      return ((lam+disc)/2,(lam-disc)/2)
    rpos=roots(q-1); rneg=roots(-(q+1))
    return {
      'q':q,'point_vertices':v,'degree':k,'directed_edges':directed,
      'BBt_singular_bands':sing,
      'extra_Bass_plus_minus_1_each_multiplicity':m-v,
      'nontrivial_normalized_roots':{
        'lambda_q_minus_1':[[z.real/math.sqrt(k-1),z.imag/math.sqrt(k-1)] for z in rpos],
        'lambda_minus_q_plus_1':[[z.real/math.sqrt(k-1),z.imag/math.sqrt(k-1)] for z in rneg],
      },
      'asymptotic_angles':'pi/3 and 2pi/3 for the two nontrivial adjacency sectors; the O(q^5) Bass +/-1 sector collapses to zero after sqrt(k-1) normalization.'
    }


def main():
    qs=(3,5,7,9,11,13,25,49,101)
    out={
      'status':'THEOREM_ATOMIC_SCALING_LIMIT_NO_WEYL_CONTINUUM',
      'hodge_theorem':(
        'For the Levi flag Hodge operator L1=D^T D, the normalized full spectral measure tends delta_0 because the q^4 cycle space occupies asymptotic fraction 1. '
        'After deleting the cycle sector and dividing eigenvalues by q+1, the remaining spectral measure tends delta_1 (the isolated top eigenvalue has vanishing weight).'
      ),
      'hashimoto_theorem':(
        'For every k-regular graph, the nonbacktracking matrix B has singular values k-1 (multiplicity v) and 1 (multiplicity v(k-1)), since B is permutation-equivalent locally to blocks J_k-I_k. '
        'For the W(3,q) point graph, Ihara-Bass nontrivial roots normalize to finitely many unit-circle atoms while the much larger extra +/-1 Bass sector collapses to zero.'
      ),
      'continuum_verdict':'Neither maximally symmetric all-q Hodge nor Hashimoto family has a Weyl-law spectral tower or stable nontrivial diffusion dimension. Any continuum dynamics must use symmetry breaking, a refinement/tower, phase-sensitive transport, disorder, or a different operator.',
      'hodge_samples':[hodge(q) for q in qs],
      'hashimoto_samples':[hashimoto(q) for q in qs],
      'boundary':'This is a no-go for these maximally symmetric scaling families, not a no-go for all Hodge/nonbacktracking dynamics after physical symmetry breaking or on a multiscale tower.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__': main()
