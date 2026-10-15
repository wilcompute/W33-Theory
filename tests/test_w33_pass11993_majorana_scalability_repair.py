"""Native gate realization and an exact non-Gaussian block interface."""
import sys
import json
from pathlib import Path
from functools import lru_cache
import numpy as np
import sympy as s
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11993_majorana_scalability_repair as m

@lru_cache(None)
def fresh():return m.payload()


def test_actual_five_native_gates_have_quadratic_majorana_hamiltonians():
    d=fresh();assert d['selected_Fock_basis_indices']==[1,2,4,7]
    assert np.array_equal(d['bilinear_restricted_Gram'],np.eye(15))
    for row in d['native_five_gate_Hamiltonians']:
        assert row['gate_reconstruction_error']<1e-10 and row['Majorana_cover_error']<1e-10


def test_gaussian_dimension_gap_is_symbolic_and_scales_beyond_one_block():
    k=s.symbols('k',integer=True,positive=True);poly=18*k*k-3*k
    assert s.expand(-1-poly.subs(k,k+1)+16+16*poly-27*k*(10*k-3))==0
    d=fresh()['Gaussian_scalability_dimension_controls'];assert d[0]['Gaussian_group_dimension']==15
    assert d[1]['Gaussian_group_dimension']==66 and d[1]['encoded_SU_dimension']==255
    assert all(r['Gaussian_group_dimension']<r['encoded_SU_dimension'] for r in d[1:])


def test_all_quadratic_and_quartic_parity_interfaces_are_checked():
    d=fresh()['two_blocks'];assert d['all_quadratic_generators']==66
    assert d['individual_block_parity_preserving_quadratics']==30
    assert d['cross_block_quadratics_that_leave_code']==36
    d=fresh();assert d['quartic_code_leakage']<1e-12
    assert np.allclose(d['quartic_product_input_squared_Schmidt_values'],[.5,.5,0,0])
    assert d['four_point_Wick_defect']>1-1e-12


def test_fixed_quartic_conjugation_and_pauli_closure_are_exact():
    labels=[x|(z<<4) for x in range(16) for z in range(16) if (x or z) and ((x|z)&12==0 or (x|z)&3==0)]
    Q=5<<4;U=expm(-1j*np.pi*m.pauli(0,5)/4);seed=set(labels)
    for a in labels:
        b=a^Q if m.anticommutes(a,Q) else a;seed.add(b)
        A=m.pauli(a&15,a>>4);B=m.pauli(b&15,b>>4);image=U@A@U.conj().T
        assert min(np.max(abs(image-B)),np.max(abs(image+B)))<1e-12
    assert m.lie_labels(labels)==sorted(labels)
    assert m.lie_labels(seed)==list(range(1,256))


def test_quartic_off_control_does_not_entangle_the_two_blocks():
    local=np.array([1,0,1,0])/np.sqrt(2);initial=np.kron(local,local)
    output=expm(-1j*np.pi*m.pauli(0,5)/4)@initial
    assert np.allclose(np.linalg.svd(initial.reshape(4,4),compute_uv=False)**2,[1,0,0,0])
    assert np.allclose(np.linalg.svd(output.reshape(4,4),compute_uv=False)**2,[.5,.5,0,0])


def test_density_mediator_matching_is_an_actual_operator_identity():
    x,g,M,nA,nB=s.symbols('x g M nA nB',real=True,nonzero=True)
    V=M*M*x*x/2+g*x*(nA+nB);minimum=-g*(nA+nB)/(M*M)
    eliminated=s.expand(V.subs(x,minimum)).subs({nA*nA:nA,nB*nB:nB})
    assert s.expand(eliminated+g*g*(nA+nB)/(2*M*M)+g*g*nA*nB/(M*M))==0
    a=np.diag([0,0,1,1]);b=a.copy();N_A=np.kron(a,np.eye(4));N_B=np.kron(np.eye(4),b)
    Q=(2*N_A-np.eye(16))@(2*N_B-np.eye(16))
    assert np.array_equal(Q,4*N_A@N_B-2*N_A-2*N_B+np.eye(16))


def test_frozen_hamiltonian_coefficients_reconstruct_the_native_gates():
    d=json.loads((ROOT/'data/w33_pass11993_majorana_scalability_repair.json').read_text())
    gamma,_,selected=m.gamma6();source=json.loads((ROOT/'data/w33_pass11987_atlas_spin_gate_alphabet.json').read_text())['gates']
    assert d['exact_Pauli_Lie_closure']==fresh()['exact_Pauli_Lie_closure']==list(range(1,256))
    for row,target in zip(d['native_five_gate_Hamiltonians'],source):
        H=np.zeros((8,8),complex)
        for term in row['bilinear_Hamiltonian']:
            a,b=term['Majoranas'];H+=term['coefficient']*1j*gamma[a]@gamma[b]
        U=expm(-1j*H)[np.ix_(selected,selected)]
        assert np.max(abs(U-(np.array(target['gate_real'])+1j*np.array(target['gate_imag']))))<1e-10
