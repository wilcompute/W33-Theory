#!/usr/bin/env python3
"""Execution tests for all 5 steps of Passes 1153-1157."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from analysis.w33_pass1154_colored_bridge_checker import check_bridge, main as p1154_main
from analysis.w33_pass1155_separator_registry_wire import SPECIES
from analysis.w33_pass1156_central_channel_encoder import main as p1156_main
from analysis.w33_pass1157_sp43_stabilizer_conjugacy import STABILIZER_ORDER, SP43_ORDER, ORBIT_SIZE

def test_colored_bridge_uncolored_cap():
    assert check_bridge(81, False)['severity'] == 'OK'
    assert check_bridge(82, False)['severity'] == 'UNCOLORED_OVERCLAIM'
    assert check_bridge(243, False)['severity'] == 'FATAL_OVERCLAIM'

def test_colored_bridge_colored_cap():
    assert check_bridge(243, True)['severity'] == 'OK'
    assert check_bridge(244, True)['severity'] == 'OVERCLAIM'

def test_species_separator_collision_free():
    triples = [tuple(s['separator']) for s in SPECIES]
    assert len(set(triples)) == 5

def test_species_twins_separated():
    twins = [s for s in SPECIES if s['tom'] in (78, 81)]
    assert {t['normalizer'] for t in twins} == {96, 48}

def test_central_channel_encoder():
    r = p1156_main()
    assert r['central_channel_count'] == 27
    assert r['equivariant_noncentral_count'] == 51

def test_stabilizer_arithmetic():
    assert SP43_ORDER == ORBIT_SIZE * STABILIZER_ORDER
    assert STABILIZER_ORDER == 60
    assert STABILIZER_ORDER != 120

if __name__ == '__main__':
    import pytest, sys
    sys.exit(pytest.main([__file__, '-v']))
