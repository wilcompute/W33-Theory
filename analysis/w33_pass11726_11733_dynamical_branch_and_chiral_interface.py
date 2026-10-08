"""Eight finite interface experiments; no claim of a completed physical TOE.

11721-25 owns the actual E8 principal embedding and mixed invariant;
11271 owns the symmetric-family Yukawa operator; 11301 owns the finite
Leibniz obstruction. Classical orbit, index, conformal and tensor-product
theorems are explicitly imported, not claimed as new mathematics.
"""
from __future__ import annotations
from collections import Counter
from functools import lru_cache
import itertools as it
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
import sympy as s
from scipy.optimize import root

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11721_11725_coherent_vacuum_gauge_bridge as B
E=B.E
OUT=ROOT/'data/w33_pass11726_11733_dynamical_branch_and_chiral_interface.json'


@lru_cache(None)
def roots():
    """240 roots in the sl9 Cartan, coordinates multiplied by3."""
    labels=[];weights=[]
    for i,j in it.permutations(range(9),2):
        w=np.zeros(9,dtype=int);w[i]=3;w[j]=-3
        labels.append(('A',i,j));weights.append(tuple(w))
    for kind,sign in [('x',1),('k',-1)]:
        for t in E.TR:
            w=-np.ones(9,dtype=int);w[list(t)]+=3
            labels.append((kind,*t));weights.append(tuple(sign*w))
    assert len(set(weights))==240 and all(sum(x*x for x in w)==18 for w in weights)
    return labels,weights,{w:i for i,w in enumerate(weights)}


def orbit_certificate():
    labels,weights,_=roots()
    rho=np.diag([s.Rational(8,9)]+[s.Rational(-1,9)]*8)
    # Charges of the actual bracket [rho, root], not graph adjacency.
    charges=Counter(s.Rational(w[0],3) for w in weights)
    assert charges=={s.Integer(0):56,s.Integer(1):8,s.Integer(-1):8,
                    s.Rational(2,3):28,s.Rational(-2,3):28,
                    s.Rational(1,3):56,s.Rational(-1,3):56}
    h=(np.array(rho,dtype=complex),np.zeros(84),np.zeros(84))
    x=E._zero();x[1][E.TI[(0,1,2)]]=1
    compact=B.scale(1/np.sqrt(2),B.add(x,B.star(x)))
    tangent=B.scale(1j,E.bracket(compact,h))
    assert np.linalg.norm(tangent[1])>0 and np.linalg.norm(tangent[2])>0
    # Compact E8 transport leaves the norm fixed but exits the sl9 slice.
    theta=.23;transport=h;term=h
    for n in range(1,24):
        term=B.scale(1j*theta/n,E.bracket(compact,term));transport=B.add(transport,term)
    norm=lambda a:float(np.vdot(E._vec(a),E._vec(a)).real)
    assert abs(norm(transport)-norm(h))<1e-12
    assert np.linalg.norm(transport[1])>.01
    # KKS periods: rho pairs with all coroots in thirds, so the minimal
    # integral level is3 (in the standard long-root norm2 convention).
    positives=[w for w in weights if w[0]>0 or (w[0]==0 and sum(i*w[i] for i in range(9))>0)]
    positive_set=set(positives)
    simple=[w for w in positives if not any(tuple(x-y for x,y in zip(w,v)) in positive_set for v in positives)]
    assert len(positives)==120 and len(simple)==8
    dynkin=sorted(int(w[0]) for w in simple)
    assert dynkin==[0]*7+[1]
    twice_delta_times3=[sum(w[i] for w in positives) for i in range(9)]
    dimension=s.Integer(1)
    for w in positives:
        denominator=s.Rational(sum(x*y for x,y in zip(twice_delta_times3,w)),18)
        assert denominator>0
        dimension*=1+s.Rational(int(w[0]))/denominator
    assert dimension==147250
    casimir=8+int(twice_delta_times3[0])
    assert casimir==144
    return dict(status='PASS',root_charge_multiplicities={str(k):v for k,v in charges.items()},
        stabilizer_Lie_algebra='su8+u1',stabilizer_dimension=64,real_orbit_dimension=184,
        SU9_ray_fiber_real_dimension=16,E8_SU9_base_real_dimension=168,
        associated_bundle='E8 x_(SU9/Z3) CP8 -> E8/(SU9/Z3)',
        explicit_map='[g,[psi]] -> Ad_g(psi psi_dagger-I9/9)',
        projective_center_descent=True,compact_transport_norm_residual=abs(norm(transport)-norm(h)),
        leaves_sl9_slice=True,
        KKS_quantization={'minimal_integral_level':3,'highest_weight':'3rho=(8/3,-1/3,...,-1/3)',
                          'highest_weight_norm_squared':8,'simple_root_Dynkin_labels_sorted':dynkin,
                          'holomorphic_orbit_quantization_dimension':int(dimension),'quadratic_Casimir':casimir,
                          'boundary':'Classical compact-orbit geometric quantization at supplied hbar and KKS normalization; this is not a fundamental9, a predicted particle multiplet or a claim that147250 physical states are observed.'},
        scope='A well-defined E8-equivariant orbit extension of the density, not an E8 fundamental9. An E8-invariant function on this transitive orbit is constant; the Pauli-dependent S4 selector requires an additional moving frame.')


def partitions(n,minimum=1):
    if not n:yield ();return
    for j in range(minimum,n+1):
        for tail in partitions(n-j,j):yield (j,*tail)


def su2_generators(parts):
    n=sum(parts);Jz=np.zeros((n,n));Jp=np.zeros((n,n));offset=0
    for d in parts:
        j=(d-1)/2
        for k in range(d):Jz[offset+k,offset+k]=j-k
        for k in range(d-1):Jp[offset+k,offset+k+1]=np.sqrt((k+1)*(d-1-k))
        offset+=d
    return [(Jp+Jp.T)/2,(Jp-Jp.T)/(2j),Jz]


def clock_classes():
    rows=[]
    for n0 in range(6):
        for n1 in range(6-n0):
            n2=5-n0-n1
            if (n1+2*n2)%3:continue
            re=s.Rational(3*n0-5,2);im2=s.Rational(3,4)*(n1-n2)**2
            rows.append(dict(multiplicities=[n0,n1,n2],Re_trace=str(re),Im_trace_squared=str(im2),
                             energy_a1_b1=str(-im2-re),centralizer_dimension=n0*n0+n1*n1+n2*n2-1))
    return rows


@lru_cache(None)
def branch_certificate():
    # Inverse-Casimir auxiliary excludes zero without prescribing its radius.
    rows=[]
    for p in partitions(5):
        Js=su2_generators(p);C=sum(j@j for j in Js)
        t=float((np.trace(C)/np.trace(C@C)).real) if np.trace(C@C).real>0 else 0
        residual=float(np.linalg.norm(t*C-np.eye(5))**2)
        c=[s.Rational(d*d-1,4) for d in p for _ in range(d)]
        S1=sum(c);S2=sum(x*x for x in c)
        exact_residual=5-S1*S1/S2 if S2 else s.Integer(5)
        assert abs(residual-float(exact_residual))<1e-12
        rows.append(dict(partition=list(p),inverse_Casimir_residual=residual,
                         exact_inverse_Casimir_residual=str(exact_residual),
                         auxiliary_t=str(s.Rational(float(t)).limit_denominator(100000))))
    assert [r['partition'] for r in rows if r['inverse_Casimir_residual']<1e-12]==[[5]]
    cs=clock_classes();best=min(s.Rational(r['energy_a1_b1']) for r in cs)
    winners=[r['multiplicities'] for r in cs if s.Rational(r['energy_a1_b1'])==best]
    assert winners==[[2,0,3],[2,3,0]]
    C,_,_,_=B.adjoint_kinetics()
    vals,Q=np.linalg.eigh(C);P0=Q[:,abs(vals)<1e-8]@Q[:,abs(vals)<1e-8].conj().T
    P2=Q[:,abs(vals-2)<1e-8]@Q[:,abs(vals-2)<1e-8].conj().T
    assert round(np.trace(P0).real)==24 and round(np.trace(P2).real)==33
    _,weights,_=roots();errors=[]
    for row in cs:
        n0,n1,n2=row['multiplicities'];levels=[0]*n0+[1]*n1+[2]*n2
        ex=np.zeros(9,dtype=int);ex[B.F5]=levels
        labels,_,_=roots()
        ph=[]
        for lab in labels:
            q=ex[lab[1]]-ex[lab[2]] if lab[0]=='A' else sum(ex[list(lab[1:])])*(1 if lab[0]=='x' else -1)
            ph.append(B.V.W**q)
        U=np.diag([*ph[:72],*([1]*8),*ph[72:]])
        R=(np.trace(P2@U).real-3)/6
        I2=np.trace(P0@U).real+1-R*R
        errors.append(max(abs(R-float(s.Rational(row['Re_trace']))),abs(I2-float(s.Rational(row['Im_trace_squared'])))))
    assert max(errors)<1e-10
    return dict(status='PASS',all_SU2_partitions=rows,
        branch_action='sum_ab ||[Phi_a,Phi_b]-i epsilon_abc Phi_c||^2+||t sum_a Phi_a^2-I5||^2, supplied compact auxiliary0<=t<=2',
        zero_branch='The unique unitary SU2 representation is the irreducible5; t=1/6 is derived.',
        unbounded_auxiliary_negative_control='Without the supplied compact t domain, Phi=epsilon J,t=1/(6epsilon^2) has energy60epsilon^2(epsilon-1)^2 ->0 at infinity; unique finite zero does not mean a coercive potential.',
        clock_energy='-a (Im Tr5 U)^2-b Re Tr5 U, on U in SU5 with U^3=I',
        exact_open_selection_wedge='b>0 and a>2b/3',all_clock_classes=cs,
        selected_multiplicities=winners,selected_Lie_algebra='su3+su2+u1',
        E8_covariant_clock_contractions='R=(Tr_ad(P2 AdU)-3)/6; B=Tr_ad(P0 AdU)+1-R^2; V=-a B-b R',
        Casimir_projector_ranks={'P0':24,'P2':33},clock_contraction_max_error=max(errors),
        scope='Principal-branch selection in a supplied hidden-SU5 matrix carrier; clock selection on its compact, cubed-identity centralizer sector. This removes the old trace5 target, but the sector constraints, scalar action and coupling wedge are inputs; no full off-constraint E8 polynomial potential is certified.')


def line_spin_cohomology(ns):
    # Spin Dirac = Dolbeault twisted by K^(1/2); each CP1 factor has O(n-1).
    if 0 in ns:return 0,0
    return sum(n<0 for n in ns),abs(int(np.prod(ns)))


def chiral_certificate():
    ns=[(1,1,1),(1,1,-2),(-2,-2,1)]
    assert np.sum(ns,axis=0).tolist()==[0,0,0]
    modes=[line_spin_cohomology(n) for n in ns]
    left=sum(m for q,m in modes if q%2==0);right=sum(m for q,m in modes if q%2)
    x,y,z=s.symbols('x y z');l=[sum(n*v for n,v in zip(t,(x,y,z))) for t in ns]
    c3=s.expand(s.prod(l)).coeff(x,1).coeff(y,1).coeff(z,1)
    assert (left,right,c3)==(5,2,6)
    # A named finite-rank smoothing perturbation, not a local Yukawa solution.
    M=s.Matrix([[0,1,0,0,0],[0,0,0,0,1]])
    assert M.rank()==2 and len(M.nullspace())==3 and len(M.T.nullspace())==0
    anomalies={}
    charges=[(6,s.Rational(1,6),3,2),(3,s.Rational(-2,3),3,1),
             (3,s.Rational(1,3),3,1),(2,s.Rational(-1,2),1,2),(1,s.Integer(1),1,1)]
    anomalies['Y']=sum(d*q for d,q,c,w in charges)
    anomalies['Y3']=sum(d*q**3 for d,q,c,w in charges)
    anomalies['SU3^2_Y']=2*s.Rational(1,6)/2+s.Rational(-2,3)/2+s.Rational(1,3)/2
    anomalies['SU2^2_Y']=3*s.Rational(1,6)/2+s.Rational(-1,2)/2
    assert not any(anomalies.values())
    return dict(status='PASS',supplied_spin_six_manifold='CP1 x CP1 x CP1; not a Calabi-Yau or solved compactification',
        SU3_bundle_line_multidegrees=[list(n) for n in ns],integral_c3=int(c3),Dirac_index=3,
        actual_zero_modes={'positive':left,'negative':right},cohomology_degree_dimension=[list(x) for x in modes],
        smoothing_pair_lift_matrix=[[int(x) for x in row] for row in M.tolist()],remaining_positive_modes=3,
        one_SM_family_anomalies={k:str(v) for k,v in anomalies.items()},SU2_doublets_per_family=4,
        scope='Exact index/cohomology of a supplied split bundle, with a specified nonlocal finite-rank lift leaving3 complex positive Dirac modes. E6 matter requires an additional compactification interpretation; local interactions, stable bundle, ten-dimensional field equations and observed Yukawa eigenvalues remain absent.')


def w33_laplacian():
    pts=B.PTS
    A=np.array([[int(i!=j and B.V.om(p,q)==0) for j,q in enumerate(pts)] for i,p in enumerate(pts)],float)
    assert np.all(A.sum(axis=0)==12) and np.all(A@A==8*np.eye(40)-2*A+4*np.ones((40,40)))
    return 12*np.eye(40)-A


def conformal_solution(a,b=2.,R=1.,L=None):
    L=w33_laplacian() if L is None else L
    def equation(u):
        phi=np.exp(u);return 8*L@phi+R*phi-a*phi**-7+b*phi**5
    sol=root(equation,np.zeros(len(a)),tol=1e-11)
    phi=np.exp(sol.x);res=np.linalg.norm(equation(sol.x),np.inf)
    assert res<1e-9
    H=8*L+np.diag(R+7*a*phi**-8+5*b*phi**4)
    return phi,res,float(np.linalg.eigvalsh(H)[0])


def gravity_certificate():
    L=w33_laplacian();a=1+np.arange(40)/40
    phi,res,gap=conformal_solution(a,L=L)
    phi2,res2,gap2=conformal_solution(a,L=3*L)
    const,rc,_=conformal_solution(np.ones(40)*3,L=L)
    assert np.max(abs(const-1))<1e-10 and gap>0
    rng=np.random.default_rng(11729);p=rng.permutation(40)
    perm,permres,_=conformal_solution(a[p],L=L[np.ix_(p,p)])
    assert np.linalg.norm(perm-phi[p],np.inf)<1e-10
    return dict(status='PASS',vertices=40,edges=240,
        equation='8 L phi+R phi-a phi^-7+b phi^5=0, phi_i>0',
        continuum_dictionary='b=2 K^2/3-2 Lambda, a=|sigma_TT|^2, conditional on a supplied 3-metric and TT tensor',
        variational_energy='4 phi^T L phi+(R/2)sum phi^2+sum a/(6 phi^6)+(b/6)sum phi^6',
        uniqueness_theorem='For a_i>0,b>0,R>=0, the energy is coercive with a boundary barrier, and its Hessian8L+diag(R+7a phi^-8+5b phi^4) is positive definite: exactly one positive solution.',
        source=a.tolist(),positive_solution=phi.tolist(),residual=res,Hessian_gap=gap,
        constant_solution_max_error=float(np.max(abs(const-1))),permutation_control=permres,
        Laplacian_scale_control_solution=phi2.tolist(),scale_change_norm=float(np.linalg.norm(phi-phi2)),
        scope='A nonlinear graph analogue of the CMC Hamiltonian constraint, not a proof of Lorentzian evolution, TT realizability, momentum constraints, ADM closure or a3D continuum limit. The fixed expander is not silently identified with space.')


def vacuum_shift_certificate():
    # Direct sum of two finite shape sectors; different volumes make C physical.
    H=np.array([[0.,1.,0.,0.],[1.,2.,0.,0.],[0.,0.,-1.,.3],[0.,0.,.3,1.]])
    volume=np.diag([2.,2.,3.,3.]);state=np.array([1,0,1,0],complex)/np.sqrt(2)
    from scipy.linalg import expm
    C=.73;t=.4
    shifted=expm(-1j*t*(H+C*volume))@state
    control=expm(-1j*t*H)@state
    cross=np.outer(shifted,shifted.conj())[0,2]/np.outer(control,control.conj())[0,2]
    assert abs(cross-np.exp(1j*C*t))<1e-12
    shift_errors=[]
    for delta in [-100.,-np.sqrt(2),0.,.73,100.]:
        lam=.27
        # Relabelling Lambda cancels C; holding Lambda fixed does not.
        shift_errors.append(float(np.linalg.norm((H+(lam-delta)*volume)+delta*volume-(H+lam*volume))))
    assert max(shift_errors)<1e-12
    Lambda=s.diag(-1,0,1);tr0=s.trace(Lambda)
    # Similarity preserves trace, ruling out Lambda -> Lambda-C I in finite dim.
    assert s.trace(Lambda-s.eye(3))!=tr0
    return dict(status='PASS',fixed_volume_state_probabilities_shift_invariant=True,
        volume_coherent_cross_phase={'real':float(cross.real),'imag':float(cross.imag)},
        volume_superselection_required_for_fixed_sector_cancellation=True,
        translated_Lambda_operator_residual=max(shift_errors),
        fixed_data_boundary='H(Lambda,C)=H0+(Lambda+C)V is covariant under Lambda->Lambda-C, but that changes Lambda-state/boundary data. It is not fixed-data screening.',
        finite_register_obstruction='A unitary shift U Lambda Udag=Lambda-C I for all realC is impossible in finite dimension by trace; a bounded spectrum cannot be invariant under all real translations either.',
        continuous_completion='On L2(R,dLambda), (T_C f)(Lambda)=f(Lambda+C) implements the shift, with translated states. A translation-invariant normalizable state on R does not exist.',
        scope='An exact quantum Ward/negative-control test of a supplied unimodular-type interface. No cosmological constant value or state-selection mechanism is derived.')


def topology_certificate():
    # Five roots for V plus two trivial lines. Work in H*(CP1^3), x_i^2=0.
    # The hidden defining5 restricts to the dual of the physical SU3 on3,4,5:
    # its Cartan eigenvalues are -h3,-h4,-h5,0,0 (11681 bracket convention).
    x,y,z=s.symbols('x y z');r=[-x-y-z,-x-y+2*z,2*x+2*y-z,0,0]
    coeff=lambda p:s.expand(p).coeff(x,1).coeff(y,1).coeff(z,1)
    c3=int(coeff(sum(s.prod(t) for t in it.combinations(r,3))))
    assert c3==-6
    # An unoriented principal triplet reduces to the real spin2 representation.
    a=s.symbols('a');spin2=[2*a,a,0,-a,-2*a]
    odd=s.expand(sum(s.prod(t) for t in it.combinations(spin2,3)))
    assert odd==0
    return dict(status='PASS',bundle='W=V_dual direct_sum O direct_sum O, rank5, c1=0; duality follows from the actual hidden5 Cartan convention',integral_c3_W=c3,
        ordered_triplet_stabilizer='Z5, by irreducibility and Schur lemma inside SU5',
        ordered_global_triplet_obstruction='A smooth everywhere principal ordered triplet reduces the SU5 bundle to finite Z5; rational positive-degree Chern classes vanish, contradicting integral c3=-6. Conjugating the family convention reverses the sign but not the obstruction.',
        rotating_triplet_stabilizer='principal SU2 image times central Z5 (normalizer, with triplet rotations)',
        rotating_triplet_c3=0,
        possible_escape='Allow Higgs rank-loss defects or nonprincipal patches, use a different gauge-breaking inventory, or separate the family-index bundle from this hidden-SU5 bundle. None is constructed here.',
        scope='A compatibility theorem for the specified same-bundle compactification interface. It does not refute prior finite-point E8 Higgs certificates, which never asserted a global compactification bundle.')


def dual(label):
    if label[0]=='A':return ('A',label[2],label[1]),1
    return (('k' if label[0]=='x' else 'x'),*label[1:]),-1


def root_bracket(a,b):
    """Exact root-to-root Chevalley constants in11681's actual sl9 basis.

    A zero return can also mean a Cartan output, excluded from the weight4
    sector used below. Validation compares every nonzero constant used with
    the original tensor bracket.
    """
    ka,kb=a[0],b[0];ta,tb=a[1:],b[1:]
    if ka=='A' and kb=='A':
        i,j=ta;k,l=tb
        if j==k and i!=l:return ('A',i,l),1
        if l==i and k!=j:return ('A',k,j),-1
        return None,0
    if ka!='A' and kb=='A':
        c,v=root_bracket(b,a);return c,-v
    if ka=='A':
        i,j=ta;old,new,sgn=(j,i,1) if kb=='x' else (i,j,-1)
        if old not in tb or new in tb:return None,0
        u=tuple(new if q==old else q for q in tb)
        return (kb,*sorted(u)),sgn*E.psign(u)
    if ka==kb:
        if set(ta)&set(tb):return None,0
        rest=tuple(q for q in range(9) if q not in ta+tb)
        return (('k' if ka=='x' else 'x'),*rest),E.psign(ta+tb+rest)
    if ka=='k':
        c,v=root_bracket(b,a);return c,-v
    common=tuple(sorted(set(ta)&set(tb)))
    if len(common)!=2:return None,0
    i=next(x for x in ta if x not in common);j=next(x for x in tb if x not in common)
    return ('A',i,j),-E.psign((i,*common))*E.psign((j,*common))


def root_element(label):
    out=E._zero()
    if label[0]=='A':out[0][label[1],label[2]]=1
    else:out[1 if label[0]=='x' else 2][E.TI[label[1:]]]=1
    return out


@lru_cache(None)
def weight_casimir(weight):
    labs,ws,lookup=roots();index={t:i for i,t in enumerate(labs)}
    pairs=[]
    for i,w in enumerate(ws):
        j=lookup.get(tuple(x-y for x,y in zip(weight,w)))
        if j is not None and i<=j:pairs.append((i,j))
    # Used only at nonzero weights of norm4 or6: neither roots nor twice roots.
    assert all(i!=j for i,j in pairs)
    pos={p:i for i,p in enumerate(pairs)};Omega=s.zeros(len(pairs));used=set()
    for col,(a,b) in enumerate(pairs):
        Omega[col,col]+=s.Rational(sum(x*y for x,y in zip(ws[a],ws[b])),9)
        terms=Counter()
        for r in labs:
            rd,sign=dual(r)
            for u,v in [(labs[a],labs[b]),(labs[b],labs[a])]:
                c,ca=root_bracket(r,u);d,cb=root_bracket(rd,v)
                if ca and cb:
                    used.add((r,u));used.add((rd,v))
                    terms[tuple(sorted((index[c],index[d])))]+=sign*ca*cb
        for p,c in terms.items():Omega[pos[p],col]+=s.Rational(c,2)
    assert Omega==Omega.T
    return pairs,Omega,used


@lru_cache(None)
def exceptional_section_certificate():
    labs,ws,_=roots();index={t:i for i,t in enumerate(labs)}
    section=[('A',3,i) for i in range(9) if i!=3];checks=[]
    for a,b in it.combinations_with_replacement(section,2):
        wa,wb=ws[index[a]],ws[index[b]]
        assert np.max(abs(E._vec(E.bracket(root_element(a),root_element(b)))))==0
        assert tuple(-x for x in wa)!=wb # invariant bilinear zero
        if a==b:
            # The weight2a sector has only a tensor a, with Omega=||a||^2=2.
            weight=tuple(2*x for x in wa)
            assert not any(tuple(x-y for x,y in zip(weight,w)) in roots()[2]
                           for w in ws if w!=wa)
            size=1;res=0
        else:
            weight=tuple(x+y for x,y in zip(wa,wb));pairs,Om,_=weight_casimir(weight)
            size=len(pairs);res=Om-2*s.eye(size)
            assert res==s.zeros(size)
        checks.append(dict(pair=[list(a),list(b)],symmetric_weight_sector_dimension=size,P3875_zero=True))
    extensions=[];kept=[];rejections=Counter()
    for r,w in zip(labs,ws):
        for a in section:
            wa=ws[index[a]];dot=s.Rational(sum(x*y for x,y in zip(w,wa)),9)
            if dot<0:
                kind='singlet' if dot==-2 else 'adjoint'
                if dot==-1:assert root_bracket(a,r)[1]!=0
                rejections[kind]+=1;extensions.append(dict(root=list(r),witness=list(a),rejected_by=kind));break
            if dot==0:
                weight=tuple(x+y for x,y in zip(w,wa));pairs,Om,_=weight_casimir(weight)
                P=(2*s.eye(len(pairs))-Om)/14;ii=pairs.index(tuple(sorted((index[a],index[r]))))
                assert P[ii,ii]==s.Rational(1,7)
                rejections['3875']+=1;extensions.append(dict(root=list(r),witness=list(a),rejected_by='3875',projection_norm_squared='1/7'));break
        else:kept.append(r)
    assert kept==section and rejections=={'singlet':1,'adjoint':57,'3875':174}
    cartan=s.Matrix([[int((a[1]==i)-(a[1]==8)-(a[2]==i)+(a[2]==8)) for i in range(8)] for a in section])
    assert cartan.rank()==8
    # A one-dimensional literal vector-field algebra along a chosen section
    # coordinate has the ordinary nonlinear Leibniz/Lie bracket on polynomials.
    u=s.symbols('u');N=u*u+1;M=u**3-u;f=u**4+2
    D=lambda n,g:n*s.diff(g,u)
    residual=s.expand(D(N,D(M,f))-D(M,D(N,f))-D(N*s.diff(M,u)-M*s.diff(N,u),f))
    assert residual==0
    return dict(status='PASS',real_split_section_generators=[list(x) for x in section],section_dimension=8,
        all36_symmetric_pair_checks=checks,singlet_and_adjoint_constraints_zero=True,
        maximal_linear_section=True,all240_root_extension_audit=extensions,
        extension_rejections=dict(rejections),Cartan_extension_constraint_rank=8,
        maximality_proof='All232 external root directions fail a named constraint; distinct root weights cannot cancel for a fixed section generator. The eight Cartan commuting equations have rank8. Hence no further complex adjoint direction can extend this constant linear section.',
        strong_constraint='P_(1+248+3875)(partial tensor partial)=0; invariant form identifies the displayed root vectors with derivative covectors.',
        ray_dictionary='For a chosen ray[psi] in CP8, the complex section is span{|psi><v|: <v|psi>=0}; its conjugates satisfy the same algebraic constraints. The displayed real section uses psi=e3, the previous11723 SM-neutral density example.',
        one_coordinate_nonlinear_vector_field_commutator_residual=str(residual),
        Yukawa_negative_control='The11732 pair A30,x013 has P3875 squared norm1/7. A30 is in the displayed section; x013 cannot be added to it as an independent derivative.',
        scope='An explicit section of established E8(8) exceptional field theory in11681 coordinates. The classical EFT action, external Lorentzian3-space, field inventory, scale and section choice are additional input. No EFT action or4D Einstein dynamics is derived from the finite graph; complex SU9 transports need not preserve the chosen split-real form.',
        primary_source='https://arxiv.org/abs/1406.3348')


@lru_cache(None)
def yukawa_projector_certificate():
    labs,ws,lookup=roots();index={t:i for i,t in enumerate(labs)}
    # Both roots are in the same fundamental-family component of (27,3),
    # for family SU3 on levels3,4,5, inside the hidden SU5 and commuting
    # with the visible SU5 on0,1,2,7,8. Do not mistake the color SU3 for family.
    aa=index['A',3,0];bb=index['x',0,1,3]
    weight=tuple(x+y for x,y in zip(ws[aa],ws[bb]))
    assert sum(x*x for x in weight)==36
    pairs,Omega,used=weight_casimir(weight);pos={p:i for i,p in enumerate(pairs)}
    assert len(pairs)==7 and Omega.eigenvals()=={-12:1,2:6}
    P=(2*s.eye(7)-Omega)/14
    assert P*P==P and P.rank()==1
    seed=pos[tuple(sorted((aa,bb)))];assert P[seed,seed]>0
    worst=0
    for a,b in sorted(used):
        c,k=root_bracket(a,b)
        err=E._vec(B.add(E.bracket(root_element(a),root_element(b)),B.scale(-k,root_element(c))))
        worst=max(worst,float(np.max(abs(err))))
    assert worst==0
    dims=[1,650,8,78*8,2*27*3,2*351*3,2*27*6]
    assert sum(dims)==3875
    return dict(status='PASS',classical_decomposition='Sym2(248)=1+3875+27000',
        classical_E6_SU3_branching='(1,1)+(650,1)+(1,8)+(78,8)+(27,3)+conjugate+(351,3)+conjugate+(27,6bar)+conjugate',
        branching_dimension_sum=sum(dims),seed_roots=[list(labs[aa]),list(labs[bb])],
        family_SU3_levels=[3,4,5],commuting_visible_SU5_levels=B.F5,
        selected_weight_times3=[int(x) for x in weight],weight_sector_dimension=7,
        symmetric_root_pair_basis=[[list(labs[i]),list(labs[j])] for i,j in pairs],
        cross_Casimir_matrix=[[int(x) for x in row] for row in Omega.tolist()],
        cross_Casimir_eigenvalues={'-12':1,'2':6},
        projector='P3875=-(Omega+60)(Omega-2)/672; on this sector (2-Omega)/14',
        projector_matrix=[[str(x) for x in row] for row in P.tolist()],projector_rank=1,
        seed_projected_norm_squared=str(P[seed,seed]),seed_index=seed,
        tensor_bracket_constants_checked=len(used),tensor_bracket_residual=worst,
        E8_covariant_Yukawa='y H_ab psi^a_alpha psi^b_beta epsilon^(alpha beta), H in real3875 subset Sym2(adj), Weyl psi in adj248',
        restricted_operator='The H_(27,6bar) channel gives the prior11271 symmetric d_ABC psi_i^A psi_j^B H^(C,ij). The Lorentz bilinear is symmetric in combined gauge/flavor indices.',
        scope='A nonzero actual E8 projector witness and classical branching completion of11271, not a selected H vev or a chiral248 spectrum. The3875 changes the scalar inventory; local zero-mode overlap integrals and observed fermion masses remain uncomputed.')


def quartic_certificate():
    # Exact second variations on the already-selected traceless Hermitian SU5.
    Y=s.diag(-2,-2,-2,3,3);eps=s.symbols('eps')
    hessian=[]
    for block in [(0,1),(3,4)]:
        d=s.zeros(5);d[block[0],block[0]]=1;d[block[1],block[1]]=-1
        T=Y+eps*d;p2=s.trace(T*T);p4=s.trace(T**4)
        f=960*(p4-s.Rational(7,30)*p2*p2)
        h=s.diff(f,eps,2).subs(eps,0)/s.trace(d*d);hessian.append(int(h))
    assert hessian==[19200,76800]
    return dict(status='PASS',branch_EFT_selector='eta (I-1304 p2^2)=960 eta (p4-7 p2^2/30), eta>0',
        positive_physical_shape_Hessian_eigenvalues={'19200 eta':8,'76800 eta':3},
        gauge_orbit_zero_modes=12,radial_mode='Positive if the supplied (p2-30)^2 term is retained; eigenvalue240 in Tr(dSigma^2) metric.',
        compared_with11725='The earlier square of this nonnegative selector has zero quadratic curvature. Its unsquared branch restriction gives11 positive shape modes.',
        scope='An exact low-energy Hessian on the selected SU5 centralizer and principal branch. Nonnegativity is certified on that branch; the unsquared mixed E8 invariant is not asserted nonnegative off branch, so this is not a full E8 UV potential or measured Higgs spectrum.')


def payload():
    functions=[orbit_certificate,branch_certificate,chiral_certificate,gravity_certificate,
               vacuum_shift_certificate,topology_certificate,yukawa_projector_certificate,quartic_certificate]
    out={'status':'PASS','reservation':'5470f3255','schema':'w33-eight-interface-v1','passes':{},
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest()}
    for n,f in enumerate(functions,11726):
        out['passes'][str(n)]=f();print(n,'PASS',flush=True)
        if n==11729:out['passes'][str(n)]['exceptional_field_theory_section']=exceptional_section_certificate()
    out['physical_boundary']='No derived Lorentzian spacetime, local chiral vacuum, observed masses/mixing/couplings, or cosmological constant value. These constructions expose and improve specific interfaces.'
    return out


if __name__=='__main__':
    out=payload();OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(OUT)
