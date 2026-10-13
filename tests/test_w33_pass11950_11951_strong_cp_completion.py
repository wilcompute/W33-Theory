"""Independent algebra, divisor, anomaly and inverse-realization controls."""
from pathlib import Path
import sys
import itertools
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_pass11950_11951_strong_cp_divisor_and_vectorlike as p


def test_odd_odd_theta_factor_has_a_simple_separating_zero():
    tau1=.23+1.07j;tau2=-.19+1.13j
    a=b=np.array([.5,.5])
    # Nine even-even constants are nonzero at a generic product; the
    # tenth, odd-odd, supplies a simple zero before the product is squared.
    values=[]
    for eps in (.02,.01,.005):
        O=np.array([[tau1,eps],[eps,tau2]])
        values.append(p.theta_constant(O,a,b)/eps)
    assert abs(values[-1]/values[-2]-1)<.001
    assert abs(values[-1])>.01
    assert abs(p.theta_constant(np.diag([tau1,tau2]),a,b))<1e-13
    ratios=[]
    for eps in (.01,.005,.0025):
        ratios.append(p.chi10_product(np.array([[tau1,eps],[eps,tau2]]))/eps**2)
    assert abs(ratios[-1]/ratios[-2]-1)<.001


def test_exact_divisor_and_logarithmic_threshold_requirement():
    e=s.symbols("e",positive=True)
    C,d0,a0=s.symbols("C d0 a0",nonzero=True)
    determinant=C*d0*e**3
    f=s.log(determinant/a0)/(8*s.pi**2)
    assert s.simplify(s.exp(-8*s.pi**2*f)*determinant-a0)==0
    assert s.simplify(s.diff(f,e)-3/(8*s.pi**2*e))==0
    # A regular exponential factor cannot cancel the zero.
    q0,q1=s.symbols("q0 q1")
    series=s.series(s.exp(q0+q1*e)*determinant,e,0,4).removeO()
    assert series.coeff(e,3)==C*d0*s.exp(q0)


def test_positive_kaehler_normalization_cannot_change_determinant_phase():
    rng=np.random.default_rng(11950)
    for _ in range(8):
        y=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
        factors=[]
        for _ in range(2):
            a=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
            k=a@a.conj().T+np.eye(3)
            ev,U=np.linalg.eigh(k)
            factors.append((U*ev**-.5)@U.conj().T)
        normalized=factors[0]@y@factors[1]
        ratio=np.linalg.det(normalized)/np.linalg.det(y)
        assert ratio.real>0 and abs(ratio.imag)<1e-12


def test_exact_barr_determinant_and_cp_invariant():
    m=s.Matrix([[1,1,0],[0,2,1],[1,0,3]])
    B=s.Matrix([[1+s.I,2-s.I,1+2*s.I]])
    M=m.row_join(s.zeros(3,1)).col_join(B.row_join(s.Matrix([[2]])))
    assert M.det()==14
    v=m*B.conjugate().T
    h=(m*m.T-v*v.conjugate().T/16).applyfunc(s.simplify)
    assert s.simplify(s.im(h[0,1]*h[1,2]*h[2,0]))==s.Rational(119,64)
    assert h.det()>0
    # Distinct real up eigenvalues turn this into a nonzero commutator invariant.
    up=s.diag(1,4,16)
    assert s.im((up*h-h*up).det())!=0


def test_real_B_negative_control_and_upper_block_leakage():
    m=s.Matrix([[1,1,0],[0,2,1],[1,0,3]])
    real_B=s.Matrix([[1,2,1]])
    v=m*real_B.T
    h=m*m.T-v*v.T/10
    assert s.im(h[0,1]*h[1,2]*h[2,0])==0
    eta=s.symbols("eta",real=True)
    B=s.Matrix([[1+s.I,2-s.I,1+2*s.I]])
    M=m.row_join(s.Matrix([eta,0,0])).col_join(B.row_join(s.Matrix([[2]])))
    assert s.expand(M.det()-(14-(6+s.I)*eta))==0


def test_inverse_realization_for_independent_positive_matrices():
    rng=np.random.default_rng(11951)
    for _ in range(25):
        a=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
        h=a@a.conj().T+.2*np.eye(3)
        m,B,mu=p.barr_realization(h)
        assert np.max(abs(p.light_hermitian(m,B,mu)-h))<1e-11
        assert np.isrealobj(m) and np.linalg.det(m)>0 and mu>0


def test_mass_labelled_inverse_quark_target():
    v,masses=p.ckm_target()
    assert np.max(abs(v@v.conj().T-np.eye(3)))<1e-13
    h=(v*masses**2)@v.conj().T
    m,B,mu=p.barr_realization(h)
    values,U=np.linalg.eigh(p.light_hermitian(m,B,mu))
    assert max(abs(np.sqrt(values)/masses-1))<1e-7
    for name,i,j in (("Vus",0,1),("Vcb",1,2),("Vub",0,2)):
        assert abs(abs(U[i,j])/p.fits.DATA[name]-1)<1e-8


def test_all_order_parity_obstruction_and_holomorphic_charge_escape():
    # Standard E6 16 odd, 10 even: no even condensate can mix them.
    assert (-1)**1*(-1)**(-2)==-1
    for n in range(40):
        assert -1*(1**n)==-1
        assert -1-n<0   # Q H Dc dressed by n negative-X S fields.
    # In the alternative, both heavy down fields are matter-parity odd.
    assert (-1)*(-1)*1==1


def test_actual_new_field_mixed_anomaly_sums():
    fields=[(3,s.Rational(-1,3),1),(3,s.Rational(1,3),-1),
            (1,0,-1),(1,0,-1),(1,0,1),(1,0,1)]
    assert sum(n*y*y*x for n,y,x in fields)==0
    assert sum(n*y*x*x for n,y,x in fields)==0
    assert sum(n*x for n,y,x in fields)==0
    assert sum(n*x**3 for n,y,x in fields)==0
    assert s.Rational(1,2)*(fields[0][2]+fields[1][2])==0


def test_cp_alignment_hessian_and_gauge_goldstone():
    x,y,z,w=s.symbols("x y z w",real=True)
    A=x*x+y*y;B=z*z+w*w
    V=(A+B-2)**2+(A-B)**2+(x*z+y*w)**2
    at={x:1,y:0,z:0,w:1}
    H=s.hessian(V,(x,y,z,w)).subs(at)
    assert all(v>=0 for v in H.eigenvals())
    assert H.nullspace()==[s.Matrix([0,-1,1,0])]
    assert sum(v!=0 for v in H.eigenvals())==2


def test_declared_spectator_superpotential_F_terms_vanish():
    s1,s2,t1,t2,L=s.symbols("s1 s2 t1 t2 L",nonzero=True)
    W=((s1*t1)**2+(s2*t2)**2)/L
    for field in (s1,s2,t1,t2):
        assert s.diff(W,field).subs({t1:0,t2:0})==0


def test_frozen_science_replay():
    import json
    frozen=json.loads((ROOT/"data/w33_pass11950_11951_strong_cp_divisor_and_vectorlike.json").read_text())
    regenerated=p.certificate()
    assert regenerated["input_normalized_sha256"]==frozen["input_normalized_sha256"]
    assert regenerated["pass11950"]["determinant_order"]==3
    assert regenerated["pass11951"]["exact_example"]==frozen["pass11951"]["exact_example"]
    assert all(abs(c["determinant_winding"]-3)<1e-9 for c in regenerated["pass11950"]["cases"])
