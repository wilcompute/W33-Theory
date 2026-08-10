from pathlib import Path
import importlib.util
ROOT=Path(__file__).resolve().parents[1]
def load():
 p=ROOT/'analysis/w33_pass1856_1860_verify_frozen.py';s=importlib.util.spec_from_file_location('v',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def test_frozen_packet():assert load().verify()['status']=='PASS'
def test_boundary_flags():
 import json
 d=json.loads((ROOT/'data/w33_pass1856_1860_five_frontiers.json').read_text(encoding="utf-8"));assert d['status']=='PASS_WITH_PROOF_BOUNDARIES';assert len(d['boundaries'])==3
