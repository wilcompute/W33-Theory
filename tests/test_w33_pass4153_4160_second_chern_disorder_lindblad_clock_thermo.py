from __future__ import annotations
import importlib.util
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'analysis/w33_pass4153_4160_second_chern_disorder_lindblad_clock_thermo.py'

@pytest.fixture(scope='module')
def packet():
    spec=importlib.util.spec_from_file_location('packet4153',SCRIPT)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    assert mod.verify()
    return mod.CERT

def test_4153_second_chern(packet):
    assert packet['pass4153_second_chern_pump']['second_chern_number']==1
    assert packet['pass4153_second_chern_pump']['projector_rank']==2

def test_4154_disorder(packet):
    x=packet['pass4154_disordered_hawking']
    assert x['patterns']==512 and x['minimum_logarithmic_negativity']>0.09

def test_4155_lindblad(packet):
    x=packet['pass4155_lindblad_scale_rg']
    assert x['selected_spectral_dimension']==4
    assert abs(x['demo']['variance_s']-.0025)<1e-15

def test_4156_clock(packet):
    x=packet['pass4156_compressed_gray_clock']
    assert x['minimum_clock_qubits']==5 and x['adjacent_hamming_distance']==1
    assert x['clock_plus_SWAP_locality']==7

def test_4157_thermo(packet):
    x=packet['pass4157_levi_thermodynamics']
    assert abs(5*__import__('math').tanh(x['beta_c_J_bethe'])-1)<1e-15

def test_4158_zeno(packet):
    x=packet['pass4158_zeno_firewall']
    assert x['demo'][-1]['pair_probability']<4e-5

def test_4159_dimension(packet):
    x=packet['pass4159_dimension_spectroscopy']
    assert x['active_bundle_dimension']==2 and x['full_singlet_dimension']==6

def test_4160_echo(packet):
    x=packet['pass4160_torsion_echo']
    assert x['numeric_residual']<2e-14

def test_certificate(packet):
    assert packet['all_checks_hold']
    assert packet['semantic_sha256']=='0e9080801a2cfcca3b7b39afd807835d7bdc6b1a483cd685763b6dfe63405691'
