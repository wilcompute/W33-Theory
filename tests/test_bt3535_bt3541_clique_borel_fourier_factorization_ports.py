from __future__ import annotations
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAIN=ROOT/'analysis/bt3535_3541_clique_borel_fourier_factorization_ports.py'
CLIQUE=ROOT/'analysis/bt3535_star_clique_recertify.py'
FROZEN=ROOT/'data/PART_BT3535_BT3541_CLIQUE_BOREL_FOURIER_FACTORIZATION_PORTS_results.json'


def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_exact_packet_matches_frozen_certificate():
    mod=load(MAIN,'bt3535_main')
    generated=mod.build()
    frozen=json.loads(FROZEN.read_text(encoding="utf-8"))
    assert generated==frozen
    assert generated['semantic_sha256']=='34ea459ab6acea3a2b5624ba6523016cfb914ffb54220ed64230f74f78a1fb6b'
    assert len(generated['pass3537_bonkers_four_archetypes']['four_action_archetypes'])==4
    assert generated['pass3538_perkel_fourier_projectors']['ranks']==[1,2,18,36]


def test_factorization_and_polynomial_fronts():
    mod=load(MAIN,'bt3535_main_again')
    fact=mod.factorization_design()
    assert sorted(fact['HS_row_factorization_indices'])==list(range(6))
    assert fact['global_separable_ansatz']['successful_bijections']==0
    assert fact['global_separable_ansatz']['fixed_points_histogram']=={'2':2400}
    ports=mod.polynomial_ports()
    assert ports['graphs_regenerated_exactly']['W33']['parameters']==[40,12]
    assert ports['graphs_regenerated_exactly']['Gewirtz']['parameters']==[56,10]


def test_independent_clique_engine_controls():
    mod=load(CLIQUE,'bt3535_clique')
    assert mod.self_tests()=={'K9':9,'C5':2,'K5_7':2}
