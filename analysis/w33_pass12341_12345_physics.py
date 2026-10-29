"""Finite six-loop response, chiral charge audit and string-threshold probe.

This is a named free-fermion patch and a truncated string integrand. Neither
is a microscopic TOE, a full string partition function or a vacuum proof.
"""
from functools import lru_cache
from pathlib import Path
import hashlib
import json
import sys

import numpy as np
import sympy as sp
from scipy.linalg import eigh
from scipy.integrate import quad
from scipy.special import expit, expn
from scipy.sparse import kron, eye, diags, csr_matrix
from scipy.sparse.linalg import eigsh, LinearOperator, cg, splu
from numpy.polynomial.legendre import leggauss

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261027_microscopic_response_and_lifts as native
import w33_20261027_five_front_followthrough as previous


@lru_cache(None)
def six_loop_operators():
    C,B,_=native.lifted_patch(d=6,N=3)
    # These are the actual 6 based commutators in the prior N=3 lifted patch.
    assert C.shape==(6,48) and B.shape==(48,43)
    assert np.linalg.matrix_rank(C)==6 and not np.any(C@B)
    assert B.shape[0]-B.shape[1]+1==6
    dual=C.T@np.linalg.inv(C@C.T)
    assert np.max(abs(C@dual-np.eye(6)))<1e-12
    rng=np.random.default_rng(12344)
    chi=rng.normal(size=B.shape[1])
    alpha=np.column_stack((dual,B@chi))
    edges=[];K=np.zeros((43,43))
    for row in B:
        a=int(np.flatnonzero(row<0)[0]);b=int(np.flatnonzero(row>0)[0])
        edges.append((a,b));K[a,b]=K[b,a]=-1
    ev,U=eigh(K)
    vertices=[]
    for i in range(7):
        op=np.zeros_like(K,dtype=complex)
        for e,(a,b) in enumerate(edges):
            op[b,a]=-1j*alpha[e,i];op[a,b]=1j*alpha[e,i]
        vertices.append(U.T@op@U)
    vertices.append(U.T@np.diag(chi)@U)
    return C,B,dual,alpha,edges,K,ev,U,vertices


def six_loop_response(T=0.,mu=.3):
    C,B,dual,alpha,edges,K,ev,U,vertices=six_loop_operators()
    if T==0 and min(abs(ev-mu))<1e-9:
        raise ValueError('T=0 chemical potential must avoid one-particle levels')
    f=expit((mu-ev)/T) if T else (ev<mu).astype(float)
    rho=(U*f)@U.T
    contact=np.zeros((8,8),complex)
    for e,(a,b) in enumerate(edges):
        contact[:7,:7]+=2*rho[a,b]*np.outer(alpha[e],alpha[e])
    delta=ev[:,None]-ev[None,:];df=f[:,None]-f[None,:]
    mask=abs(delta)>1e-9
    regular=np.zeros_like(delta);np.divide(df,delta,out=regular,where=mask)
    static=regular.copy()
    if T:
        derivative=-f*(1-f)/T
        static[~mask]=np.broadcast_to(derivative[:,None],delta.shape)[~mask]
    electric=np.zeros_like(delta);np.divide(-df,delta**3,out=electric,where=mask)
    def bubble(weights):
        return np.array([[np.sum(weights*vertices[i]*vertices[j].T) for j in range(8)] for i in range(8)])
    S=(contact+bubble(static))[:6,:6].real
    E=bubble(electric)[:6,:6].real
    frequency=.73
    Kfrequency=contact+bubble(df/(delta+1j*frequency))
    pure=np.array([0.]*6+[1.,-frequency])
    ward=float(np.max(abs(Kfrequency@pure)))
    static_gauge=float(np.max(abs((contact+bubble(static))[6,:7])))
    assert ward<1e-9 and static_gauge<1e-9
    H=np.array(previous.inputs()[-2],dtype=float)
    J=np.zeros((6,6));J[0,5]=J[5,0]=1;J[1,4]=J[4,1]=-1;J[2,3]=J[3,2]=1
    X=np.stack((H.ravel(),J.ravel()),axis=1)
    coef=np.linalg.lstsq(X,S.ravel(),rcond=None)[0]
    residual=float(np.linalg.norm(S-coef[0]*H-coef[1]*J)/np.linalg.norm(S))
    scales=np.linalg.lstsq(E.ravel()[:,None],S.ravel(),rcond=None)[0]
    mismatch=float(np.linalg.norm(S-scales[0]*E)/np.linalg.norm(S))
    direction=np.array([.4,-.2,.3,.1,-.5,.6]);edge_angle=dual@direction
    def potential(step):
        Hstep=K.astype(complex)
        for e,(a,b) in enumerate(edges):
            Hstep[b,a]=-np.exp(1j*step*edge_angle[e]);Hstep[a,b]=Hstep[b,a].conjugate()
        values=eigh(Hstep,eigvals_only=True)
        return -T*np.logaddexp(0,(mu-values)/T).sum() if T else np.minimum(values-mu,0).sum()
    eps=.001
    fd=float((potential(eps)+potential(-eps)-2*potential(0))/eps**2)
    direct=float(direction@S@direction)
    assert abs(fd-direct)<2e-6
    return dict(T=T,mu=mu,sites=43,edges=48,cycles=6,particle_expectation=float(sum(f)),
        spectral_distance_to_mu=float(min(abs(ev-mu))),
        static_hessian=S.tolist(),electric_coefficient=E.tolist(),
        static_eigenvalues=np.linalg.eigvalsh(S).tolist(),electric_eigenvalues=np.linalg.eigvalsh(E).tolist(),
        best_common_cone_coefficients=coef.tolist(),best_common_cone_relative_residual=residual,
        best_static_vs_electric_scale=float(scales[0]),static_vs_electric_relative_residual=mismatch,
        ward_frequency=frequency,combined_gauge_density_ward_residual=ward,
        static_gradient_ward_residual=static_gauge,
        independent_grand_potential_finite_difference=fd,
        predicted_directional_second_derivative=direct,
        finite_difference_absolute_error=abs(fd-direct),
        scope='Actual six-commutator, open43-vertex48-edge lifted patch; supplied spinless free fermions, unit hopping and charge. All six fluxes and one pure-gauge direction come from one Peierls Hamiltonian. Not the infinite periodic cover, interacting E6 determinant, non-Abelian theory or continuum Maxwell action.')


def interacting_six_loop_response(U=2.):
    """One up and one down fermion, full six-cycle patch, supplied Hubbard U."""
    C,B,dual,alpha,edges,K,_,_,_=six_loop_operators()
    n=len(K);I=eye(n,format='csr');Ksp=csr_matrix(K)
    interaction=diags(U*np.eye(n).reshape(-1),format='csc')
    H=kron(Ksp,I,format='csc')+kron(I,Ksp,format='csc')+interaction
    start=np.random.default_rng(12345).normal(size=n*n)
    vals,vec=eigsh(H,k=4,which='SA',tol=1e-11,v0=start)
    idx=np.argsort(vals);vals=vals[idx];psi=vec[:,idx[0]];P=psi.reshape(n,n)
    gap=float(vals[1]-vals[0]);assert gap>1e-6
    rho=P@P.T+P.T@P
    b=[];contact=np.zeros((8,8),complex)
    for i in range(7):
        j=np.zeros_like(K,dtype=complex)
        for e,(a,z) in enumerate(edges):
            j[z,a]=-1j*alpha[e,i];j[a,z]=1j*alpha[e,i]
        b.append((j@P+P@j.T).ravel())
    chi=np.linalg.lstsq(B,alpha[:,6],rcond=None)[0]
    density=((chi[:,None]+chi[None,:])*P).ravel()
    density-=psi*np.vdot(psi,density)
    b.append(density);b=np.column_stack(b)
    assert np.linalg.norm(psi.conj()@b)<1e-8
    for e,(a,z) in enumerate(edges):
        contact[:7,:7]+=2*rho[a,z]*np.outer(alpha[e],alpha[e])
    A=H-vals[0]*eye(n*n,format='csc')
    operator=LinearOperator(A.shape,matvec=lambda x:A@x+psi*np.vdot(psi,x),dtype=complex)
    residuals=[]
    def solve(rhs):
        x,info=cg(operator,rhs,rtol=1e-11,atol=1e-13,maxiter=10000)
        assert info==0
        residuals.append(float(np.linalg.norm(operator@x-rhs)))
        return x
    X=np.column_stack([solve(b[:,i]) for i in range(7)])
    Y=np.column_stack([solve(X[:,i]) for i in range(6)])
    S=(contact[:7,:7]-2*(b[:,:7].conj().T@X).real).real
    E=2*(X[:,:6].conj().T@Y).real
    frequency=.73
    lu=splu(A.astype(complex)-1j*frequency*eye(n*n,format='csc'))
    xm=lu.solve(b);xp=lu.solve(b.conj()).conj()
    Pi=contact-b.conj().T@xm-(b.conj().T@xp).T
    gauge=np.array([0.]*6+[1.,-frequency])
    ward=float(np.max(abs(Pi@gauge)))
    static_ward=float(np.max(abs(S[6])))
    assert ward<1e-9 and static_ward<1e-9
    H0=np.array(previous.inputs()[-2],float)
    J=np.zeros((6,6));J[0,5]=J[5,0]=1;J[1,4]=J[4,1]=-1;J[2,3]=J[3,2]=1
    fit=np.stack((H0.ravel(),J.ravel()),axis=1)
    coeff=np.linalg.lstsq(fit,S[:6,:6].ravel(),rcond=None)[0]
    fiterror=float(np.linalg.norm(S[:6,:6]-coeff[0]*H0-coeff[1]*J)/np.linalg.norm(S[:6,:6]))
    scale=float(np.sum(S[:6,:6]*E)/np.sum(E*E))
    mismatch=float(np.linalg.norm(S[:6,:6]-scale*E)/np.linalg.norm(S[:6,:6]))
    direction=np.array([.4,-.2,.3,.1,-.5,.6]);angle=dual@direction
    def ground(step):
        ks=K.astype(complex)
        for e,(a,z) in enumerate(edges):
            ks[z,a]=-np.exp(1j*step*angle[e]);ks[a,z]=ks[z,a].conjugate()
        m=csr_matrix(ks)
        h=kron(m,I,format='csr')+kron(I,m,format='csr')+interaction
        return float(eigsh(h,k=1,which='SA',tol=1e-11,v0=start,return_eigenvectors=False)[0])
    eps=.001
    fd=(ground(eps)+ground(-eps)-2*vals[0])/eps**2
    expected=float(direction@S[:6,:6]@direction)
    assert abs(fd-expected)<1e-6 and max(residuals)<1e-8
    return dict(U=U,sites=43,edges=48,hilbert_dimension=n*n,particles='one up plus one down',
        ground_energy=float(vals[0]),sampled_lowest_gap=gap,
        ground_Ritz_residual=float(np.linalg.norm(H@psi-vals[0]*psi)),
        static_hessian=S[:6,:6].tolist(),electric_coefficient=E.tolist(),
        static_eigenvalues=np.linalg.eigvalsh(S[:6,:6]).tolist(),
        electric_eigenvalues=np.linalg.eigvalsh(E).tolist(),
        best_common_cone_coefficients=coeff.tolist(),best_common_cone_relative_residual=fiterror,
        best_static_vs_electric_scale=scale,static_vs_electric_relative_residual=mismatch,
        static_gradient_ward_residual=static_ward,combined_gauge_density_ward_residual=ward,
        max_projected_resolvent_residual=max(residuals),
        independent_ground_energy_second_difference=float(fd),
        directional_hessian=float(expected),finite_difference_absolute_error=float(abs(fd-expected)),
        scope='One fixed two-particle spinful Hubbard sector on the actual finite six-commutator patch. Electric and magnetic coefficients use the same interacting Hamiltonian and ground state. Sampled Ritz gaps and finite-volume response are numerical; not a full E6 matter theory, full Fock ensemble, dynamical gauge field or continuum limit.')


def charge_anomalies():
    # (SU5 representation, multiplicity, chi, psi, doubled Dynkin index, cubic SU5 anomaly)
    pieces=[('10',10,1,1,3,1),('bar5',5,-3,1,1,-1),('1',1,5,1,0,0),
            ('5',5,-2,-2,1,1),('bar5',5,2,-2,1,-1),('1',1,0,4,0,0)]
    def one(rows):
        return dict(dimension=sum(d for _,d,x,p,t,a in rows),
          SU5_cubic=sum(a for _,d,x,p,t,a in rows),
          SU5_squared_U1psi=sum(t*p for _,d,x,p,t,a in rows),
          gravitational_U1psi=sum(d*p for _,d,x,p,t,a in rows),
          U1psi_cubed=sum(d*p**3 for _,d,x,p,t,a in rows),
          U1chi_squared_U1psi=sum(d*x*x*p for _,d,x,p,t,a in rows),
          SU5_squared_U1chi=sum(t*x for _,d,x,p,t,a in rows),
          gravitational_U1chi=sum(d*x for _,d,x,p,t,a in rows),
          U1chi_cubed=sum(d*x**3 for _,d,x,p,t,a in rows),
          U1chi_U1psi_squared=sum(d*x*p*p for _,d,x,p,t,a in rows))
    sixteen=one(pieces[:3]);ten=one(pieces[3:5]);singlet=one(pieces[5:]);whole=one(pieces)
    assert sixteen['dimension']==16 and sixteen['SU5_cubic']==0
    assert [sixteen[x] for x in ('SU5_squared_U1psi','gravitational_U1psi','U1psi_cubed','U1chi_squared_U1psi')]==[4,16,16,80]
    assert all(v==0 for k,v in whole.items() if k!='dimension')
    return dict(conventions='Left-handed Weyl fields; chi and psi integer charges as in the canonical E6 decomposition; doubled Dynkin index 2T(5)=1, 2T(10)=3.',
                chiral_16=sixteen,complementary_10=ten,complementary_1=singlet,complete_27=whole,
                interpretation='If a proposed four-dimensional projection retains only this chiral16 while leaving U1psi gauged and supplies no compensating chiral fields or anomaly-canceling mechanism, its nonzero SU5^2 U1psi, mixed-gravitational U1psi, U1psi^3 and U1chi^2 U1psi coefficients fail the ordinary 4D anomaly cancellation test.',
                boundary='Necessary conditional 4D charge accounting only. It does not show which modes a native orbifold retains, compute localized boundary anomalies, exclude anomaly inflow/Green-Schwarz cancellation, or construct a chiral measure.')


@lru_cache(None)
def angular_nodes(count):
    x,w=leggauss(count)
    return x/2,w/2,np.sqrt(1-(x/2)**2)


def string_potential(R,nmax=5,wmax=36,nodes=96,upper=None,rectangle=False):
    """Analytic tau2 integration of the previously supplied truncation.

    Integral t^-3 exp(-a t) from lower lo to infinity is E3(a lo)/lo^2;
    its R derivative is -a'(R) E2(a lo)/lo. Optional finite upper bound
    reproduces the old cutoff while a rectangle option reproduces its x grid.
    """
    Rc=np.sqrt(3/8)
    if R<=0 or R>Rc+1e-14:raise ValueError('Outside the tested tachyon-free interval')
    if rectangle:
        x=np.linspace(-.5,.5,401);weights=np.ones(401)/400;lo=np.sqrt(1-x*x)
    else:
        x,weights,lo=angular_nodes(nodes)
    total=np.zeros(2);parts=[]
    for q,ell,multiplicity in ((0.,0.,-222),(.5,0.,288),(.5,-1/6,-16)):
        n,w=np.meshgrid(np.arange(nmax+1)+q,np.arange(wmax+1),indexing='ij')
        multiplicities=np.where(n==0,1,2)*np.where(w==0,1,2)
        a=np.pi*(n*n/R**2+w*w*R**2+4*ell)
        if a.min() < -1e-12:raise ValueError('Negative exponent rate')
        a=np.maximum(a,0.)
        da=2*np.pi*(-n*n/R**3+w*w*R)
        arg=a[None,:,:]*lo[:,None,None]
        oscillation=np.cos(2*np.pi*x[:,None,None]*n[None,:,:]*w[None,:,:])
        value=expn(3,arg)/lo[:,None,None]**2
        derivative=-da[None,:,:]*expn(2,arg)/lo[:,None,None]
        if upper is not None:
            value-=expn(3,a*upper)[None,:,:]/upper**2
            derivative+=da[None,:,:]*expn(2,a*upper)[None,:,:]/upper
        prefactor=weights[:,None,None]*multiplicities*oscillation
        result=multiplicity*np.array([np.sum(prefactor*value),np.sum(prefactor*derivative)])
        total+=result;parts.append(result.tolist())
    return total,parts


def threshold_tachyon_second_derivative(R,nodes=128):
    _,weights,lo=angular_nodes(nodes)
    a=np.pi/(4*R*R)-2*np.pi/3
    if a<=0:raise ValueError('Second derivative formula is for the open window')
    da=-np.pi/(2*R**3);dda=3*np.pi/(2*R**4)
    return float(-32*(da*da*np.sum(weights*expn(1,a*lo))-
                      dda*np.sum(weights*expn(2,a*lo)/lo)))


def string_audit():
    edge=np.sqrt(3/8)
    radii=np.r_[np.linspace(.1,.6,101),np.linspace(.6,edge,101)[1:]]
    values=np.array([string_potential(float(r),nodes=80)[0] for r in radii])
    pick=int(np.argmin(values[:,1]));assert values[pick,1]>0
    controls={}
    for R in (.15,.4,.6,edge):
        values_hi=string_potential(R,nmax=6,wmax=45,nodes=160)[0]
        values_lo=string_potential(R,nmax=5,wmax=36,nodes=80)[0]
        controls[str(R)]=dict(value=float(values_hi[0]),derivative=float(values_hi[1]),
                              refined_vs_base_abs_error=np.abs(values_hi-values_lo).tolist())
    exact_rect=string_potential(.4,nmax=8,wmax=8,upper=40.,rectangle=True)[0][0]
    exact_legendre=string_potential(.4,nmax=8,wmax=8,upper=40.,nodes=160)[0][0]
    old=json.loads((ROOT/'analysis/search_drivers_12335/controls.json').read_text())['R04_T40']
    coefficient=4096*np.pi**2/27
    critical=[]
    for dx in (1e-5,1e-7,1e-9):
        R=edge-dx;rate=np.pi/(4*R*R)-2*np.pi/3
        curvature=threshold_tachyon_second_derivative(R)
        critical.append(dict(distance=dx,rate=float(rate),tachyon_mode_second_derivative=curvature,
                             regularized=float(curvature+coefficient*np.log(1/rate))))
    assert abs(critical[-1]['regularized']-critical[-2]['regularized'])<.1
    small_coefficient=222*2/5*quad(lambda x:(1-x*x)**(-5/4),-.5,.5,epsabs=1e-12)[0]
    return dict(species='-222 integer massless +288 half-integer massless -16 half-integer internal tachyons',
        edge_R=float(edge),nodes=201,interval=[.1,float(edge)],min_sampled_slope=float(values[pick,1]),
        min_sampled_slope_R=float(radii[pick]),controls=controls,
        original_R04_T40=old,exact_tau2_same_rectangle_T40=float(exact_rect),
        exact_tau2_gauss_angular_T40=float(exact_legendre),
        cutoff_infinity_gauss_value=float(string_potential(.4,nmax=6,wmax=45,nodes=160)[0][0]),
        small_R_coefficient=float(small_coefficient),
        small_R_formula='V(R) ~ -C/R, C=(444/5) integral_{-1/2}^{1/2} (1-x^2)^(-5/4) dx',
        threshold_second_derivative_singular_coefficient='-4096*pi^2/27',
        threshold_law='As a=pi/(4R^2)-2pi/3 tends to0+, the n=+-1/2,w=0 tachyon contribution obeys V_second=-(4096*pi^2/27) log(1/a)+O(1). Its value and first derivative are finite at the edge; the second derivative diverges to minus infinity.',
        threshold_numerical_controls=critical,
        boundary='The sampled derivative is positive at201 points, not an interval proof of monotonicity. Tau2 is integrated analytically, but angular quadrature and mode cutoffs are numerical. Massive internal states and winding projections are omitted. This finite-state truncation is not a modular-invariant full string partition function or a stabilized vacuum.')


def run():
    result=[six_loop_response(T,mu) for T,mu in ((0.,.3),(.25,-.4),(1.,0.))]
    interacting=[interacting_six_loop_response(U) for U in (0.,2.,8.)]
    assert result[0]['static_eigenvalues'][0]<-.08 and result[0]['static_eigenvalues'][-1]>.04
    assert result[0]['electric_eigenvalues'][0]>.019
    assert result[0]['best_common_cone_relative_residual']>.99
    assert interacting[1]['best_common_cone_relative_residual']>.59
    assert interacting[1]['static_vs_electric_relative_residual']>.68
    return dict(schema='w33.pass12341_12345.physics.v1',matter=result,interacting_matter=interacting,chirality=charge_anomalies(),
        string=string_audit(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        prior_owners=['analysis/w33_20261027_microscopic_response_and_lifts.py',
          'analysis/w33_20261027_five_front_followthrough.py',
          'analysis/search_drivers_12335/potential.py',
          'analysis/w33_20261028_five_fronts_followup.py'])


if __name__=='__main__':
    data=run();target=ROOT/'data/w33_pass12341_12345_physics.json'
    target.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',matter_ward=max(x['combined_gauge_density_ward_residual'] for x in data['matter']),
                          min_sampled_slope=data['string']['min_sampled_slope'])))
