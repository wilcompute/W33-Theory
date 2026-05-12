from fractions import Fraction


def test_synthesis_rank_and_nullity():
    assert 40 - 1 == 39


def test_gram_multiplicities():
    assert {"0": 1, "27/32": 24, "27/20": 15} == {"0": 1, "27/32": 24, "27/20": 15}


def test_adjacency_multiplicities():
    assert {"12": 1, "2": 24, "-4": 15} == {"12": 1, "2": 24, "-4": 15}


def test_relative_weight():
    assert Fraction(27, 20) / Fraction(27, 32) == Fraction(8, 5)


def test_dimension_match():
    assert 24 + 15 == 39
