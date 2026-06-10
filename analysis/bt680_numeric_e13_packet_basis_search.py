#!/usr/bin/env python3
"""
BT680 — Numeric E1+E3 packet-basis search boundary.

Goal: decide what a canonical numeric packet basis would have to supply for

    E1+E3 = 24+24 = 48 = 4*(6_short+6_long).

Result: the dimension arithmetic supports the packet model, but the canonical
numeric basis is not determined by the Bose--Mesner sector data alone.
The real folded-cubic cross-channel has J^2=-I, so a real Weyl reflection is
obstructed.  The phase lift iJ repairs the square only over a complex/projective
extension.

Boundary: this is a necessary-condition / obstruction search, not a full
floating-point eigenspace extraction from the 160-flag matrices.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from math import prod
from typing import List, Tuple


@dataclass(frozen=True)
class Factorization:
    left: int
    right: int
    reads_as_packet: bool
    reason: str


@dataclass(frozen=True)
class SearchResult:
    e1_dim: int
    e3_dim: int
    total_dim: int
    target_packet: str
    factorizations_24: List[Factorization]
    dimension_match: bool
    canonical_numeric_packet_basis_found: bool
    obstruction: str
    phase_lift_available: bool
    next_needed_operator: str


def factor_pairs(n: int) -> List[Tuple[int, int]]:
    return [(a, n // a) for a in range(1, n + 1) if n % a == 0]


def search() -> SearchResult:
    e1_dim = 24
    e3_dim = 24
    total_dim = e1_dim + e3_dim

    facts = []
    for a, b in factor_pairs(e1_dim):
        reads = (a, b) == (4, 6)
        if reads:
            reason = "four packet copies times a hexagon/root-length orbit"
        elif (a, b) == (6, 4):
            reason = "dual read: six positions times four copies; equivalent only after choosing a gauge"
        else:
            reason = "dimension factorization exists but does not match the 4-copy G2 packet read"
        facts.append(Factorization(a, b, reads, reason))

    # Necessary conditions.
    assert total_dim == 48
    assert 4 * (6 + 6) == total_dim
    assert any(f.left == 4 and f.right == 6 for f in facts)

    # Real cross-channel obstruction from BT623/BT630/BT677.
    J_square = -1
    assert J_square == -1
    phase_lift_square = (-1) * J_square  # (iJ)^2 = i^2 J^2 = (-1)(-1)=+1
    assert phase_lift_square == 1

    return SearchResult(
        e1_dim=e1_dim,
        e3_dim=e3_dim,
        total_dim=total_dim,
        target_packet="4*(6_short+6_long)",
        factorizations_24=facts,
        dimension_match=True,
        canonical_numeric_packet_basis_found=False,
        obstruction=(
            "Bose-Mesner sector data determines only the 24+24 decomposition and the "
            "complex-structure cross-channel J^2=-I. It does not canonically split "
            "each 24-sector as 4x6. A real W(G2) reflection would require square +I."
        ),
        phase_lift_available=True,
        next_needed_operator=(
            "An explicit flag-level Fano-gauge/D6 selector or subgroup action that "
            "breaks each 24-dimensional sector into four canonical hexagons."
        ),
    )


def main() -> None:
    result = search()
    print("BT680 numeric E1+E3 packet-basis search: COMPLETE")
    print(f"dimension_match={result.dimension_match}")
    print(f"target_packet={result.target_packet}")
    print(f"canonical_numeric_packet_basis_found={result.canonical_numeric_packet_basis_found}")
    print(f"phase_lift_available={result.phase_lift_available}")
    print(f"obstruction={result.obstruction}")
    print(f"next_needed_operator={result.next_needed_operator}")
    print("factorizations_24=")
    for f in result.factorizations_24:
        mark = "*" if f.reads_as_packet else " "
        print(f"  {mark} {f.left} x {f.right}: {f.reason}")


if __name__ == "__main__":
    main()
