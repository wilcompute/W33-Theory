#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1404_holonet_scope_microframe.json"
HTML_OUT = ROOT / "docs" / "bt1404_holonet_scope.html"


def load_json(path: str) -> dict[str, Any]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def packet_word_for(row: dict[str, Any]) -> list[dict[str, Any]]:
    h = int(row["h"])
    r = int(row["route_trit"])
    p = int(row["phase_trit"])
    parity = (r + p) % 2
    labels = [
        ("ERASE", row["branch"]),
        ("ROUTE", f"r={r}"),
        ("PHASE", f"p={p}"),
        ("X-CORR", f"X^{r}"),
        ("Z-CORR", f"Z^{p}"),
        ("T-BIT", str(parity)),
        ("RESTORE", "Clifford ABI"),
        ("NEXT", f"word {h:02d}"),
    ]
    return [
        {
            "tick": tick,
            "microframe_tick": 8 * h + tick,
            "lane": lane,
            "value": value,
        }
        for tick, (lane, value) in enumerate(labels)
    ]


def build_scope() -> dict[str, Any]:
    bt1403 = load_json("data/bt1403_hesse_port_eraser_lift.json")
    hesse = load_json("data/bt1385_hesse_sic_t_port_abi.json")
    queue = load_json("data/bt1391_hesse_sic_t_queue_model.json")
    runtime = load_json("data/bt1378_runtime_contract_verification.json")

    frames = []
    for row in bt1403["eraser_lift"]["grid"]:
        packet_word = packet_word_for(row)
        frames.append(
            {
                "h": int(row["h"]),
                "route_trit": int(row["route_trit"]),
                "phase_trit": int(row["phase_trit"]),
                "branch": row["branch"],
                "pauli_correction": row["pauli_correction"],
                "t_frame_bit": (int(row["route_trit"]) + int(row["phase_trit"])) % 2,
                "microframe_start_tick": packet_word[0]["microframe_tick"],
                "microframe_end_tick": packet_word[-1]["microframe_tick"],
                "packet_word": packet_word,
            }
        )

    word_ticks = int(hesse["timing_contract"]["word_ticks"])
    microframe_ticks = int(hesse["timing_contract"]["microframe_ticks"])
    clifford_window_ticks = int(hesse["timing_contract"]["clifford_window_ticks"])
    total_scope_ticks = len(frames) * word_ticks
    holonet = " ".join(read("photonic_holonet.tex").split())
    single_photon = " ".join(read("single_photon_universal_computation.tex").split())

    checks = {
        "bt1403_verified": bt1403["verified"] is True,
        "runtime_verified": runtime["verified"] is True,
        "nine_hesse_cells": len(frames) == 9,
        "eight_ticks_per_packet_word": word_ticks == 8
        and all(len(frame["packet_word"]) == 8 for frame in frames),
        "one_hesse_grid_equals_one_microframe": total_scope_ticks
        == microframe_ticks
        == 72,
        "microframes_tile_clifford_window": clifford_window_ticks // microframe_ticks
        == queue["window"]["microframes"]
        == 720,
        "all_microframe_ticks_used_once": sorted(
            tick["microframe_tick"] for frame in frames for tick in frame["packet_word"]
        )
        == list(range(72)),
        "all_hesse_outcomes_still_factor_3x3": [frame["h"] for frame in frames]
        == list(range(9))
        and sorted((frame["route_trit"], frame["phase_trit"]) for frame in frames)
        == [(r, p) for r in range(3) for p in range(3)],
        "t_frame_bit_is_outcome_parity": all(
            frame["t_frame_bit"] == frame["h"] % 2 for frame in frames
        ),
        "manuscripts_expose_bt1403_boundary": "BT1403 eraser-lift port" in holonet
        and "BT1403 eraser-lift port" in single_photon,
    }

    return {
        "bt": 1404,
        "title": "Single-photon holonet scope microframe",
        "verified": all(checks.values()),
        "checks": checks,
        "scope_identity": "9 Hesse outcomes * 8 packet ticks = 72 ticks = one microframe",
        "timing": {
            "hesse_outcomes": len(frames),
            "word_ticks": word_ticks,
            "microframe_ticks": microframe_ticks,
            "clifford_window_ticks": clifford_window_ticks,
            "microframes_per_clifford_window": queue["window"]["microframes"],
        },
        "parity_rule": "t_frame_bit = (route_trit + phase_trit) mod 2 = h mod 2",
        "frames": frames,
        "physical_reading": (
            "The whole Hesse non-Clifford outcome alphabet can be displayed as "
            "one 72-tick microframe: each of the nine eraser-lift outcomes owns "
            "one 8-tick return word that erases the branch, records route and "
            "phase, applies X/Z frame correction, stores the T-frame bit, and "
            "restores the Clifford packet ABI."
        ),
        "html_scope": HTML_OUT.relative_to(ROOT).as_posix(),
        "boundary": (
            "BT1404 is a packet-scope/ABI visualization and verifier. It does "
            "not implement physical SIC optics, detector electronics, or a "
            "magic-state factory."
        ),
    }


def json_for_script(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True).replace("</", "<\\/")


def render_html(scope: dict[str, Any]) -> str:
    data = json_for_script(scope)
    title = html.escape(scope["title"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>BT1404 Holonet Scope</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #172027;
      --muted: #5d6973;
      --line: #cbd5dd;
      --paper: #f7f8f4;
      --panel: #ffffff;
      --route: #087e8b;
      --phase: #8a4f00;
      --frame: #8d2f6a;
      --abi: #345c2c;
      --next: #3949ab;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--paper);
      color: var(--ink);
    }}
    main {{
      width: min(1180px, calc(100vw - 32px));
      margin: 0 auto;
      padding: 28px 0 34px;
    }}
    header {{
      display: flex;
      align-items: end;
      justify-content: space-between;
      gap: 18px;
      border-bottom: 1px solid var(--line);
      padding-bottom: 16px;
    }}
    h1 {{
      margin: 0;
      font-size: clamp(1.55rem, 2.2vw, 2.2rem);
      line-height: 1.05;
      letter-spacing: 0;
    }}
    .sub {{
      margin-top: 8px;
      color: var(--muted);
      max-width: 760px;
      line-height: 1.45;
      font-size: 0.98rem;
    }}
    .metrics {{
      display: grid;
      grid-template-columns: repeat(4, minmax(110px, 1fr));
      gap: 10px;
      margin: 18px 0;
    }}
    .metric, .panel {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
    }}
    .metric {{
      padding: 12px;
      min-height: 70px;
    }}
    .metric strong {{
      display: block;
      font-size: 1.35rem;
      line-height: 1;
      margin-bottom: 7px;
    }}
    .metric span {{
      color: var(--muted);
      font-size: 0.86rem;
    }}
    .layout {{
      display: grid;
      grid-template-columns: minmax(280px, 390px) 1fr;
      gap: 16px;
      align-items: stretch;
    }}
    .panel {{
      padding: 14px;
    }}
    .panel h2 {{
      margin: 0 0 12px;
      font-size: 1rem;
      letter-spacing: 0;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(76px, 1fr));
      gap: 9px;
    }}
    button.cell {{
      appearance: none;
      border: 1px solid var(--line);
      background: #fbfcfd;
      border-radius: 8px;
      min-height: 88px;
      padding: 10px;
      color: var(--ink);
      cursor: pointer;
      text-align: left;
      transition: border-color 120ms ease, background 120ms ease, transform 120ms ease;
    }}
    button.cell[aria-pressed="true"] {{
      border-color: var(--route);
      background: #eaf7f8;
      transform: translateY(-1px);
    }}
    .hnum {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-weight: 700;
      margin-bottom: 8px;
    }}
    .branch {{
      color: var(--muted);
      font-size: 0.82rem;
      overflow-wrap: anywhere;
    }}
    .detail {{
      display: grid;
      grid-template-columns: repeat(4, minmax(90px, 1fr));
      gap: 10px;
      margin-bottom: 14px;
    }}
    .detail div {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 10px;
      background: #fbfcfd;
      min-height: 68px;
    }}
    .detail span {{
      display: block;
      color: var(--muted);
      font-size: 0.78rem;
      margin-bottom: 7px;
    }}
    .detail strong {{
      font-size: 1.02rem;
      overflow-wrap: anywhere;
    }}
    .trace {{
      display: grid;
      grid-template-columns: repeat(8, minmax(68px, 1fr));
      gap: 8px;
    }}
    .tick {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fbfcfd;
      min-height: 112px;
      display: grid;
      grid-template-rows: auto 1fr auto;
      overflow: hidden;
    }}
    .tick b {{
      padding: 8px 8px 2px;
      font-size: 0.78rem;
      color: var(--muted);
    }}
    .tick strong {{
      padding: 4px 8px;
      font-size: 0.88rem;
      overflow-wrap: anywhere;
    }}
    .tick small {{
      display: block;
      padding: 7px 8px;
      background: #eef1f3;
      color: #3f4a51;
      font-size: 0.74rem;
    }}
    .lane-ERASE {{ border-top: 5px solid var(--route); }}
    .lane-ROUTE {{ border-top: 5px solid var(--route); }}
    .lane-PHASE {{ border-top: 5px solid var(--phase); }}
    .lane-X-CORR, .lane-Z-CORR {{ border-top: 5px solid var(--abi); }}
    .lane-T-BIT {{ border-top: 5px solid var(--frame); }}
    .lane-RESTORE {{ border-top: 5px solid var(--abi); }}
    .lane-NEXT {{ border-top: 5px solid var(--next); }}
    .micro {{
      margin-top: 14px;
      display: grid;
      grid-template-columns: repeat(72, 1fr);
      gap: 2px;
      min-height: 34px;
    }}
    .slot {{
      border-radius: 2px;
      background: #d9dfe4;
      min-width: 2px;
    }}
    .slot.active {{ background: var(--route); }}
    .legend {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 14px;
      color: var(--muted);
      font-size: 0.84rem;
    }}
    .legend span {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}
    .swatch {{
      width: 12px;
      height: 12px;
      border-radius: 2px;
      display: inline-block;
      background: var(--line);
    }}
    .swatch.route {{ background: var(--route); }}
    .swatch.phase {{ background: var(--phase); }}
    .swatch.frame {{ background: var(--frame); }}
    .swatch.abi {{ background: var(--abi); }}
    .swatch.next {{ background: var(--next); }}
    footer {{
      margin-top: 18px;
      color: var(--muted);
      font-size: 0.86rem;
      line-height: 1.45;
    }}
    a {{ color: #225ea8; }}
    @media (max-width: 880px) {{
      main {{ width: min(100vw - 20px, 760px); padding-top: 18px; }}
      header {{ display: block; }}
      .metrics {{ grid-template-columns: repeat(2, 1fr); }}
      .layout {{ grid-template-columns: 1fr; }}
      .detail {{ grid-template-columns: repeat(2, 1fr); }}
      .trace {{ grid-template-columns: repeat(4, minmax(64px, 1fr)); }}
    }}
    @media (max-width: 520px) {{
      .metrics, .detail {{ grid-template-columns: 1fr; }}
      .grid {{ grid-template-columns: repeat(3, minmax(58px, 1fr)); gap: 6px; }}
      button.cell {{ min-height: 78px; padding: 8px; }}
      .trace {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <div>
        <h1>{title}</h1>
        <div class="sub">9 Hesse outcomes x 8 packet ticks = 72 ticks: one complete non-Clifford return microframe for the single-photon holonet ABI.</div>
      </div>
      <a href="../analysis/BT1404_holonet_scope_microframe.md">BT1404 note</a>
    </header>
    <section class="metrics" aria-label="scope metrics">
      <div class="metric"><strong id="m-outcomes">9</strong><span>Hesse outcomes</span></div>
      <div class="metric"><strong id="m-word">8</strong><span>ticks per packet word</span></div>
      <div class="metric"><strong id="m-micro">72</strong><span>ticks per microframe</span></div>
      <div class="metric"><strong id="m-window">720</strong><span>microframes per Clifford window</span></div>
    </section>
    <section class="layout">
      <div class="panel">
        <h2>Hesse Outcome Grid</h2>
        <div class="grid" id="grid"></div>
        <div class="legend">
          <span><i class="swatch route"></i>branch/route</span>
          <span><i class="swatch phase"></i>phase</span>
          <span><i class="swatch frame"></i>T-frame</span>
          <span><i class="swatch abi"></i>ABI restore</span>
        </div>
      </div>
      <div class="panel">
        <h2>8-Tick Return Word</h2>
        <div class="detail">
          <div><span>Outcome</span><strong id="d-h">h=0</strong></div>
          <div><span>Branch</span><strong id="d-branch">Omega</strong></div>
          <div><span>Correction</span><strong id="d-correction">X^0 Z^0</strong></div>
          <div><span>Microframe ticks</span><strong id="d-range">0-7</strong></div>
        </div>
        <div class="trace" id="trace"></div>
        <div class="micro" id="micro"></div>
      </div>
    </section>
    <footer>
      Boundary: this page renders the verified packet ABI, not physical SIC optics or a magic-state factory.
    </footer>
  </main>
  <script id="scope-data" type="application/json">{data}</script>
  <script>
    const scope = JSON.parse(document.getElementById("scope-data").textContent);
    const grid = document.getElementById("grid");
    const trace = document.getElementById("trace");
    const micro = document.getElementById("micro");
    document.getElementById("m-outcomes").textContent = scope.timing.hesse_outcomes;
    document.getElementById("m-word").textContent = scope.timing.word_ticks;
    document.getElementById("m-micro").textContent = scope.timing.microframe_ticks;
    document.getElementById("m-window").textContent = scope.timing.microframes_per_clifford_window;

    function render(frame) {{
      for (const button of grid.querySelectorAll("button")) {{
        button.setAttribute("aria-pressed", String(Number(button.dataset.h) === frame.h));
      }}
      document.getElementById("d-h").textContent = `h=${{frame.h}}`;
      document.getElementById("d-branch").textContent = frame.branch;
      document.getElementById("d-correction").textContent = `${{frame.pauli_correction}}, T=${{frame.t_frame_bit}}`;
      document.getElementById("d-range").textContent = `${{frame.microframe_start_tick}}-${{frame.microframe_end_tick}}`;

      trace.replaceChildren(...frame.packet_word.map((tick) => {{
        const node = document.createElement("div");
        node.className = `tick lane-${{tick.lane}}`;
        node.innerHTML = `<b>tick ${{tick.tick}}</b><strong>${{tick.lane}}<br>${{tick.value}}</strong><small>micro ${{tick.microframe_tick}}</small>`;
        return node;
      }}));

      const active = new Set(frame.packet_word.map((tick) => tick.microframe_tick));
      micro.replaceChildren(...Array.from({{ length: scope.timing.microframe_ticks }}, (_, i) => {{
        const node = document.createElement("div");
        node.className = active.has(i) ? "slot active" : "slot";
        node.title = `microframe tick ${{i}}`;
        return node;
      }}));
    }}

    for (const frame of scope.frames) {{
      const button = document.createElement("button");
      button.className = "cell";
      button.type = "button";
      button.dataset.h = frame.h;
      button.setAttribute("aria-pressed", "false");
      button.innerHTML = `<span class="hnum">h=${{frame.h}} <small>r${{frame.route_trit}} p${{frame.phase_trit}}</small></span><span class="branch">${{frame.branch}}</span>`;
      button.addEventListener("click", () => render(frame));
      grid.appendChild(button);
    }}
    render(scope.frames[0]);
  </script>
</body>
</html>
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--html-out", type=Path, default=HTML_OUT)
    ns = ap.parse_args()
    scope = build_scope()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(scope, indent=2) + "\n", encoding="utf-8")
    ns.html_out.parent.mkdir(parents=True, exist_ok=True)
    ns.html_out.write_text(render_html(scope), encoding="utf-8")
    print(
        json.dumps(
            {
                "bt": scope["bt"],
                "verified": scope["verified"],
                "scope_ticks": scope["timing"]["microframe_ticks"],
                "html": ns.html_out.relative_to(ROOT).as_posix(),
            },
            indent=2,
        )
    )
    if not scope["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
