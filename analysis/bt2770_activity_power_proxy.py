#!/usr/bin/env python3
"""Technology-independent switching proxy for the complete Holonet controller."""
from __future__ import annotations

import itertools
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def bits(x: int, width: int) -> tuple[int, ...]:
    return tuple((x >> i) & 1 for i in range(width))


def hd(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    return sum(x != y for x, y in zip(a, b))


def add3(a: int, b: int) -> int:
    return (a + b) % 3


def neg3(a: int) -> int:
    return (-a) % 3


def frame_bits(v: tuple[int, int, int, int]) -> tuple[int, ...]:
    return sum((bits(x, 2) for x in v), ())


def data_bits(v: tuple[int, int]) -> tuple[int, ...]:
    return bits(v[0], 2) + bits(v[1], 2)


def build() -> dict:
    toggles = defaultdict(list)
    frames = list(itertools.product(range(3), repeat=4))
    for xp, zp, xf, zf in frames:
        before = frame_bits((xp, zp, xf, zf))
        outs = {
            "Fp": (neg3(zp), xp, xf, zf),
            "Ff": (xp, zp, neg3(zf), xf),
            "Sp": (xp, add3(zp, xp), xf, zf),
            "Sf": (xp, zp, xf, add3(zf, xf)),
            "Zp": (xp, add3(zp, 1), xf, zf),
            "Zf": (xp, zp, xf, add3(zf, 1)),
            "CX_p_to_f": (xp, add3(zp, neg3(zf)), add3(xf, xp), zf),
            "CX_f_to_p": (add3(xp, xf), zp, xf, add3(zf, neg3(zp))),
        }
        for name, out in outs.items():
            toggles[name].append(hd(before, frame_bits(out)))

    for p, f in itertools.product(range(3), repeat=2):
        before = data_bits((p, f))
        toggles["CX_p_to_f_data"].append(hd(before, data_bits((p, add3(f, p)))))
        toggles["CX_f_to_p_data"].append(hd(before, data_bits((add3(p, f), f))))

    for a, b, c, d in itertools.product(range(6), range(2), range(6), range(2)):
        outa = (a + ((-c) if b else c)) % 6
        before = bits(a, 3) + bits(b, 1)
        after = bits(outa, 3) + bits(b ^ d, 1)
        toggles["D12"].append(hd(before, after))

    rom = json.loads((ROOT / "data" / "PART_BT2767_M36_PREPARATION_ROM.json").read_text())
    zero = bits(0, 2) + bits(0, 2) + bits(0, 3) * 4
    for row in rom["rows"]:
        after = bits(row["dark_mode"], 2) + bits(row["grade_code"], 2)
        for p in row["phase6"]:
            after += bits(p, 3)
        toggles["M36_control_load"].append(hd(zero, after))

    rows = {}
    total = 0
    samples = 0
    for name, vals in sorted(toggles.items()):
        rows[name] = {
            "samples": len(vals),
            "mean_output_bit_toggles": sum(vals) / len(vals),
            "max_output_bit_toggles": max(vals),
            "distribution": {str(k): vals.count(k) for k in sorted(set(vals))},
        }
        total += sum(vals)
        samples += len(vals)
    return {
        "schema": "w33.pass2770.switching_activity_proxy.v1",
        "status": "TECHNOLOGY_INDEPENDENT_PROXY_ONLY",
        "rows": rows,
        "aggregate_mean_output_bit_toggles": total / samples,
        "boundary": (
            "Toggle counts are not watts. Physical power requires a placed netlist, "
            "device capacitances, voltage, frequency, and representative activity factors."
        ),
    }


def main() -> None:
    out = build()
    path = ROOT / "data" / "PART_BT2770_SWITCHING_ACTIVITY_PROXY.json"
    path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
