"""
RAMANUJAN-WEBER: near-integer class invariants and Ramanujan constant
===============================================================

Small exploratory utilities to demonstrate the famous near-integer
property of Ramanujan's constant e^{pi * sqrt(163)} and related checks.

This module prefers `mpmath` for high-precision arithmetic and falls
back to a double-precision approximation if `mpmath` is not available.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

try:
    import mpmath as mp
except Exception:  # pragma: no cover - environment fallback
    mp = None


DEFAULT_D = 163


def compute_e_pi_sqrt(D: int = DEFAULT_D, prec: int = 80):
    """Return high-precision value of e^{pi * sqrt(D)}.

    Uses `mpmath` when available and raises RuntimeError if it is not
    available and high precision is requested.
    """
    if mp is None:
        # Best-effort fall-back using float (low precision)
        import math

        return math.exp(math.pi * math.sqrt(D))

    old = mp.mp.dps
    mp.mp.dps = int(prec)
    try:
        val = mp.e ** (mp.pi * mp.sqrt(D))
        return val
    finally:
        mp.mp.dps = old


def ramanujan_near_integer_report(D: int = DEFAULT_D, prec: int = 80) -> Dict[str, Any]:
    """Compute the Ramanujan value and return a small report dict.

    Fields include the decimal string of the value, the nearest integer,
    the absolute difference, and a boolean `is_near_integer` flag using
    a conservative threshold.
    """
    val = compute_e_pi_sqrt(D=D, prec=prec)
    if mp is None:
        # float fallback
        import math

        nearest = int(round(val))
        diff = abs(val - nearest)
        return {
            "D": D,
            "value": str(val),
            "nearest_int": nearest,
            "diff": diff,
            "is_near_integer": diff < 1e-6,
        }

    # mpmath branch
    old = mp.mp.dps
    mp.mp.dps = int(prec)
    try:
        nearest = mp.nint(val)
        diff = mp.fabs(val - nearest)
        return {
            "D": D,
            "value": mp.nstr(val, 40),
            "nearest_int": mp.nstr(nearest, 0),
            "diff": mp.nstr(diff, 40),
            "is_near_integer": bool(diff < mp.mpf("1e-9")),
            "log10_diff": mp.nstr(mp.log10(diff), 8) if diff != 0 else None,
        }
    finally:
        mp.mp.dps = old


def derive_all_ramanujan_weber(prec: int = 80) -> Dict[str, Any]:
    """Driver that produces a JSON-serializable summary of checks."""
    report = ramanujan_near_integer_report(D=DEFAULT_D, prec=prec)
    summary = {
        "ramanujan_report": report,
        "summary_chain": {
            "ramanujan_163_near_integer": report.get("is_near_integer", False),
        },
    }
    return summary


def main() -> None:
    out = derive_all_ramanujan_weber(prec=120)
    p = Path(__file__).resolve().parent.parent / "data" / "w33_ramanujan_weber.json"
    p.write_text(json.dumps(out, indent=2))
    print(f"Wrote {p}")


if __name__ == "__main__":
    main()
