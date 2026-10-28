"""Five independent follow-ups; exact patch gap, supplied matter and radion controls.

Owners: Oct27 certified_rotor_bounds and native_operator_closure; Pass12002
path overlap; Pass12311 mass pairing. No continuum TOE completion is claimed.
"""
from pathlib import Path
from itertools import product, combinations
from fractions import Fraction as F
import json, sys, re
import numpy as np
import sympy as s
from scipy.sparse import coo_matrix, kron, eye, diags
from scipy.sparse.linalg import eigsh, LinearOperator, cg
from scipy.linalg import expm, block_diag
from scipy.optimize import brentq, linprog
import mpmath as mp
sys.path.insert(0,str(Path(__file__).resolve().parent))
import w33_20261027_certified_rotor_bounds as rotor
import w33_20261027_native_operator_closure as native
import w33_pass12002_native_path_overlap as pathop
ROOT=Path(__file__).resolve().parents[1]


def gap_certificate(d=6):
    C,_,_=rotor.old.lifted_patch(d);G=s.Matrix(C@C.T);vmax=max(G.inv()[i,i]for i in range(d))
    shell=list(product(range(-2,3),repeat=d));values=[sum(m[i]*int(G[i,j])*m[j]for i in range(d)for j in range(d))for m in shell]
    shortest=min(x for x in values if x);outside=9/vmax
    assert shortest==12 and outside>shortest
    previous=json.loads((ROOT/'data/w33_20261027_certified_rotor_bounds.json').read_text())
    rec=next(x for x in previous['controls']if x['loops']==d and x['cutoff']==(2 if d==6 else 3))
    A,den,_,_,states=rotor.integer_operator(d,rec['cutoff']);idx={m:i for i,m in enumerate(states)}
    p=list(map(int,rec['strictly_positive_integer_test_vector']))
    even=[p[i]+p[idx[tuple(-x for x in m)]]for i,m in enumerate(states)]
    # A simple odd vector is an exact second variational direction. No Ritz
    # excited-state output enters the certificate.
    v=[0]*len(states);m=next(m for m,z in zip(shell,values)if z==shortest)
    v[idx[m]]=1;v[idx[tuple(-x for x in m)]]=-1
    def ray(x):
        hx=[sum(int(A.data[k])*x[int(A.indices[k])]for k in range(A.indptr[i],A.indptr[i+1]))for i in range(len(x))]
        return F(sum(a*b for a,b in zip(x,hx)),den*sum(a*a for a in x)),hx
    upper0,hp=ray(even);upper1,hv=ray(v)
    assert sum(a*b for a,b in zip(even,v))==sum(a*b for a,b in zip(even,hv))==0
    assert upper1>upper0
    lower0=s.sympify(rec['infinite_ground_lower_exact']);lowergap=s.Rational(6)-s.Rational(upper0.numerator,upper0.denominator)
    return dict(loops=d,gram=[[int(x)for x in row]for row in G.tolist()],shortest_norm=shortest,
        shortest_vectors=[list(m)for m,z in zip(shell,values)if z==shortest],outside_box_norm_lower=str(outside),
        first_excited_interval=[6.,float(upper1)],first_excited_upper_exact=str(upper1),ground_upper_exact=str(upper0),
        gap_lower_exact=str(lowergap),gap_interval=[float(lowergap),float(s.Rational(upper1.numerator,upper1.denominator)-lower0)],
        proof='Cauchy-Schwarz bounds every vector outside [-2,2]^d; exhaustive integer arithmetic inside gives min nonzero mGm=12. V>=0 implies lambda1(H)>=lambda1(T)=6 by min-max. The previously certified trial vector symmetrized under m->-m gives E0<=b. An odd two-delta vector is orthogonal both in norm and Hamiltonian form, so its Rayleigh quotient bounds lambda1 above.',
        scope='Infinite electric-flux Hilbert space on a finite spatial patch, g=1 and supplied positive potential. Not an infinite-volume physical mass gap.')


def kinetic(cells=1):
    B,V,edges,_=native.geometry();n=27*cells;rr=[];cc=[]
    for c in range(cells):
        for e,(a,b)in enumerate(edges):
            u=c*27+a;v=((c+int(V[e,0]))%cells)*27+b
            rr.extend([v,u]);cc.extend([u,v])
    K=coo_matrix((-np.ones(len(rr)),(rr,cc)),shape=(n,n)).tocsr()
    return K


def translated_response(U=2.):
    K=kinetic(2);n=K.shape[0];N=n*n
    H=kron(K,eye(n))+kron(eye(n),K)+diags([U if a==b else 0 for a in range(n)for b in range(n)])
    ev,Q=eigsh(H,k=2,which='SA',tol=1e-11,v0=np.ones(N));psi=Q[:,0];E0=ev[0]
    B,V,edges,h= native.geometry();rng=np.random.default_rng(271027);chi=rng.normal(size=n)
    vertices=[];contacts=np.zeros((9,9));P=psi.reshape(n,n)
    # Four deck twists, four harmonic representatives, one gauge derivative.
    for c in range(2):
        for e,(a,b)in enumerate(edges):
            u=c*27+a;v=((c+int(V[e,0]))%2)*27+b
            alpha=np.r_[V[e],h[e],chi[v]-chi[u]]
            contact=2*(P[v]@P[u]+P[:,v]@P[:,u])
            contacts+=contact*np.outer(alpha,alpha)
    for j in range(9):
        J=np.zeros((n,n),complex)
        for c in range(2):
            for e,(a,b)in enumerate(edges):
                u=c*27+a;v=((c+int(V[e,0]))%2)*27+b
                alpha=V[e,j]if j<4 else(h[e,j-4]if j<8 else chi[v]-chi[u])
                J[v,u]+=-1j*alpha;J[u,v]+=1j*alpha
        vertices.append((J@P+P@J.T).ravel())
    mat=H.tocsr().astype(complex)
    A=LinearOperator((N,N),matvec=lambda x:mat@x-E0*x+psi*np.vdot(psi,x),dtype=complex)
    inv=[];inv2=[];residuals=[]
    for b in vertices:
        b=b-psi*np.vdot(psi,b);x,info=cg(A,b,rtol=1e-11,maxiter=3000);assert info==0
        y,info=cg(A,x,rtol=1e-11,maxiter=3000);assert info==0
        residuals.append(float(np.linalg.norm(A@x-b)));inv.append(x);inv2.append(y)
    static=contacts-2*np.real(np.array([[np.vdot(a,b)for b in inv]for a in vertices]))
    electric=2*np.real(np.array([[np.vdot(a,b)for b in inv2]for a in inv]))
    assert np.max(abs(static[-1]))<1e-7
    assert np.max(abs(static[:4,:4]-static[4:8,4:8]))<1e-7
    target=h.T@h
    def fit(K):
        scale=float(np.sum(K*target)/np.sum(target*target))
        return dict(scale=scale,relative_Frobenius_error=float(np.linalg.norm(K-scale*target)/np.linalg.norm(K)))
    return dict(cells=2,vertices=n,links=270,sector='one up + one down',dimension=N,U=U,
        energies=ev.tolist(),ground_residual=float(np.linalg.norm(H@psi-E0*psi)),
        static_twist_and_gauge_kernel=static.tolist(),electric_twist_and_gauge_kernel=electric.tolist(),
        probe_order='deck V[0:4], physical harmonic h[4:8], gauge[8]',
        static_Ward_error=float(np.max(abs(static[-1]))),resolvent_residuals=residuals,
        static_harmonic_metric_fit=fit(static[4:8,4:8]),electric_harmonic_metric_fit=fit(electric[4:8,4:8]),
        scope='Periodic two-cell cover in first primitive direction. External gauge response, fixed particle sector; no thermodynamic or dynamical-gauge limit.')


def larger_sector(U=2.):
    K=kinetic();pairs=list(combinations(range(27),2));where={p:i for i,p in enumerate(pairs)};rr=[];cc=[];vv=[]
    for i,p in enumerate(pairs):
        for a in p:
            for b in K[:,a].nonzero()[0]:
                if b in p:continue
                target=tuple(sorted((set(p)-{a})|{int(b)}));sign=(-1)**sum(min(a,b)<x<max(a,b)for x in p)
                rr.append(where[target]);cc.append(i);vv.append(-sign)
    Kup=coo_matrix((vv,(rr,cc)),shape=(len(pairs),len(pairs))).tocsr();assert (Kup-Kup.T).nnz==0
    H=kron(Kup,eye(27))+kron(eye(len(pairs)),K)+diags([U*(b in p)for p in pairs for b in range(27)])
    ev,Q=eigsh(H,k=24,which='SA',tol=1e-10,v0=np.random.default_rng(27).normal(size=H.shape[0]))
    mult=int(sum(abs(ev-ev[0])<1e-7))
    return dict(sector='two up + one down',dimension=H.shape[0],U=U,lowest_24_energies=ev.tolist(),
        observed_ground_multiplicity_in_Ritz_sample=mult,max_Ritz_residual=float(max(np.linalg.norm(H@Q[:,i]-ev[i]*Q[:,i])for i in range(24))),
        response_status='Unique-ground Kubo formula deliberately not applied to a degenerate multiplet. Multiplicity is numerical and not certified.')


def nonabelian_heavy_frame():
    rng=np.random.default_rng(1200227);shifts=[]
    for _ in range(4):
        X=rng.normal(size=(5,5))+1j*rng.normal(size=(5,5));X=(X+X.conj().T)/2;X-=np.trace(X)*np.eye(5)/5
        shifts.append(expm(.3j*X))
    bridge=native.canonical_cubic_intertwiner();Smap=np.array(bridge['canonical_to_SU5_signed_permutation'])
    def rep27(U):return Smap.T@block_diag(native.old.wedge2(U),U.conj(),np.eye(1),U,U.conj(),np.eye(1))@Smap
    records=[]
    for name,S in [('5',shifts),('10',[native.old.wedge2(U)for U in shifts]),('canonical27',[rep27(U)for U in shifts])]:
        D,G5=pathop.wilson(S);F0,E,gap=pathop.heavy_frame(D,G5,4.,steps=24)
        P,_=pathop.projector(G5@(D+4*np.eye(len(D))))
        X=rng.normal(size=(5,5))+1j*rng.normal(size=(5,5));X=(X+X.conj().T)/2;X-=np.trace(X)*np.eye(5)/5
        g=expm(.5j*X);g=g if name=='5'else(native.old.wedge2(g)if name=='10'else rep27(g))
        G=np.kron(np.eye(4),g);Fg,_,_=pathop.heavy_frame(G.conj().T@D@G,G5,4.,steps=24)
        covariance=np.max(abs(Fg-G.conj().T@F0@(E.conj().T@G@E)))
        records.append(dict(representation=name,dimension=len(D),gap=gap,projector_error=float(np.max(abs(F0@F0.conj().T-P))),gauge_covariance_error=float(covariance)))
    edges,V,paths,tree,T,words=pathop.native_paths();R=max(len(w)+2*len(p)for w in words for p in paths.values());degree=np.zeros(27,int)
    for e in tree:
        a,b=edges[e];degree[a]+=1;degree[b]+=1
    kappa=4*27**2;coefficient=8*R+2*kappa*int(max(degree));epsilon=F(1,4*coefficient)
    # Noncommuting pullback transports on ALL135 actual native links.
    links=[]
    for _ in edges:
        X=rng.normal(size=(5,5))+1j*rng.normal(size=(5,5));X=(X+X.conj().T)/2;X-=np.trace(X)*np.eye(5)/5
        links.append(expm(.2j*X))
    def walk(a,word):
        U=np.eye(5,dtype=complex)
        for e,sgn in word:
            u,v=edges[e];assert a==(u if sgn>0 else v)
            U=U@(links[e]if sgn>0 else links[e].conj().T);a=v if sgn>0 else u
        return a,U
    transports=[walk(0,paths[a])[1]for a in range(27)];Ut=block_diag(*transports)
    shifts=[];rootloops=[]
    for word in words:
        end,C=walk(0,word);assert end==0;rootloops.append(C);blocks=[]
        for a in range(27):
            p=paths[a];rev=[(e,-sgn)for e,sgn in reversed(p)]
            end,U=walk(a,rev+word+p);assert end==a;blocks.append(U)
        shifts.append(block_diag(*blocks))
    lap=np.zeros((135,135),complex);L0=np.zeros((27,27))
    for e in tree:
        a,b=edges[e];aa=slice(5*a,5*a+5);bb=slice(5*b,5*b+5)
        lap[aa,aa]+=np.eye(5);lap[bb,bb]+=np.eye(5);lap[aa,bb]-=links[e];lap[bb,aa]-=links[e].conj().T
        L0[a,a]+=1;L0[b,b]+=1;L0[a,b]-=1;L0[b,a]-=1
    factor_error=max(np.max(abs(U-Ut.conj().T@np.kron(np.eye(27),C)@Ut))for U,C in zip(shifts,rootloops))
    tree_error=np.max(abs(lap-Ut.conj().T@np.kron(L0,np.eye(5))@Ut))
    assert max(factor_error,tree_error)<1e-11
    # Representation checks for Craig2026 Proposition11.1, not a verification
    # of its analytic/global proof or implementation of its measure current.
    t=s.Symbol('t',nonzero=True);fund=[t,1/t,s.Integer(1),s.Integer(1),s.Integer(1)]
    wedge=[a*b for a,b in combinations(fund,2)];character=s.expand(sum(wedge)+sum(fund)+2*sum(1/a for a in fund)+2)
    assert s.expand(character-(6*t+6/t+15))==0
    cartan=[1,1,1,1,-4];fundtrace=sum(x**3 for x in cartan);wedgetrace=sum((a+b)**3 for a,b in combinations(cartan,2))
    cubic_trace=wedgetrace-fundtrace+fundtrace-fundtrace;assert cubic_trace==0
    acoustic=dict(SU2_character=str(character),doublet_multiplicity=6,singlet_multiplicity=15,
        fundamental_Cartan_cubic_trace=fundtrace,wedge2_Cartan_cubic_trace=wedgetrace,total_cubic_trace=cubic_trace,
        cubic_anomaly_reason='SU5 has a unique cubic invariant; comparison on diag(1,1,1,1,-4) gives anomaly coefficients10=1,5=1,bar5=-1. The complete27 has10+bar5+1+5+bar5+1, total0.',
        theorem_hypotheses_checked='Cubic SU5 anomaly cancels and standard embedded SU2 has6 doublets, no higher half-integer irreps. Supply common real spin boundary signs. These meet the representation conditions of Craig2026 Proposition11.1.',
        conditional_reduction='If Proposition11.1 and all its admissibility/reconstruction hypotheses hold for the coarse Wilson mass-one operator, its acoustic measure pulls back through the bounded native root paths; combine with the heavy frame. Choose native link neighborhood small enough that every coarse root plaquette is admissible, in addition to the explicit gap radius.',
        not_completed='No independent proof audit of Craig2026, acoustic current implementation, native plaquette-admissible domain across all topological sectors, or nearest-edge reduction.',
        primary='https://arxiv.org/html/2610.09093v1#S11.SS1')
    return dict(samples=records,native_SU5_transport_factorization_error=float(factor_error),native_SU5_tree_factorization_error=float(tree_error),native_transport_links_tested=135,
        acoustic_measure_representation_checks=acoustic,
        heavy_gap_lower_all_unitary_links=3,native_range=R,optical_coefficient=kappa,
        weak_representation_link_norm_radius_exact=str(epsilon),weak_fundamental_SU5_link_norm_radius_for_all27_exact=str(epsilon/2),
        full_norm_upper=7+2*kappa*int(max(degree)),uniform_weak_field_gap_lower=.75,
        proof='Each directional mass-zero Wilson term is I-(Pminus T+Pplus Tdagger), accretive since the parenthesized matrix is unitary. Thus Re[(shift-1)I+t DW0]>=3I for shift>=4. Hermitian gamma5 times this matrix has singular gap>=3. The onsite projector and canonical gapped homotopy define a global gauge-covariant Kato frame, now also for noncommuting unitary representation links.',
        locality='Pass12002 finite native paths, norm and weak-field gap argument extends with operator norms. For representation links ||U-I||<=epsilon=1/(4*(8R+2*kappa*degree)), the same telescoping bounds give acoustic/full gap>=3/4 uniformly in volume. This uses the path/tree regulator.',
        boundary='Heavy frame explicit; acoustic measure has a conditional reduction to Craig2026 after exact representation checks, not an independently verified or implemented current. Nearest-edge all-volume locality remains unproved. Heavy samples are coarse one-cell controls; native path/tree factorization is also tested on all135 links.',prior_owner='Pass12002; HJL hep-lat/9808010')


def radion():
    mp.mp.dps=40;z=mp.zeta(5);out=[]
    def shape(x):return mp.polylog(5,mp.exp(-x))+x*mp.polylog(4,mp.exp(-x))+x*x/3*mp.polylog(3,mp.exp(-x))
    for p in (4,6):
        def D(x):return p*shape(x)+x*x/3*(mp.polylog(3,mp.exp(-x))+x*mp.polylog(2,mp.exp(-x)))
        root=mp.findroot(lambda x:D(x)-p*z/2,(1,5));curvature=-4*mp.diff(D,root)/root**(p+1)
        assert curvature>0
        out.append(dict(power=p,frame='four-dimensional Einstein'if p==6 else'Jordan',x_root=str(root),R_times_mass=str(root/(2*mp.pi)),dimensionless_potential=str((4*shape(root)-2*z)/root**p),positive_second_derivative=str(curvature)))
    return dict(samples=out,shape='S(x)=Li5(exp(-x))+x Li4(exp(-x))+x^2 Li3(exp(-x))/3; x=2pi*m*R',
        supplied_content='One periodic massive Dirac field (weight +4), two massless real bosons (weight -2). V proportional to (4S(x)-2zeta(5))/x^p. Overall positive normalization omitted.',
        proof='Dp=pS-xSprime decreases strictly: termwise derivative is -exp(-y)*y*((p-2)*(1+y)+y^2)/(3*n^4), y=nx. It runs from p*zeta(5) to 0. Thus Dp=p*zeta(5)/2 has exactly one root; Vprime changes from negative to positive and Vsecond=-4 Dpprime/x^(p+1)>0. V diverges positively at zero and approaches zero negatively at infinity, proving a unique global minimum.',
        boundary='Standard massive Casimir mechanism; supplied fields, mass and boundary conditions. Radius scales as 1/m; negative vacuum energy, gravitational backreaction and native matter origin unresolved.',primary='https://arxiv.org/abs/hep-ph/0105021')


def representation_thresholds():
    path=ROOT/'analysis/search_drivers_12281/bro/Z6II_60_SM_20260917_810_v9__w6odd.nsoq'
    sys.path.insert(0,str(ROOT/'analysis/search_drivers_12286'));from lr_hypercharge import solve,fermions
    c,eq,sol=solve(fermions(path));ss=sol[0];free=sorted((set(c)-set(ss))|{z for v in ss.values()for z in s.sympify(v).free_symbols},key=str)
    cv=[s.sympify(ss.get(ci,ci)).subs(free[0],s.Rational(-1,148))for ci in c];groups={}
    for line in path.read_text().splitlines():
        m=re.match(r'FIELD \d+ m=(\S+) k=\S+ mm=\S+ n=\S+ lat=\S+ dim=(\S*) q=(\S*)',line)
        if not m or int(m[1])not in (19,15,16):continue
        kind=int(m[1]);d3,dl,dr,dh=[abs(int(re.match(r'-?\d+',x)[0]))for x in m[2].split(',')]
        q=[s.nsimplify(float(x),tolerance=1e-9,rational=True)for x in m[3].split(',')if x];y=sum(a*b for a,b in zip(cv,q))
        for t in ([s.Rational(1,2),-s.Rational(1,2)]if dr==2 else[0]):
            key=('W'if kind==19 else'S',d3,dl,abs(y+t));factor=s.Rational(2,3)if kind==19 else s.Rational(1,6)
            beta=factor*dh*s.Matrix([{1:0,3:s.Rational(1,2),8:3}[d3]*dl,{1:0,2:s.Rational(1,2),3:2}[dl]*d3,(y+t)**2*d3*dl])
            groups[key]=groups.get(key,s.zeros(3,1))+beta
    light={('W',3,2,s.Rational(1,6)):[2,3,s.Rational(1,3)],('W',3,1,s.Rational(2,3)):[1,0,s.Rational(8,3)],('W',3,1,s.Rational(1,3)):[1,0,s.Rational(2,3)],('W',1,2,s.Rational(1,2)):[0,1,1],('W',1,1,s.Integer(1)):[0,0,2],('S',1,2,s.Rational(1,2)):[0,s.Rational(1,6),s.Rational(1,6)]}
    for key,v in light.items():groups[key]-=s.Matrix(v)
    groups={k:v for k,v in groups.items()if any(v)};assert all(x>=0 for v in groups.values()for x in v)
    beta=list(groups.values());full=s.Matrix([7,16,s.Rational(148,3)]);A=s.Matrix([1/s.Rational('.118'),s.Rational('127.95')*s.Rational('.2312'),s.Rational('127.95')*(1-s.Rational('.2312'))])
    variables=s.symbols('x:'+str(1+len(beta)));inv=A-full*variables[0]
    for b,t in zip(beta,variables[1:]):inv+=b*t
    mat,rhs=s.linear_eq_to_matrix([inv[1]-inv[0],inv[2]-s.Rational(8,3)*inv[1]],variables)
    lower=np.log(1e3/91.1876)/(2*np.pi);upper=np.log(1e16/91.1876)/(2*np.pi);yc=np.log(1e19/91.1876)/(2*np.pi)
    aub=np.zeros((len(beta)+1,len(variables)));bub=np.zeros(len(beta)+1)
    for i in range(len(beta)):aub[i,0]=-1;aub[i,i+1]=1
    aub[-1]=[-float(inv[1].coeff(t))for t in variables];bub[-1]=float(A[1]-1)
    # Maximize a common margin before reconstructing an exact rational point.
    # Every mass stays strictly above 1TeV and below the crossing at this point.
    bounds=[(lower,yc)]+[(lower,upper)]*len(beta)
    aa=[np.r_[row,1.]for row in aub];bb=list(bub)
    for i,(lo,hi)in enumerate(bounds):
        row=np.zeros(len(variables)+1);row[i]=-1;row[-1]=1;aa.append(row);bb.append(-lo)
        row=np.zeros(len(variables)+1);row[i]=1;row[-1]=1;aa.append(row);bb.append(hi)
    objective=np.zeros(len(variables)+1);objective[-1]=-1
    result=linprog(objective,A_ub=aa,b_ub=bb,A_eq=np.column_stack((np.array(mat,float),np.zeros(2))),b_eq=np.array(rhs,float).ravel(),bounds=bounds+[(0,None)],method='highs')
    record=dict(groups=[dict(representation=list(map(str,k)),beta=list(map(str,v)))for k,v in groups.items()],feasible=bool(result.success),message=result.message,
        prior_pairing=json.loads((ROOT/'analysis/search_drivers_12311/vacuum.json').read_text()),
        boundary='Independent SM representation thresholds only; frozen one-loop inputs and kY=8/3. Not full left-right matching, two-loop running, a shared singlet vacuum or generated mass matrix. Pass12311 matching permits pair operators but does not fix their masses.')
    assert sum(beta,s.zeros(3,1))==s.Matrix([14,s.Rational(115,6),s.Rational(85,2)])
    if result.success:
        pivots=mat.rref()[1];freecols=[i for i in range(len(variables))if i not in pivots]
        exact=s.zeros(len(variables),1)
        for i in freecols:exact[i]=s.Rational(float(result.x[i])).limit_denominator(10**8)
        remaining=rhs-mat*exact;solution=mat[:,list(pivots)].inv()*remaining
        for i,z in zip(pivots,solution):exact[i]=z
        assert mat*exact==rhs
        vals=np.array(exact,float).ravel();aval=A-full*exact[0]
        for b,t in zip(beta,exact[1:]):aval+=b*t
        assert aval[0]==aval[1]and aval[2]==s.Rational(8,3)*aval[1]and aval[1]>1
        assert max(aub@vals-bub)<0 and all(lo<x<hi for (lo,hi),x in zip(bounds,vals))
        assert all(1<t<4 for t in exact[1:])and 4<exact[0]<5
        # Strict mass-domain control using only rational inequalities:
        # 3<pi<22/7 and e<3; exp(6)>1+6+18=25.
        mass_domain=dict(exact_log_relations='1<t_j<4<y<5',
            threshold_lower_GeV=str(s.Rational('91.1876')*25),
            threshold_upper_GeV=str(s.Rational('91.1876')*3**26),
            crossing_upper_GeV=str(s.Rational('91.1876')*3**32),
            proof='3<pi<22/7, e<3 give Mj>91.1876*(1+6+18)>1000, Mj<91.1876*3^26<1e16, Mcross<91.1876*3^32<1e19. Exact t_j<y gives thresholds below crossing.')
        assert s.Rational(mass_domain['threshold_lower_GeV'])>1000 and s.Rational(mass_domain['threshold_upper_GeV'])<10**16 and s.Rational(mass_domain['crossing_upper_GeV'])<10**19
        record.update(exact_log_thresholds=list(map(str,exact)),exact_inverse_couplings=list(map(str,aval)),LP_margin=float(result.x[-1]),
            exact_mass_domain_certificate=mass_domain,
            log_thresholds=vals.tolist(),matching_residual=float(np.max(abs(np.array(mat,float)@vals-np.array(rhs,float).ravel()))),inequality_violation=float(max(aub@vals-bub)),thresholds_GeV=(91.1876*np.exp(2*np.pi*vals[1:])).tolist(),crossing_GeV=float(91.1876*np.exp(2*np.pi*vals[0])))
    return record


def run():
    return dict(schema='native_gap_matter_radion_followups_v1',rotor=[gap_certificate(3),gap_certificate(6)],heavy_measure=nonabelian_heavy_frame(),translated_matter=translated_response(),translated_matter_controls=[translated_response(U)for U in (0.,8.)],larger_particle_sector=larger_sector(),massive_radion=radion(),representation_thresholds=representation_thresholds())


if __name__=='__main__':
    result=run();(ROOT/'data/w33_20261027_gap_matter_radion.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
