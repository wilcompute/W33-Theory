import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def J():return json.loads((R/'data/PART_W33_PASS5082_5089_RESULTS.json').read_text())
def test_sharp_q3_and_q4_kernel():
    x=J();assert x['5083']['active_chart_minimum']==108;assert x['5084']['generator_dependency_code']==[425,169,5]
def test_decoder_and_intrinsic_charts():
    x=J();assert x['5086']['double_failures']==0;assert x['5088']['exact_match'] is True
def test_quadratic_and_integral_lifts():
    x=J();assert x['5087']['polynomial']=='x^2-2x-16';assert x['5089']['torsion_free'] is True
