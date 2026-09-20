"""Regression checks for actual surfaces, complete certificates and rejected surgery."""
import json
from pathlib import Path
import sys
import numpy as np
import pytest
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_genus_six_execution import audit,validate_surface,HandleVM

@pytest.fixture(scope='module')
def result():return json.loads(json.dumps(audit()))

def test_exact_surface_and_instruction_certificates(result):
    stored=json.loads((ROOT/'analysis/w33_genus_six_execution.json').read_text())
    for key in ('surface','handle_vm','modular'):assert result[key]==stored[key]
    for key in ('tau_real','tau_imag','lattice_complex_structure'):
        np.testing.assert_allclose(result['periods'][key],stored['periods'][key],rtol=1e-13,atol=1e-13)
    np.testing.assert_allclose(result['oscillator']['rows'],stored['oscillator']['rows'],rtol=1e-12,atol=1e-12)

def test_boundary_equivalence_and_coordinate_basis_change(result):
    a=result['surface'];H=s.Matrix(a['homology_projection']);d2=s.Matrix(a['d2'])
    C=s.Matrix(a['lattice_to_cycles']);d1=s.Matrix(a['d1'])
    # Adding an arbitrary boundary leaves every homology coordinate unchanged.
    boundary=d2*s.Matrix([i%5-2 for i in range(44)])
    cycle=C*s.Matrix(range(12))
    assert H*(cycle+boundary)==H*cycle and d1*(cycle+boundary)==s.zeros(12,1)
    E=s.Matrix(json.loads((ROOT/'analysis/w33_k12_genus_polarization.json').read_text())['eisenstein_alternating_form'])
    U=s.eye(12);U[0,1]=3;U[4,7]=-2
    assert U.det()==1
    K=-s.Matrix(a['cup_matrix']).inv()
    assert (H*C*U).T*K*(H*C*U)==U.T*E*U

def test_surface_corruption_and_empty_free_are_rejected(result):
    faces=result['surface']['oriented_faces']
    with pytest.raises(ValueError):validate_surface(faces[:-1])
    with pytest.raises(ValueError):validate_surface(faces+[faces[0]])
    with pytest.raises(ValueError):HandleVM(faces).free()
