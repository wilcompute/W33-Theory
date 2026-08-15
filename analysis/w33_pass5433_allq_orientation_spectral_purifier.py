#!/usr/bin/env python3
"""Pass5433: orientation signs are an exact all-q Hodge spectral purifier.

For the same flag/apartment carrier, Pass5404 gives the unsigned Gram
  U=q^4 A0+q^3 A1+q^2 A2+q A3+A4,
which is positive definite on all five primitive flag sectors.  Pass5396 gives
  S=q^4 A0-q^3 A1+q^2 A2-q A3+A4=N E_cyc,
where N=(q+1)^2(q^2+1).
Thus changing only the signs on the odd-distance shells A1,A3 annihilates the
four non-cycle primitive sectors exactly and retains the q^4-dimensional cycle
sector with one flat eigenvalue N.  The diagonal and hence total trace are
unchanged; orientation does not remove coordinate energy, it reorganizes it
into the Hodge cycle projector.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5433_ALLQ_ORIENTATION_SPECTRAL_PURIFIER.json'
ANCHORS=(2,3,4,5,7,8,9,11,13)

def row(q:int)->dict:
    N=(q+1)**2*(q*q+1);r=q**4;cut=N-r
    vertices=2*(q+1)*(q*q+1)
    assert cut==vertices-1
    trace=N*r
    return {'q':q,'flags':N,'cycle_rank':r,'cut_rank':cut,
      'unsigned_rank':N,'signed_rank':r,'common_trace':trace,
      'signed_nonzero_eigenvalue':N}

def main():
    rows={str(q):row(q) for q in ANCHORS}
    assert rows['3']=={'q':3,'flags':160,'cycle_rank':81,'cut_rank':79,'unsigned_rank':160,'signed_rank':81,'common_trace':12960,'signed_nonzero_eigenvalue':160}
    out={
      'pass':5433,'status':'THEOREM_ALLQ_ORIENTATION_SIGNS_EXACT_HODGE_SPECTRAL_PURIFIER',
      'domain':'finite generalized quadrangles GQ(q,q), q>1',
      'unsigned':'U=q^4 A0+q^3 A1+q^2 A2+q A3+A4; full rank N.',
      'signed':'S=q^4 A0-q^3 A1+q^2 A2-q A3+A4=N E_cyc; rank q^4.',
      'difference':'U-S=2(q^3 A1+q A3): only odd flag-distance shells change sign.',
      'purifier_statement':'That odd-shell sign change kills every primitive flag sector except the terminal Hodge/cycle sector, on which the eigenvalue becomes the flat value N.',
      'rank_removed':'N-q^4=2(q+1)(q^2+1)-1=rank of the Levi cut space.',
      'trace_conservation':'tr(U)=tr(S)=N q^4. The operation is spectral cancellation, not deletion of diagonal coordinate energy.',
      'anchors':rows,
      'boundary':'Algebraic Hodge filtering of apartment incidence. The word purifier denotes exact spectral projection here, not a thermodynamic or physical decoherence process.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
