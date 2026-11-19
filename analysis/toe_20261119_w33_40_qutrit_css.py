#!/usr/bin/env python3
"""A 40-qutrit CSS code from the W(3,3) adjacency algebra over F3.

CERTIFIED:
  Hx = A+I, Hz = A+I-J (mod 3)
  rank(Hx)=11, rank(Hz)=10, Hx Hz^T=0
  [[n,k,d]]_3 = [[40,19,4]]_3; d_X=4, d_Z=6.
This code is distinct from the repo's 240-edge CSS code.
Prior art: the common [40,11,13] and [40,10,18] classical row spaces
and N^2=J were established by Pass4948 and Pass7733-7740.
"""
import itertools
import json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
P=3
NQ=40


def points():
    """All projective one-dimensional subspaces of F3^4, canonical form."""
    return sorted({min(v,tuple((-x)%3 for x in v))
                   for v in itertools.product(range(3),repeat=4)
                   if any(v)})


def symplectic(x,y):
    return (x[0]*y[1]-x[1]*y[0]+x[2]*y[3]-x[3]*y[2])%3


def checks():
    PTS=points()
    assert len(PTS)==NQ
    A=np.zeros((NQ,NQ),dtype=np.int64)
    for i in range(NQ):
        for j in range(i+1,NQ):
            if symplectic(PTS[i],PTS[j])==0:
                A[i,j]=A[j,i]=1
    I=np.eye(NQ,dtype=np.int64)
    J=np.ones((NQ,NQ),dtype=np.int64)
    assert np.array_equal(A@A,8*I-2*A+4*J)
    assert np.all(A.sum(axis=1)==12)
    # Exact integral lift of the modular nilpotency:
    assert np.array_equal((A+I)@(A+I),9*I+4*J)
    HX=(A+I)%3
    HZ=(A+I-J)%3
    assert np.all((HX@HX-J)%3==0)
    assert np.all((HX@HZ.T)%3==0)
    return PTS,A,HX,HZ


def rref_mod3(matrix):
    a=np.array(matrix,dtype=np.int64,copy=True)%3
    nrow,ncol=a.shape
    rank=0
    for j in range(ncol):
        pivot=next((i for i in range(rank,nrow) if a[i,j]),None)
        if pivot is None:continue
        if pivot!=rank:a[[rank,pivot]]=a[[pivot,rank]]
        a[rank]=(a[rank]*(1 if a[rank,j]==1 else 2))%3
        for i in range(nrow):
            if i!=rank and a[i,j]:
                a[i]=(a[i]-int(a[i,j])*a[rank])%3
        rank+=1
        if rank==nrow:break
    return a[:rank]


def rank_mod3(matrix):
    return rref_mod3(matrix).shape[0]


def normalized_syndrome(syndrome):
    s=bytes(np.asarray(syndrome,dtype=np.uint8)%3)
    t=bytes((-np.asarray(syndrome,dtype=np.int64)%3).astype(np.uint8))
    return min(s,t)


def projective_errors(check,max_weight):
    """Enumerate every projective-weight <= max_weight ternary Pauli error."""
    for weight in range(1,max_weight+1):
        for support in itertools.combinations(range(check.shape[1]),weight):
            for tail in itertools.product((1,2),repeat=weight-1):
                coefficients=(1,)+tail
                syndrome=np.zeros(check.shape[0],dtype=np.int64)
                for position,coefficient in zip(support,coefficients):
                    syndrome+=coefficient*check[:,position]
                syndrome%=3
                yield weight,support,coefficients,syndrome


def count_undetectable_through_three(H):
    counts={1:0,2:0,3:0}
    for weight,support,coefficients,syndrome in projective_errors(H,3):
        if not np.any(syndrome):counts[weight]+=1
    return counts


def verify_no_Z_weight_four_or_five(HZcheck):
    """Meet-in-middle proof for no HZcheck-kernel vectors of weight 4/5.

    If a weight-4 or weight-5 codeword exists, partition its support
    into sets of sizes <=2 and <=3. Their syndromes match up to sign.
    Comparing all normalized syndromes is exhaustive, up to scalar.
    """
    seen={}
    weight_two_count=0
    for weight,support,coefs,syndrome in projective_errors(HZcheck,2):
        if not np.any(syndrome):
            raise AssertionError("undetectable support <=2")
        key=normalized_syndrome(syndrome)
        if key in seen:
            prev_w,prev_s,prev_c=seen[key]
            if (weight,support,coefs)!=(prev_w,prev_s,prev_c):
                raise AssertionError("syndrome collision gives <=4 Z-error")
        seen[key]=(weight,support,coefs)
        if weight==2:weight_two_count+=1
    checks3=0
    for weight,support,coefs,syndrome in projective_errors(HZcheck,3):
        if weight!=3:continue
        checks3+=1
        if not np.any(syndrome):raise AssertionError("undetectable Z weight3")
        if normalized_syndrome(syndrome) in seen:
            raise AssertionError("Z syndrome collision gives <=5 Z-error")
    return {"weight_two_projective_patterns":weight_two_count,
            "weight_three_projective_patterns":checks3,
            "weight_four_five_Z_kernel_vectors_exist":False}


def certify():
    PTS,A,HX,HZ=checks()
    rX=rank_mod3(HX)
    rZ=rank_mod3(HZ)
    assert (rX,rZ)==(11,10)
    small_X=count_undetectable_through_three(HZ)
    small_Z=count_undetectable_through_three(HX)
    assert small_X==small_Z=={1:0,2:0,3:0}
    zproof=verify_no_Z_weight_four_or_five(HX)
    # Four collinear W33 points support an X-type logical operator.
    x=np.zeros(40,dtype=np.int64)
    x[:4]=1
    assert all(p[:2]==(0,0) for p in PTS[:4])
    assert np.all((HZ@x)%3==0)
    assert rank_mod3(np.column_stack((HX,x)))==rX+1
    # The dual [40,29,6] code supplies a six-support Z word.
    z=np.zeros(40,dtype=np.int64)
    z[[0,1,2]]=1
    z[[4,9,11]]=2
    assert np.all((HX@z)%3==0)
    assert rank_mod3(np.column_stack((HZ,z)))==rZ+1
    assert int(np.count_nonzero(z))==6
    return {
      "status":"PASS",
      "graph":"W(3,3), strongly regular (40,12,2,4)",
      "SRG_adjacency_spectrum":"12^1, 2^24, (-4)^15",
      "integral_identity":"(A+I)^2=9I+4J",
      "characteristic_three_identity":"(A+I)^2=J mod3",
      "check_definitions":"H_X=(A+I) mod3; H_Z=(A+I-J) mod3",
      "rank_HX":rX,"rank_HZ":rZ,
      "commutation":"H_X*H_Z.T=0 mod3",
      "physical_qutrits":40,"logical_qutrits":40-rX-rZ,
      "code_parameters":"[[40,19,4]]_3",
      "X_distance":4,"Z_distance":6,
      "zero_syndrome_counts_X_through_weight3":small_X,
      "zero_syndrome_counts_Z_through_weight3":small_Z,
      "Z_distance_lower_bound_exhaustion":zproof,
      "X_logical_weight4_positions":[0,1,2,3],
      "Z_logical_weight6_positions_and_coeffs":{
          "positions":[0,1,2,4,9,11],"coefficients":[1,1,1,2,2,2]},
      "projective_points_first_four":[list(x) for x in PTS[:4]],
      "prior_art":["Pass4948: F3 modular radical N^2=J",
                   "Pass7733-7740: common [40,11,13], [40,10,18] row spaces across 234 polarities",
                   "repo's 240-edge [[240,81,...]] CSS remains a separate construction"],
      "novel_claim_scope":"derived asymmetric qutrit CSS pairing and exact distance witnesses, not uniqueness/literature priority",
      "not_claimed":["decoder threshold","fault-tolerant gate implementation",
                     "spacetime dynamics","experimental physical memory"]
    }


if __name__=="__main__":
    result=certify()
    target=ROOT/"data"/"toe_20261119_w33_40_qutrit_css.json"
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps({"status":result["status"],"code":result["code_parameters"],
                      "dX":result["X_distance"],"dZ":result["Z_distance"],
                      "rank_X":result["rank_HX"],"rank_Z":result["rank_HZ"],
                      "output":str(target)}))
