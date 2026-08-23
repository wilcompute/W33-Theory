#!/usr/bin/env python3
"""Pass8569-8576: the 144 mixed Leech Lagrangians have a canonical 9:1 Q+(3,3) quotient.

The four 36-components are indexed by the projective direction d of the first
coordinate pair.  Every projected mixed Lagrangian also contains one of the four
radical points, whose last-coordinate direction is e.  Thus every mixed
Lagrangian has a canonical coarse label (d,e) in PG(1,3)xPG(1,3).

For distinct coarse blocks, |L cap L'| >= 3 iff they share d or e.  Each block has
nine lifts, so the threshold intersection graph is exactly the lexicographic
9-blowup of the 4x4 rook graph Q+(3,3).  The labels (d,e) are literally the
projective rank-one matrices d e^T in M2(F3), tying the full Lagrangian atlas to
the tensor residue embedded into E8 at Pass7949.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
from analysis.w33_pass8101_8108_leech_h27_gl23_lagrangian_controller import lagrangians,proj,qdir,canon
from analysis.w33_pass7949_7956_literal_qplus33_in_e8_qplus73 import T,qdet,qsum
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS8569_8576_LEECH144_QPLUS33_NINEFOLD_QUOTIENT.json'

def c2(v):return canon((v[0],v[1],0,0))[:2]
def c4(v):return canon(tuple(v))
def srg(A):
    k=set(map(int,A.sum(1)));assert len(k)==1;k=k.pop();la=set();mu=set()
    for i,j in itertools.combinations(range(len(A)),2):
        z=int(A[i]@A[j]);(la if A[i,j] else mu).add(z)
    assert len(la)==len(mu)==1
    return [len(A),k,la.pop(),mu.pop()]

def main():
    L=lagrangians();assert len(L)==144
    labels=[];rank1=[]
    for H in L:
        S=proj(H)
        non=[u for u in S if (u[0],u[1])!=(0,0)]
        rad=[u for u in S if (u[0],u[1])==(0,0)]
        assert len(non)==3 and len(rad)==1
        d=qdir(non[0]);assert all(qdir(u)==d for u in non)
        e=c2((rad[0][2],rad[0][3]))
        labels.append((d,e))
        X=np.outer(np.array(d,dtype=int),np.array(e,dtype=int))%3
        x=c4(tuple(map(int,X.reshape(-1))))
        assert qdet(x)==0
        rank1.append(x)
    mult=Counter(labels);assert len(mult)==16 and set(mult.values())=={9}
    assert len(set(rank1))==16

    # Every projective rank-one matrix occurs once at the coarse level.
    all_rank1={c4(x) for x in itertools.product(range(3),repeat=4) if any(x) and qdet(x)==0}
    assert set(rank1)==all_rank1 and len(all_rank1)==16

    # Actual 144-vertex threshold graph: intersection >=3.
    A=np.zeros((144,144),dtype=np.uint8)
    for i,j in itertools.combinations(range(144),2):
        if len(L[i]&L[j])>=3:A[i,j]=A[j,i]=1
    assert set(map(int,A.sum(1)))=={62}

    # The same graph is the exact K9 lexicographic blow-up of the rook graph on labels.
    E=np.zeros_like(A)
    for i,j in itertools.combinations(range(144),2):
        same=labels[i]==labels[j]
        rook=(labels[i][0]==labels[j][0] or labels[i][1]==labels[j][1])
        if same or rook:E[i,j]=E[j,i]=1
    assert np.array_equal(A,E)

    labs=sorted(mult);li={z:i for i,z in enumerate(labs)}
    R=np.zeros((16,16),dtype=np.uint8)
    for i,j in itertools.combinations(range(16),2):
        if labs[i][0]==labs[j][0] or labs[i][1]==labs[j][1]:R[i,j]=R[j,i]=1
    assert srg(R)==[16,6,2,2]
    vals=Counter(round(float(x),8) for x in np.linalg.eigvalsh(A.astype(float)))
    assert vals==Counter({-1.0:128,-10.0:9,26.0:6,62.0:1})

    # Recheck only the coordinate isometry used by Pass7949; no 2240-leaf rebuild needed.
    for x in itertools.product(range(3),repeat=4):
        assert qsum((T@np.array(x,dtype=np.int8))%3)==qdet(x)

    out={
      'schema':'w33.pass8569_8576.leech144_qplus33_ninefold_quotient.v1','status':'PASS','passes':'8569-8576',
      'mixed_Lagrangians':144,'coarse_blocks':16,'lifts_per_block':9,
      'coarse_coordinates':'(d,e) in PG(1,3) x PG(1,3), equivalently projective rank-one matrix d e^T in M2(F3)',
      'coarse_graph':'Q+(3,3) = rook SRG(16,6,2,2)',
      'threshold_graph':{'rule':'distinct L,L prime adjacent iff |L intersect L prime| >= 3','degree':62,'identification':'Q+(3,3)[K9] lexicographic blow-up','spectrum':'62^1 + 26^6 + (-10)^9 + (-1)^128'},
      'E8_dependency':'Pass7949-7956 maps these same 16 projective rank-one M2(F3) points by the explicit isometry T into 16 actual E8 A2 radicals in Q+(7,3).',
      'theorem':'The entire 144-object mixed Leech Lagrangian atlas canonically collapses 9-to-1 onto the same 16-point tensor quadric Q+(3,3) that is already embedded objectwise in the current E8 triality carrier. The collapse is detected purely by Lagrangian intersection: after coarse quotient, sharing one tensor factor is exactly rook collinearity.',
      'claim_boundary':'Exact finite linking/tensor/E8 coordinate chain. The nine lifts are not assigned physical states.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','mixed':144,'quotient':16,'fiber':9,'graph':'Q+(3,3)[K9]'}))
if __name__=='__main__':main()
