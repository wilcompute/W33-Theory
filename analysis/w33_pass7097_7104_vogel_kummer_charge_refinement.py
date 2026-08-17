#!/usr/bin/env python3
"""Passes 7097--7104: refine the Vogel E6 27x78 eigenspaces by the adjacent Z4 charge.

The Pass7049 split-Casimir certificate gives
    27 x 78 = 1728 + 351 + 27.
Pass7081 shows that the Kummer E8 Z4 grading restricts on E6 to the standard
D5+u1 branching.  This script computes the mod-4 charge profiles exactly from
E6 weights and identifies the 351 occurring in 27x78.

Results (residues 0,1,2,3):
    27   : (1,16,10,0)
    78   : (46,16,0,16)
    351  : (45,160,130,16)
    1728 : (256,736,576,160)

The 351 is the fundamental highest-weight module lambda_5 in this script's
0-based E6 numbering (index 4), equivalently conjugate to wedge^2(27); its
profile is computed independently as wedge^2(27*).

This is representation theory only.  It does not identify Vogel's universal
Lie algebra with Kummer geometry; it says the actual E6 Vogel projector channels
are simultaneously resolved by the Kummer-adjacent order-four automorphism.
"""
from __future__ import annotations

from collections import Counter, deque
from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7097_7104_VOGEL_KUMMER_CHARGE_REFINEMENT.json'

A=np.array([
 [2,-1,0,0,0,0],
 [-1,2,-1,0,0,0],
 [0,-1,2,-1,-1,0],
 [0,0,-1,2,0,0],
 [0,0,-1,0,2,-1],
 [0,0,0,0,-1,2],
],dtype=np.int64)


def refl(mu,i):
    return tuple(int(mu[j]-mu[i]*A[j,i]) for j in range(6))


def orbit(start):
    seen={start}; q=deque([start])
    while q:
        mu=q.popleft()
        for i in range(6):
            nu=refl(mu,i)
            if nu not in seen:
                seen.add(nu); q.append(nu)
    return sorted(seen)


def inverse_fraction(A0):
    n=len(A0)
    M=[[Fraction(int(A0[i,j])) for j in range(n)]+[Fraction(int(i==j)) for j in range(n)] for i in range(n)]
    for c in range(n):
        piv=next(i for i in range(c,n) if M[i][c])
        M[c],M[piv]=M[piv],M[c]
        z=M[c][c]; M[c]=[x/z for x in M[c]]
        for i in range(n):
            if i==c: continue
            z=M[i][c]
            if z: M[i]=[M[i][j]-z*M[c][j] for j in range(2*n)]
    return [row[n:] for row in M]


def weyl_dimension(lam, pos_root_coeffs):
    ans=Fraction(1)
    for c in pos_root_coeffs:
        ans*=Fraction(sum(c[i]*(lam[i]+1) for i in range(6)),sum(c))
    assert ans.denominator==1
    return ans.numerator


def conv4(a,b):
    return [sum(a[i]*b[(r-i)%4] for i in range(4)) for r in range(4)]


def main():
    # 27 is minuscule highest weight lambda_1 in this numbering.
    W27=orbit((1,0,0,0,0,0)); assert len(W27)==27
    # Adjoint nonzero weights are the 72 roots, highest weight lambda_4 here.
    R=orbit((0,0,0,1,0,0)); assert len(R)==72

    # U(1) charge for E6 -> D5+u1: vanish on simple roots 1..5 and
    # normalize the 27 highest weight to +4.
    q=np.array([4,5,6,3,4,2],dtype=np.int64)
    for i in range(1,6):
        assert int(q @ A[:,i])==0
    assert int(q[0])==4

    charges27=[int(q@np.array(w,dtype=np.int64)) for w in W27]
    exact27=Counter(charges27)
    assert exact27==Counter({1:16,-2:10,4:1})
    p27=[sum(n for c,n in exact27.items() if c%4==r) for r in range(4)]
    assert p27==[1,16,10,0]

    charges78=[int(q@np.array(w,dtype=np.int64)) for w in R]+[0]*6
    exact78=Counter(charges78)
    assert exact78==Counter({0:46,-3:16,3:16})
    p78=[sum(n for c,n in exact78.items() if c%4==r) for r in range(4)]
    assert p78==[46,16,0,16]

    # Identify the relevant 351 in 27 x 78.  Build the E6 positive roots in
    # simple-root coefficients so the candidate fundamental dimensions can be
    # checked by the Weyl dimension formula.
    Ainv=inverse_fraction(A)
    pos=[]
    for r in R:
        c=[sum(Ainv[i][j]*r[j] for j in range(6)) for i in range(6)]
        assert all(x.denominator==1 for x in c)
        ci=[int(x) for x in c]
        if all(x>=0 for x in ci): pos.append(ci)
    assert len(pos)==36
    fundamental_dims=[]
    for i in range(6):
        lam=[0]*6; lam[i]=1
        fundamental_dims.append(weyl_dimension(lam,pos))
    assert fundamental_dims==[27,351,2925,78,351,27]

    # Dominant tensor weights show that the 351 summand selected by 27x78 has
    # highest weight index 4 (the conjugate of the wedge^2(27) fundamental).
    adj_weights=Counter({r:1 for r in R}); adj_weights[(0,0,0,0,0,0)]+=6
    tensor_weights=Counter()
    for w in W27:
        for a,m in adj_weights.items():
            tensor_weights[tuple(w[i]+a[i] for i in range(6))]+=m
    dominant={w:m for w,m in tensor_weights.items() if all(x>=0 for x in w)}
    assert (1,0,0,1,0,0) in dominant
    assert (0,0,0,0,1,0) in dominant
    assert weyl_dimension((1,0,0,1,0,0),pos)==1728
    assert weyl_dimension((0,0,0,0,1,0),pos)==351

    # The index-4 351 is conjugate to wedge^2(27).  Therefore its weight
    # multiset is obtained exactly from pairwise sums of weights of 27*=-27.
    wedge_conj=Counter()
    for i,j in combinations(range(27),2):
        ch=(-charges27[i]-charges27[j])%4
        wedge_conj[ch]+=1
    p351=[wedge_conj[r] for r in range(4)]
    assert p351==[45,160,130,16] and sum(p351)==351

    total=conv4(p27,p78)
    assert total==[302,912,716,176] and sum(total)==27*78
    p1728=[total[r]-p351[r]-p27[r] for r in range(4)]
    assert p1728==[256,736,576,160] and sum(p1728)==1728

    # Lift to the CE2 triplet: A2 triplet is neutral under this Z4 restriction,
    # so every profile simply triples on (27 x 78) x 3.
    lifted={
      'V1728_x3':[3*x for x in p1728],
      'V351_x3':[3*x for x in p351],
      'V27_x3':[3*x for x in p27],
    }
    assert [sum(x) for x in lifted.values()]==[5184,1053,81]

    report={
      'passes':list(range(7097,7105)),
      'e6_to_d5_u1':{
        'charge_vector_in_fundamental_weight_coordinates':q.tolist(),
        '27_exact_charges':{str(k):v for k,v in sorted(exact27.items())},
        '78_exact_charges':{str(k):v for k,v in sorted(exact78.items())}
      },
      'z4_profiles_residues_0_1_2_3':{
        '27':p27,'78':p78,'27_tensor_78_total':total,
        '351_vogel_channel':p351,'1728_vogel_channel':p1728
      },
      'vogel_decomposition_check':'27x78=1728+351+27, profile-wise in every Z4 residue',
      'ce2_triplet_lift':lifted,
      'status':'VOGEL_PROJECTOR_CHANNELS_EXACTLY_REFINED_BY_KUMMER_ADJACENT_Z4',
      'boundary':'This is an E6 branching/projector compatibility theorem. It does not identify Vogel universal-Lie-algebra diagrams with Kummer geometry or with the E8 Z12 grading as a physical phase group.'
    }
    OUT.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))
    return report

if __name__=='__main__': main()
