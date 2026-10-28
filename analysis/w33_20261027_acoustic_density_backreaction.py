"""Finite acoustic comparison current, full-Fock free response and 5D backreaction.

Prior owners: Pass12002, Oct27 gap_matter_radion and microscopic response.
Standard methods: spectral projector calculus, Lehmann response, Casimir EFT.
None is a complete native chiral measure or a derived gravitational theory.
"""
from pathlib import Path
from fractions import Fraction as F
from math import lcm
import sys,json
import numpy as np
import sympy as s
import mpmath as mp
from scipy.linalg import eigh,expm,expm_frechet,block_diag
from scipy.special import expit
from numpy.polynomial.legendre import leggauss
sys.path.insert(0,str(Path(__file__).resolve().parent))
import w33_20261027_native_operator_closure as native
import w33_pass12002_native_path_overlap as overlap
ROOT=Path(__file__).resolve().parents[1]


def spectral_projector(H,derivatives=()):
    ev,Q=eigh(H);p=(ev>0).astype(float);P=(Q*p)@Q.conj().T
    delta=ev[:,None]-ev[None,:];numer=p[:,None]-p[None,:]
    divided=np.zeros_like(delta);np.divide(numer,delta,out=divided,where=abs(delta)>1e-10)
    return P,[Q@(divided*(Q.conj().T@X@Q))@Q.conj().T for X in derivatives],float(min(abs(ev)))


def acoustic_operators(t=1.,a=0.,b=0.,representation='5'):
    rng=np.random.default_rng(27003);gamma,g5=overlap.gamma4();nc=5 if representation=='5' else 27
    def hermitian():
        X=rng.normal(size=(5,5))+1j*rng.normal(size=(5,5));X=(X+X.conj().T)/2
        return X-np.trace(X)*np.eye(5)/5
    def representation_generator(X):
        if nc==5:return X
        # Hermitian generator of exterior-square and conjugate blocks.
        E=np.eye(5);pairs=list(__import__('itertools').combinations(range(5),2));W=np.zeros((10,10),complex)
        for j,(u,v)in enumerate(pairs):
            Z=np.outer(X[:,u],E[:,v])-np.outer(X[:,v],E[:,u])
            Z+=np.outer(E[:,u],X[:,v])-np.outer(E[:,v],X[:,u])
            W[:,j]=[Z[c,d]for c,d in pairs]
        return block_diag(W,-X.conj(),np.zeros((1,1)),X,-X.conj(),np.zeros((1,1)))
    shifts=[np.zeros((2*nc,2*nc),complex)for _ in range(4)]
    tangent=[[np.zeros_like(shifts[0])for _ in range(4)]for _ in range(3)]
    for cell in range(2):
        for mu in range(4):
            Z=.10*hermitian();X=hermitian()if(cell,mu)==(0,0)else np.zeros((5,5))
            Y=hermitian()if(cell,mu)==(1,2)else np.zeros((5,5));Q=representation_generator(Z+a*X+b*Y)
            X=representation_generator(X);Y=representation_generator(Y);U=expm(1j*t*Q)
            derivatives=[1j*Q@U,expm_frechet(1j*t*Q,1j*t*X,compute_expm=False),expm_frechet(1j*t*Q,1j*t*Y,compute_expm=False)]
            dst=(cell+1)%2 if mu==0 else cell
            # Common real antiperiodic sign in first direction removes free
            # overlap zero modes without changing projector/measure identities.
            sign=-1 if mu==0 and cell==1 else 1
            rr=slice(cell*nc,(cell+1)*nc);cc=slice(dst*nc,(dst+1)*nc)
            shifts[mu][rr,cc]=sign*U
            for target,der in zip(tangent,derivatives):target[mu][rr,cc]=sign*der
    D,G5=overlap.wilson(shifts);H=G5@D;ders=[]
    for variations in tangent:
        dD=np.zeros_like(D)
        for g,dT in zip(gamma,variations):dD-=.5*(np.kron(np.eye(4)-g,dT)+np.kron(np.eye(4)+g,dT.conj().T))
        ders.append(G5@dD)
    return H,ders,G5


def curvature(P,A,B):return float(np.real(1j*np.trace(P@(A@B-B@A))))


def acoustic_comparison(representation='5'):
    def current(a,b,order):
        nodes,weights=leggauss(order);answer=np.zeros(2);gap=10.
        for t,w in zip((nodes+1)/2,weights/2):
            H,ders,_=acoustic_operators(t,a,b,representation);P,(Pt,Pa,Pb),g=spectral_projector(H,ders)
            answer+=w*np.array([curvature(P,Pt,Pa),curvature(P,Pt,Pb)]);gap=min(gap,g)
        return answer,gap
    H,ders,G5=acoustic_operators(representation=representation);P,(_,Pa,Pb),gap=spectral_projector(H,ders)
    omega=curvature(P,Pa,Pb);eps=.0002
    bbp,_=current(eps,0,16);bbm,_=current(-eps,0,16);bap,_=current(0,eps,16);bam,_=current(0,-eps,16)
    curl=(bbp[1]-bbm[1]-bap[0]+bam[0])/(2*eps)
    B8,g8=current(0,0,8);B16,g16=current(0,0,16)
    Hp,_,_=acoustic_operators(a=eps,representation=representation);Hm,_,_=acoustic_operators(a=-eps,representation=representation)
    Pp,_,_=spectral_projector(Hp);Pm,_,_=spectral_projector(Hm)
    P0,_,_=spectral_projector(acoustic_operators(t=0,representation=representation)[0])
    rng=np.random.default_rng(33);nc=len(H)//8;diag=rng.normal(size=5);diag-=np.mean(diag)
    g=np.diag(np.exp(.2j*diag))
    if nc==27:g=block_diag(native.old.wedge2(g),g.conj(),np.eye(1),g,g.conj(),np.eye(1))
    gauge=np.kron(np.eye(4),block_diag(g,np.eye(nc)))
    corners=[(-.02,-.02),(.02,-.02),(.02,.02),(-.02,.02),(-.02,-.02)]
    nodes,weights=leggauss(4);line_integral=0.
    for start,end in zip(corners,corners[1:]):
        direction=np.array(end)-start
        for z,w in zip((nodes+1)/2,weights/2):
            point=np.array(start)+z*direction;oneform,_=current(*point,8)
            line_integral+=w*float(oneform@direction)
    def holonomy(steps):
        H0,_,_=acoustic_operators(a=corners[0][0],b=corners[0][1],representation=representation)
        e,U=eigh(H0);F=U[:,e>0];initial=F.copy()
        for start,end in zip(corners,corners[1:]):
            for z in np.linspace(0,1,steps+1)[1:]:
                point=np.array(start)+z*(np.array(end)-start)
                Pt,_,_=spectral_projector(acoustic_operators(a=point[0],b=point[1],representation=representation)[0])
                gram=F.conj().T@Pt@F;e,U=eigh(gram);assert min(e)>.9
                F=Pt@F@(U/np.sqrt(e))@U.conj().T
        phase,_=np.linalg.slogdet(initial.conj().T@F)
        return float(np.angle(phase))
    loop12=holonomy(12);loop24=holonomy(24)
    return dict(representation=representation,dimension=len(H),projector_rank=int(round(np.trace(P).real)),
        endpoint_gap=gap,sampled_radial_gap_min=min(g8,g16),projector_curvature=omega,comparison_current=B16.tolist(),
        exterior_derivative_current=curl,curvature_identity_error=abs(curl-omega),quadrature_8_vs_16_error=float(max(abs(B8-B16))),
        Frechet_derivative_finite_difference_error=float(np.max(abs((Pp-Pm)/(2*eps)-Pa))),
        projector_tangent_identity_error=float(np.max(abs(P@Pa+Pa@P-Pa))),
        free_reference_local_gauge_commutator=float(np.linalg.norm(P0@gauge-gauge@P0)),
        finite_rectangle_current_integral=line_integral,Kato_rectangle_phase_12=loop12,Kato_rectangle_phase_24=loop24,
        finite_rectangle_phase_error=abs(np.angle(np.exp(1j*(loop24-line_integral)))),Kato_discretization_change=abs(loop24-loop12),
        implemented='b_eta=i integral_0^1 Tr P(t)[d_t P(t),d_eta P(t)]dt on a finite radial acoustic comparison; Frechet derivatives are spectral divided differences.',
        boundary='A finite chart/comparison current only. Not the coarse/fine refinement tower, anomaly-divergence correction, volume-uniform locality or full closed-loop phase proof. The free acoustic reference fails to commute with local gauge transformations, so the onsite-heavy-frame argument cannot be transferred.',
        primary='https://arxiv.org/html/2610.09093v1#S5')


def harmonic_response_identity():
    """Exact rational tensors underlying the observed ALL-temperature shape law."""
    from fractions import Fraction as F
    B,V,edges,_=native.geometry();b=s.Matrix(B[:,1:]);h=s.Matrix(V)-b*(b.T*b).inv()*b.T*s.Matrix(V)
    den=int(s.ilcm(*[z.q for z in h]));hi=np.array(h*den,dtype=np.int64);M=hi.T@hi
    K=np.zeros((27,27),dtype=np.int64)
    for u,v in edges:K[u,v]=K[v,u]=-1
    I=np.eye(27,dtype=np.int64);projectors=[np.ones_like(K),-(K+10*I)@(K-5*I),(K+10*I)@(K+I)];pd=[27,54,90]
    currents=[]
    for a in range(4):
        A=np.zeros_like(K)
        for e,(u,v)in enumerate(edges):A[v,u]=-hi[e,a];A[u,v]=hi[e,a]
        assert not (A@np.ones(27,dtype=np.int64)).any();currents.append(A)
    coefficients=[]
    for i in range(3):
        row=[]
        for j in range(3):
            tensor=np.array([[-int(np.trace(projectors[i]@X@projectors[j]@Y))for Y in currents]for X in currents],dtype=np.int64)
            coefficient=F(int(tensor[0,0]),int(M[0,0])*pd[i]*pd[j])
            assert np.array_equal(tensor*coefficient.denominator,M*(coefficient.numerator*pd[i]*pd[j]))
            row.append(str(coefficient))
        coefficients.append(row)
    assert coefficients==[['0','0','0'],['0','5/3','1/6'],['0','1/6','0']]
    # Independent unimodular coordinate realization of the same identities.
    T=np.array([[1,1,0,0],[0,1,0,0],[0,0,1,1],[0,0,0,1]],dtype=np.int64)
    changed=[sum((int(T[k,j])*currents[k]for k in range(4)),np.zeros_like(K))for j in range(4)]
    tensor=np.array([[-int(np.trace(projectors[1]@X@projectors[2]@Y))for Y in changed]for X in changed])
    assert np.array_equal(6*tensor,(T.T@M@T)*pd[1]*pd[2])
    return dict(harmonic_denominator=den,metric_exact=[[str(z)for z in row]for row in(h.T*h).tolist()],
        energy_levels=[-10,-1,5],spectral_projector_denominators=pd,current_block_tensor_coefficients=coefficients,
        tensor_definition='Tr(P_a J_i P_b J_j)=c_ab M_ij, M=h^T h. P_a exact spectral projectors; J_i=i A_i with real skew A_i.',
        all_T_mu_formulas=dict(electric='(f(-1)-f(5))*M/648',regular_zero_frequency='(4*f(-10)+5*f(-1)-9*f(5))*M/54',
            thermal_static='regular_zero_frequency-(5/(3T))*f(-1)*(1-f(-1))*M',zero_Matsubara_jump='-(5/(3T))*f(-1)*(1-f(-1))*M'),
        gapped_zero_temperature=dict(chemical_potential_interval=[-1,5],filled_orbitals=21,static_coefficient='1/6',electric_coefficient='1/648',ratio_static_to_electric='108'),
        proof='Exact rational harmonic projection, polynomial spectral projectors and integer tensor traces. The ground-current block vanishes. Only the(-1,5) cross block contributes to the regular electric coefficient, with energy difference6; thermal degeneracy contributes only the displayed static jump. An independent unimodular basis verifies covariance.',
        boundary='Four harmonic zero-spatial-momentum probes on one finite27-site graph. No nonzero-spatial-momentum polarization, spatial refinement, interacting finite-density theorem, spin/chirality or physical3+1 limiting speed.')


def density_response(T=1.,mu=-1.):
    B,V,edges,h=native.geometry();K=np.zeros((27,27))
    for a,b in edges:K[a,b]=K[b,a]=-1
    ev,Q=eigh(K);f=expit((mu-ev)/T)if T else(ev<mu).astype(float);rho=(Q*f)@Q.T;chi=np.random.default_rng(27).normal(size=27)
    alpha=np.column_stack((h,B@chi));currents=[]
    # B[e] has -1 at a,+1 at b, so alpha_gauge=chi_b-chi_a.
    contact=np.zeros((6,6))
    for a in range(5):
        J=np.zeros((27,27),complex)
        for e,(u,v)in enumerate(edges):J[v,u]=-1j*alpha[e,a];J[u,v]=1j*alpha[e,a]
        currents.append(Q.T@J@Q)
    currents.append(Q.T@np.diag(chi)@Q)
    for e,(u,v)in enumerate(edges):contact[:5,:5]+=2*rho[u,v]*np.outer(alpha[e],alpha[e])
    delta=ev[:,None]-ev[None,:];df=f[:,None]-f[None,:];nondeg=abs(delta)>1e-8
    W0=np.zeros_like(delta);np.divide(df,delta,out=W0,where=nondeg)
    derivative=-f*(1-f)/T if T else np.zeros_like(f);W0[~nondeg]=np.broadcast_to(derivative[:,None],delta.shape)[~nondeg]
    def bubble(W):return np.array([[np.sum(W*A*Z.T)for Z in currents]for A in currents])
    static=contact+bubble(W0);regular=np.zeros_like(delta);np.divide(df,delta,out=regular,where=nondeg)
    limit=contact+bubble(regular)
    ecoeff=np.zeros_like(delta);np.divide(-df,delta**3,out=ecoeff,where=nondeg)
    electric=bubble(ecoeff)[:4,:4].real;target=h.T@h
    scale=float(np.sum(electric*target)/np.sum(target*target));error=float(np.linalg.norm(electric-scale*target)/max(np.linalg.norm(electric),1e-100))
    samples=[]
    for n in (1,2):
        w=2*np.pi*T*n if T else .2*n;W=df/(delta+1j*w);Pi=contact+bubble(W);g=np.array([0,0,0,0,1,-w])
        # This spectral convention gives the right null vector(1,-omega).
        ward=float(np.max(abs(Pi@g)));assert ward<1e-8
        samples.append(dict(bosonic_n=n if T else None,omega=w,Ward_error=ward,pure_spatial_gauge_response=float(Pi[4,4].real),
            mixed_spatial_density=[float(Pi[4,5].real),float(Pi[5,4].real)],density_response=float(Pi[5,5].real)))
    static_scale=float(np.sum(static[:4,:4].real*target)/np.sum(target*target))
    return dict(T=T,mu=mu,mean_particles=float(sum(f)),static_metric_scale=static_scale,static_harmonic=static[:4,:4].real.tolist(),
        electric_harmonic=electric.tolist(),electric_metric_scale=scale,electric_metric_shape_error=error,
        zero_Matsubara_vs_dynamic_limit_norm=float(np.linalg.norm((static-limit)[:4,:4])),
        static_gauge_Ward_error=float(np.max(abs(static[4]))),frequency_samples=samples,
        scope='Exact full-Fock grand-canonical FREE spinless27-site fermions. No Hubbard interaction. Thermal medium and finite geometry are not Lorentz-invariant vacuum or a continuum light-cone derivation.')


def rational_bloch_shifted(t,cut='71/25'):
    """Exact nearest-edge Bloch matrix at rational unit-circle coordinates."""
    B,V,edges,_=native.geometry();t=list(map(F,t));phase=[((1-x*x)/(1+x*x),2*x/(1+x*x))for x in t]
    real=[[F(0)for _ in range(27)]for _ in range(27)];imag=[[F(0)for _ in range(27)]for _ in range(27)]
    def multiply(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
    for e,(a,b)in enumerate(edges):
        z=(F(-1),F(0))
        for p,n in zip(phase,V[e]):
            factor=p if n>=0 else(p[0],-p[1])
            for _ in range(abs(int(n))):z=multiply(z,factor)
        real[b][a]=real[a][b]=z[0];imag[b][a]=z[1];imag[a][b]=-z[1]
    for i in range(27):real[i][i]=-F(cut)
    den=lcm(*(x.denominator for row in real+imag for x in row))
    return np.array([[int(x*den)for x in row]for row in real],dtype=object),np.array([[int(x*den)for x in row]for row in imag],dtype=object),den


def verify_inertia_certificate(record):
    A,B,den=rational_bloch_shifted(record['rational_t'],record['cut_exact']);X=np.array(record['integer_basis_real'],dtype=object);Y=np.array(record['integer_basis_imag'],dtype=object)
    U=A@X-B@Y;V=A@Y+B@X;R=X.T@U+Y.T@V;I=X.T@V-Y.T@U
    assert np.array_equal(R,R.T)and np.array_equal(I,-I.T)
    radii=[sum(abs(int(R[i,j]))+abs(int(I[i,j]))for j in range(27)if i!=j)for i in range(27)]
    signs=[];margins=[]
    for i,radius in enumerate(radii):
        value=int(R[i,i]);assert abs(value)>radius
        signs.append(1 if value>0 else-1);margins.append(abs(value)-radius)
    # A strictly sign-separated Gershgorin homotopy to the diagonal preserves
    # inertia. Nonsingularity also proves that the proposed basis is invertible.
    return dict(negative=signs.count(-1),positive=signs.count(1),
        normalized_margin_exact=str(F(min(margins),den*record['basis_scale']**2)))


def cover_filling_counterexample():
    records=[]
    for k in [[1.65388538,1.43037726,-2.06711778,1.16047372],[.99440494,2.03769984,-1.85875248,1.19274570]]:
        t=[F(float(np.tan(x/2))).limit_denominator(1000)for x in k]
        A,B,den=rational_bloch_shifted(t);H=np.array(A,float)/den+1j*np.array(B,float)/den
        ev,Q=eigh(H);scale=10**8
        rec=dict(rational_t=list(map(str,t)),cut_exact='71/25',basis_scale=scale,
            integer_basis_real=np.rint(Q.real*scale).astype(np.int64).tolist(),integer_basis_imag=np.rint(Q.imag*scale).astype(np.int64).tolist())
        rec['exact_inertia_certificate']=verify_inertia_certificate(rec);records.append(rec)
    assert records[0]['exact_inertia_certificate']['negative']==20
    assert records[1]['exact_inertia_certificate']['negative']==22
    return dict(cut_exact='71/25',certificates=records,
        conclusion='No global noninteracting insulating gap at filling21 for the actual nearest-edge infinite periodic cover. At one exact Bloch point lambda21>71/25; at another lambda22<71/25 (one-based indices). Therefore max_k lambda21(k)>min_k lambda22(k). The single-cell chemical-potential plateau(-1,5) does not extend to a21-band insulator.',
        proof='Rational Cayley coordinates exp(ik_j)=(1+i t_j)/(1-i t_j) give exact Gaussian-rational matrices. Floating eigensolvers only propose integer congruence bases. Exact sign-separated Gershgorin disks of Qdagger(H-cut)Q certify inertias20/7 and22/5. The diagonal homotopy preserves inertia and proves each basis nonsingular; Sylvester law transfers it to H-cut.',
        boundary='Exact obstruction for this fixed nearest-edge hopping kernel. Not all regulators/interactions/fillings. The harmonic finite-cell tensor identity remains valid and is a holonomy response, not a nonzero-momentum Maxwell magnetic stiffness.')


def backreaction():
    mp.mp.dps=45;z=mp.zeta(5);C=mp.mpf(3)/(64*mp.pi**6)
    def S(x):return mp.polylog(5,mp.exp(-x))+x*mp.polylog(4,mp.exp(-x))+x*x/3*mp.polylog(3,mp.exp(-x))
    records=[]
    inventory=[(4,2,'matter with classical gravity'),(4,7,'same matter plus graviton loop'),
        (8,7,'two Dirac fields plus scalars and graviton'),
        (8,79,'same two Dirac fields plus massless SU5 gauge fields'),
        (108,85,'supplied massive Dirac27 plus massless SU5 and twoU1 gauge fields')]
    for A,B,label in inventory:
        rec=dict(massive_fermion_weight=A,massless_boson_weight=B,label=label,has_minimum=A>B)
        if A>B:
            def shape(x):return A*S(x)-B*z
            def potential(x):return shape(x)/x**6
            def stationarity(x):return x*mp.diff(shape,x)-6*shape(x)
            root=mp.findroot(stationarity,(mp.mpf('.3'),mp.mpf('3')));R=root/(2*mp.pi)
            # m=1, M5=1000; flat-circle stress is reliable to leading order
            # when ell/R and M5 R are both large.
            M5=mp.mpf(1000);VJ=C*shape(root)/R**4;rho=VJ/(2*mp.pi*R)
            pressure=-(C*(-4*shape(root)+root*mp.diff(shape,root))/R**5)/(2*mp.pi)
            ell=mp.sqrt(-3*M5**3/rho);mass_ell2=-2*root**2*mp.diff(potential,root,2)/potential(root)
            assert abs(pressure+2*rho)<mp.mpf('1e-35')and mass_ell2>0
            rec.update(x=str(root),mR=str(R),rho5=str(rho),pressure5=str(pressure),circle_Einstein_stress_residual=str(pressure+2*rho),
                ell_over_R=str(ell/R),M5_R=str(M5*R),radion_mass_squared_times_ell_squared=str(mass_ell2))
        else:rec['proof']='Dp=6S-xSprime decreases from6zeta(5) to0. A<=B implies Vprime=[6Bzeta(5)-A Dp]/x^7>0 for all x>0: no finite stationary radius.'
        records.append(rec)
    return dict(samples=records,graviton_physical_polarizations=5,massless_SU5_gauge_polarizations=72,
        complete_test_inventory='Last control:27-component5D Dirac field contributes108 massive fermion degrees; SU5 gauge72, twoU1 gauge6, graviton5 and two massless scalars2 contribute85. This is supplied vectorlike5D matter, not a derived4D chiral spectrum.',
        equations='For AdS4(ell) x S1(R), M5^3 Gmunu=-rho5 gmunu gives3 M5^3/ell^2=-rho5; the55 equation requires p5=-2rho5. With rho5=VJ/(2piR), p5=-dVJ/dR/(2pi), this is R VJprime=2VJ, equivalently d(VJ/R^2)/dR=0.',
        radion_normalization='phi=sqrt(3/2) M4 log(R/Rstar), M4^2=2pi Rstar M5^3. Thus mphi^2 ell^2=-2 xstar^2 vsecond(xstar)/v(xstar), v=(A S-B zeta5)/x^6.',
        boundary='Supplied five-dimensional Einstein EFT and periodic fields; bulk cosmological constant renormalized to zero. Flat-circle one-loop stress on weakly curved product background is a leading derivative-expansion solution, not an exact curved-space effective action or native derivation of gravity. Graviton loop removes the previous minimal matter-only minimum; adding a second massive Dirac restores a conditional AdS minimum.',
        primary=['https://doi.org/10.1103/PhysRevD.28.772','https://doi.org/10.1140/epjc/s10052-014-3237-0'])


def run():return dict(schema='acoustic_density_and_backreaction_v1',acoustic=[acoustic_comparison(r)for r in ('5','27')],exact_harmonic_response=harmonic_response_identity(),density=[density_response(T,mu)for T in (.25,1.,2.)for mu in (-10.,-1.,2.)]+[density_response(0.,2.)],cover_filling=cover_filling_counterexample(),backreaction=backreaction())


if __name__=='__main__':
    d=run();(ROOT/'data/w33_20261027_acoustic_density_backreaction.json').write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d,indent=2))
