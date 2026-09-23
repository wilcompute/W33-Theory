from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis/w33_e6_cubic_fourier54_alignment.py"
DATA=ROOT/"data/w33_e6_cubic_fourier54_alignment.json"
def load():
    s=importlib.util.spec_from_file_location("fourier54",SCRIPT);assert s and s.loader
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def test_replay():
    assert load().main(write=False)==json.loads(DATA.read_text())
def test_full_retyped_quotient_is_covered():
    o=json.loads(DATA.read_text())
    q=o["background_results"]["quadratic"]
    assert q["characteristic_zero_jacobian_rank"]==78
    assert q["quotient_projection_rank"]==54
    assert q["S1_image_intersection_dimension"]==24
    assert all(x["combined_rank"]==81 for x in q["split_prime_certificates"])
    assert o["compiler_consequence"]["quadratic_background_covers_all_retyped_quotient_directions"] is True
    assert o["compiler_consequence"]["image_equals_canonical_S2_plus_L_subspace"] is False
    assert all(o["checks"].values())
