#!/usr/bin/env python3
"""Pass5428: canonical dual/tomography theorem for oriented GQ(q,q) apartments.

Pass5396 proves, for the signed flag-by-apartment matrix C,

    C C^T = N E_cyc,
    N=(q+1)^2(q^2+1),

where E_cyc is the orthogonal projector onto the q^4-dimensional Levi cycle
space.  Hence every nonzero singular value of C is sqrt(N), the Moore--Penrose
inverse is C^+=N^{-1} C^T on the cycle image, and every cycle flow z has the
canonical minimum-l2 apartment reconstruction

    a_A = <c_A,z>/N,        z = sum_A a_A c_A.

Equivalently sum_A <c_A,z>^2 = N ||z||^2.  Since ||c_A||^2=8, the normalized
apartments u_A=c_A/sqrt(8) form a unit-norm tight frame with frame bound N/8
and canonical dual (8/N)u_A.
"""
from __future__ import annotations
import json
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5428_ALLQ_ORIENTED_APARTMENT_TOMOGRAPHY.json'
ANCHORS=(2,3,4,5,7,8,9,11,13)

def row(q:int)->dict:
    N=(q+1)**2*(q*q+1)
    r=q**4
    A=N*r//8
    assert N*r==8*A
    return {
      'q':q,'flags':N,'cycle_rank':r,'apartments':A,
      'nonzero_singular_value_squared':N,
      'moore_penrose':'C^+=(1/N) C^T on im(C)=Z1',
      'cycle_reconstruction':'z=(1/N) C C^T z for z in Z1',
      'coefficient_energy':f'||a_min||^2=||z||^2/{N}',
      'parseval_energy':f'sum_A <c_A,z>^2={N}||z||^2',
      'unit_frame_bound':str(Fraction(N,8)),
      'redundancy':str(Fraction(A,r)),
    }

def main():
    rows={str(q):row(q) for q in ANCHORS}
    assert rows['3']['flags']==160 and rows['3']['cycle_rank']==81 and rows['3']['apartments']==1620
    assert rows['3']['unit_frame_bound']=='20' and rows['3']['redundancy']=='20'
    out={
      'pass':5428,'status':'THEOREM_ALLQ_CANONICAL_ORIENTED_APARTMENT_TOMOGRAPHY',
      'domain':'finite generalized quadrangles GQ(q,q), q>1',
      'input':'Pass5396: C C^T = N E_cyc with N=(q+1)^2(q^2+1).',
      'pseudoinverse':'C^+=(1/N)C^T on the cycle image; C C^+=E_cyc.',
      'minimum_norm_reconstruction':'For every real Levi cycle flow z, a_min=C^T z/N is the unique minimum-l2 coefficient vector among all apartment decompositions Ca=z.',
      'tight_frame_energy':'sum_A <c_A,z>^2=N||z||^2 and ||a_min||^2=||z||^2/N.',
      'normalized_frame':'u_A=c_A/sqrt(8) is unit norm, frame bound N/8, canonical dual (8/N)u_A.',
      'anchors':rows,
      'boundary':'Real/characteristic-zero frame tomography. This does not assert a binary unique decoding theorem or physical-noise threshold.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
