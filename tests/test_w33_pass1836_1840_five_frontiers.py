from pathlib import Path
import importlib.util,json
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('vf',ROOT/'analysis'/'w33_pass1836_1840_verify_frozen.py');vf=importlib.util.module_from_spec(spec);spec.loader.exec_module(vf)
def test_frozen_release():
 r=vf.verify();assert r['status']=='PASS';assert r['aggregate_sha256']=='3df51bf4293867129b62fa65cb6207ff4247e1b36e86da07dd2cf2d51a797063'
def test_evidence_boundaries():
 a=json.loads((ROOT/'data'/'w33_pass1836_1840_five_frontiers.json').read_text(encoding="utf-8"))
 text=' '.join(a['boundaries']).lower();assert 'not a frame-cover resolution' in text;assert 'remains open' in text;assert 'weight-8/10' in text
