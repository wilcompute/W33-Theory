"""Adversarial immutable S8 high-z hybrid decomposition checks."""
from __future__ import annotations
import importlib.util,os
from pathlib import Path
import pytest
SOURCE=Path(__file__).resolve().parents[1]
ROOT=Path(os.environ.get("W33_REPO_ROOT",str(SOURCE)))
p=importlib.util.spec_from_file_location("s8_shapley",SOURCE/"analysis/w33_20261108_s8_hybrid_shapley_audit.py")
M=importlib.util.module_from_spec(p);p.loader.exec_module(M)
@pytest.fixture(scope="module")
def cert():return M.produce(ROOT)

@pytest.mark.parametrize("survey",["des","kids"])
def test_fixed_Hybrid_cells_and_unchanged_frozen_ledger(cert,survey):
    a=cert["surveys"][survey]
    assert set(a)=={"all","low","high","mixed"}
    assert all("order_independent_shapley_power" in x for x in a.values())
    assert cert["frozen_prereg"].endswith("prereg_highz.json")

@pytest.mark.parametrize("survey",["des","kids"])
@pytest.mark.parametrize("block",["all","low","high","mixed"])
def test_exact_nonadditive_decomposition(cert,survey,block):
    x=cert["surveys"][survey][block]
    assert x["one_factor_power_at_fading_baseline"]+x["one_factor_geometry_at_fading_baseline"]+x["nonadditive_interaction"]==pytest.approx(x["CPL_minus_fading_total"],abs=1e-11)
    assert x["order_independent_shapley_power"]+x["order_independent_shapley_geometry"]==pytest.approx(x["CPL_minus_fading_total"],abs=1e-11)

def test_DES_interaction_is_sizeable_negative(cert):
    x=cert["surveys"]["des"]["all"]
    assert x["CPL_minus_fading_total"]==pytest.approx(2.8844828876623865,abs=1e-11)
    assert x["nonadditive_interaction"]==pytest.approx(-1.2482386764653484,abs=1e-11)
    assert x["order_independent_shapley_power"]==pytest.approx(1.5771974332296281,abs=1e-11)
    assert x["order_independent_shapley_geometry"]==pytest.approx(1.3072854544327583,abs=1e-11)

def test_KiDS_interaction_is_sizeable_negative(cert):
    x=cert["surveys"]["kids"]["all"]
    assert x["CPL_minus_fading_total"]==pytest.approx(4.503428628031344,abs=1e-11)
    assert x["nonadditive_interaction"]==pytest.approx(-0.7308211483503726,abs=1e-11)
    assert x["order_independent_shapley_power"]==pytest.approx(2.829947695596914,abs=1e-11)
    assert x["order_independent_shapley_geometry"]==pytest.approx(1.6734809324344297,abs=1e-11)

def test_provenance_and_scientific_limits(cert):
    assert "NOT generally" in cert["additive_identification_warning"]
    assert "No new raw" in cert["evidence_limit"]
    assert "not" in cert["frozen_claim"].lower()
