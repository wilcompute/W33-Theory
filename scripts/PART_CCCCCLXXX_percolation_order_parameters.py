#!/usr/bin/env python3
"""Order-parameter utilities for W33 genus/quantum percolation.

Input is a spectrum of C_H(p)=Y_p Y_p^* restricted to K=H1.
The functions are deliberately dependency-free so they can be reused by
larger W33, toroidal, and cellular-automaton simulations.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from typing import Iterable


@dataclass(frozen=True)
class VisibilityLedger:
    rank: int
    trace: float
    trace2: float
    d_eff: float
    split_count: int
    outcome_class: str


def positive_values(eigenvalues: Iterable[float], eps: float = 1e-12) -> list[float]:
    return sorted(float(x) for x in eigenvalues if float(x) > eps)


def rank_positive(eigenvalues: Iterable[float], eps: float = 1e-12) -> int:
    return len(positive_values(eigenvalues, eps))


def split_count(eigenvalues: Iterable[float], eps: float = 1e-9) -> int:
    vals = positive_values(eigenvalues, eps)
    if not vals:
        return 0
    groups = 1
    last = vals[0]
    for x in vals[1:]:
        if abs(x - last) > eps:
            groups += 1
            last = x
    return groups


def traces_and_deff(eigenvalues: Iterable[float]) -> tuple[float, float, float]:
    vals = [float(x) for x in eigenvalues]
    t1 = sum(vals)
    t2 = sum(x * x for x in vals)
    d_eff = 0.0 if t2 == 0 else (t1 * t1) / t2
    return t1, t2, d_eff


def classify_visibility(eigenvalues: Iterable[float], full_dim: int = 81, eps: float = 1e-12) -> str:
    vals = list(float(x) for x in eigenvalues)
    r = rank_positive(vals, eps)
    if r == 0:
        return "zero"
    if r < full_dim:
        return "rank_defective"
    s = split_count(vals)
    if s == 1:
        return "full_isotropic"
    return "full_split"


def visibility_ledger(eigenvalues: Iterable[float], full_dim: int = 81) -> VisibilityLedger:
    vals = list(float(x) for x in eigenvalues)
    t1, t2, d_eff = traces_and_deff(vals)
    return VisibilityLedger(
        rank=rank_positive(vals),
        trace=t1,
        trace2=t2,
        d_eff=d_eff,
        split_count=split_count(vals),
        outcome_class=classify_visibility(vals, full_dim=full_dim),
    )


def main() -> None:
    examples = {
        "zero": [0.0] * 81,
        "full_isotropic": [2.0] * 81,
        "full_split": [3.0] * 40 + [1.0] * 41,
        "rank_defective": [1.0] * 27 + [0.0] * 54,
    }
    payload = {name: asdict(visibility_ledger(vals)) for name, vals in examples.items()}
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
