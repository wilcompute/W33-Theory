"""Regression suite: five W33/RH frontiers have scoped, falsifiable outputs."""
from analysis.w33_20261021_rh_five_frontiers import (
    hecke,levi,weil_negative_control,signed_levi,infinite_scaffold
)

def test_e8_hecke():
    r=hecke()
    assert r["status"]=="PASS" and r["identities"]==1200

def test_levi_module_construction():
    r=levi()
    assert r["status"]=="PASS" and r["rank_mod_101"]==[96,60]
    assert r["nontrivial_transfer_dimension"]==156

def test_weil_negative_orbit():
    r=weil_negative_control()
    assert r["off_line_kernel_eigenvalues"][0]<0
    assert r["negative_directions_after_tensor_projector"]==[24,15]

def test_levi_one_edge_sign():
    r=signed_levi()
    assert r["exact_trace_defect"]==2592
    assert r["signed_radius"]>r["pure_weight_1_bound"]

def test_infinite_operator_scaffold():
    r=infinite_scaffold()
    assert r["status"]=="PASS"
    assert 0.04<r["mean_first20_relative_error_unperturbed"]<0.06
    assert r["bounded_shift_max"]<=0.050000001
