from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'analysis/w33_pass4261_4268_girth18_cd_hysteresis_clock37_nongaussian_search_defect_thermal.py'
spec=importlib.util.spec_from_file_location('p4261_4268',P);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def test_semantic_hash(): assert m.semantic_hash(m.C)==m.C['semantic_sha256']
def test_4261_cover(): m.check_cover()
def test_4262_holonomy(): m.check_holonomy()
def test_4263_lindblad(): m.check_lindblad()
def test_4264_clock(): m.check_clock()
def test_4265_hawking_search_boundary(): m.check_hawking_meta()
def test_4266_4267_search_and_defect(): m.check_search_defect()
def test_4268_thermal_entanglement(): m.check_thermal()
def test_all_checks_frozen(): assert m.C['all_checks_hold'] and all(m.C['checks'].values())
