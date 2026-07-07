import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "analysis"))

import bt1814_packet_kernel_scheduler_adoption as bt1814  # noqa: E402
import bt1815_hesse_magic_aperture as bt1815  # noqa: E402
import bt1816_page_cache_churn_simulator as bt1816  # noqa: E402


def test_bt1813_round_robin_bound_samples():
    for length in range(1, 64):
        loads = [0, 0, 0]
        for i in range(length):
            loads[i % 3] += 1
        assert max(loads) == math.ceil(length / 3)
        assert max(loads) - min(loads) <= 1


def test_bt1814_adoption_table_counts():
    summary = bt1814.theorem_summary()
    assert summary["directed_edges"] == 480
    assert summary["phase_choices_per_edge"] == 3
    assert summary["compiled_rows"] == 1440
    assert summary["max_phase_reuse_per_edge"] == 4


def test_bt1815_magic_aperture_counts():
    summary = bt1815.theorem_summary()
    assert summary["phase_rows_total"] == 360
    assert summary["apertures_per_phase_row"] == 4
    assert summary["apertures_total_with_center_fibers"] == 1440


def test_bt1816_page_cache_profiles():
    summary = bt1816.theorem_summary()
    assert summary["ordered_moves"] == 1560
    assert summary["churn_points_per_move"] == 9
    assert summary["edge_profile"] == {"0_survivors": 3, "3_survivors": 6}
    assert summary["nonedge_profile"] == {"2_survivors": 9}
