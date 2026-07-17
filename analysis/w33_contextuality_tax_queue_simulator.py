#!/usr/bin/env python3
"""Runtime simulator and falsifier gate for the contextuality-tax queue.

The holonomy queue certificate proves a three-slot slack queue after the
isolated 7-star pack.  This module turns that static burst into a variable
arrival simulator and records the first falsifier that would distinguish a
mere bounded queue from an actual solved holonomy transport law.
"""

from __future__ import annotations

from collections import defaultdict, deque
from html import escape
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_contextuality_tax_holonomy_queue import (  # noqa: E402
    build_certificate as build_queue_certificate,
)


OUT_JSON = ROOT / "data" / "w33_contextuality_tax_queue_simulator.json"
OUT_HTML = ROOT / "docs" / "holonet_contextuality_tax_queue_simulator.html"
QUEUE_JSON = ROOT / "data" / "w33_contextuality_tax_holonomy_queue.json"
SCHEDULER_JSON = ROOT / "data" / "w33_contextuality_tax_scheduler.json"

CASE_ORDER = ("time_slice", "serialize", "escalate", "hard_escalate")

SCENARIOS: dict[str, list[tuple[int, str]]] = {
    "four_request_burst": [
        (0, "time_slice"),
        (0, "serialize"),
        (0, "escalate"),
        (0, "hard_escalate"),
    ],
    "six_request_launch": [
        (0, "time_slice"),
        (0, "serialize"),
        (0, "escalate"),
        (0, "hard_escalate"),
        (0, "escalate"),
        (0, "serialize"),
    ],
    "steady_three_per_cycle": [
        (0, "time_slice"),
        (0, "serialize"),
        (0, "escalate"),
        (1, "hard_escalate"),
        (1, "time_slice"),
        (1, "serialize"),
        (2, "escalate"),
        (2, "hard_escalate"),
        (2, "time_slice"),
    ],
    "lumpy_backlog": [
        (0, "time_slice"),
        (0, "serialize"),
        (1, "hard_escalate"),
        (1, "hard_escalate"),
        (1, "escalate"),
        (1, "serialize"),
        (1, "time_slice"),
        (2, "time_slice"),
    ],
}


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _queue_certificate() -> dict[str, Any]:
    if QUEUE_JSON.exists():
        data = _load_json(QUEUE_JSON)
        if data.get("verified") is True and "primary_replay_frame" in data[
            "replay_trace_bridge"
        ]["case_replay_hits"]["time_slice"]:
            return data
    return build_queue_certificate()


def _request_library(
    queue: dict[str, Any], scheduler: dict[str, Any]
) -> dict[str, dict[str, Any]]:
    cases = queue["replay_trace_bridge"]["case_replay_hits"]
    scheduler_cases = scheduler["eighth_tax_policy"]["cases"]
    return {
        name: {
            "request": name,
            "center": cases[name]["center"],
            "decision": cases[name]["decision"],
            "shared_line_count": scheduler_cases[name]["shared_line_count"],
            "shared_lines": scheduler_cases[name]["shared_lines"],
            "localized_policy_ticks": scheduler_cases[name]["localized_collision_ticks"],
            "queue_slot_ticks": queue["holonomy_queue"]["single_star_ticks"],
            "replay_job_hits": cases[name]["replay_job_hits"],
            "replay_packet_hits": cases[name]["replay_packet_hits"],
            "primary_replay_frame": cases[name]["primary_replay_frame"],
        }
        for name in CASE_ORDER
    }


def _materialize_requests(
    scenario_name: str,
    arrivals: list[tuple[int, str]],
    library: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    requests = []
    for ordinal, (arrival_cycle, request_name) in enumerate(arrivals):
        template = library[request_name]
        requests.append(
            {
                "id": f"{scenario_name}:{ordinal:02d}:{request_name}",
                "arrival_cycle": arrival_cycle,
                **template,
            }
        )
    return requests


def _avg(values: list[int]) -> int:
    return sum(values) // len(values) if values else 0


def _simulate_scenario(
    scenario_name: str,
    arrivals: list[tuple[int, str]],
    queue: dict[str, Any],
    library: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    active_ticks = queue["holonomy_queue"]["active_pack_ticks"]
    slot_ticks = queue["holonomy_queue"]["single_star_ticks"]
    supercycle_ticks = queue["holonomy_queue"]["supercycle_ticks"]
    slots_per_cycle = queue["holonomy_queue"]["slack_star_slots"]

    requests = _materialize_requests(scenario_name, arrivals, library)
    future = defaultdict(list)
    for request in requests:
        future[int(request["arrival_cycle"])].append(request)

    pending: deque[dict[str, Any]] = deque()
    service_rows: list[dict[str, Any]] = []
    cycle_rows: list[dict[str, Any]] = []
    cycle = 0
    while len(service_rows) < len(requests):
        arrivals_now = future.get(cycle, [])
        pending.extend(arrivals_now)
        queue_before = len(pending)
        served_this_cycle = []
        for slot in range(slots_per_cycle):
            if not pending:
                break
            request = pending.popleft()
            start_tick = cycle * supercycle_ticks + active_ticks + slot * slot_ticks
            completion_tick = start_tick + slot_ticks
            wait_cycles = cycle - int(request["arrival_cycle"])
            row = {
                **request,
                "service_cycle": cycle,
                "slack_slot": slot,
                "wait_cycles": wait_cycles,
                "start_tick": start_tick,
                "completion_tick": completion_tick,
                "latency_ticks_from_arrival_cycle": wait_cycles * supercycle_ticks
                + active_ticks
                + (slot + 1) * slot_ticks,
                "spilled": wait_cycles > 0,
            }
            service_rows.append(row)
            served_this_cycle.append(row)
        service_load = len(served_this_cycle) * slot_ticks
        cycle_rows.append(
            {
                "cycle": cycle,
                "arrivals": len(arrivals_now),
                "queue_before_service": queue_before,
                "served": len(served_this_cycle),
                "service_load_ticks": service_load,
                "total_cycle_ticks_with_active_pack": active_ticks + service_load
                if served_this_cycle or queue_before
                else 0,
                "backlog_after_service": len(pending),
                "served_request_ids": [row["id"] for row in served_this_cycle],
            }
        )
        cycle += 1

    service_class_stats = {}
    for request_name in CASE_ORDER:
        rows = [row for row in service_rows if row["request"] == request_name]
        service_class_stats[request_name] = {
            "count": len(rows),
            "avg_latency_ticks": _avg(
                [int(row["latency_ticks_from_arrival_cycle"]) for row in rows]
            ),
            "max_wait_cycles": max((int(row["wait_cycles"]) for row in rows), default=0),
            "spilled_count": sum(1 for row in rows if row["spilled"]),
        }

    latency_values = [int(row["latency_ticks_from_arrival_cycle"]) for row in service_rows]
    return {
        "name": scenario_name,
        "description": {
            "four_request_burst": "The original mixed burst: three requests fit in cycle 0 and the fourth spills.",
            "six_request_launch": "A launch spike that shows two full queue cycles under heavy mixed pressure.",
            "steady_three_per_cycle": "A saturated but stable arrival pattern with no backlog growth.",
            "lumpy_backlog": "A realistic burst after a quiet cycle; prior spill consumes the next cycle's first slots.",
        }[scenario_name],
        "requests": requests,
        "cycle_rows": cycle_rows,
        "service_rows": service_rows,
        "service_class_stats": service_class_stats,
        "summary": {
            "request_count": len(requests),
            "spilled_request_count": sum(1 for row in service_rows if row["spilled"]),
            "max_wait_cycles": max((int(row["wait_cycles"]) for row in service_rows), default=0),
            "avg_latency_ticks": _avg(latency_values),
            "max_latency_ticks": max(latency_values) if latency_values else 0,
            "completion_cycle_count": cycle,
        },
    }


def _build_transport_falsifier(queue: dict[str, Any]) -> dict[str, Any]:
    cases = queue["replay_trace_bridge"]["case_replay_hits"]
    hard = cases["hard_escalate"]
    escalate = cases["escalate"]
    return {
        "verdict": "bounded_queue_only_until_transport_certificate_exists",
        "first_measurable_condition": (
            "A solved holonomy transport claim must reduce a three/four-shared-line "
            "escalation below one full 5184-tick star slot while preserving replay "
            "coverage and supplying a phase-consistent transport signature."
        ),
        "current_observation": {
            "hard_escalate_center": hard["center"],
            "hard_escalate_shared_line_count": 4,
            "current_service_ticks": queue["holonomy_queue"]["single_star_ticks"],
            "current_replay_packet_hits": hard["replay_packet_hits"],
            "current_primary_replay_frame": hard["primary_replay_frame"],
            "escalate_primary_replay_frame": escalate["primary_replay_frame"],
        },
        "solved_transport_gate": {
            "max_allowed_transport_ticks": 2592,
            "min_packet_coverage": hard["replay_packet_hits"],
            "required_shared_line_count": 4,
            "requires_phase_signature": True,
            "requires_no_extra_cycle_slot": True,
        },
        "falsification_rows": [
            {
                "measurement": "hard escalation latency",
                "bounded_queue_prediction": "5184 tick star slot and possible cycle spill",
                "solved_transport_requirement": "<=2592 ticks with no queued star slot",
                "current_status": "not_observed",
            },
            {
                "measurement": "packet coverage",
                "bounded_queue_prediction": f"{hard['replay_packet_hits']} replay packets remain attached to the queued star",
                "solved_transport_requirement": f">={hard['replay_packet_hits']} packets remain covered after compression",
                "current_status": "ready_to_test",
            },
            {
                "measurement": "phase-consistent transport signature",
                "bounded_queue_prediction": "not required by the queue model",
                "solved_transport_requirement": "non-null signature across all four shared lines",
                "current_status": "not_observed",
            },
        ],
        "claim_boundary": (
            "This falsifier defines the next measurement gate. It does not claim "
            "that holonomy transport is solved in the current replay."
        ),
    }


def build_certificate() -> dict[str, Any]:
    queue = _queue_certificate()
    scheduler = _load_json(SCHEDULER_JSON)
    library = _request_library(queue, scheduler)
    scenarios = {
        name: _simulate_scenario(name, arrivals, queue, library)
        for name, arrivals in SCENARIOS.items()
    }
    falsifier = _build_transport_falsifier(queue)
    checks = {
        "source_queue_verified": queue["verified"] is True,
        "four_request_spills_one": scenarios["four_request_burst"]["summary"][
            "spilled_request_count"
        ]
        == 1,
        "six_request_launch_uses_two_cycles": scenarios["six_request_launch"][
            "summary"
        ]["completion_cycle_count"]
        == 2,
        "steady_three_has_no_spill": scenarios["steady_three_per_cycle"]["summary"][
            "spilled_request_count"
        ]
        == 0,
        "falsifier_requires_latency_compression": falsifier["solved_transport_gate"][
            "max_allowed_transport_ticks"
        ]
        == 2592,
        "demo_links_exist": all(
            "mode=micro" in library[name]["primary_replay_frame"]["replay_url"]
            for name in CASE_ORDER
        ),
    }
    return {
        "theorem": "W33 contextuality tax queue simulator and transport falsifier",
        "verified": all(checks.values()),
        "breakthrough": (
            "The bounded holonomy queue is now a runtime simulator: variable "
            "arrival bursts produce deterministic cycle spill charts and "
            "service-class latency, and the next architecture claim has a "
            "measurable falsifier instead of an informal transport promise."
        ),
        "source_certificates": [
            "data/w33_contextuality_tax_holonomy_queue.json",
            "data/w33_contextuality_tax_scheduler.json",
        ],
        "outputs": {
            "json": "data/w33_contextuality_tax_queue_simulator.json",
            "html": "docs/holonet_contextuality_tax_queue_simulator.html",
        },
        "queue_constants": {
            "active_pack_ticks": queue["holonomy_queue"]["active_pack_ticks"],
            "single_star_ticks": queue["holonomy_queue"]["single_star_ticks"],
            "slack_star_slots": queue["holonomy_queue"]["slack_star_slots"],
            "supercycle_ticks": queue["holonomy_queue"]["supercycle_ticks"],
        },
        "request_library": library,
        "scenarios": scenarios,
        "transport_falsifier": falsifier,
        "checks": checks,
        "claim_boundary": [
            "The simulator is deterministic queue accounting over existing certificates, not a hardware runtime.",
            "The falsifier is a future measurement gate, not evidence that transport compression has been achieved.",
            "Replay links identify current microkernel frames/jobs; they are not physical detector shots.",
        ],
    }


def _scenario_button(name: str, active: bool = False) -> str:
    label = name.replace("_", " ")
    cls = "scenario-btn active" if active else "scenario-btn"
    return f'<button class="{cls}" data-scenario="{escape(name)}">{escape(label)}</button>'


def _write_html(certificate: dict[str, Any], path: Path = OUT_HTML) -> None:
    compact = json.dumps(certificate, sort_keys=True, separators=(",", ":"))
    buttons = "\n".join(
        _scenario_button(name, active=i == 0)
        for i, name in enumerate(certificate["scenarios"])
    )
    gate = certificate["transport_falsifier"]["solved_transport_gate"]
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Holonet Queue Simulator</title>
  <style>
    :root {{ --ink:#172033; --muted:#647084; --line:#cbd5e1; --paper:#f8fafc; --panel:#fff; --accent:#0f766e; --warn:#b45309; --hot:#dc2626; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font-family:Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color:var(--ink); background:var(--paper); }}
    header {{ padding:22px clamp(18px,4vw,44px); background:#fff; border-bottom:1px solid var(--line); }}
    h1 {{ margin:0; font-size:clamp(26px,4vw,42px); letter-spacing:0; }}
    main {{ display:grid; gap:18px; padding:18px clamp(18px,4vw,44px) 42px; }}
    .panel {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:16px; }}
    .grid {{ display:grid; grid-template-columns:repeat(3,minmax(180px,1fr)); gap:12px; }}
    .toolbar {{ display:flex; flex-wrap:wrap; gap:8px; }}
    button {{ min-height:36px; border:1px solid #94a3b8; border-radius:7px; background:#fff; color:var(--ink); font-weight:700; padding:0 12px; cursor:pointer; }}
    button.active {{ color:#fff; background:var(--accent); border-color:var(--accent); }}
    .metric {{ border:1px solid var(--line); border-radius:8px; padding:12px; background:#fff; }}
    .label {{ color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.06em; }}
    .value {{ font-size:22px; font-weight:800; margin-top:4px; }}
    table {{ width:100%; border-collapse:collapse; font-size:14px; }}
    th, td {{ padding:8px; border-bottom:1px solid #e2e8f0; text-align:left; vertical-align:top; }}
    th {{ color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.05em; }}
    code {{ background:#eef6ff; border:1px solid #bfdbfe; border-radius:4px; padding:0 4px; }}
    .spill {{ color:var(--hot); font-weight:800; }}
    @media (max-width:900px) {{ .grid {{ grid-template-columns:1fr; }} }}
  </style>
</head>
<body>
  <header>
    <h1>Holonet Queue Simulator</h1>
  </header>
  <main>
    <section class="panel">
      <div class="toolbar">{buttons}</div>
    </section>
    <section class="grid" id="metrics"></section>
    <section class="panel">
      <h2 id="scenario-title"></h2>
      <p id="scenario-description"></p>
      <h3>Cycle Spill Chart</h3>
      <table>
        <thead><tr><th>Cycle</th><th>Arrivals</th><th>Before</th><th>Served</th><th>Load</th><th>Backlog</th></tr></thead>
        <tbody id="cycle-rows"></tbody>
      </table>
      <h3>Service Rows</h3>
      <table>
        <thead><tr><th>ID</th><th>Class</th><th>Arrive</th><th>Serve</th><th>Slot</th><th>Latency</th><th>Replay</th></tr></thead>
        <tbody id="service-rows"></tbody>
      </table>
    </section>
    <section class="panel">
      <h2>Transport Falsifier</h2>
      <p>{escape(certificate['transport_falsifier']['first_measurable_condition'])}</p>
      <p>Gate: hard escalation must compress to <code>&lt;={gate['max_allowed_transport_ticks']}</code> ticks, preserve at least <code>{gate['min_packet_coverage']}</code> packets, provide a phase signature, and consume no extra queue slot.</p>
      <table>
        <thead><tr><th>Measurement</th><th>Queue Prediction</th><th>Transport Requirement</th><th>Status</th></tr></thead>
        <tbody>
          {''.join('<tr><td>'+escape(row['measurement'])+'</td><td>'+escape(row['bounded_queue_prediction'])+'</td><td>'+escape(row['solved_transport_requirement'])+'</td><td>'+escape(row['current_status'])+'</td></tr>' for row in certificate['transport_falsifier']['falsification_rows'])}
        </tbody>
      </table>
    </section>
  </main>
  <script id="sim-data" type="application/json">{compact}</script>
  <script>
    const data = JSON.parse(document.getElementById('sim-data').textContent);
    const buttons = Array.from(document.querySelectorAll('.scenario-btn'));
    function metric(label, value) {{
      return `<div class="metric"><div class="label">${{label}}</div><div class="value">${{value}}</div></div>`;
    }}
    function render(name) {{
      const scenario = data.scenarios[name];
      buttons.forEach(btn => btn.classList.toggle('active', btn.dataset.scenario === name));
      document.getElementById('scenario-title').textContent = name.replaceAll('_', ' ');
      document.getElementById('scenario-description').textContent = scenario.description;
      document.getElementById('metrics').innerHTML = [
        metric('Requests', scenario.summary.request_count),
        metric('Spills', scenario.summary.spilled_request_count),
        metric('Max Wait', `${{scenario.summary.max_wait_cycles}} cycles`),
        metric('Avg Latency', scenario.summary.avg_latency_ticks),
        metric('Max Latency', scenario.summary.max_latency_ticks),
        metric('Completion Cycles', scenario.summary.completion_cycle_count)
      ].join('');
      document.getElementById('cycle-rows').innerHTML = scenario.cycle_rows.map(row => `
        <tr><td>${{row.cycle}}</td><td>${{row.arrivals}}</td><td>${{row.queue_before_service}}</td><td>${{row.served}}</td><td>${{row.service_load_ticks}}</td><td>${{row.backlog_after_service}}</td></tr>
      `).join('');
      document.getElementById('service-rows').innerHTML = scenario.service_rows.map(row => {{
        const cls = row.spilled ? 'spill' : '';
        const replay = row.primary_replay_frame ? `<a href="${{row.primary_replay_frame.replay_url}}">frame ${{row.primary_replay_frame.spread_epoch}}</a>` : 'none';
        return `<tr><td>${{row.id}}</td><td>${{row.request}}</td><td>${{row.arrival_cycle}}</td><td>${{row.service_cycle}}</td><td>${{row.slack_slot}}</td><td class="${{cls}}">${{row.latency_ticks_from_arrival_cycle}}</td><td>${{replay}}</td></tr>`;
      }}).join('');
    }}
    buttons.forEach(btn => btn.addEventListener('click', () => render(btn.dataset.scenario)));
    render('four_request_burst');
  </script>
</body>
</html>
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")


def main() -> int:
    certificate = build_certificate()
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(
        json.dumps(certificate, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _write_html(certificate, OUT_HTML)
    print(certificate["theorem"])
    print(f"  verified: {certificate['verified']}")
    print("  simulator: 4 variable burst scenarios")
    print("  falsifier: hard escalation must compress below one star slot")
    print(f"  wrote {OUT_JSON}")
    print(f"  wrote {OUT_HTML}")
    return 0 if certificate["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
