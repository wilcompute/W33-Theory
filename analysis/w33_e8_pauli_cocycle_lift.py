#!/usr/bin/env python3
"""Exact Chevalley/lattice-cocycle lift of the E8 order-3 A8 sector to two-qutrit Pauli matrices.

This upgrades the previous support-level certificate.  We choose an explicit
bimultiplicative E8 lattice cocycle, construct an order-three lift of
 g=c^10 to the root algebra, build the 80 invariant oriented-A2 orbit vectors,
and solve the homogeneous phase rescaling which identifies their full Lie
bracket with the standard tensor-qutrit Pauli basis of sl(9,C).

Everything is exact over Z, F_2, F_3 and the phase group <zeta_12>.  The 9x9
Pauli matrices are stored exactly as monomial actions with omega=zeta_3 powers.
"""
from __future__ import annotations
import itertools, json
from collections import Counter, defaultdict
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_e8_pauli_cocycle_lift.json'
import w33_e8_twisted_fibration_weld as base


def imod_matrix(A,p):
    return sp.Matrix([[int(x)%p for x in row] for row in A.tolist()])

def rref_mod(A,p):
    A=[[int(x)%p for x in row] for row in A]
    m,n=len(A),len(A[0]); piv=[]; r=0
    for c in range(n):
        q=next((i for i in range(r,m) if A[i][c]%p),None)
        if q is None: continue
        A[r],A[q]=A[q],A[r]
        inv=pow(A[r][c],-1,p); A[r]=[(x*inv)%p for x in A[r]]
        for i in range(m):
            if i!=r and A[i][c]%p:
                f=A[i][c]%p
                A[i]=[(A[i][j]-f*A[r][j])%p for j in range(n)]
        piv.append(c); r+=1
    return A,piv

def rank_mod(rows,p): return len(rref_mod(rows,p)[1])

def inv_mod_matrix(A,p):
    n=A.rows
    aug=[[int(A[i,j])%p for j in range(n)]+[int(i==j) for j in range(n)] for i in range(n)]
    R,piv=rref_mod(aug,p)
    assert piv[:n]==list(range(n))
    return sp.Matrix([row[n:] for row in R])

def int_tuple(row):
    out=[]
    for x in list(row):
        x=sp.Rational(x); assert x.q==1; out.append(int(x))
    return tuple(out)

def solve_mod_p(eqs,p,nvar):
    A=[[x%p for x in row]+[b%p] for row,b in eqs]
    m=len(A); r=0; piv=[]
    for c in range(nvar):
        q=next((i for i in range(r,m) if A[i][c]%p),None)
        if q is None: continue
        A[r],A[q]=A[q],A[r]
        inv=pow(A[r][c],-1,p); A[r]=[(x*inv)%p for x in A[r]]
        for i in range(m):
            if i!=r and A[i][c]%p:
                f=A[i][c]%p
                A[i]=[(A[i][j]-f*A[r][j])%p for j in range(nvar+1)]
        piv.append(c); r+=1
    for i in range(r,m):
        assert not (all(A[i][c]%p==0 for c in range(nvar)) and A[i][nvar]%p)
    x=[0]*nvar
    for ri,c in enumerate(piv): x[c]=A[ri][nvar]%p
    return x,piv

def solve_mod12(eqs,nvar):
    x3,p3=solve_mod_p(eqs,3,nvar)
    x2,p2=solve_mod_p(eqs,2,nvar)
    lift=[]
    for row,b in eqs:
        val=sum((row[i]%4)*(x2[i]%2) for i in range(nvar))
        d=(b%4-val)%4; assert d%2==0
        lift.append(([a%2 for a in row],(d//2)%2))
    y,p2b=solve_mod_p(lift,2,nvar)
    x4=[(x2[i]+2*y[i])%4 for i in range(nvar)]
    x=[]
    for a,b in zip(x3,x4): x.append(next(t for t in range(12) if t%3==a and t%4==b))
    assert all((sum(row[i]*x[i] for i in range(nvar))-b)%12==0 for row,b in eqs)
    return x,{'rank_mod3':len(p3),'rank_mod2':len(p2),'lift_rank_mod2':len(p2b)}

def pauli_sparse(v):
    x1,z1,x2,z2=v; out=[]
    for j in range(3):
        for k in range(3):
            col=3*j+k; jj=(j+x1)%3; kk=(k+x2)%3; row=3*jj+kk
            out.append({'row':row,'column':col,'omega_power':(z1*j+z2*k)%3})
    return out

def main(write=True):
    roots=sorted(base.e8_roots()); rset=set(roots); ridx={r:i for i,r in enumerate(roots)}
    B=sp.Matrix(base.SIMPLE_ROOTS); Binv=B.inv(); Gram=B*B.T/4
    c=sp.eye(8)
    for r in base.SIMPLE_ROOTS: c=c*base.reflection(r)
    g=c**10; G=B*g*Binv; G=sp.Matrix([[int(x) for x in row] for row in G.tolist()])
    M=sp.eye(8)-G; Omega=G*Gram+2*(G**2)*Gram
    assert G**3==sp.eye(8) and sp.eye(8)+G+G**2==sp.zeros(8)
    Glist=[[int(G[i,j]) for j in range(8)] for i in range(8)]
    Gramlist=[[int(Gram[i,j]) for j in range(8)] for i in range(8)]
    Olist=[[int(Omega[i,j]) for j in range(8)] for i in range(8)]
    def coeff_direct(r): return int_tuple(sp.Matrix([r])*Binv)
    rootc={r:coeff_direct(r) for r in roots}
    def coeff(r): return rootc[r]
    gmap={r:int_tuple(sp.Matrix([r])*g) for r in roots}
    def actroot(r): return gmap[r]
    def rowmul(a,A):
        AA=Glist if A is G else ([[int(A[i,j]) for j in range(8)] for i in range(8)] if hasattr(A,'rows') else A)
        return tuple(sum(int(a[i])*AA[i][j] for i in range(8)) for j in range(8))
    def omega(a,b): return sum(int(a[i])*Olist[i][j]*int(b[j]) for i in range(8) for j in range(8))%3

    L=sp.zeros(8)
    for i in range(8):
        for j in range(i): L[i,j]=int(Gram[i,j])%2
    Llist=[[int(L[i,j]) for j in range(8)] for i in range(8)]
    def eexp(a,b): return sum(int(a[i])*Llist[i][j]*int(b[j]) for i in range(8) for j in range(8))%2
    def eps(a,b): return -1 if eexp(a,b) else 1
    D=(L+G*L*G.T).applyfunc(lambda x:int(x)%2)
    assert D==D.T
    def h(a):
        s=0
        for i in range(8):
            s += int(D[i,i])*(int(a[i])*(int(a[i])-1)//2)
            for j in range(i): s += int(D[i,j])*int(a[i])*int(a[j])
        return s%2
    def eta(a): return -1 if h(a) else 1

    cocycle_comm=True; lift_compat=True
    for ra in roots:
        a=coeff(ra)
        assert (h(a)+h(rowmul(a,G))+h(rowmul(a,G**2)))%2==0
        for rb in roots:
            b=coeff(rb)
            inner=sum(int(a[i])*Gramlist[i][j]*int(b[j]) for i in range(8) for j in range(8))
            cocycle_comm &= (eps(a,b)*eps(b,a) == ((-1)**(inner%2)))
            lhs=(h(tuple(a[i]+b[i] for i in range(8)))+eexp(a,b))%2
            rhs=(h(a)+h(b)+eexp(rowmul(a,G),rowmul(b,G)))%2
            lift_compat &= lhs==rhs
    assert cocycle_comm and lift_compat

    unseen=set(roots); orbits=[]
    while unseen:
        rr=min(unseen); cyc=[rr,actroot(rr),actroot(actroot(rr))]
        rr=min(cyc); cyc=(rr,actroot(rr),actroot(actroot(rr)))
        for x in cyc: unseen.remove(x)
        orbits.append(cyc)
    orbits=sorted(orbits,key=lambda x:x[0]); assert len(orbits)==80
    oid={r:i for i,o in enumerate(orbits) for r in o}
    invcoef=[]
    for o in orbits:
        a0,a1=coeff(o[0]),coeff(o[1])
        cs=(1,eta(a0),eta(a0)*eta(a1))
        assert eta(a0)*eta(a1)*eta(coeff(o[2]))==1
        invcoef.append(dict(zip(o,cs)))

    R,piv=rref_mod(M.tolist(),3); free=[j for j in range(8) if j not in piv]
    null=[]
    for f in free:
        x=[0]*8; x[f]=1
        for i,col in enumerate(piv): x[col]=(-R[i][f])%3
        null.append(x)
    N=sp.Matrix.hstack(*[sp.Matrix(x) for x in null]); assert N.shape==(8,4)
    assert all(int(x)%3==0 for x in M*N)
    Nlist=[[int(N[i,j])%3 for j in range(4)] for i in range(8)]
    def qraw(a): return tuple(sum(int(a[i])*Nlist[i][j] for i in range(8))%3 for j in range(4))
    rep={(0,0,0,0):(0,)*8}
    for o in orbits: rep[qraw(coeff(o[0]))]=coeff(o[0])
    assert len(rep)==81
    def omq(u,v): return omega(rep[u],rep[v])
    V=list(itertools.product(range(3),repeat=4))
    p1=next(v for v in V if any(v)); q1=next(v for v in V if omq(p1,v)==1)
    W=[v for v in V if omq(p1,v)==0 and omq(q1,v)==0]
    p2=next(v for v in W if any(v)); q2=next(v for v in W if omq(p2,v)==1)
    SB=sp.Matrix([p1,q1,p2,q2]); SBi=inv_mod_matrix(SB,3)
    assert int(SB.det())%3!=0
    def qstd(a): return tuple(int(x)%3 for x in (sp.Matrix([qraw(a)])*SBi))
    def plabel(a):
        y=qstd(a)
        return (y[1],y[0],y[3],y[2])
    def psymp(v,w):
        x,z,u,t=v; y,s,r,k=w
        return (z*y-s*x+t*r-k*u)%3
    labels=[plabel(coeff(o[0])) for o in orbits]; assert len(set(labels))==80
    for i in range(80):
        for j in range(80):
            assert omega(coeff(orbits[i][0]),coeff(orbits[j][0]))==psymp(labels[i],labels[j])

    def bracket_scalar(i,j):
        vals=defaultdict(int)
        for ra,ca in invcoef[i].items():
            aa=coeff(ra)
            for rb,cb in invcoef[j].items():
                s=tuple(ra[k]+rb[k] for k in range(8))
                if s in rset: vals[s]+=ca*cb*eps(aa,coeff(rb))
        if not vals: return 0,None
        ts={oid[r] for r in vals}; assert len(ts)==1; t=next(iter(ts))
        ratios=[]
        for r,v in vals.items():
            assert v%invcoef[t][r]==0; ratios.append(v//invcoef[t][r])
        assert len(set(ratios))==1
        return ratios[0],t
    opposite={i:oid[tuple(-x for x in orbits[i][0])] for i in range(80)}
    cartan_cancel=True
    for i,j in opposite.items():
        v=[0]*8
        for ra,ca in invcoef[i].items():
            rb=tuple(-x for x in ra); cb=invcoef[j][rb]; aa=coeff(ra)
            e=eps(aa,coeff(rb))
            for k in range(8): v[k]+=ca*cb*e*aa[k]
        cartan_cancel &= all(x==0 for x in v)
    assert cartan_cancel

    bc=Counter(); eqs=[]
    phase_table={(0,1):11,(0,2):1,(1,0):5,(1,2):3,(2,0):7,(2,1):9}
    def pprod(v,w): return (v[1]*w[0]+v[3]*w[2])%3
    for i,j in itertools.combinations(range(80),2):
        ce,t=bracket_scalar(i,j); bc[ce]+=1
        if ce==0: continue
        a,b=pprod(labels[i],labels[j]),pprod(labels[j],labels[i]); assert a!=b
        pe=phase_table[(a,b)]; se=0 if ce==1 else 6
        row=[0]*80; row[i]=1; row[j]+=1; row[t]-=1
        eqs.append((row,(se-pe)%12))
    assert bc==Counter({1:1100,-1:1060,0:1000}) and len(eqs)==2160
    phases,solve_meta=solve_mod12(eqs,80)
    assert all((sum(row[i]*phases[i] for i in range(80))-b)%12==0 for row,b in eqs)

    entries=[]
    for i,o in enumerate(orbits):
        v=labels[i]
        entries.append({
            'orbit_index':i,
            'pauli_degree':list(v),
            'root_cycle':[list(r) for r in o],
            'lift_invariant_coefficients':[invcoef[i][r] for r in o],
            'operator':f'X^{v[0]} Z^{v[1]} tensor X^{v[2]} Z^{v[3]}',
            'pauli_monomial_9x9':pauli_sparse(v),
            'lie_isomorphism_scale':{'magnitude':'1/sqrt(3)','zeta12_exponent':phases[i]},
        })

    checks={
      'lattice_cocycle_has_e8_commutator':cocycle_comm,
      'explicit_lift_intertwines_cocycle':lift_compat,
      'lift_has_order_three_on_all_roots':all((h(coeff(r))+h(rowmul(coeff(r),G))+h(rowmul(coeff(r),G**2)))%2==0 for r in roots),
      '80_invariant_root_orbits':len(orbits)==80,
      'quotient_coordinates_cover_all_nonzero_F3_4':len(set(labels))==80,
      'quotient_form_equals_standard_two_qutrit_symplectic_form':True,
      'opposite_degree_cartan_brackets_cancel':cartan_cancel,
      'full_e8_bracket_census':bc==Counter({1:1100,-1:1060,0:1000}),
      'phase_system_has_2160_nonzero_brackets':len(eqs)==2160,
      'phase_system_solved_mod12':True,
      'all_nonzero_brackets_match_pauli_structure_constants':True,
      'all_80_actual_9x9_pauli_actions_materialized':len(entries)==80 and all(len(e['pauli_monomial_9x9'])==9 for e in entries),
    }
    assert all(checks.values())
    result={
      'schema':'w33.e8_pauli_cocycle_lift.v1','status':'PASS',
      'headline':'An explicit E8 lattice cocycle and order-3 lift turn the 80 oriented A2 root orbits into invariant Chevalley generators, and a solved zeta_12 rescaling identifies their complete Lie bracket with the standard two-qutrit Pauli basis of sl(9,C).',
      'lift':{
        'g':'c^10','cocycle':'epsilon(a,b)=(-1)^(a L b^T), L=lower-triangular off-diagonal E8 Gram matrix mod 2',
        'lift_phase':'eta(a)=(-1)^h(a), where delta h = epsilon/epsilon after g and h includes diagonal binomial terms',
        'order':3,
      },
      'quotient':{
        'right_kernel_matrix_mod3':[[int(N[i,j])%3 for j in range(4)] for i in range(8)],
        'raw_symplectic_basis_rows':[list(x) for x in (p1,q1,p2,q2)],
        'pauli_coordinate_order':['x1','z1','x2','z2'],
      },
      'brackets':{
        'unordered_pair_census':{'plus_one':bc[1],'minus_one':bc[-1],'zero':bc[0]},
        'nonzero_equations':len(eqs),
        'phase_solver':solve_meta,
        'phase_exponent_census':{str(k):v for k,v in sorted(Counter(phases).items())},
        'isomorphism':'Phi(E_v)=zeta_12^{m_v}/sqrt(3) * (X^x1 Z^z1 tensor X^x2 Z^z2)',
      },
      'entries':entries,
      'check_count':len(checks),'checks':checks,
      'scope':'This fixes an explicit root-algebra/lattice-cocycle lift and an explicit matrix realization. Different cocycle gauges or symplectic bases give equivalent tables; the certificate claims exact equivalence, not uniqueness of gauge.',
    }
    if write: OUT.write_text(json.dumps(result,separators=(',',':'))+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='entries'},indent=2))
    return result

if __name__=='__main__': main(True)
