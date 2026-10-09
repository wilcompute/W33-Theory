"""Exact Pass11769 canonical time-reversal regression."""
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('firewall',ROOT/'analysis/w33_20261008_current_time_reversal_firewall.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_complete_incidence_witness():
    x=module.certificate()
    assert x['status']=='PASS'
    assert x['ordered_point_pairs_checked']==1560
    assert x['incidences']==160
    assert x['exact_symbol_energy_difference']=='H(q,p)-H(q,-p)=1/25'
    assert x['sample']['H_num']-x['sample']['H_time_reversed_num']==16
