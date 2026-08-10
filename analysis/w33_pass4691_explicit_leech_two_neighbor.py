#!/usr/bin/env python3
"""Pass 4691 -- explicit A1^24 Niemeier -> Leech 2-neighbor from the corrected Golay/sextet coordinates.

Start with the even unimodular Golay Construction-A lattice

  N = (1/sqrt(2)){x in Z^24 : x mod 2 in G24}.

Coordinate 0 belongs to the first tetrad of the corrected Pass4633 sextet.  Put

  a=(3,1,...,1),  v=a/sqrt(2),  v^2=16,
  M={x in N : (x,v)=0 mod 2},
  L=M + Z(v/2).

M has index two in N and v/2 has even norm four, so L is an even unimodular
2-neighbor.  Every norm-two root of N is a coordinate root +/-sqrt(2)e_i and
has odd pairing 3 or 1 with v, hence is removed from M.  Every vector in the
new coset has an odd integer numerator in all 24 coordinates over denominator
2sqrt(2), so its squared norm is at least 24/8=3; evenness raises this to at
least four.  Therefore L is rootless.  An explicit 24-vector numerator basis Y
for L/(1/(2sqrt(2))) is frozen below.  det(Y)=2^36, so det Gram(L)=1; the Gram
matrix is integral even and contains a norm-four basis vector.  Thus L has
minimum norm four and is the Leech lattice.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import w33_pass4592_paired_axes_simplex_hexacode_golay as p4592
import w33_pass4633_m24_sextet_section_stabilizer as p4633

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4691_EXPLICIT_LEECH_TWO_NEIGHBOR.json'
A=np.ones(24,dtype=np.int64);A[0]=3
# Integer numerator basis.  Actual lattice basis is Y/(2*sqrt(2)).
Y=np.array([
[8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[4,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[4,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[4,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[4,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[4,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[4,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[4,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[4,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0],
[4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0],
[6,0,2,0,0,2,0,0,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0],
[6,2,2,2,0,2,2,0,2,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0],
[0,2,2,2,2,0,2,2,0,2,0,0,0,0,2,0,0,0,0,0,0,0,0,0],
[0,0,2,2,2,2,0,2,2,0,2,0,0,0,0,2,0,0,0,0,0,0,0,0],
[0,0,0,2,2,2,2,0,2,2,0,2,0,0,0,0,2,0,0,0,0,0,0,0],
[6,0,2,0,2,0,2,2,2,0,0,2,0,0,0,0,0,2,0,0,0,0,0,0],
[6,2,2,2,0,0,0,2,0,0,2,2,0,0,0,0,0,0,2,0,0,0,0,0],
[6,2,0,2,2,2,0,0,0,2,2,0,0,0,0,0,0,0,0,2,0,0,0,0],
[0,2,2,0,2,2,2,0,0,0,2,2,0,0,0,0,0,0,0,0,2,0,0,0],
[6,0,0,2,0,0,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,2,0,0],
[0,2,0,0,2,0,0,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,2,0],
[3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
],dtype=np.int64)

def det_bareiss(M):
    Z=[list(map(int,row)) for row in M];n=len(Z);sgn=1;prev=1
    for k in range(n-1):
        if Z[k][k]==0:
            r=next((r for r in range(k+1,n) if Z[r][k]),None)
            if r is None:return 0
            Z[k],Z[r]=Z[r],Z[k];sgn=-sgn
        piv=Z[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):Z[i][j]=(Z[i][j]*piv-Z[i][k]*Z[k][j])//prev
        prev=piv
        for i in range(k+1,n):Z[i][k]=0
        for j in range(k+1,n):Z[k][j]=0
    return sgn*Z[-1][-1]
def parity_word(x):return sum((int(x[i])&1)<<i for i in range(24))

def main()->int:
    G=set(p4592.golay24());weights={w.bit_count() for w in G};assert 4 not in weights and 8 in weights and 24 in weights
    allone=(1<<24)-1;assert allone in G
    def in_M(x):return parity_word(x) in G and int(np.dot(x,A))%4==0
    # Every basis row is explicitly in M or v/2+M in common numerator coordinates.
    for y in Y:
        if np.all((y&1)==0):x=y//2
        else:
            assert np.all((y&1)==1);x=(y-A)//2
        assert in_M(x)
    detY=abs(det_bareiss(Y));assert detY==2**36
    Q=Y@Y.T;assert np.all(Q%8==0);Gram=Q//8
    assert np.all(Gram==Gram.T) and np.all(np.diag(Gram)%2==0)
    # det(Gram)=det(Y)^2/8^24 = 1 exactly.
    gram_det_num=detY*detY;gram_det_den=8**24;assert gram_det_num==gram_det_den
    assert min(map(int,np.diag(Gram)))==4
    # Root proof in N: x.x=4 gives either +/-2e_i or four +/-1 entries; the latter
    # would require a weight-4 Golay word, which does not exist.  Coordinate roots
    # have pairing A_i in {1,3}, hence are all outside M.
    assert set(map(int,A))=={1,3} and all(int(x)&1 for x in A)
    # New coset numerators are odd in all 24 coordinates, hence y.y >= 24 and norm >=3;
    # evenness of the neighbor excludes norm 3, so minimum is >=4.  Gram exhibits 4.
    # The 24 choices of distinguished coordinate lie in one orbit of the sextet stabilizer.
    H=p4633.build()['H'];orbit0={g[0] for g in H};assert len(orbit0)==24
    out={'pass':4691,
      'neighbor':{'base':'Golay Construction-A A1^24 Niemeier','distinguished_coordinate':0,'distinguished_coordinate_sextet_tetrad':[0,2,7,21],'v_integer_numerator':[3]+[1]*23,'v_norm':16,'definition':'M={x in N:(x,v) even}; L=M+Z(v/2)','neighbor_index_each_way':2},
      'explicit_basis':{'coordinate_scale':'1/(2*sqrt(2))','integer_numerator_basis':Y.tolist(),'numerator_determinant':detY,'gram_determinant':1,'integral_even_gram':True,'exhibited_basis_minimum_norm':4},
      'rootlessness':{'old_N_roots':'exactly 48 coordinate roots +/-sqrt(2)e_i','all_old_roots_have_odd_v_pairing':True,'new_coset_all_24_numerators_odd':True,'new_coset_raw_norm_lower_bound':3,'even_lattice_strengthens_lower_bound_to':4,'minimum_norm':4},
      'sextet_weld':{'24_distinguished_coordinate_neighbors_in_one_sextet_stabilizer_orbit':True},
      'theorem':'The explicit two-neighbor of the Golay Construction-A A1^24 Niemeier lattice defined by v=(3,1^23)/sqrt(2) is even, unimodular, rootless, and has minimum norm four.  Its frozen basis has Gram determinant one.  Hence it is the Leech lattice; the 24 coordinate choices form one orbit of the corrected sextet stabilizer.',
      'boundary':'Exact lattice construction.  The Leech identification uses the standard uniqueness of the rootless even unimodular lattice in dimension 24; no physical interpretation is inferred.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='explicit_basis'},indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
