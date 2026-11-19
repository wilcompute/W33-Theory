#!/usr/bin/env python3
"""A Lorentzian event-exchange bridge: dimension, time, mass and gauge curvature.

Independent derivations and tests of:
 - Poisson-sprinkled Minkowski causal-diamond order statistics d=2,3,4;
 - Johnston's EXACT-in-ensemble 1+1 massive retarded causal-chain kernel;
 - proper-time estimate from longest increasing causal chain;
 - U(1) Wilson-link gauge covariance and nonzero loop holonomy;
 - charged Klein-Gordon kernel in a constant external electric field:
       G_R=.5 theta(t)theta(t^2-x^2) exp(i q E tx/2) f(t^2-x^2),
       4[s f''+f']+(m^2+(qE)^2 s/4) f=0, f(0)=1;
 - a Poisson falling-factorial event-count estimator of f that is EXACTLY
   ensemble-unbiased for fixed endpoints/volume when the whole finite
   polynomial for each realized N is retained.

This uses established causal-set/charged KG technology and the continuum
field equation as external input; it DOES NOT derive dimension, masses,
gauge couplings, or Einstein gravity and is NOT a solved TOE.
"""
from __future__ import annotations
import bisect, cmath, json, math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import gammaln,j0,erfcx

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/"data"/"toe_20261119_causal_exchange_propagator_gauge_gate.json"
PI=np.pi


def ordered_fraction(d):
    # Probability a random UNORDERED pair in flat causal diamond is related.
    # Some literature divides this by 2 for a directed ordered pair.
    return float(np.exp(gammaln(d+1)+gammaln(d/2)
                        -gammaln(3*d/2)-np.log(2)))


def dimension_from_fraction(r):
    if not 0<r<1:raise ValueError("fraction must be strictly between 0 and 1")
    return float(brentq(lambda d:ordered_fraction(d)-r,1.,10.))


def sample_causal_diamond(d,n,rng,T=2.):
    """n points uniform in d-dimensional Alexandrov interval of proper T."""
    if d<2:raise ValueError("spacetime d must be >=2")
    # Cross-section n=d-1 spatial ball, radius R=T/2-|t|.
    # |2t/T|~Beta(1,d), so z=1-(1-u)^(1/d).
    z=1-(1-rng.random(n))**(1/d)
    t=(rng.integers(0,2,n)*2-1)*z*T/2
    R=(1-z)*T/2
    rad=R*rng.random(n)**(1/(d-1))
    if d==2:space=(rng.integers(0,2,n)*2-1)[:,None]*rad[:,None]
    else:
        dirs=rng.normal(size=(n,d-1))
        dirs/=np.linalg.norm(dirs,axis=1)[:,None]
        space=dirs*rad[:,None]
    return np.column_stack([t,space])


def pair_fraction(X,rng,num_pairs=240000):
    n=len(X)
    i=rng.integers(0,n,size=num_pairs)
    j=rng.integers(0,n-1,size=num_pairs)
    j+=j>=i
    v=X[i]-X[j]
    related=np.abs(v[:,0])>np.linalg.norm(v[:,1:],axis=1)
    return float(np.mean(related))


def dimension_gate():
    rng=np.random.default_rng(202611191)
    rows=[]
    for d in (2,3,4):
        frac=pair_fraction(sample_causal_diamond(d,6500,rng),rng)
        d_hat=dimension_from_fraction(frac)
        expected=ordered_fraction(d)
        assert abs(frac-expected)<.025
        assert abs(d_hat-d)<.23
        rows.append({"input_dimension":d,"theoretical_unordered_pair_fraction":expected,
                     "measured_fraction":frac,"estimated_dimension":d_hat,
                     "pair_samples":240000,"events":6500})
    assert np.isclose(ordered_fraction(2),.5)
    assert np.isclose(ordered_fraction(4),.1)
    return {"status":"PASS","data":rows,
            "meaning":"Dimension estimation assumes the sample was sprinkled in a preselected Minkowski dimension; does not dynamically select 3+1 dimensions."}


def sprinkle_1d_uv(tau,rho,rng):
    # Alexandrov interval between (u,v)=(0,0) and (tau,tau).
    # 1+1 Minkowski 4-volume here V=tau²/2, du dv=2 dt dx.
    N=int(rng.poisson(rho*tau*tau/2))
    return rng.random(N)*tau,rng.random(N)*tau


def chain_mass_kernel_1p1(u,v,rho,m):
    """Johnston chain sum, fast 2D dominance-prefix Fenwick recursion.

    K_ab=.5 C_ab - (m²/(2rho)) sum_{a<c<b} K_ac C_cb.
    The density-scaled mass scattering exactly recovers J0(m*tau)
    on averaging over Poisson-sprinkled causal diamonds, at any rho.
    """
    n=len(u)
    if len(v)!=n:raise ValueError("u,v shape mismatch")
    idx=np.argsort(u)
    v=np.asarray(v)[idx]
    v_ranks=np.argsort(np.argsort(v))+1
    fenwick=np.zeros(n+1,float)
    g=m*m/(2*rho)
    S=0.
    for r in v_ranks:
        r=int(r)
        j=r-1
        prefix=0.
        while j>0:
            prefix+=fenwick[j]
            j-=j&-j
        F=.5-g*prefix
        S+=F
        j=r
        while j<=n:
            fenwick[j]+=F
            j+=j&-j
    return float(.5-g*S)


def chain_exact_small(u,v,rho,m):
    """Independent dense nilpotent-matrix inversion for small causets."""
    u=np.r_[0,np.asarray(u),2.]
    v=np.r_[0,np.asarray(v),2.]
    order=np.argsort(u+v)
    u,v=u[order],v[order]
    C=((u[:,None]<u[None,:])&(v[:,None]<v[None,:])).astype(float)
    K=.5*C@np.linalg.inv(np.eye(len(u))+m*m/(2*rho)*C)
    return float(K[0,-1])


def longest_increasing_chain(u,v):
    """2D Minkowski causal longest-chain DP equals LIS after ordering u."""
    vv=np.asarray(v)[np.argsort(u)]
    tails=[]
    for a in vv:
        j=bisect.bisect_left(tails,float(a))
        if j==len(tails):tails.append(float(a))
        else:tails[j]=float(a)
    return len(tails)


def mass_chain_gate():
    tau=2.;m=.8
    continuum=.5*float(j0(m*tau))
    rng=np.random.default_rng(202611192)
    density=[]
    for rho,trials in [(12.,1200),(45.,1200),(120.,1000)]:
        amps=[];height=[]
        for _ in range(trials):
            u,v=sprinkle_1d_uv(tau,rho,rng)
            amps.append(chain_mass_kernel_1p1(u,v,rho,m))
            height.append(longest_increasing_chain(u,v))
        A=np.asarray(amps)
        mean=float(A.mean())
        stderr=float(A.std(ddof=1)/np.sqrt(len(A)))
        assert abs(mean-continuum) < 5*stderr+.006, (rho,mean,stderr,continuum)
        # Longest chain scaling ~2 sqrt(N) with N~rho V,
        # not an exact finite-density proper-time estimator.
        chainT=np.mean(height)/np.sqrt(2*rho)
        assert .7*tau<chainT<1.1*tau
        density.append({"density":rho,"trials":trials,
            "expected_internal_events":rho*tau*tau/2,
            "sample_mean_retarded_amplitude":mean,
            "standard_error":stderr,
            "continuum_half_J0_m_tau":continuum,
            "z_deviation":(mean-continuum)/stderr,
            "mean_longest_chain":float(np.mean(height)),
            "asymptotic_chain_proper_time_estimator":float(chainT)})
    u=np.array([.2,.5,.9,1.2]);v=np.array([.7,.4,1.,1.4])
    fast=chain_mass_kernel_1p1(u,v,30,m)
    brute=chain_exact_small(u,v,30,m)
    assert abs(fast-brute)<1e-13
    return {
        "status":"PASS",
        "dimension":"1+1 Minkowski","tau":tau,"mass":m,"continuum":continuum,
        "density_trials":density,
        "fast_Fenwick_vs_dense_nilpotent_matrix_error":abs(fast-brute),
        "ensemble_identity":"E[(C^(k+1))_ab]=(rho V)^k/(k!)², V=tau²/2. Hence E[K_ab]=J0(m tau)/2 at every positive density rho.",
        "limitations":[
            "Johnston's causal-set retarded free scalar propagator is known prior art.",
            "The ensemble expectation is exact on the Poisson Minkowski background; a finite realization has stochastic noise.",
            "Sprinkling assumes the continuum Lorentzian volume and dimension, not a dynamical derivation.",
            "The retarded Green function is not a physical full quantum-state Feynman propagator.",
            "Asymptotic chain height does not yield a coordinate-free metric at finite density without calibration."]
    }


def coeff_KG(m,qe,order):
    """Power series in sigma=t²-x²: 4(s f''+f')+(m²+qe²*s/4)f=0."""
    c=np.zeros(order+1,float);c[0]=1.
    for n in range(order):
        previous=c[n-1] if n else 0.
        c[n+1]=-(m*m*c[n]+qe*qe*previous/4)/(4*(n+1)**2)
    return c


def radial_factor(sigma,m,qe):
    if sigma<0:raise ValueError("inside future lightcone only")
    c=coeff_KG(m,qe,45)
    # Horner avoids catastrophic powers at high order.
    return float(np.polynomial.polynomial.polyval(sigma,c))


def radial_factor_ode(sigma,m,qe):
    # independent ODE integration from regular-origin series.
    s0=1e-7
    c=coeff_KG(m,qe,7)
    f0=float(np.polynomial.polynomial.polyval(s0,c))
    fp0=sum(n*c[n]*s0**(n-1) for n in range(1,len(c)))
    def ode(s,y):
        f,fp=y
        return [fp,-fp/s-(m*m+qe*qe*s/4)*f/(4*s)]
    sol=solve_ivp(ode,(s0,sigma),(f0,fp0),rtol=2e-11,atol=2e-12)
    assert sol.success
    return float(sol.y[0,-1])


def poisson_factorial_KG_estimator(N,rho,m,qe):
    """FINITE n-dependent polynomial whose Poisson expectation equals f(2V).

    Coefficients c_n obey KG recurrence. The unbiased moment substitution
    sigma^n=(2V)^n -> (2/rho)^n*(N)_n yields terms A_n with
    A_(n+1)=-(N-n)/(2rho(n+1)^2) * [m² A_n
                     +qe²/4 * 2(N-n+1)/rho A_(n-1)].
    """
    an=1.;prev=0.;total=1.
    for n in range(N):
        prior=prev
        nex=-(N-n)/(2*rho*(n+1)**2)*(
                 m*m*an+(qe*qe/4)*2*(N-n+1)/rho*prior)
        total+=nex
        prev,an=an,nex
        if not np.isfinite(total):raise ArithmeticError("unstable estimator")
    return float(total)


def charged_kernel_gate():
    tau=2.;sigma=tau*tau;V=sigma/2
    rows=[]
    for m,qe in [(0,0),(.8,0),(0,.9),(.8,.9)]:
        f=radial_factor(sigma,m,qe)
        ode=radial_factor_ode(sigma,m,qe)
        assert abs(f-ode)<2e-9,(m,qe,f,ode)
        if qe==0:assert abs(f-j0(m*tau))<1e-12
        if m==0:assert abs(f-j0(qe*sigma/4))<1e-12
        rows.append({"m":m,"qE":qe,"sigma":sigma,
                     "radial_factor_series":f,
                     "independent_ODE_solution":ode,
                     "series_ODE_absolute_difference":abs(f-ode)})
    rng=np.random.default_rng(202611193)
    unbiased=[]
    for rho in (12.,80.):
        draws=rng.poisson(rho*V,size=10000)
        for m,qe in [(0,.9),(.8,.9)]:
            values=np.fromiter((poisson_factorial_KG_estimator(int(n),rho,m,qe)
                                for n in draws),float,count=len(draws))
            exact=radial_factor(sigma,m,qe)
            mean=float(np.mean(values))
            se=float(np.std(values,ddof=1)/np.sqrt(len(values)))
            assert abs(mean-exact)<5*se+.003,(rho,m,qe,mean,se,exact)
            unbiased.append({"rho":rho,"m":m,"qE":qe,"samples":len(values),
              "analytic_continuum_radial_factor":exact,
              "Poisson_falling_factorial_estimator_mean":mean,
              "standard_error":se,
              "absolute_discrepancy":abs(mean-exact)})
    assert abs(radial_factor(sigma,0,.9)-j0(.9))<1e-12
    return {
      "status":"PASS","field":"constant background electric field E in 1+1 Minkowski; A_x=E t, A_t=0, qE dimension mass²",
      "charged_exact_retarded_kernel_inside_cone":"G_R(t,x;0,0) = [1/2] exp(i qE t x/2) f(t²-x²); f solves 4(s f''+f')+[m²+(qE)²s/4]f=0, f(0)=1",
      "m0_closed_form":"f(s)=J0(qE s/4)",
      "m_nonzero_E_zero":"f(s)=J0(m sqrt(s))",
      "derivation":"D_t=partial_t, D_x=partial_x-i q E t; using straight-line U=exp(i qE t x/2), covariant wave operator reduces to stated ODE",
      "radial_checks":rows,"Poisson_unbiased_volume_estimator":unbiased,
      "mathematical_unbiasedness":"For N~Poisson(rho V), E[(N)_n]=(rho V)^n; replacing s^n=(2V)^n by (2/rho)^n(N)_n in exact radial power series gives unbiased ensemble kernel at ANY rho, assuming known m,E and continuum background.",
      "important_limits":[
         "This uses continuum minimally coupled charged Klein-Gordon dynamics as input, not its derivation from order alone.",
         "The Poisson count estimator assumes the background diamond volume and density are given, and the constant electric field is external.",
         "A bare event count determines volume only statistically; it does not produce a general curved spacetime metric.",
         "No claim to derive charge, coupling, gauge group, matter spin, interactions, or quantum gravity."]
    }


def wilson_phase(t1,x1,t2,x2,qe):
    # Straight segment A_x=Et: q int A dx= qe*(x2-x1)*(t1+t2)/2.
    return qe*(x2-x1)*(t1+t2)/2


def charged_endpoint_kernel(u,v,rho,m,qe,chi=None,tau=2.):
    order=np.argsort(u)
    uu=np.asarray(u)[order];vv=np.asarray(v)[order]
    t=(uu+vv)/2; x=(uu-vv)/2
    ch=lambda a,b:0. if chi is None else chi(a,b)
    s=(0.,0.)
    endpoint=(tau,0.)
    F=np.zeros(len(uu),complex)
    alpha=m*m/(2*rho)
    for i in range(len(uu)):
        F[i]=.5*np.exp(1j*(wilson_phase(*s,t[i],x[i],qe)
                    +ch(t[i],x[i])-ch(*s)))
        for j in range(i):
            if vv[j]<vv[i]:
                phase=wilson_phase(t[j],x[j],t[i],x[i],qe)
                F[i]-=alpha*F[j]*np.exp(1j*(phase+ch(t[i],x[i])-ch(t[j],x[j])))
    end=.5*np.exp(1j*(wilson_phase(*s,*endpoint,qe)+ch(*endpoint)-ch(*s)))
    for j in range(len(uu)):
        phase=wilson_phase(t[j],x[j],*endpoint,qe)
        end-=alpha*F[j]*np.exp(1j*(phase+ch(*endpoint)-ch(t[j],x[j])))
    return complex(end)


def gauge_covariance_and_failure_gate():
    rng=np.random.default_rng(202611194)
    rho=25.;tau=2.;m=.8;qe=.9
    u,v=sprinkle_1d_uv(tau,rho,rng)
    chi=lambda t,x:.32*t+.47*x+.12*t*t
    K=charged_endpoint_kernel(u,v,rho,m,qe)
    K2=charged_endpoint_kernel(u,v,rho,m,qe,chi)
    gauge_factor=np.exp(1j*(chi(tau,0)-chi(0,0)))
    assert abs(K2-gauge_factor*K)<1e-12
    Kflat=charged_endpoint_kernel(u,v,rho,m,0)
    Kpure=charged_endpoint_kernel(u,v,rho,m,0,chi)
    assert abs(Kflat-Kpure/gauge_factor)<1e-12
    # For m=0 all mass-scattering terms vanish; naive Wilson-edge
    # propagator is .5 U, completely blind to genuine field curvature.
    naive=.5*np.exp(1j*wilson_phase(0,0,tau,0,qe))
    exact=.5*radial_factor(tau*tau,0,qe)
    assert abs(naive-.5)<1e-14
    assert abs(exact-.5)> .08
    # Gauge invariant two-path interference phase is nonzero when F!=0.
    p=(.62,.15);q=(1.21,-.24);end=(tau,0.)
    pathp=wilson_phase(0,0,*p,qe)+wilson_phase(*p,*end,qe)
    pathq=wilson_phase(0,0,*q,qe)+wilson_phase(*q,*end,qe)
    oriented_area=.5*(tau*p[1]-tau*q[1]) # signed via s->p->end->q->s
    # Compute actual area by full shoelace to avoid sign guess.
    poly=[(0.,0.),p,end,q]
    shoelace=.5*sum(poly[k][0]*poly[(k+1)%4][1]-poly[k][1]*poly[(k+1)%4][0] for k in range(4))
    # coordinates (t,x); the Wilson integral delta is qe times oriented
    # loop integral of t dx = qe times area in (t,x) plane.
    assert abs(pathp-pathq - qe*shoelace)<1e-12
    # Direct covariant PDE residual for G_naive=.5 U in cone at t,x.
    # (D_t²-D_x²) U = (qE)^2 (t²-x²)/4 U;
    # properly corrected exact m=0 factor solves homogeneous PDE.
    t=1.44;x=.3;s=t*t-x*x
    U=np.exp(1j*qe*t*x/2)
    residual_naive=.5*qe*qe*s/4*U
    assert abs(residual_naive)> .05
    h=1e-4
    def corrected(t,x):
        return .5*np.exp(1j*qe*t*x/2)*radial_factor(t*t-x*x,0,qe)
    G=corrected(t,x)
    dtt=(corrected(t+h,x)-2*G+corrected(t-h,x))/h**2
    dxx=(corrected(t,x+h)-2*G+corrected(t,x-h))/h**2
    dx=(corrected(t,x+h)-corrected(t,x-h))/(2*h)
    covariant_residual=dtt-dxx+2j*qe*t*dx+(qe*t)**2*G
    assert abs(covariant_residual)<2e-6,(covariant_residual,residual_naive)
    return {
      "status":"PASS",
      "flat_gauge_covariance_error":float(abs(Kflat-Kpure/gauge_factor)),
      "constant_field_gauge_covariance_error":float(abs(K2-gauge_factor*K)),
      "electric_field_two_path_holonomy_phase":float(pathp-pathq),
      "oriented_spacetime_loop_area":float(shoelace),
      "loop_flux_analytic_qE_times_area":float(qe*shoelace),
      "naive_massless_Wilson_kernel_at_tau_2":float(naive.real),
      "exact_massless_charged_kernel_at_tau_2":float(exact),
      "naive_minus_exact_amplitude":float(naive.real-exact),
      "naive_covariant_KG_PDE_residual_abs_at_event":float(abs(residual_naive)),
      "corrected_covariant_KG_numeric_PDE_residual_abs":float(abs(covariant_residual)),
      "conclusion":"Gauge covariance of edge phases is NOT sufficient for correct dynamics in nonzero curvature. The bare m=0 Wilson-edge causal sum misses a known exact J0(qE*s/4) tail.",
      "scope":"External constant electric field in fixed 1+1 flat spacetime; no derivation of full nonabelian gauge dynamics, Born rule or quantum gravity."
    }


def four_dimensional_lightcone_link_gate():
    """Known 4D causal-link scaling; compare the 2D all-chain kernel.
    In d=4, an Alexandrov interval of proper time sqrt(sigma) has
    volume V4=pi*sigma^2/24. Poisson link probability exp(-rho V4).
    K4_rho(sigma)=sqrt(rho)/(2pi sqrt(6))*exp(-rho V4)
    converges distributionally to delta(sigma)/(2pi), on sigma>=0.
    """
    a=PI/24
    beta=1.
    rows=[]
    for rho in [1.,16.,256.,4096.]:
        # Integrate K4 against test h(sigma)=exp(-beta sigma).
        # Normalized by the exactly integrated constant test h=1.
        # Analytic exact ratio is exp(z^2)erfc(z), z=beta/(2sqrt(a*rho)).
        z=beta/(2*np.sqrt(a*rho))
        ratio=float(erfcx(z))
        expected=(1/(2*PI))*ratio
        assert 0<ratio<1
        assert abs((np.sqrt(rho)/(2*PI*np.sqrt(6)))*
                np.sqrt(PI)/(2*np.sqrt(a*rho)) - 1/(2*PI))<1e-14
        mean_sigma=1/np.sqrt(PI*a*rho)
        rows.append({"rho":rho,
                     "test_exp_minus_sigma_integral":expected,
                     "integral_divided_by_distributional_limit":ratio,
                     "characteristic_null_shell_sigma_mean":float(mean_sigma)})
    assert all(rows[j+1]["integral_divided_by_distributional_limit"] >
               rows[j]["integral_divided_by_distributional_limit"] for j in range(len(rows)-1))
    assert rows[-1]["integral_divided_by_distributional_limit"]>.96
    return {"status":"PASS",
      "spacetime_dim":4,
      "interval_volume":"V4(sigma)=pi*sigma²/24 for sigma=t²-r²",
      "Poisson_link_probability":"exp(-rho*pi*sigma²/24)",
      "scaled_retarded_kernel":"K4_rho(sigma)=sqrt(rho)/(2pi sqrt(6))* exp(-rho*pi*sigma²/24) inside cone",
      "distributional_limit":"delta(sigma)/(2pi) for sigma>=0",
      "integration_test_function":"exp(-sigma)",
      "rows":rows,
      "physical_distinction":"2D massless scalar propagates throughout the light cone, while 4D massless retarded scalar is supported on the null cone. Full 2D causal relation matrix C cannot replace dimension-sensitive 4D near-null link L.",
      "limitations":["Known causal-set link propagator scaling from Johnston and review papers, not new physics.",
                     "External 3+1 flat Minkowski geometry and Poisson density are assumed.",
                     "This weak distribution test does not recover arbitrary matter, 4D spinor chirality or quantum gravity dynamics."]}


def run_all():
    parts={
      "Myrheim_Meyer_dimension_control":dimension_gate(),
      "mass_and_proper_time_from_causal_chains":mass_chain_gate(),
      "exact_constant_E_charged_KG_and_Poisson_count":charged_kernel_gate(),
      "gauge_covariance_vs_dynamical_failure":gauge_covariance_and_failure_gate(),
      "four_dimensional_null_cone_link_distribution":four_dimensional_lightcone_link_gate()
    }
    assert all(x["status"]=="PASS" for x in parts.values())
    return {
      "date":"2026-11-19",
      "theme":"Causal event exchange bridge: time, volume, relativistic propagation and gauge curvature",
      "status":"Mathematically verified controls and one sharp false-step falsifier; NO TOE",
      "TOE_solved":False,
      "four_dimensional_spacetime_derived":False,
      "metric_dynamics_or_Einstein_equations_derived":False,
      "mass_charge_or_gauge_dynamics_derived":False,
      "prior_art":[
       "Johnston (2008), Particle propagators on discrete spacetime, arXiv:0806.3083",
       "Surya (2019), The causal set approach to quantum gravity, Living Reviews in Relativity",
       "Path sums for propagators in causal sets, Phys Rev D 109 046008 (2024)",
       "Gauge Fields in Causal Set Theory (Sverdlov/Bombelli et al.)",
       "Link-based causal set propagators in 1+1 dimensions, Phys Rev D (2026)"],
      "new_to_repository_calculations":[
       "Constructive analytic 1+1 constant-E charged KG Green radial ODE with Wilson transport",
       "Poisson falling-factorial unbiased event-count estimator for charged radial amplitude",
       "Exact flat U1 finite-chain gauge covariance and nonzero Wilson-loop holonomy",
       "PDE witness that gauge covariance alone fails to supply field-curvature tail"],
      "results":parts
    }


def main():
    out=run_all()
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps(out,indent=2),encoding="utf8")
    result=out["results"]
    print(json.dumps({
      "result":"PASS",
      "dimensions":[{"d":x["input_dimension"],"estimate":x["estimated_dimension"]}
         for x in result["Myrheim_Meyer_dimension_control"]["data"]],
      "mass_continuum":result["mass_and_proper_time_from_causal_chains"]["continuum"],
      "mass_sample_means":[x["sample_mean_retarded_amplitude"] for x in
                            result["mass_and_proper_time_from_causal_chains"]["density_trials"]],
      "charged_exact_vs_naive":[
         result["gauge_covariance_vs_dynamical_failure"]["exact_massless_charged_kernel_at_tau_2"],
         result["gauge_covariance_vs_dynamical_failure"]["naive_massless_Wilson_kernel_at_tau_2"]],
      "charged_estimates":result["exact_constant_E_charged_KG_and_Poisson_count"]["Poisson_unbiased_volume_estimator"],
      "output":str(OUTPUT)
    }))


if __name__=="__main__":
    main()
