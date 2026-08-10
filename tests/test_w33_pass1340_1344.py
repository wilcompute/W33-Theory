from __future__ import annotations
from pathlib import Path
import json
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'data/w33_pass1340_1344_cartan_atlas_selector_padic.json').read_text(encoding="utf-8"))
ATLAS=json.loads((ROOT/'data/w33_pass1341_atlas_standard_20_matrices.json').read_text(encoding="utf-8"))


def test_release_status_and_scope():
    assert DATA['status']=='PASS'
    assert all(DATA['checks'].values())


def test_cartan_matrices_and_projectives():
    expected={
        '2':([[1,0],[0,22]],[2,22]),
        '3':([[5,1,3,0],[1,3,2,0],[3,2,5,0],[0,0,0,1]],[9,6,10,1]),
        '5':([[1,0,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0,0],[0,0,1,0,0,0,0,0,0],[0,0,0,1,0,0,0,0,0],[0,0,0,0,1,0,0,0,0],[0,0,0,0,0,1,0,0,0],[0,0,0,0,0,0,2,1,1],[0,0,0,0,0,0,1,1,0],[0,0,0,0,0,0,1,0,2]],[3,2,1,1,1,1,4,2,3]),
    }
    for p,(C,pdims) in expected.items():
        rec=DATA['pass1340_modular_cartan'][p]
        assert rec['cartan_matrix']==C
        assert rec['projective_indecomposable_dimensions']==pdims
        D=sp.Matrix(rec['decomposition_matrix'])
        assert (D.T*D).tolist()==C
        assert rec['decomposition_rows_unique']


def test_regular_module_dimensions():
    for rec in DATA['pass1340_modular_cartan'].values():
        assert sum(a*b for a,b in zip(rec['projective_indecomposable_dimensions'],rec['modular_simple_dimensions']))==26
        assert sum(rec['block_algebra_dimensions'])==26


def _matrix(raw):
    return sp.Matrix([[sp.Rational(x) for x in row] for row in raw])


def test_atlas_standard_generators():
    C=_matrix(ATLAS['matrices']['c']);D=_matrix(ATLAS['matrices']['d']);I=sp.eye(20)
    assert C**2==I
    assert D**9==I
    assert (C*D)**10==I
    assert ATLAS['class_trace_vector']==[20,4,4,2,5,-1,0,0,0,-2,1,1,1,-1,0,10,2,2,2,1,1,-1,0,0,-1]
    assert ATLAS['matrix_sha256']=='8d0c52cf1f962471be1ab6dc4d98af5bc397fe003cbf9660a819ac0572689deb'


def test_minimal_selector():
    rec=DATA['pass1342_minimal_cycle_idempotent_selector']['minimal_combined_selector']
    assert rec['cycle_length']==4
    assert rec['W_E6_cycle_orbit_size']==120
    assert rec['combined_orbit_size']==360
    assert rec['combined_stabilizer_order']==864
    assert rec['combined_group_order']==rec['combined_orbit_size']*rec['combined_stabilizer_order']


def test_cycle_census_through_six():
    rec=DATA['pass1342_minimal_cycle_idempotent_selector']['cycle_orbits']
    assert [rec[str(n)]['cycle_count'] for n in range(3,7)]==[160,1740,18144,146880]
    assert [rec[str(n)]['dihedral_orbit_count'] for n in range(3,7)]==[1,2,2,11]


def test_padic_lifts_and_filtrations():
    rec=DATA['pass1343_padic_lifting']['records']
    assert [rec[p]['modulus'] for p in ('2','3','5')]==[64,729,15625]
    assert [rec[p]['primitive_idempotent_count'] for p in ('2','3','5')]==[3,4,12]
    assert all(rec[p]['complete_orthogonal_system_verified'] for p in ('2','3','5'))
    assert rec['2']['smith_cumulative_ranks'][:5]!=rec['2']['loewy_quotient_dimensions'][:5]
    assert rec['3']['smith_cumulative_ranks']!=rec['3']['loewy_quotient_dimensions'][:4]
    assert rec['5']['smith_cumulative_ranks']==rec['5']['loewy_quotient_dimensions'][1:]


def test_manuscript_integrator_contract():
    insert=ROOT/DATA['pass1344_manuscript_closure']['insert']
    tool=ROOT/DATA['pass1344_manuscript_closure']['integrator']
    assert insert.exists() and tool.exists()
    text=insert.read_text(encoding="utf-8")
    assert 'Exact modular and selector closure' in text
    assert 'runtime checks' in text
