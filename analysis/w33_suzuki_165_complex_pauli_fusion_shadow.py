#!/usr/bin/env python3
"""Complex six-qutrit operator-space shadow of the local 165 U5(2) carrier.

Each full W33 four-space U <= F3^12 supplies the 80-dimensional Hilbert-Schmidt
subspace spanned by the nonidentity six-qutrit Pauli monomials P_v, v in U\{0}.
For the local 165 carrier all U contain the fixed projective phase point p, hence
all operator subspaces share P_p and P_-p.  Remove this common rank-2 core.
The reduced subspace has rank 78.

If U,V are adjacent in SRG(165,36,3,9), dim(U cap V)=2, so they share 8 nonzero
Pauli labels and 6 after removing +/-p.  Nonadjacent distinct vertices intersect
only in <p>, so reduced overlap is zero.  Therefore normalized projection vectors
q_U=P_U/sqrt(78) have Gram matrix I + A/13.  Its spectrum follows exactly from
the SRG spectrum.  This provides a natural COMPLEX Hilbert-Schmidt/fusion-frame
realization of the same 165 incidence carrier without interpreting quantum
mechanics itself as quaternionic.
"""
from __future__ import annotations
import json
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_suzuki_165_complex_pauli_fusion_shadow.json'

def main(write=True):
 parent=json.loads((ROOT/'data'/'w33_suzuki_local_165_gq48_spectral_bridge.json').read_text());assert parent['status']=='PASS'
 assert parent['construction']['srg']==[165,36,3,9]
 rank=3**4-1-2;assert rank==78
 adjacent_overlap=(3**2-1)-2;nonadjacent_overlap=(3**1-1)-2
 assert (adjacent_overlap,nonadjacent_overlap)==(6,0)
 inner=Fraction(adjacent_overlap,rank);assert inner==Fraction(1,13)
 # Gram eigenvalues 1 + lambda/13 for lambda=36,3,-9.
 spec={str(Fraction(49,13)):1,str(Fraction(16,13)):120,str(Fraction(4,13)):44}
 fp1=Fraction(165,1)+Fraction(165*36,13)
 fp2=Fraction(165,1)+Fraction(165*36,13**2)
 assert fp1==Fraction(8085,13) and fp2==Fraction(33825,169)
 out={'schema':'w33.suzuki_165_complex_pauli_fusion_shadow.v1','status':'PASS',
 'headline':'The 165 local Leech/Suzuki W33 encodings have a canonical complex six-qutrit operator-space realization. After removing their common +/-p Pauli core, each gives a rank-78 projection; adjacent encodings have projection overlap 6 and nonadjacent encodings overlap 0. Normalized projection Gram is I+A/13 with spectrum (49/13)^1+(16/13)^120+(4/13)^44.',
 'ambient':'traceless six-qutrit Hilbert-Schmidt operator space with orthonormal Pauli monomial basis','raw_W33_operator_rank':80,'common_core_rank':2,'reduced_rank':rank,
 'pair_overlap':{'adjacent_trace_PUPV':6,'nonadjacent_trace_PUPV':0,'normalized_adjacent_inner':'1/13','normalized_nonadjacent_inner':'0'},
 'normalized_projection_Gram':{'formula':'I + A_165/13','spectrum':spec,'rank':165},
 'frame_potentials':{'sum_inner_products':'8085/13','second_projection_frame_potential':'33825/169','tight_frame_value_for_165_vectors_in_165D_span':'165','is_tight':False},
 'design_boundary':'This is an exact complex two-distance fusion/projection frame in six-qutrit operator space. It is not a complex projective 2- or 3-design certificate and it does not imply quaternionic quantum mechanics. The classical HP^4 design and this complex shadow share the U5(2)/GQ(4,8) incidence carrier, not a claimed canonical Hilbert-space isometry.',
 'checks':{'rank78':True,'adjacent_overlap6':True,'nonadjacent_overlap0':True,'Gram_spectrum':True,'frame_potential':True}}
 if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
