"""Controlled continuum EFT, Clifford extension and bounded current dynamics.

The external spatial lattice, CAR extension and regulator are supplied.
Prior lattice fermion/overlap objects: BT4057_BT4064, BT4105_BT4112 and
PASS11570_11579_EXECUTABLE_GAUGE_GRAVITY_OVERLAP. No doubling novelty claimed.
"""
from pathlib import Path
import hashlib,itertools,json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11769_quantized_current_vacuum as A
OUT=ROOT/'data/w33_pass11771_11773_11777_cones_fermions_propagation.json'


def oscillator_response():
    g=A.geometry();tr=A.exact_trial()
    m,t,f=[tr[k] for k in ('m','t','f')]
    vx,vy,c=t*m,m/t+f*f*t*m,f*t*m
    b=1/20;pw,adj=g['pw'],g['g']
    bm=np.diag(g['s'])@(4*pw-adj)
    q=2*(vy+b)*(4*pw-adj)
    p=2*(vx+b)*(4*pw+adj)
    r=4*(c+b)*bm.T
    pinv=(pw/4-adj/10+(adj@adj)/40)/(2*(vx+b))
    assert np.allclose(p@pinv,pw,atol=2e-13)
    omega=np.block([[np.zeros((80,80)),pw],[-pw,np.zeros((80,80))]])
    hess=np.block([[q,r],[r.T,p]])
    generator=omega@hess
    alpha=4*((vx+b)*(vy+b)-4*(c+b)**2)
    target=alpha*(16*pw-adj@adj)
    assert alpha>0
    assert np.allclose(generator@generator,-np.block([[target,np.zeros_like(pw)],
                         [np.zeros_like(pw),target]]),atol=2e-11)
    records=[]
    for lattice_laplacian in (0.,.2,1.3,4.):
        matched=hess.copy();matched[:80,:80]+=lattice_laplacian*pinv
        flow=omega@matched
        wanted=target+lattice_laplacian*pw
        error=float(np.max(np.abs(flow@flow+np.block([[wanted,np.zeros_like(pw)],
                              [np.zeros_like(pw),wanted]]))))
        assert error<2e-11
        records.append(dict(lattice_laplacian=lattice_laplacian,error=error))
    return dict(status='PASS',covariance_moments=dict(vx=vx,vy=vy,cross=c),
        alpha=float(alpha),frequency_squared_48=float(10*alpha),frequency_squared_30=float(16*alpha),
        exact_frequency_ratio='sqrt(16/10)',
        hessian='Q=2(vy+b)(4P-A); Pmom=2(vx+b)(4P+A); R=4(c+b)*Bsum^T; b=1/20.',
        interpretation='Fixed-covariance Gaussian displacement variational dynamics; not the exact many-body excitation spectrum.',
        naive_gradient='Adding kappa*lattice_Laplacian*I to Q gives squared speed proportional to the kinetic eigenvalues2(vx+b)*(4+lambda), lambda=+sqrt6,-sqrt6,0. It generally produces different cones.',
        matched_gradient='Add kappa*lattice_Laplacian*Pmom^-1 to Q. The exact phase-space flow square then shifts by -kappa*lattice_Laplacian*I in every internal sector.',
        inverse_exact='Pmom^-1=(P/4-A/10+A^2/40)/(2(vx+b)); only distance<=2 internal adjacency is needed.',
        matched_checks=records,
        continuum='On a supplied cubic3D lattice with spacing ell, choose kappa=c0^2/ell^2; omega_j(k)^2=omega_j(0)^2+(4c0^2/ell^2)*sum_i sin(k_i*ell/2)^2. At fixed k, ell->0 gives omega_j(0)^2+c0^2*|k|^2.',
        boundary='Spatial dimension, c0, the lattice, spring law and covariance restriction are supplied. Common Lorentz-like quadratic dispersion is not a derivation of3+1 spacetime, interacting Lorentz symmetry, GR or particle masses.')


def clifford_extension():
    g=A.geometry();edges=A.actual_edges()
    pair=g['v']@g['u'].T
    adjacent=[]
    for e in range(160):
        for f in range(e+1,160):
            disjoint=set(edges[e]).isdisjoint(edges[f])
            assert disjoint==(abs(pair[e,f])<1e-12 and abs(pair[f,e])<1e-12)
            if not disjoint:adjacent.append([e,f])
    assert len(adjacent)==480
    # Independent finite Clifford identity check; the symbolic formula scales
    # to160 currents without materializing a2^80-dimensional spinor matrix.
    sx=np.array([[0,1],[1,0]],complex)
    sy=np.array([[0,-1j],[1j,0]],complex)
    sz=np.diag([1,-1]).astype(complex)
    gamma=[sx,sy,sz];currents=[sx+sz,sy-2*sz,2*sx-sy]
    d=sum(np.kron(c,j) for c,j in zip(gamma,currents))
    rhs=np.kron(np.eye(2),sum(j@j for j in currents))
    for e in range(3):
        for f in range(e+1,3):
            rhs+=np.kron(gamma[e]@gamma[f],currents[e]@currents[f]-currents[f]@currents[e])
    assert np.allclose(d@d,rhs)
    zeros=[]
    for bits in itertools.product((0,1),repeat=3):
        zeros.append(dict(corner_pi_units=list(bits),chirality=(-1)**sum(bits),
                          wilson_mass=2*sum(bits)))
    assert sum(r['chirality'] for r in zeros)==0
    return dict(status='PASS',adjacent_curvature_pairs=480,
        proposed_supercharge='Dslash=sum_e gamma_e tensor J_e; {gamma_e,gamma_f}=2delta_ef.',
        square_identity='Dslash^2=I tensor H+sum_(e<f) gamma_e gamma_f tensor [J_e,J_f].',
        spinor_complex_dimension='2^80',chirality='Gamma_star anticommutes with all160 gamma_e and hence with Dslash.',
        locality='Only480 pairs of adjacent incidence edges contribute curvature; all disjoint-pair commutators vanish.',
        square_check_error=float(np.max(np.abs(d@d-rhs))),
        supersymmetry_boundary='The spin-curvature term can cancel positive bosonic energy. The11770 floor for H does not automatically bound Dslash^2. No Fredholm index or normalizable supersymmetric vacuum is proved.',
        lattice_control={'operator':'h(k)=sum_i sigma_i sin(k_i)', 'zeros':zeros,
            'net_chirality':0,'prior':'BT4057_BT4064 already supplies the4D Wilson/16-corner control; BT4105_BT4112 and later packets supply overlap operators. This3D eight-corner replay is a control, not a new no-go theorem.'},
        interaction_boundary='This supplies a CAR/Clifford sector and explicit boson-spin interactions. It does not identify the160 Clifford labels with SM fermions, establish Weyl chirality in spacetime or construct the E6 Yukawa map.',
        literature='https://maggiexheuw.github.io/pdf/nielsen19812.pdf')


def bounded_propagation():
    tr=A.exact_trial();m,t,f=[tr[k] for k in ('m','t','f')]
    vx,vy,c=t*m,m/t+f*f*t*m,f*t*m;b=1/20
    sigma=np.array([[vx,c],[c,vy]])
    nodes,weights=np.polynomial.hermite_e.hermegauss(5)
    weights/=np.sqrt(2*np.pi)
    eta=np.array(np.meshgrid(nodes,nodes,indexing='ij')).reshape(2,-1)
    w=np.outer(weights,weights).ravel()
    x,y=np.linalg.cholesky(sigma)@eta+np.sqrt(b)
    fourth_sum=160*float(w@((x*y)**4))
    swap=np.array([[0,1],[1,0]])
    mu=np.full(2,np.sqrt(b));rows=[]
    for tau in (.01,.05,.1,.2):
        z=np.eye(2)-1j*tau*sigma@swap
        characteristic=np.exp(1j*tau*(mu@swap@np.linalg.solve(z,mu))/2)/np.sqrt(np.linalg.det(z))
        energy=160*2*(1-characteristic.real)/tau**2
        difference=tr['energy']-energy
        bound=tau*tau*fourth_sum/12
        assert -1e-8<difference<bound+1e-8
        rows.append(dict(tau=tau,trial_energy=float(energy),error=float(difference),
                         fourth_moment_error_bound=float(bound),term_norm_bound=4/tau**2))
    return dict(status='PASS',
        regularized_hamiltonian='H_tau=(2/tau^2)*sum_e(I-cos(tau*J_e)); each edge term has norm<=4/tau^2.',
        form_control='0<=<H-H_tau>_psi<=tau^2/12*sum_e||J_e^2 psi||^2 on Schwartz space. This supplies controlled form convergence for each such vector, not automatically spectral-gap convergence.',
        gaussian_fourth_current_moment_sum=fourth_sum,trial_records=rows,
        locality='Bounded functions of disjoint currents commute, so fixed-tau interactions form a bounded local current net.',
        finite_graph_bound='For A supported on edge e, B on f, the formal support theorem and bounded H_tau give ||[alpha_t(A),B]|| <=2||A||||B|| sum_(k>=max(0,d(e,f)-1)) (2||H_tau||*abs(t))^k/k!, with ||H_tau||<=640/tau^2.',
        LR_scope='Bounded commuting local algebras admit the usual Lieb-Robinson commutator iteration; a conservative weighted-interaction estimate at degree4 has velocity parameter<=64*exp(mu)/(mu*tau^2). This diverges as tau->0. No regulator-uniform causal speed for H is established.',
        boundary='A bounded regularization is a changed energy law. Its positive floor cannot be inferred from H_tau<=H. Neither finite Fock cutoffs nor bounded velocities at fixed tau prove a causal continuum for the unregularized model.',
        literature='https://arxiv.org/abs/math-ph/0506030')


def payload():
    return dict(schema='w33.pass11771_11773_11777.v1',
        source_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
        pass11771=oscillator_response(),pass11773=clifford_extension(),pass11777=bounded_propagation())


if __name__=='__main__':
    result=payload();OUT.write_text(json.dumps(result,indent=2)+'\n')
    print('11771 PASS kinetic-matched common cone;11773 PASS Clifford curvature;11777 PASS bounded propagation/form controls')
