#!/usr/bin/env python3
"""Independent W33/Q8 -> 72-unitary 2-design -> mixed-state purity certificate.

Combinatorial assertions are exact over F3. Complex Clifford gate checks are
numerical; their identities also follow from the exact MUB/2-design theorem.
No imports from the repository's existing mathematical implementations.
"""
import itertools, json, sys
from collections import Counter
from pathlib import Path
import numpy as np

I=(1,0,0,1)
def mul(a,b):
    x,y,z,w=a; u,v,s,t=b
    return ((x*u+y*s)%3,(x*v+y*t)%3,(z*u+w*s)%3,(z*v+w*t)%3)
def inv(a):
    x,y,z,w=a
    return (w,-y%3,-z%3,x)
def order(a):
    b=I
    for n in range(1,25):
        b=mul(b,a)
        if b==I:return n
    raise ValueError(a)
def fixed(a):
    x,y,z,w=a
    return ((x-1)*(w-1)-y*z)%3==0
def maximal_cliques(G):
    out=[]
    def visit(R,P,X):
        if not P and not X:
            out.append(frozenset(R)); return
        pivot=max(P|X,key=lambda u:len(G[u]&P)) if P|X else None
        for v in sorted(P-(G[pivot] if pivot is not None else set())):
            visit(R|{v},P&G[v],X&G[v])
            P.remove(v);X.add(v)
    visit(set(),set(G),set())
    return out
def generators_as_unitaries(G):
    w=np.exp(2j*np.pi/3)
    F=np.array([[w**(i*j) for j in range(3)] for i in range(3)])/np.sqrt(3)
    P=np.diag([1,1,w]).astype(complex)
    steps=[((0,2,1,0),F),((1,0,1,1),P)]
    U={I:np.eye(3,dtype=complex)}
    queue=[I]
    for s in queue:
        for t,gate in steps:
            st=mul(s,t)
            if st not in U:U[st]=U[s]@gate; queue.append(st)
    assert len(U)==24 and set(U)==set(G)
    X=np.roll(np.eye(3),1,axis=0)
    Z=np.diag([w**j for j in range(3)])
    def choi(gate):return gate.T.reshape(9)/np.sqrt(3)
    return {s:np.array([choi(np.linalg.matrix_power(X,a)@
                                 np.linalg.matrix_power(Z,b)@U[s])
                       for a in range(3) for b in range(3)]).T for s in G}
def purity(rho):
    return float(np.trace(rho@rho).real)
def partial_purity(rho):
    r=rho.reshape(3,3,3,3)
    ra=np.trace(r,axis1=1,axis2=3)
    rb=np.trace(r,axis1=0,axis2=2)
    return purity(ra),purity(rb)
def main(out_file=None):
    G=sorted(m for m in itertools.product(range(3),repeat=4)
             if (m[0]*m[3]-m[1]*m[2])%3==1)
    assert len(G)==24
    Q=frozenset(s for s in G if order(s) in (1,2,4))
    assert len(Q)==8
    assert all(mul(a,b) in Q for a in Q for b in Q)
    assert all(frozenset(mul(g,mul(q,inv(g))) for q in Q)==Q for g in G)
    assert all(not fixed(q) for q in Q if q!=I)
    cosets={frozenset(mul(g,q) for q in Q) for g in G}
    assert len(cosets)==3
    adj={g:{h for h in G if g!=h and not fixed(mul(inv(g),h))}
         for g in G}
    cliques=maximal_cliques(adj)
    census=dict(sorted(Counter(map(len,cliques)).items()))
    assert census=={5:144,6:24,8:3}
    assert {c for c in cliques if len(c)==8}==cosets
    C=generators_as_unitaries(G)
    rng=np.random.default_rng(20261109)
    rows=[]
    for coset in sorted(cosets,key=lambda x:sorted(x)):
        E=np.concatenate([C[s] for s in sorted(coset)],axis=1)
        assert E.shape==(9,72)
        gram=np.abs(E.conj().T@E)**2
        for j in range(8):
            assert np.max(np.abs(gram[9*j:9*j+9,9*j:9*j+9]-
                                 np.eye(9)))<1e-11
        cross=gram.copy()
        for j in range(8):cross[9*j:9*j+9,9*j:9*j+9]=np.nan
        assert np.nanmax(np.abs(cross-1/9))<1e-11
        # F_2 = (1/72^2) sum_UV |tr(U*V)|^4 = 2.
        fp2=81*np.sum(gram**2)/72**2
        assert abs(fp2-2)<1e-11
        errors=[]
        for rank in (1,2,3,4,6,9):
            for _ in range(12):
                x=(rng.normal(size=(9,rank))+
                   1j*rng.normal(size=(9,rank)))
                rho=x@x.conj().T
                rho/=np.trace(rho)
                p=np.real(np.sum(E.conj()*(rho@E),axis=0))
                a,b=partial_purity(rho)
                want=1+purity(rho)-(a+b)/3
                errors.append(abs(float(np.sum(p*p))-want))
        assert max(errors)<2e-11
        rows.append({'clifford_gates':72,'MUB_bases':8,
                     'frame_potential_2':round(float(fp2),12),
                     'mixed_state_trials':len(errors),
                     'max_collision_purity_error':max(errors)})
    result={
      'status':'PASS_EXACT_Q8_CLIQUE_AND_UNITARY2DESIGN_WITH_MIXED_PURITY_CONTROLS',
      'SL2_3_order':len(G),'Q8_order':len(Q),'Q8_normal':True,
      'SL2_3_element_orders':dict(Counter(order(g) for g in G)),
      'maximal_clique_sizes':census,
      'Q8_coset_count':len(cosets),
      'maximal_eight_cliques_equal_Q8_cosets':True,
      'single_qutrit_Clifford_partition':'216=3*72',
      'exact_frame_potential':'(81+63)/72 = 2',
      'exact_purity_identity':
        'sum_{e in any 72-Choi family}(tr(rho |e><e|))^2 = 1+tr(rho^2)-(tr(rho_A^2)+tr(rho_B^2))/3',
      'exact_centered_identity':
        'F8(rho)=tr(rho^2)+1/9-(tr(rho_A^2)+tr(rho_B^2))/3',
      'pure_state_entanglement':
        'F8=10/9-(2/3)tr(rho_A^2) in [4/9,8/9]',
      'conditional_purity_ceilings':
        'Combining Pass12639: unbiased 8-MUB states have tr(rho^2)<=1/3; unbiased 5-MUB states <=2/3',
      'family_checks':rows,
      'limitations':'Finite geometry and known unitary-2-design criterion, not TOE dynamics or observed physics.'
    }
    if out_file:
        Path(out_file).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('PASS',json.dumps({'cosets':len(cosets),'maximal_cliques':census,
                              'maximum_numerical_error':max(r['max_collision_purity_error'] for r in rows)}))
    return result
if __name__=='__main__':
    main(sys.argv[1] if len(sys.argv)>1 else None)
