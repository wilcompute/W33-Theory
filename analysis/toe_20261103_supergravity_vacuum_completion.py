"""Couple the actual prior holomorphic vacuum EFT to declared N=1 supergravity.

Canonical tree-level Kahler potential and a supplied Planck scale. Standard
supergravity formulas: Martin's Supersymmetry Primer, section7.6.
"""
import json,math,pathlib,sys
import numpy as np
import sympy as s
from scipy.optimize import root
ROOT=pathlib.Path(__file__).resolve().parents[1]
WEIGHTS=np.array([2,1,1,1,1,1,1,1],float)

def setup():
    old=json.loads((ROOT/'data/w33_20261103_native_quantum_vacuum_displacement.json').read_text())
    variables=s.symbols('t z r q l k S T');local=dict(zip(old['variables'],variables));eps=s.Symbol('epsilon');wc=s.Symbol('Wconstant')
    tree=s.sympify(old['neutral_tree_superpotential'],locals=local);P=s.sympify(old['mass_Pfaffian'],locals=local)
    W=tree+3*eps*(P/variables[0]**2)**s.Rational(1,3)+wc
    return (s.lambdify((*variables,eps,wc),W,'numpy'),
        s.lambdify((*variables,eps,wc),s.Matrix([s.diff(W,x)for x in variables]),'numpy'),
        s.lambdify((*variables,eps,wc),s.hessian(W,variables),'numpy'))

def global_point(epsilon):
    def equation(b):
        tt=1+5*b*b;R=2*(1+5*b)/tt;A=b*tt/(1-2*b-5*b*b)
        return A*tt*complex(R)**(2/3)-epsilon
    def real(y):
        v=equation(complex(*y));return [v.real,v.imag]
    b0=2**(-2/3)*epsilon;sol=root(real,[b0.real,b0.imag],tol=1e-12);b=complex(*sol.x)
    assert abs(equation(b))<2e-15
    tt=1+5*b*b;R=2*(1+5*b)/tt;A=b*tt/(1-2*b-5*b*b);z=A*(1-R)
    return np.array([complex(tt)**.5,z,1,1,5*b,-b,3*A-z,-2*A-z],complex)

def values(functions,phi,epsilon,wc=0):
    args=(*phi,epsilon,wc);W=complex(functions[0](*args));F=np.array(functions[1](*args),complex).ravel();H=np.array(functions[2](*args),complex)
    return W,F,H

def DW(functions,phi,epsilon,alpha,wc=0):
    W,F,H=values(functions,phi,epsilon,wc);return F+alpha*WEIGHTS*phi.conj()*W

def potential(functions,phi,epsilon,alpha,wc=0):
    W,F,H=values(functions,phi,epsilon,wc);D=F+alpha*WEIGHTS*phi.conj()*W;K=float(np.sum(WEIGHTS*abs(phi)**2))
    return math.exp(alpha*K)*(float(np.sum(abs(D)**2/WEIGHTS))-3*alpha*abs(W)**2)

def supergravity_point(functions,seed,epsilon,alpha,wc=0):
    def unpack(y):return y[:8]+1j*y[8:]
    def eq(y):
        D=DW(functions,unpack(y),epsilon,alpha,wc);return np.r_[D.real,D.imag]
    def jac(y):
        phi=unpack(y);W,F,H=values(functions,phi,epsilon,wc);ki=WEIGHTS*phi.conj()
        A=H+alpha*np.outer(ki,F);B=alpha*W*np.diag(WEIGHTS)
        return np.block([[(A+B).real,-(A-B).imag],[(A+B).imag,(A-B).real]])
    sol=root(eq,np.r_[seed.real,seed.imag],jac=jac,tol=1e-11)
    assert np.max(abs(eq(sol.x)))<3e-12
    return unpack(sol.x)

def finite_scalar_hessian(functions,phi,epsilon,alpha,h=2e-4):
    q=np.r_[phi.real,phi.imag];v0=potential(functions,phi,epsilon,alpha);H=np.zeros((16,16))
    def V(y):return potential(functions,y[:8]+1j*y[8:],epsilon,alpha)
    for i in range(16):
        a=np.zeros(16);a[i]=h;H[i,i]=(V(q+a)-2*v0+V(q-a))/h**2
        for j in range(i):
            b=np.zeros(16);b[j]=h;H[i,j]=H[j,i]=(V(q+a+b)-V(q+a-b)-V(q-a+b)+V(q-a-b))/(4*h*h)
    scale=1/np.sqrt(2*np.r_[WEIGHTS,WEIGHTS]);return H*np.outer(scale,scale)

def build():
    funcs=setup();rows=[];seeds=[]
    for j in range(3):
        epsilon=.001*np.exp(2j*np.pi*j/3);seed=global_point(epsilon);Wg,Fg,Hg=values(funcs,seed,epsilon)
        assert np.max(abs(Fg))<3e-13;seeds.append((epsilon,seed,Wg))
        for Mp in [10.,30.,100.]:
            alpha=1/Mp**2;phi=supergravity_point(funcs,seed,epsilon,alpha);W,F,H=values(funcs,phi,epsilon)
            K=float(np.sum(WEIGHTS*abs(phi)**2));v=potential(funcs,phi,epsilon,alpha);expected=-3*alpha*math.exp(alpha*K)*abs(W)**2
            assert v<0 and abs(v/expected-1)<2e-10
            first=-alpha*np.linalg.solve(Hg,WEIGHTS*seed.conj()*Wg)
            error=float(np.max(abs(phi-seed-first)))
            # At D W=0, covariant Z_ij=W_ij-alpha^2 K_i K_j W.
            ki=WEIGHTS*phi.conj();Z=H-alpha*alpha*W*np.outer(ki,ki)
            norm=1/np.sqrt(WEIGHTS);Zhat=Z*np.outer(norm,norm);mf=math.exp(alpha*K/2)*np.linalg.svd(Zhat,compute_uv=False)
            mgr=alpha*math.exp(alpha*K/2)*abs(W)
            masses=np.sort(np.r_[mf*mf-2*mgr*mgr-mgr*mf,mf*mf-2*mgr*mgr+mgr*mf])
            assert masses[0]>0
            if j==0 and Mp==30:
                fd=np.linalg.eigvalsh(finite_scalar_hessian(funcs,phi,epsilon,alpha));fd_err=float(np.max(abs(fd-masses)))
                assert fd_err<4e-5
            else:fd_err=None
            # A constant nilpotent uplift can cancel V at the old point but has
            # a nonzero scalar gradient there; stationarity must be solved again.
            f2=3*alpha*abs(W)**2;uplift_grad=alpha*math.exp(alpha*K)*ki*f2
            assert np.max(abs(uplift_grad))>0
            rows.append(dict(gaugino_branch=j,epsilon=[epsilon.real,epsilon.imag],Planck_mass_in_input_units=Mp,
                scalar_VEV_complex_pairs=[[float(a.real),float(a.imag)]for a in phi],DW_max_residual=float(np.max(abs(DW(funcs,phi,epsilon,alpha)))),
                potential=v,AdS_formula=expected,gravitino_mass=mgr,neutral_scalar_mass_squared=masses.tolist(),
                independent_real_finite_difference_mass_error=fd_err,first_order_in_inverse_Planck_squared_displacement_error=error,
                naive_energy_cancelling_nilpotent_f_squared=f2,naive_uplift_holomorphic_gradient_max=float(np.max(abs(uplift_grad)))))
    # A deliberately tuned constant can make one global F-flat solution exactly
    # supersymmetric Minkowski, since both W and its gradient then vanish.
    wc=-seeds[0][2];tuned=[]
    for j,(epsilon,seed,Wg)in enumerate(seeds):
        phi=supergravity_point(funcs,seed,epsilon,1/900,wc)
        W,F,H=values(funcs,phi,epsilon,wc);v=potential(funcs,phi,epsilon,1/900,wc)
        if j==0:assert abs(W)<1e-13 and abs(v)<1e-24
        else:assert v<0
        tuned.append(dict(branch=j,potential=v,absolute_total_superpotential=abs(W)))
    return dict(status='PASS_SUPERGRAVITY_ADS_COMPLETION_AND_TUNING_CONTROLS',rows=rows,tuned_constant_complex_pair=[wc.real,wc.imag],single_constant_control=tuned,
        supplied_gravity='4D two-derivative N=1 supergravity, canonical tree-level K=sum_i w_i |phi_i|^2 with weights[2,1,1,1,1,1,1,1], supplied Planck mass, and the prior holomorphic eight-field effective superpotential. Sp gauge moments vanish on the singlet ansatz.',
        potential='V=exp(K/Mp^2)*(sum_i |D_i W|^2/w_i-3|W|^2/Mp^2), D_i W=partial_i W+w_i conjugate(phi_i) W/Mp^2',
        conclusion='The actual nearby supersymmetric gravitational vacua have negative vacuum energy for nonzero W. Global F-flatness and Vglobal=0 do not solve the observed cosmological-constant problem.',
        constant_control='An adjustable Wconstant=-W(global critical point) makes that one point exactly supersymmetric Minkowski. The same chosen constant does not cancel the other two gaugino branches. This is explicit tuning, not a prediction.',
        nilpotent_control='For Kadd=X Xbar,Wadd=fX,X^2=0, adding exp(K/Mp^2)|f|^2 can cancel the energy at the former AdS point but gives gradient_i=(exp(K/Mp^2)/Mp^2)*K_i*|f|^2 there. Nonzero gradients are exported; no de Sitter vacuum is claimed from energy cancellation alone.',
        scalar_mass_control='At SUSY AdS, neutral canonical scalar masses are mf^2-2mgr^2+-mgr*mf. The smaller branch equals(mf-mgr/2)^2-(9/4)mgr^2, verifying the Breitenlohner-Freedman bound. The displayed weak examples have positive masses; an independent16-real-coordinate finite difference checks one case.',
        source='https://arxiv.org/abs/hep-ph/9709356',
        ownership='The Nov3 native29 producer owns the supplied deformed global model, and the quantum-vacuum-displacement producer owns its exact effective critical curve. Standard supergravity/AdS formulas are prior physics. This constructs the gravitational consistency test of that concrete EFT.',
        boundary='Declared low-energy supergravity with a chosen Kahler potential and hierarchy, not a derived quantum-gravity UV completion, positive observed vacuum energy or solution of the TOE.')

if __name__=='__main__':
    d=build();(ROOT/'data/toe_20261103_supergravity_vacuum_completion.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');print(d['status'],[(r['gaugino_branch'],r['Planck_mass_in_input_units'],r['potential'])for r in d['rows']],flush=True)
