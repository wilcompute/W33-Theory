"""
Shift-tower primitives for the polynomial W(3,q) family.

This packages the clean q-polynomial part of the substrate so the recent
May 19 shift-tower and commutation audits can be expressed in reusable code
rather than one-off analysis scripts.
"""

from __future__ import annotations


def shift_tower_primitives(q: int) -> dict[str, int]:
    """Return the polynomial primitive packet at a given q."""
    return {
        "v": (q + 1) * (q * q + 1),
        "k": q * (q + 1),
        "lambda": q - 1,
        "mu": q + 1,
        "Phi3": q * q + q + 1,
        "Phi4": q * q + 1,
        "Phi6": q * q - q + 1,
    }


def build_shift_tower(q_values=range(3, 8)) -> dict[int, dict[str, int]]:
    """Return the shift tower over the supplied q-window."""
    return {q: shift_tower_primitives(q) for q in q_values}


def build_shift_tower_reverse_lookup(
    tower: dict[int, dict[str, int]] | None = None,
    q_values=range(3, 8),
) -> dict[int, list[tuple[str, int]]]:
    """Map primitive values in the shift tower back to their (name, q) occurrences."""
    tower = tower or build_shift_tower(q_values=q_values)
    reverse: dict[int, list[tuple[str, int]]] = {}
    for q, primitives in tower.items():
        for name, value in primitives.items():
            reverse.setdefault(value, []).append((name, q))
    return reverse