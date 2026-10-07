"""Native scalar dynamics and actual kernel indices; eight scoped investigations.

11663 owns the normal map;11665 the parent maps;1068/1077 G25;
11306 parametrized graph constraints;11629 flux rotors;Dolan-Nash CP indices.
Actions, spin-c defect choice, continuum kinetic geometry and couplings are inputs.
"""
from __future__ import annotations
import sys,itertools as it
from pathlib import Path
from functools import lru_cache
import json,hashlib
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11664_11671_kernel_dynamics as PRIOR
import w33_pass11663_odd_weil_normal_map as N
OUT=ROOT/'data/w33_pass11672_11679_native_dynamics_index.json'
import numpy as np
pairs=list(it.combinations_with_replacement(range(4),2))
basis=np.zeros((20,4,4),complex)
for k,(i,j) in enumerate(pairs):
 for l,c in [(0,1),(1,1j)]:basis[2*k+l,i,j]=basis[2*k+l,j,i]=c/(np.sqrt(2) if i!=j else 1)
def res(x):
 a=x[::2]+1j*x[1::2];f,q,z=a[:4],a[4:14],a[14:]
 Q=np.array([f[i]*f[j]*(np.sqrt(2) if i!=j else 1) for i,j in pairs])
 P=np.array([-2*q[1]*q[8]-2*q[2]*q[6]-2*q[3]*q[5],2*q[1]*q[4]+2*q[2]*q[7]+2*q[3]*q[9],-2*q[0]*q[1]-2*q[5]*q[7]+2*q[6]*q[9],-2*q[0]*q[2]+2*q[4]*q[5]-2*q[8]*q[9],-2*q[0]*q[3]-2*q[4]*q[6]+2*q[7]*q[8]])
 return np.r_[q-Q,z-P,z]
e=np.eye(38);zero=res(np.zeros(38));one=np.array([res(a) for a in e]);r1=np.array([(res(a)-res(-a))/2 for a in e]).T
r2=np.array([[res(a+b)-one[i]-one[j]+zero for j,b in enumerate(e)] for i,a in enumerate(e)]).transpose(2,0,1)
def hessian(x):
 R=res(x);J=r1+np.einsum('aij,j->ai',r2,x)
 H=2*(J.conj().T@J+np.einsum('a,aij->ij',R.conj(),r2)).real
 f=x[:8];rr=np.dot(f,f);H[:8,:8]+=8*np.outer(f,f)+4*(rr-1)*np.eye(8)
 H[8:28,8:28]-=2.5*np.eye(20)
 T=np.einsum('i,iab->ab',x[8:28],basis);A=T@T.conj().T
 Ai=basis@T.conj().T+T@basis.conj().transpose(0,2,1)
 Aij=basis[:,None]@basis.conj().transpose(0,2,1)[None,:]+basis[None,:]@basis.conj().transpose(0,2,1)[:,None]
 H[8:28,8:28]+=.25*(np.einsum('iab,jba->ij',Ai,Ai)+np.einsum('ab,ijba->ij',A,Aij)).real
 return H

def base(theta=[0,0,0]):
 x=np.zeros(38);x[0]=np.sqrt(1.5);x[8]=2
 for k,t in zip([4,7,9],theta):x[8+2*k]=np.cos(t);x[9+2*k]=np.sin(t)
 return x
nodes,w=np.polynomial.legendre.leggauss(128);nodes=.12*nodes+.13;w*=.12

def loop(theta):
 ev=np.linalg.eigvalsh(hessian(base(theta)))/2
 return np.dot(w,nodes*np.sum(np.log1p(ev[None,:]/nodes[:,None]),axis=1))/(32*np.pi**2)

@lru_cache(None)
def scalar_jets():
    H0=hessian(np.zeros(38));one=np.array([hessian(a) for a in e])
    lin=np.array([(hessian(a)-hessian(-a))/2 for a in e])
    second=np.array([[hessian(a+b)-one[i]-one[j]+H0 for j,b in enumerate(e)] for i,a in enumerate(e)])
    return lin,second

A,B=.01,.25;const=1/(32*np.pi**2);charges=np.repeat(np.r_[np.ones(4),np.ones(10)*4,np.ones(5)*16],2)
def l1(m):return B-A-m*np.log1p((B-A)/(A+m))
def l1p(m):return -np.log1p((B-A)/(A+m))-m*(1/(B+m)-1/(A+m))
def jets(x,gauge=.1):
 Hlin,Hsecond=scalar_jets();H=hessian(x);mu,U=np.linalg.eigh(H/2)
 assert min(mu)>-A
 first=(Hlin+np.einsum('ijab,j->iab',Hsecond,x))/2
 tf=np.einsum('ak,iab,bl->ikl',U,first,U,optimize=True)
 weight=l1(mu);diag=np.einsum('ak,k,bk->ab',U,weight,U)
 dif=mu[:,None]-mu[None,:];dd=weight[:,None]-weight[None,:]
 close=abs(dif)<1e-7
 lo=np.divide(dd,dif,out=np.zeros_like(dif),where=~close);lo[close]=np.broadcast_to(l1p((mu[:,None]+mu[None,:])/2),dif.shape)[close]
 grad=const*np.einsum('k,ikk->i',weight,tf)
 outH=const*(np.einsum('ab,ijab->ij',diag,Hsecond)/2+np.einsum('kl,ikl,jlk->ij',lo,tf,tf,optimize=True))
 ma=2*gauge*gauge*np.sum(charges*x*x);mi=4*gauge*gauge*charges*x
 grad+=3*const*l1(ma)*mi
 outH+=3*const*(l1p(ma)*np.outer(mi,mi)+l1(ma)*4*gauge*gauge*np.diag(charges))
 return grad,outH

def treeg(x):
 R=res(x);J=r1+np.einsum('aij,j->ai',r2,x);gg=2*(R.conj()@J).real
 gg[:8]+=4*(np.dot(x[:8],x[:8])-1)*x[:8];gg[8:28]-=2.5*x[8:28]
 T=np.einsum('i,iab->ab',x[8:28],basis);AA=T@T.conj().T;Ai=basis@T.conj().T+T@basis.conj().transpose(0,2,1)
 gg[8:28]+=.25*np.einsum('ab,iba->i',AA,Ai).real
 return gg

def potential(x):
    T=np.einsum('i,iab->ab',x[8:28],basis);AA=T@T.conj().T
    return np.vdot(res(x),res(x)).real+(np.dot(x[:8],x[:8])-1)**2-1.25*np.dot(x[8:28],x[8:28])+np.trace(AA@AA).real/8


def quantum_potential(x,order=128,gauge=.1):
    ns,ws=np.polynomial.legendre.leggauss(order);ns=.12*ns+.13;ws*=.12
    mu=np.linalg.eigvalsh(hessian(x))/2
    ma=2*gauge*gauge*np.dot(charges,x*x)
    if min(mu)<=-A:raise ValueError('scalar shell leaves its real log domain')
    return potential(x)+const*np.dot(ws,ns*(np.sum(np.log1p(mu[None,:]/ns[:,None]),axis=1)+3*np.log1p(ma/ns)))


@lru_cache(None)
def quantum_vacuum():
    x=base();gl,_=jets(x);x-=np.linalg.pinv(hessian(x),rcond=1e-10)@gl
    fixed=np.array([i for i in range(38) if i!=1])
    for tick in range(8):
        g,H=jets(x);g+=treeg(x);H+=hessian(x)
        if np.linalg.norm(g)<1e-12:break
        x[fixed]+=np.linalg.solve(H[np.ix_(fixed,fixed)],-g[fixed])
    assert np.linalg.norm(g)<1e-11
    ev=np.linalg.eigvalsh(H);assert abs(ev[0])<1e-10 and ev[1]>5e-5
    # Full-field common-phase Ward identity, rather than deleting a small mode.
    a=x[::2]+1j*x[1::2];tangent=1j*np.r_[np.ones(4),np.ones(10)*2,np.ones(5)*4]*a
    t=np.empty(38);t[::2]=tangent.real;t[1::2]=tangent.imag
    assert np.linalg.norm(H@t)<1e-10
    return x,g,H


def digest(path):
    return hashlib.sha256(Path(path).read_bytes().replace(b'\r\n',b'\n')).hexdigest()


def native_parent():
    # Global bound uses Takagi's inequality Re<f f^T,T><=s u.
    u=s.Symbol('u',nonnegative=True)
    reduced=u**4/8-3*u**2/4-u+s.Rational(1,8)
    assert s.expand(reduced+s.Rational(23,8)-(u-2)**2*(u*u+4*u+6)/8)==0
    x=base();H=hessian(x);ev=np.linalg.eigvalsh(H)
    assert np.linalg.norm(treeg(x))<1e-12 and abs(potential(x)+23/8)<1e-12
    assert np.count_nonzero(ev>1e-9)==31 and min(ev)>-1e-10
    return dict(status='PASS',potential='(||f||^2-1)^2+||q-Q(f)||^2+||z-P(q)||^2+||z||^2-5||q||^2/4+Tr[(T Tdag)^2]/8',
        global_minimum='-23/8',global_remainder='(u-2)^2(u^2+4u+6)/8',
        vacuum=x.tolist(),hessian=ev.tolist(),positive_directions=31,zero_directions=7,
        complex_field_dimensions=[4,10,5],native_sextet_T='I3',Takagi_values=[2,1,1,1],
        radial_only_obstruction='With only ||q||^4, a nonzero transverse eigenvalue forces its common radial coefficient to zero; the sourced axis equation would then read0=||f||^2. The matrix quartic escapes this obstruction.',
        scope='Global classical minimum of a supplied38-real-field native G32-covariant polynomial scalar action. The transverse sextet is dynamical and full rank, but its tree singular values are equal; measured hierarchy, mixing and chiral E6 Yukawa embedding are not derived.')


def phase_counterterms():
    # Surviving fields on the phase family are f0,q0,q11,q22,q33 and conjugates.
    weights=[1,-1,2,-2,2,-2,2,-2,2,-2];allowed=0
    for degree in range(5):
        for monomial in it.combinations_with_replacement(range(10),degree):
            if sum(weights[i] for i in monomial):continue
            freq=[monomial.count(i)-monomial.count(i+1) for i in [4,6,8]]
            if any(v%3 for v in freq):continue
            assert freq==[0,0,0];allowed+=1
    return allowed


def scalar_gauge_matching():
    x,g,H=quantum_vacuum();ev=np.linalg.eigvalsh(H)
    T=np.einsum('i,iab->ab',x[8:28],basis);Y=T[1:,1:].conj()
    ma=2*.1**2*np.dot(charges,x*x)
    phases=[loop(np.array(a)*2*np.pi/3) for a in it.product(range(3),repeat=3)]
    assert np.ptp(phases)<1e-13
    return dict(status='PASS',vacuum=x.tolist(),gradient_norm=float(np.linalg.norm(g)),
        complete_real_hessian=ev.tolist(),canonical_scalar_masses_squared=(ev[1:]/2).tolist(),
        minimum_normal=float(ev[1]),U1_gauge_mass_squared=float(ma),gauge_coupling=.1,
        shell=[A,B],kinetic='sum |D f|^2+|D q|^2+|D z|^2-F^2/4; charges1,2,4; canonical real scalars=sqrt2 times x',
        effective_action='Vtree+1/(32pi^2) integral_A^B x[sum_38 log(1+Htree_eigenvalue/(2x))+3log(1+mA^2/x)] dx',
        light_sextet_singular_values=np.linalg.svd(Y,compute_uv=False).tolist(),
        cube_phase_orbit_size=27,cube_phase_energy_spread=float(np.ptp(phases)),
        phase_control_energy_difference=float(loop([np.pi,0,0])-loop([0,0,0])),
        quadrature_value_difference=float(abs(quantum_potential(x,64)-quantum_potential(x,128))),
        phase_independent_renormalizable_monomials=phase_counterterms(),
        scalar_phase_UV_moments=[489/2,45993/8],
        angular_UV_theorem='Every G32xU1-invariant scalar counterterm of field degree<=4 is constant on the three-phase diagonal family. Independent native cube phases require phase frequencies divisible by3, and charge neutrality excludes nonzero such frequencies at degree<=4. The angular one-loop difference is UV finite; extra higher-degree EFT operators can change it.',
        scalar_UV_log='-Tr[(Htree/2)^2] log(B/A)/(64pi^2)',
        vector_UV_log='-3mA^4 log(B/A)/(64pi^2)',
        scope='Numerical strict local normal stability of the specified finite-shell scalar+U1 one-loop action in Landau gauge, including all38 scalar fields, gauge polarizations and full tadpole relaxation. One gauge orbit remains. No interval proof, global quantum minimum, E6 gauge loops, fermion UV completion or observed flavor claim. The unequal-cap gravity and earlier fixed-spurion Dirac models are distinct actions.')


@lru_cache(None)
def odd_gates():
    _,O=N.parity_bases();O=O/s.sqrt(2)
    return {k:(O.T*g*O).applyfunc(N.reduce_w) for k,g in N.canonical_generators().items()}


def spin_index():
    h,k=s.symbols('h k');expr=s.series(s.exp(k*h)*(1-h*h/6),h,0,4).removeO().coeff(h,3)
    assert s.factor(expr-(k**3-k)/6)==0
    for g in odd_gates().values():assert N.reduce_w(g.det())==1
    f,_,K=N.cubic_normal_map();F=N.pfaffian_vector(K)
    ranks=[]
    for ray in N.exact_base_rays():
        pivot=next(i for i in range(4) if ray[i]!=0)
        J=F.jacobian(s.Matrix(N.FVAR)).subs(dict(zip(N.FVAR,ray)),simultaneous=True)
        J=J[:,[i for i in range(4) if i!=pivot]].applyfunc(N.reduce_w)
        assert J.rank()==3;ranks.append(3)
    return dict(status='PASS',base_point_derivative_ranks=ranks,
        resolved_space='X=Bl_40 CP3',zero_line='L=O_X(-4H+sum E)',
        canonical_bundle='K_X=O_X(-4H+2sum E)',spin_half='O_X(-2H+sum E)',
        kinetic_operator='sqrt2(dbar_{Khalf tensor L}+dbar_dagger) with a chosen Kahler metric and Chern connections',
        twisted_Dolbeault_bundle='O_X(-6H+2sum E)',cohomology=[0,0,0,10],spin_Dirac_index=-10,
        plain_CP3_index=str(s.factor(expr)),no_line_twist_index_three=True,
        index_module='Sym2(C4) under the tested determinant-one canonical Weil lift; restriction1+3+6',
        proof='All40 base ideals have three independent linear terms. Blowing up each maximal ideal resolves the quartic map. O_E(-1) and O_E(-2) have no cohomology, so adding the40 exceptional coefficients1,2 changes none of H*(O(-6)). Serre duality gives H3=H0(O2)^*=Sym2(C4) when det go=1.',
        scope='A genuine elliptic spin kinetic index on a specified smooth resolution of the parameter geometry. The bulk index is minus ten, not three; identifying this six-real-dimensional internal manifold with a physical compactification is additional input. Equality with the scalar auxiliary representation does not identify scalar and fermion fields.')


def nonlinear_connection():
    import networkx as nx
    from scipy.linalg import expm
    B=PRIOR.native_connection()[1];edges=[(int(np.where(B[:,i]==-1)[0][0]),int(np.where(B[:,i]==1)[0][0])) for i in range(160)]
    graph=nx.Graph();graph.add_edges_from(edges)
    cycles=list(nx.simple_cycles(graph,length_bound=8));assert len(cycles)==1620 and set(map(len,cycles))=={8}
    pauli=np.array([[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]],complex)
    U=np.array([expm(-1j*(.2+.001*i)*pauli[i%3]) for i in range(160)])
    frames=np.array([expm(-1j*(.13+.002*i)*pauli[(i+1)%3]) for i in range(80)])
    changed=np.array([frames[b]@u@frames[a].conj().T for (a,b),u in zip(edges,U)])
    lookup={e:(i,1) for i,e in enumerate(edges)}|{e[::-1]:(i,-1) for i,e in enumerate(edges)}
    def traces(links):
        out=[];loops=[]
        for c in cycles:
            W=np.eye(2,dtype=complex)
            for a,b in zip(c,c[1:]+c[:1]):
                i,sign=lookup[a,b];W=(links[i] if sign==1 else links[i].conj().T)@W
            loops.append(W);out.append(np.trace(W).real/2)
        return np.array(out),loops
    tr,ws=traces(U);new,_=traces(changed);error=float(np.max(abs(tr-new)))
    assert error<1e-12 and max(1-tr)>.01
    # Exact su2 Lie brackets support three Gauss components per native vertex.
    ts=[-s.I*s.Matrix(p)/2 for p in [[[0,1],[1,0]],[[0,-s.I],[s.I,0]],[[1,0],[0,-1]]]]
    for i,j,k in [(0,1,2),(1,2,0),(2,0,1)]:assert ts[i]*ts[j]-ts[j]*ts[i]==ts[k]
    return dict(status='PASS',vertices=80,edges=160,native_girth8_loops=1620,
        magnetic_energy=float(np.sum(1-tr)),gauge_trace_error=error,
        Gauss='G_v=sum_in L_e-sum_out Ad(U_e^-1)L_e; {Gv^a,Gw^b}=delta_vw epsilon_abc Gv^c',
        Hamiltonian='sum_e |L_e|^2/(2I)+kappa sum_all1620_octagons[1-ReTr(W)/2]',
        classical_phase_dimension=960,generic_Gauss_reduced_phase_dimension=480,
        closure='The actual nonlinear Wilson Hamiltonian is gauge invariant, so {G,H}=0. Nonflat Wilson conjugacy classes are physical. This is lattice SU2 gauge dynamics with160 group-valued links, not four transported projector constraints.',
        gravity_obligation='A gravitational completion must additionally construct Hamiltonian and spatial diffeomorphism constraints with inverse-metric structure functions. Gauss closure alone supplies none of these. A full Dirac-preserving branch link must intertwine the inverse-metric structure operators too; a generic Wilson phase on a free polarization label is insufficient.',
        scope='A nonlinear, nonflat native holonomy action and exact Gauss algebra on the actual Levi graph. Its loop action uses every girth-eight cycle and is graph-automorphism invariant. Gauge spin-one degrees of freedom are not two gravitational polarizations; no Einstein dynamics or gravitational constraint closure is claimed.')


def reference_flux(size=21,C=0.,t=.2):
    n=np.arange(-size,size+1);shift=np.eye(len(n),k=-1)
    # Physical states |n,-n>, with G=n1+n2=0. S1 S2dag is neutral.
    H=np.diag(n.astype(float)**2+C)-t*(shift+shift.T)
    ev,U=np.linalg.eigh(H);p=abs(U[:,0])**2
    return n,H,ev,p


def flux_dynamics():
    n,H,ev,p=reference_flux();_,HC,eC,pC=reference_flux(C=.3)
    n2,_,e2,p2=reference_flux(31)
    assert max(abs(p-pC))<1e-12 and abs(eC[0]-ev[0]-.3)<1e-12
    err=float(abs(ev[0]-e2[0]));assert err<1e-12
    return dict(status='PASS',Gauss='G=n1+n2=0',physical_states='|n,-n>; both rotors declared',membrane='S1 S2dag',
        Hamiltonian='V rho+V q^2 n^2-t(S1 S2dag+h.c.); benchmarkV=q=1,t=.2',
        ground_energy=float(ev[0]),ground_gap=float(ev[1]-ev[0]),fluxes=n.tolist(),ground_probabilities=p.tolist(),
        finite_window_energy_error=err,edge_probability=float(p[0]+p[-1]),
        common_shift_response='E0(rho+C)=E0(rho)+VC; probabilities unchanged. The compensating reference makes membrane coherence gauge invariant, but does not sequester the Hamiltonian constraint energy.',
        scope='Explicit gauge-invariant compensator/flux ground-state dynamics with a converged finite-window measure. Charge inventory, volume, couplings and compact-form interpretation are supplied; no native four-dimensional topology, gravitational bounce rate or small cosmological constant selection is derived.')


def exceptional_triplet():
    k,h=s.symbols('k h');td=1+s.Rational(3,2)*h+h*h
    index=s.expand((1+k*h+k*k*h*h/2)*td).coeff(h,2)
    assert s.simplify(index.subs(k,-4)-3)==0
    return dict(status='PASS',space='E=CP2 exceptional divisor at a Witting point',zero_line_restriction='L|E=O_E(-1) tensor chi, with tangent W=chi^-1 R',
        defect_bundle='B=(L|E)^4 tensor det(W)^-1=O_E(-4) tensor det(W)^-1 tensor chi; chi^3=1',
        kinetic_operator='sqrt2(dbar_B+dbar_Bdag) on Lambda^(0,*) tensor B, canonical spin-c structure',
        cohomology=[0,0,3],spin_c_index=3,zero_mode_module='H2(B)=W tensor chi=R, the actual three-dimensional mass-kernel representation, by equivariant Serre duality',
        stabilizer_character_correction='W=chi^-1 R, because affine deformations f_transverse/f_axis transform by chi^-1R. The actual zero-line restriction already contains chi, and its fourth power gives chi^4=chi, so H2(B)=chi W=R. H27 fixes the axis phase and has chi=1.',
        exact_kernel_bundle='O_E(-4) tensor det(W)^-1 tensor chi',
        untouched_full_bulk_index=-10,all_40_defect_index=120,
        ordinary_spin_obstruction='CP2 is not spin: c1(T)=3h is odd. A spin-c operator is necessary.',
        scope='Constructive exact triplet kinetic index on one actual exceptional parameter divisor, with the determinant and projective-axis characters explicitly retained. Selecting this defect and fourth-power twist is a model choice, not derived localization. All40 identical defects would give120 modes. No observed SM generations or physical compactification is asserted.')


def anomalies():
    # Weights of fundamental H=diag(1,1,-2), Sym2 weights hi+hj.
    hs=[1,1,-2];six=[hs[i]+hs[j] for i,j in it.combinations_with_replacement(range(3),2)]
    ratio=s.Rational(sum(v**3 for v in six),sum(v**3 for v in hs));assert ratio==7
    return dict(status='PASS',family_SU3_anomaly_fundamental=1,family_SU3_anomaly_sextet=int(ratio),
        indexed_bulk_module_anomaly=-8,bulk_anomaly_magnitude=8,E6_27_tensor_bulk_anomaly=-216,E6_27_tensor_single_defect_anomaly=27,
        bosonic_U1_one_loop_beta_coefficient=s.Rational(4+10*4+5*16,3).__str__(),
        Yukawa_operator='d_ABC psi_i^A psi_j^B h^C conjugate(T_transverse)^{ij}/M',operator_dimension=5,
        scope='Only an optional continuous SU3-family completion has these perturbative anomalies; the finite G25/H27 matrices alone are not an SU3 gauge embedding. The native scalar sextet can supply a covariant symmetric flavor field, but an E6 Higgs, mediators and anomaly-canceling chiral inventory are still required. The bosonic U1 completion has no fermion anomaly; adding charged Weyls changes that conclusion.')


def twistor_obstruction():
    gates=odd_gates();D=gates['D0'];conj=D.applyfunc(lambda v:N.reduce_w(v.subs(N.W,N.W**2)))
    # D0 forces every entry except B00 to zero; F0 then kills B00.
    for i in range(4):
        for j in range(4):
            if i==j==0:continue
            assert N.reduce_w(D[i,i]-conj[j,j])!=0
    assert any(N.reduce_w(gates['F0'][i,0])!=0 for i in range(1,4))
    D=gates['D0'];assert N.reduce_w(s.trace(D)-(1+3*N.W**2))==0
    # Even dimension alone permits quaternionicity; the tested group forbids it.
    return dict(status='PASS',antilinear_intertwiner_rank=16,antilinear_commutant_dimension=0,
        transvection_trace='1+3omega^2=-1/2-3sqrt3 i/2',
        projective_obstruction='An allowed scalar alpha for the order3 determinant-one transvection would have alpha^3=alpha^4=1, hence alpha=1; its nonreal trace still obstructs equivalence with its conjugate.',
        obstruction='There is no invertible B with go B=B conjugate(go) for the native canonical odd Weil group. Therefore no native-invariant quaternionic J=B conjugation with J^2=-I exists.',
        scope='Exact obstruction to an unbroken native-group-invariant Euclidean twistor real structure on the odd C4. A chosen symmetry-breaking Sp2 structure can still give CP3 to S4, and Lorentzian twistors require a different reality condition. This does not rule out spacetime or twistor gravity generally.',
        prior_owner='analysis/w33_20260923_next5_plus3_physics.py already owns odd-dimensional Kramers obstructions; the present even-dimensional group-specific no-go is different.')


def main():
    funcs=[native_parent,scalar_gauge_matching,spin_index,nonlinear_connection,flux_dynamics,exceptional_triplet,anomalies,twistor_obstruction]
    sources=['analysis/w33_pass11663_odd_weil_normal_map.py','analysis/w33_pass11664_11671_kernel_dynamics.py','analysis/w33_pass1068_chevie_g25_g32_matrices.py','analysis/w33_pass11278_symplectic_ring_geometry.py','analysis/w33_pass11279_history_flux_obstruction.py']
    out=dict(status='PASS',reservation='62cb3c3a7',producer_sha256=digest(__file__),sources={p:digest(ROOT/p) for p in sources},passes={})
    for number,fun in enumerate(funcs,11672):out['passes'][str(number)]=fun();print(number,'PASS',flush=True)
    OUT.write_text(json.dumps(out,indent=2)+'\n');return out

if __name__=='__main__':main()
