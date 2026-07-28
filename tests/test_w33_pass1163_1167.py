#!/usr/bin/env python3
"""Corrected regressions for the occupied Passes 1163-1167 surfaces."""
import pathlib, sys
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from analysis.w33_pass1163_sp43_stabilizer_precompute import main as p1163
from analysis.w33_pass1164_1920_module_identification import main as p1164
from analysis.w33_pass1166_ihara_zeta_degree10 import main as p1166
from analysis.w33_pass1167_40pt_carrier_decomposition import main as p1167


def test_projective_geometry_corrected():
    r=p1163(); assert r["acting_group"]=="PSp(4,3) on projective W(3,3) objects"
    assert r["geometry"]=={"points":40,"lines":40,"flags":160}
    assert r["unordered_pair_orbits"]==[240,540]


def test_residual_exact_not_1920_guess():
    r=p1164(); assert r["dimension"]==1952; assert r["commutant_dimension"]==1109


def test_ihara_degree10_corrected():
    r=p1166(); assert r["hashimoto_quadratic_coefficient"]==11
    assert r["closed_nonbacktracking_traces"][2]==960


def test_point_module_rank3():
    r=p1167(); assert r["subdegrees"]==[1,12,27]; assert r["decomposition"]=="1 + 24 + 15"
