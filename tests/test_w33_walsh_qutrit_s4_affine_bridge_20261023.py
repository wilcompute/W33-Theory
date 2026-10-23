"""Physical four-rail S4 action on Walsh qutrit and exact cyclic Pauli."""
import itertools,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_walsh_qutrit_s4_affine_bridge_20261023 import four_rail_perm,result
from w33_walsh_qutrit_metaplectic_noise_20261023 import code_basis

def test_all_24_s4_permutations_preserve_three_dimensional_code():
    out=result()
    assert out['physical_rail_permutation_count']==24
    assert out['logical_sign_permutation_count']==24
    V,a=code_basis()
    for sigma in itertools.permutations(range(4)):
        P=four_rail_perm(sigma)
        logical=V.T@P@V
        assert np.linalg.norm(P@V-V@logical)<1e-12
        assert np.linalg.norm(P@a-a)<1e-12
def test_order_three_rail_permutation_is_cyclic_qutrit_x():
    out=result()
    assert out['three_cycle_rail_permutation']==[0,2,3,1]
    L=np.array(out['three_cycle_logical_X3'])
    assert np.array_equal(L,np.array([[0,1,0],[0,0,1],[1,0,0]]))
    assert np.array_equal(L@L@L,np.eye(3,dtype=int))
def test_qutrit_fourier_conjugation_gives_pauli_z_inverse():
    out=result()
    Z=np.array(out['Z3_F3_conjugate_real'])+1j*np.array(out['Z3_F3_conjugate_imag'])
    w=np.exp(2j*np.pi/3)
    assert np.linalg.norm(Z-np.diag([1,w*w,w]))<1e-12
def test_existing_xor_switches_cannot_produce_a_three_cycle():
    from w33_fractal_linebus_switch_matrix_20261023 import permutation_matrix
    G=four_rail_perm([0,2,3,1])
    assert all(np.linalg.norm(G-permutation_matrix(mask))>1 for mask in range(4))
    assert any('cannot execute rail 3-cycle' in s for s in result()['engineering_boundary'])
