#!/usr/bin/env python3
"""Pass5141: cubic theta moment is the first nonconstant normalized local spectral moment.

For an induced simple graph adjacency A_S, tr(A_S)=0,
tr(A_S^2)=2|E(S)|, and tr(A_S^3)=6 T(S). Pass5134 fixes
2|E(S)|/|S|=8 for every q=3 codeword support. Pass5140 provides a family
where T(S)/|S| varies, so the normalized third moment is the first of these
local adjacency moments that distinguishes the supports.
"""
from __future__ import annotations
import json
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data/PART_W33_PASS5140_Q3_THETA_TRIANGLE_CURVATURE.json'
OUT=ROOT/'data/PART_W33_PASS5141_Q3_CUBIC_THETA_MOMENT.json'
def row(d):
    n=d['weight'];e=d['induced_edges'];t=d['selected_triangles']
    return {'weight':n,'normalized_moment_1':'0','normalized_moment_2':str(Fraction(2*e,n)),'normalized_moment_3':str(Fraction(6*t,n))}
def main():
    d=json.loads(SRC.read_text());assert d['pass']==5140
    rows={'chamber_star':row(d['single_chamber_star'])}
    rows.update({f'two_star_gallery_{k}':row(v) for k,v in d['two_star_xor_by_gallery_distance'].items()})
    assert {v['normalized_moment_2'] for v in rows.values()}=={'8'}
    assert [rows[k]['normalized_moment_3'] for k in rows]==['8','6','7','98/13','39/5']
    out={'pass':5141,'status':'THEOREM_Q3_CUBIC_THETA_MOMENT_FIRST_NONCONSTANT','identities':['tr(A_S)=0','tr(A_S^2)=2|E(S)|','tr(A_S^3)=6 T(S)'],'rows':rows,'conclusion':'Within this exact chamber-star/two-star family, normalized moments 1 and 2 are rigid (0 and 8), while normalized moment 3 varies. Thus the common-root triangle curvature is exactly a cubic spectral moment invisible to first-order theta expansion.','boundary':'This is an exact q=3 local spectral statement on the certified family. It does not prove that moment 3 alone classifies all codeword supports or proves q5/all-q distance.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
