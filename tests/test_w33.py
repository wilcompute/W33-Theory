import math
import pytest
from w33.substrate import *
from w33.phenomenology import *
from w33.cosmology import *

def test_proton_electron_ratio():
    assert abs(get_proton_electron_ratio() - 1836.0) < 1e-4

def test_w_boson_decay():
    assert abs(get_w_boson_decay_fraction() - 0.0259259) < 1e-5

def test_qed_running():
    assert abs(get_qed_running_residue() - 0.035956) < 1e-5

def test_holography():
    assert get_bekenstein_hawking_factor() == 4
    assert get_conformal_holography_dimension() == 15

def test_moonshine_decomposition():
    # 196883 = (v+Phi6)(v+k+Phi6)(73 - lambda_) 
    # where Phi12(3) = 73
    Phi12 = 73
    dim_M = (v + Phi6) * (v + k + Phi6) * (Phi12 - lambda_)
    assert dim_M == 196883
    
    # 15 Moonshine primes 
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41, 47, 59, 71]
    assert len(primes) == g # 15 negative bulk modes

def test_tensor_to_scalar():
    assert abs(get_tensor_to_scalar_ratio() - (1.0/45)) < 1e-6
