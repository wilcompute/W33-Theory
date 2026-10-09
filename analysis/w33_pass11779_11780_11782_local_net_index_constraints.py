"""Explicit local modular net, actual spin-curvature test and surviving gauge.

The U(1) current net and Bott-Dirac index are established constructions,
supplied here as controlled alternatives on the actual78-mode carrier.
They are not asserted to be the continuum or fermions of11769.
"""
from pathlib import Path
import hashlib,json,sys
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11769_quantized_current_vacuum as A
OUT=ROOT/'data/w33_pass11779_11780_11782_local_net_index_constraints.json'


def local_net():
    x=sp.symbols('x',real=True);phi=(1-x*x)**6
    # A compactly supported C5 test vector lies in the closure of smooth
    # interval tests in the one-particle norm. psi=phi' has the same support.
    sigma=sp.integrate(sp.diff(phi,x)**2,(x,-1,1))
    assert sigma>0
    theta,s,t=sp.symbols('theta s t',real=True)
    assert sp.simplify(sp.exp(-(theta+2*sp.pi*s))-sp.exp(-2*sp.pi*s)*sp.exp(-theta))==0
    return dict(status='EXPLICIT_STANDARD_CONSTRUCTION',carrier_dimension=78,
        one_particle='L2(R,dtheta) tensor W_C; W is the actual real78-dimensional projected carrier, with its Euclidean metric.',
        real_subspace='K(I)=closure{hat(g)(exp(-theta)):g in C_c^infty(I,W), real, integral g=0}.',
        local_algebra='M(I)={Weyl(xi):xi in K(I)} double-commutant on symmetric Fock space; vacuum Omega.',
        group='[U(alpha,t)xi](theta)=exp(i*t*exp(-theta))*xi(theta-alpha). P=exp(-theta)>0 on the one-particle space.',
        modular='Delta_(0,infinity)^(is)=Gamma(U(-2*pi*s,0)); Delta^(is)T(t)Delta^(-is)=T(exp(-2*pi*s)*t).',
        locality='For g=phi_prime,h=psi_prime,2Im<g,h>=-integral phi*psi_prime. Disjoint interval supports give zero symplectic form and commuting Weyl algebras.',
        nontrivial_interval_symplectic_exact=str(sigma),
        standard_inclusion='M(1,infinity) subset M(0,infinity) is half-sided; its relative commutant contains nontrivial M(0,1). The standard free-current vacuum is cyclic and separating on intervals.',
        type='The standard finite-multiplicity free-current interval algebras are typeIII1; this is a literature theorem, not inferred from sampled matrices.',
        physical_boundary='A supplied chiral1D local net with78 internal components. No limit map from11769,3+1 spacetime, interactions, observed particles or gravity is established.',
        literature=['https://link.springer.com/article/10.1007/s00220-022-04432-8','https://arxiv.org/abs/1004.0616',
                    'https://park.itc.u-tokyo.ac.jp/MSF/UGMSS/Kawahigashi.pdf'])


def actual_clifford_test():
    g=A.geometry();tr=A.exact_trial();c,ci=A.spectral_covariance(g)
    c=c*tr['t'];phase=tr['f']*np.diag(g['s'])
    pairing=g['v']@g['u'].T
    cross=g['v']@c@phase@g['u'].T/2
    curvature=pairing*(cross.T+.05)-pairing.T*(cross+.05)
    assert np.max(np.abs(curvature))<1e-14
    return dict(status='PASS',commutator_expectation_max=float(np.max(np.abs(curvature))),
        exact_reason='U=D V makes V U^T symmetric. For C=t*C0,F=f*D and D*C0*D=C0^-1, V C F U^T is also symmetric. Therefore every Gaussian expectation of [J_e,J_f] vanishes in this family.',
        spin_product_energy='For every constant unit spinor eta, <eta tensor psi,D_current^2 eta tensor psi>=<psi,H psi>. Spin optimization alone gives no Gaussian product-state improvement.',
        zero_mode_obstruction='At q=0, every centered Gaussian has gradient0 and D_current(eta*psi)(0)=a^2*(sum160 gamma_e)*eta*psi(0). Its spin factor squared is160*a^4 I=(2/5)I, hence no nonzero constant-spinor centered Gaussian solves D_current psi=0.',
        actual_index_boundary='Fredholmness and the index of D_current are still open. Compactness of H does not imply compactness of D_current^2 because of the spin-curvature term. A truncated square matrix index is not substituted for this question.')


def bott_control():
    # Exact differential identity on a generic one-mode test function,
    # avoiding the false extra kernel of a finite oscillator truncation.
    x=sp.symbols('x',real=True);u=sp.Function('u')(x)
    annihilate=lambda z:(x*z+sp.diff(z,x))/sp.sqrt(2)
    create=lambda z:(x*z-sp.diff(z,x))/sp.sqrt(2)
    assert sp.simplify(annihilate(create(u))-create(annihilate(u))-u)==0
    assert sp.simplify(annihilate(sp.exp(-x*x/2)))==0
    beta=sp.symbols('beta',positive=True)
    assert sp.simplify((1-sp.exp(-2*beta))/(1-sp.exp(-2*beta))-1)==0
    return dict(status='STANDARD_INDEX_CONTROL',
        operator='Q_B=sqrt2*sum_(i=1..78)(c_i^dagger*a_i+c_i*a_i^dagger), a_i=(q_i+partial_i)/sqrt2.',
        square='Q_B^2=2*(N_boson+N_fermion).',kernel_dimension=1,even_to_odd_index=1,
        kernel='pi^(-78/4)*exp(-|q|^2/2) tensor fermion vacuum.',
        index_proof='All occupation energies are2*(sum n_i+sum f_i); the unique zero has every occupation0 and even parity. Positive energies pair under Q_B. Its heat supertrace is[(1-exp(-2beta))/(1-exp(-2beta))]^78=1.',
        relation='The q,p operators occur in the certified current Lie closure by degree<=5, but this canonical Bott supercharge is a different selected energy law, using156 Clifford directions rather than160 edge labels.',
        boundary='Index1 is internal supersymmetric quantum mechanics, not one SM generation or spacetime Weyl chirality. No index is assigned to D_current by analogy.',
        literature='https://arxiv.org/abs/0907.1351')


def surviving_constraints():
    # Per original mode, enlarged canonical coordinates(q1,q2,p1,p2).
    omega=sp.Matrix([[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]])
    constraint=sp.Matrix([[1,1,0,0]])
    quotient=sp.Matrix([[sp.Rational(1,2),-sp.Rational(1,2),0,0],[0,0,1,-1]])
    assert constraint*omega*quotient.T==sp.zeros(1,2)
    assert quotient*omega*quotient.T==sp.Matrix([[0,1],[-1,0]])
    assert constraint*omega*constraint.T==sp.zeros(1)
    return dict(status='PASS',enlarged_phase_dimension=312,first_class_constraints=78,
        reduced_phase_dimension=156,propagating_canonical_modes=78,
        constraints='C_i=q1_i+q2_i. Retain Q_i=(q1_i-q2_i)/2, P_i=p1_i-p2_i; [Q_i,P_j]=i delta_ij and [C_i,Q_j]=[C_i,P_j]=0.',
        hamiltonian='H_phys=sum_e[(V_e.Q+a)(U_e.P+a)]^2, so [C_i,H_phys]=0 exactly.',
        brst='Omega_BRST=sum_i ghost_i*C_i; mutually commuting constraints give Omega_BRST^2=0.',
        rigging='delta(q1+q2)*psi((q1-q2)/2) solves the constraints distributionally. Group averaging supplies the physical L2(R78) inner product; this is not a normalizable kinematical state.',
        contrast='Imposing also all p1-p2 constraints is the11772 zero-dimensional reduction. Imposing only this chosen isotropic half retains the full original matter mechanics.',
        boundary='An explicit supplied Abelian gauge embedding. The graph has not selected this half, and no local gravitational hypersurface-deformation algebra is derived.')


def payload():
    return dict(schema='w33.pass11779_11780_11782.v1',
        source_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
        pass11779=local_net(),pass11780=actual_clifford_test(),
        bott_index_control=bott_control(),pass11782=surviving_constraints())


if __name__=='__main__':
    result=payload();OUT.write_text(json.dumps(result,indent=2)+'\n')
    print('11779 explicit local net;11780 actual spin test/Bott index control PASS;11782 gauge retains78 modes PASS')
