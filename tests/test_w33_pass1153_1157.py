#!/usr/bin/env python3
from analysis.w33_pass1153_fourier_selection_audit import main as p1153
from analysis.w33_pass1154_degree540_species_separator import main as p1154
from analysis.w33_pass1155_crossed_commutant_center_lock import main as p1155
from analysis.w33_pass1156_432_carrier_typing import main as p1156
from analysis.w33_pass1157_publication_sync_rule import main as p1157

def test_pass1153_uncolored_cap():
    r = p1153()
    assert r["uncolored_target_visible_rank_cap"] == 81
    assert r["color_forgotten_hidden_dimension"] == 162

def test_pass1154_separator_collision_free():
    r = p1154()
    assert r["collision_free"] is True
    assert len(r["species"]) == 5

def test_pass1155_center_lock():
    r = p1155()
    assert r["crossed_center_dimension"] == 27
    assert r["commutator_subspace_dimension"] == 51

def test_pass1156_typed_distinction():
    r = p1156()
    assert r["same_cardinality_not_same_carrier"] is True
    assert r["carriers"]["Sp43_432"]["stabilizer_order"] == 60

def test_pass1157_sync_tags():
    r = p1157()
    assert r["required_tags"] == [
        "acting_group",
        "stabilizer_label_or_order",
        "color_retained_or_forgotten",
    ]
