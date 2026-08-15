#!/usr/bin/env python3
"""Pass5376: close the all-odd binary footprint rank theorem.

Let M=F2^{L1} be the point permutation module of W(3,q), q odd, and let
C_W=Im(eta_{2,1}) be the binary point-line incidence code.  The footprint
matrix F has one row per W-point and one column per polarity pair of
non-isotropic projective lines; the column is the indicator of H union H^perp.

Elementary geometry from Pass5201/5288 gives:
  (i) every W-line meets every footprint block in 0 or 2 points, hence
      im(F) <= C_W^perp;
  (ii) every point occurs in q^2 footprint blocks, so the sum of all columns
       of F is the all-one vector 1 (q odd);
  (iii) one footprint block has weight 2(q+1), strictly between 0 and
        v=(q+1)(q^2+1), hence im(F) is strictly larger than <1>.

The module-theoretic input is Lataille--Sin--Tiep, J. Algebra 268 (2003),
Theorem 2.13 together with Lemmas 2.5--2.7 and Remark 2.15.  Their incidence
map eta_{m,1} sends a maximal isotropic m-space to the formal sum of its
incident points.  For m=2, their C=Im(eta_{2,1}) is exactly C_W.  They prove
C^perp=U'.  Since m=2 is even, U' is uniserial with composition series

    U' > <1> > 0.

Remark 2.15 carries the lattice to every field of characteristic 2; over F2
the only q mod 8 change occurs in the middle Weil quotient, not in this bottom
interval.  Thus C_W^perp/<1> is simple over F2.

Now im(F) is a G-submodule with

    <1> < im(F) <= C_W^perp.

Simplicity forces im(F)=C_W^perp.  Lataille--Sin--Tiep also give

    dim C_W = 1 + q(q+1)^2/2,

so

    rank_2(F)=dim C_W^perp=q(q^2+1)/2.

Taking orthogonal complements gives ker(F^T)=C_W.  This closes the all-odd
rank-complement conjecture, not merely another finite anchor.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5376_ALLODD_FOOTPRINT_RANK_MODULE_CLOSURE.json'

def dims(q:int)->dict[str,int]:
    assert q%2==1 and q>=3
    v=(q+1)*(q*q+1)
    f=q*(q+1)**2//2
    g=q*(q*q+1)//2
    c=1+f
    assert v==c+g
    block=2*(q+1)
    components=q*q*(q*q+1)//2
    row_weight=q*q
    assert 0<block<v and row_weight%2==1
    return {'q':q,'points_v':v,'line_code_dimension':c,
      'point_code_dimension_g':g,'footprint_block_weight':block,
      'P_components':components,'components_through_point':row_weight,
      'binary_footprint_rank':g,'binary_kernel_dimension':c}

def main()->None:
    sample={str(q):dims(q) for q in (3,5,7,9,11,13,17,19,25,27,49)}
    anchors={3:15,5:65,7:175,9:369,11:671,13:1105}
    for q,r in anchors.items():assert dims(q)['binary_footprint_rank']==r
    out={
      'pass':5376,
      'status':'THEOREM_ALLODD_BINARY_FOOTPRINT_RANK_CLOSED',
      'domain':'all odd prime powers q',
      'theorem':'im_2(F)=C_W^perp; rank_2(F)=q(q^2+1)/2; ker_2(F^T)=C_W.',
      'module_argument':[
        'LST define C=Im(eta_{m,1}); at m=2 this is exactly the W(3,q) binary line-incidence code C_W.',
        'LST prove C^perp=U_prime.',
        'For m=2 even, U_prime is uniserial U_prime > <1> > 0, so C_W^perp/<1> is simple.',
        'LST Remark 2.15 transports the lattice to arbitrary characteristic-2 fields; over F2 only the middle Weil quotient changes when q=+-3 mod8.',
        'Every footprint block has even intersection with every W-line, so im(F)<=C_W^perp.',
        'Each point belongs to q^2 components, hence the sum of all footprint columns is 1 over F2.',
        'A footprint block has weight 2(q+1)<v, so im(F) is strictly larger than <1>.',
        'Simplicity of C_W^perp/<1> forces im(F)=C_W^perp.'
      ],
      'dimension_input':'LST Theorem 2.13 recalls dim C = 1 + q(q^m-1)(q^(m-1)+1)/(2(q-1)); at m=2 this is 1+q(q+1)^2/2.',
      'primary_source':{
        'authors':'J. M. Lataille, Peter Sin, Pham Huu Tiep',
        'title':'The modulo 2 structure of rank 3 permutation modules for odd characteristic symplectic groups',
        'journal':'Journal of Algebra 268 (2003)',
        'author_pdf':'https://people.clas.ufl.edu/sin/files/paper2.pdf',
        'used_results':'definition of eta_{r,s}; Lemmas 2.5--2.7; C=Im eta_{m,1}; C^perp=U_prime; Theorem 2.13; Remark 2.15'
      },
      'finite_anchor_reconciliation':{str(q):r for q,r in anchors.items()},
      'sample_dimensions':sample,
      'boundary':'This closes the binary rank/kernel equality only. It does not by itself determine the minimum distance of im(F^T), the q=11 dual weight-20 existence question, or the Hoffman shortened-code distance.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
