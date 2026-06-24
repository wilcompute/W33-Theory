#!/usr/bin/env python3
"""BT1701 - Holonet packet trace visualizer.

The BT1698/BT1699 packet is now executable.  BT1701 emits a compact SVG/HTML
schematic of the 72-tick packet, its hardware windows, its guard weld, and the
BT1700 recursive compiler law.
"""

from __future__ import annotations

import html
import json
from collections import Counter
from pathlib import Path
from typing import Any

from bt1699_holonet_abi_to_hardware_lowering import build_certificate as build_lowering
from bt1700_recursive_holonet_packet_compiler import (
    build_certificate as build_recursive,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1701_holonet_packet_trace_visualizer.json"
HTML_OUT = ROOT / "docs" / "bt1701_holonet_packet_trace_visualizer.html"

STAGE_COLORS = {
    "source_switch": "#2563eb",
    "program_delay": "#7c3aed",
    "analyzer_or_fuel_body": "#059669",
    "detector_or_hesse_handoff": "#d97706",
    "dark_reference": "#475569",
}


def stage_label(stage: str) -> str:
    return stage.replace("_", " ")


def svg_trace(rows: list[dict[str, Any]]) -> str:
    tick_w = 12
    height = 92
    width = 72 * tick_w + 44
    parts = [
        f'<svg class="packet-svg" viewBox="0 0 {width} {height}" '
        'role="img" aria-label="72 tick Holonet packet trace">'
    ]
    parts.append('<rect x="0" y="0" width="100%" height="100%" fill="#f8fafc"/>')
    for row in rows:
        tick = int(row["tick"])
        x = 24 + tick * tick_w
        stage = row["hardware_stage"]
        color = STAGE_COLORS[stage]
        y = 28 if row["logical_region"] == "tomotope_body" else 56
        parts.append(
            f'<rect class="tick {stage}" x="{x}" y="{y}" width="{tick_w - 1}" '
            f'height="20" fill="{color}"><title>tick {tick}: '
            f'{html.escape(row["logical_op"])} / {html.escape(stage_label(stage))}'
            "</title></rect>"
        )
        if tick % 8 == 0:
            parts.append(
                f'<text x="{x}" y="18" font-size="8" text-anchor="middle" '
                f'fill="#334155">{tick}</text>'
            )
    parts.append('<text x="8" y="43" font-size="9" fill="#0f172a">body</text>')
    parts.append('<text x="8" y="71" font-size="9" fill="#0f172a">guard</text>')
    parts.append(
        '<text x="24" y="88" font-size="9" fill="#334155">'
        "72 = 48 body ticks + 24 Hesse/guard ticks; colors are hardware stages"
        "</text>"
    )
    parts.append("</svg>")
    return "\n".join(parts)


def render_html(cert: dict[str, Any]) -> str:
    legend = "\n".join(
        f'<span class="legend-item"><span class="swatch" '
        f'style="background:{color}"></span>{html.escape(stage_label(stage))}</span>'
        for stage, color in STAGE_COLORS.items()
    )
    laws = cert["recursive_law"]
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>BT1701 Holonet Packet Trace</title>
  <style>
    body {{ font-family: system-ui, -apple-system, Segoe UI, sans-serif; margin: 0; color: #0f172a; background: #f8fafc; }}
    main {{ max-width: 1120px; margin: 0 auto; padding: 32px 20px 48px; }}
    h1 {{ font-size: 28px; margin: 0 0 8px; }}
    p {{ line-height: 1.55; }}
    .panel {{ background: white; border: 1px solid #cbd5e1; border-radius: 8px; padding: 18px; margin: 18px 0; }}
    .packet-svg {{ width: 100%; height: auto; border: 1px solid #cbd5e1; border-radius: 6px; }}
    .legend {{ display: flex; flex-wrap: wrap; gap: 12px; margin-top: 12px; font-size: 14px; }}
    .legend-item {{ display: inline-flex; align-items: center; gap: 6px; }}
    .swatch {{ width: 14px; height: 14px; border-radius: 3px; display: inline-block; }}
    code {{ background: #e2e8f0; padding: 2px 5px; border-radius: 4px; }}
    table {{ border-collapse: collapse; width: 100%; margin-top: 10px; }}
    th, td {{ border-bottom: 1px solid #e2e8f0; padding: 8px; text-align: left; font-size: 14px; }}
  </style>
</head>
<body>
<main>
  <h1>BT1701 Holonet Packet Trace</h1>
  <p>The finite packet is shown as the verified 72-tick ABI: 48 body ticks and
  24 guard/Hesse ticks, lowered onto the physical frame stages from BT1699.</p>
  <section class="panel">
    {cert["svg"]}
    <div class="legend">{legend}</div>
  </section>
  <section class="panel">
    <h2>Compiler Law</h2>
    <table>
      <tr><th>quantity</th><th>law</th></tr>
      <tr><td>packet count</td><td><code>{html.escape(laws["packet_count"])}</code></td></tr>
      <tr><td>commit clock</td><td><code>{html.escape(laws["commit_clock"])}</code></td></tr>
      <tr><td>scheduler</td><td><code>{html.escape(laws["scheduler"])}</code></td></tr>
      <tr><td>supercycle</td><td><code>{html.escape(laws["supercycle"])}</code></td></tr>
    </table>
  </section>
  <section class="panel">
    <h2>Guard Weld</h2>
    <p>The 24-row interface is port flag <code>168+i</code>, CSS edge row
    <code>216+i</code>, and D4 magic aperture <code>i</code> for
    <code>0 &lt;= i &lt; 24</code>.</p>
  </section>
</main>
</body>
</html>
"""


def build_certificate() -> dict[str, Any]:
    lowering = build_lowering()
    recursive = build_recursive()
    rows = lowering["lowering_rows"]
    stage_histogram = Counter(row["hardware_stage"] for row in rows)
    tick_cells = [
        {
            "tick": row["tick"],
            "logical_region": row["logical_region"],
            "logical_op": row["logical_op"],
            "hardware_stage": row["hardware_stage"],
            "tomotope_flag": row["tomotope_flag"],
        }
        for row in rows
    ]
    cert: dict[str, Any] = {
        "theorem": "BT1701 Holonet Packet Trace Visualizer",
        "verified": False,
        "breakthrough": (
            "The execution stack now has a rendered packet schematic: every "
            "tick, hardware stage, guard weld, and recursive scaling law is "
            "visible from one generated HTML/SVG artifact."
        ),
        "html_output": str(HTML_OUT.relative_to(ROOT)),
        "stage_colors": STAGE_COLORS,
        "stage_histogram": dict(sorted(stage_histogram.items())),
        "tick_cells": tick_cells,
        "guard_weld_sample": lowering["guard_weld"][:6],
        "recursive_law": recursive["compiler_law"],
        "svg": svg_trace(rows),
        "source_certificates": [
            "data/bt1698_holonet_packet_state_machine.json",
            "data/bt1699_holonet_abi_to_hardware_lowering.json",
            "data/bt1700_recursive_holonet_packet_compiler.json",
        ],
    }
    html_text = render_html(cert)
    checks = {
        "bt1699_verified": lowering["verified"] is True,
        "bt1700_verified": recursive["verified"] is True,
        "has_72_tick_cells": len(tick_cells) == 72,
        "stage_histogram_matches_8_24_16_16_8": dict(stage_histogram)
        == {
            "source_switch": 8,
            "program_delay": 24,
            "analyzer_or_fuel_body": 16,
            "detector_or_hesse_handoff": 16,
            "dark_reference": 8,
        },
        "svg_contains_72_rectangles": cert["svg"].count('class="tick ') == 72,
        "html_contains_svg_and_guard_weld": "<svg" in html_text
        and "Guard Weld" in html_text
        and "BT1701 Holonet Packet Trace" in html_text,
    }
    cert["checks"] = checks
    cert["verified"] = all(checks.values())
    cert["html"] = html_text
    return cert


def main() -> int:
    cert = build_certificate()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    HTML_OUT.parent.mkdir(parents=True, exist_ok=True)
    HTML_OUT.write_text(cert.pop("html"), encoding="utf-8")
    OUT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(cert["theorem"])
    print(f"  verified: {cert['verified']}")
    print(f"  html: {cert['html_output']}")
    print(f"  ticks rendered: {len(cert['tick_cells'])}")
    print(f"  wrote {OUT}")
    return 0 if cert["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
