from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'analysis/w33_pass4213_4220_small_cover_su4_quantum_hysteresis_clock_hawking_pell_vacuum_velocity.py'
spec=importlib.util.spec_from_file_location('p4213',P);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
C=json.loads(m.OUT.read_text())
def test_00_semantic_hash(): assert m.semantic_hash(C)==C['semantic_sha256'] and C['all_checks_hold']
def test_4213_cover(): m.cover_check(C)
def test_4214_su4(): m.su4_check(C)
def test_4215_hysteresis(): m.hyst_check(C)
def test_4216_clock(): m.clock_check(C)
def test_4217_hawking(): m.hawking_check(C)
def test_4218_pell(): m.pell_check(C)
def test_4219_vacuum(): m.vac_check(C)
def test_4220_velocity(): m.velocity_check(C)
