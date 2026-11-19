"""Independent controls for the spin-YM and auxiliary-Cfield packet."""
import importlib.util
from pathlib import Path
import sys
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
spec=importlib.util.spec_from_file_location('spin_packet',ROOT/'analysis/toe_20261119_E8_spin_connection_YM_spectral_flow.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)


def test_mixed_spectator_curvature_not_only_radial_ansatz():
    # Two rational active spectator coordinates, including cross brackets.
    p=[s.Rational(2,7),s.Rational(-3,5)]
    def T(a,b):return s.Matrix(m.matrix_generator(a,b))
    u=sum(x*x for x in p)
    for a in range(5):
        for b in range(a+1,5):
            Aa=sum((x*T(a,5+i) for i,x in enumerate(p)),s.zeros(16))
            Ab=sum((x*T(b,5+i) for i,x in enumerate(p)),s.zeros(16))
            F=T(a,b)+Aa*Ab-Ab*Aa
            assert F==(1-u)*T(a,b)
            assert -s.trace(F*F)/2==(1-u)**2


def test_second_variation_matches_Jacobi_with_norm():
    # Unit R and quotient volume, gYM=1. Norm of each a is5;
    # YM0=5. Second derivative is -20, so J eigenvalue is -4.
    v=s.symbols('v',real=True)
    kinetic_norm=sum(-int(np.trace(m.matrix_generator(a,5)@m.matrix_generator(a,5)))//2 for a in range(5))
    assert kinetic_norm==5
    assert s.diff(5*(1-v*v)**2,v,2).subs(v,0)==-4*kinetic_norm


def test_spinor_tensor_spectrum_by_dense_linear_algebra():
    gam=m.clifford_data();eye=s.eye(4)
    lap=s.zeros(16)
    for a in range(5):
        for b in range(a+1,5):
            T=gam[a]*gam[b]/2
            generator=s.kronecker_product(T,eye)-s.kronecker_product(eye,T.T)
            lap-=generator*generator
    # End(spinor4)=scalar+vector5+adjoint10 under Spin5.
    assert lap.eigenvals()=={s.Integer(0):1,s.Integer(4):5,s.Integer(6):10}
    psi=eye.reshape(16,1)
    for sign in [-1,1]:
        perturb=sum((s.kronecker_product(s.I*g,-sign*s.I*g.T/2) for g in gam),s.zeros(16))
        assert perturb*psi==sign*s.Rational(5,2)*psi
        assert perturb==perturb.conjugate().T


def test_flat_H27_character_using_numerical_matrices():
    z=np.exp(2j*np.pi/3)
    X=np.roll(np.eye(3),1,axis=0);Z=np.diag([1,z,z*z])
    traces=[]
    for a in range(3):
        for b in range(3):
            for c in range(3):
                g=z**c*np.linalg.matrix_power(X,b)@np.linalg.matrix_power(Z,a)
                assert abs(np.linalg.det(g)-1)<1e-13
                traces.append(np.trace(g))
    assert abs(sum(traces)/27)<1e-13
    assert abs(sum(abs(t)**2-1 for t in traces)/27)<1e-13
    assert abs(sum(78+abs(t)**2-1+27*(t+t.conjugate()) for t in traces)/27-78)<1e-12


def test_pontryagin_density_in_independent_four_plane():
    # Coefficient e0123 includes the three pairings, in both orders.
    T=lambda a,b:m.matrix_generator(a,b)
    coeff=2*np.trace(T(0,1)@T(2,3)-T(0,2)@T(1,3)+T(0,3)@T(1,2))
    assert coeff==0
    assert np.trace(T(0,1)@T(0,1))==-2  # nonzero energy is compatible with zero Pontryagin form
    eq=m.Cfield_equivalence()
    assert eq['same_shifted_Cfield_for_all_v']
    assert eq['flat_same_characteristic_difference_group']=='0'


def test_exact_kernel_census_and_embedding():
    census=m.sphere_kernel_census()
    assert census['cover_D5_complex_kernel_dimension']==32
    assert sorted(census['Y7_D7_complex_kernel_by_base_spin_structure'].values())==[0,0,0,64]
    assert m.orthogonal_branching()['basic_embedding_index']==1
