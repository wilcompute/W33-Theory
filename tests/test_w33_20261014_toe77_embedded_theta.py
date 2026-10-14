"""TOE77 regression: restore 69-vertex native exterior to 11-site theta."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe77_embedded_theta_exterior_flux import certificate

def test_full_80_site_embedded_theta_rank_flux_and_zeta_moments():
    c=certificate()
    assert c["status"]=="PASS_TOE77_W33_EMBEDDED_THETA_EXTERIOR_FLUX"
    assert c["W33_Levi_vertices_edges"]==[80,160]
    assert c["native_theta_vertices_edges"]==[11,12]
    assert c["full_incidence_rank_without_phases"]==25
    assert c["full_incidence_rank_max_with_two_phases"]==27
    assert c["full_80_vertex_exact_zero_mode_lower_bound"]==26
    assert c["complement_vertices"]==69
    assert c["external_links"]==148
    assert c["nonzero_winding_octagon_count"]>=81
    assert len(c["trace_H8_independent_spectral_cross_checks"])==9
    assert max(z["absolute_error"] for z in c["trace_H8_independent_spectral_cross_checks"])<5e-6
    assert len(c["outside_hopping_flux_scan"])==4
    assert abs(c["outside_hopping_flux_scan"][0]["corner_and_120_ground_energies"]["120"]+7.232839384725914)<1e-8
    assert all(z["best_multistart"]["energy"]<=min(z["corner_and_120_ground_energies"].values())+1e-7 for z in c["outside_hopping_flux_scan"])
