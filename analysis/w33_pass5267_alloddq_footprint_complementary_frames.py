#!/usr/bin/env python3
"""Pass5267: all-odd-q complementary real footprint frames and the modular-rank target.

For odd q, Pass5201 gives the point/P-component incidence Gram law

  F F^T = (q^2-1) I + (q-1) A_W + J,

where A_W is the W(3,q) point-collinearity graph.  Its nontrivial eigenvalues are
r=q-1 and s=-(q+1), with multiplicities

  f=q(q+1)^2/2,  g=q(q^2+1)/2,

and v=(q+1)(q^2+1)=1+f+g.

Hence over R the footprint Gram has eigenvalues

  2q^2(q+1)^1,  [2q(q-1)]^f,  0^g.

After subtracting the centroid 2/(q^2+1) on the P-component coordinates, the v
point-footprint vectors form a two-distance tight frame in the f-dimensional
r-eigenspace.  After unit normalization their inner products are

  (q-1)/(q(q+1))  for collinear points,
  -1/q^2           for noncollinear points.

Taking the Naimark complement and then removing its constant direction gives the
complementary centered frame in the g-dimensional s-eigenspace.  Its normalized
inner products are

  -1/q  for collinear points,
  +1/q^2 for noncollinear points.

At q=3,5,7, Pass5202 computes rank_2(F)=15,65,175, exactly g.  Thus the verified
binary footprint dimension equals the multiplicity of the negative real
W-eigenspace at all three anchors.  This is a structural target for the all-odd-q
binary-rank theorem, not a proof of it.

Literature boundary: Bagchi-Brouwer-Wilbrink (1991) determine dimensions of
binary line/neighborhood codes for Sp(4,q) and dual O(5,q), and Lataille-Sin-Tiep
(2003) determine mod-2 submodule lattices for the relevant rank-3 symplectic and
orthogonal permutation modules.  Those works justify using the classical O5
modular-module framework, but the accessible statements do not by themselves
identify this P-component footprint code or prove its minimum distance.
"""
from __future__ import annotations
import json
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5267_ALLODDQ_FOOTPRINT_COMPLEMENTARY_FRAMES.json'

def row(q):
    v=(q+1)*(q*q+1);f=q*(q+1)**2//2;g=q*(q*q+1)//2
    assert v==1+f+g
    norm=Fraction(q*q*(q*q-1),q*q+1)
    rawbound=2*q*(q-1)
    pos_col=Fraction(q-1,q*(q+1));pos_non=Fraction(-1,q*q)
    neg_col=Fraction(-1,q);neg_non=Fraction(1,q*q)
    return {'q':q,'vectors':v,'positive_frame_dimension':f,'negative_frame_dimension':g,
      'real_Gram_spectrum':{str(2*q*q*(q+1)):1,str(rawbound):f,'0':g},
      'centroid':f'2/{q*q+1}','centered_norm_squared':str(norm),
      'positive_unit_inner_products':{'collinear':str(pos_col),'noncollinear':str(pos_non)},
      'negative_unit_inner_products':{'collinear':str(neg_col),'noncollinear':str(neg_non)}}

def main():
    A={str(q):row(q) for q in (3,5,7,9,11)}
    ranks={'3':15,'5':65,'7':175}
    for qs,r in ranks.items():assert A[qs]['negative_frame_dimension']==r
    out={'pass':5267,'status':'THEOREM_ALLODDQ_FOOTPRINT_COMPLEMENTARY_TWO_DISTANCE_FRAMES',
      'domain':'odd prime powers q',
      'positive_frame':'dimension f=q(q+1)^2/2; unit inner products (q-1)/(q(q+1)) on collinear pairs and -1/q^2 on noncollinear pairs.',
      'negative_frame':'dimension g=q(q^2+1)/2; unit inner products -1/q on collinear pairs and +1/q^2 on noncollinear pairs.',
      'decomposition':'v=(q+1)(q^2+1)=1+f+g; the two centered frames are the r=q-1 and s=-(q+1) eigenspace embeddings of the W(3,q) point graph.',
      'binary_rank_anchors':{'q3':15,'q5':65,'q7':175},
      'anchor_alignment':'At q=3,5,7, rank_2(F)=g exactly.',
      'literature_context':['Bagchi-Brouwer-Wilbrink, Geometriae Dedicata 39 (1991), binary codes for Sp(4,q) and dual O(5,q).','Lataille-Sin-Tiep, J. Algebra 268 (2003), complete mod-2 rank-3 permutation-module structure with similar O(5,q) results.'],
      'anchors':A,
      'boundary':'The real frame theorem is all odd q. The identity rank_2(F)=g remains computationally certified only at q=3,5,7 here; no all-odd-q footprint minimum-distance theorem is claimed.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
