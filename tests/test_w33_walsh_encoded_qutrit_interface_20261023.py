"""Four physical spatial XOR modes support a leakage-free 3D Fourier character subspace."""
import sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_walsh_encoded_qutrit_interface_20261023 import certificate
from w33_fractal_linebus_switch_matrix_20261023 import permutation_matrix
def test_all_four_xor_switches_preserve_walsh_encoded_three_modes():
    c=certificate();V=np.array(c['V_real'])
    assert V.shape==(4,3)
    for mask in range(4):
        P=permutation_matrix(mask)
        G=V.T@P@V
        assert np.linalg.norm(P@V-V@G)<1e-12
        assert np.linalg.norm(G.T@G-np.eye(3))<1e-12
def test_qutrit_encoder_orthogonal_to_single_auxiliary_character():
    c=certificate()
    v=np.array(c['V_real']);a=np.array(c['auxiliary_character_real'])
    assert np.linalg.norm(v.T@a)<1e-12
    assert np.linalg.norm(v@v.T+np.outer(a,a)-np.eye(4))<1e-12
def test_embedded_f3_unitary_noncommuting_and_ancilla_preserving():
    c=certificate()
    U=np.array(c['embedded_F3_real'])+1j*np.array(c['embedded_F3_imag'])
    assert np.linalg.norm(U.conj().T@U-np.eye(4))<1e-12
    assert c['F3_noncommutation_with_XOR_logical_phase']>2
    assert c['encoded_F3_unitarity_residual']<1e-12
def test_reproducibility_and_logical_character_signs():
    a=certificate();b=certificate()
    assert a['sha256']==b['sha256']
    assert a['switch_logical_characters'][0]['logical_signs']==[1,1,1]
    assert all(set(k['logical_signs']).issubset({-1,1}) for k in a['switch_logical_characters'])
