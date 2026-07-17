#!/usr/bin/env python3
"""Holonomy queue and interactive replay bridge for the contextuality tax scheduler.

The eighth-tax scheduler decides what to do at the first collision frontier.  This
module adds the missing queue layer:

* the isolated 7-pack consumes 36288 ticks;
* the remaining slack is exactly three 5184-tick star slots;
* a mixed request burst of time-slice, serialize, escalate, hard-escalate fills
  those three slots and spills the fourth request to the next supercycle.

It also parses the existing UOR replay page and attaches real microkernel packet
hits to each scheduler center, so the exception policy is connected to the
clickable replay surface rather than only to aggregate benchmark rows.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
from typing import Any
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.w33_h4_orbital_no_go import _line_intersection_graph  # noqa: E402


OUT_JSON = ROOT / "data" / "w33_contextuality_tax_holonomy_queue.json"
OUT_HTML = ROOT / "docs" / "holonet_contextuality_tax_scheduler.html"
REPLAY_HTML = ROOT / "docs" / "holonet_uor_os_replay.html"


class ReplayDataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.capture = False
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = dict(attrs)
        if tag == "script" and attr_map.get("id") == "replay-data":
            self.capture = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self.capture:
            self.capture = False

    def handle_data(self, data: str) -> None:
        if self.capture:
            self.parts.append(data)


def _load_json(relpath: str) -> dict[str, Any]:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def _load_replay_payload(path: Path = REPLAY_HTML) -> dict[str, Any]:
    parser = ReplayDataParser()
    parser.feed(path.read_text(encoding="utf-8"))
    if not parser.parts:
        raise ValueError(f"missing replay-data script in {path}")
    return json.loads("".join(parser.parts))


def _star_lines(lines: list[tuple[int, int, int, int]]) -> dict[int, list[int]]:
    star: dict[int, list[int]] = defaultdict(list)
    for line_id, line in enumerate(lines):
        for point in line:
            star[point].append(line_id)
    return {point: sorted(line_ids) for point, line_ids in star.items()}


def _shared_lines(
    center: int, active_centers: list[int], star_lines: dict[int, list[int]]
) -> dict[int, list[int]]:
    center_lines = set(star_lines[center])
    return {
        active: sorted(center_lines & set(star_lines[active]))
        for active in active_centers
        if center_lines & set(star_lines[active])
    }


def _decision_for_shared_count(count: int, active: bool) -> str:
    if active:
        return "ACTIVE_ISOLATED"
    if count == 0:
        return "ADMIT_ISOLATED"
    if count == 1:
        return "TIME_SLICE_SHARED_LINE"
    if count == 2:
        return "SERIALIZE_WHOLE_STAR"
    return "ESCALATE_HOLONOMY"


def _replay_index(payload: dict[str, Any]) -> dict[str, Any]:
    line_hits: Counter[int] = Counter()
    packets_by_line: dict[int, set[str]] = defaultdict(set)
    jobs_by_line: dict[int, list[str]] = defaultdict(list)
    job_locations: dict[str, dict[str, int]] = {}
    for tick in payload["micro"]["ticks"]:
        for job_id in tick["jobs"]:
            job_locations[job_id] = {
                "tick": int(tick["tick"]),
                "spread_epoch": int(tick["spread_epoch"]),
            }
    for job_id, job in payload["micro"]["jobs"].items():
        line_id = int(job["line_index"])
        line_hits[line_id] += 1
        packets_by_line[line_id].add(str(job["packet_id"]))
        jobs_by_line[line_id].append(job_id)
    return {
        "line_hits": line_hits,
        "packets_by_line": packets_by_line,
        "jobs_by_line": jobs_by_line,
        "job_locations": job_locations,
    }


def _replay_link(tick: int, frame: int, job_id: str) -> str:
    return (
        "holonet_uor_os_replay.html"
        f"?mode=micro&tick={tick}&frame={frame}&job={quote(job_id, safe='')}"
    )


def _replay_hits_for_center(
    center: int,
    star_lines: dict[int, list[int]],
    replay_index: dict[str, Any],
) -> dict[str, Any]:
    line_ids = star_lines[center]
    jobs: list[str] = []
    packets: set[str] = set()
    frame_jobs: dict[tuple[int, int], list[str]] = defaultdict(list)
    line_hit_rows = []
    for line_id in line_ids:
        line_jobs = sorted(replay_index["jobs_by_line"].get(line_id, []))
        jobs.extend(line_jobs)
        packets.update(replay_index["packets_by_line"].get(line_id, set()))
        for job_id in line_jobs:
            loc = replay_index["job_locations"].get(job_id)
            if loc:
                frame_jobs[(loc["tick"], loc["spread_epoch"])].append(job_id)
        line_hit_rows.append(
            {
                "line": line_id,
                "job_count": len(line_jobs),
                "sample_jobs": line_jobs[:5],
            }
        )
    frame_hit_rows = [
        {
            "tick": tick,
            "spread_epoch": frame,
            "job_count": len(frame_row_jobs),
            "sample_jobs": sorted(frame_row_jobs)[:5],
        }
        for (tick, frame), frame_row_jobs in sorted(
            frame_jobs.items(), key=lambda item: (-len(item[1]), item[0][0], item[0][1])
        )
    ]
    primary_frame = frame_hit_rows[0] if frame_hit_rows else None
    if primary_frame:
        primary_job = primary_frame["sample_jobs"][0]
        primary_frame = {
            **primary_frame,
            "primary_job": primary_job,
            "replay_url": _replay_link(
                int(primary_frame["tick"]),
                int(primary_frame["spread_epoch"]),
                primary_job,
            ),
        }
    return {
        "line_contexts": line_ids,
        "replay_job_hits": len(jobs),
        "replay_packet_hits": len(packets),
        "sample_jobs": sorted(jobs)[:8],
        "sample_packets": sorted(packets)[:8],
        "line_hit_rows": line_hit_rows,
        "frame_hit_rows": frame_hit_rows[:6],
        "primary_replay_frame": primary_frame,
    }


def _candidate_rows(
    active_centers: list[int],
    star_lines: dict[int, list[int]],
    replay_index: dict[str, Any],
) -> list[dict[str, Any]]:
    rows = []
    for center in sorted(star_lines):
        active = center in active_centers
        shared_by_center = (
            {} if active else _shared_lines(center, active_centers, star_lines)
        )
        shared_lines = sorted(
            {line for lines in shared_by_center.values() for line in lines}
        )
        replay = _replay_hits_for_center(center, star_lines, replay_index)
        rows.append(
            {
                "center": center,
                "active": active,
                "shared_line_count": 0 if active else len(shared_lines),
                "shared_lines": [] if active else shared_lines,
                "colliding_active_centers": {
                    str(k): v for k, v in sorted(shared_by_center.items())
                },
                "decision": _decision_for_shared_count(len(shared_lines), active),
                **replay,
            }
        )
    return rows


def _queue_burst(
    scheduler: dict[str, Any],
    case_rows: dict[str, dict[str, Any]],
    *,
    slack_star_slots: int,
    star_runtime_ticks: int,
) -> dict[str, Any]:
    ordered_case_names = ["time_slice", "serialize", "escalate", "hard_escalate"]
    rows = []
    cycle = 0
    slot = 0
    for name in ordered_case_names:
        case = scheduler["eighth_tax_policy"]["cases"][name]
        if slot >= slack_star_slots:
            cycle += 1
            slot = 0
        rows.append(
            {
                "request": name,
                "center": case["center"],
                "decision": case["decision"],
                "shared_line_count": case["shared_line_count"],
                "cycle": cycle,
                "slack_slot": slot,
                "service_ticks": star_runtime_ticks,
                "spills_from_first_supercycle": cycle > 0,
                "replay_job_hits": case_rows[name]["replay_job_hits"],
                "replay_packet_hits": case_rows[name]["replay_packet_hits"],
                "primary_replay_frame": case_rows[name]["primary_replay_frame"],
            }
        )
        slot += 1

    cycle_loads: dict[int, int] = defaultdict(int)
    for row in rows:
        cycle_loads[int(row["cycle"])] += int(row["service_ticks"])
    return {
        "policy": "three 5184-tick slack slots after preserving the isolated 7-pack",
        "slack_star_slots_per_supercycle": slack_star_slots,
        "request_order": ordered_case_names,
        "rows": rows,
        "cycle_load_ticks": {str(k): v for k, v in sorted(cycle_loads.items())},
        "spilled_request_count": sum(
            1 for row in rows if row["spills_from_first_supercycle"]
        ),
    }


def _write_interactive_html(certificate: dict[str, Any], path: Path = OUT_HTML) -> None:
    compact = json.dumps(certificate, sort_keys=True, separators=(",", ":"))
    rows = certificate["candidate_policy_rows"]
    buttons = "\n".join(
        f'<button class="center-btn {row["decision"].lower()}" data-center="{row["center"]}">{row["center"]}</button>'
        for row in rows
    )
    queue_rows = "\n".join(
        "<tr>"
        f"<td>{escape(row['request'])}</td>"
        f"<td>{row['center']}</td>"
        f"<td>{escape(row['decision'])}</td>"
        f"<td>{row['cycle']}</td>"
        f"<td>{row['slack_slot']}</td>"
        f"<td><a href=\"{escape(row['primary_replay_frame']['replay_url'])}\">frame {row['primary_replay_frame']['spread_epoch']}</a></td>"
        "</tr>"
        for row in certificate["holonomy_queue"]["burst_simulation"]["rows"]
    )
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Holonet Contextuality Tax Scheduler</title>
  <style>
    :root {{ --ink:#172033; --muted:#647084; --line:#cbd5e1; --paper:#f8fafc; --panel:#fff; --blue:#2563eb; --orange:#f97316; --amber:#d97706; --red:#dc2626; --dark:#7f1d1d; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font-family:Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color:var(--ink); background:var(--paper); }}
    header {{ padding:22px clamp(18px,4vw,44px); background:#fff; border-bottom:1px solid var(--line); }}
    h1 {{ margin:0; font-size:clamp(26px,4vw,42px); letter-spacing:0; }}
    main {{ display:grid; gap:18px; padding:18px clamp(18px,4vw,44px) 42px; }}
    .grid {{ display:grid; grid-template-columns:minmax(280px,.9fr) minmax(340px,1.1fr); gap:18px; align-items:start; }}
    .panel {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:16px; }}
    .centers {{ display:grid; grid-template-columns:repeat(8,minmax(38px,1fr)); gap:8px; }}
    .center-btn {{ min-height:42px; border:1px solid #94a3b8; border-radius:8px; background:#e5e7eb; color:#111827; font-weight:750; cursor:pointer; }}
    .center-btn.active_isolated {{ background:var(--blue); color:#fff; }}
    .center-btn.time_slice_shared_line {{ background:var(--orange); color:#fff; }}
    .center-btn.serialize_whole_star {{ background:var(--amber); color:#fff; }}
    .center-btn.escalate_holonomy {{ background:var(--red); color:#fff; }}
    .center-btn.selected {{ outline:3px solid #0f172a; outline-offset:2px; }}
    .metric-grid {{ display:grid; grid-template-columns:repeat(4,minmax(120px,1fr)); gap:10px; }}
    .metric {{ border:1px solid var(--line); border-radius:8px; padding:12px; background:#fff; }}
    .label {{ color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.06em; }}
    .value {{ font-size:22px; font-weight:800; margin-top:4px; }}
    .scheduler-img {{ width:100%; display:block; border:1px solid var(--line); border-radius:8px; background:#f8fafc; }}
    table {{ width:100%; border-collapse:collapse; font-size:14px; }}
    th, td {{ padding:8px; border-bottom:1px solid #e2e8f0; text-align:left; vertical-align:top; }}
    th {{ color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.05em; }}
    code {{ background:#eef6ff; border:1px solid #bfdbfe; border-radius:4px; padding:0 4px; }}
    @media (max-width:900px) {{ .grid, .metric-grid {{ grid-template-columns:1fr; }} .centers {{ grid-template-columns:repeat(5,minmax(40px,1fr)); }} }}
  </style>
</head>
<body>
  <header>
    <h1>Holonet Contextuality Tax Scheduler</h1>
  </header>
  <main>
    <section class="metric-grid">
      <div class="metric"><div class="label">Active Pack</div><div class="value">7 stars</div></div>
      <div class="metric"><div class="label">Slack Queue</div><div class="value">3 slots</div></div>
      <div class="metric"><div class="label">Replay Packets</div><div class="value">{certificate['replay_trace_bridge']['packet_count']}</div></div>
      <div class="metric"><div class="label">Native Slots</div><div class="value">{certificate['replay_trace_bridge']['clock_native_tick_count']}</div></div>
    </section>
    <section class="grid">
      <div class="panel">
        <h2>Centers</h2>
        <div class="centers" id="centers">{buttons}</div>
      </div>
      <div class="panel">
        <h2 id="detail-title">Center</h2>
        <div id="detail"></div>
      </div>
    </section>
    <section class="grid">
      <div class="panel">
        <h2>Scheduler Panel</h2>
        <img class="scheduler-img" src="holonet_contextuality_tax_scheduler.svg" alt="Contextuality tax scheduler panel">
      </div>
      <div class="panel">
        <h2>Holonomy Queue Burst</h2>
        <table>
          <thead><tr><th>Request</th><th>Center</th><th>Decision</th><th>Cycle</th><th>Slot</th><th>Replay</th></tr></thead>
          <tbody>{queue_rows}</tbody>
        </table>
      </div>
    </section>
  </main>
  <script id="queue-data" type="application/json">{compact}</script>
  <script>
    const data = JSON.parse(document.getElementById('queue-data').textContent);
    const rows = new Map(data.candidate_policy_rows.map(row => [String(row.center), row]));
    const buttons = Array.from(document.querySelectorAll('.center-btn'));
    function render(center) {{
      const row = rows.get(String(center));
      buttons.forEach(btn => btn.classList.toggle('selected', btn.dataset.center === String(center)));
      document.getElementById('detail-title').textContent = `Center ${{center}}`;
      const packets = row.sample_packets.length ? row.sample_packets.join(', ') : 'none';
      const jobs = row.sample_jobs.length ? row.sample_jobs.join(', ') : 'none';
      const primary = row.primary_replay_frame;
      const replayLink = primary
        ? `<a href="${{primary.replay_url}}">Open replay tick ${{primary.tick}}, frame ${{primary.spread_epoch}}, job ${{primary.primary_job}}</a>`
        : 'none';
      const frameRows = row.frame_hit_rows.length
        ? row.frame_hit_rows.map(frame => `<tr><td>${{frame.tick}}</td><td>${{frame.spread_epoch}}</td><td>${{frame.job_count}}</td><td>${{frame.sample_jobs.join(', ')}}</td></tr>`).join('')
        : '<tr><td colspan="4">No replay frame hits</td></tr>';
      document.getElementById('detail').innerHTML = `
        <table>
          <tbody>
            <tr><th>Decision</th><td><code>${{row.decision}}</code></td></tr>
            <tr><th>Shared lines</th><td>${{row.shared_lines.length ? row.shared_lines.join(', ') : 'none'}}</td></tr>
            <tr><th>Replay hits</th><td>${{row.replay_job_hits}} micro-jobs across ${{row.replay_packet_hits}} packets</td></tr>
            <tr><th>Replay link</th><td>${{replayLink}}</td></tr>
            <tr><th>Sample packets</th><td>${{packets}}</td></tr>
            <tr><th>Sample jobs</th><td>${{jobs}}</td></tr>
          </tbody>
        </table>
        <h3>Replay Frames</h3>
        <table>
          <thead><tr><th>Tick</th><th>Frame</th><th>Jobs</th><th>Sample</th></tr></thead>
          <tbody>${{frameRows}}</tbody>
        </table>`;
    }}
    buttons.forEach(btn => btn.addEventListener('click', () => render(btn.dataset.center)));
    render('3');
  </script>
</body>
</html>
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")


def build_certificate() -> dict[str, Any]:
    scheduler = _load_json("data/w33_contextuality_tax_scheduler.json")
    packing = _load_json("data/w33_contextuality_tax_packing_law.json")
    replay = _load_replay_payload()
    lines, _line_adjacency = _line_intersection_graph()
    star_lines = _star_lines(lines)
    replay_index = _replay_index(replay)
    active_centers = scheduler["active_isolated_pack"]["centers"]
    candidate_rows = _candidate_rows(active_centers, star_lines, replay_index)

    star_ticks = scheduler["active_isolated_pack"]["single_star_ticks"]
    active_ticks = scheduler["active_isolated_pack"]["runtime_ticks"]
    supercycle_ticks = 51_840
    slack_star_slots = packing["packing_capacity"]["capacity_shortfall_star_reserves"]
    case_rows = {
        name: next(
            row
            for row in candidate_rows
            if row["center"] == scheduler["eighth_tax_policy"]["cases"][name]["center"]
        )
        for name in ["time_slice", "serialize", "escalate", "hard_escalate"]
    }
    burst = _queue_burst(
        scheduler,
        case_rows,
        slack_star_slots=slack_star_slots,
        star_runtime_ticks=star_ticks,
    )

    replay_summary = {
        "source": "docs/holonet_uor_os_replay.html",
        "packet_count": replay["trace"]["packet_count"],
        "os_tick_count": replay["trace"]["tick_count"],
        "micro_tick_count": replay["micro"]["tick_count"],
        "micro_job_count": len(replay["micro"]["jobs"]),
        "clock_native_tick_count": replay["clock_native"]["tick_count"],
        "clock_native_connector_count": replay["clock_native"]["connector_slot_count"],
        "case_replay_hits": {
            name: {
                "center": row["center"],
                "decision": row["decision"],
                "replay_job_hits": row["replay_job_hits"],
                "replay_packet_hits": row["replay_packet_hits"],
                "sample_jobs": row["sample_jobs"],
                "primary_replay_frame": row["primary_replay_frame"],
                "frame_hit_rows": row["frame_hit_rows"],
            }
            for name, row in case_rows.items()
        },
    }

    cycle0_load = active_ticks + int(burst["cycle_load_ticks"]["0"])
    cycle1_load = int(burst["cycle_load_ticks"]["1"])
    checks = {
        "source_scheduler_verified": scheduler["verified"] is True,
        "source_packing_verified": packing["verified"] is True,
        "replay_payload_loaded": replay_summary["packet_count"] == 33
        and replay_summary["micro_tick_count"] == 14
        and replay_summary["clock_native_tick_count"] == 15,
        "slack_queue_has_three_star_slots": slack_star_slots == 3,
        "cycle0_fills_supercycle_exactly": cycle0_load == supercycle_ticks,
        "fourth_request_spills_to_cycle1": burst["spilled_request_count"] == 1
        and burst["rows"][-1]["cycle"] == 1,
        "cycle1_load_is_one_star": cycle1_load == star_ticks,
        "time_slice_replay_hits_are_real": case_rows["time_slice"]["replay_job_hits"]
        == 14
        and case_rows["time_slice"]["replay_packet_hits"] == 12,
        "serialize_replay_hits_are_real": case_rows["serialize"]["replay_job_hits"]
        == 2
        and case_rows["serialize"]["replay_packet_hits"] == 2,
        "escalate_replay_hits_are_real": case_rows["escalate"]["replay_job_hits"]
        == 5
        and case_rows["escalate"]["replay_packet_hits"] == 4,
        "hard_escalate_replay_hits_are_real": case_rows["hard_escalate"][
            "replay_job_hits"
        ]
        == 15
        and case_rows["hard_escalate"]["replay_packet_hits"] == 12,
    }

    return {
        "theorem": "W33 contextuality tax holonomy queue and replay bridge",
        "verified": all(checks.values()),
        "breakthrough": (
            "The unresolved holonomy escalation is now a bounded queue interface. "
            "After preserving the seven isolated point-star reserves, the remaining "
            "supercycle slack is exactly three 5184-tick star slots. A four-request "
            "burst fills cycle 0 and spills only the fourth request to cycle 1, and "
            "each scheduler decision is tied to real UOR replay micro-jobs."
        ),
        "source_certificates": [
            "data/w33_contextuality_tax_scheduler.json",
            "data/w33_contextuality_tax_packing_law.json",
            "docs/holonet_uor_os_replay.html",
        ],
        "outputs": {
            "json": "data/w33_contextuality_tax_holonomy_queue.json",
            "html": "docs/holonet_contextuality_tax_scheduler.html",
        },
        "holonomy_queue": {
            "active_pack_ticks": active_ticks,
            "single_star_ticks": star_ticks,
            "supercycle_ticks": supercycle_ticks,
            "slack_star_slots": slack_star_slots,
            "slack_ticks": slack_star_slots * star_ticks,
            "burst_simulation": burst,
            "cycle0_total_ticks_with_active_pack": cycle0_load,
            "cycle1_total_ticks": cycle1_load,
        },
        "replay_trace_bridge": replay_summary,
        "candidate_policy_rows": candidate_rows,
        "checks": checks,
        "claim_boundary": [
            "This is a bounded queue interface, not a solved holonomy transport law.",
            "Replay hits are parsed from the generated UOR replay page, not physical measurements.",
            "The interactive HTML is an inspection surface over point ids and replay jobs, not a chip layout.",
        ],
    }


def main() -> int:
    cert = build_certificate()
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _write_interactive_html(cert, OUT_HTML)
    print(cert["theorem"])
    print(f"  verified: {cert['verified']}")
    print("  queue: 3 slack star slots, fourth burst request spills to cycle 1")
    print("  replay: parsed docs/holonet_uor_os_replay.html")
    print(f"  wrote {OUT_JSON}")
    print(f"  wrote {OUT_HTML}")
    return 0 if cert["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
