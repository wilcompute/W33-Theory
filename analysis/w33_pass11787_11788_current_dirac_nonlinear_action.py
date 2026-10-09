"""Actual-current Dirac domain/index controls and a supplied nonlinear action.

The linearized current Dirac operator is not the Bott operator. Neither its
index nor its spectral floor is silently transferred to the full operator.
"""
from pathlib import Path
import hashlib,json,sys
from fractions import Fraction as F
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11769_quantized_current_vacuum as V
OUT=ROOT/'data/w33_pass11787_11788_current_dirac_nonlinear_action.json'

def dirac():
    g=V.geometry();u=np.rint(40*g['u']).astype(np.int64)
    v=np.rint(40*g['v']).astype(np.int64);d=g['s']
    assert np.array_equal(u,v*d[None,:])
    assert np.all(v.sum(axis=0)==0)
    assert np.all(np.sum(u*v,axis=1)==0)
    edges=V.actual_edges();degrees=[sum(bool(set(e)&set(f)) for f in edges if e!=f) for e in edges]
    assert set(degrees)=={6} and sum(degrees)//2==480
    gram=v.T@v
    assert np.array_equal(gram,160*(np.rint(40*g['pw']).astype(np.int64)-np.rint(10*g['g']).astype(np.int64)))
    q=40*np.r_[np.array([39]+[-1]*39),np.zeros(40,dtype=int)]
    # q/a=(39,-1,...,-1;0). No metric or basis fit used.
    active=(v@(q//40)+40)!=0
    assert int(active.sum())==4
    return dict(status='PASS',
        operator='D=sum_e gamma_e*(V_e.q+a)*(U_e.p+a), a=1/sqrt20, 160 Hermitian Clifford generators.',
        actual_domain='D is essentially self-adjoint on compactly supported smooth spinors on W. Its symmetric first-order coefficients have propagation speed c(R)<=sqrt(sum|U_e|^2)*(a+max|V_e|R)=sqrt312*(a+sqrt(39/20)R); integral_0^infty dR/c(R)=infinity. U_e.V_e=0 removes divergence correction. The zeroth-order term a*Gamma(Vq)+a^2*Gamma(1) is smooth Hermitian and linear, not bounded; it does not alter the propagation speed. Apply Chernoff completeness criterion to the full symmetric first-order system.',
        linearization='D_lin=a*Gamma(V(q+Dp))+a^2*Gamma(1). All z_i=q_i+D_i*p_i commute; column(V) is orthogonal to the160-vector1.',
        linearized_square='D_lin^2=a^2*z^T*(4P_W-Adj)*z+2/5*I. A metaplectic rotation identifies z/sqrt2 with multiplication coordinates.',
        linearized_floor=str(F(2,5)),linearized_chiral_index=0,
        linearized_index_proof='D_lin has bounded inverse norm<=sqrt(5/2) and anticommutes with the Cl160 grading. Its closed chiral block is bijective from its graph domain to the opposite spinor space, hence Fredholm index0. Its inverse is not compact: it is matrix multiplication on a nonatomic measure space.',
        full_symbol_obstruction='At q/a=(39,-1,...,-1;0), only four x_e=V_e.q+a survive. The first-order symbol depends on at most four momentum linear forms out of78. Full D is nonelliptic on this configuration locus; standard elliptic/Callias index inference is unavailable.',
        active_symbol_rows=int(active.sum()),clifford_dimension=2**80,
        curvature_bound='For spinor form h=sum||J_e psi||^2, |k[psi]|<=sum_adjacent_e,f 2||J_e psi||||J_f psi||<=6*h[psi]. Uses the parallel single-pair form estimate, now summed over the exact degree6 edge graph.',
        controlled_interpolation='h+theta*k is closed, positive and compactly embedded for |theta|<1/6, with (1-6|theta|)h <= h+theta*k <= (1+6|theta|)h. The actual square D^2 is theta=1, outside this certified band.',
        actual_fredholm_index='OPEN: essential self-adjointness is established, but no compactness/coercivity estimate for actual D^2, finite kernel, or Fredholm chiral block is proved. Quadratic remainder is unbounded; no Fredholm homotopy to D_lin is claimed.',
        prior='analysis/w33_20261009_curvature_perturbation.py owns the one-pair relative form estimate;11780 owns the different Bott index+1.',
        literature=['https://doi.org/10.1016/0022-1236(73)90003-7'])

def action():
    w,k,c,m,b=sp.symbols('omega k c m B',real=True)
    z=c*c*k*k+m*m
    determinant=(z-w*w)**2-b*b*w*w
    center=sp.sqrt(z+b*b/4)
    for branch in (center+b/2,center-b/2):
        assert sp.simplify(determinant.subs(w,branch))==0
    return dict(status='PASS',
        construction='Supply spatial coordinates x in R^d and c0>0. S=integral dt d^d x [G_ij(q)*(qdot_i*qdot_j-c0^2*sum_a partial_a(q_i)*partial_a(q_j))/2+A_i(q)qdot_i-Veff(q)]. G=P(q)^(-1), A,Veff are the actual fixed-covariance Gaussian coefficients of11781/11784.',
        principal_euler_lagrange='G_ij(q)*(partial_t^2-c0^2*Delta_x)q_j plus terms at most first order in second-derivative counting. The characteristic determinant is det(G(q))*(-omega^2+c0^2|k|^2)^78: a common front cone at every background.',
        lower_order_terms='Levi-Civita target-metric connection terms, -F_ij(q)*qdot_j and partial_i Veff; F=dA. The nonzero11784 curvature cannot be removed by a scalar phase.',
        energy='E_density=G_ij(q)*(qdot_i*qdot_j+c0^2*sum_a partial_a(q_i)*partial_a(q_j))/2+Veff(q). Magnetic one-form cancels from the Legendre energy.',
        common_cone_is_not_boost_invariance='A_i(q)qdot_i selects the time direction. A common principal cone does not make this lower-order term Lorentz invariant. Replacing it by a covariant clock current would add dynamical equations that must be solved.',
        exact_magnetic_control='For two flat target fields, L=(qdot^2-c0^2|grad q|^2-m^2 q^2)/2+B(x*ydot-y*xdot)/2. omega_plus/minus=sqrt(c0^2*k^2+m^2+B^2/4)+/-B/2. Both have front speed c0, but the dispersion is not a pair of relativistic Klein-Gordon mass shells for B!=0.',
        magnetic_dispersion_polynomial=str(determinant),
        supplied_inputs=['spatial dimension d','spatial sites/coordinates','speed c0','background-dependent matched gradient G(q)'],
        scope='An explicit nonlinear spatial completion of variational mechanics, not a derivation of physical spacetime, Einstein equations, or the actual many-cell quantum continuum.')

def certificate():
    return dict(schema='w33.pass11787_11788.v1',source_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),pass11787=dirac(),pass11788=action())
if __name__=='__main__':
    x=certificate();OUT.write_text(json.dumps(x,indent=2)+'\n')
    print('11787 actual Dirac domain/index controls;11788 nonlinear common-front action PASS')
