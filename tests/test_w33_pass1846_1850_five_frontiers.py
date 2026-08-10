from analysis.w33_pass1846_1850_verify_frozen import verify
def test_frozen_packet(): assert verify(False)['status']=='PASS'
def test_exact_weight5_coefficient():
 import json
 from pathlib import Path
 d=json.loads((Path(__file__).resolve().parents[1]/'data'/'w33_pass1847_exact_weight5_decoder_completion.json').read_text(encoding="utf-8"))
 assert d['weight_enumerator']=={'A4':540,'A6':9600,'A8':424170,'A10':17523360}
 assert d['decoder']['global_unique_minimum_weight5']==2993248416
