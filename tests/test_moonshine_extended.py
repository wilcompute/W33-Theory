"""Extended verification: decompose j(tau) via Leech vector counts and p_24

This test exercises the decomposition identity

    [q^n] j(tau) = 720*delta_{n,0} + sum_k N_{2k}(Lambda) * p_{24}(n-k+1)

for n from -1 up to 10.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "exploration"))

from w33_moonshine_decomposed import derive_all_moonshine_decomposed


def test_moonshine_decomposition_up_to_q10():
    chain = derive_all_moonshine_decomposed(max_n=10)
    # verify inv_delta vs p24
    assert chain["inv_delta_equals_q_inv_p24"]["all_match"] is True

    # verify each decomposition matches actual j coefficient
    for n in range(-1, 11):
        d = chain["all_decompositions"][f"q^{n}"]
        assert d["match"] is True
