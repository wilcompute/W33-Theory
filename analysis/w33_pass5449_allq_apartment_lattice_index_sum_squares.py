#!/usr/bin/env python3
"""Pass5449: all-q apartment lattice index sum-of-squares theorem.

Let Lambda=Z_1(Levi;Z) be the integral cycle lattice, rank r=q^4.  Pass5439 gives
an apartment fundamental-cycle Z-basis, and Pass5441 gives its squared covolume

  covol(Lambda)^2 = tau(Levi)
    =(q^2+1)^(f-1)(q+1)^(2g).

For any r-subset S of signed apartment columns:
- if dependent, set m_S=0;
- if independent, the columns span a finite-index sublattice Lambda_S<=Lambda,
  with integer index m_S=[Lambda:Lambda_S].  Lattice covolumes give

    det(C_S^T C_S)=tau * m_S^2.

Pass5444 gives sum_S det(C_S^T C_S)=N^r.  Therefore

    sum_{|S|=r} m_S^2 = N^r/tau.

This is an exact integer identity.  In particular index-one apartment lattice
bases contribute one each, while higher-index real apartment bases contribute
perfect-square weights.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5449_ALLQ_APARTMENT_LATTICE_INDEX_SUM_SQUARES.json'
ANCHORS=(2,3,4,5,7,8,9,11,13)

def row(q:int)->dict:
    N=(q+1)**2*(q*q+1);r=q**4;f=q*(q+1)**2//2;g=q*(q*q+1)//2
    e1=2*r-2*g;e2=r-(f-1)
    assert e1>=0 and e2>=0
    return {'q':q,'rank':r,'flags':N,
      'sum_of_index_squares':f'(q+1)^{e1}(q^2+1)^{e2}',
      'exponents':{'q+1':e1,'q^2+1':e2}}

def main():
    rows={str(q):row(q) for q in ANCHORS}
    assert rows['3']['exponents']=={'q+1':132,'q^2+1':58}
    out={
      'pass':5449,'status':'THEOREM_ALLQ_APARTMENT_LATTICE_INDEX_SUM_OF_SQUARES',
      'domain':'finite generalized quadrangles GQ(q,q), q>1',
      'cycle_lattice':'Lambda=Z_1(Levi;Z), rank q^4, squared covolume tau(Levi).',
      'individual_volume_quantization':'For every independent q^4-apartment set S, det(C_S^T C_S)=tau(Levi)*[Lambda:Lambda_S]^2.',
      'global_identity':'sum_{|S|=q^4} m_S^2=N^(q^4)/tau(Levi), with m_S=0 for dependent S.',
      'closed_form_rhs':'(q+1)^(2q^4-2g) (q^2+1)^(q^4-f+1), f=q(q+1)^2/2, g=q(q^2+1)/2.',
      'q3':'sum m_S^2 = 2^322*5^58.',
      'interpretation':'The real tight-frame Cauchy-Binet volume budget decomposes into perfect-square integer lattice-index packets.',
      'anchors':rows,
      'boundary':'This identity does not enumerate index-one bases or assert that all real apartment bases generate the full integer cycle lattice.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
