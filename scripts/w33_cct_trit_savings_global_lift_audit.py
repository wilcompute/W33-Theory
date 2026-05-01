"""Global-selector obstruction and lifted-consistency witness for CCT trit-savings.

This audit attacks the Chapter-6 frontier directly: local least-change ties are
exact, but a single-valued global selector can fail because cycle transport can
carry a tie choice to its complement after one loop (monodromy obstruction).

We package a minimal executable witness:
- base cycle: no one-loop fixed selector exists,
- Z2 lift: two-loop consistency exists (period-2 lifted section).
"""

from __future__ import annotations

import json
from typing import Dict, Tuple

from scripts.w33_cct_trit_savings_variational_audit import (
    cct_trit_savings_variational_summary,
)

Q = 3
MU = 4
K = 12
NEIGHBOR_PACKET = K - MU

TieChoice = int
LiftedChoice = Tuple[int, int]  # (local tie symbol, lift bit)


def cycle_transport_base(choice: TieChoice) -> TieChoice:
    """One turn around A->B->C->A on base ties: identity, identity, then complement."""
    return 1 - choice


def iterate_base_transport(choice: TieChoice, turns: int) -> TieChoice:
    """Iterate the base transport map for a finite number of turns."""
    state = choice
    for _ in range(turns):
        state = cycle_transport_base(state)
    return state


def cycle_transport_lifted(choice: LiftedChoice) -> LiftedChoice:
    """Lifted one-turn transport: complement local tie and flip the lift bit."""
    local, lift_bit = choice
    return (1 - local, 1 - lift_bit)


def cct_trit_savings_global_lift_summary() -> Dict[str, object]:
    variational = cct_trit_savings_variational_summary()
    maximizing_indices = variational["variational_packet"]["argmax_overlap_indices"]

    base_fixed_points = tuple(c for c in (0, 1) if cycle_transport_base(c) == c)
    lifted_two_step_fixed_points = tuple(
        state
        for state in ((0, 0), (0, 1), (1, 0), (1, 1))
        if cycle_transport_lifted(cycle_transport_lifted(state)) == state
    )

    orbit_from_zero = (
        (0, 0),
        cycle_transport_lifted((0, 0)),
        cycle_transport_lifted(cycle_transport_lifted((0, 0))),
    )

    odd_turns = (1, 3, 5)
    odd_turn_fixed_points = {
        turns: tuple(c for c in (0, 1) if iterate_base_transport(c, turns) == c)
        for turns in odd_turns
    }
    one_turn_holonomy_class = 1

    return {
        "source_scope": {
            "book": "Cycle Clock Theory",
            "chapter": 6,
            "focus": "global selector / lift frontier for least-change tie transport",
            "status": (
                "finite obstruction-witness on a minimal cycle; this is a frontier "
                "diagnostic, not a full global Penrose/FIG closure theorem"
            ),
        },
        "local_tie_packet": {
            "neighbor_packet": NEIGHBOR_PACKET,
            "maximizing_candidate_indices": maximizing_indices,
            "binary_tie_symbols": (0, 1),
            "local_law": "each local step chooses one maximizer from the tie set",
            "variational_boundary": variational["w33_alignment_packet"]["boundary"],
        },
        "base_monodromy_packet": {
            "cycle": ("A", "B", "C", "A"),
            "edge_transport": (
                "A->B: identity on tie symbol",
                "B->C: identity on tie symbol",
                "C->A: complement on tie symbol",
            ),
            "one_turn_map": "c -> 1-c",
            "fixed_points": base_fixed_points,
            "obstruction_statement": (
                "no one-turn fixed selector on the base cycle"
            ),
        },
        "holonomy_packet": {
            "coefficient_group": "Z2",
            "one_turn_holonomy_class": one_turn_holonomy_class,
            "interpretation": "non-trivial class: one loop toggles tie branch",
            "odd_turn_fixed_points": odd_turn_fixed_points,
            "minimal_consistent_turns": 2,
            "minimality_statement": (
                "all checked odd turns have no fixed selector; two turns are the first global consistency period"
            ),
        },
        "lift_packet": {
            "lift_group": "Z2",
            "lifted_symbol": "(c,s) with c in {0,1}, s in {0,1}",
            "one_turn_lifted_map": "(c,s) -> (1-c,1-s)",
            "two_turn_map": "identity",
            "two_step_fixed_points": lifted_two_step_fixed_points,
            "example_period_2_orbit": orbit_from_zero,
            "resolution_statement": (
                "base obstruction persists at one turn, but a two-turn lifted section "
                "is globally consistent"
            ),
        },
        "w33_alignment_packet": {
            "count_identity": "K-1 = (K-MU)+Q = 11",
            "neighbor_packet": NEIGHBOR_PACKET,
            "qutrit_owner": Q,
            "boundary": (
                "this certifies a finite monodromy obstruction witness and a lifted "
                "two-step consistency witness; it does not claim full global selector closure"
            ),
        },
        "theorem": {
            "base_cycle_has_no_one_turn_fixed_selector": len(base_fixed_points) == 0,
            "base_cycle_map_is_complement": all(
                cycle_transport_base(c) == 1 - c for c in (0, 1)
            ),
            "holonomy_class_is_nontrivial_z2": one_turn_holonomy_class == 1,
            "checked_odd_turns_have_no_fixed_selector": all(
                len(odd_turn_fixed_points[turns]) == 0 for turns in odd_turns
            ),
            "two_turn_base_transport_is_identity": all(
                iterate_base_transport(c, 2) == c for c in (0, 1)
            ),
            "lifted_two_turn_map_is_identity": all(
                cycle_transport_lifted(cycle_transport_lifted(state)) == state
                for state in ((0, 0), (0, 1), (1, 0), (1, 1))
            ),
            "lifted_example_orbit_has_period_two": orbit_from_zero[0] == orbit_from_zero[2],
            "neighbor_packet_matches_chapter6_count": NEIGHBOR_PACKET == 8,
        },
    }


if __name__ == "__main__":
    print(json.dumps(cct_trit_savings_global_lift_summary(), indent=2))
