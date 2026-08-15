#!/usr/bin/env python3
"""Pass5360: all-odd complex Wedderburn theorem for the PSL2(q) pair Hecke algebra.

Input 1 (Pass5357): for Lambda=C(P^1(q),2),
  r(q)=dim End_{PSL2(q)} C[Lambda]
      =(3q+9)/4 if q=1 mod4,
       (3q+7)/4 if q=3 mod4.

Input 2 (Darafsheh--Pournaki, AAECC 10 (2000) 237--250,
DOI 10.1007/s002000050127, Theorem 4 proof): the permutation character xi on
2-subsets has multiplicities only 1 and 2.  For q=1 mod4 the multiplicity-two
constituents are psi and the chi_i with i=0 mod4; for q=3 mod4 they are the
theta_j with j=2 mod4.  The q mod8 exceptional xi_1,xi_2 or eta_1,eta_2, when
present, occur with multiplicity one.

Counting the multiplicity-two constituents gives
  d(q)=floor((q+3)/8).
Therefore, because the centralizer algebra of a complex permutation module with
multiplicities m_chi is direct sum M_{m_chi}(C),

  A_q ~= C^{s(q)} + M_2(C)^{d(q)},
  s(q)=r(q)-4d(q),
  dim Z(A_q)=r(q)-3d(q),
  dim [A_q,A_q]=3d(q).

This upgrades the finite Pass5359 pattern to an all-odd theorem and recovers
Pass5336 at q=5.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5360_ALLODD_PAIR_HECKE_WEDDERBURN.json'

def rank_formula(q):
    assert q%2==1
    return (3*q+9)//4 if q%4==1 else (3*q+7)//4

def data(q):
    r=rank_formula(q); d=(q+3)//8; s=r-4*d; z=s+d; c=3*d
    assert s>=0 and s+4*d==r and z==r-3*d and c==r-z
    if q%4==1:
        source_rule='multiplicity 2: psi plus chi_i with i divisible by 4'
    else:
        source_rule='multiplicity 2: theta_j with j congruent 2 mod 4'
    exceptional={1:'xi1,xi2 present with multiplicity 1',3:'eta1,eta2 present with multiplicity 1',5:'no exceptional pair',7:'no exceptional pair'}[q%8]
    return {'q':q,'q_mod_8':q%8,'orbital_rank':r,'M2_blocks':d,'scalar_blocks':s,
      'center_dimension':z,'commutator_dimension':c,'multiplicity_two_rule':source_rule,
      'exceptional_character_rule':exceptional,
      'wedderburn':f'C^{s} + M2(C)^{d}' if d else f'C^{s}'}

def main():
    rows={str(q):data(q) for q in (3,5,7,9,11,13,17,19,23,25,27,29,31,49)}
    # Exact reconciliation with the finite intersection-tensor census of Pass5359.
    finite={3:(4,0,4,0),5:(6,1,3,3),7:(7,1,4,3),11:(10,1,7,3),
            13:(12,2,6,6),17:(15,2,9,6),19:(16,2,10,6),23:(19,3,10,9)}
    for q,(r,d,z,c) in finite.items():
        x=data(q);assert (x['orbital_rank'],x['M2_blocks'],x['center_dimension'],x['commutator_dimension'])==(r,d,z,c)
    out={'pass':5360,'status':'THEOREM_ALLODD_COMPLEX_PAIR_HECKE_WEDDERBURN',
      'domain':'odd prime powers q',
      'theorem':'A_q = End_{PSL2(q)} C[C(P^1(q),2)] ~= C^{s(q)} + M2(C)^{d(q)}.',
      'd_formula':'d(q)=floor((q+3)/8)',
      's_formula':'s(q)=r(q)-4d(q), with r(q) from Pass5357',
      'center_formula':'dim Z(A_q)=r(q)-3d(q)',
      'commutator_formula':'dim [A_q,A_q]=3d(q)',
      'published_character_input':'Darafsheh--Pournaki, Applicable Algebra in Engineering, Communication and Computing 10 (2000), 237--250, DOI 10.1007/s002000050127, proof of Theorem 4.',
      'finite_tensor_reconciliation':'Pass5359 q=3,5,7,11,13,17,19,23 intersection tensors match exactly.',
      'sample_rows':rows,
      'boundary':'Complex/characteristic-zero centralizer theorem for the canonical pair space. It does not identify the modular characteristic-2 pair module and does not prove the all-odd footprint-rank theorem.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
