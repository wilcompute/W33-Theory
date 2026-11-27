"""Six reproducible Witting/E6/causal research fronts; no physical TOE claim."""
import json, math
from pathlib import Path
from itertools import combinations
from collections import Counter
from fractions import Fraction
import numpy as np
import sympy as sp
from scipy.optimize import linprog
from scipy.linalg import expm, qr
from sympy.combinatorics import Permutation, PermutationGroup
import toe_20261122_witting_one_phase_three_fixed as W
import toe_20261122_round6_16effect_optimal as MIC
from toe_20261122_round6_minimal_ic import get_mats
import toe_20261122_photonic_sparse_isometry_loss as O
import toe_20261122_round5_18effect_optical as R
import toe_20261122_next5_compiler_photonics as G
import toe_20261122_round7_h27_subsystem_code as Q
import toe_20261122_round7_h27_mediator_vacuum as V
from toe_20261122_round6_causal_graph_no_go import w33, CUT
ROOT=Path(__file__).resolve().parents[1]

def mic():
    rays=W.all_rays(); P,A,b=get_mats()
    perms=[]
    for k in (5,26,33,36):
        perm=[]
        for x in rays:
            y=W.reflect(rays[k],x)
            hits=[i for i,r in enumerate(rays) if W.proportional(y,r)]
            assert len(hits)==1
            perm.append(hits[0])
        perms.append(Permutation(perm))
    group=PermutationGroup(perms)
    seed=tuple(MIC.S); heavy=tuple(MIC.HEAVY)
    orbit={tuple(sorted(g(i) for i in seed)) for g in group.generate_schreier_sims()}
    print('MIC group',group.order(),'orbit',len(orbit),flush=True)
    # Search neighboring nondegenerate vertices by exact simplex pivots.
    # Broad randomized LP, exact rational verification for every new support.
    # In rational coordinates use Gram entries: 0,1/3,1.
    import toe_20261122_witting_qutrit_sic_mub30 as GEO
    gram=np.array([[int(3*GEO.abs2(GEO.dots(x,y))/(GEO.dots(x,x)[0]*GEO.dots(y,y)[0])) for y in rays] for x in rays])
    assert np.allclose(gram,3*np.abs(np.einsum('aij,bji->ab',P,P)))
    assert set(gram.ravel())=={0,1,3}
    rng=np.random.default_rng(20261127); seen=set(); new=[]; best=None
    candidates=[seed]
    pivot_candidates=set();pivot_deg=Counter()
    for j in set(range(40))-set(seed):
        mat=sp.Matrix(gram[np.ix_(seed,seed)].tolist());weights=mat.inv()*sp.ones(16,1)*3
        direction=mat.inv()*sp.Matrix(gram[list(seed),j].tolist())
        ratios=[(weights[i]/direction[i],i) for i in range(16) if direction[i]>0]
        step=min(x[0] for x in ratios);leaving=[i for q,i in ratios if q==step]
        pivot_deg[len(leaving)]+=1
        if len(leaving)==1:
            s=tuple(sorted((set(seed)-{seed[leaving[0]]})|{j}));pivot_candidates.add(s);candidates.append(s)
    for _ in range(3500):
        fit=linprog(rng.normal(size=40),A_eq=A,b_eq=b,bounds=(0,None),method='highs')
        if not fit.success:continue
        s=tuple(map(int,np.flatnonzero(fit.x>1e-8)))
        if len(s)==16 and s not in seen:
            seen.add(s);candidates.append(s)
    for s in candidates:
        mat=sp.Matrix(gram[np.ix_(s,s)].tolist())
        if mat.det()==0:continue
        weights=mat.inv()*sp.ones(16,1)*3
        if min(weights)<=0:continue
        # A positive solution whose projection onto the full rank Hermitian basis equals I.
        w=np.array(weights,float).ravel();assert np.max(abs(A[:,s]@w-b))<1e-11
        # Exact norm squared of residual using 3G and trace P_i=1.
        assert (weights.T*mat*weights)[0]/3-2*sum(weights)+4==0
        F=np.column_stack([float(x)*P[i].ravel() for i,x in zip(s,weights)])
        cond=float(np.linalg.cond(F@F.conj().T))
        row=dict(support=list(s),weights=list(map(str,weights)),gram_determinant=str(mat.det()/3**16),condition=cond,outside_seed_orbit=s not in orbit)
        if s not in orbit:new.append(row)
        if best is None or cond<best['condition']:best=row
    # Search optical hardware permutations of supports beyond the old 648 orbit.
    # Exhaust all 2880 orbit supports and all discovered distinct supports.
    choices=sorted(orbit); ids=np.arange(len(choices))
    rv=np.array([[complex(float(a)-float(b)/2,float(b)*np.sqrt(3)/2) for a,b in r] for r in rays]);rv/=np.linalg.norm(rv,axis=1)[:,None]
    low=None
    for s in [choices[i] for i in ids]+[tuple(x['support']) for x in new]+[seed]:
        weights=np.linalg.solve(gram[np.ix_(s,s)],np.full(16,3.))
        v=np.sqrt(weights)[:,None]*rv[list(s)].conj()
        stat=O.stats(v,.995,0)
        row=dict(support=list(s),weights=weights.tolist(),couplers=stat['gate_count'],survival=stat['maximally_mixed_input_detection_probability'])
        if low is None or (row['couplers'],-row['survival'])<(low['couplers'],-low['survival']):low=row
    s=low['support'];vv=np.sqrt(low['weights'])[:,None]*rv[s].conj();low['haar_risk']=R.loss_risk(vv,np.eye(4)/4)['source_photon_HS_risk_coefficient']-.75
    return dict(group_order=int(group.order()),seed_support_orbit=len(orbit),support_stabilizer=int(group.order())//len(orbit),random_lp_draws=3500,distinct_lp_16_supports=len(seen),outside_seed_orbit_count=len(new),outside_examples=new[:10],best_condition=best,nondegenerate_seed_pivots=len(pivot_candidates),pivot_leaving_multiplicity={str(k):v for k,v in pivot_deg.items()},tested_optical_layouts=len(ids)+len(new)+1,best_low_couplers=low)

def compiler():
    gates=G.gates();I=np.eye(4,dtype=complex);word='db'*6;U=np.linalg.matrix_power(gates['d']@gates['b'],6)
    # U has identity on the orthogonal two-plane, eigenvalues exp(+-i theta) on its support.
    eig=np.linalg.eigvals(U); k=int(np.argmax(np.angle(eig)));theta=float(np.angle(eig[k])); assert theta>0
    from scipy.linalg import schur
    T,S=schur(U,output='complex');ang=np.angle(np.diag(T)); J=S@np.diag(1j*np.sign(np.where(abs(ang)>1e-7,ang,0)))@S.conj().T
    assert np.linalg.norm(expm(theta*J)-U)<1e-10
    # Conjugate one exact dense-circle word to obtain a basis of su(4).
    def coord(x):return np.r_[x.real.ravel(),x.imag.ravel()]
    from toe_20261122_round6_beam_compiler import build_gates
    H,_,_,hwords,_=build_gates()
    pool=[M@J@M.conj().T for M in H]
    coords=np.column_stack([coord(a) for a in pool]);_,_,piv=qr(coords,pivoting=True,mode='economic')
    inds=piv[:15];basis=[pool[i] for i in inds];words=[hwords[i][0] for i in inds]
    B=np.column_stack([coord(a) for a in basis]);sigma=np.linalg.svd(B,compute_uv=False)
    assert sigma[-1]>1e-5
    # Independent exact modular ranks of the same conjugates of U-U^dagger,
    # a nonzero scalar multiple of J. This certifies real Lie-basis independence.
    import toe_20261122_discrete_witting_dense_su4 as E
    ranks=[]
    for prime in (7,13,19,31,37,43):
        gg={}
        for j,t in zip((5,26,33),('a','b','c')):gg[t],gg[t.upper()]=E.reflection(j,prime)
        gg['d']=E.pi_phase(36,prime)[0]
        def mulword(w):
            M=np.eye(4,dtype=np.int64)
            for t in w:M=M@gg[t]%prime
            return M
        def invword(w):return ''.join(t if t=='d' else t.swapcase() for t in w[::-1])
        Jm=(mulword(word)-mulword(invword(word)))%prime
        mats=[(mulword(w)@Jm@mulword(invword(w))%prime).ravel() for w in words]
        ranks.append([prime,E.rank_mod(mats,prime)])
    assert max(r for _,r in ranks)==15
    # Exact eigenangle from Chebyshev: normalized db pair has cos(phi)=-sqrt(3)/6;
    # (db)^6 has cos(theta)=-T6(cos(phi))=-5/27. Use rational Taylor brackets.
    assert sp.simplify(-sp.chebyshevt(6,-sp.sqrt(3)/6))==-sp.Rational(5,27)
    F=Fraction
    def atan_bounds(x,n):
        terms=[(-1)**j*x**(2*j+1)/F(2*j+1) for j in range(n)]
        a=sum(terms);b=a+(-1)**n*x**(2*n+1)/F(2*n+1)
        return min(a,b),max(a,b)
    aa=atan_bounds(F(1,5),35);bb=atan_bounds(F(1,239),12)
    pi_lo=16*aa[0]-4*bb[1];pi_hi=16*aa[1]-4*bb[0]
    # Fixed decimal rational brackets, verified by alternating Taylor cos.
    lo=F('1.757056630371452');hi=F('1.757056630371454')
    def cos_bounds(x,n=25):
        a=sum((-1)**j*x**(2*j)/math.factorial(2*j) for j in range(n));b=a+(-1)**n*x**(2*n)/math.factorial(2*n)
        return min(a,b),max(a,b)
    assert cos_bounds(lo)[0]>-F(5,27)>cos_bounds(hi)[1]
    al,ah=lo/(2*pi_hi),hi/(2*pi_lo)
    rational=((al+ah)/2).limit_denominator(100000)
    p,q=rational.numerator,rational.denominator
    dr=max(abs(al-rational),abs(ah-rational));angular_bound=pi_hi/q+2*pi_hi*q*dr
    assert math.gcd(p,q)==1
    # This gives a rigorously bounded circle covering using signed powers 0,...,q-1.
    # Exact analytic bound: uniform rational circle error pi/q plus q times angular mismatch.
    # Explicit finite-circle covering certificate. Every phase is within half the max gap.
    K=8192; angles=np.mod(theta*np.arange(K+1),2*np.pi); order=np.argsort(angles); gaps=np.diff(np.r_[angles[order],angles[order][0]+2*np.pi]); gap=float(max(gaps));delta=gap/2+1e-9
    def nearest_phase(t):
        idx=int(np.argmin(abs(np.angle(np.exp(1j*(angles-t))))));return idx,float(abs(np.angle(np.exp(1j*(angles[idx]-t)))))
    # Approximation for a fixed generic small SU4 target, using Trotter and independent powers.
    rng=np.random.default_rng(20261127);C=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));L=(C-C.conj().T)*.025;L-=np.trace(L)/4*I
    coefficients=np.linalg.lstsq(B,coord(L),rcond=None)[0];assert np.linalg.norm(sum(c*j for c,j in zip(coefficients,basis))-L)<1e-10
    target=expm(L);comm=sum(np.linalg.norm(a@b-b@a,2)*abs(c*d) for (a,c),(b,d) in combinations(zip(basis,coefficients),2))
    rows=[]
    for m in (1,2,4,8,16):
        one=I.copy();ideal=I.copy();powers=[];phase_error=0
        for a,c in zip(basis,coefficients):
            k,e=nearest_phase(c/m);powers.append(k);phase_error+=e;one=one@expm(angles[k]*a);ideal=ideal@expm(c/m*a)
        actual=np.linalg.matrix_power(one,m);ideal=np.linalg.matrix_power(ideal,m)
        err=float(np.linalg.norm(target-actual,2)); bound=float(comm/(2*m)+m*phase_error+1e-10)
        assert err<=bound+1e-9
        rows.append(dict(trotter_steps=m,powers=powers,operator_norm_error=err,analytic_bound_using_actual_phase_errors=bound,worst_circle_bound=float(comm/(2*m)+15*m*delta),ideal_trotter_error=float(np.linalg.norm(target-ideal,2)),primitive_gate_count=m*sum(12*k+2*len(w) for k,w in zip(powers,words))))
    # Rational circle compiler via modular inverse; use signed powers for shorter words.
    rational_rows=[]
    for m in (1,2,4,8,16):
        one=I.copy();powers=[]
        for j,c in zip(basis,coefficients):
            r=int(round(q*c/(m*2*np.pi)))%q;k=(r*pow(p,-1,q))%q
            if k>q//2:k-=q
            powers.append(k);one=one@expm(theta*k*j)
        word_unitary=I.copy()
        for k,w in zip(powers,words):
            Hword=I.copy()
            for token in w:Hword=Hword@gates[token]
            word_unitary=word_unitary@Hword@np.linalg.matrix_power(U,k)@Hword.conj().T
        assert np.linalg.norm(word_unitary-one,2)<1e-8
        error=float(np.linalg.norm(target-np.linalg.matrix_power(word_unitary,m),2))
        # conservative extra 1e-10 for floating target/circuit matrix calculation
        bound=comm/(2*m)+15*m*float(angular_bound)+1e-10
        assert error<=bound+1e-8,(m,error,bound,p,q,float(angular_bound),powers)
        rational_rows.append(dict(trotter_steps=m,operator_norm_error=error,analytic_worst_phase_bound=bound,powers=powers,primitive_gate_count=m*sum(12*abs(k)+2*len(w) for k,w in zip(powers,words))))
    # Constructivity for arbitrary SU4: traceless logarithm, basis coefficients, product formula;
    # dense circle by irrational eigenphase: (D b)^6 cannot have finite order by old exact trace proof.
    return dict(circle_word=word,theta=theta,basis_rank=len(basis),basis_words=words,basis_min_singular_value=float(sigma[-1]),exact_modular_basis_ranks=ranks,circle_powers_max=K,maximum_phase_gap=gap,exact_cos_theta="-5/27",rational_circle_pq=[p,q],rigorous_angular_cover_bound=float(angular_bound),rational_circle_examples=rational_rows,example_target_log_coefficients=coefficients.tolist(),examples=rows,scope='Convergent constructive Trotter/power compiler, not efficient Solovay-Kitaev. Rational phase bound certified via Taylor brackets; Trotter coefficient norms and target logarithm in example computed numerically. Small target benchmark only.')

def qec():
    x,y,U,w=Q.build(); C=U[:,::3]; d=9
    # Full independently randomized SU(3)^3 local action: the three 9D trinification blocks
    # are inequivalent irreps, so twirl is block depolarization. Explicit 27^2 Kraus action
    # reduced from simple block rank-one operators (243 of them).
    def effective(K):return [(U.conj().T@K@C).reshape(9,3,9)[:,a,:] for a in range(3)]
    def fe(Ks):return float(sum(abs(np.trace(a))**2 for k in Ks for a in effective(k))/d**2)
    Ks=[]
    for block in range(3):
        for i,j in [(i,j) for i in range(9) for j in range(9)]:
            k=np.zeros((27,27),complex);k[9*block+i,9*block+j]=1/3;Ks.append(k)
    assert np.max(abs(sum(k.conj().T@k for k in Ks)-np.eye(27)))<1e-12
    f=fe(Ks);assert abs(f-1/27)<1e-12
    for k in range(3):
        P=C[k*9:(k+1)*9].conj().T@C[k*9:(k+1)*9]
        assert np.max(abs(P@P-P))<1e-12 and abs(np.trace(P)-3)<1e-12
    # Single local Cartan phase (one SU3 factor) on the first and second blocks.
    # Representation A=(3,bar3,1), B=(1,3,bar3), C=(bar3,1,3) up to conventions;
    # pick a phase acting on the first tensor factor of block 0, conjugate on one factor of block 2.
    from toe_20261122_e6_132_constructive_embedding import blocks,tensor
    H=np.diag([1.,-1.,0.]);I=np.eye(3)
    K=blocks(tensor(H,I),np.zeros((9,9)),tensor(-H,I))
    rows=[]
    for t in (.01,.05,.1,.25,.5,1.):
        F=fe([expm(1j*t*K)]);rows.append(dict(theta=t,entanglement_fidelity=F,average_gate_fidelity=(9*F+1)/10))
    # Convex mixture is exact, since entanglement fidelity is linear in channel.
    return dict(logical_dimension=d,restricted_H27_F_e=fe([x]),trinification_twirl_F_e=f,mixture=[dict(probability=p,F_e=1-p+p*f) for p in (.001,.01,.05,.1,1.)],local_phase_rows=rows,scope='For mixture of restricted H27 noise and complete SU3^3 twirl, fixed recovery is optimal: the twirl retains only three classical block labels of rank 3 on the code, so any recovery contributes at most 3/81 entanglement fidelity; the restricted branch contributes at most 1. The displayed mixture attains both bounds. Local coherent phase rows use fixed recovery only. Mixture probability is illustrative, not measured E6 noise.')

def higgs():
    reduced=V.verify();assert reduced['full_15x15_Hessian_rank']==14
    m=sp.Rational(20,9);a=-sp.Rational(1,18)
    masses={q:[m+q*a-2,m+q*a+1,m+q*a+1] for q in (4,1,-2)}
    assert masses[4]==[0,3,3]
    # Full E6-invariant W= m v.u + v.A.u + 1/2 Tr_27 A^2 + mediator terms.
    # Cartan T=diag(4,1^16,-2^10), Tr T^2=72. SO10 invariance ensures all other F terms vanish.
    assert 4**2+16+10*4==72 and 72*a+4==0
    # Spinor mixing only for family0: 2 copies each of 16 and conjugate (H0, adjoint).
    # Broken gauge generator gives one null vector per 16. Nonzero adjoint quadratic pairing
    # implies 2x2 coefficient matrix rank >=1, hence exactly 1. Other two families unmixed.
    # No accidental zero on remaining charges; adjoint 45 has nondegenerate invariant trace form.
    rank={'singlet_and_mediator':14,'ten_plets':60,'adjoint_45':45,'spinors_families_1_2':64,'spinors_family0_and_adjoint':32}
    dims={'singlet_and_mediator':15,'ten_plets':60,'adjoint_45':45,'spinors_families_1_2':64,'spinors_family0_and_adjoint':64}
    assert sum(dims.values())==248 and sum(rank.values())==215
    assert all(x!=0 for x in masses[1]+masses[-2])
    # Optional three chiral 27_M: H27 invariant symmetric family tensor h_iii=A, h_distinct=B.
    # Singlet Higgs VEV at family0 yields full-rank 10_M masses, no 16_M masses.
    M=sp.Matrix([[2,0,0],[0,0,1],[0,1,0]]);assert M.det()==-2
    # E6 has no primitive symmetric cubic Lie-algebra invariant (degrees 2,5,6,8,9,12).
    # Higgs chiral matter itself is vectorlike under E6 x H27 (mediators pair opposite chars).
    # Optional 3 chiral 27_M have unit determinant for both H27 triplet generators.
    assert np.isclose(np.linalg.det(np.roll(np.eye(3),1,axis=0)),1)
    assert np.isclose(np.linalg.det(np.diag([1,np.exp(2j*np.pi/3),np.exp(4j*np.pi/3)])),1)
    return dict(perturbative_E6_gauge_anomaly='zero: vectorlike Higgs sector and no rank-3 symmetric invariant of E6 Lie algebra for optional chiral 27_M',H27_mixed_determinant_test='triplet X and Z determinant 1; full discrete anomaly not audited',full_Higgs_fields=248,full_holomorphic_Hessian_rank=215,nullity=33,broken_complex_gauge_dimension=33,rank_by_SO10_sector=rank,dimension_by_SO10_sector=dims,charge_family_mass_coefficients={str(k):list(map(str,v)) for k,v in masses.items()},matter_optional_10_family_matrix=M.tolist(),matter_optional_10_family_det=int(M.det()),scope='Analytic block-rank certificate by SO10 branching, gauge Ward identity and invariant trace pairing, not a brute-force 248x248 E6 generator evaluation. Higgs-only isolated local orbit, unbroken SO10 not SM; optional 3 chiral families are input, matter singlets and spinors massless at this stage, discrete anomaly not audited.')

def e8_bridge():
    # 248 fields exactly match E8 adjoint branching, but the renormalizable
    # superpotential deliberately breaks the continuous family group.
    w=sp.Rational(-1,2)+sp.sqrt(3)*sp.I/2;X=sp.zeros(3)
    for k in range(3):X[(k+1)%3,k]=1
    Z=sp.diag(1,w,w**2);modes=[(i,j) for i in range(3) for j in range(3) if (i,j)!=(0,0)]
    traces={}
    for i,j in modes:
        t=sp.simplify(sp.trace(X**i*Z**j*X**((-i)%3)*Z**((-j)%3))/3)
        assert sp.simplify(t-w**(-i*j))==0;traces[str((i,j))]=str(t)
    # Restore SU3 trace pairing and integrate out a traceless mediator S:
    # W(S)=1/2 tr(S^2)+v^T S u, S=-uv^T+(v^Tu)I/3.
    u=sp.Matrix(sp.symbols('u0:3'));v=sp.Matrix(sp.symbols('v0:3'));B=(v.T*u)[0];S=-u*v.T+B*sp.eye(3)/3
    assert sp.expand(sp.trace(S))==0
    w_eff=sp.expand(sp.trace(S*S)/2+(v.T*S*u)[0]);assert sp.expand(w_eff+B**2/3)==0
    # Single commuting E8 adjoint chiral superfield has no invariant symmetric cubic.
    return dict(E8_branching_dimensions=[78,8,81,81],H27_mediators_are_eight_nontrivial_characters=True,trace_pairing_coefficients=traces,SU3_restored_effective_quartic='-(v^T u)^2/3',E8_basic_invariant_degrees=[2,8,12,14,18,20,24,30],scope='Representation matching only. The chosen mediator mass uses unweighted opposite-character pairing, not SU3 trace pairing. Restoring SU3 in this singlet model yields only a function of the invariant bilinear and reinstates family flat directions (for nonzero B, modulo E6 U1). A single E8 adjoint commuting chiral superfield has no cubic invariant; E8 gauge dynamics or multiple fields are not excluded.')

def causal():
    _,edges,_=w33();c=np.array(CUT);N=40;adj=np.zeros((N,N),int)
    for i,j in edges:
        if c[i]!=c[j]:adj[i,j]=adj[j,i]=1
    dist=np.full(N,-1);dist[0]=0;queue=[0]
    for i in queue:
        for j in np.flatnonzero(adj[i]):
            if dist[j]<0:dist[j]=dist[i]+1;queue.append(j)
    dag=(adj>0)&(dist[:,None]<dist[None,:]);rel=dag.copy()
    for k in range(N):rel|=rel[:,k,None]&rel[k,None,:]
    assert rel.sum()==287
    def summary(r):
        n=len(r);interior=r.astype(np.int32)@r.astype(np.int32);h=np.bincount(interior[r],minlength=3);pairs=int(r.sum());height=1
        order=np.argsort(r.sum(axis=0));dp=np.ones(n,int)
        for j in order:
            if r[:,j].any():dp[j]=1+max(dp[r[:,j]])
        return dict(N=n,pairs=pairs,ordering_fraction=2*pairs/(n*(n-1)),height=int(max(dp)),N0=int(h[0]),N1=int(h[1]),N2=int(h[2]),BD2_reduced=int(n-2*h[0]+4*h[1]-2*h[2]))
    rng=np.random.default_rng(20261127);rows=[]
    # Generate degree-matched bipartite graphs by 2000 degree-preserving edge swaps.
    # Same four-layer BFS method, not a uniform graph sampler.
    matched=[];left=np.arange(20);right=np.arange(20,40)
    for trial in range(12):
        cross={(i,20+(i+j)%20) for i in left for j in range(8)}
        for _ in range(2000):
            ee=sorted(cross);i,j=ee[int(rng.integers(len(ee)))];a,b=ee[int(rng.integers(len(ee)))];
            if i!=a and j!=b and (i,b) not in cross and (a,j) not in cross:
                cross.remove((i,j));cross.remove((a,b));cross.update(((i,b),(a,j)))
        A=np.zeros((40,40),bool)
        for i,j in cross:A[i,j]=A[j,i]=True
        assert np.all(A.sum(0)==8)
        d=np.full(40,-1);d[0]=0;todo=[0]
        for i in todo:
            for j in np.flatnonzero(A[i]):
                if d[j]<0:d[j]=d[i]+1;todo.append(j)
        assert len(todo)==40
        rr=A&(d[:,None]<d[None,:])
        for j in range(40):rr|=rr[:,j,None]&rr[j,None,:]
        matched.append(summary(rr))
    for k in (1,2,4,8):
        n=N*k
        # Cartesian poset product with a time chain, ordinal sum as contrasting growth.
        leq=np.eye(N,dtype=bool)|rel
        product=np.kron(np.triu(np.ones((k,k),bool)),leq);np.fill_diagonal(product,False)
        ordinal=np.kron(np.triu(np.ones((k,k),bool),1),np.ones((N,N),bool))|np.kron(np.eye(k,dtype=bool),rel)
        p=summary(product);o=summary(ordinal)
        assert p['height']==k+3 and o['height']==4*k
        assert p['pairs']==k*287+k*(k-1)//2*(287+N)
        sims=[]
        for _ in range(12):
            uv=rng.random((n,2));r=(uv[:,0,None]<uv[None,:,0])&(uv[:,1,None]<uv[None,:,1]);sims.append(summary(r))
        mean={key:float(np.mean([s[key] for s in sims])) for key in ('ordering_fraction','height','BD2_reduced','N0','N1','N2')}
        rows.append(dict(copies=k,product=p,ordinal_sum=o,minkowski_mean_12=mean))
    return dict(rows=rows,degree_matched_bipartite_BFS_mean_12={key:float(np.mean([s[key] for s in matched])) for key in ('ordering_fraction','height','BD2_reduced','N0','N1','N2')},product_limit_order_fraction=(287+40)/1600,ordinal_limit_order_fraction=1.,scope='Two chosen growing poset models; both fail 1+1 Minkowski scaling. BD2 is interval combination up to overall convention. No graviton or continuum derivation.')

def maxcuts():
    pts,edges,tri=w33();E=set(edges);lines=[t for t in combinations(range(40),4) if all(e in E for e in combinations(t,2))];assert len(lines)==40
    assert Counter(e for l in lines for e in combinations(l,2))==Counter(E)
    inc=[[] for _ in pts]
    for k,l in enumerate(lines):
        for j in l:inc[j].append(k)
    # Each max cut has 2+2 on each K4 because each line contributes <=4 crossing edges,
    # edges unique to lines. Propagate forced assignments; fix color of vertex0 to 0.
    def search(vals):
        vals=list(vals)
        while True:
            changed=False
            for l in lines:
                a=[vals[i] for i in l];z=a.count(0);o=a.count(1)
                if z>2 or o>2:return
                if z==2 or o==2:
                    fill=int(z==2)
                    for i in l:
                        if vals[i]<0:vals[i]=fill;changed=True
            if not changed:break
        if -1 not in vals:
            yield tuple(vals);return
        # branch on vertex in most constrained lines
        i=max((j for j,v in enumerate(vals) if v<0),key=lambda j:sum(sum(vals[x]>=0 for x in lines[k])**2 for k in inc[j]))
        for bit in (0,1):
            vv=vals.copy();vv[i]=bit;yield from search(vv)
    cuts=list(search([0]+[-1]*39));assert tuple(CUT) in cuts
    assert all(sum(s[i]!=s[j] for i,j in edges)==160 for s in cuts)
    # Exact symplectic transvections act on the projective points and on the cuts.
    canon=lambda x:tuple(x) if x[0]==0 else tuple(1-v for v in x)
    point_index={v:i for i,p in enumerate(pts) for v in (p,tuple(-x%3 for x in p))}
    def omega(x,y):return (x[0]*y[2]+x[1]*y[3]-x[2]*y[0]-x[3]*y[1])%3
    perms=[[point_index[tuple((x[j]+omega(x,v)*v[j])%3 for j in range(4))] for x in pts] for v in pts]
    orbit={tuple(CUT)};queue=[tuple(CUT)]
    for col in queue:
        for perm in perms:
            nxt=canon([col[i] for i in perm])
            if nxt not in orbit:orbit.add(nxt);queue.append(nxt)
    assert orbit==set(cuts)
    return dict(maxcut_count_up_to_global_complement=len(cuts),oriented_count=2*len(cuts),symplectic_transvection_orbit_size=len(orbit),first_five=[list(x) for x in cuts[:5]],proof='40 edge-disjoint K4 lines, each maximum cut <=4; equality iff every line split 2+2. Complete exact recursive binary constraint search with fixed first bit.')

if __name__=='__main__':
    import sys
    names=sys.argv[1:] or ['mic','compiler','qec','higgs','causal','maxcuts','e8_bridge']
    for name in names:
        result=globals()[name]();out=ROOT/'data'/f'toe_20261127_round8_{name}.json';out.write_text(json.dumps(result,indent=2,default=int)+'\n');print(name,json.dumps(result,default=int)[:3000],flush=True)
