"""Exact nonlinear cone obstruction, magnetic curvature and Lorentzian lift.

The metric is that of fixed-covariance Gaussian variational mechanics.
It is not identified with the full quantum principal symbol or Einstein gravity.
Eisenhart--Duval lifting is a standard construction, applied to this explicit
W33 Hamiltonian; the curvature certificate uses exact integer geometry.
"""
from pathlib import Path
import hashlib,json,sys
from fractions import Fraction
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11769_quantized_current_vacuum as A
OUT=ROOT/'data/w33_pass11781_11784_11785_nonlinear_cone_bargmann_lift.json'


def setup():
    g=A.geometry();trial=A.exact_trial();m=trial['m'];t=trial['t'];f=trial['f']
    basis=np.linalg.qr(g['pw'][:,np.r_[0:39,40:79]])[0]
    return dict(g=g,basis=basis,u=g['u']@basis,v=g['v']@basis,
                a=np.sqrt(.05),vx=t*m,vy=m/t+f*f*t*m,c=f*t*m)


def coefficients(q,z=None):
    z=setup() if z is None else z
    u,v,a,vx,vy,c=(z[k] for k in ('u','v','a','vx','vy','c'))
    x=v@q+a
    kinetic=2*u.T@((vx+x*x)[:,None]*u)
    linear=u.T@(2*a*x*x+4*c*x)
    scalar=np.sum((vx+x*x)*a*a+vy*x*x+4*c*x*a+vx*vy+2*c*c)
    connection=-np.linalg.solve(kinetic,linear)
    effective=scalar-.5*linear@np.linalg.solve(kinetic,linear)
    jac=-np.linalg.solve(kinetic,u.T@((4*x*(u@connection+a)+4*c)[:,None]*v))
    return kinetic,linear,float(scalar),connection,float(effective),jac-jac.T


def wick_energy(q,p,z=None):
    z=setup() if z is None else z
    x=z['v']@q+z['a'];y=z['u']@p+z['a']
    return float(np.sum(x*x*y*y+z['vx']*y*y+z['vy']*x*x+4*z['c']*x*y
                        +z['vx']*z['vy']+2*z['c']**2))


def nonlinear_cone():
    z=setup();g=z['g'];w=np.r_[g['kernel_witness'],np.zeros(40)]
    p0=coefficients(np.zeros(78),z)[0];p0i=np.linalg.inv(p0)
    leverage=np.einsum('ij,jk,ik->i',z['u'],p0i,z['u'])
    exact_leverage=39/(160*(z['vx']+.05))
    assert np.max(np.abs(leverage-exact_leverage))<1e-13
    samples=[]
    for epsilon in [0,.01,.1,.5]:
        q=epsilon*w@z['basis'];p,_,_,_,_,curl=coefficients(q,z)
        # Symmetric generalized eigenproblem, rather than a nonnormal eigenvalue call.
        root=np.linalg.cholesky(p0);ri=np.linalg.inv(root)
        speeds=np.linalg.eigvalsh(ri@p@ri.T)
        trace=float(np.trace(p@p0i)-78)
        expected=2106*epsilon**2/(5*(z['vx']+.05))
        assert abs(trace-expected)<1e-10
        samples.append(dict(epsilon=epsilon,squared_speed_min=float(speeds[0]),
            squared_speed_max=float(speeds[-1]),trace_excess=trace,
            curvature_frobenius=float(np.linalg.norm(curl))))
    return dict(status='EXACT_NONLINEAR_OBSTRUCTION',
        variational_energy='E(q,p)=sum[x_e^2*y_e^2+vx*y_e^2+vy*x_e^2+4*c*x_e*y_e+vx*vy+2*c^2], x=Vq+a,y=Up+a.',
        kinetic='P(q)=2*U^T*diag(vx+(Vq+a)^2)*U. It is positive definite globally since vx>0 and U has rank78.',
        fixed_gradient='With the11771 centered matched spatial gradient P(0)^(-1), the squared-speed matrix at background q is P(q)P(0)^(-1).',
        exact_trace='For q=epsilon*(w_point,0), norm(w)^2=216, trace[P(q)P(0)^(-1)]-78=2106*epsilon^2/[5*(vx+1/20)]>0 if epsilon!=0.',
        leverage='u_e^T*P(0)^(-1)*u_e=39/[160*(vx+1/20)] for every actual edge. Linear trace terms cancel since sum V_e=0; sum(V_e.w)^2=864.',
        samples=samples,
        boundary='This is an exact Wick/finite-background obstruction in the fixed-covariance Gaussian variational model, not a computed one-loop self-energy. The common centered quadratic cone has no automatic nonlinear protection; a background-dependent gradient would be an additional prescription.')


def exact_curvature():
    z=setup();g=z['g'];w=np.r_[g['kernel_witness'],np.zeros(40)].astype(np.int64)
    u40=np.rint(40*g['u']).astype(np.int64);v40=np.rint(40*g['v']).astype(np.int64)
    pw40=np.rint(40*g['pw']).astype(np.int64);g10=np.rint(10*g['g']).astype(np.int64)
    assert np.max(np.abs(u40/40-g['u']))<1e-14
    assert np.all((v40@w)%40==0)
    x=(v40@w)//40
    mnum=25*pw40-40*g10+g10@g10
    numerator=mnum@u40.T@(x[:,None]*v40)
    skew=numerator-numerator.T
    r=np.zeros(80,dtype=np.int64);r[0]=1;r[39]=-1
    s=np.zeros(80,dtype=np.int64);s[40]=1;s[79]=-1
    entry=Fraction(int(r@skew@s),6400000)
    assert entry==Fraction(-31,10)
    beta=2*(z['c']+.05)/(z['vx']+.05)
    coefficient=-31*.05*(2*beta-1)/(5*(z['vx']+.05))
    q=z['a']*1e-5*w@z['basis'];curl=coefficients(q,z)[-1]
    measured=float((r@z['basis'])@curl@(s@z['basis']))/1e-5
    assert abs(measured-coefficient)<1e-5
    return dict(status='EXACT_NONZERO_CURVATURE',
        connection='A(q)=-P(q)^(-1)*ell(q), ell=U^T[2a*(Vq+a)^2+4c*(Vq+a)]. E=.5*(p-A)^T*P*(p-A)+Veff.',
        effective_potential='Veff(q)=min_p E(q,p)>=E0>0 and Veff(q) tends to infinity as |q| tends to infinity. Otherwise normalized displaced fixed-covariance Gaussians at minimizing momenta would lie in a bounded form ball while converging weakly to zero by translation of their modulus, contradicting the11778 compact embedding.',
        beta='beta=2*(c+a^2)/(vx+a^2)',
        expansion='A(q)=-beta*Dq+2a*(2beta-1)*P(0)^(-1)*U^T*(Vq)^2+O(|q|^3).',
        integer_recipe='Mnum=25*(40Pw)-40*(10Adj)+(10Adj)^2; Snum=antisym[Mnum*(40U)^T*diag(Vw)*(40V)]. M=Pw/4-Adj/10+Adj^2/40.',
        witness_r=r.tolist(),witness_s=s.tolist(),denominator=6400000,
        contracted_integer=int(r@skew@s),contracted_exact=str(entry),
        directional_taylor='For q=a*epsilon*w, r^T*(dA-dA^T)*s = -31*a^2*(2beta-1)/[5*(vx+a^2)]*epsilon+O(epsilon^2).',
        coefficient=float(coefficient),finite_difference_coefficient=measured,
        consequence='The induced momentum shift is not locally removable by a scalar canonical phase on a neighborhood of the origin. Nonzero exterior curvature is basis invariant.',
        boundary='An induced variational magnetic two-form, not an identified SM gauge field or a solution of gravitational field equations.')


def lorentzian_lift():
    g,a,v=sp.symbols('g a v',real=True,nonzero=True)
    metric=sp.Matrix([[g,a,0],[a,-2*v,1],[0,1,0]])
    inverse=sp.Matrix([[1/g,0,-a/g],[0,0,1],[-a/g,1,2*v+a*a/g]])
    assert sp.simplify(metric*inverse)==sp.eye(3)
    p,pu,pv=sp.symbols('p pu pv',real=True)
    momenta=sp.Matrix([p,pu,pv])
    h=(momenta.T*inverse*momenta)[0]/2
    assert sp.simplify(h-((p-pv*a)**2/(2*g)+pu*pv+v*pv*pv))==0
    return dict(status='EXACT_STANDARD_LIFT_APPLIED',dimension=80,signature_positive=79,signature_negative=1,
        metric='ds^2=G_ij(q)dq_i*dq_j+2du[dv+A_i(q)dq_i-Veff(q)du], G=P^(-1).',
        hamiltonian='H_lift=.5*(p-p_v*A)^T*P*(p-p_v*A)+p_u*p_v+Veff*p_v^2.',
        reduction='The conserved p_v=1 and null constraint H_lift=0 give p_u+E(q,p)=0 exactly.',
        signature_proof='The coframe dv_prime=dv+A.dq-Veff*du gives G(dq,dq)+2du*dv_prime pointwise. Positive G yields79 positive and1 negative direction; partial_v is a null Killing vector.',
        energy_shift='Veff -> Veff+Lambda is removed by v_new=v-Lambda*u. This lift cannot by itself identify a constant vacuum energy with a measurable cosmological constant.',
        quantum_clock='Independently, C=p_t+H for the actual self-adjoint11769 Hamiltonian has solutions Psi(t)=exp(-itH)psi0; group averaging retains physical L2(R78). This supplied ideal clock needs no matter-killing opposite-center constraint.',
        boundary='A standard Eisenhart-Duval lift of the fixed-covariance variational Hamiltonian and a supplied parametrized clock. Not a derived3+1 spacetime, Einstein dynamics, observed mass spectrum or cosmological-constant solution.',
        literature=['https://arxiv.org/abs/1503.07802','https://arxiv.org/abs/1605.01932'])


def payload():
    return dict(schema='w33.pass11781_11784_11785.v1',
        source_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
        pass11781=nonlinear_cone(),pass11784=exact_curvature(),pass11785=lorentzian_lift())


if __name__=='__main__':
    result=payload();OUT.write_text(json.dumps(result,indent=2)+'\n')
    print('11781 nonlinear common-cone obstruction;11784 exact magnetic curvature;11785 Lorentzian lift/clock PASS')
