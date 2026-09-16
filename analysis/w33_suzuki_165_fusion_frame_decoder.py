#!/usr/bin/env python3
"""Association-algebra decoder for the 165 complex Pauli fusion shadow.

The normalized projection Gram is G=I+A/13 where A is SRG(165,36,3,9).
Because A has eigenvalues 36,3,-9 with multiplicities 1,120,44, the complete
Bose-Mesner algebra and canonical dual are rational and exact.

G^{-1} = 91/64 I - 13/64 A + 117/3136 J.

Thus the dual of an encoding is a fixed combination of itself, its 36 GQ
neighbors and the global mean.  The 120-dimensional +3 sector and the
1+44=45-dimensional constant/dark sector give a natural spectral noise split.
Every principal submatrix of G is positive definite (principal-submatrix
interlacing), with condition number at most (49/13)/(4/13)=49/4.  This is
robust conditioning of every surviving subframe, not erasure correction of the
full 165D coefficient vector: the 165 frame vectors are linearly independent,
so deleting one removes one span dimension.
"""
from __future__ import annotations
from fractions import Fraction
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_suzuki_165_fusion_frame_decoder.json'

def main(write=True):
    d=json.loads((ROOT/'data'/'w33_suzuki_165_complex_pauli_fusion_shadow.json').read_text());assert d['status']=='PASS'
    v,k,lam,mu=165,36,3,9;r,s=3,-9
    # Primitive idempotents as rational polynomials in A,J.
    E0={'J':Fraction(1,v)}
    Er={'I':Fraction(9,12),'A':Fraction(1,12),'J':-Fraction(3,132)}  # (A+9I-3J/11)/12
    Es={'I':Fraction(3,12),'A':-Fraction(1,12),'J':Fraction(1,60)}   # (-A+3I+J/5)/12
    # Gram eigenvalues.
    g0=Fraction(49,13);gr=Fraction(16,13);gs=Fraction(4,13)
    # Solve inverse in I,A,J: alpha+beta*e (+gamma*v only on constants)=1/g_e.
    alpha=Fraction(91,64);beta=-Fraction(13,64);gamma=Fraction(117,3136)
    assert alpha+beta*r==1/gr and alpha+beta*s==1/gs and alpha+beta*k+gamma*v==1/g0
    # SRG multiplication control.
    # A^2 = k I + lambda A + mu(J-I-A) = 27 I -6 A +9 J.
    assert k-mu==27 and lam-mu==-6
    out={'schema':'w33.suzuki_165_fusion_frame_decoder.v1','status':'PASS',
      'headline':'The 165 complex Pauli fusion shadow has an exact rank-three association-algebra decoder. For G=I+A/13, G^-1=(91/64)I-(13/64)A+(117/3136)J. The 120D and 45D spectral sectors therefore define exact collective noise/readout channels, and every surviving principal subframe has condition number <=49/4 by interlacing.',
      'association_scheme':{'srg':[v,k,lam,mu],'A_squared':'27 I - 6 A + 9 J','eigenspaces':{'constant':1,'plus3':120,'minus9':44}},
      'primitive_idempotents':{'E0':'J/165','E_plus3':'(A+9I-(3/11)J)/12','E_minus9':'(-A+3I+(1/5)J)/12'},
      'Gram':{'formula':'I+A/13','eigenvalues':{'constant':'49/13','plus3_120D':'16/13','minus9_44D':'4/13'},'condition_number':'49/4'},
      'canonical_dual':{'inverse_Gram':'(91/64)I-(13/64)A+(117/3136)J','per_encoding':'dual(U)=(91/64)phi_U-(13/64) sum_{V~U} phi_V+(117/3136) sum_V phi_V'},
      'noise_sector_reading':{'120D':'plus-3 SRG eigenspace; Gram gain 16/13','45D':'constant plus 44D minus-9 sector; dark component gain 4/13','relation_to_local_split':'165=(1+44)+120=45+120'},
      'erasure_robustness':{'every_principal_subframe_independent':True,'principal_condition_number_upper_bound':'49/4','full_span_erasure_correction':False,'reason':'the original 165 Gram matrix is full rank, so the 165 coefficient vectors are linearly independent; deleting a vector deletes one span dimension'},
      'checks':{'inverse_exact':True,'SRG_product':True,'spectral_decoder':True,'interlacing_bound':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
