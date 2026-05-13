#!/usr/bin/env python3
"""Part DCI: Markov spectral-moment bridge for toroidal/tomotope transport.

Uses the exact rational Markov chain from Part DC and the transport counts from
Part CCCCCXCIX to expose an exact moment identity:

  Tr(P^2) = 37/16,
  nontrivial second moment = Tr(P^2) - 1 = 21/16.

Scaling by 16 recovers the toroidal unoriented transport count 21; doubling
recovers oriented transport count 42; multiplying by stabilizer 4 recovers the
active packet weight 168.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MARKOV_PATH = ROOT / "data" / "tomotope_toroidal_markov_ground_bridge.json"
STEP_PATH = ROOT / "data" / "tomotope_toroidal_step_transport_bridge.json"
OUT_PATH = ROOT / "data" / "tomotope_toroidal_markov_spectral_moment_bridge.json"


def _parse_fraction(text: str) -> Fraction:
    a, b = text.split("/")
    return Fraction(int(a), int(b))


def _mat_mul(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    n = len(a)
    out = [[Fraction(0, 1) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if a[i][k] == 0:
                continue
            aik = a[i][k]
            for j in range(n):
                out[i][j] += aik * b[k][j]
    return out


def _trace(m: list[list[Fraction]]) -> Fraction:
    return sum(m[i][i] for i in range(len(m)))


@dataclass(frozen=True)
class SpectralMomentSummary:
    state_count: int
    trace_p_num: int
    trace_p_den: int
    trace_p2_num: int
    trace_p2_den: int
    nontrivial_second_moment_num: int
    nontrivial_second_moment_den: int
    scaled_unoriented_transport: int
    scaled_oriented_transport: int
    stabilizer_weighted_transport: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    markov = json.loads(MARKOV_PATH.read_text(encoding="utf-8"))
    step = json.loads(STEP_PATH.read_text(encoding="utf-8"))

    p = [[_parse_fraction(x) for x in row] for row in markov["transition_matrix"]]
    n = len(p)
    p2 = _mat_mul(p, p)

    tr_p = _trace(p)
    tr_p2 = _trace(p2)

    # From Part DC the chain has eigenvalues: 1, 0, and six nontrivial modes.
    # Therefore sum(nontrivial modes^2) = Tr(P^2) - 1.
    nontrivial_second_moment = tr_p2 - Fraction(1, 1)

    scaled_unoriented = int(nontrivial_second_moment * 16)
    scaled_oriented = 2 * scaled_unoriented

    slot_stabilizer = int(step["summary"]["slot_stabilizer_size"])
    weighted = scaled_oriented * slot_stabilizer

    unoriented_expected = int(step["summary"]["unoriented_transport_count"])
    oriented_expected = int(step["summary"]["oriented_transport_count"])
    active_expected = int(step["summary"]["active_packet_weight"])

    identities = {
        "trace_p_is_one": tr_p == Fraction(1, 1),
        "trace_p2_is_37_over_16": tr_p2 == Fraction(37, 16),
        "nontrivial_second_moment_is_21_over_16": nontrivial_second_moment == Fraction(21, 16),
        "scaled_unoriented_matches_21": scaled_unoriented == 21,
        "scaled_unoriented_matches_step_count": scaled_unoriented == unoriented_expected,
        "scaled_oriented_matches_42": scaled_oriented == 42,
        "scaled_oriented_matches_step_count": scaled_oriented == oriented_expected,
        "stabilizer_weighted_matches_168": weighted == 168,
        "stabilizer_weighted_matches_active_packet": weighted == active_expected,
    }

    summary = SpectralMomentSummary(
        state_count=n,
        trace_p_num=tr_p.numerator,
        trace_p_den=tr_p.denominator,
        trace_p2_num=tr_p2.numerator,
        trace_p2_den=tr_p2.denominator,
        nontrivial_second_moment_num=nontrivial_second_moment.numerator,
        nontrivial_second_moment_den=nontrivial_second_moment.denominator,
        scaled_unoriented_transport=scaled_unoriented,
        scaled_oriented_transport=scaled_oriented,
        stabilizer_weighted_transport=weighted,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "identities": identities,
        "notes": (
            "Exact spectral-moment bridge: Tr(P^2)-1 = 21/16 is the nontrivial "
            "mode-square packet. Scaling by 16 gives 21 (unoriented transports), "
            "doubling gives 42 (oriented transports), and stabilizer weighting by 4 "
            "gives 168 (active toroidal/tomotope packet weight)."
        ),
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
