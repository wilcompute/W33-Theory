#!/usr/bin/env python3
"""Synthetic Holonet physical-substrate stub: CPU waveform -> EOM/ring -> photon qutrit.

This is not a hardware claim. It is the executable interface model we can demo today:

    Holonet VM route program
        -> ternary electrical control waveform
        -> electro-optic phase modulator + ring-resonator bucket model
        -> one self-entangled photon qutrit pair in time/phase bins
        -> mock detector stream

The point is to make the "classical machine as interface" precise. A normal CPU supplies a
route-coded control waveform. The quantum state lives in a coupling medium. In this stub, that
medium is an idealized qutrit EOM/ring model with a tunable visibility and loss.
"""

from __future__ import annotations

import cmath
import csv
import json
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import holonet_node as hn  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DOCS = ROOT / "docs"
OMEGA = cmath.exp(2j * math.pi / 3)


def qutrit_fourier(state):
    out = []
    for k in range(3):
        amp = sum((OMEGA ** (j * k)) * state[j] for j in range(3)) / math.sqrt(3)
        out.append(amp)
    return out


def normalize_probs(probs):
    s = sum(probs)
    if s <= 0:
        return [1 / len(probs)] * len(probs)
    return [p / s for p in probs]


def route_program(ticks=72):
    """Build a deterministic ternary waveform from W(3,3) route decisions."""

    pts = hn.POINTS
    rows = []
    for t in range(ticks):
        src = pts[(7 * t + 3) % len(pts)]
        dst = pts[(11 * t + 5) % len(pts)]
        b = hn.symplectic(src, dst)
        path = hn.route(src, dst)
        relays = hn.multipath(src, dst) if b else []
        # Control trit: route data mixed with tick phase so all three trits appear in one packet.
        trit = (b + len(path) - 1 + len(relays) + t) % 3
        rows.append(
            {
                "tick": t,
                "src": "".join(map(str, src)),
                "dst": "".join(map(str, dst)),
                "symplectic": int(b),
                "route_hops": len(path) - 1,
                "relays": len(relays),
                "control_trit": int(trit),
            }
        )
    return rows


def apply_eom_ring(control_trit, visibility=0.94, ring_q=18.0):
    """Return detector probabilities for a qutrit self-entangled time/phase carrier.

    Carrier: |Phi_3> = (|00> + |11> + |22>) / sqrt(3). We only track the reduced time-bin
    amplitudes after a route-coded EOM phase and a coarse ring-resonator bucket. The detector
    is a Fourier analyzer. Visibility/loss make it look like a real instrument.
    """

    phase_state = [(OMEGA ** (control_trit * j)) / math.sqrt(3) for j in range(3)]
    # Ring bucket: the addressed bin is closest to resonance; non-addressed bins leak.
    detuning = [abs(j - control_trit) for j in range(3)]
    ring = [1.0 / (1.0 + (2 * d / ring_q) ** 2) for d in detuning]
    after_ring = [phase_state[j] * ring[j] for j in range(3)]
    analyzed = qutrit_fourier(after_ring)
    ideal = [abs(a) ** 2 for a in analyzed]
    ideal = normalize_probs(ideal)
    noisy = normalize_probs([visibility * p + (1 - visibility) / 3 for p in ideal])
    return noisy


def sample(probs, rng):
    r = rng.random()
    acc = 0.0
    for i, p in enumerate(probs):
        acc += p
        if r <= acc:
            return i
    return len(probs) - 1


def run(ticks=72, shots_per_tick=32, seed=33):
    rng = random.Random(seed)
    program = route_program(ticks)
    detector_rows = []
    correct = 0
    total = 0
    per_trit = {0: [0, 0], 1: [0, 0], 2: [0, 0]}

    for row in program:
        probs = apply_eom_ring(row["control_trit"])
        for shot in range(shots_per_tick):
            det = sample(probs, rng)
            # With the DFT convention below, a phase omega^(trit*j) peaks at detector -trit mod 3.
            expected = (-row["control_trit"]) % 3
            ok = det == expected
            correct += int(ok)
            total += 1
            per_trit[expected][0] += int(ok)
            per_trit[expected][1] += 1
            detector_rows.append(
                {
                    "tick": row["tick"],
                    "shot": shot,
                    "control_trit": expected,
                    "detector": det,
                    "accepted": True,
                    "correct": ok,
                    "probabilities": [round(p, 6) for p in probs],
                }
            )

    accuracy = correct / total if total else 0.0
    return {
        "ticks": ticks,
        "shots_per_tick": shots_per_tick,
        "total_shots": total,
        "route_program": program,
        "detector_stream": detector_rows,
        "accuracy": accuracy,
        "per_trit_accuracy": {
            str(k): (v[0] / v[1] if v[1] else None) for k, v in per_trit.items()
        },
        "interface_chain": [
            "Holonet VM route program",
            "ternary electrical waveform",
            "EOM phase phi = 2*pi*trit/3",
            "ring-resonator bucket",
            "self-entangled photon qutrit time/phase carrier",
            "Fourier analyzer detector stream",
        ],
        "boundary": (
            "Synthetic substrate stub only. It proves the interface ABI and detector estimator path, "
            "not a physical photonic run."
        ),
    }


def write_outputs(payload):
    DATA.mkdir(exist_ok=True)
    DOCS.mkdir(exist_ok=True)
    (DATA / "holonet_physical_substrate_stub.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )
    with (DATA / "holonet_physical_substrate_detector_stream.csv").open(
        "w", newline="", encoding="utf-8"
    ) as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "tick",
                "shot",
                "control_trit",
                "detector",
                "accepted",
                "correct",
            ],
        )
        writer.writeheader()
        for row in payload["detector_stream"]:
            writer.writerow({k: row[k] for k in writer.fieldnames})

    svg = build_svg(payload)
    (DOCS / "holonet_physical_substrate_stub.svg").write_text(svg, encoding="utf-8")


def build_svg(payload):
    prog = payload["route_program"][:72]
    width = 900
    height = 330
    cell = 10
    colors = ["#5bd18f", "#5bc7f2", "#f2c65b"]
    rects = []
    for row in prog:
        x = 60 + row["tick"] * cell
        y = 80
        rects.append(
            f'<rect x="{x}" y="{y}" width="{cell-1}" height="80" fill="{colors[row["control_trit"]]}"/>'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="{width}" height="{height}" fill="#0b1017"/>
  <text x="40" y="36" fill="#ecf5ff" font-family="Segoe UI, Arial" font-size="24" font-weight="700">Holonet VM -> EOM/ring -> photon qutrit stub</text>
  <text x="40" y="64" fill="#a9b9c8" font-family="Segoe UI, Arial" font-size="14">72 route-coded ternary control ticks; synthetic detector accuracy {payload['accuracy']:.3f}</text>
  {''.join(rects)}
  <text x="60" y="190" fill="#a9b9c8" font-family="Segoe UI, Arial" font-size="14">control trit waveform</text>
  <circle cx="70" cy="235" r="9" fill="#5bd18f"/><text x="88" y="240" fill="#dcecff" font-family="Segoe UI, Arial" font-size="14">trit 0</text>
  <circle cx="170" cy="235" r="9" fill="#5bc7f2"/><text x="188" y="240" fill="#dcecff" font-family="Segoe UI, Arial" font-size="14">trit 1</text>
  <circle cx="270" cy="235" r="9" fill="#f2c65b"/><text x="288" y="240" fill="#dcecff" font-family="Segoe UI, Arial" font-size="14">trit 2</text>
  <text x="40" y="292" fill="#a9b9c8" font-family="Segoe UI, Arial" font-size="13">Boundary: simulated ABI only; physical speedup requires actual photon/electron coupling medium and detector.</text>
</svg>
"""


def main():
    payload = run()
    write_outputs(payload)
    print("HOLONET PHYSICAL SUBSTRATE STUB")
    print("--------------------------------")
    print("chain: " + " -> ".join(payload["interface_chain"]))
    print(
        f"ticks={payload['ticks']} shots/tick={payload['shots_per_tick']} total={payload['total_shots']}"
    )
    print(f"detector accuracy={payload['accuracy']:.4f}")
    print(f"per-trit accuracy={payload['per_trit_accuracy']}")
    print("boundary: " + payload["boundary"])
    print("wrote data/holonet_physical_substrate_stub.json")
    print("wrote data/holonet_physical_substrate_detector_stream.csv")
    print("wrote docs/holonet_physical_substrate_stub.svg")


if __name__ == "__main__":
    main()
