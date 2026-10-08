"""Coherent Witting/flag vacua and an explicit E8 adjoint Higgs interface.

11663 owns rank1/rank2 Pauli projectors;11698 owns the320 stabilizer vacua;
11672 owns the native parent;11271 owns a different E6 SM Higgs interface.
All actions, scales and the principal embedding are supplied model choices.
"""
from __future__ import annotations
from collections import Counter, defaultdict, deque
from functools import lru_cache
import hashlib
import itertools as it
import json
from pathlib import Path
import sys
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11697_11698_chirality_vacuum as V
import w33_pass11663_odd_weil_normal_map as N
import w33_pass11672_11679_native_dynamics_index as PARENT
import w33_pass11681_e8_from_two_qutrits as E
import w33_pass11701_11702_clock_symmetry_breaking as CLOCK
OUT=ROOT/'data/w33_pass11721_11725_coherent_vacuum_gauge_bridge.json'
PTS=sorted({tuple(x*next(y for y in v if y)%3 for x in v) for v in V.nonzero(2)})
PI=V.parity(2).astype(int)
NEG=np.argmax(PI,axis=0)
EV,OD=N.parity_bases()
ON=np.array(OD,dtype=float)/np.sqrt(2)
EN=np.array(EV,dtype=float)@np.diag([1,*([1/np.sqrt(2)]*4)])

# Z[omega] matrices are pairs(a,b), meaning a+b*omega. All exact census
# projectors below have explicitly recorded denominators9 or18.
def emul(x,y):
    a,b=x;c,d=y
    return a@c-b@d,a@d+b@c-b@d

def escale(x,k):return tuple(k*a for a in x)
def eadd(*xs):return tuple(sum(x[i] for x in xs) for i in range(2))
def edag(x):a,b=x;return a.T-b.T,-b.T
def ekey(x):return tuple(a.tobytes() for a in x)
def enum(x):return x[0]+V.W*x[1]
def etrace(x):return tuple(int(np.trace(a)) for a in x)

def exact_weyl(v,phase=0):
    out=[np.zeros((9,9),dtype=np.int64) for _ in range(2)]
    for i,(x,y) in enumerate(it.product(range(3),repeat=2)):
        j=3*((x+v[0])%3)+(y+v[2])%3
        t=(phase+2*v[0]*v[1]+2*v[2]*v[3]+v[1]*x+v[3]*y)%3
        a,b=[(1,0),(0,1),(-1,-1)][t]
        out[0][j,i]=a;out[1][j,i]=b
    return tuple(out)

@lru_cache(None)
def exact_flags():
    lines=set()
    for a,b in it.combinations(PTS,2):
        if V.om(a,b)==0:
            lines.add(tuple(sorted({tuple((i*a[k]+j*b[k])%3 for k in range(4)) for i,j in it.product(range(3),repeat=2)})))
    rows=[];odd={};even={};by_point=defaultdict(list)
    for li,L in enumerate(sorted(lines)):
        a=next(v for v in L if any(v));a1={tuple(t*x%3 for x in a) for t in range(3)}
        b=next(v for v in L if v not in a1)
        for ca,cb in it.product(range(3),repeat=2):
            if ca==cb==0:continue
            r=eadd(*[exact_weyl(tuple((i*a[k]+j*b[k])%3 for k in range(4)),-i*ca-j*cb) for i,j in it.product(range(3),repeat=2)])
            assert ekey(emul(r,r))==ekey(escale(r,9)) and etrace(r)==(9,0)
            assert ekey(edag(r))==ekey(r)
            zeros=[p for p in PTS if p in L and ekey(emul(exact_weyl(p),r))==ekey(r)]
            assert len(zeros)==1
            pr=tuple(x[NEG,:] for x in r);rp=tuple(x[:,NEG] for x in r);prp=tuple(x[NEG,:][:,NEG] for x in r)
            o=eadd(r,escale(pr,-1),escale(rp,-1),prp)
            e=eadd(r,pr,rp,prp)
            assert etrace(o)==etrace(e)==(18,0)
            assert ekey(emul(o,o))==ekey(escale(o,18))
            assert ekey(emul(e,e))==ekey(escale(e,18))
            oi=odd.setdefault(ekey(o),len(odd));ei=even.setdefault(ekey(e),len(even))
            row=dict(point=PTS.index(zeros[0]),line=li,character=[ca,cb],odd_ray=oi,even_ray=ei,
                     projector9_sha256=hashlib.sha256(b''.join(ekey(r))).hexdigest())
            rows.append((row,r,o,e));by_point[row['point']].append((o,e))
    assert len(lines)==40 and len(rows)==320 and len(odd)==40 and len(even)==160
    assert set(Counter(r[0]['odd_ray'] for r in rows).values())=={8}
    assert set(Counter(r[0]['even_ray'] for r in rows).values())=={2}
    for p,block in by_point.items():
        qs={ekey(e):e for o,e in block};assert len(qs)==4
        q=list(qs.values())
        for i,j in it.product(range(4),repeat=2):
            assert etrace(emul(q[i],q[j]))==((324 if i==j else 108),0)
        L=eadd(exact_weyl((0,0,0,0)),exact_weyl(PTS[p]),edag(exact_weyl(PTS[p])))
        even_plane=eadd(L,tuple(a[NEG,:] for a in L))
        odd_line=eadd(L,escale(tuple(a[NEG,:] for a in L),-1))
        assert ekey(eadd(*q))==ekey(escale(even_plane,6)) # sum tetra projectors=2Qp
        assert ekey(block[0][0])==ekey(escale(odd_line,3))
    return rows

def projection_certificate():
    rows=exact_flags()
    return dict(status='PASS',field='Z[omega], omega^2+omega+1=0; projectors scaled by9 or18',
                chirality_vacua=320,odd_rays=40,odd_fiber=8,even_rays=160,even_fiber=2,
                tetrahedra=40,tetrahedron_squared_overlap='1/3',tetrahedron_frame_sum='2 Q_p',
                coherent_lift='psi=(e+o)/sqrt2; Pi psi=(e-o)/sqrt2, with phases inherited from the full projector',
                rows=[r[0] for r in rows],
                scope='Exact projective flag-to-parity-projection map, not three chiral fermion generations.')

def realify(a):
    out=np.empty((2*a.shape[0],2*a.shape[1]))
    out[::2,::2]=a.real;out[1::2,1::2]=a.real
    out[::2,1::2]=-a.imag;out[1::2,::2]=a.imag
    return out

def realvec(z):
    x=np.empty(2*len(z));x[::2]=z.real;x[1::2]=z.imag;return x

OPS=np.array([V.weyl(v) for v in V.nonzero(2)])
IMOPS=np.array([(d-d.conj().T)/(2j) for d in OPS])
GOPS=np.array([realify(a) for a in IMOPS])

def s4(psi):return float(np.sum(np.einsum('i,kij,j->k',psi.conj(),OPS,psi).imag**4))

def chirality_hessian(psi):
    x=realvec(psi);r=x@x;m=np.einsum('i,kij,j->k',x,GOPS,x);dm=2*np.einsum('kij,j->ki',GOPS,x)
    c=27/8
    return 8*np.outer(x,x)+4*(r-1)*np.eye(18)+8*c*r**3*np.eye(18)+48*c*r**2*np.outer(x,x)-\
        np.einsum('k,ki,kj->ij',12*m*m,dm,dm)-np.einsum('k,kij->ij',8*m**3,GOPS)

@lru_cache(None)
def ray_transport():
    w=s.Rational(-1,2)+s.sqrt(3)*s.I/2
    gs=[np.array(g.subs(N.W,w).evalf(),dtype=complex) for g in N.canonical_generators().values()]
    go=[ON.conj().T@g@ON for g in gs]
    def key(U):
        r=U[:,0];p=np.outer(r,r.conj());return tuple(np.round(realvec(p.ravel()),9))
    identity=np.eye(4,dtype=complex);todo=deque([identity]);seen={key(identity):identity}
    while todo:
        U=todo.popleft()
        for g in go:
            h=g@U;k=key(h)
            if k not in seen:seen[k]=h;todo.append(h)
    assert len(seen)==40
    return list(seen.values())

def parent_lift(psi):
    f=np.sqrt(3)*ON.conj().T@psi
    U=max(ray_transport(),key=lambda u:abs(np.vdot(u[:,0],f)))
    assert abs(abs(np.vdot(U[:,0],f))-np.sqrt(1.5))<1e-10
    phase=np.vdot(U[:,0],f)/np.sqrt(1.5)
    T=phase**2*U@np.diag([2,1,1,1])@U.T
    q=np.array([T[i,j]*(np.sqrt(2) if i!=j else 1) for i,j in PARENT.pairs])
    return realvec(np.r_[f,q,np.zeros(5)])

def coupled_potential(x,psi):
    c=27/8;r=np.vdot(psi,psi).real;f=x[:8:2]+1j*x[1:8:2]
    return PARENT.potential(x)+23/8+(r-1)**2+c*r**4-s4(psi)+np.linalg.norm(f-np.sqrt(3)*ON.conj().T@psi)**2

def coupled_certificate():
    rows=exact_flags();worst=0;pure_odd=0;witting=0
    for _,r,_,_ in rows:
        psi=np.linalg.eigh(enum(r)/9)[1][:,-1];x=parent_lift(psi)
        worst=max(worst,abs(coupled_potential(x,psi)))
        o=np.sqrt(2)*ON@ON.conj().T@psi
        pure_odd=max(pure_odd,s4(o));witting=max(witting,np.linalg.norm(N.quartic(ON.conj().T@o)))
    psi=np.eye(9,dtype=complex)[:,1];x=parent_lift(psi)
    H=np.zeros((56,56));H[:38,:38]=PARENT.hessian(x);H[38:,38:]=chirality_hessian(psi)
    J=np.zeros((8,56));J[:,:8]=np.eye(8);J[:,38:]=-np.sqrt(3)*realify(ON.conj().T)
    H+=2*J.T@J;ev=np.linalg.eigvalsh(H)
    assert worst<1e-11 and pure_odd<1e-25 and witting<1e-11
    assert min(ev)>-1e-9 and sum(ev>1e-8)==51
    return dict(status='PASS',potential='Vparent+23/8+(||psi||^2-1)^2+(27/8)||psi||^8-S4(psi)+||f-sqrt3 Odag psi||^2',
        global_minimum=0,all320_exact_projective_chirality_vacua_lift=True,numeric_zero_control=worst,
        pure_odd_maximum_S4=pure_odd,odd_projection_max_Maschke_norm=witting,
        phase_law='S4((e+exp(i theta)o)/sqrt2)=(27 cos(theta)^4+9 sin(theta)^4)/8',
        fields_real=56,charges='f1,q2,z4,psi1; the even companion is new and has charge1',
        hessian=ev.tolist(),positive_directions=51,zero_directions=5,
        old_z_cannot_be_even_companion='The old even5 z has charge4; mixing it directly with charge1 f is not a common-charge quantum state.',
        scope='Global tree minimum of a supplied degree8 EFT; projection is discrete, auxiliary q minima can remain continuous. No inherited full-loop stability or physical Weyl index.')

F5=[0,1,2,7,8]
R4=[3,4,5,6]
Y0=np.array([-2,-2,-2,0,0,0,0,3,3])

def covariance_certificate():
    psi=np.eye(9)[:,3];rho=np.outer(psi,psi)-np.eye(9)/9
    clocks=[CLOCK.lifts(CLOCK.Z9**np.array([3*x*y*y for x,y in CLOCK.XY]))[1],
            CLOCK.lifts(CLOCK.Z9**np.array([x**3+3*x*y+3*x*x*y for x,y in CLOCK.XY]))[1]]
    mask=CLOCK.kept(clocks[0])&CLOCK.kept(clocks[1])
    assert CLOCK.typ(mask)==('A1','A2') and sum(mask)==8
    cartan=[np.diag(np.eye(9)[i]-np.eye(9)[8]) for i in range(8)]
    assert all(np.linalg.norm(h@rho-rho@h)==0 for h in cartan)
    return dict(status='PASS',joint_root_count=8,Cartan_dimension=8,unbroken_dimension=16,center_rank=5,
        density_matrix_leaves_all_five_U1s=True,extra_U1_beyond_hypercharge=4,
        vector_criterion='Y psi=0 is a specified charged-vector criterion, stronger than [Y,rho]=0.',
        global_group_obstruction='omega I9 acts trivially on E8=sl9+Lambda3+dual but nontrivially on C9; the9 does not descend to SU9/Z3.',
        distinction='A quantum Hilbert-space state or projective ray need not be an E8 Higgs field. The density matrix is an adjoint element, but the rank1 SU9 orbit is not a full E8 orbit.',
        scope='An additive physical-interface audit; preserves11708 conditional hypercharge enumeration and the prior holonomy-centralizer scope correction.')

def scale(c,a):return tuple(c*x for x in a)
def add(*a):return tuple(sum(x[i] for x in a) for i in range(3))
def star(a):return a[0].conj().T,-a[2].conj(),-a[1].conj()

@lru_cache(None)
def hidden_su5():
    roots=[]
    for i in R4:
        z=E._zero();z[1][E.TI[tuple(j for j in R4 if j!=i)]]=1;roots.append(z)
    duals=[star(a) for a in roots];hs=[E.bracket(a,b) for a,b in zip(roots,duals)]
    total=add(*hs);units={}
    for i,j in it.product(range(5),repeat=2):
        if i==j:units[i,j]=add(hs[i],scale(-.2,total)) if i<4 else scale(-.2,total)
        elif j==4:units[i,j]=roots[i]
        elif i==4:units[i,j]=duals[j]
        else:units[i,j]=E.bracket(roots[i],duals[j])
    # Scale by15 to clear every rational denominator. Integer products and
    # the exactly divisible contractions stay below2^53 in this finite check.
    iu={key:tuple(np.rint(a.real*15).astype(np.int64) for a in val) for key,val in units.items()}
    assert max(np.max(abs(E._vec(add(scale(15,units[k]),scale(-1,iu[k]))))) for k in units)<1e-12
    # Independent defining matrix-unit relations, including dual/star signs.
    err=0
    for i,j,k,l in it.product(range(5),repeat=4):
        rhs=add(scale(15*int(j==k),iu[i,l]),scale(-15*int(l==i),iu[k,j]))
        err=max(err,float(np.max(np.abs(E._vec(add(E.bracket(iu[i,j],iu[k,l]),scale(-1,rhs)))))))
    assert err==0
    Jz=add(*[scale(2-i,units[i,i]) for i in range(5)])
    Jp=add(*[scale(np.sqrt((i+1)*(4-i)),units[i,i+1]) for i in range(4)])
    Jm=star(Jp);Js=[scale(.5,add(Jp,Jm)),scale(1/(2j),add(Jp,scale(-1,Jm))),Jz]
    return units,Js,err

@lru_cache(None)
def adjoint_kinetics():
    units,Js,err=hidden_su5();basis,Sl,_=E.e8_basis()
    Q=np.linalg.qr(Sl)[0];Z84=np.zeros(84,complex)
    basis=[(Q[:,i].reshape(9,9),Z84,Z84) for i in range(80)]+basis[80:]
    coords=lambda a:np.r_[Q.conj().T@a[0].ravel(),a[1],a[2]]
    ads=[np.array([coords(E.bracket(j,b)) for b in basis]).T for j in Js]
    Y=(np.diag(Y0).astype(complex),Z84,Z84)
    ay=np.array([coords(E.bracket(Y,b)) for b in basis]).T
    assert max(np.max(abs(a-a.conj().T)) for a in ads+[ay])<1e-12
    C=sum(a@a for a in ads);K=C+ay@ay
    return C,K,ads,ay

def exact_joint_spectrum():
    _,Js,_=hidden_su5();h=Js[2][0].diagonal().real
    weights=Counter({(0,0):8})
    for kind,idx,_ in CLOCK.T.ROOTS:
        z=h[idx[0]]-h[idx[1]] if kind=='A' else sum(h[i] for i in idx)*(1 if kind=='L' else -1)
        y=Y0[idx[0]]-Y0[idx[1]] if kind=='A' else sum(Y0[i] for i in idx)*(1 if kind=='L' else -1)
        assert abs(z-round(z))<1e-12
        weights[int(round(z)),int(y)]+=1
    modules=[];spectrum=Counter()
    for q in sorted({q for j,q in weights}):
        for j in range(5):
            count=weights[j,q]-weights[j+1,q]
            assert count>=0
            if count:
                modules.append(dict(spin=j,Y6=q,copies=count))
                spectrum[j*(j+1)+q*q]+=count*(2*j+1)
    assert sum(spectrum.values())==248 and spectrum[0]==12
    return modules,spectrum

def adjoint_higgs_certificate():
    units,Js,err=hidden_su5();modules,spectrum=exact_joint_spectrum()
    C,K,ads,ay=adjoint_kinetics();ev=np.linalg.eigvalsh(K)
    observed=Counter(np.rint(ev).astype(int));assert observed==spectrum
    assert max(abs(ev-np.rint(ev)))<1e-9
    assert sum(abs(np.linalg.eigvalsh(C))<1e-8)==24
    for a,b in it.combinations(range(3),2):
        c=3-a-b;sign=1 if (a,b,c) in [(0,1,2),(1,2,0),(2,0,1)] else -1
        assert np.max(abs(E._vec(add(E.bracket(Js[a],Js[b]),scale(-1j*sign,Js[c])))))<1e-12
    # An alternative compatible clock uses the native Weil quadratic phase,
    # not the original pair whose Higgs invariance is not automatic.
    lam=V.W**Y0
    phases=[lam[i]/lam[j] for i in range(9) for j in range(9) if i!=j]+[1]*8
    phases += [np.prod(lam[list(t)]) for t in E.TR]
    phases += [np.prod(lam[list(t)]).conjugate() for t in E.TR]
    phases=np.array(phases)
    assert abs(np.sum(phases)-5)<1e-12 and sum(abs(phases-1)<1e-10)==86
    assert np.linalg.norm(C@np.diag(phases)-np.diag(phases)@C)<1e-11
    kt=C+np.diag(abs(phases-1)**2)
    clock_spectrum=Counter(np.rint(np.linalg.eigvalsh(kt)).astype(int))
    exact_clock_spectrum=Counter()
    for m in modules:
        exact_clock_spectrum[m['spin']*(m['spin']+1)+(3 if m['Y6']%3 else 0)]+=m['copies']*(2*m['spin']+1)
    assert clock_spectrum==exact_clock_spectrum and clock_spectrum[0]==12
    classes=[]
    for n0 in range(6):
        for n1 in range(6-n0):
            n2=5-n0-n1
            if (n1+2*n2)%3:continue
            a,b=s.Integer(n0-n2),s.Integer(n1-n2)
            re5=a-b/2;norm=a*a-a*b+b*b
            re10=((a*a-b*b)-(2*a*b-b*b)/2-re5)/2
            trace=23+norm+10*re10+20*re5
            classes.append(dict(SU5_cube_root_multiplicities=[n0,n1,n2],E8_adjoint_trace=int(trace)))
    assert {tuple(r['SU5_cube_root_multiplicities']) for r in classes if r['E8_adjoint_trace']==5}=={(2,3,0),(2,0,3)}
    return dict(status='PASS',hidden_levels=R4,visible_SU5_levels=F5,
        hidden_SU5_generators='E_i4=trivector of R4 minus i; E_4i=star(E_i4); E_ij=[E_i4,E_4j]',
        all625_matrix_unit_relations_residual=err,
        all625_scaled_integer_relations_exact=True,
        compact_invariant_norm='||a||^2=Tr(A dagger A)+x dagger x+k dagger k; star(A,x,k)=(A dagger,-conj(k),-conj(x))',
        principal_Jz_diagonal=[str(s.Rational(float(x)).limit_denominator(3)) for x in Js[2][0].diagonal().real],
        principal_SU2_centralizer_dimension=24,with_Y6_centralizer_dimension=12,hypercharge_Y6=Y0.tolist(),
        gauge_mass_operator='sum_a ad(J_a)^2+ad(Y6)^2; overall gauge coupling and vev scales set to1',
        exact_gauge_mass_squared_multiplicities={str(k):v for k,v in sorted(spectrum.items())},
        exact_spin_and_charge_modules=modules,numeric_248_spectrum_max_error=float(max(abs(ev-np.rint(ev)))),
        compatible_native_clock='U=diag(omega on the three colour levels,1 elsewhere)=omega D0; the scalar omega is E8-trivial',
        clock_fixed_E8_dimension=86,clock_E8_adjoint_trace=5,
        clock_Higgs_mass_operator='C_J+(AdU-I)dag(AdU-I)',
        clock_Higgs_mass_squared_multiplicities={str(k):v for k,v in sorted(exact_clock_spectrum.items())},
        exact_clock_mass_law='j(j+1)+3 when Y6 is nonzero mod3, otherwise j(j+1)',
        all_SU5_cubed_identity_clock_classes=classes,
        bounded_clock_Higgs_action='Vfuzzy+sum_a||AdU Phi_a-Phi_a||^2+||Ad(U^3)-I||^2+|Tr_ad U-5|^2',
        exact_clock_branch_selection='On the principal-SU2 branch and the identity component of its centralizerSU5, the zero conditions force clock multiplicities2+3 and exactly the SM Lie algebra. The conjugacy-class targettrace5 is supplied, not dynamically derived from W33.',
        commuting_clocks_only_boundary='For the original SM-shaped pair, every clock-invariant SM-singlet adjoint lies in its five-dimensional abelian center; such vevs cannot lift any of those U1s. The compatible native clock above has a larger86-dimensional fixed algebra before the Higgs is added.',
        scope='Explicit E8-adjoint rank reduction to the SM Lie algebra, using supplied principal SU2 with Y6 or a compatible native clock. Branch and class selection inputs remain; no chirality, observed masses or spacetime derivation.')

def selection_certificate():
    # Compare two Cartan directions of the SAME fixed E8 quadratic norm.
    a=[-2,-2,-2,3,3,0,0,0,0];b=[1,1,1,1,-4,0,0,0,0]
    def traces(x,scale2=1):
        vals=[]
        for kind,idx,_ in CLOCK.T.ROOTS:
            q=x[idx[0]]-x[idx[1]] if kind=='A' else sum(x[i] for i in idx)*(1 if kind=='L' else -1)
            vals.append(q)
        return {str(k):str(sum(s.Integer(q)**k for q in vals)*s.Rational(scale2)**(k//2)) for k in [2,4,6,8]}
    ta,tb=traces(a),traces(b,s.Rational(3,2))
    assert all(ta[str(k)]==tb[str(k)] for k in [2,4,6]) and ta['8']!=tb['8']
    # The mixed invariant is degree8 in the actual FOUR adjoint fields:
    # C=sum ad(Phi)^2 has degree2 and Tr C^2 ad(Sigma)^4 has degree8.
    # At principal hidden SU2:5=spin2,10=spin1+spin3. Hence
    # I=360 Tr_10 Sigma^4+2040 Tr_5 Sigma^4
    #  =1080 p2^2+960 p4.
    C,K,ads,ay=adjoint_kinetics();mixed=float(np.trace(C@C@ay@ay@ay@ay).real)
    assert abs(mixed-1173600)<1e-7
    two_value={str(k):str(s.Rational((5-k)**3+k**3,25*k*(5-k))) for k in [1,2]}
    assert two_value=={'1':'13/20','2':'7/30'}
    return dict(status='PASS',supplied_nonnegative_renormalizable_action=
        'sum_ab ||[Phi_a,Phi_b]-i epsilon_abc Phi_c||^2 + sum_a ||[Sigma,Phi_a]||^2 + (||Sigma||^2-30)^2',
        zero_energy_configuration='Phi_a=J_a in hidden SU5; Sigma=Y6 in visible SU5',
        exact_flat_family='Every Sigma in visible su5 with ||Sigma||^2=30 has zero energy at the same Phi.',
        Sigma_sphere_dimension=23,GG_gauge_orbit_dimension=12,GG_extra_Hessian_flat_directions=11,
        generic_Cartan_shape_moduli=3,primitive_E8_invariant_degrees=[2,8,12,14,18,20,24,30],
        normalized_Cartan_traces_GG=ta,normalized_Cartan_traces_other=tb,
        primitive_trace8_control='Pure Tr_ad Sigma^8 does distinguish shapes but is not a GG minimizer: the normalized2+2+1 shape has23085000, below GG23727600.',
        mixed_degree8_invariant='I(Phi,Sigma)=Tr_ad[(sum_a ad(Phi_a)^2)^2 ad(Sigma)^4]',
        exact_principal_branch_reduction='I=1080(Tr5 Sigma^2)^2+960 Tr5 Sigma^4',
        exact_quartic_shape_bound='Tr5 Sigma^4 >= (7/30)(Tr5 Sigma^2)^2, equality precisely2+3 eigenvalues',
        stationary_two_value_ratios=two_value,stationary_three_value_ratios=['1/4','1/2'],
        mixed_minimum_at_norm30=1173600,numeric_adjoint_trace_control=mixed,
        bounded_completion='V16=Vren+eta*(I-1304||Sigma||^4)^2, eta>0; every term is nonnegative and the explicit J,Y6 configuration is a zero.',
        exact_branch_selection='On the supplied principal-SU2 branch with [Sigma,J]=0, V16=0 iff Sigma is SU5-conjugate to +/-Y6. Thus this branch has exactly the SM Lie algebra.',
        scalar_shape_softness='The squared selector starts at fourth order in the11 former physical flat directions; it selects the orbit without giving those modes positive quadratic masses.',
        remaining_input='The principal-SU2 embedding branch, scales, coefficients and the added higher-degree interaction are supplied. Other SU2 embedding branches are not excluded; loops, chiral kinetic matter, gravity and vacuum energy remain open.',
        scope='Constructive globally nonnegative degree16 E8xSO3-invariant EFT with exact3+2 selection on its specified principal branch. No UV renormalizability or globally unique physical vacuum is claimed.')

def main():
    functions=[projection_certificate,coupled_certificate,covariance_certificate,adjoint_higgs_certificate,selection_certificate]
    out=dict(pass_ids=list(range(11721,11726)),schema='w33.coherent-vacuum-gauge-bridge.v1')
    for i,f in zip(out['pass_ids'],functions):out[str(i)]=f();print(i,out[str(i)]['status'],flush=True)
    out['status']='PASS'
    out['source_sha256']=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
    OUT.write_text(json.dumps(out,indent=2)+'\n')

if __name__=='__main__':main()
