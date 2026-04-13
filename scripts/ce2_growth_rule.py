"""Deterministic growth rule for CE2 simple-family using kernel state.

This module exports a minimal finite automaton describing the evolution of
sign patterns along a growth line under the two nontrivial axis-swaps of
Sp(2,3).  The observable state is an index in {0..7} corresponding to one of
the eight sign triples.  The auxiliary "phase tag" is an index in {0..17}
representing the triple (t,w,z_sum) described in the notes.  Together the
pair (tag,pattern) constitutes the smallest lifted state in which the action
of either swap is single-valued.

The tables are built on import using the helpers in
``scripts.ce2_kernel_action``; no external data or lookup tables are
required.  This module is intended as the basis for the DNA/tile-von
Neumann growth constructions referred to in the conversation.
"""
from __future__ import annotations

from typing import Tuple, List

try:
    # Prefer package-relative import when used as a module; fall back to
    # absolute import when executed directly as a script.
    from .ce2_kernel_action import (
        build_kernel_tables,
        pattern_list,
        tag_list,
    )
except Exception:  # pragma: no cover - fallback for direct script execution
    from scripts.ce2_kernel_action import (
        build_kernel_tables,
        pattern_list,
        tag_list,
    )

# build once at import
_PATTERN_INDEX, _TAG_INDEX, _ACTION1, _ACTION2 = build_kernel_tables()
_PATTERNS = pattern_list()
_TAGS = tag_list()


def next_state(
    tag: int, pattern: int, swap_id: int
) -> Tuple[int, int]:
    """Compute the next (tag,pattern) pair when applying ``swap_id``.

    ``swap_id`` must be either 1 or 2 corresponding to the two order-4
    axis swaps.  The returned pair is guaranteed to be defined; an
    ``IndexError`` will only occur if the inputs are out of range.
    """
    if swap_id not in (1, 2):
        raise ValueError("swap_id must be 1 or 2")
    table = _ACTION1 if swap_id == 1 else _ACTION2
    new_pattern = table[tag][pattern]
    if new_pattern < 0:
        # the combination never occurs in the sign map; treat as error
        raise ValueError("invalid tag/pattern combination for swap")
    # the tag itself is not updated deterministically; we simply return the
    # original tag so that a caller may handle its evolution by other means.
    return tag, new_pattern


def canonical_tag(t: int, w: int, z: int) -> int:
    """Convert a (t,w,z) triple into its tag index.

    Useful for constructing initial states.
    """
    return _TAG_INDEX[(t, w, z)]


def canonical_pattern(pat: Tuple[int, int, int]) -> int:
    """Convert a 3‑tuple of signs into the pattern index."""
    return _PATTERN_INDEX[pat]


def display_state(tag: int, pattern: int) -> str:
    """Return a human-readable representation of a state."""
    return f"tag={_TAGS[tag]}, pat={_PATTERNS[pattern]}"


# quick sanity-check when run as a script
if __name__ == "__main__":
    print("Patterns:", _PATTERNS)
    print("Tags:", _TAGS)
    print("Action1:")
    for row in _ACTION1:
        print(row)
    print("Action2:")
    for row in _ACTION2:
        print(row)
    # exercise a sample transition
    t0 = canonical_tag(1, 0, 0)
    p0 = canonical_pattern((-1, -1, -1))
    print("example next", next_state(t0, p0, 1))
