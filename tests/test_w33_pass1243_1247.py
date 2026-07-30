#!/usr/bin/env python3
"""Tests for Passes 1243-1247."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from analysis.w33_pass1243_explicit_81sector_intertwiner_build_plan import main as p1243
from analysis.w33_pass1244_p1_projection_recipe_27line_frame import main as p1244
from analysis.w33_pass1245_species20_matrix_unit_gap_manifest import main as p1245
from analysis.w33_pass1246_hecke_orbit_enumeration_execution_plan import main as p1246
from analysis.w33_pass1247_shifted_adjacency_independent_theorem_stub import main as p1247


def test_1243_five_steps():
    assert len(p1243()['build_steps']) == 5


def test_1244_target_dim():
    assert p1244()['target_packet']['dimension'] == 201


def test_1245_manifest_exports():
    assert len(p1245()['gap_manifest']['artifacts_expected']) == 3


def test_1246_carrier_size():
    assert p1246()['carrier_size'] == 432


def test_1247_provisional():
    assert p1247()['theorem_state'] == 'PROVISIONAL'


if __name__ == '__main__':
    import pytest, sys
    sys.exit(pytest.main([__file__, '-v']))
