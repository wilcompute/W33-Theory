"""Regression for W33 40x40 incidence nuclear norm and flux crossover."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe77_nuclear_norm_transition import certificate
def test_native_80_vertex_nuclear_norm_embedding_and_120_to_pi_crossing():
    c=certificate()
    assert c["status"]=="PASS_TOE77_EMBEDDED_W33_RAMANUJAN_TO_FLUX_NUCLEAR_NORM"
    assert c["W33_incidence_40_by_40_rank"]==25
    assert c["any_two_entry_flux_at_least_26_exact_one_body_zeros"]
    assert len(c["outside_amplitude_symmetry_line_scan"])==14
    assert all(x["zero_singular_values_tolerance_1e-9"]>=13 for x in c["full_t1_singular_controls"].values())
    assert .5<c["fixed_120_vs_pi_pi_energy_crossing_t_numeric"]<1
    assert c["outside_amplitude_symmetry_line_scan"][0]["fixed_phase_E120_minus_Epi_pi"]<0
    assert c["outside_amplitude_symmetry_line_scan"][-1]["fixed_phase_E120_minus_Epi_pi"]>0
    assert c["unphased_W33_exact_half_filled_energy_numeric"]<0
