"""Exact executable lift of prior Schur48/A4 classification, with phase cocycle.
Prior: w33_schur176_sixteen_line_fibre_structure, w33_schur_cross_kernel_matrices,
w33_projective_phase_fibre_dichotomy. Known coherent-control phase semantics,
not a new group classification or a control oracle for unknown operations.
"""
from itertools import product
from pathlib import Path
import json
import sympy as s
import w33_schur_cross_kernel_matrices as prior

def norm(M): return M.applyfunc(lambda x:s.expand(x))
def audit():
    I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
    omega=(-1+s.I*s.sqrt(3))/2;T=(-I+s.I*(X+Y+Z))/2;C=norm(omega*T)
    assert norm(C**3)==I
    pl=list(product(range(4),range(2),range(2)))
    P={g:s.I**g[0]*Z**g[1]*X**g[2] for g in pl}
    alpha={g:next(h for h in pl if norm(T*P[g]*T.conjugate().T)==P[h]) for g in pl}
    assert all(alpha[alpha[alpha[g]]]==g for g in pl)
    labels=[(*g,k) for k in range(3) for g in pl];idx={g:i for i,g in enumerate(labels)}
    def mul(a,b):
        h=b[:3]
        for _ in range(a[3]):h=alpha[h]
        return (*prior.mul(a[:3],h),(a[3]+b[3])%3)
    mats=[norm(P[g[:3]]*C**g[3]) for g in labels]
    assert len({tuple(m) for m in mats})==48
    table=[[idx[mul(a,b)] for b in labels] for a in labels]
    # Check all products against exact matrices, then all associativity triples.
    for i,j in product(range(48),repeat=2):assert norm(mats[i]*mats[j])==mats[table[i][j]]
    for i,j,k in product(range(48),repeat=3):assert table[table[i][j]][k]==table[i][table[j][k]]
    raw=json.loads(Path(prior.__file__).with_suffix('.json').read_text())
    S=s.Matrix([[s.sympify(v) for v in row] for row in raw['conjugator_to_pauli']])
    x,y=s.symbols('x y');u,v=S*s.Matrix([x,y])
    phi=s.Poly(s.expand(prior.f.phi(u,v)),x,y).as_expr()
    hess=s.Poly(s.expand(prior.f.hess(u,v)),x,y).as_expr()
    def invariant(poly,M,factor):
        U,V=M*s.Matrix([x,y])
        return all(s.simplify(v)==0 for v in s.Poly(s.expand(poly.subs({x:U,y:V},simultaneous=True)-factor*poly),x,y).coeffs())
    # Generator identities plus exact closure certify all 48 polynomial identities.
    assert all(invariant(phi,M,1) for M in (X,Z,s.I*I,C))
    assert all(invariant(hess,M,1) for M in (X,Z,s.I*I))
    assert invariant(hess,C,omega**2)
    ql=list(product(range(2),range(2),range(3)));qi={g:i for i,g in enumerate(ql)}
    qt=[];coc=[]
    for a,b,k in ql:
        row=[];ph=[]
        for c,d,l in ql:
            z=mul((0,a,b,k),(0,c,d,l));row.append(qi[z[1:]]);ph.append(z[0])
        qt.append(row);coc.append(ph)
    for a,b,c in product(range(12),repeat=3):
        assert (coc[a][b]+coc[qt[a][b]][c]-coc[b][c]-coc[a][qt[b][c]])%4==0
    # Commuting quotient elements have phase commutator -1. A section rephase
    # adds a coboundary whose antisymmetric part vanishes on commuting pairs.
    # Thus no choice of scalar gauge makes this extension split.
    za=qi[(1,0,0)];xb=qi[(0,1,0)]
    assert qt[za][xb]==qt[xb][za]
    assert (coc[za][xb]-coc[xb][za])%4==2
    # Identical standalone channels; distinct phase-referenced controlled circuits.
    compass=[]
    for p in range(4):
        U=s.I**p*I;assert norm(U*Z*U.conjugate().T)==Z
        psi=s.Matrix([1,s.I**p])/s.sqrt(2)
        compass.append([str(s.simplify((psi.conjugate().T*M*psi)[0])) for M in (X,Y,Z)])
    assert len(set(map(tuple,compass)))==4
    return {'status':'PASS','normal_form':'i^p Z^a X^b C^k; C=omega*(-I+i(X+Y+Z))/2',
      'omega':str(omega),'labels':labels,'matrices':[[[str(v) for v in row] for row in M.tolist()] for M in mats],
      'alpha':[[g,alpha[g]] for g in pl],'multiplication_table':table,'matrix_products_checked':2304,
      'associativity_triples_checked':110592,'quotient_labels':ql,'quotient_table':qt,'central_cocycle_mod4':coc,
      'cocycle_triples_checked':1728,'non_split_witness':{'quotient_pair':[za,xb],'phase_commutator_mod4':2},'hessian_character':'omega^(2*k)','hessian_kernel_order':16,
      'controlled_central_phase_ancilla_bloch_XYZ':compass,
      'boundary':'Prior owns 48/A4 classification. Exact phase ISA and cocycle instantiate it. Coherent control assumes a known phase-referenced implementation; projective black-box access cannot supply this information. No TOE particle or physical realization claim.'}
if __name__=='__main__':
    import sys
    out=audit()
    if '--write' in sys.argv:Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('labels','matrices','alpha','multiplication_table','quotient_table','central_cocycle_mod4')},indent=2))
