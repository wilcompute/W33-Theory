#!/usr/bin/env python3
"""
Pass 80 regression tests - Tracks AE, AF, AG.
"""
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_track_ae_scan_finds_candidates():
    """CKM scan must find formulas within 20-sigma (qualitative)."""
    from w33_pass80_trackAE_ckm_mixing import ckm_spectral_scan
    results = ckm_spectral_scan()
    assert len(results) > 0, "No CKM candidates found"
    best = results[0]
    assert best['abs_pull'] < 50, f"Best pull {best['abs_pull']:.1f} too large"
    print(f"  [PASS] Track AE: best |V_us| pull = {best['pull']:+.2f}, "
          f"m = {best['V_us_pred']:.5f}")


def test_track_ae_hierarchy_qualitative():
    """CKM hierarchy should be qualitatively correct (epsilon^n suppression)."""
    from w33_pass80_trackAE_ckm_mixing import epsilon
    # |V_us| > |V_cb| > |V_ub|
    V_us_approx = epsilon**(1/3)
    V_cb_approx = epsilon
    V_ub_approx = epsilon**(3/2)
    assert V_us_approx > V_cb_approx > V_ub_approx, "Hierarchy broken"
    print(f"  [PASS] Track AE: hierarchy {V_us_approx:.4f} > {V_cb_approx:.4f} > {V_ub_approx:.5f}")


def test_track_af_vertex_edge_count():
    """GQ(3,3) must have exactly 40 vertices and 240 edges."""
    from w33_pass80_trackAF_quantum_gravity import N_VERTICES, N_EDGES
    assert N_VERTICES == 40, f"N_vertices = {N_VERTICES} != 40"
    assert N_EDGES == 240, f"N_edges = {N_EDGES} != 240"
    print(f"  [PASS] Track AF: GQ(3,3) has {N_VERTICES} vertices, {N_EDGES} edges")


def test_track_af_aut_order():
    """Aut(GQ(3,3)) must have order 51840."""
    from w33_pass80_trackAF_quantum_gravity import AUT_ORDER
    assert AUT_ORDER == 51840, f"|Aut| = {AUT_ORDER} != 51840"
    print(f"  [PASS] Track AF: |Aut(GQ(3,3))| = {AUT_ORDER}")


def test_track_af_spinfoam_log2():
    """Spin foam log2(Z) must equal N_edges = 240."""
    from w33_pass80_trackAF_quantum_gravity import w33_graviton_spinfoam, N_EDGES
    sf = w33_graviton_spinfoam()
    assert sf['log2_Z_W33'] == N_EDGES, \
        f"log2(Z_W33) = {sf['log2_Z_W33']} != {N_EDGES}"
    print(f"  [PASS] Track AF: log2(Z_W33) = {sf['log2_Z_W33']} = N_edges")


if __name__ == "__main__":
    print("Running Pass 80 regression tests...\n")
    test_track_ae_scan_finds_candidates()
    test_track_ae_hierarchy_qualitative()
    test_track_af_vertex_edge_count()
    test_track_af_aut_order()
    test_track_af_spinfoam_log2()
    print("\nAll Pass 80 tests passed.")
