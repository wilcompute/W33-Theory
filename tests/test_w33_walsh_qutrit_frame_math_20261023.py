"""Regression for complete Walsh-qutrit logical and scalar optical frame states.

Unknown random XOR routing masks leave no auxiliary leakage but completely
dephase an equal-superposition qutrit after uniform twirling. Tracking
two-bit logical XOR mask restores state in exact ideal model.
"""
import itertools,random,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_fractal_linebus_switch_matrix_20261023 import permutation_matrix
from w33_walsh_qutrit_metaplectic_noise_20261023 import code_basis
def logical(mask):
    V,a=code_basis()
    return V.conj().T@permutation_matrix(mask)@V

def test_sign_group_is_two_bit_xor_and_composes():
    for p,q in itertools.product(range(4),repeat=2):
        assert np.linalg.norm(logical(p)@logical(q)-logical(p^q))<1e-12
        assert np.linalg.norm(logical(p).conj().T@logical(p)-np.eye(3))<1e-12

def test_unknown_uniform_mask_is_complete_qutrit_dephasing():
    psi=np.ones(3,complex)/np.sqrt(3)
    rho=np.outer(psi,psi.conj())
    mixed=sum(logical(m)@rho@logical(m).conj().T for m in range(4))/4
    assert np.linalg.norm(mixed-np.eye(3)/3)<1e-12
    assert abs(np.trace(mixed@mixed)-1/3)<1e-12

def test_tracked_mask_correction_restores_coherence_exactly():
    rng=random.Random(20261023)
    psi=np.array([1,1j,-1],complex)/np.sqrt(3)
    for _ in range(120):
        phase=0;mask_accum=0
        raw=psi.copy()
        for _ in range(rng.randrange(1,40)):
            mask=rng.randrange(4)
            raw=((1j)**mask.bit_count())*logical(mask)@raw
            phase=(phase+mask.bit_count())%4
            mask_accum^=mask
        corrected=((1j)**(-phase))*logical(mask_accum)@raw
        assert np.linalg.norm(corrected-psi)<1e-11

def test_phase_frame_alone_is_not_sufficient_to_restore_qutrit():
    # mask=01 and mask=10 both give i scalar but DISTINCT qutrit signs.
    assert 1 .bit_count()==1
    A=logical(1);B=logical(2)
    assert np.linalg.norm(A-B)>1
    assert np.linalg.norm(A@B-logical(3))<1e-12

def test_backpressure_math_reference_800_cycles():
    rng=random.Random(20023)
    state_phase=0;state_mask=0;out_valid=False
    for _ in range(800):
        cmd_mask=rng.randrange(4)
        valid=bool(rng.getrandbits(1))
        ready=bool(rng.getrandbits(1))
        clear=bool(rng.randrange(47)==0)
        can_accept=not out_valid or ready
        old=(state_phase,state_mask)
        if can_accept:
            out_valid=valid
            if valid:
                state_phase=((0 if clear else state_phase)+cmd_mask.bit_count())%4
                state_mask=(0 if clear else state_mask)^cmd_mask
                assert state_phase in range(4) and state_mask in range(4)
        else:
            assert old==(state_phase,state_mask)
