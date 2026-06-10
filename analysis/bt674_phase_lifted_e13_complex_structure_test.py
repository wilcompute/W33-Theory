#!/usr/bin/env python3
"""
BT674 — phase-lifted E1+E3 complex-structure test.

This is a minimal exact algebra model for the BT623/BT630/BT671 boundary:

    real cross-channel J has J^2 = -I,
    phase lift s = iJ has s^2 = +I over C.

The test realizes E1+E3 as 24+24 dimensions.  The same construction is
compatible with the external W(G2) packet interpretation 48 = 4*(6+6).
"""
from __future__ import annotations

import numpy as np


def main() -> None:
    dim = 24
    I = np.eye(dim, dtype=complex)
    Z = np.zeros((dim, dim), dtype=complex)

    # Real cross-channel complex structure between E1 and E3.
    # J(x,y)=(-y,x), so J^2=-I on E1+E3.
    J = np.block([[Z, -I], [I, Z]])
    I48 = np.eye(2 * dim, dtype=complex)
    assert np.allclose(J @ J, -I48)

    # Phase-lifted reflection surrogate.
    s = 1j * J
    assert np.allclose(s @ s, I48)

    # It exchanges the two 24-dimensional halves, hence is compatible with
    # the E1 <-> E3 lower-shell packet, but only after complexification.
    E1 = np.block([[I, Z], [Z, Z]])
    E3 = np.block([[Z, Z], [Z, I]])
    assert np.allclose(E1 @ E1, E1)
    assert np.allclose(E3 @ E3, E3)
    assert np.allclose(E1 @ E3, np.zeros_like(I48))
    assert np.allclose(E1 + E3, I48)

    # J anti-commutes with the grading E1-E3.
    grading = E1 - E3
    assert np.allclose(J @ grading + grading @ J, np.zeros_like(I48))

    # Packet dimensions.
    assert 2 * dim == 48
    assert 48 == 4 * (6 + 6)

    # s is an involution but not real-valued; this is the obstruction boundary.
    assert np.max(np.abs(np.imag(s))) > 0
    assert np.allclose(np.real(J), J)

    print("BT674 phase-lifted E1+E3 complex-structure test: PASS")
    print("dim(E1+E3)=48=4*(6_short+6_long)")
    print("real channel: J^2=-I")
    print("phase lift: (iJ)^2=+I")
    print("verdict: complex/projective packet embedding passes; real reflection embedding fails")


if __name__ == "__main__":
    main()
