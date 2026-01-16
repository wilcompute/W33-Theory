import warnings
import importlib
import pytest

from scripts import projective_phase_alignment as ppa
from scripts import action_candidate_predictor as acp


def test_parse_counts_empty_and_none():
    assert ppa.parse_counts('') == {}
    assert ppa.parse_counts(None) == {}
    assert acp.parse_counts('') == {}


def test_parse_counts_malformed_json_warns():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        res = ppa.parse_counts("{1: 2}")  # invalid JSON (unquoted key)
        assert res == {}
        assert any('Could not parse counts' in str(item.message) for item in w)


def test_parse_counts_single_quotes_and_doubles():
    s1 = "{'1': 2, '3': 4}"
    s2 = '{"1": 2, "3": 4}'
    assert ppa.parse_counts(s1) == {1: 2, 3: 4}
    assert ppa.parse_counts(s2) == {1: 2, 3: 4}
    assert acp.parse_counts(s1) == {1: 2, 3: 4}


def test_parse_counts_non_integer_skips():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        res = ppa.parse_counts('{"a": "b", "2": 3}')
        assert res == {2: 3}
        assert any('Non-integer' in str(item.message) for item in w)
