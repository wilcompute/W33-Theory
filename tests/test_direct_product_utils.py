#!/usr/bin/env python3
"""Tests for the direct product helper functions."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from THEORY_PART_CXCIV_DIRECT_PRODUCT_UTILS import direct_product_closure
from THEORY_PART_CXCVI_TOMOTOPE_AUTOMORPHISMS import (
    build_graph,
    compute_automorphisms,
    load_r_generators,
)
from THEORY_PART_CXCVII_AUT_NORMALISER import build_gamma, load_permutations


@lru_cache(maxsize=1)
def load_Gamma_H():
    perms = load_permutations()
    Gamma = build_gamma(perms)
    G = build_graph(load_r_generators())
    autos = compute_automorphisms(G)
    H = [tuple(autos[i][j] for j in range(192)) for i in range(len(autos))]
    return Gamma, H


def test_direct_product_size():
    Gamma, H = load_Gamma_H()
    assert len(Gamma) == 18432
    assert len(H) == 96
    assert len(Gamma) * len(H) == 1769472

    sample_closure = direct_product_closure(tuple(Gamma[:3]), tuple(H[:3]))
    assert len(sample_closure) == 9
    assert len(set(sample_closure)) == len(sample_closure)


def test_contains_Gamma_and_H():
    Gamma, H = load_Gamma_H()
    idp = tuple(range(192))
    assert idp in H
    assert idp in Gamma
