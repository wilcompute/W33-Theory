from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'analysis/w33_pass4214_4221_small_cover_su4_quantum_hysteresis_clock_hawking_pell_vacuum_velocity.py'
s=importlib.util.spec_from_file_location('p4214',P);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
C=json.loads(m.OUT.read_text(encoding="utf-8"));E=m.load_engine();L=m.legacy_view(C)
def test_00_semantic_hash(): assert m.semantic_hash(C)==C['semantic_sha256'] and C['all_checks_hold']
def test_4214_cover(): E.cover_check(L)
def test_4215_su4(): E.su4_check(L)
def test_4216_hysteresis(): E.hyst_check(L)
def test_4217_clock(): E.clock_check(L)
def test_4218_hawking(): E.hawking_check(L)
def test_4219_pell(): E.pell_check(L)
def test_4220_vacuum(): E.vac_check(L)
def test_4221_velocity(): E.velocity_check(L)
