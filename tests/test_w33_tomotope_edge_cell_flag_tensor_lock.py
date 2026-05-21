from __future__ import annotations

from analysis.w33_tomotope_edge_cell_flag_tensor_lock import (
    tomotope_edge_cell_flag_tensor_lock_packet,
)


def test_mclxxxvi_packet_values() -> None:
    packet = tomotope_edge_cell_flag_tensor_lock_packet()

    assert packet["tomotope_packet"] == {
        "edges": 12,
        "cells": 8,
        "automorphism": 96,
        "flags": 192,
        "monodromy": 18432,
    }
    assert packet["locks"] == {
        "edge_cell_generator": 96,
        "edge_cell_flag_tensor": 18432,
        "automorphism_times_flags": 18432,
        "identity": "18432 = 12*8*192 = 96*192 with 96=12*8",
    }


def test_mclxxxvi_all_checks_pass() -> None:
    packet = tomotope_edge_cell_flag_tensor_lock_packet()

    assert packet["checks"] == {
        "automorphism_equals_edges_times_cells": True,
        "flags_are_double_automorphism": True,
        "monodromy_equals_edge_cell_flag_tensor": True,
        "monodromy_equals_automorphism_times_flags": True,
        "tensor_and_bilinear_forms_match": True,
        "monodromy_over_flags_is_automorphism": True,
        "monodromy_over_automorphism_is_flags": True,
        "monodromy_over_cells_is_edges_times_flags": True,
        "monodromy_over_edges_is_cells_times_flags": True,
        "numeric_identity": True,
    }
    assert packet["n_verified"] == 10
