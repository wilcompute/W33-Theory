#!/usr/bin/env python3
"""Pass5382: exact characteristic-2 primary projectors for the q=5 connected-L graph.

Pass5240 determines the q=5 GF(2) Jordan structure of A=A_L:
  zero primary: J1^2156 + J3^520  (dimension 3716),
  one primary : J1^804 + J2^1471 + J3^48 + J4^536 (dimension 6034).
Hence the exact minimal polynomial is x^3 (x+1)^4.  Over F2,
(x+1)^4=x^4+1.  Chinese remainder therefore gives an unexpectedly simple pair
of canonical polynomial projectors:

  P_1 = A^4,
  P_0 = I + A^4.

Indeed A^4 vanishes on the 0-primary component (nilpotence index <=3) and equals
I on the 1-primary component because A=I+N with N^4=0.  Thus P_i^2=P_i,
P_0P_1=0, P_0+P_1=I, with ranks 3716 and 6034.

This does not repair the Pass5266 channelwise-Jordan no-go: the raw 10-channel
syndrome images are not A-invariant.  Rather it supplies a canonical invariant
that any correct twisted 10-dimensional channel transport must respect after
forgetting channel coordinates.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5382_Q5_CONNECTEDL_PRIMARY_PROJECTORS.json'

def main():
    zero_blocks={1:2156,3:520}; one_blocks={1:804,2:1471,3:48,4:536}
    z=sum(k*v for k,v in zero_blocks.items());o=sum(k*v for k,v in one_blocks.items())
    assert (z,o,z+o)==(3716,6034,9750)
    # Polynomial identities in F2[x]/(x^3(x+1)^4): P1=x^4, P0=1+x^4.
    # Idempotence residual x^8+x^4 is divisible by both primary factors.
    out={'pass':5382,'status':'THEOREM_Q5_CONNECTEDL_GF2_CANONICAL_PRIMARY_PROJECTORS',
      'dimension':9750,
      'minimal_polynomial':'x^3 (x+1)^4 over F2',
      'zero_primary':{'dimension':z,'Jordan_blocks':{'J1':2156,'J3':520},'projector':'P0=I+A_L^4'},
      'one_primary':{'dimension':o,'Jordan_blocks':{'J1':804,'J2':1471,'J3':48,'J4':536},'projector':'P1=A_L^4'},
      'identities':['P0^2=P0','P1^2=P1','P0 P1=0','P0+P1=I'],
      'reason':'On the zero-primary space A^3=0, hence A^4=0. On the one-primary space A=I+N with N^4=0, so A^4=(I+N)^4=I in characteristic2.',
      'transport_consequence':'Any proposed scalar connected-L invariant subspace is automatically split by A_L^4 into its generalized 0/1-primary parts. Pass5266 shows the raw even/full 10-channel syndrome images fail this invariance, so a correct lift must use nontrivial channel transport rather than A_L tensor I_10.',
      'boundary':'Exact scalar q5 GF2 theorem. It does not construct the missing twisted 10-channel transport and by itself gives no new distance bound.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
