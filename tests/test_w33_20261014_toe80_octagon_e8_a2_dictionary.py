"""Exact eight-way W33-native octagon to earlier E8 E6 x A2 matter-sector dictionaries."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe80_octagon_e8_a2_dictionary import certificate

def test_all_eight_E8_E6_A2_matter_sectors_have_native_W33_octagon_bijections():
    x=certificate()
    assert x["status"]=="PASS_TOE80_EIGHT_E8_MATTER_TO_NATIVE_W33_OCTAGON_DICTIONARIES"
    assert x["verified_independent_81_root_sectors"]==8
    assert x["total_E8_matter_root_sector_memberships"]==648
    assert x["E6_roots_recovered_from_nonadjacent_native_octagon_differences"]==72
    assert x["all_729_fraction_Gram_entries_per_sector_match"]
    assert x["natural_Weyl_graph_isomorphism_gauge_choices_one_address_anchor"]==1920
    for item in x["each_coordinate_sector_noncanonical_address_maps"]:
        assert len(item["native_octagon_to_E8_projected_weight_index"])==27
        assert len(set(item["native_octagon_to_E8_projected_weight_index"]))==27
        assert all(len(z)==3 for z in item["three_A2_phases_per_octagon"])
        assert item["all_72_E6_roots_match_as_exact_Fraction_vectors"]
