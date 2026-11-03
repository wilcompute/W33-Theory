"""Actual Spin6 intertwiner and an equal-order Weyl-group false lead.

Uses the existing gamma axes and symplectic form, not a dimension match.
SU4=Spin6 and signed permutation groups are prior mathematics.
The determinant-one signed group B6+ is not W(D6), despite equal order23040.
"""
import collections
import itertools
import json
import math
import pathlib
import sys

import sympy as s

ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261102_toroidal_knight_clifford_bridge import matrices


def multiply(a,b):
    p,x=a;q,y=b
    return tuple(p[q[i]] for i in range(6)),y^sum(((x>>q[i])&1)<<i for i in range(6))


def parity(p):return sum(p[i]>p[j] for i in range(6) for j in range(i+1,6))%2


def element_order(p,b):
    seen=set();order=1
    for j in range(6):
        if j in seen:continue
        k=j;n=0;sign=0
        while k not in seen:seen.add(k);n+=1;sign^=b>>k&1;k=p[k]
        order=math.lcm(order,n*(2 if sign else 1))
    return order


def build():
    gamma,blades,old,omega=matrices();U=(s.eye(4)+s.I*blades[15])/s.sqrt(2)
    forms=[s.I*omega]+[g*omega for g in gamma]
    assert all(B.T==-B for B in forms)
    assert all(s.trace(A.conjugate().T*B)==(4 if i==j else 0) for i,A in enumerate(forms) for j,B in enumerate(forms))
    generators=[];actions=[]
    for V in old+[U]:
        A=s.Matrix(6,6,lambda i,j:s.simplify(s.trace(forms[i].conjugate().T*V*forms[j]*V.T)/4))
        assert A.T*A==s.eye(6) and A.det()==1
        p=[];bits=0
        for j in range(6):
            nz=[i for i in range(6) if A[i,j]!=0];assert len(nz)==1
            i=nz[0];assert A[i,j] in [1,-1];p.append(i);bits|=int(A[i,j]==-1)<<j
        assert bits.bit_count()%2==parity(p)
        generators.append((tuple(p),bits));actions.append([[int(x) for x in row] for row in A.tolist()])
    identity=(tuple(range(6)),0);seen={identity};queue=[identity]
    for a in queue:
        for g in generators:
            b=multiply(g,a)
            if b not in seen:seen.add(b);queue.append(b)
        assert len(seen)<=23040
    assert len(seen)==23040
    actual=collections.Counter(element_order(p,b) for p,b in seen)
    rotational=collections.Counter();weyl=collections.Counter()
    for p in itertools.permutations(range(6)):
        for b in range(64):
            order=element_order(p,b)
            if b.bit_count()%2==parity(p):rotational[order]+=1
            if b.bit_count()%2==0:weyl[order]+=1
    assert actual==rotational and actual[2]==631 and weyl[2]==751
    center=[a for a in seen if all(multiply(a,g)==multiply(g,a) for g in generators)]
    assert set(center)=={identity,(tuple(range(6)),63)}
    assert (s.I*s.eye(4))*forms[0]*(s.I*s.eye(4)).T==-forms[0]
    return dict(status='PASS_ACTUAL_SPIN6_ROTATIONAL_GROUP_NOT_WEYL_D6',
        exterior_square_basis=[[[str(x) for x in row] for row in B.tolist()] for B in forms],
        generator_orthogonal_matrices=actions,group_order=23040,projective_quotient_order=11520,
        actual_element_order_histogram={str(k):v for k,v in sorted(actual.items())},
        W_D6_element_order_histogram={str(k):v for k,v in sorted(weyl.items())},
        actual_involutions=631,W_D6_involutions=751,
        exact_group='All signed6x6 permutation matrices with determinant+1; the rotation subgroup of the B6 hyperoctahedral group.',
        false_lead='W(D6) instead requires an even number of sign flips, independent of permutation parity. It has the same order but different involution and element-order counts, so is not isomorphic to this actual image.',
        map='The actual SU4 matrices act by B -> U B U^T on the recorded six skew forms. Kernel of this exterior-square action is +/-I4; iI4 maps to -I6. Thus linear Clifford46080 -> rotational signed23040 -> projective Clifford11520.',
        boundary='Exact internal finite group/representation bridge. No physical six-dimensional spacetime, E7/E8 extension, universal gate set or new Lie-group isomorphism is inferred.')


if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261102_spin6_rotation_group_audit.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
    print(d['status'],d['actual_involutions'],d['W_D6_involutions'],flush=True)
