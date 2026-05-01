"""Regression tests for Part CXXXVII — Hashimoto Spectral Trichotomy."""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from PART_CXXXVI_DOOB_BRIDGE_GENERATION_SPECTRUM import (  # noqa: E402
    build_w33_adjacency,
    build_hashimoto,
)
from PART_CXXXVII_HASHIMOTO_SPECTRAL_TRICHOTOMY import (  # noqa: E402
    adjacency_spectrum_w33,
    hashimoto_spectrum_via_bass,
    magnitude_distribution,
)


# ---------------------------------------------------------------------------
# Bass-formula closed form
# ---------------------------------------------------------------------------
def test_adjacency_spectrum_closed_form():
    adj = adjacency_spectrum_w33()
    assert len(adj) == 40
    assert adj.count(12.0) == 1
    assert adj.count(2.0) == 24
    assert adj.count(-4.0) == 15
    # Degree = trace of A^2 over n? No — sum of squares of eigenvalues = n*k = 480.
    assert sum(l * l for l in adj) == pytest.approx(40 * 12)


def test_bass_prediction_total_equals_2m():
    adj = adjacency_spectrum_w33()
    spec = hashimoto_spectrum_via_bass(adj, k=12, n=40, m=240)
    assert len(spec) == 480


def test_bass_prediction_trichotomy_multiplicities():
    adj = adjacency_spectrum_w33()
    spec = hashimoto_spectrum_via_bass(adj, k=12, n=40, m=240)
    mag = magnitude_distribution(spec)
    perron = round(11.0, 6)
    ramanu = round(math.sqrt(11), 6)
    triv = round(1.0, 6)
    assert mag[perron] == 1
    assert mag[ramanu] == 78
    assert mag[triv] == 401
    assert mag[perron] + mag[ramanu] + mag[triv] == 480


def test_bass_perron_pair_from_lambda_12():
    # λ=12 produces the Perron μ=11 *and* a μ=1 mate (roots of x²−12x+11).
    adj = [12.0]
    spec = hashimoto_spectrum_via_bass(adj, k=12, n=40, m=240)
    # 2 from λ=12 + 2(m-n)=400 trivial
    assert len(spec) == 2 + 400
    reals = sorted(z.real for z in spec if abs(z.imag) < 1e-12)
    # Should contain exactly 11 and 1 from the Perron pair plus ±1 trivial
    assert reals.count(11.0) == 1
    # μ=1 from Perron pair plus 200 trivial +1 = 201
    assert reals.count(1.0) == 1 + 200
    assert reals.count(-1.0) == 200


def test_bass_ramanujan_layer_from_nontrivial_eigs():
    # λ ∈ {2,−4} both give |μ|=√q=√11 (discriminant negative).
    for lam in (2.0, -4.0):
        disc = lam * lam - 4 * 11
        assert disc < 0, "expected nontrivial λ to have complex Hashimoto roots"
        modsq = (lam / 2) ** 2 + (-disc) / 4
        assert modsq == pytest.approx(11.0)


# ---------------------------------------------------------------------------
# Direct diagonalisation
# ---------------------------------------------------------------------------
@pytest.fixture(scope="module")
def hashimoto_eigs():
    A, edges = build_w33_adjacency()
    B, _ = build_hashimoto(A, edges)
    eigs = np.linalg.eigvals(B.toarray())
    return list(eigs)


def test_direct_eigenvalue_count(hashimoto_eigs):
    assert len(hashimoto_eigs) == 480


def test_direct_trichotomy_matches_bass(hashimoto_eigs):
    mag = magnitude_distribution([complex(e) for e in hashimoto_eigs], decimals=6)
    perron = round(11.0, 6)
    ramanu = round(math.sqrt(11), 6)
    triv = round(1.0, 6)
    assert mag[perron] == 1
    assert mag[ramanu] == 78
    assert mag[triv] == 401


def test_direct_perron_eigenvalue_is_11(hashimoto_eigs):
    largest = max(abs(complex(e)) for e in hashimoto_eigs)
    assert largest == pytest.approx(11.0, abs=1e-8)


def test_direct_subdominant_is_sqrt_11(hashimoto_eigs):
    sqrt11 = math.sqrt(11)
    # Strip the unique Perron μ=11 plus its real mate μ=1
    rest = sorted(
        (abs(complex(e)) for e in hashimoto_eigs),
        reverse=True,
    )
    # The next 78 magnitudes after the singleton Perron should all be √11
    for x in rest[1:79]:
        assert x == pytest.approx(sqrt11, abs=1e-8)


# ---------------------------------------------------------------------------
# Algebraic identities
# ---------------------------------------------------------------------------
def test_identity_total_decomposition():
    assert 1 + 78 + 401 == 480
    assert 480 == 2 * 240  # 2m


def test_identity_ramanujan_count_equals_2_times_nontrivial_adj():
    # f + g = 24 + 15 = 39 nontrivial adjacency eigenvalues
    # 2(f+g) = 78 nontrivial Hashimoto eigenvalues
    assert 78 == 2 * (24 + 15)


def test_identity_trivial_count_equals_2mn_plus_one():
    # 2(m−n) Bass trivial eigenvalues + 1 Perron-mate at μ=1
    assert 401 == 2 * (240 - 40) + 1


def test_identity_perron_quadratic():
    # Roots of x² − 12x + 11 = 0 are 11 and 1
    a, b, c = 1.0, -12.0, 11.0
    disc = b * b - 4 * a * c
    assert disc == 100.0  # 144 − 44
    r1 = (-b + math.sqrt(disc)) / 2
    r2 = (-b - math.sqrt(disc)) / 2
    assert {r1, r2} == {11.0, 1.0}
