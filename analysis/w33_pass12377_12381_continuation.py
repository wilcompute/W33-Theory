"""Reproducible five-front continuation; no claim of a completed TOE.

Run from repository root with Python, numpy, sympy and mpmath.
The finite-temperature determinant is a supplied spinless hopping model.
The modular invariant is the known 10D parent, not a new 4D vacuum.
Prior-art guard: analysis/BT7163_BT7170_e8_hexagonal_lift.md concerns
the E8 root fibration and codes, not the Weber CM ratio tested here.
"""
from pathlib import Path
from itertools import product
from collections import Counter
import hashlib
import json
import sys
import numpy as np
import sympy as s
import mpmath as mp

ROOT = Path(__file__).resolve().parents[1]
R = np.array([[1,0,5,-5,1,0],[0,1,-1,0,1,0],[0,0,5,-5,0,1]])
N = s.Matrix([[10,-5,1,-6],[-5,10,-5,6],[1,-5,10,-6],[-6,6,-6,12]])

def weber():
    mp.mp.dps = 90
    def eta(t):
        q = mp.exp(2j*mp.pi*t)
        return mp.exp(mp.pi*1j*t/12)*mp.fprod(1-q**n for n in range(1,160))
    rows = []
    for name,t in [('square',1j),('hexagonal',mp.mpf('.5')+1j*mp.sqrt(3)/2),
                   ('CM_counterexample',1+1j*mp.sqrt(3)/2)]:
        f = mp.exp(-mp.pi*1j/24)*eta((t+1)/2)/eta(t)
        # Independent half-integer q product, avoiding complex-power branches.
        g = mp.exp(-mp.pi*1j*t/24)*mp.fprod(1+mp.exp(2j*mp.pi*t*(n-mp.mpf('.5'))) for n in range(1,160))
        assert abs(f-g) < mp.mpf('1e-80')
        rows.append({'home':name,'ratio':mp.nstr(abs(f)**16/4,75),
                     'independent_product_error':mp.nstr(abs(f-g),5)})
    assert mp.mpf(rows[-1]['ratio']) < 1
    # 4*tau^2-8*tau+7=0 has discriminant -48: exact CM witness.
    t=1+s.I*s.sqrt(3)/2
    assert s.expand(4*t*t-8*t+7)==0
    return {'values':rows,'CM_polynomial':'4*tau^2-8*tau+7',
            'prior':'Pass12046 already gives 0.513; this corrects stale universal-CM wording, not a new flavour model.'}

def torsion_census():
    """Exact Phi_n remainders of Q on ALL n^4 characters for declared n.

    Enumerate h characters; W is unimodular, so this is bijective with z.
    Integer coefficient accumulation and polynomial remainders avoid tolerances.
    A census at order n includes all orders dividing n, not mixed coprime orders.
    """
    h=s.symbols('h:4');x=s.Symbol('x');d=s.Matrix(h)-s.ones(4,1)
    terms=s.Poly(s.expand((d.T*N*d)[0]/2),*h).terms()
    exps=np.array([e for e,c in terms],dtype=np.int64)
    coeff=np.array([int(c) for e,c in terms],dtype=np.int64)
    out=[]
    for n in [2,3,4,5,7,8,9,11,13,16,25,27,32]:
        phi=s.Poly(s.cyclotomic_poly(n,x),x);degree=phi.degree()
        rem=np.zeros((n,degree),dtype=np.int64)
        for j in range(n):
            p=s.Poly(s.rem(x**j,phi.as_expr(),x),x)
            for (a,),c in p.terms():rem[j,a]=int(c)
        hits=[]
        for a in range(n):
            rest=np.array(list(product(range(n),repeat=3)),dtype=np.int64)
            points=np.column_stack((np.full(len(rest),a),rest))
            powers=points@exps.T % n
            vals=np.zeros((len(points),degree),dtype=np.int64)
            for j,c in enumerate(coeff):vals+=c*rem[powers[:,j]]
            hits.extend(points[np.all(vals==0,axis=1)].tolist())
        orders=Counter(n//int(s.gcd(n,s.gcd_list(v))) for v in hits)
        assert len(hits)==(11 if n%3==0 else 1)
        out.append({'n':n,'characters':n**4,'exact_order_histogram':dict(sorted(orders.items())),
                    'h_exponents_of_zeros':hits})
    return {'method':'integer remainders modulo Phi_n, exhaustive n^4', 'cases':out,
            'scope':'Does not eliminate the remaining mixed-prime members of the 464 necessary orders.'}

def geometry():
    def mul(g,h):
        a,b,c=g;A,B,C=h
        return ((a+A)%3,(b+B)%3,(c+C-b*A)%3)
    H=list(product(range(3),repeat=3));ix={g:i for i,g in enumerate(H)}
    dirs=((0,0,1),(0,1,1),(1,0,1),(1,1,0),(1,2,2))
    edges=sorted({tuple(sorted((ix[g],ix[mul(g,t)]))) for g in H for z in dirs for t in (z,mul(z,z))})
    a,b=np.array(edges).T
    cover=json.loads((ROOT/'data/w33_pass11991_native_four_period_cover.json').read_text())
    V=np.array(cover['primitive_integer_edge_voltages'],dtype=int)
    faces=json.loads((ROOT/'data/PART_20261023_NATIVE_ZERO_HOLONOMY_FACE_COMPLETION.json').read_text())
    loops=json.loads((ROOT/'data/w33_20261027_native_bloch_face_module.json').read_text())
    assert len(edges)==135 and V.shape==(135,4)
    return a,b,V,[r['boundary'] for r in faces['independent_face_basis']],loops['commutator_boundaries']

def curl(boundaries,V,k):
    F=np.zeros((len(boundaries),135),complex)
    for r,face in enumerate(boundaries):
        p=np.zeros(4,dtype=int)
        for e,sign in face:
            if sign<0:p-=V[e]
            F[r,e]+=sign*np.exp(1j*(p@k))
            if sign>0:p+=V[e]
        assert not p.any()
    return F

def gradient(a,b,V,k):
    D=np.zeros((135,27),complex)
    D[np.arange(135),a]=-1;D[np.arange(135),b]=np.exp(1j*(V@k))
    return D

def dispersion():
    a,b,V,faces,loops=geometry();rows=[]
    points=[('identity',np.zeros(4)),('order3',2*np.pi/3*np.array([1,1,0,0])),
            ('generic',np.array([.17,-.23,.31,.11])),('inactive_line',np.array([0,0,0,.37]))]
    for t in [.04,.02,.01,.005]:points.append(('infrared',t*np.array([1,2,-1,1.])))
    for label,k in points:
        F=curl(faces,V,k);L=curl(loops,V,k);D=gradient(a,b,V,k)
        U,sv,_=np.linalg.svd(D,full_matrices=True);rank=int(sum(sv>1e-10));T=U[:,rank:]
        base=np.vstack((F,R@L));w=float(sum(abs(np.exp(1j*k[:3])-1)**2))
        repaired=np.vstack((base,np.sqrt(.001*w)*L[[0,5]]))
        rec={'label':label,'k':k.tolist(),'gradient_rank':rank,'weight':w,'operators':{}}
        for name,A in [('mixed_unweighted',base),('six_term_epsilon_001',repaired),('six_loop_unweighted',np.vstack((F,L)))]:
            ward=float(np.max(abs(A@D)));ev=np.linalg.eigvalsh((A@T).conj().T@(A@T))
            assert ward<1e-10
            rec['operators'][name]={'physical_nullity_tolerance_1e_10':int(sum(ev<1e-10)),
                                    'lowest_eigenvalues':ev[:5].tolist(),'ward_residual':ward}
        rows.append(rec)
    assert rows[1]['operators']['mixed_unweighted']['physical_nullity_tolerance_1e_10']==1
    assert rows[1]['operators']['six_term_epsilon_001']['physical_nullity_tolerance_1e_10']==0
    return {'matrix_size':135,'electric_metric':'identity, external Hamiltonian time supplied',
            'couplings':'unit short-face and R^T R mixed-loop couplings; epsilon=.001',
            'cases':rows,'scope':'Sampled full-link dispersion, not a uniform gap or observed light speed.'}

def determinant():
    a,b,V,_,loops=geometry();bits=np.array(list(product(range(2),repeat=4)))
    beta=2.;mu=.3
    def band(k,chem):
        phase=(-1.)**(V@k);H=np.zeros((27,27))
        H[a,b]-=phase;H[b,a]-=phase
        E,U=np.linalg.eigh(H);f=1/(1+np.exp(beta*(E-chem)))
        return E,U,f,phase
    def kernel(q,chem):
        K=np.zeros((135,135));contacts=np.zeros(135)
        for k in bits:
            E,U,f,phase=band(k,chem);Ep,Up,fp,phasep=band(k^q,chem)
            delta=Ep[:,None]-E[None,:];num=fp[:,None]-f[None,:]
            weight=np.empty((27,27));mask=abs(delta)>1e-9
            np.divide(num,delta,out=weight,where=mask)
            fm=(fp[:,None]+f[None,:])/2;weight[~mask]=(-beta*fm*(1-fm))[~mask]
            J=-phase[:,None,None]*Up[a,:,None]*U[b,None,:]+phasep[:,None,None]*Up[b,:,None]*U[a,None,:]
            X=J.reshape(135,-1)
            rho=(U*f)@U.T;contact=2*phase*rho[a,b];contacts+=contact
            K+=(X*weight.ravel())@X.T
        return (K+np.diag(contacts))/16
    def omega(q,u,eps,chem):
        H=np.zeros((432,432),complex)
        ix={tuple(v):i for i,v in enumerate(bits)}
        for cell,c in enumerate(bits):
            sign=(-1.)**int(c@q)
            for e,(aa,bb) in enumerate(zip(a,b)):
                target=ix[tuple((c+V[e])%2)]
                i=27*cell+aa;j=27*target+bb
                value=-np.exp(1j*eps*u[e]*sign)
                H[i,j]+=value;H[j,i]+=value.conjugate()
        E=np.linalg.eigvalsh(H)
        return float(-np.logaddexp(0,-beta*(E-chem)).sum()/(16*beta))
    rows=[];fd=[]
    for q in [np.array([1,0,0,0]),np.array([0,0,1,0]),np.array([1,1,0,0])]:
        K0=kernel(q,mu);K1=kernel(q,mu-.7);delta=K1-K0
        D=gradient(a,b,V,np.pi*q).real
        ward=float(max(np.max(abs(K0@D)),np.max(abs(K1@D))))
        assert ward<1e-10
        u=curl(loops,V,np.pi*q)[0].real;u/=np.linalg.norm(u)
        aa=float(u@(120*K0+10*delta)@u);bb=float(u@(72*K0+10*delta)@u)
        ab=float(u@(10*delta)@u)
        if not rows:
            analytic=float(u@K0@u);zero=omega(q,u,0,mu)
            for step in [.003,.0015]:
                value=(omega(q,u,step,mu)+omega(q,u,-step,mu)-2*zero)/step**2
                assert abs(value-analytic)<2e-6
                fd.append({'step':step,'finite_difference':value,'bloch_kernel':analytic,'error':abs(value-analytic)})
        rows.append({'q_bits':q.tolist(),'ward':ward,'chi_chi':aa,'psi_psi':bb,'chi_psi':ab,'ratio':aa/bb,
                     'K0_extreme_eigenvalues':np.linalg.eigvalsh(K0)[[0,-1]].tolist()})
    charges=[(10,1,1),(5,-3,1),(1,5,1),(5,-2,-2),(5,2,-2),(1,0,4)]
    moments=[sum(d*x**i*y**j for d,x,y in charges) for i,j in [(1,0),(0,1),(3,0),(0,3),(2,1),(1,2)]]
    assert moments==[0]*6
    return {'cover_cells':16,'sites':432,'beta':beta,'chemical_potential':mu,
            'charges_dimension_chi_psi':charges,'linear_and_cubic_charge_moments':moments,
            'symmetry_breaking_input':'onsite energy .7 on the dimension-10 multiplet only',
            'independent_432_site_grand_potential_check':fd,
            'cases':rows,'scope':'Free spinless number-conserving lattice fermions. Charge moments match the E6 branch; no Weyl spectrum, interacting determinant, or dynamical mass selection.'}

def hamming():
    sys.path.insert(0,str(ROOT/'analysis'))
    from w33_20261029_klein_e8_hamming_twistor_transform import generators,hamming_code,partition_rulings,transform_certificate
    gs=generators();codes=[hamming_code(g) for g in gs];alpha,beta=partition_rulings(gs)
    M,B=transform_certificate(alpha,beta)
    def perm(p):
        def word(x):return sum(1<<p[j] for j in range(8) if x>>j&1)
        return [codes.index(frozenset(word(x) for x in c)) for c in codes]
    p=perm([1,2,0,3,4,5,6,7]);q=perm([0,1,2,4,5,3,6,7])
    assert all(p[q[i]]==q[p[i]] for i in range(30))
    unseen=set(range(30));orbits=[]
    while unseen:
        todo=[min(unseen)];orbit=set(todo)
        for i in todo:
            for j in [p[i],q[i]]:
                if j not in orbit:orbit.add(j);todo.append(j)
        orbits.append(sorted(orbit));unseen-=orbit
    # Even coordinate permutations preserve each ruling and incidence intertwiner.
    A=[gs.index(g) for g in alpha];C=[gs.index(g) for g in beta]
    for perm30 in [p,q]:
        pa=[A.index(perm30[i]) for i in A];pb=[C.index(perm30[i]) for i in C]
        assert all(B[pa[i]][pb[j]]==B[i][j] for i in range(15) for j in range(15))
    # Explicit rank-nine native intertwiner: average the centre of the regular
    # 27-address module, then embed the C3^2 regular module into a nine-orbit.
    # Integer map uses centre SUM; multiplying by 1/3 gives the average.
    H=list(product(range(3),repeat=3));hx={g:i for i,g in enumerate(H)}
    J=np.zeros((30,27),dtype=int);base=next(o[0] for o in orbits if len(o)==9)
    for a,b,c in H:
        target=base
        for _ in range(a):target=p[target]
        for _ in range(b):target=q[target]
        J[target,hx[a,b,c]]=1
    assert np.linalg.matrix_rank(J)==9
    # Left translations by X,Y,Z in the native law c+C-b*A.
    for g,perm30 in [((1,0,0),p),((0,1,0),q),((0,0,1),list(range(30)))]:
        for h in H:
            a,b,c=g;A,B,C=h;gh=((a+A)%3,(b+B)%3,(c+C-b*A)%3)
            assert all(J[perm30[row],hx[gh]]==J[row,hx[h]] for row in range(30))
    return {'quotient_generators_on_30_codes':[p,q],'orbit_sizes':list(map(len,orbits)),'orbits':orbits,
            'incidence_transform_equivariant_under_C3_squared':True,
            'native_regular_to_codes_integer_intertwiner':J.tolist(),
            'maximal_intertwiner_rank_for_this_action':9,'killed_native_dimension':18,
            'Hom_dimension_for_this_action':30,
            'obstruction':'v3(8!)=2, so any image of H27 in S8 has order at most 9, hence is abelian and kills its commutator centre. No faithful coordinate-permutation H27 lift.',
            'scope':'Allows a nonfaithful C3^2 quotient; does not exclude projective Hilbert-space actions or general unitaries.'}

def string_control():
    # Character order O,V,S,C, dimensions SO8 and SO16 respectively.
    S=s.Matrix([[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]])/2
    A=s.zeros(4,16)
    for r,i,j,c in [(1,0,0,1),(1,2,2,1),(2,0,2,-1),(2,2,0,-1),
                     (0,1,3,1),(0,3,1,1),(3,1,1,-1),(3,3,3,-1)]:A[r,4*i+j]=c
    assert S*A*s.kronecker_product(S,S).T==A
    # h-c/24 measured in units 24: SO8 c=4, SO16 c=8.
    tr=[-4,8,8,8];tl=[-8,4,16,16]
    phases=[(tr[r]-tl[i]-tl[j])%24 for r in range(4) for i in range(4) for j in range(4) if A[r,4*i+j]]
    assert phases==[0]*8
    broken=A.copy();broken[0,4*1+3]=0
    assert S*broken*s.kronecker_product(S,S).T!=broken
    return {'known_parent':'SO(16)xSO(16) ten-dimensional heterotic string',
            'character_coefficient_matrix':[[int(v) for v in row] for row in A.tolist()],'exact_S_invariance':True,'exact_T_residues_mod24':phases,
            'missing_sector_negative_control':True,'scope':'Gauge/spin character block only, common bosonic factors suppressed. Not a 4D partition function, new vacuum, stabilization or escape from the 99-model exclusion.',
            'external_lead':'https://arxiv.org/abs/2011.04113 (different Z2xZ2 Pati-Salam families; not a verified W33 embedding)'}

def run():
    out={}
    for name,f in [('weber',weber),('torsion',torsion_census),('dispersion',dispersion),('matter',determinant),('hamming',hamming),('string_control',string_control)]:
        out[name]=f();print(name,'finished',flush=True)
    out['producer_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    return out

if __name__=='__main__':
    result=run();target=ROOT/'data/w33_pass12377_12381_continuation.json'
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(target)
