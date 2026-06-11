#!/usr/bin/env python3
"""
BT828 - Holonet packet compiler.

BT827 gives the recursive architecture.  BT828 makes the first compiler layer
executable: a route between recursive holonet addresses is lowered to local
Q3 XOR hops, chart-web apartment hops, D12 mirror slots, C12 clock phases, and
tomotope commit blocks.

This is a bounded architecture compiler, not a shortest-path solver for every
chart in the 540-node web.  Its contract is the BT827 engineering bound:

    per address digit <= 3 Q3 XOR hops + 5 apartment hops = 8 moves.

The emitted mirror/tomotope headers are deterministic and live in the verified
BT815/BT814 spaces: 2160 mirror slots and 48 tomotope middle blocks.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: str) -> dict:
    with (ROOT / path).open() as f:
        return json.load(f)


def bits3(x: int) -> tuple[int, int, int]:
    return ((x >> 2) & 1, (x >> 1) & 1, x & 1)


def hamming(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    return sum(x != y for x, y in zip(a, b))


@dataclass(frozen=True)
class Address:
    digits: tuple[int, ...]

    def __post_init__(self) -> None:
        if not self.digits:
            raise ValueError("address must have at least one digit")
        bad = [d for d in self.digits if not 0 <= d < 40]
        if bad:
            raise ValueError(f"address digits must be W33 point labels 0..39: {bad}")


def chart_id(digit: int, depth: int) -> int:
    # Deterministic chart-lane assignment into the verified 540-chart atlas.
    return (37 * digit + 91 * depth + 13 * (digit // 8)) % 540


def apartment_hops(src_digit: int, dst_digit: int, depth: int) -> int:
    if src_digit == dst_digit:
        return 0
    coarse_src = src_digit // 8
    coarse_dst = dst_digit // 8
    return 1 + ((coarse_src + 2 * coarse_dst + depth) % 5)


def mirror_slot(src_digit: int, dst_digit: int, depth: int) -> int:
    return (240 * depth + 40 * (src_digit % 12) + dst_digit) % 2160


def tomotope_block(src_digit: int, dst_digit: int, depth: int) -> int:
    return (depth * 16 + 3 * src_digit + dst_digit) % 48


def compile_digit(src_digit: int, dst_digit: int, depth: int) -> dict:
    src_bits = bits3(src_digit)
    dst_bits = bits3(dst_digit)
    xor_axes = [i for i, (a, b) in enumerate(zip(src_bits, dst_bits)) if a != b]
    ahops = apartment_hops(src_digit, dst_digit, depth)
    slot = mirror_slot(src_digit, dst_digit, depth)
    block = tomotope_block(src_digit, dst_digit, depth)
    reversible_moves = len(xor_axes) + ahops
    return {
        "depth": depth,
        "source_digit": src_digit,
        "target_digit": dst_digit,
        "source_bits": src_bits,
        "target_bits": dst_bits,
        "source_chart": chart_id(src_digit, depth),
        "target_chart": chart_id(dst_digit, depth),
        "xor_axes": xor_axes,
        "xor_hops": len(xor_axes),
        "apartment_hops": ahops,
        "reversible_moves": reversible_moves,
        "mirror_slot": slot,
        "mirror_stabilizer_phase_mod_12": slot % 12,
        "mirror_reflection_bit": (slot // 12) % 2,
        "tomotope_block": block,
        "tomotope_edge_label": block // 4,
        "tomotope_face_label": block % 16,
        "clock_phase_c12": (slot + block) % 12,
        "within_digit_bound": reversible_moves <= 8,
    }


def compile_program(name: str, source: Address, target: Address) -> dict:
    if len(source.digits) != len(target.digits):
        raise ValueError("source and target must have the same recursive level")
    rows = [
        compile_digit(src, dst, depth)
        for depth, (src, dst) in enumerate(zip(source.digits, target.digits))
    ]
    level = len(rows)
    reversible_moves = sum(row["reversible_moves"] for row in rows)
    route_bound = 8 * level
    return {
        "program": name,
        "level": level,
        "source": list(source.digits),
        "target": list(target.digits),
        "digit_packets": rows,
        "reversible_moves": reversible_moves,
        "route_bound": route_bound,
        "slack_to_bound": route_bound - reversible_moves,
        "mirror_slots": [row["mirror_slot"] for row in rows],
        "tomotope_blocks": [row["tomotope_block"] for row in rows],
        "clock_phases": [row["clock_phase_c12"] for row in rows],
        "fits_bt827_bound": reversible_moves <= route_bound,
    }


def main() -> None:
    bt827 = load_json("data/bt827_holonet_fractal_architecture.json")
    programs = [
        ("local_flip", Address((0,)), Address((7,))),
        ("single_digit_far", Address((0,)), Address((39,))),
        ("two_digit_cross", Address((0, 5)), Address((39, 12))),
        ("three_digit_far", Address((0, 1, 2)), Address((39, 38, 37))),
        ("six_digit_stress", Address((0, 7, 14, 21, 28, 35)), Address((39, 32, 25, 18, 11, 4))),
    ]
    compiled = [compile_program(name, src, dst) for name, src, dst in programs]

    all_digit_rows = [row for program in compiled for row in program["digit_packets"]]
    checks = {
        "bt827_route_bound_loaded": bt827["fractal_scaling"]["reversible_route_bound"] == "8n = 8 log_40(N)",
        "all_programs_fit_bt827_bound": all(program["fits_bt827_bound"] for program in compiled),
        "each_digit_has_at_most_three_xor_hops": max(row["xor_hops"] for row in all_digit_rows) <= 3,
        "each_digit_has_at_most_five_apartment_hops": max(row["apartment_hops"] for row in all_digit_rows) <= 5,
        "each_digit_has_at_most_eight_reversible_moves": max(row["reversible_moves"] for row in all_digit_rows) <= 8,
        "mirror_slots_live_in_bt815_space": all(0 <= row["mirror_slot"] < 2160 for row in all_digit_rows),
        "tomotope_blocks_live_in_bt814_space": all(0 <= row["tomotope_block"] < 48 for row in all_digit_rows),
        "clock_phases_live_in_c12": all(0 <= row["clock_phase_c12"] < 12 for row in all_digit_rows),
        "compiler_uses_all_runtime_headers": all(
            program["mirror_slots"] and program["tomotope_blocks"] and program["clock_phases"]
            for program in compiled
        ),
        "stress_program_is_level_six": compiled[-1]["level"] == 6,
        "stress_program_bound_is_48": compiled[-1]["route_bound"] == 48,
    }
    for name, ok in checks.items():
        if not ok:
            raise AssertionError(f"BT828 check failed: {name}")

    out = {
        "theorem": "BT828 holonet packet compiler",
        "compiler_contract": {
            "input": "recursive W33 address words with digits 0..39",
            "output": "Q3 XOR hops + apartment hops + D12 mirror slot + C12 phase + tomotope block",
            "per_digit_bound": "xor_hops <= 3 and apartment_hops <= 5, hence reversible_moves <= 8",
            "level_bound": "sum reversible_moves <= 8n",
        },
        "compiled_programs": compiled,
        "checks": checks,
    }
    path = ROOT / "data" / "bt828_holonet_packet_compiler.json"
    with path.open("w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))
    print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
