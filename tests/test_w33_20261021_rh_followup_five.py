"""Five scoped RH followups: reject unproven classical-RH upgrades."""
from analysis.w33_20261021_rh_followup_five import conjugator, hecke, holonomy, weil, spectrum

def test_156d_rational_intertwiner():
    d=conjugator()
    assert d["rank_mod_101"]==156
    assert d["block_counts"]=={"x4+9":24,"x2+3":30}

def test_formal_hecke_nonuniqueness():
    d=hecke()
    assert len(d["prime_witnesses"])==5
    assert all(r["scalar_trace"]!=r["nonconstant_trace"] for r in d["prime_witnesses"])

def test_binary_apartment_separation():
    d=holonomy()
    assert d["GF2_rank"]==d["cycle_space_dim"]==81
    assert d["octagons"]==1620 and d["cycles_per_edge"]==81

def test_completed_arithmetic_weil_numerics():
    d=weil()
    assert d["minimum_eigenvalue"]>0.2
    assert d["max_zero_side_discrepancy_first60"]<2e-9

def test_w33_infinite_spectral_nonidentifiability():
    d=spectrum()
    assert len(d["models"])==3
    assert abs(d["models"][1]["inverse_moments_2_4_6"][0]-
               d["models"][2]["inverse_moments_2_4_6"][0])>1e-7
