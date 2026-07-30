from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name:str):
    path=ROOT/"analysis"/name; spec=importlib.util.spec_from_file_location(name,path); mod=importlib.util.module_from_spec(spec); assert spec and spec.loader; spec.loader.exec_module(mod); return mod
def test_pass1148():
    r=load("w33_pass1148_hecke_geometric_filtration.py").main(); assert r["hecke_dimension"]==26 and r["commutator_subspace_dimension"]==17
def test_pass1149():
    r=load("w33_pass1149_fourier_steinberg_kernel_bridge.py").main(); assert r["dimension"]==243 and r["aligned_bridge"]["fourier_block_ranks"]==[81,81,81]
def test_pass1151():
    r=load("w33_pass1151_degree540_taxonomy_lock.py").main(); assert len(r["canonical_species"])==5 and r["joint_rank_determinant"]==83712
def test_pass1152():
    r=load("w33_pass1152_crossed_c3_commutant.py").main(); assert r["crossed_commutant"]["dimension"]==78 and r["crossed_commutant"]["center_dimension"]==27
