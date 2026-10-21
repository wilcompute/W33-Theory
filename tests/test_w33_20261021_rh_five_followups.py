"""Five RH research follow-up regressions, all with explicit theorem boundaries."""
import base64
import hashlib
import zlib
import numpy as np
import pytest
from analysis.w33_20261021_rh_five_followups import (
    geometry, levi_intertwiner, completed_weil_resolvent,
    formal_hecke, holonomy, spectral_benchmark,
)

@pytest.fixture(scope="module")
def geo():
    return geometry()

def test_full_rational_levi_embedding_and_symmetry(geo):
    points,lines,A,N,_=geo
    result,artifact=levi_intertwiner(points,lines,A,N)
    assert result["status"]=="PASS"
    assert result["rank_mod101"]==156
    assert result["blocks_quartic"]==24 and result["blocks_quadratic"]==30
    assert result["symplectic_transvection_commutes"]
    raw=zlib.decompress(base64.b64decode(artifact["data"]))
    assert hashlib.sha256(raw).hexdigest()==artifact["sha256_raw"]
    assert np.frombuffer(raw,dtype="<i4").reshape((160,156)).shape==(160,156)
    square=zlib.decompress(base64.b64decode(artifact["coordinate_square_data"]))
    assert hashlib.sha256(square).hexdigest()==artifact["coordinate_square_sha256"]
    assert np.frombuffer(square,dtype="<i4").reshape((156,156)).shape==(156,156)
    assert result["square_coordinate_rank_mod101"]==156

def test_completed_resolvent_and_negative_quartet():
    result=completed_weil_resolvent()
    assert float(result["smallest_completed_kernel_eigenvalue"])>0
    assert float(result["off_line_quartet_smallest_eigenvalue"])<0
    assert abs(float(result["gamma_endpoint_term_first"])-
               float(result["prime_term_first"])-
               float(result["completed_xi_log_derivative_first"]))<1e-11

def test_nonconstant_toy_hecke_is_not_modularity(geo):
    result=formal_hecke(geo[2])
    assert result["status"]=="PASS"
    assert result["three_projector_ranks"]==[1,24,15]
    assert "no modular" in result["scope"]

def test_apartment_holonomies_classify_gauge(geo):
    result=holonomy(geo[2],geo[3],geo[4])
    assert result["GF2_apartment_span_rank"]==81
    assert result["one_edge_syndrome_weight"]==81
    assert sum(result["two_edge_syndrome_distance_census"].values())==12720

def test_compact_diagonal_but_wrong_xi_determinant():
    result=spectral_benchmark()
    assert result["status"]=="PASS"
    assert result["finite_det_relative_errors"]["W33_scalar"]["6"]>0.10
    assert result["finite_model_data"]["W33_scalar"]["mean_first20_relative_error"]>0.04
