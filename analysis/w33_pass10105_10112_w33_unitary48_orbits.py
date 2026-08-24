#!/usr/bin/env python3
"""Pass10105-10112 outside-box: the chamber-selected W33 has a canonical 16|12|12 partition.

Pass10081-10088 produced W(3,3) from the middle Hermitian quotient Q=F4/F2,
which is two-dimensional over F9 and four-dimensional over F3.  Multiplication
by i is a symplectic complex structure R with R^2=-I.  Its centralizer inside
Sp4(3) is U2(3), of order 96; projectively, quotienting by +-I gives order 48.

This pass does not rely only on the order formula.  It exhausts all 3^8
F3-linear matrices commuting with R, represented in block form

    X = [[P, 2Q], [Q, P]],    P,Q in M2(F3),

and keeps exactly the invertible symplectic ones.  There are 96.  It then
computes the induced projective action on all 40 points of PG(3,3).

The orbit sizes are exactly

    16 + 12 + 12.

The 16-point orbit is the union of the four Hermitian-isotropic F9 projective
lines, each contributing four F3 projective points.  The two 12-point orbits
are the two nonzero Hermitian norm classes.  Hence the chamber-selected W33
comes with an intrinsic three-colour point partition, not a bare 40-set.
"""
from __future__ import annotations
import itertools,json
from collections import deque,Counter
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10105_10112_W33_UNITARY48_ORBITS.json'
P=3
J=np.array([[0,1],[2,0]],dtype=np.int64)%P
K=np.block([[J,np.zeros((2,2),dtype=np.int64)],[np.zeros((2,2),dtype=np.int64),J]])%P
R=np.block([[np.zeros((2,2),dtype=np.int64),2*np.eye(2,dtype=np.int64)],
            [np.eye(2,dtype=np.int64),np.zeros((2,2),dtype=np.int64)]])%P


def rankp(M):
    A=np.array(M,dtype=np.int64)%P;m,n=A.shape;r=0
    for c in range(n):
        q=next((i for i in range(r,m) if A[i,c]),None)
        if q is None:continue
        A[[r,q]]=A[[q,r]]
        A[r]=(A[r]*pow(int(A[r,c]),-1,P))%P
        for i in range(m):
            if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%P
        r+=1
        if r==m:break
    return r

def canon(v):
    v=tuple(int(x)%P for x in v)
    for x in v:
        if x:
            u=pow(x,-1,P);return tuple(u*y%P for y in v)
    raise ValueError

def points():return sorted({canon(v) for v in itertools.product(range(P),repeat=4) if any(v)})

def matkey(M):return tuple(int(x) for x in (np.array(M,dtype=np.int64)%P).ravel())

def act_point(M,p):return canon((np.array(M,dtype=np.int64)@np.array(p,dtype=np.int64))%P)

def hermitian_norm(v):
    # v=(a0,a1,b0,b1) represents x=a+i b in F9^2. H=iJ.
    # h(x,x) lies in F3. Expand directly: h = (a+i b) iJ (a-i b)^T.
    a=np.array(v[:2],dtype=np.int64)%P;b=np.array(v[2:],dtype=np.int64)%P
    # real coefficient: a J b^T + b J a^T = 2*a J b^T because J^T=-J? compute exactly.
    # Direct F9 multiplication gives h real = a J b^T - b J a^T = 2*a J b^T mod3.
    return int((2*(a@J@b))%P)

def main():
    I4=np.eye(4,dtype=np.int64)%P
    assert np.array_equal(R@R%P,(-I4)%P)
    assert np.array_equal(R.T@K@R%P,K)

    group=[]
    for vals in itertools.product(range(P),repeat=8):
        Pm=np.array(vals[:4],dtype=np.int64).reshape(2,2)%P
        Qm=np.array(vals[4:],dtype=np.int64).reshape(2,2)%P
        X=np.block([[Pm,2*Qm],[Qm,Pm]])%P
        if rankp(X)<4:continue
        if np.array_equal(X.T@K@X%P,K):group.append(X)
    assert len(group)==96
    # exact centralizer check
    assert all(np.array_equal(X@R%P,R@X%P) for X in group)
    keys={matkey(X) for X in group}
    assert len(keys)==96 and matkey(I4) in keys and matkey((-I4)%P) in keys

    pts=points();assert len(pts)==40
    unseen=set(pts);orbits=[]
    while unseen:
        seed=next(iter(unseen));orb={act_point(X,seed) for X in group}
        # one application of whole group is the full orbit because group is enumerated.
        orbits.append(sorted(orb));unseen-=orb
    sizes=sorted(len(o) for o in orbits)
    assert sizes==[12,12,16]

    # Classify by Hermitian norm after canonical F3 scaling; norm is invariant under +/- scaling.
    norm_counts=[]
    for orb in orbits:
        cnt=Counter(hermitian_norm(p) for p in orb)
        norm_counts.append({'size':len(orb),'norm_counts':{str(k):v for k,v in sorted(cnt.items())}})
    norm_counts=sorted(norm_counts,key=lambda x:(x['size'],str(x['norm_counts'])))
    assert sorted((x['size'],x['norm_counts'].get('0',0)) for x in norm_counts)==[(12,0),(12,0),(16,16)]
    # The two 12s must each be constant nonzero norm, one class 1 and one class 2.
    nz=[x for x in norm_counts if x['size']==12]
    assert sorted([tuple(sorted(x['norm_counts'].items())) for x in nz])==[(('1',12),),(('2',12),)]

    # Four isotropic F9 projective lines, each splits into 4 F3 points: 16 total.
    # Number of isotropic F9 lines for nondegenerate Hermitian dim2 over F9 is q+1=4 (q=3).
    iso_points=sum(1 for p in pts if hermitian_norm(p)==0)
    assert iso_points==16

    out={
      'schema':'w33.pass10105_10112.w33_unitary48_orbits.v1','status':'PASS','passes':'10105-10112','outside_box':True,
      'middle_W33':{'underlying':'F9-Hermitian dimension 2 viewed as F3 symplectic dimension 4','points':40},
      'complex_structure':{'R_squared':'-I','R_symplectic':True},
      'centralizer':{'enumeration_space':'all 3^8 complex-linear matrices [[P,2Q],[Q,P]]','Sp4_3_centralizer_order':96,'isomorphism':'U2(3)','projective_order':48,'projective_kernel':'{+I,-I}'},
      'point_orbits':{'sizes':sizes,'classification':norm_counts,'partition':'16 | 12 | 12'},
      'Hermitian_interpretation':{'isotropic_F9_lines':4,'F3_points_per_F9_line':4,'isotropic_F3_points':16,'nonzero_norm1_points':12,'nonzero_norm2_points':12},
      'theorem':'The chamber-selected W33 has a canonical projective unitary centralizer of order 48. Its 40 points split into three exact orbits 16+12+12: 16 Hermitian-isotropic directions and two 12-point nonzero Hermitian norm classes. Thus the local W33 carries an intrinsic 16|12|12 selector partition.',
      'possible_connection':'The earlier Witting 36-ray Clifford census has classes 4,8,12,12, so its middle 24 rays also split 12+12. The size match is recorded as a target for an explicit intertwiner; no identification is claimed here.',
      'boundary':'Exhaustive finite enumeration of the centralizer and its 40-point action. The 12+12 Witting comparison is only a count-pattern target until an objectwise map is constructed.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','centralizer':96,'projective':48,'orbits':sizes,'iso':iso_points}))
    return 0
if __name__=='__main__':raise SystemExit(main())
