#!/usr/bin/env python3
"""Helpers that make a certificate survive being re-run.  Pass 4395.

Pass 4392 re-ran this session's passes and found six certificates that cannot regenerate.
They fell into exactly two kinds, and this module is one function per kind.

FLOAT-TAIL.  `rho = 4.078733846523831` re-runs as `...846`.  Both are correct to every
digit anybody uses; neither is reproducible, because LAPACK does not promise bit-identical
eigenvalues across builds, and writing fifteen significant digits claims that it does.
`round_floats` truncates to a declared precision so the artifact becomes portable.

LINE-NUMBER.  Four certificates record positions inside living manuscripts -- "the claim on
line 581 of the blueprint".  Those expire on the next edit anywhere above line 581, which
in this repository is most days.  `anchor` records what was matched instead of where, plus
a digest of the file it came from, so a mismatch tells you the source changed rather than
merely that time passed.

    A certificate that records WHERE something is expires.
    One that records WHAT it says does not.

    py -3 scripts/cert_util.py        # runs the selftest
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

DEFAULT_PRECISION = 12


def round_floats(obj, precision: int = DEFAULT_PRECISION):
    """Recursively round every float so the serialisation is reproducible.

    Precision 12 is chosen against the actual numbers here: spectral radii of small
    integer matrices, known far better than 1e-12, whose last three digits are LAPACK
    build noise.  It is a declared precision, not a guess -- record it in the certificate.
    """
    if isinstance(obj, float):
        r = round(obj, precision)
        return 0.0 if r == 0 else r
    if isinstance(obj, dict):
        return {k: round_floats(v, precision) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [round_floats(v, precision) for v in obj]
    return obj


def source_digest(path: str | Path) -> str:
    """sha256 of a file, so a certificate can say which version it describes."""
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:16]


def anchor(path: str | Path, text: str, context: int = 60) -> dict:
    """Record WHAT was matched and in which version of the file -- never the line number."""
    return {"file": str(Path(path).name), "text": " ".join(text.split())[:context],
            "source": source_digest(path)}


def dumps(obj, precision: int = DEFAULT_PRECISION) -> str:
    """The repository's serialisation, with the round-trip rule from CLAUDE.md baked in.

    Hash the ROUND-TRIPPED object, never the live dict (Pass 2482): integer keys sort
    numerically before a JSON round-trip and lexicographically after, so the two differ
    permanently.
    """
    obj = round_floats(obj, precision)
    return json.dumps(json.loads(json.dumps(obj)), indent=2, sort_keys=True) + "\n"


def _selftest() -> int:
    ok = True

    # float-tail: two numbers that differ only in LAPACK noise must serialise identically
    a = {"rho": 4.078733846523831, "loc": 0.612867051661117}
    b = {"rho": 4.078733846523846, "loc": 0.6128670516611174}
    same = dumps(a) == dumps(b)
    print(f"  float tails collapse at precision {DEFAULT_PRECISION}        "
          f"{'PASS' if same else 'FAIL'}")
    ok &= same

    # ...but a REAL difference must survive.  A rounding that hides everything is the
    # vacuous check of CLAUDE.md failure mode 7 wearing a different hat.
    c = {"rho": 4.078733846523831, "loc": 0.612867051661117}
    d = {"rho": 4.078734846523831, "loc": 0.612867051661117}   # differs at 1e-6
    differs = dumps(c) != dumps(d)
    print(f"  a genuine 1e-6 difference still shows      "
          f"{'PASS' if differs else 'FAIL'}")
    ok &= differs

    # nested structures and integer keys
    nested = {"m": {1: 0.1 + 0.2, 10: [1.0000000000001, {"x": 2.5}]}}
    round_trips = dumps(nested) == dumps(json.loads(json.dumps(nested)))
    print(f"  integer keys round-trip stably             "
          f"{'PASS' if round_trips else 'FAIL'}")
    ok &= round_trips

    # anchor records text, not position
    p = Path(__file__)
    an = anchor(p, "  a  matched   sentence  ")
    shaped = (an["text"] == "a matched sentence" and len(an["source"]) == 16
              and "line" not in an)
    print(f"  anchor records text and a digest, no line  "
          f"{'PASS' if shaped else 'FAIL'}")
    ok &= shaped

    print(f"\n  selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(_selftest())
