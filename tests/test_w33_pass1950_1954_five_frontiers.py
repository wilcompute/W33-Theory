from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(path):
    s=importlib.util.spec_from_file_location('mod',path)
    m=importlib.util.module_from_spec(s)
    assert s.loader
    s.loader.exec_module(m)
    return m
def test_frozen_packet():
    out=load(ROOT/'analysis/w33_pass1950_1954_verify_frozen.py').main()
    assert out['n_verified']==35
def test_exact_boundaries_and_nonvacuity():
    a=json.loads((ROOT/'data/w33_pass1950_1954_five_frontiers.json').read_text(encoding="utf-8"))
    assert a['critical_values']['colourfree_milp_status']=='UNKNOWN'
    x=json.loads((ROOT/'data/w33_pass1952_frame_chart_abi_sound_lex.json').read_text(encoding="utf-8"))
    assert x['checks']['lex_nonvacuous']
    assert x['sound_lex_witness']['cut_assignment_sha256'] != x['sound_lex_witness']['surviving_equivalent_sha256']
    y=json.loads((ROOT/'data/w33_pass1953_arithmetic_group_sl3z.json').read_text(encoding="utf-8"))
    assert y['classification']['ambient']=='SL3(Z)'
