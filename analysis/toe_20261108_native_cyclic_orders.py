"""Exhaustive symplectic-basis construction of Sp(4,3) and projective orders.

Known finite-group data are controls, not new group theory or physical sectors.
Independent enumeration avoids trusting BT542's unrelated interpretation of
the81-element Sylow3 as an extraspecial group (not used here).
"""
import itertools
import json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]


def enumerate_symplectic():
    v=np.array(list(itertools.product(range(3),repeat=4)),dtype=np.int64)
    J=np.array([[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]],dtype=np.int64)
    rows=[]
    for a in v[1:]:
        for b in v[(v@J.T@a)%3==1]:
            # a^T J b=1. The vector filter above evaluates a^T J b.
            orth=v[((v@J.T@a)%3==0)&((v@J.T@b)%3==0)]
            for c in orth[np.any(orth!=0,axis=1)]:
                ds=orth[(orth@J.T@c)%3==1]
                for d in ds:rows.append(np.stack([a,c,b,d],axis=1))
    G=np.array(rows,dtype=np.int64)
    assert len(G)==51840 and len({x.tobytes()for x in G})==51840
    assert np.all((np.swapaxes(G,1,2)@J@G-J)%3==0)
    return G,J


def orders(G,projective=False):
    I=np.eye(4,dtype=np.int64);power=np.broadcast_to(I,G.shape).copy();result=np.zeros(len(G),dtype=np.int64)
    for k in range(1,73):
        power=(power@G)%3
        hit=np.all(power==I,axis=(1,2))
        if projective:hit|=np.all(power==(2*I)%3,axis=(1,2))
        result[(result==0)&hit]=k
        if np.all(result):break
    assert np.all(result)
    return {str(k):int(np.sum(result==k)) for k in sorted(set(result.tolist()))}


def three_qutrit_order24(G,J):
    """Standard symplectic direct sum: lcm(8,3)=24, not new group theory."""
    I4=np.eye(4,dtype=np.int64)
    for g in G:
        if np.array_equal(np.linalg.matrix_power(g,4)%3,2*I4):
            break
    else:raise AssertionError('No order-eight block')
    T=np.array([[1,1],[0,1]],dtype=np.int64)
    M=np.zeros((6,6),dtype=np.int64);M[:4,:4]=g;M[4:,4:]=T
    K=np.zeros((6,6),dtype=np.int64);K[:4,:4]=J;K[4:,4:]=[[0,1],[-1,0]]
    assert np.all((M.T@K@M-K)%3==0)
    power=np.eye(6,dtype=np.int64);I6=power.copy();hit=[];projective=[]
    for n in range(1,25):
        power=power@M%3
        if np.array_equal(power,I6):hit.append(n)
        if np.array_equal(power,I6)or np.array_equal(power,2*I6):projective.append(n)
    assert hit==[24] and projective==[24]
    return dict(matrix=M.tolist(),symplectic_form=K.tolist(),order=24,projective_order=24,
                construction='Order8 Sp4 block plus independent order3 transvection Sp2 block; direct-sum symplectic space dimension6. The8block fourth power is -I4, not a scalar on the full6space, so projectivizing retains24.',
                scope='Explicit Z24 subgroup in Sp6(3) and PSp6(3), corresponding to three-qutrit symplectic labels. Does not identify a24-partner regular fermion representation or a protected physical action. This deliberately enlarges the original W33 label space.')


def build():
    G,J=enumerate_symplectic();D=np.diag([1,1,2,2]);extension=(D@G)%3
    assert np.all((np.swapaxes(extension,1,2)@J@extension-2*J)%3==0)
    sp=orders(G);psp={k:v//2 for k,v in orders(G,True).items()}
    full=orders(np.concatenate([G,extension]),True);pgsp={k:v//2 for k,v in full.items()}
    result=dict(status='EXHAUSTIVE_NATIVE_MATRIX_GROUP_ORDER_CONTROL',Sp43=sp,PSp43=psp,PGSp43=pgsp,
                enlarged_three_qutrit_control=three_qutrit_order24(G,J),
                sizes=dict(Sp43=sum(sp.values()),PSp43=sum(psp.values()),PGSp43=sum(pgsp.values())),
                proof='80choicesforfirstnonzeroa,27forbwithomega(a,b)=1,8fornonzerocintheorthogonalcomplement,3fordwithomega(c,d)=1. Unique matrices checked. Similitude coset D=diag(1,1,2,2). Projective orders hit+Ior-I, then central pairs counted once.',
                ownership='BT542 already records Sp43 element orders including18. Its other Sylow/physical identifications are not used or validated. Groups Sp43 and PGSp43 have equal order but are distinguished.',
                scope='Only protecting cyclic symmetries required to embed as an element of these particular groups are screened. Does not rule out larger Clifford extensions, additional global symmetries, larger qudit systems or added sector replication.')
    (ROOT/'data/toe_20261108_native_cyclic_orders.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('GROUPS',result['sizes'],'orders',list(sp),list(pgsp),flush=True)
    return result


if __name__=='__main__':build()
