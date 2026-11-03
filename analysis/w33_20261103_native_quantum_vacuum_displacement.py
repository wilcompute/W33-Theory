"""Explicit holomorphic thresholds and perturbative quantum vacuum displacement.

Continuation of the native29 deformed model, with supplied4D N=1 dynamics.
Sp SQCD decoupling/gaugino condensation are standard Intriligator-Pouliot input.
"""
import json,pathlib,sys
import sympy as s
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261103_native_singlet_stabilization import model,DUADS

def build():
    t,z,r,q,l,k,S,T=s.symbols('t z r q l k S T');a=[t,z,r,q,l,k,S,T]
    C=s.Matrix([[1+k,2+q],[3-r,5-l]])
    M=s.Matrix([[0,t,C[0,0],C[1,0]],[-t,0,C[0,1],C[1,1]],[-C[0,0],-C[0,1],0,t],[-C[1,0],-C[1,1],-t,0]])
    P=s.expand(t*t-C.det());assert s.expand(M.det()-P**2)==0
    x,W,v=model();at={y:0 for y in x}
    at.update({x[DUADS.index((0,2))]:t,x[DUADS.index((1,3))]:t,x[14]:z,x[19]:r,x[26]:q,x[20]:l,x[25]:k,x[27]:S,x[28]:T})
    # x14=A45 in the inherited lexicographic duad order.
    assert DUADS[14]==(4,5)
    Wn=z*(r*q-l*k-t*t)+l*k+S*(r-1)+T*(q-1)
    assert s.expand(W.subs(at)-Wn)==0
    charged=[DUADS.index((i,j))for j in [4,5]for i in range(4)]+list(range(15,19))+list(range(21,25))
    H=s.hessian(W,x).extract(charged,charged).subs(at)
    O=s.Matrix([[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]])
    B=s.diag(s.eye(4),s.eye(4),O,O)
    assert s.simplify(B.T*H*B-s.kronecker_product(M,O))==s.zeros(16)
    base={t:1,z:0,r:1,q:1,l:0,k:0,S:0,T:0};assert P.subs(base)==2
    R=P/t**2;U=3*R**s.Rational(1,3);H0=s.hessian(Wn,a).subs(base);assert H0.det()!=0
    grad=s.Matrix([s.diff(U,y).subs(base)for y in a]);d1=s.simplify(-H0.inv()*grad)
    c=2**s.Rational(-2,3);expected=s.Matrix([0,-c,0,0,5*c,-c,4*c,-c]);assert s.simplify(d1-expected)==s.zeros(8,1)
    Hnp=s.hessian(U,a).subs(base)
    nonlinear=s.Matrix([sum(s.diff(Wn,y,b,d).subs(base)*d1[j]*d1[h]for j,b in enumerate(a)for h,d in enumerate(a))/2 for y in a])
    d2=s.simplify(-H0.inv()*(nonlinear+Hnp*d1));assert s.simplify(d2[0]-s.Rational(5,2)*c*c)==0
    # Check all order0,1,2 F coefficients directly from the derivative tensors.
    assert s.Matrix([s.diff(Wn,y).subs(base)for y in a])==s.zeros(8,1)
    assert s.simplify(H0*d1+grad)==s.zeros(8,1)
    assert s.simplify(H0*d2+nonlinear+Hnp*d1)==s.zeros(8,1)
    assert s.simplify((M.det()).subs(base))==4
    # Continue beyond the series: eliminate all8 effective F equations by one
    # auxiliary parameter b. This is exact in the stated holomorphic EFT.
    b,e=s.symbols('b epsilon');tt=1+5*b*b;RR=2*(1+5*b)/tt
    AA=b*tt/(1-2*b-5*b*b);zz=AA*(1-RR)
    curve={t:s.sqrt(tt),z:zz,r:1,q:1,l:5*b,k:-b,S:3*AA-zz,T:-2*AA-zz}
    for y in a:
        # dWnp/dphi=A*(dP/dphi-2P/t for phi=t), with A=epsilon R^(-2/3)/t^2.
        Fi=s.diff(Wn,y)+s.Symbol('auxA')*(s.diff(P,y)-(2*P/t if y==t else 0))
        assert s.simplify(Fi.subs(curve,simultaneous=True).subs(s.Symbol('auxA'),AA))==0
    eps3=s.factor(AA**3*RR**2*tt**3)
    poly=s.expand(4*b**3*(1+5*b)**2*(1+5*b*b)**4-e**3*(1-2*b-5*b*b)**3)
    assert s.degree(poly,b)==13
    assert s.cancel(poly.subs(e**3,eps3))==0
    return dict(status='PASS_NATIVE29_HOLOMORPHIC_THRESHOLD_AND_QUANTUM_DISPLACEMENT',
        variables=list(map(str,a)),neutral_tree_superpotential=str(Wn),charged_flavor_matrix=[[str(x)for x in row]for row in M.tolist()],
        exact_charged_Hessian_factorization='diag(I4,I4,Omega,Omega)^T Hcharged diag(I4,I4,Omega,Omega)=Mflavor tensor Omega',
        mass_Pfaffian=str(P),charged_Hessian_determinant='P^8',mass_Pfaffian_at_classical_vacuum=2,
        holomorphic_matching='Lambda_Sp_Nf2^7=C_H*Lambda_SU4^9/t^2; Lambda_pure^9=C_m*P*Lambda_Sp_Nf2^7. Thus Lambda_pure^9=C*Lambda_SU4^9*P/t^2. Nonzero scheme/threshold constants absorbed in epsilon.',
        quantum_superpotential='Wneutral+3 epsilon*(P/t^2)^(1/3)',
        expansion='phi=phi0+epsilon*d1+epsilon^2*d2+O(epsilon^3), in the branch analytic near P/t^2=2. The three gaugino branches multiply epsilon by the three cube roots of unity.',
        classical_neutral_VEV=[int(base[y])for y in a],first_order_displacement=list(map(str,d1)),second_order_displacement=list(map(str,d2)),
        F_residual_coefficients_orders_0_1_2_all_zero=True,
        exact_effective_critical_curve=dict(parameter='b',coordinates={str(y):str(curve[y])for y in a},
            mass_Pfaffian='2+10*b',Higgs_modulus_squared='1+5*b^2',epsilon_cubed=str(eps3),
            eliminated_polynomial=str(poly),polynomial_degree=13,
            all8_effective_F_equations_identically_zero=True,
            exclusions='t=0, P=0 and1-2b-5b^2=0 are excluded from this massive Higgs patch. Squaring/cubing removes branch labels: solutions must be assigned to a consistent gaugino cube-root branch.',
            weak_branch='b=2^(-2/3)*epsilon+O(epsilon^2), three gaugino branches near b=0. Other algebraic roots are not automatically weakly coupled or additional physical vacua.',
            scope='Exact parametrized stationarity of the supplied holomorphic effective superpotential, with an algebraic scale relation; not proof of the complete finite-coupling UV dynamics.'),
        Higgs_modulus='t=1+(5/2)*2^(-4/3)*epsilon^2+O(epsilon^3); the radial shift starts at second order, while previously zero singlet coordinates shift already at first order.',
        exact_constraints='r=q=1 enforced by S,T for every epsilon; F_z gives t^2=1-l*k. Unbroken USp4 remains on this singlet ansatz.',
        classical_gauge_moment='chi=t Omega implies chi chi-dagger=|t|^2 I4. All other ansatz fields are SU4 singlets; charged fundamentals remain zero.',
        derivation='Exact full16-coordinate Hessian factorization, Pfaffian identity, tree neutral restriction and all8 formal F equations through epsilon^2. Pure-gauge superpotential and holomorphic matching are supplied standard dynamics, not derived from finite geometry.',
        assumptions='Canonical classical Kähler potential, supplied4D global N=1 SU4 gauge theory, the explicit native29 mass deformation, all heavy scales above Lambda, nonzero t and P, and standard Wilsonian holomorphic threshold matching. Fields/masses are in the common input mass unit.',
        ownership='Prior native29 stabilization owns the deformed model. Prior Nov3 effective audit owns the undeformed1/t matching and ADS obstruction. This computes the different deformed mass Pfaffian and its controlled quantum displacement.',
        reference='https://arxiv.org/abs/hep-th/9505006',
        boundary='Exact algebraic stationarity in the declared holomorphic EFT and explicit weak-coupling series through second order. No global UV solution, convergence bound, measured scale prediction or TOE.')

if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261103_native_quantum_vacuum_displacement.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');print(d['status'],d['mass_Pfaffian'],d['first_order_displacement'],flush=True)
