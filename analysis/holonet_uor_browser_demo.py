#!/usr/bin/env python3
"""Generate a standalone browser replay for the Holonet-UOR OS trace."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any

from w33_uor_runtime_model import all_lines, find_spreads

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TRACE = ROOT / "data" / "holonet_os_scheduler_trace.json"
DEFAULT_MOCK = ROOT / "data" / "holonet_uor_mock_runtime_report.json"
DEFAULT_SHACL = ROOT / "data" / "holonet_uor_shacl_shape_report.json"
DEFAULT_COMPILER = ROOT / "data" / "w33_line_context_compiler.json"
DEFAULT_CLOCK = ROOT / "data" / "w33_spread_clock_graph.json"
DEFAULT_OUT = ROOT / "docs" / "holonet_uor_os_replay.html"


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_html(
    trace: dict[str, Any],
    mock: dict[str, Any],
    shacl: dict[str, Any],
    compiler: dict[str, Any],
    clock: dict[str, Any],
) -> str:
    compiler_jobs = {row["job_id"]: row for row in compiler["lowering"]["jobs"]}
    spreads = find_spreads(all_lines(), limit=10000)
    payload = {
        "trace": trace,
        "micro": {
            "status": compiler["status"],
            "tick_count": compiler["active_schedule"]["tick_count"],
            "job_count": compiler["lowering"]["job_count"],
            "schedule_hash": compiler["active_schedule"]["schedule_hash"],
            "optimality": compiler["optimizer"]["optimality_status"],
            "exact_backend": compiler["optimizer"]["exact_backend"]["status"],
            "ticks": compiler["active_schedule"]["ticks"],
            "jobs": compiler_jobs,
        },
        "clock": {
            "status": clock["status"],
            "srg_parameters": clock["clock_graph"]["srg_parameters"],
            "coarse_clock_slots": clock["schedule_embeddings"]["coarse_site_os"][
                "clock_slot_count"
            ],
            "micro_clock_slots": clock["schedule_embeddings"][
                "active_line_context_microkernel"
            ]["clock_slot_count"],
            "micro_connectors": clock["schedule_embeddings"][
                "active_line_context_microkernel"
            ]["connector_slot_count"],
            "coarse_connectors": clock["schedule_embeddings"]["coarse_site_os"][
                "connector_slot_count"
            ],
            "micro_expanded_walk": clock["schedule_embeddings"][
                "active_line_context_microkernel"
            ]["expanded_clock_walk"],
            "clock_native_slots": clock["schedule_embeddings"][
                "clock_native_line_context_microkernel"
            ]["clock_slot_count"],
            "clock_native_connectors": clock["schedule_embeddings"][
                "clock_native_line_context_microkernel"
            ]["connector_slot_count"],
            "frames": [
                {"spread_epoch": idx, "line_indices": spread}
                for idx, spread in enumerate(spreads)
            ],
        },
        "clock_native": {
            "tick_count": compiler["clock_native_schedule"]["tick_count"],
            "clock_slot_count": compiler["clock_native_schedule"]["clock_slot_count"],
            "connector_slot_count": compiler["clock_native_schedule"][
                "connector_slot_count"
            ],
            "schedule_hash": compiler["clock_native_schedule"]["schedule_hash"],
            "ticks": compiler["clock_native_schedule"]["ticks"],
        },
        "mock": {
            "status": mock["status"],
            "pipeline_complete": mock["pipeline_complete"],
            "responses": list(mock["responses"].keys()),
        },
        "shacl": {
            "status": shacl["status"],
            "results": [
                {
                    "source": row["source"],
                    "conforms": row["conforms"],
                    "checked_constraints": row["checked_constraints"],
                    "live_ok": bool((row.get("live_uor_shacl_probe") or {}).get("ok")),
                }
                for row in shacl["results"]
            ],
        },
    }
    data = json.dumps(payload, separators=(",", ":"), ensure_ascii=True)
    title = "Holonet UOR OS Replay"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #18212f;
      --muted: #586272;
      --line: #c8d0d9;
      --paper: #f7f8fa;
      --panel: #ffffff;
      --accent: #0f766e;
      --warn: #b45309;
      --hot: #9f1239;
      --blue: #1d4ed8;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--paper);
      color: var(--ink);
    }}
    header {{
      padding: 22px clamp(18px, 4vw, 48px);
      border-bottom: 1px solid var(--line);
      background: #ffffff;
      display: grid;
      gap: 10px;
    }}
    h1 {{ margin: 0; font-size: clamp(24px, 4vw, 42px); letter-spacing: 0; }}
    .subtitle {{ margin: 0; color: var(--muted); max-width: 980px; line-height: 1.45; }}
    main {{
      padding: 18px clamp(18px, 4vw, 48px) 42px;
      display: grid;
      gap: 18px;
    }}
    .toolbar {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 10px;
      padding: 12px;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
    }}
    button {{
      border: 1px solid #8894a3;
      background: #ffffff;
      color: var(--ink);
      border-radius: 7px;
      min-height: 36px;
      padding: 0 12px;
      font-weight: 650;
      cursor: pointer;
    }}
    button:hover {{ border-color: var(--accent); color: var(--accent); }}
    button.active {{ border-color: var(--accent); color: #fff; background: var(--accent); }}
    input[type="range"] {{ flex: 1 1 240px; min-width: 180px; accent-color: var(--accent); }}
    .stats {{
      display: grid;
      grid-template-columns: repeat(4, minmax(120px, 1fr));
      gap: 10px;
    }}
    .stat, .panel {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
    }}
    .stat {{ padding: 12px; }}
    .label {{ font-size: 12px; color: var(--muted); text-transform: uppercase; letter-spacing: .08em; }}
    .value {{ font-size: 24px; font-weight: 750; margin-top: 4px; }}
    .grid {{
      display: grid;
      grid-template-columns: minmax(280px, 1.1fr) minmax(320px, 1.6fr);
      gap: 18px;
      align-items: start;
    }}
    .panel {{ padding: 14px; }}
    .panel h2 {{ margin: 0 0 10px; font-size: 18px; }}
    .ticklist {{ display: grid; gap: 8px; max-height: 520px; overflow: auto; padding-right: 4px; }}
    .tick {{
      border: 1px solid var(--line);
      border-radius: 7px;
      padding: 10px;
      cursor: pointer;
      display: grid;
      grid-template-columns: 48px 1fr auto;
      gap: 10px;
      align-items: center;
    }}
    .tick.active {{ border-color: var(--accent); box-shadow: inset 4px 0 0 var(--accent); }}
    .tick small {{ color: var(--muted); }}
    .board {{
      display: grid;
      grid-template-columns: repeat(10, minmax(22px, 1fr));
      gap: 6px;
      margin-top: 10px;
    }}
    .site {{
      aspect-ratio: 1;
      border: 1px solid #b9c3ce;
      border-radius: 6px;
      display: grid;
      place-items: center;
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 10px;
      color: #334155;
      background: #f8fafc;
    }}
    .site.used {{ background: #ccfbf1; border-color: var(--accent); color: #0f3f3a; font-weight: 700; }}
    .packet-table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    .packet-table th, .packet-table td {{ padding: 7px 8px; border-bottom: 1px solid #e2e8f0; text-align: left; }}
    .packet-table th {{ color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: .06em; }}
    .packet-table tr.highlighted {{ background: #fff7ed; box-shadow: inset 4px 0 0 var(--hot); }}
    .badges {{ display: flex; flex-wrap: wrap; gap: 8px; }}
    .badge {{ border: 1px solid var(--line); border-radius: 999px; padding: 5px 9px; background: #fff; font-size: 13px; }}
    .ok {{ color: var(--accent); border-color: #99d7ce; }}
    .warn {{ color: var(--warn); border-color: #f1c27d; }}
    .clock-panel {{
      margin-top: 14px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fbfdff;
      padding: 10px;
    }}
    .clock-title {{
      display: flex;
      justify-content: space-between;
      gap: 10px;
      align-items: baseline;
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: .06em;
      margin-bottom: 4px;
    }}
    .clock-svg {{ width: 100%; max-height: 300px; display: block; }}
    .clock-link {{ stroke: #94a3b8; stroke-width: 1.4; opacity: .48; }}
    .clock-link.current {{ stroke: var(--hot); stroke-width: 3; opacity: .95; }}
    .frame-node {{ fill: #fff; stroke: #aab6c4; stroke-width: 1.4; }}
    .frame-node.path {{ fill: #e0f2fe; stroke: var(--blue); }}
    .frame-node.connector {{ fill: #fef3c7; stroke: var(--warn); }}
    .frame-node.current {{ fill: #ffe4e6; stroke: var(--hot); stroke-width: 2.6; }}
    .frame-g {{ cursor: pointer; }}
    .frame-label {{ font: 9px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; fill: #334155; text-anchor: middle; dominant-baseline: central; }}
    .frame-inspect {{
      margin-top: 8px;
      font-size: 12px;
      line-height: 1.45;
      color: var(--muted);
      max-height: 120px;
      overflow: auto;
    }}
    .frame-inspect strong {{ color: var(--ink); }}
    @media (max-width: 860px) {{
      .stats, .grid {{ grid-template-columns: 1fr; }}
      .board {{ grid-template-columns: repeat(5, minmax(34px, 1fr)); }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>Holonet UOR OS Replay</h1>
    <p class="subtitle">A deterministic replay of the current Holonet wrapper packets at two layers: the 8-tick coarse site OS trace and the 14-tick strict line-context microkernel, with the 36-frame spread clock underneath.</p>
  </header>
  <main>
    <section class="toolbar">
      <button id="coarseMode" class="active">OS Ticks</button>
      <button id="microMode">Microkernel</button>
      <button id="clockMode">Clock Walk</button>
      <button id="nativeMode">Clock Native</button>
      <button id="prev">Prev</button>
      <button id="play">Play</button>
      <button id="next">Next</button>
      <input id="slider" type="range" min="0" value="0">
      <span id="tickLabel" class="badge"></span>
    </section>
    <section class="stats" id="stats"></section>
    <section class="grid">
      <div class="panel">
        <h2 id="listTitle">Spread Ticks</h2>
        <div class="ticklist" id="tickList"></div>
      </div>
      <div class="panel">
        <h2 id="detailTitle">Tick</h2>
        <div class="badges" id="badges"></div>
        <div class="board" id="board"></div>
        <div class="clock-panel">
          <div class="clock-title"><span>Frame Clock</span><span id="clockMeta"></span></div>
          <div id="clockPanel"></div>
          <div id="frameInspect" class="frame-inspect"></div>
        </div>
        <h2 style="margin-top:18px;">Packets</h2>
        <table class="packet-table">
          <thead><tr><th>Item</th><th>Sites</th><th>Route</th></tr></thead>
          <tbody id="packets"></tbody>
        </table>
      </div>
    </section>
  </main>
  <script id="replay-data" type="application/json">{data}</script>
  <script>
    const payload = JSON.parse(document.getElementById('replay-data').textContent);
    const trace = payload.trace;
    const micro = payload.micro;
    const clockNative = payload.clock_native;
    let mode = 'coarse';
    let idx = 0;
    let selectedFrame = null;
    let highlightedJob = null;
    let timer = null;
    const slider = document.getElementById('slider');
    function layer() {{
      if (mode === 'coarse') {{
        return {{ label: 'OS Ticks', ticks: trace.ticks, hash: trace.replay_hash, kind: 'coarse' }};
      }}
      if (mode === 'micro') {{
        return {{ label: 'Microkernel Ticks', ticks: micro.ticks, hash: micro.schedule_hash, kind: 'micro' }};
      }}
      if (mode === 'native') {{
        return {{ label: 'Clock Native', ticks: clockNative.ticks, hash: clockNative.schedule_hash, kind: 'native' }};
      }}
      const ticks = payload.clock.micro_expanded_walk.map((slot, i) => {{
        const source = slot.kind === 'active' ? micro.ticks[slot.source_tick] : null;
        return {{
          tick: i,
          spread_epoch: slot.spread_epoch,
          kind: slot.kind,
          source_tick: slot.source_tick,
          between_ticks: slot.between_ticks,
          dispatch_count: source ? source.dispatch_count : 0,
          used_site_count: source ? source.used_site_count : 0,
          jobs: source ? source.jobs : []
        }};
      }});
      return {{ label: 'Clock Walk', ticks, hash: micro.schedule_hash, kind: 'clock' }};
    }}

    function syncModeButtons() {{
      document.getElementById('coarseMode').classList.toggle('active', mode === 'coarse');
      document.getElementById('microMode').classList.toggle('active', mode === 'micro');
      document.getElementById('clockMode').classList.toggle('active', mode === 'clock');
      document.getElementById('nativeMode').classList.toggle('active', mode === 'native');
    }}

    function applyInitialQuery() {{
      const params = new URLSearchParams(window.location.search);
      const requestedMode = params.get('mode');
      if (['coarse', 'micro', 'clock', 'native'].includes(requestedMode)) {{
        mode = requestedMode;
      }}
      highlightedJob = params.get('job') || null;
      const current = layer();
      const ticks = current.ticks;
      const tickParam = Number(params.get('tick'));
      const frameParam = Number(params.get('frame'));
      if (Number.isInteger(tickParam) && tickParam >= 0 && tickParam < ticks.length) {{
        idx = tickParam;
      }} else if (highlightedJob) {{
        const jobIndex = ticks.findIndex(t => (t.jobs || []).includes(highlightedJob));
        if (jobIndex >= 0) idx = jobIndex;
      }} else if (Number.isInteger(frameParam)) {{
        const frameIndex = ticks.findIndex(t => Number(t.spread_epoch) === frameParam);
        if (frameIndex >= 0) idx = frameIndex;
      }}
      if (Number.isInteger(frameParam) && frameParam >= 0 && frameParam < 36) {{
        selectedFrame = frameParam;
      }}
    }}

    const coarseSites = trace.ticks.flatMap(t => t.packets.flatMap(p => p.sites));
    const microSites = micro.ticks.flatMap(t => t.jobs.flatMap(id => (micro.jobs[id] || {{sites: []}}).sites));
    const nativeSites = clockNative.ticks.flatMap(t => t.jobs.flatMap(id => (micro.jobs[id] || {{sites: []}}).sites));
    const allSites = Array.from(new Set([...coarseSites, ...microSites, ...nativeSites])).sort();

    function stat(label, value) {{
      return `<div class="stat"><div class="label">${{label}}</div><div class="value">${{value}}</div></div>`;
    }}
    document.getElementById('stats').innerHTML = [
      stat('Packets', trace.packet_count),
      stat('OS Ticks', trace.tick_count),
      stat('Micro Ticks', micro.tick_count),
      stat('Clock Slots', `${{payload.clock.coarse_clock_slots}} / ${{payload.clock.micro_clock_slots}} / ${{payload.clock.clock_native_slots}}`)
    ].join('');

    function normalizedItems(t) {{
      if (mode === 'coarse') {{
        return t.packets.map(p => ({{
          id: p.packet_id,
          sites: p.sites,
          route: `${{p.hops}} hop${{p.hops === 1 ? '' : 's'}}`
        }}));
      }}
      if (mode === 'clock' && t.kind === 'connector') {{
        return [{{
          id: `connector ${{t.between_ticks[0]}}→${{t.between_ticks[1]}}`,
          sites: [],
          route: `spread ${{t.spread_epoch}} bridge`
        }}];
      }}
      return t.jobs.map(id => {{
        const job = micro.jobs[id] || {{ sites: [], line_index: '?', hop_index: '?' }};
        return {{
          id,
          sites: job.sites,
          route: `line ${{job.line_index}}, hop ${{job.hop_index}}`
        }};
      }});
    }}

    function renderFrameInspect(current, t, pathSlots) {{
      const frame = selectedFrame === null ? Number(t.spread_epoch) : Number(selectedFrame);
      const hits = pathSlots.filter(slot => slot.spread === frame);
      const currentItems = Number(t.spread_epoch) === frame ? normalizedItems(t) : [];
      const slotText = hits.length
        ? hits.map(slot => `${{slot.index}}:${{slot.kind}}`).join(', ')
        : 'unused by this replay layer';
      const connectorText = hits
        .filter(slot => slot.kind === 'connector')
        .map(slot => `slot ${{slot.index}} bridges ticks ${{(slot.between_ticks || []).join('→')}}`)
        .join('; ');
      const frameLines = ((payload.clock.frames || [])[frame] || {{ line_indices: [] }}).line_indices || [];
      const jobText = currentItems.length
        ? currentItems.map(item => item.id).slice(0, 8).join(', ') + (currentItems.length > 8 ? ' ...' : '')
        : 'no active jobs at the current selected tick';
      document.getElementById('frameInspect').innerHTML = [
        `<div><strong>Frame ${{frame}}</strong> in ${{current.label}}</div>`,
        `<div>Spread lines: ${{frameLines.join(', ')}}</div>`,
        `<div>Slots: ${{slotText}}</div>`,
        connectorText ? `<div>Connector reason: ${{connectorText}}</div>` : `<div>Connector reason: none for selected frame in this layer</div>`,
        `<div>Current active jobs/packets: ${{jobText}}</div>`
      ].join('');
    }}

    function renderClockPanel(current, t) {{
      const n = 36;
      const size = 320;
      const cx = size / 2;
      const cy = size / 2;
      const radius = 126;
      const points = Array.from({{ length: n }}, (_, i) => {{
        const angle = -Math.PI / 2 + 2 * Math.PI * i / n;
        return {{ x: cx + radius * Math.cos(angle), y: cy + radius * Math.sin(angle) }};
      }});
      const pathSlots = current.ticks.map((slot, i) => ({{
        spread: Number(slot.spread_epoch),
        kind: slot.kind || 'active',
        index: i,
        between_ticks: slot.between_ticks || []
      }}));
      const seen = new Map();
      for (const slot of pathSlots) {{
        if (!seen.has(slot.spread)) seen.set(slot.spread, new Set());
        seen.get(slot.spread).add(slot.kind);
      }}
      const links = [];
      for (let i = 1; i < pathSlots.length; i++) {{
        const a = points[pathSlots[i - 1].spread];
        const b = points[pathSlots[i].spread];
        links.push(`<line class="clock-link ${{i === idx ? 'current' : ''}}" x1="${{a.x.toFixed(1)}}" y1="${{a.y.toFixed(1)}}" x2="${{b.x.toFixed(1)}}" y2="${{b.y.toFixed(1)}}"></line>`);
      }}
      const nodes = points.map((p, i) => {{
        const classes = ['frame-node'];
        const kinds = seen.get(i);
        if (kinds) classes.push('path');
        if (kinds && kinds.has('connector')) classes.push('connector');
        if (i === Number(t.spread_epoch)) classes.push('current');
        return `<g class="frame-g" data-frame="${{i}}"><circle class="${{classes.join(' ')}}" cx="${{p.x.toFixed(1)}}" cy="${{p.y.toFixed(1)}}" r="8"></circle><text class="frame-label" x="${{p.x.toFixed(1)}}" y="${{p.y.toFixed(1)}}">${{i}}</text></g>`;
      }});
      document.getElementById('clockPanel').innerHTML = `<svg class="clock-svg" viewBox="0 0 ${{size}} ${{size}}" role="img" aria-label="36-frame spread clock walk">${{links.join('')}}${{nodes.join('')}}</svg>`;
      document.querySelectorAll('.frame-g').forEach(el => el.addEventListener('click', () => {{
        selectedFrame = Number(el.dataset.frame);
        render();
      }}));
      const connectorCount = pathSlots.filter(slot => slot.kind === 'connector').length;
      document.getElementById('clockMeta').textContent = `${{pathSlots.length}} slots / ${{connectorCount}} connectors`;
      renderFrameInspect(current, t, pathSlots);
    }}

    function renderList() {{
      const current = layer();
      document.getElementById('listTitle').textContent = current.label;
      document.getElementById('tickList').innerHTML = current.ticks.map((t, i) => `
        <div class="tick ${{i === idx ? 'active' : ''}}" data-idx="${{i}}">
          <strong>${{i}}</strong>
          <div><div>Spread ${{t.spread_epoch}}</div><small>${{mode === 'clock' && t.kind === 'connector' ? 'connector frame' : `${{t.dispatch_count}} ${{mode === 'coarse' ? 'packets' : 'jobs'}}, ${{t.used_site_count}} sites`}}</small></div>
          <span class="badge ${{mode !== 'coarse' || t.conflict_free ? 'ok' : 'warn'}}">${{mode !== 'coarse' || t.conflict_free ? 'clean' : 'conflict'}}</span>
        </div>
      `).join('');
      document.querySelectorAll('.tick').forEach(el => el.addEventListener('click', () => {{
        idx = Number(el.dataset.idx);
        render();
      }}));
    }}

    function render() {{
      const current = layer();
      const t = current.ticks[idx];
      slider.value = idx;
      slider.max = Math.max(0, current.ticks.length - 1);
      document.getElementById('tickLabel').textContent = `${{current.label}} ${{idx + 1}} / ${{current.ticks.length}}`;
      document.getElementById('detailTitle').textContent = `${{mode === 'clock' ? 'Clock slot' : 'Tick'}} ${{t.tick}} - Spread ${{t.spread_epoch}}`;
      const items = normalizedItems(t);
      document.getElementById('badges').innerHTML = [
        `<span class="badge ok">${{mode === 'clock' && t.kind === 'connector' ? 'connector frame' : `${{t.dispatch_count}} ${{mode === 'coarse' ? 'packets' : 'jobs'}}`}}</span>`,
        `<span class="badge ok">${{t.used_site_count}} occupied sites</span>`,
        `<span class="badge ${{mode !== 'coarse' || t.conflict_free ? 'ok' : 'warn'}}">${{mode !== 'coarse' || t.conflict_free ? 'verified' : 'conflict'}}</span>`,
        `<span class="badge ok">clock SRG(${{payload.clock.srg_parameters.join(',')}})</span>`,
        `<span class="badge ${{micro.exact_backend === 'unavailable' ? 'warn' : 'ok'}}">exact ${{micro.exact_backend}}</span>`,
        `<span class="badge ${{payload.mock.pipeline_complete ? 'ok' : 'warn'}}">mock UOR ${{payload.mock.status}}</span>`,
        `<span class="badge ${{payload.shacl.status === 'PASS' ? 'ok' : 'warn'}}">shape ${{payload.shacl.status}}</span>`
      ].join('');
      const used = new Set(items.flatMap(p => p.sites));
      document.getElementById('board').innerHTML = allSites.map(s => `<div class="site ${{used.has(s) ? 'used' : ''}}">${{s}}</div>`).join('');
      renderClockPanel(current, t);
      document.getElementById('packets').innerHTML = items.map(p => `
        <tr class="${{p.id === highlightedJob ? 'highlighted' : ''}}"><td>${{p.id}}</td><td>${{p.sites.join(' ')}}</td><td>${{p.route}}</td></tr>
      `).join('');
      renderList();
    }}
    function step(delta) {{
      const count = layer().ticks.length;
      idx = (idx + delta + count) % count;
      render();
    }}
    function setMode(nextMode) {{
      mode = nextMode;
      idx = 0;
      selectedFrame = null;
      highlightedJob = null;
      syncModeButtons();
      render();
    }}
    document.getElementById('coarseMode').onclick = () => setMode('coarse');
    document.getElementById('microMode').onclick = () => setMode('micro');
    document.getElementById('clockMode').onclick = () => setMode('clock');
    document.getElementById('nativeMode').onclick = () => setMode('native');
    document.getElementById('prev').onclick = () => step(-1);
    document.getElementById('next').onclick = () => step(1);
    document.getElementById('play').onclick = () => {{
      if (timer) {{
        clearInterval(timer); timer = null; document.getElementById('play').textContent = 'Play';
      }} else {{
        timer = setInterval(() => step(1), 900); document.getElementById('play').textContent = 'Pause';
      }}
    }};
    slider.oninput = e => {{ idx = Number(e.target.value); render(); }};
    applyInitialQuery();
    syncModeButtons();
    render();
  </script>
</body>
</html>
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trace", default=str(DEFAULT_TRACE))
    parser.add_argument("--mock", default=str(DEFAULT_MOCK))
    parser.add_argument("--shacl", default=str(DEFAULT_SHACL))
    parser.add_argument("--compiler", default=str(DEFAULT_COMPILER))
    parser.add_argument("--clock", default=str(DEFAULT_CLOCK))
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    args = parser.parse_args(argv)

    trace = load(
        Path(args.trace) if Path(args.trace).is_absolute() else ROOT / args.trace
    )
    mock = load(Path(args.mock) if Path(args.mock).is_absolute() else ROOT / args.mock)
    shacl = load(
        Path(args.shacl) if Path(args.shacl).is_absolute() else ROOT / args.shacl
    )
    compiler = load(
        Path(args.compiler)
        if Path(args.compiler).is_absolute()
        else ROOT / args.compiler
    )
    clock = load(
        Path(args.clock) if Path(args.clock).is_absolute() else ROOT / args.clock
    )
    output = Path(args.out) if Path(args.out).is_absolute() else ROOT / args.out
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_html(trace, mock, shacl, compiler, clock), encoding="utf-8")
    print(f"wrote: {output.relative_to(ROOT)}")
    print(
        f"ticks: {trace['tick_count']} coarse / {compiler['active_schedule']['tick_count']} micro; packets: {trace['packet_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
