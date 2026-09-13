"""Explicit Schur cross-fibre kernel: quartic matrices and the one-qubit Pauli group.
Prior fibre result: w33_schur176_sixteen_line_fibre_structure.py.
All identities are exact over Q(sqrt(3),i); no hardware interpretation is implied.
"""
from itertools import product
from collections import Counter
from pathlib import Path
import json
import sympy as s
import w33_schur176_sixteen_line_fibre_structure as f


def simp(M):return M.applyfunc(s.simplify)
def equal(A,B):return simp(A-B)==s.zeros(*A.shape)
def mul(x,y):
    p,a,b=x;q,c,d=y
    return ((p+q+2*b*c)%4,a^c,b^d)


def audit():
    I=s.eye(2);om=(-1+s.I*s.sqrt(3))/2
    A=s.Matrix([[-1,1],[2,1]])/s.sqrt(3)
    B=s.Matrix([[-1,om],[2*s.conjugate(om),1]])/s.sqrt(3)
    assert equal(A*A,I) and equal(B*B,I) and equal(A*B,-B*A)
    G=s.diag(2,1)
    assert equal(A.conjugate().T*G*A,G) and equal(B.conjugate().T*G*B,G)
    labels=list(product(range(4),range(2),range(2)))
    mats={g:simp(s.I**g[0]*(A**g[1])*(B**g[2])) for g in labels}
    keys={tuple(M) for M in mats.values()};assert len(keys)==16
    table=[]
    for x in labels:
        row=[]
        for y in labels:
            z=mul(x,y);assert equal(mats[x]*mats[y],mats[z]);row.append(labels.index(z))
        table.append(row)
    # Check the actual quartic and Hessian, not just abstract group relations.
    for M in mats.values():
        u,v=f.u,f.v;U,V=M*s.Matrix([u,v])
        assert all(s.simplify(x)==0 for x in s.Poly(f.phi(U,V)-f.phi(u,v),u,v).coeffs())
        assert all(s.simplify(x)==0 for x in s.Poly(f.hess(U,V)-f.hess(u,v),u,v).coeffs())
    # Explicit conjugator sends these two quartic-preserving involutions to Z,X.
    vp=s.Matrix([1,1+s.sqrt(3)]);assert equal(A*vp,vp)
    S=simp(s.Matrix.hstack(vp,B*vp));Sinv=simp(S.inv())
    Z=s.diag(1,-1);X=s.Matrix([[0,1],[1,0]])
    assert equal(Sinv*A*S,Z) and equal(Sinv*B*S,X)
    assert equal(S.conjugate().T*G*S,(s.simplify((vp.conjugate().T*G*vp)[0]))*I)
    for g in labels:assert equal(Sinv*mats[g]*S,s.I**g[0]*Z**g[1]*X**g[2])
    center=[x for x in labels if all(mul(x,y)==mul(y,x) for y in labels)]
    assert len(center)==4
    orders={}
    for x in labels:
        z=(0,0,0)
        for n in range(1,5):
            z=mul(z,x)
            if z==(0,0,0):orders[x]=n;break
    assert len(orders)==16
    # Left regular permutations provide an independent integral realization.
    perms={x:tuple(labels.index(mul(x,y)) for y in labels) for x in labels}
    for x,y in product(labels,repeat=2):assert tuple(perms[x][perms[y][i]] for i in range(16))==perms[mul(x,y)]
    prior=json.loads((Path(__file__).resolve().parents[1]/'data/w33_schur176_sixteen_line_fibre_structure.json').read_text())
    assert prior['cross_fibres']['kernel_order']==16 and prior['cross_fibres']['is_C2^4'] is False
    return {'schema':'w33.schur-cross-kernel-matrices.v1','status':'PASS','group':'one-qubit Pauli group including phases {1,i,-1,-i}',
      'presentation':'z central, z^4=A^2=B^2=1, BA=z^2 AB; z=iI',
      'normal_form':'i^p A^a B^b','multiplication':'(p,a,b)*(q,c,d)=(p+q+2bc mod4,a xor c,b xor d)',
      'order':16,'center_order':len(center),'element_order_histogram':dict(Counter(orders.values())),
      'positive_hermitian_form':[[str(x) for x in row] for row in G.tolist()],
      'conjugator_to_pauli':[[str(x) for x in row] for row in S.tolist()],
      'elements':[{'label':list(g),'matrix':[[str(x) for x in row] for row in mats[g].tolist()],'left_regular_permutation':list(perms[g])} for g in labels],
      'multiplication_table':table,'quartic_and_hessian_invariance_checks':16,
      'boundary':'Explicit kernel of the previously certified cross-fibre action. The unitarizing form is basis-dependent and supplied explicitly; no canonical physical metric, common global action on all eleven blocks, or device implementation is claimed.'}

if __name__=='__main__':
    import sys
    r=audit()
    if '--write' in sys.argv:Path(__file__).with_suffix('.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:r[k] for k in ['status','group','order','center_order','element_order_histogram']},indent=2))
