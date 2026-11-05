"""Regress the nonprime F9 null-clock construction separately from prime fields."""
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"analysis"/"w33_20261105_f9_null_clock_extension.py"
s=importlib.util.spec_from_file_location("q9clock",P)
m=importlib.util.module_from_spec(s)
s.loader.exec_module(m)
def test_f9_extension_field_clock():
    r=m.verify()
    assert r["eigenvalues"]=={"-10":288,"-1":80,"8":360,"80":1}
    assert r["fixed_modes"]==81 and r["clock_order"]==9
    assert r["nontrivial_normalized_adjacency_radius"]==0.125
