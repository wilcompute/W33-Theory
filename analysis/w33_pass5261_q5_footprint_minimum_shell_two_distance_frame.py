#!/usr/bin/env python3
"""Pass5261 (outside-box): the exact q=5 footprint minimum shell is a two-distance tight frame.

Authoritative Pass5238 proves C_F=[325,65,25]_2 and that its 156 minimum
supports are exactly the W(3,5) point footprints.  Let F be their 156x325
incidence matrix.  Pass5201 gives

  F F^T = 24 I + 4 A_W + J,

where A_W is the W(3,5) collinearity graph, with spectrum 30^1,4^90,(-6)^65.
Thus the row Gram has spectrum 300^1,40^90,0^65.

Every footprint coordinate lies in12 minimum words, so the row centroid is
m=(1/13)1_325.  Centering removes the 300-dimensional uniform eigenline and
leaves Gram spectrum 40^90,0^66.  Hence the 156 centered minimum-shell vectors
form an equal-norm tight frame for a 90-dimensional real space.

After unit normalization their two off-diagonal inner products are

  collinear W points: 2/15,
  noncollinear W points: -1/25.

This packages the binary minimum shell as a real two-distance spherical frame.
"""
from __future__ import annotations
import json
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5261_Q5_FOOTPRINT_MINIMUM_SHELL_TWO_DISTANCE_FRAME.json'

def main():
    n=156;ambient=325;w=25;coord_rep=12
    gram_spec={300:1,40:90,0:65}
    centroid=Fraction(coord_rep,n);assert centroid==Fraction(1,13)
    norm2=Fraction(w,1)-Fraction(25,13);assert norm2==Fraction(300,13)
    coll=Fraction(5,1)-Fraction(25,13);non=Fraction(1,1)-Fraction(25,13)
    assert coll==Fraction(40,13) and non==Fraction(-12,13)
    assert coll/norm2==Fraction(2,15) and non/norm2==Fraction(-1,25)
    assert Fraction(n,1)*norm2/Fraction(90,1)==40
    out={'pass':5261,'status':'THEOREM_Q5_FOOTPRINT_MINIMUM_SHELL_TWO_DISTANCE_TIGHT_FRAME',
      'minimum_shell':{'code':'C_F=[325,65,25]_2','minimum_words':156,'supports':'exactly the W(3,5) point footprints'},
      'incidence_Gram':'F F^T=24I+4A_W+J',
      'uncentered_Gram_spectrum':{'300':1,'40':90,'0':65},
      'centroid':'(1/13) 1_325','centered_vector_norm_squared':'300/13',
      'centered_Gram_spectrum':{'40':90,'0':66},
      'tight_frame_dimension':90,'tight_frame_bound':40,
      'unit_inner_products':{'collinear_points':'2/15','noncollinear_points':'-1/25'},
      'interpretation':'The exact binary minimum shell becomes a 156-vector two-distance unit-norm tight frame after centering; its two distances recover W(3,5) collinearity.',
      'boundary':'This is a finite code/real-frame theorem. It does not close the strict zero-footprint apartment-code sector or imply a physical state-space embedding.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
