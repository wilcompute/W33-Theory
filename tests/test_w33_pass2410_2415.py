import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_frozen_packet():subprocess.run([sys.executable,str(R/'analysis/w33_pass2410_2415_verify_frozen.py')],check=True)
def test_boundaries():
 a=json.loads((R/'data/w33_pass2412_proof_producing_nine_colour_search.json').read_text(encoding="utf-8"));b=json.loads((R/'data/w33_pass2411_global_u6_collision_ledger.json').read_text(encoding="utf-8"));assert a['literal_all_different_search']['status']=='UNKNOWN';assert 'singleton' in b['boundary']
