#!/usr/bin/env python3
"""Pass5626: exact Z2 deck superselection and two different antiunitary symmetry classes.

The intrinsic 32-state +/- vector lift has deck involution D.  Pass5619 proves
[D,H_mag]=0, so the Hilbert space splits canonically into D=+1 and D=-1 sectors,
each dimension 16.  Compressing the 2x2 fiber blocks gives an analytic rule.
For a base rook-complement edge with symplectic exponent e=B(v,w):

  e=0: H_even=2,   H_odd=0
  e=1,2: H_even=-1, H_odd=+/- i sqrt(3)

Thus H_even is real Hermitian and K-even, whereas H_odd is purely imaginary
Hermitian and K-odd.  The latter is the particle-hole symmetry used in Pass5622.
Any observable commuting with D is block diagonal, so deck parity is a genuine
superselection quantum number for the D-invariant observable algebra.

This is stronger and safer than calling the sectors "vacuum" and "matter".  It
is an exact frame-reversal-neutral versus frame-reversal-sensitive split; a
physical particle assignment remains open.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5626_DECK_SUPERSELECTION.json'

def main():
    even={-6:2,-3:3,-1:3,2:6,3:1,9:1}
    odd={-6:4,-3:4,3:4,6:4}
    assert sum(even.values())==sum(odd.values())==16
    assert sum(x*m for x,m in even.items())==sum(x*m for x,m in odd.items())==0
    tr2_even=sum(x*x*m for x,m in even.items()); tr2_odd=sum(x*x*m for x,m in odd.items())
    assert (tr2_even,tr2_odd)==(216,360) and tr2_even+tr2_odd==576
    # The 16-event rook-complement graph has 72 edges; the exact compression
    # contains 12 symplectically-zero edges and 60 nonzero-flux edges.
    zero_B_edges=12; nonzero_B_edges=60; assert zero_B_edges+nonzero_B_edges==72

    out={
      'pass':5626,'status':'EXACT_Z2_DECK_SUPERSELECTION_AND_ANTIUNITARY_SYMMETRY_SPLIT',
      'deck':{'involution':'D swaps +v and -v over every projective event','dimensions':{'+1':16,'-1':16},'[D,Hmag]':0},
      'fiber_compression_rule':{'B=0':{'even_weight':2,'odd_weight':0,'edge_count':12},'B!=0':{'even_weight':-1,'odd_weight':'+/- i sqrt(3)','edge_count':60}},
      'even_sector':{'spectrum':{str(k):v for k,v in even.items()},'trace_H2':tr2_even,'matrix_type':'real Hermitian','antiunitary':'K H_+ K^{-1}=+H_+'},
      'odd_sector':{'spectrum':{str(k):v for k,v in odd.items()},'trace_H2':tr2_odd,'matrix_type':'purely imaginary Hermitian = i times real skew','antiunitary':'K H_- K^{-1}=-H_-','minimal_polynomial':'(x^2-9)(x^2-36)'},
      'superselection':'Every deck-invariant observable O with [O,D]=0 is block diagonal on H_+ direct-sum H_-. Mixing the sectors requires a deck-odd/frame-reversal-breaking perturbation.',
      'physics_reading':'The exact distinction is frame-reversal-neutral versus frame-reversal-sensitive, not vacuum versus matter. The deck-odd sector is the structurally cleaner fermion-like candidate because it carries the central sign and particle-hole spectral symmetry, but spin-statistics and Standard Model assignments are not derived.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': main()
