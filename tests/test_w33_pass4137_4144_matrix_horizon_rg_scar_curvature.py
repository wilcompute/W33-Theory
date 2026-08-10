from __future__ import annotations
import hashlib,importlib.util,json
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
CERT=ROOT/"data/PART_4137_4144_MATRIX_HORIZON_RG_SCAR_CURVATURE.json"
SCRIPT=ROOT/"analysis/w33_pass4137_4144_matrix_horizon_rg_scar_curvature.py"
@pytest.fixture(scope="module")
def frozen(): return json.loads(CERT.read_text(encoding="utf-8"))
@pytest.fixture(scope="module")
def regen():
    s=importlib.util.spec_from_file_location("m",SCRIPT);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m.verify()
def test_hash(frozen):
    raw={k:v for k,v in frozen.items() if k!="semantic_sha256"}
    h=hashlib.sha256(json.dumps(raw,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    assert h=="d16f8ab7ce51f2953cfd4866e7a716e31a271b3337a05b6105b367736bcecb6d"==frozen["semantic_sha256"]
def test_4137(frozen): assert frozen["pass4137"]["singlet_dimension"]==6 and frozen["pass4137"]["commutator_trace"]=="-1/4"
def test_4138(regen):
    x=regen["pass4138"];assert x["paraunitary_residual"]<1e-10 and x["logneg"]>0
    assert len(x["uv_roots"])==2 and x["uv_group_velocities"][0]*x["uv_group_velocities"][1]<0
def test_4139(regen):
    x=regen["pass4139"];assert x["channels"]==4 and x["deterministic_ds"]==4 and x["KL_t1"]<x["KL0"]
def test_4140(regen): assert regen["pass4140"]["endpoint_amplitude"]>1-1e-10 and regen["pass4140"]["full_revival_residual"]<1e-10
def test_4141(frozen):
    x=frozen["pass4141"];assert x["law"]=="R_N=R_1/N" and abs(x["R0"]["100"]-x["R0"]["1"]/100)<1e-14
def test_4142(frozen): assert frozen["pass4142"]["fidelity"]=="7/16" and frozen["pass4142"]["commutator_trace"]=="-1/4"
def test_4143(regen): assert regen["pass4143"]["edge_connectivity"]==4 and regen["pass4143"]["N80_layers"]==74
def test_4144(regen):
    x=regen["pass4144"];assert x["chern_exact"]==[-2,0,2] and max(abs(a-b) for a,b in zip(x["chern_numeric"],[-2,0,2]))<1e-10
