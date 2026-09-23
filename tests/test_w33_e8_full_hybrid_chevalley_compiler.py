from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis/w33_e8_full_hybrid_chevalley_compiler.py"
DATA=ROOT/"data/w33_e8_full_hybrid_chevalley_compiler.json"
def load():
    s=importlib.util.spec_from_file_location("hybrid_e8_lie",SCRIPT);assert s and s.loader
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def test_frozen_certificate():
    o=json.loads(DATA.read_text())
    assert o["hybrid_transform"]["rank"]==248
    assert o["jacobi"]["source_basis_triples_checked"]==2511496
    assert o["jacobi"]["source_jacobi_exact"] is True
    assert o["jacobi"]["hybrid_jacobi_exact"] is True
    assert len(o["bracket"]["all_grade_products"])==6
    assert all(o["checks"].values())
def test_exact_transport_replay_without_repeating_full_jacobi_sweep():
    o=load().main(write=False,full_jacobi=False)
    assert o["source"]["dimension"]==248
    assert o["source"]["grading_dimensions"]==[86,81,81]
    assert o["hybrid_transform"]["g1_inverse_verified"] is True
    assert o["hybrid_transform"]["g2_inverse_verified"] is True
    assert o["checks"]["all_bracket_terms_respect_Z3"] is True
