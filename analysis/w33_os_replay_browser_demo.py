#!/usr/bin/env python3
"""Static browser replay for the W(3,3) OS-port demo.

The JSON witnesses are precise but not presentation-friendly.  This generator
builds a self-contained HTML page that lets a reader click through the terminal
session: keyboard command, disk object load, VM execution, and serial output.
Each selected event shows its W33 endpoint, transfer class, route, line buses,
and payload-page count.
"""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any

from w33_interactive_os_port_demo import build_payload as build_os_payload
from w33_stack_bytecode_adapter import build_payload as build_stack_payload
from w33_uor_runtime_model import ROOT


DEFAULT_JSON = ROOT / "data" / "w33_os_replay_browser_demo.json"
DEFAULT_HTML = ROOT / "docs" / "w33_os_replay_browser_demo.html"


def build_payload() -> dict[str, Any]:
    os_payload = build_os_payload()
    stack_payload = build_stack_payload()
    events = [
        {
            "tick": event["tick"],
            "title": f"{event['actor']} / {event['transfer_class']}",
            "actor": event["actor"],
            "endpoint": event["endpoint"],
            "endpoint_point": event["endpoint_point"],
            "transfer_class": event["transfer_class"],
            "direction": event["direction"],
            "discipline": event["discipline"],
            "meaning": event["meaning"],
            "payload_len": event["payload_len"],
            "payload_pages": event["payload_pages"],
            "route": event["route"]["route"],
            "hops": event["route"]["hops"],
            "line_buses": event["route"]["line_buses"],
        }
        for event in os_payload["events"]
    ]
    checks = {
        "os_payload_passes": os_payload["status"] == "PASS" and all(os_payload["checks"].values()),
        "stack_payload_passes": stack_payload["status"] == "PASS" and all(stack_payload["checks"].values()),
        "events_nonempty": len(events) == 4,
        "all_routes_diameter_two": all(event["hops"] <= 2 for event in events),
        "terminal_result_visible": os_payload["terminal_transcript"][-1] == "sum_squares=140",
        "stack_adapter_result_visible": stack_payload["execution"]["result"] == [140],
    }
    return {
        "schema": "w33.os_replay_browser_demo.v1",
        "title": "W33 OS Replay Browser Demo",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "terminal_transcript": os_payload["terminal_transcript"],
        "events": events,
        "risc_execution": os_payload["risc_execution"],
        "stack_adapter": {
            "stack_object_bytes": stack_payload["stack_object"]["byte_len"],
            "stack_pages": stack_payload["stack_object"]["page_count"],
            "tiny_instructions": len(stack_payload["tiny_program"]),
            "dynamic_steps": stack_payload["execution"]["dynamic_steps"],
            "result": stack_payload["execution"]["result"],
        },
        "checks": checks,
        "interpretation": (
            "A browser can replay the Holonet OS session as typed W33 packets: "
            "input, object loading, VM execution, and output are one inspectable "
            "route grammar."
        ),
    }


def render_html(payload: dict[str, Any]) -> str:
    data = json.dumps(payload, separators=(",", ":")).replace("</", "<\\/")
    transcript = "\n".join(html.escape(line) for line in payload["terminal_transcript"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>W33 OS Replay Browser Demo</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f7f8fb;
      --panel: #ffffff;
      --ink: #172033;
      --muted: #5b6475;
      --line: #d9dee8;
      --blue: #235db8;
      --green: #247a45;
      --gold: #8a641b;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--ink);
    }}
    main {{
      max-width: 1120px;
      margin: 0 auto;
      padding: 28px 18px 44px;
    }}
    h1 {{ margin: 0 0 8px; font-size: clamp(1.65rem, 4vw, 2.65rem); letter-spacing: 0; }}
    p {{ color: var(--muted); line-height: 1.55; }}
    .grid {{
      display: grid;
      grid-template-columns: minmax(230px, 0.8fr) minmax(0, 1.2fr);
      gap: 16px;
      align-items: start;
    }}
    .panel {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
      box-shadow: 0 8px 24px rgba(20, 30, 50, 0.05);
    }}
    .events {{ display: grid; gap: 8px; }}
    button.event {{
      width: 100%;
      text-align: left;
      border: 1px solid var(--line);
      background: #fff;
      border-radius: 6px;
      padding: 10px 12px;
      cursor: pointer;
      color: var(--ink);
    }}
    button.event[aria-pressed="true"] {{
      border-color: var(--blue);
      outline: 2px solid rgba(35, 93, 184, 0.14);
    }}
    .tick {{ color: var(--gold); font-weight: 700; font-size: 0.8rem; }}
    .event-title {{ display: block; margin-top: 2px; font-weight: 700; }}
    .event-sub {{ display: block; margin-top: 2px; color: var(--muted); font-size: 0.84rem; }}
    .kv {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 8px;
      margin-top: 12px;
    }}
    .kv div {{
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 10px;
      min-height: 62px;
    }}
    .kv span {{ display: block; color: var(--muted); font-size: 0.78rem; }}
    .kv strong {{ display: block; margin-top: 4px; overflow-wrap: anywhere; }}
    pre {{
      margin: 10px 0 0;
      padding: 12px;
      border-radius: 6px;
      background: #101828;
      color: #e8eefc;
      overflow-x: auto;
      font-size: 0.9rem;
    }}
    .route {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-top: 12px;
      align-items: center;
    }}
    .node {{
      border: 1px solid var(--blue);
      color: var(--blue);
      padding: 6px 8px;
      border-radius: 6px;
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 0.88rem;
    }}
    .arrow {{ color: var(--muted); }}
    .summary {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
      margin: 16px 0;
    }}
    .summary div {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
    }}
    .summary span {{ display: block; color: var(--muted); font-size: 0.76rem; }}
    .summary strong {{ display: block; margin-top: 3px; color: var(--green); }}
    @media (max-width: 760px) {{
      .grid, .summary {{ grid-template-columns: 1fr; }}
      .kv {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <main>
    <h1>W33 OS Replay Browser Demo</h1>
    <p>Click through the deterministic wrapper session. The classical shell sees a command,
    a disk object, and serial output; the architecture sees typed W33 packets, routes, line
    buses, and VM execution.</p>
    <div class="summary">
      <div><span>Status</span><strong id="status"></strong></div>
      <div><span>RISC steps</span><strong id="risc"></strong></div>
      <div><span>Stack adapter</span><strong id="stack"></strong></div>
      <div><span>Result</span><strong id="result"></strong></div>
    </div>
    <div class="grid">
      <section class="panel">
        <h2>Session Events</h2>
        <div id="events" class="events"></div>
        <h2>Terminal</h2>
        <pre>{transcript}</pre>
      </section>
      <section class="panel">
        <h2 id="detail-title">Event</h2>
        <p id="detail-desc"></p>
        <div class="kv">
          <div><span>Endpoint</span><strong id="endpoint"></strong></div>
          <div><span>Transfer</span><strong id="transfer"></strong></div>
          <div><span>Payload</span><strong id="payload"></strong></div>
          <div><span>Line buses</span><strong id="buses"></strong></div>
        </div>
        <h2>W33 Route</h2>
        <div id="route" class="route"></div>
      </section>
    </div>
  </main>
  <script id="w33-os-replay-data" type="application/json">{data}</script>
  <script>
    const data = JSON.parse(document.getElementById("w33-os-replay-data").textContent);
    const eventsEl = document.getElementById("events");
    const routeEl = document.getElementById("route");
    const buttons = [];
    document.getElementById("status").textContent = data.status;
    document.getElementById("risc").textContent = `${{data.risc_execution.dynamic_steps}} routed events`;
    document.getElementById("stack").textContent = `${{data.stack_adapter.stack_object_bytes}} bytes -> ${{data.stack_adapter.tiny_instructions}} tiny ops`;
    document.getElementById("result").textContent = data.terminal_transcript[data.terminal_transcript.length - 1];
    function drawRoute(route) {{
      routeEl.innerHTML = "";
      route.forEach((node, index) => {{
        const n = document.createElement("span");
        n.className = "node";
        n.textContent = node;
        routeEl.appendChild(n);
        if (index < route.length - 1) {{
          const arrow = document.createElement("span");
          arrow.className = "arrow";
          arrow.textContent = "->";
          routeEl.appendChild(arrow);
        }}
      }});
    }}
    function selectEvent(index) {{
      const event = data.events[index];
      buttons.forEach((button, idx) => button.setAttribute("aria-pressed", idx === index ? "true" : "false"));
      document.getElementById("detail-title").textContent = `Tick ${{event.tick}}: ${{event.title}}`;
      document.getElementById("detail-desc").textContent = `${{event.meaning}}. ${{event.discipline}}.`;
      document.getElementById("endpoint").textContent = `${{event.endpoint}} @ ${{event.endpoint_point}}`;
      document.getElementById("transfer").textContent = `${{event.direction}}, ${{event.hops}} hop(s)`;
      document.getElementById("payload").textContent = `${{event.payload_len}} bytes, ${{event.payload_pages}} page(s)`;
      document.getElementById("buses").textContent = event.line_buses.length ? event.line_buses.join(", ") : "local";
      drawRoute(event.route);
    }}
    data.events.forEach((event, index) => {{
      const button = document.createElement("button");
      button.type = "button";
      button.className = "event";
      button.innerHTML = `<span class="tick">tick ${{event.tick}}</span><span class="event-title">${{event.title}}</span><span class="event-sub">${{event.meaning}}</span>`;
      button.addEventListener("click", () => selectEvent(index));
      eventsEl.appendChild(button);
      buttons.push(button);
    }});
    selectEvent(0);
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
    html_out.write_text(render_html(payload), encoding="utf-8")
    print(f"status: {payload['status']}")
    print(f"events={len(payload['events'])}, result={payload['terminal_transcript'][-1]}")
    print(f"wrote: {json_out.relative_to(ROOT)}")
    print(f"wrote: {html_out.relative_to(ROOT)}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
