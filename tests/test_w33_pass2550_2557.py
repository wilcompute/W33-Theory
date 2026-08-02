from pathlib import Path
import importlib.util
ROOT=Path(__file__).resolve().parents[1]
def test_frozen_packet():
 p=ROOT/'analysis/w33_pass2550_2557_verify_frozen.py'
 spec=importlib.util.spec_from_file_location('v',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 assert m.main()>=50
def test_manuscript_insert_exists():
 assert (ROOT/'analysis/BT2557_seven_frontiers_insert.tex').exists()
def test_sources_present():
 assert len(list((ROOT/'analysis').glob('w33_pass255*.py')))+len(list((ROOT/'analysis').glob('w33_pass255*.cpp')))>=12
