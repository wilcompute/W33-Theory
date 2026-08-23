#!/usr/bin/env python3
"""Pass7949-7956: literal Q+(3,3) tensor residue inside the current E8 Q+(7,3) carrier.

Pass7909 produced the Leech 3-adic tensor layer M2(F3) with q=det and its
16-point Q+(3,3).  Pass7465 identified the 1120 current E8 A2 radicals with every
singular projective point of E8/3E8 = Q+(7,3).  This pass gives an explicit linear
isometry between those coordinate models and then audits how the embedded
16-point subquadric meets all 2240 Eisenstein W33 leaves.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np,sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from analysis import w33_pass7501_7564_common as E
OUT=ROOT/'data/PART_W33_PASS7949_7956_LITERAL_QPLUS33_IN_E8_QPLUS73.json'

T=np.array([[0,1,2,0],[1,0,0,1],[1,1,1,2],[1,2,2,2]],dtype=np.int8)%3

def canon(v):
    v=tuple(int(x)%3 for x in v)
    for x in v:
        if x:return tuple(((1 if x==1 else 2)*y)%3 for y in v)
    raise ValueError

def canon2(v):
    v=tuple(int(x)%3 for x in v)
    for x in v:
        if x:return tuple(((1 if x==1 else 2)*y)%3 for y in v)
    raise ValueError

def qdet(x):return (x[0]*x[3]-x[1]*x[2])%3
def qsum(y):return sum(int(z)*int(z) for z in y)%3

def srg(A):
    k=set(map(int,A.sum(1)));assert len(k)==1;k=k.pop();la=set();mu=set()
    for i,j in itertools.combinations(range(len(A)),2):
        c=int(A[i]@A[j]);(la if A[i,j] else mu).add(c)
    assert len(la)==len(mu)==1
    return [len(A),k,la.pop(),mu.pop()]

def main():
    # T is an exact isometry q_det -> q_sum on F3^4.
    for x in itertools.product(range(3),repeat=4):
        assert qsum((T@np.array(x,dtype=np.int8))%3)==qdet(x)
    assert round(np.linalg.det(T))%3!=0

    R,A2,ag,J,base,leaves,lgens,parity=E.build()
    radicals=[]
    for S in A2:
        vals=set()
        for i,j in itertools.combinations(sorted(S),2):
            if E.dot(R[i],R[j])==-4:
                vals.add(E.canon3(tuple(R[i][k]-R[j][k] for k in range(8))))
        assert len(vals)==1;radicals.append(next(iter(vals)))
    ri={v:i for i,v in enumerate(radicals)};assert len(ri)==1120

    rank1=sorted({canon(x) for x in itertools.product(range(3),repeat=4)
                  if any(x) and qdet(x)==0})
    assert len(rank1)==16
    mapped=[];a2ids=[];labels=[]
    for x in rank1:
        y4=tuple(int(z) for z in (T@np.array(x,dtype=np.int8))%3)
        y=E.canon3(y4+(0,0,0,0));assert qsum(y)==0 and y in ri
        mapped.append(y);a2ids.append(ri[y])
        M=np.array(x,dtype=np.int8).reshape(2,2)%3
        col=next(tuple(int(z) for z in M[:,j]) for j in range(2) if np.any(M[:,j]))
        row=next(tuple(int(z) for z in M[i,:]) for i in range(2) if np.any(M[i,:]))
        labels.append((canon2(col),canon2(row)))
    assert len(set(mapped))==len(set(a2ids))==len(set(labels))==16

    A=np.zeros((16,16),dtype=np.int8)
    for i,j in itertools.combinations(range(16),2):
        if sum(mapped[i][k]*mapped[j][k] for k in range(8))%3==0:A[i,j]=A[j,i]=1
        assert bool(A[i,j])==(labels[i][0]==labels[j][0] or labels[i][1]==labels[j][1])
    assert srg(A)==[16,6,2,2]

    dirs=sorted({x for z in labels for x in z});assert len(dirs)==4
    idlab={a2ids[i]:labels[i] for i in range(16)}
    lines={}
    for side in (0,1):
        for d in dirs:
            S=frozenset(a for a,l in idlab.items() if l[side]==d);assert len(S)==4
            lines[(side,d)]=S
    assert len(set(lines.values()))==8

    U=set(a2ids)
    census=Counter(len(set(L)&U) for L in leaves)
    assert census==Counter({0:1152,1:1024,4:64})
    byfam={p:Counter(len(set(leaves[i])&U) for i,x in enumerate(parity) if x==p) for p in (0,1)}
    assert byfam[0]==byfam[1]==Counter({0:576,1:512,4:32})
    line_profile={}
    for key,S in lines.items():
        hit=[i for i,L in enumerate(leaves) if set(L)&U==set(S)]
        assert len(hit)==8 and Counter(parity[i] for i in hit)==Counter({0:4,1:4})
        line_profile[str(key)]={'leaves':8,'family_split':[4,4]}

    # Each embedded point lies on 80 ambient maximal generators: 16 via the two
    # embedded lines through it, and 64 with point-only intersection.
    for a in U:
        hit=[i for i,L in enumerate(leaves) if a in L]
        assert len(hit)==80
        assert Counter(len(set(leaves[i])&U) for i in hit)==Counter({1:64,4:16})

    out={
      'schema':'w33.pass7949_7956.literal_qplus33_in_e8_qplus73.v1','status':'PASS','passes':'7949-7956',
      'linear_isometry_matrix':T.astype(int).tolist(),
      'source':'M2(F3), q(X)=det(X)','target':'first four coordinates of E8/3E8, q=sum x_i^2',
      'embedded_singular_points':16,'current_E8_A2_radicals':a2ids,
      'induced_collinearity':'SRG(16,6,2,2) = 4x4 rook graph','rank1_factorization':'PG(1,3) x PG(1,3)',
      'embedded_singular_lines':{'total':8,'reguli':[4,4]},
      'W33_leaf_intersections':{'all_2240':{str(k):v for k,v in sorted(census.items())},'each_generator_family':{'0':576,'1':512,'4':32},'leaves_meeting_in_a_line':64,'leaves_per_embedded_line':8,'per_line_generator_family_split':[4,4]},
      'point_profile':'each of the 16 points lies on 80 W33 leaves: 16 line-intersection leaves and 64 point-only leaves',
      'theorem':'The Leech M2(F3) plus-orthogonal tensor residue has an explicit coordinate embedding as a nondegenerate Q+(3,3) subquadric of the current E8/3E8 Q+(7,3) triality carrier, objectwise through 16 actual A2 radicals. Its eight reguli lines have an exact balanced lift into the 2240 Eisenstein W33 leaves.',
      'claim_boundary':'This is an explicit finite polar-space embedding. It does not identify the Leech and E8 acting groups or imply a physical embedding.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','Qplus33':16,'lines':8,'leaf_census':dict(census)}))
if __name__=='__main__':main()
