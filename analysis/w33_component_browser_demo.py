#!/usr/bin/env python3
"""Generate a clickable browser demo for W(3,3) component execution.

The page lets a user click source/destination projective points and watch the
control stack update:

    point address -> symplectic route -> K4 line bus -> spread clock -> commit.

All routes and hop metadata are precomputed in JSON, so the browser is a static
inspector rather than a second theorem prover.
"""

from __future__ import annotations

import argparse
import html
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

import holonet_node as hn
from w33_component_execution_simulator import (
    choose_spreads_for_lines,
    clock_walk_for_carriers,
    commit_ticks,
    line_lookup,
)
from w33_spread_clock_graph import adjacency_from_overlap, build_overlap_matrix
from w33_uor_runtime_model import ROOT, all_lines, find_spreads, point_id


DEFAULT_JSON = ROOT / "data" / "w33_component_browser_demo.json"
DEFAULT_HTML = ROOT / "docs" / "w33_component_browser_demo.html"


def coordinates(count: int) -> list[dict[str, float]]:
    cx = 420.0
    cy = 320.0
    radius = 250.0
    coords = []
    for idx in range(count):
        angle = -math.pi / 2 + 2 * math.pi * idx / count
        coords.append(
            {
                "x": round(cx + radius * math.cos(angle), 3),
                "y": round(cy + radius * math.sin(angle), 3),
            }
        )
    return coords


def route_record(
    src_idx: int,
    dst_idx: int,
    lines: list[tuple[int, ...]],
    lookup: dict[tuple[int, int], int],
    spreads: list[list[int]],
    graph: dict[int, set[int]],
) -> dict[str, Any]:
    src = hn.POINTS[src_idx]
    dst = hn.POINTS[dst_idx]
    route_points = hn.route(src, dst)
    route_indices = [hn.POINTS.index(point) for point in route_points]
    line_ids = []
    hops = []
    for hop_index, (left, right) in enumerate(zip(route_indices, route_indices[1:])):
        line_id = lookup[(left, right)]
        line_ids.append(line_id)
        hops.append(
            {
                "hop": hop_index,
                "from": left,
                "to": right,
                "line": line_id,
                "line_points": list(lines[line_id]),
            }
        )
    carriers, choices = choose_spreads_for_lines(line_ids, spreads, graph)
    clock_walk = clock_walk_for_carriers(carriers, graph)
    for hop, choice in zip(hops, choices):
        hop["spread"] = choice["chosen_spread"]
        hop["candidate_spreads"] = choice["candidate_spreads"]

    level = max(1, len(route_indices) - 1)
    return {
        "src": src_idx,
        "dst": dst_idx,
        "src_label": point_id(src),
        "dst_label": point_id(dst),
        "symplectic": int(hn.symplectic(src, dst)),
        "route": route_indices,
        "route_labels": [point_id(point) for point in route_points],
        "hops": hops,
        "hop_count": len(route_indices) - 1,
        "clock_walk": clock_walk,
        "commit": {
            "level": level,
            "route_budget": 8 * level,
            "ticks": commit_ticks(level),
            "frame_locked": commit_ticks(level) % 72 == 0,
        },
    }


def build_payload() -> dict[str, Any]:
    lines = all_lines()
    spreads = find_spreads(lines, limit=10000)
    lookup = line_lookup(lines)
    graph = adjacency_from_overlap(build_overlap_matrix(spreads))
    coords = coordinates(len(hn.POINTS))
    routes: dict[str, dict[str, Any]] = {}
    hop_hist = Counter()
    for src_idx in range(len(hn.POINTS)):
        for dst_idx in range(len(hn.POINTS)):
            record = route_record(src_idx, dst_idx, lines, lookup, spreads, graph)
            routes[f"{src_idx}:{dst_idx}"] = record
            hop_hist[record["hop_count"]] += 1

    points = [
        {
            "id": idx,
            "label": point_id(point),
            "vector": list(point),
            "x": coords[idx]["x"],
            "y": coords[idx]["y"],
        }
        for idx, point in enumerate(hn.POINTS)
    ]
    default = routes["0:2"]
    checks = {
        "forty_points": len(points) == 40,
        "forty_lines": len(lines) == 40,
        "thirty_six_spreads": len(spreads) == 36,
        "all_1600_routes_present": len(routes) == 1600,
        "hop_histogram_is_w33": {
            str(key): hop_hist[key] for key in sorted(hop_hist)
        }
        == {"0": 40, "1": 480, "2": 1080},
        "max_route_hops_two": max(hop_hist) == 2,
        "default_route_is_two_hop": default["hop_count"] == 2,
        "all_nonidentity_hops_have_line_and_spread": all(
            all("line" in hop and "spread" in hop for hop in route["hops"])
            for route in routes.values()
            if route["hop_count"] > 0
        ),
    }
    return {
        "schema": "w33.component_browser_demo.v1",
        "title": "W(3,3) component browser demo",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "points": points,
        "lines": [list(line) for line in lines],
        "spreads": spreads,
        "routes": routes,
        "default_route_key": "0:2",
        "hop_histogram": {str(key): hop_hist[key] for key in sorted(hop_hist)},
        "checks": checks,
        "boundary": (
            "The browser is a static inspector over precomputed finite W33 data. "
            "It does not prove new facts at runtime or simulate calibrated optics."
        ),
    }


def html_page(payload: dict[str, Any]) -> str:
    data = html.escape(json.dumps(payload, separators=(",", ":")), quote=False)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>W(3,3) Component Browser</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #17202a;
      --muted: #5f6f7a;
      --panel: #f4f7f8;
      --line: #cad5d9;
      --src: #2d6cdf;
      --dst: #b43b48;
      --route: #118264;
      --bus: #8a5a00;
      --clock: #6d55c7;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font: 14px/1.45 system-ui, -apple-system, Segoe UI, sans-serif;
      color: var(--ink);
      background: #ffffff;
    }}
    header {{
      padding: 20px 24px 10px;
      border-bottom: 1px solid var(--line);
    }}
    h1 {{ margin: 0 0 6px; font-size: 22px; letter-spacing: 0; }}
    .sub {{ color: var(--muted); max-width: 980px; }}
    main {{
      display: grid;
      grid-template-columns: minmax(520px, 1fr) 380px;
      gap: 18px;
      padding: 18px 24px 24px;
    }}
    svg {{
      width: 100%;
      height: auto;
      min-height: 560px;
      border: 1px solid var(--line);
      background: #fbfcfc;
    }}
    .point {{ cursor: pointer; }}
    .point circle {{ fill: #ffffff; stroke: #8aa0aa; stroke-width: 1.5; }}
    .point text {{ font-size: 10px; fill: #24343c; text-anchor: middle; dominant-baseline: central; pointer-events: none; }}
    .point.src circle {{ fill: #e7f0ff; stroke: var(--src); stroke-width: 3; }}
    .point.dst circle {{ fill: #fff0f1; stroke: var(--dst); stroke-width: 3; }}
    .point.route circle {{ fill: #e8faf3; stroke: var(--route); stroke-width: 3; }}
    .route-line {{ stroke: var(--route); stroke-width: 4; stroke-linecap: round; opacity: 0.88; }}
    .route-line.bus {{ stroke: var(--bus); }}
    .panel {{
      border: 1px solid var(--line);
      background: var(--panel);
      padding: 14px;
    }}
    .controls {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px; }}
    button {{
      border: 1px solid #8ba1aa;
      background: #ffffff;
      color: var(--ink);
      padding: 7px 10px;
      cursor: pointer;
    }}
    button.active {{ border-color: var(--clock); box-shadow: inset 0 0 0 1px var(--clock); }}
    .metric-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 12px 0; }}
    .metric {{ background: #ffffff; border: 1px solid var(--line); padding: 8px; min-height: 58px; }}
    .metric b {{ display: block; font-size: 16px; }}
    table {{ width: 100%; border-collapse: collapse; background: #ffffff; margin-top: 12px; }}
    th, td {{ border: 1px solid var(--line); padding: 6px; text-align: left; vertical-align: top; }}
    th {{ background: #e9eef1; }}
    code {{ font-family: ui-monospace, SFMono-Regular, Consolas, monospace; }}
    .stage {{ margin-top: 10px; padding: 8px; background: #ffffff; border-left: 4px solid var(--clock); }}
    @media (max-width: 960px) {{
      main {{ grid-template-columns: 1fr; padding: 12px; }}
      header {{ padding: 16px 12px 8px; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>W(3,3) Component Browser</h1>
    <div class="sub">Click a source point, then a destination point. The route, K4 line buses, spread-clock frames, and durable commit marker are precomputed from the W(3,3) incidence law.</div>
  </header>
  <main>
    <section>
      <svg id="fabric" viewBox="0 0 840 640" role="img" aria-label="W33 projective points"></svg>
    </section>
    <aside class="panel">
      <div class="controls">
        <button id="mode-source">Pick Source</button>
        <button id="mode-dest">Pick Destination</button>
        <button id="play">Play Stack</button>
        <button id="reset">Reset</button>
      </div>
      <div id="summary"></div>
      <div class="metric-grid">
        <div class="metric"><span>Route hops</span><b id="m-hops">-</b></div>
        <div class="metric"><span>Clock slots</span><b id="m-clock">-</b></div>
        <div class="metric"><span>Commit ticks</span><b id="m-commit">-</b></div>
        <div class="metric"><span>Symplectic</span><b id="m-symp">-</b></div>
      </div>
      <div id="stage" class="stage"></div>
      <div id="tables"></div>
    </aside>
  </main>
  <script id="w33-demo-data" type="application/json">{data}</script>
  <script>
  const DATA = JSON.parse(document.getElementById('w33-demo-data').textContent);
  const svg = document.getElementById('fabric');
  let source = DATA.routes[DATA.default_route_key].src;
  let dest = DATA.routes[DATA.default_route_key].dst;
  let mode = 'source';
  let timer = null;
  let stageIndex = 0;

  function el(name, attrs = {{}}, text = '') {{
    const node = document.createElementNS('http://www.w3.org/2000/svg', name);
    Object.entries(attrs).forEach(([k, v]) => node.setAttribute(k, v));
    if (text) node.textContent = text;
    return node;
  }}

  function route() {{ return DATA.routes[`${{source}}:${{dest}}`]; }}

  function draw() {{
    const r = route();
    svg.innerHTML = '';
    r.hops.forEach((hop, idx) => {{
      const a = DATA.points[hop.from];
      const b = DATA.points[hop.to];
      svg.appendChild(el('line', {{
        x1: a.x, y1: a.y, x2: b.x, y2: b.y,
        class: idx === stageIndex - 2 ? 'route-line bus' : 'route-line'
      }}));
    }});
    DATA.points.forEach((p) => {{
      const g = el('g', {{ class: pointClass(p.id, r), tabindex: 0 }});
      g.appendChild(el('circle', {{ cx: p.x, cy: p.y, r: 18 }}));
      g.appendChild(el('text', {{ x: p.x, y: p.y }}, p.label));
      g.addEventListener('click', () => choosePoint(p.id));
      svg.appendChild(g);
    }});
    updatePanel(r);
  }}

  function pointClass(id, r) {{
    const classes = ['point'];
    if (id === source) classes.push('src');
    if (id === dest) classes.push('dst');
    if (r.route.includes(id)) classes.push('route');
    return classes.join(' ');
  }}

  function choosePoint(id) {{
    if (mode === 'source') {{
      source = id;
      mode = 'dest';
    }} else {{
      dest = id;
      mode = 'source';
    }}
    stageIndex = 0;
    setModeButtons();
    draw();
  }}

  function setModeButtons() {{
    document.getElementById('mode-source').classList.toggle('active', mode === 'source');
    document.getElementById('mode-dest').classList.toggle('active', mode === 'dest');
  }}

  function stages(r) {{
    return [
      `Address source ${{r.src_label}} and destination ${{r.dst_label}}.`,
      `Symplectic route: ${{r.route_labels.join(' -> ')}}.`,
      ...r.hops.map((hop) => `Hop ${{hop.hop}} uses K4 line bus ${{hop.line}} and spread frame ${{hop.spread}}.`),
      `Clock walk: ${{r.clock_walk.map(s => s.kind + ':' + s.spread).join(', ') || 'identity'}}.`,
      `Commit marker: ${{r.commit.ticks}} ticks; route budget ${{r.commit.route_budget}} ticks.`
    ];
  }}

  function updatePanel(r) {{
    document.getElementById('summary').innerHTML =
      `<b>${{r.src_label}}</b> to <b>${{r.dst_label}}</b><br><code>${{r.route_labels.join(' -> ')}}</code>`;
    document.getElementById('m-hops').textContent = r.hop_count;
    document.getElementById('m-clock').textContent = r.clock_walk.length;
    document.getElementById('m-commit').textContent = r.commit.ticks;
    document.getElementById('m-symp').textContent = r.symplectic;
    const stageList = stages(r);
    document.getElementById('stage').textContent = stageList[Math.min(stageIndex, stageList.length - 1)];
    const hopRows = r.hops.map((hop) =>
      `<tr><td>${{hop.hop}}</td><td><code>${{DATA.points[hop.from].label}}</code></td><td><code>${{DATA.points[hop.to].label}}</code></td><td>${{hop.line}}</td><td>${{hop.spread}}</td></tr>`
    ).join('');
    document.getElementById('tables').innerHTML =
      `<table><thead><tr><th>Hop</th><th>From</th><th>To</th><th>K4 bus</th><th>Spread</th></tr></thead><tbody>${{hopRows || '<tr><td colspan="5">identity route</td></tr>'}}</tbody></table>`;
  }}

  function play() {{
    if (timer) {{ clearInterval(timer); timer = null; return; }}
    const limit = stages(route()).length - 1;
    stageIndex = 0;
    draw();
    timer = setInterval(() => {{
      stageIndex += 1;
      draw();
      if (stageIndex >= limit) {{
        clearInterval(timer);
        timer = null;
      }}
    }}, 750);
  }}

  document.getElementById('mode-source').onclick = () => {{ mode = 'source'; setModeButtons(); }};
  document.getElementById('mode-dest').onclick = () => {{ mode = 'dest'; setModeButtons(); }};
  document.getElementById('play').onclick = play;
  document.getElementById('reset').onclick = () => {{
    source = DATA.routes[DATA.default_route_key].src;
    dest = DATA.routes[DATA.default_route_key].dst;
    stageIndex = 0;
    draw();
  }};
  setModeButtons();
  draw();
  </script>
</body>
</html>
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-out", default=str(DEFAULT_JSON))
    parser.add_argument("--html-out", default=str(DEFAULT_HTML))
    args = parser.parse_args(argv)

    payload = build_payload()
    json_out = Path(args.json_out)
    if not json_out.is_absolute():
        json_out = ROOT / json_out
    html_out = Path(args.html_out)
    if not html_out.is_absolute():
        html_out = ROOT / html_out
    json_out.parent.mkdir(parents=True, exist_ok=True)
    html_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    html_out.write_text(html_page(payload), encoding="utf-8")

    print(f"status: {payload['status']}")
    print(f"routes: {len(payload['routes'])}, hop_histogram={payload['hop_histogram']}")
    print(f"wrote: {json_out.relative_to(ROOT)}")
    print(f"wrote: {html_out.relative_to(ROOT)}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
