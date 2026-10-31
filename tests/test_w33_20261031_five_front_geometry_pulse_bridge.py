"""Focused regression for the exact W33 five-front geometry/pulse certificate."""
import math
import json
from pathlib import Path
from analysis import w33_20261031_five_front_geometry_pulse_bridge as B

def test_icosahedral_q9_biadjacency_and_four_cycles():
    q=B.q9_icosa()
    assert q["intersection_graph"]["four_cycles"]==1680
    assert q["intersection_graph"]["square_cycles_per_edge"]==28
    assert q["24x24_biadjacency"]["rank_over_fields"]=={
        "2":18,"3":18,"5":11,"7":18,"11":18}
    assert q["24x24_biadjacency"]["smith_normal_form"]=={"one":11,"five":7,"zero":6}

def test_exact_plus_and_minus_81mode_pulses():
    gates=B.exact_pulse()
    assert set(gates["orientations"])=={"plus","minus"}
    assert gates["orientations"]["plus"]["factor"]==7
    assert gates["orientations"]["minus"]["factor"]==6
    for packet in gates["orientations"].values():
        assert packet["raw_rank"]==packet["quotient_rank_previous_certificate"]==54
        assert packet["exact_81x81_involution_certified"]

def test_finite_tick_entropy_threshold():
    rates=B.clock_ensemble()
    assert math.isclose(rates["prior_thermodynamic_threshold_N_over_M"],
                        math.log(3)/math.log(4),rel_tol=1e-15)
    values=list(rates["finite_N_equal_four_label_critical_ratios"].values())
    assert all(values[i]>values[i+1] for i in range(len(values)-1))

def test_chiral_graph_mincut():
    c=B.chiral_w33()
    assert c["min_edge_cut"]==12
    assert c["minimum_nontrivial_flip_excitation_energy_over_J"]=="27/4"

def test_scalar_rank_three_continuum_firewall():
    c=B.scalar_continuum()
    for q_str,data in c["numerical_families"].items():
        q=int(q_str)
        eigs=data["eigenvalues"]
        mult=data["multiplicities"]
        assert eigs==[q*(q+1),q-1,-q-1]
        assert sum(mult)==data["v"]
        assert sum(x*y for x,y in zip(eigs,mult))==0

def test_frozen_certificate_has_all_five_fronts():
    p=Path(B.OUT)
    assert p.is_file()
    d=json.loads(p.read_text())
    assert d["status"]=="PASS"
    assert len(d["checks"])==5 and all(d["checks"].values())
