from __future__ import annotations

from analysis.w33_reye_horizon_octet_factor_lock import (
    reye_horizon_octet_factor_lock_packet,
)


def test_mcxcv_packets() -> None:
    packet = reye_horizon_octet_factor_lock_packet()

    assert packet["packets"] == {
        "cells": 8,
        "horizon_total": 72,
        "reye_points": 12,
        "genus": 6,
        "reye_automorphism": 576,
        "tomotope_automorphism": 96,
    }
    assert packet["derived_invariants"] == {
        "symbols_per_cell": 9,
        "symmetry_units_per_symbol": 8,
        "identity": "576 = 8*72 = 8*12*6, with 72/8=9 and 576/72=8",
    }


def test_mcxcv_all_checks_pass() -> None:
    packet = reye_horizon_octet_factor_lock_packet()

    assert packet["checks"] == {
        "cells_is_8": True,
        "horizon_total_is_72": True,
        "reye_automorphism_is_576": True,
        "reye_points_is_12": True,
        "genus_and_parity_are_6": True,
        "total_equals_points_times_genus": True,
        "reye_symmetry_equals_cells_times_total": True,
        "reye_symmetry_equals_cells_times_points_times_genus": True,
        "tomotope_symmetry_equals_points_times_cells": True,
        "symbols_per_cell_is_9": True,
        "symmetry_units_per_symbol_is_8": True,
        "octet_nonet_duality": True,
    }
    assert packet["n_verified"] == 12
