#!/usr/bin/env python3
"""
BT704 — Explicit Fibonacci braid generators for the local K33 four-block register.

BT701 established a boundary: the K33 [9,4,4] local code has 16 states and is
best modeled as four two-state Fibonacci blocks, not as one or two blocks.
BT704 attaches the standard Fibonacci anyon braid matrices to each block and
verifies the braid relation blockwise.

For three Fibonacci anyons with total charge tau, the two-dimensional fusion
space has generators
    sigma1 = diag(-phi^{-1}, phi)
    sigma2 = F sigma1 F
where
    F = [[phi^{-1}, sqrt(phi^{-1})], [sqrt(phi^{-1}), -phi^{-1}]]
up to the conventional overall phases.  The real projective version verifies
    sigma1 sigma2 sigma1 = sigma2 sigma1 sigma2.

The four-block register has dimension 2^4=16.  Each block acts by Kronecker
extension on one tensor factor.
"""
from __future__ import annotations
import math
import numpy as np


def kron_on_block(op, block: int, blocks: int = 4):
    out = np.array([[1.0]])
    for b in range(blocks):
        out = np.kron(out, op if b == block else np.eye(2))
    return out


def main() -> None:
    phi = (1 + math.sqrt(5)) / 2
    invphi = 1 / phi
    F = np.array([[invphi, math.sqrt(invphi)], [math.sqrt(invphi), -invphi]])
    s1 = np.diag([-invphi, phi])
    s2 = F @ s1 @ F

    assert np.allclose(F @ F, np.eye(2), atol=1e-10)
    assert np.allclose(s1 @ s2 @ s1, s2 @ s1 @ s2, atol=1e-10)

    ops = []
    for b in range(4):
        S1 = kron_on_block(s1, b)
        S2 = kron_on_block(s2, b)
        assert S1.shape == (16, 16)
        assert S2.shape == (16, 16)
        assert np.allclose(S1 @ S2 @ S1, S2 @ S1 @ S2, atol=1e-10)
        ops.append((S1, S2))

    # Operators on distinct blocks commute.
    for i in range(4):
        for j in range(4):
            if i == j:
                continue
            for A in ops[i]:
                for B in ops[j]:
                    assert np.allclose(A @ B, B @ A, atol=1e-10)

    print("BT704 Fibonacci braid generators: PASS")
    print("single_block_dimension=2")
    print("number_of_blocks=4")
    print("register_dimension=16")
    print("braid_relation_verified_per_block=True")
    print("distinct_blocks_commute=True")
    print("boundary=register action only; not yet a generator-respecting map from K33 lift selectors to braid words")


if __name__ == "__main__":
    main()
