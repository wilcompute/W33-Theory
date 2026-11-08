"""Declared closed gauge ring: physical branch scales and scalar inventory.

Standard deconstruction/clockwork methods, not a new axion mechanism.
Species cutoffs and bounded operator coefficients are explicit hypotheses.
"""
import json
import math
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
MP=2.435e27;H0=1.44667e-33


def incidence(N):
    B=np.zeros((N,N),dtype=int)
    for i in range(N):B[i,i]=1;B[(i+1)%N,i]=-1
    return B


def mass_matrix(phases,eps=.053,M=1.):
    """Both gauge-allowed forward and reverse chiral hoppings retained."""
    N=len(phases);A=M*np.eye(N,dtype=complex);t=M*eps/2
    for i,theta in enumerate(phases):
        j=(i+1)%N;A[i,j]+=t*np.exp(1j*theta);A[j,i]+=t*np.exp(-1j*theta)
    return A


def quality(N,r_mass=1.,species_per_site=0.,dressed=False):
    # f_mass=sqrt(N)*F=N*f_loop. Species estimate is an external screen.
    cutoff=MP/math.sqrt(species_per_site*N)if species_per_site else MP
    F=r_mass*MP/math.sqrt(N);floop=r_mass*MP/N
    u=F*F/(2*cutoff*cutoff)
    leading=math.log10(2)+4*math.log10(cutoff)-2*math.log10(floop*H0)+N/2*math.log10(u)
    if u>=1:return dict(N=N,r_mass=r_mass,species_per_site=species_per_site,F_over_MP=F/MP,
                        f_loop_over_MP=floop/MP,cutoff_over_MP=cutoff/MP,u=u,
                        leading_log10_curvature_over_H0_squared=leading,all_scalar_bound_log10=None,
                        status='SCALAR_VEV_OUTSIDE_OPERATOR_CONVERGENCE_RADIUS')
    # All phase-dependent gauge-invariant scalar monomials have winding m>=1
    # and radial powers ki>=0. For |c_(m,k)|<=1, sum absolute curvatures:
    # 2 Lambda^4/floop^2 * (1-u)^(-N) * v(1+v)/(1-v)^3, v=u^(N/2).
    logv=N/2*math.log(u);v=math.exp(logv)if logv>-745 else 0.
    bound=leading-N*math.log10(1-u)+math.log10(1+v)-3*math.log10(1-v)
    return dict(N=N,r_mass=r_mass,species_per_site=species_per_site,F_over_MP=F/MP,
                f_mass_over_MP=r_mass,f_loop_over_MP=floop/MP,cutoff_over_MP=cutoff/MP,u=u,
                leading_log10_curvature_over_H0_squared=leading,all_scalar_bound_log10=bound,
                status='BOUNDED_FULL_SCALAR_MONOMIAL_TOWER_AT_FIXED_RADIAL_VEVS')


def matrix_control(N=24,psi=.71,eps=.053):
    rng=np.random.default_rng(1108);phases=rng.normal(size=N)
    phases+=(psi-sum(phases))/N
    A=mass_matrix(phases,eps)
    analytic=np.sort(1+eps*np.cos(psi/N+2*np.pi*np.arange(N)/N))
    error=float(max(abs(np.linalg.svd(A,compute_uv=False)[::-1]-analytic)))
    alpha=rng.normal(size=N);changed=phases+alpha-np.roll(alpha,-1)
    U=np.diag(np.exp(1j*alpha))
    covariance=float(np.max(abs(mass_matrix(changed,eps)-U@A@U.conj().T)))
    shifted=np.sort(1+eps*np.cos((psi+2*np.pi)/N+2*np.pi*np.arange(N)/N))
    assert error<1e-12 and covariance<1e-12
    assert max(abs(shifted-analytic))<1e-12
    return dict(N=N,phase_sum=float(sum(phases)),singular_spectrum_residual=error,
                gauge_covariance_residual=covariance,full_spectrum_period_2pi=True,
                physical_branch='m_k=M[1+eps*cos(phi/f_mass+2pi*k/N)] for eps<1; f_mass=sqrt(N)*F, f_loop=F/sqrt(N). Fixed k is an actual eigenbranch; winding psi by2pi permutes the full spectrum.',
                hopping_boundary='Reverse hopping is gauge allowed and explicitly included, rather than silently set to zero. Translation/reflection-symmetric real equal couplings are supplied; general allowed site-dependent/complex couplings remain a different model.')


def loop_bound_log10(N,r_mass=1.,eps=.053,M=16000.):
    # For N>=5 the cyclic sum cancels all nonconstant harmonics of degree<N.
    # (1+u)^4 log(1+u)=sum c_j u^j, |c_j|=24/[j...(j-4)] for j>=5.
    # |d_theta^2 cos^j(theta)|<=j^2 and |c_j|j^2 decreases for j>=5.
    c=24/math.prod(range(N-4,N+1))
    return (4*math.log10(M)-2*math.log10(r_mass*MP*H0)
            +math.log10(N**3*c/(8*math.pi**2*(1-eps)))+N*math.log10(eps))


def build():
    rows=[quality(N,r,nu)for r in [1.,.15]for nu in [0.,1.,2.,4.,9.]for N in [24,108,110,250,300,850]]
    thresholds=[]
    for r in [1.,.15]:
        for nu in [0.,1.,2.,4.,9.]:
            for key in ['leading_log10_curvature_over_H0_squared','all_scalar_bound_log10']:
                first=next((n for n in range(5,2001)if (v:=quality(n,r,nu)[key])is not None and v<math.log10(.01)),None)
                thresholds.append(dict(r_mass=r,species_per_site=nu,screen=key,first_N_below_one_percent_H0_squared_up_to2000=first))
    N=24;B=incidence(N);w=np.ones(N,dtype=int)
    assert np.all(B@w==0)and np.linalg.matrix_rank(B)==N-1
    # A proposed shortcut X,Y carries the charges of complementary half-paths.
    qX=B[:,:12].sum(axis=1);qY=B[:,12:].sum(axis=1)
    assert np.all(qX+qY==0)
    result=dict(status='DECLARED_GAUGE_RING_NORMAL_MODES_AND_BOUNDED_SCALAR_OPERATOR_SCREEN_NOT_UV_COMPLETION',
      action='U1^N on ring vertices, N complex links Phi_i of charge e_i-e_(i+1), N vectorlike Dirac fermions of charge e_i, radial potential sum lambda_i(|Phi_i|^2-F^2/2)^2. Fermion matrix M I plus both conjugate nearest-neighbor hoppings. Four-dimensional spacetime and all scales supplied.',
      normalization='psi=sum_i theta_i; f_loop=(sum_i F_i^-2)^-1/2, equal F gives F/sqrt(N). Uniform-gauge hopping eigenphases are psi/N+2pi*k/N, so f_mass=N*f_loop=sqrt(N)*F. Do not identify either scale with F without matching.',
      invariant_proof='B z=0 on a connected ring implies z_i=z_(i+1), hence z=m*(1,...,1). Every phase-breaking scalar monomial is (product Phi)^m times product |Phi_i|^(2ki), or its conjugate. Lowest degreeN for scalar-only inventory; phase-preserving portals do not change this proof.',
      coefficient_assumption='Each dimensionless coefficient of a phase-dependent scalar monomial bounded by1 at the supplied cutoff. Fixed radial vevs; absolute winding/radial-insertion sum included. Does not bound arbitrary unknown coefficients, added charged scalars, fermionic operators, derivative terms, gravity effects or all loop orders.',
      matrices=matrix_control(),rows=rows,thresholds=thresholds,
      fermion_loop_bound=dict(formula='|V_fermion_second|/H0^2 <= M^4 N^3 |c_N| eps^N/[8pi^2 f_mass^2 H0^2(1-eps)], c_N=24/[N(N-1)(N-2)(N-3)(N-4)], N>=5; conservative all-phase bound after cyclic cancellation.',rows=[dict(N=n,log10_bound=loop_bound_log10(n,.15,.053*.15))for n in [24,108,250,300]]),
      added_mediator_shortcut=dict(X_charge=qX.tolist(),Y_charge=qY.tolist(),allowed_operator='mu^2 X Y+h.c.',canonical_degree=2,scope='If both complementary path mediators are added as canonical scalars, their bilinear is gauge allowed. Their induced vevs and matching scale must be recomputed; a degree2 label alone does not determine its amplitude. No such extra scalars are included in the passing scalar-only screens.'),
      species='Lambda=MP/sqrt(nu*N) is a supplied species-cutoff estimate, not a proven exact quantum-gravity threshold. nu=0 means cutoffMP; nu=1,2,4,9 expose sensitivity. Null threshold means no passing bound withinN<=2000, not universal impossibility.',
      limits='No selected N, physical gauge couplings, fermion populations, radial/site-symmetry stability, SM embedding, radion/gravity or TOE. Leading and all-scalar bounds are sufficient conditional screens, not a completed UV theory.',
      ownership='Known abelian-quiver protection and Goldstone normalization:1804.01112 and repo November5 native-boundary audit. Known cyclic-particle protection2610.30253. Explicit closed-ring normal-mode matching and bounded scalar-tower/species controls are applications, not priority claims.')
    (ROOT/'data/toe_20261108_gauge_ring_quality.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('RING_THRESHOLDS',thresholds,flush=True)
    return result


if __name__=='__main__':build()
