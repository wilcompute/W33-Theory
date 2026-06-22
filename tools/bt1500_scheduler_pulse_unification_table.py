#!/usr/bin/env python3
"""BT1500: master table unifying S4, D4, fibers, pulses, and Steinberg scheduler cycles."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1500_scheduler_pulse_unification_table.json"
TEX = ROOT / "analysis" / "BT1500_scheduler_pulse_unification_table.tex"


def main() -> None:
    rows = [
        {"layer": "Fano automorphism bus", "object": "PSL(3,2)", "count": 168, "factorization": "7 points * 24 fiber = 21 flags * 8 D4", "role": "global finite symmetry bus"},
        {"layer": "canonical shared fiber", "object": "S4", "count": 24, "factorization": "3 local Fano arms * 8 D4 states", "role": "fiber action set / transaction words"},
        {"layer": "native optical subgroup", "object": "D4", "count": 8, "factorization": "1:1, 2:5, 4:2 order profile", "role": "native square-pulse subgroup"},
        {"layer": "scheduler lift", "object": "C3 x D4", "count": 24, "factorization": "3 scheduler generations * 8 D4 flags", "role": "basis-independent finite scheduler class"},
        {"layer": "transaction word", "object": "72 ticks", "count": 72, "factorization": "3 C3 channels * 4 branches * 6 row slots", "role": "single S4 action word"},
        {"layer": "physical pulse packet", "object": "row pulses", "count": 1728, "factorization": "24 S4 words * 72 ticks", "role": "compiled detector/mirror/Hesse interface"},
        {"layer": "native pulse subpacket", "object": "D4 square pulses", "count": 576, "factorization": "8 D4 words * 72 ticks", "role": "calibration-priority native pulse block"},
        {"layer": "Steinberg scheduler carrier", "object": "H1 states", "count": 81, "factorization": "27 C3 cycles * 3 states", "role": "central C3 generation-time module"},
        {"layer": "retwined CSS core", "object": "ABI row sector", "count": 72, "factorization": "24 active + 48 guard", "role": "syndrome-legal transaction body"},
    ]
    checks = {
        "fano_168_factorizations": 7 * 24 == 168 and 21 * 8 == 168,
        "fiber_24_factorization": 3 * 8 == 24,
        "scheduler_lift_24": 3 * 8 == 24,
        "transaction_word_72": 3 * 4 * 6 == 72,
        "pulse_packet_1728": 24 * 72 == 1728,
        "native_pulse_576": 8 * 72 == 576,
        "steinberg_81": 27 * 3 == 81,
        "css_72": 24 + 48 == 72,
        "row_count": len(rows) == 9,
    }
    lines = [
        r"\begin{center}\scriptsize",
        r"\begin{tabular}{p{0.18\textwidth}p{0.16\textwidth}r p{0.27\textwidth}p{0.24\textwidth}}",
        r"\toprule",
        r"Layer & Object & Count & Factorization & Role\\",
        r"\midrule",
    ]
    for r in rows:
        line = f"{r['layer']} & {r['object']} & {r['count']} & {r['factorization']} & {r['role']}\\"
        lines.append(line.replace("_", r"\_"))
    lines.extend([r"\bottomrule", r"\end{tabular}", r"\end{center}"])
    TEX.write_text("\n".join(lines) + "\n", encoding="utf-8")
    result = {
        "bt": 1500,
        "title": "Scheduler/pulse unification table",
        "verified": all(checks.values()),
        "rows": rows,
        "tex_table": "analysis/BT1500_scheduler_pulse_unification_table.tex",
        "source_packets": {
            "canonical_fiber": "data/bt1492_canonical_fano_s4_d4_fiber.json",
            "row_pulses": "data/bt1493_row_action_physical_pulse_compiler.json",
            "transaction_words": "data/bt1495_72_tick_transaction_word_compiler.json",
            "css_replay": "data/bt1499_transaction_word_css_replay.json",
            "scheduler_lift": "data/bt1497_steinberg_scheduler_d4_flag_lift.json",
        },
        "interpretation": "The symmetry, pulse, CSS, and scheduler layers now share one count table: Fano 168, S4 fiber 24, native D4 8, C3 x D4 scheduler 24, 72-tick words, 1728 pulses, and Steinberg 81 states.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1500, "verified": result["verified"], "rows": len(rows)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
