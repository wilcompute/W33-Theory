#!/usr/bin/env python3
"""No-extra-sensor Holonet side-channel suite.

This script asks: what can this classical machine observe about a Holonet-coded workload without
adding lab sensors? It reports every built-in channel it can reach: wall/process time, resource usage,
Linux /proc jiffies, CPU frequency, thermal zones, RAPL energy if exposed, and perf counters if the
host permits `perf stat`.

The result is not photon readout. It is a map of the classical interface shadows a machine can expose
while acting as a control/readout surface for a real substrate.
"""

from __future__ import annotations

import glob
import json
import os
import resource
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import holonet_node as hn  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DOCS = ROOT / "docs"


def read_int(path):
    try:
        return int(Path(path).read_text().strip())
    except Exception:
        return None


def proc_stat_total():
    try:
        vals = Path("/proc/stat").read_text().splitlines()[0].split()[1:]
        return sum(int(v) for v in vals)
    except Exception:
        return None


def snapshot():
    usage = resource.getrusage(resource.RUSAGE_SELF)
    rapl = {
        p: v
        for p in glob.glob("/sys/class/powercap/intel-rapl*/energy_uj")
        if (v := read_int(p)) is not None
    }
    thermal = {
        p: v
        for p in glob.glob("/sys/class/thermal/thermal_zone*/temp")
        if (v := read_int(p)) is not None
    }
    freq = {
        p: v
        for p in glob.glob("/sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq")[:16]
        if (v := read_int(p)) is not None
    }
    return {
        "wall_ns": time.perf_counter_ns(),
        "process_ns": time.process_time_ns(),
        "ru_utime_s": usage.ru_utime,
        "ru_stime_s": usage.ru_stime,
        "ru_maxrss_kb": usage.ru_maxrss,
        "ru_nvcsw": usage.ru_nvcsw,
        "ru_nivcsw": usage.ru_nivcsw,
        "proc_stat_total_jiffies": proc_stat_total(),
        "rapl_energy_uj": rapl,
        "thermal_millic": thermal,
        "cpu_freq_khz": freq,
    }


def delta(before, after):
    out = {}
    scalar_keys = [
        "wall_ns",
        "process_ns",
        "ru_utime_s",
        "ru_stime_s",
        "ru_maxrss_kb",
        "ru_nvcsw",
        "ru_nivcsw",
        "proc_stat_total_jiffies",
    ]
    for k in scalar_keys:
        if before.get(k) is not None and after.get(k) is not None:
            out[k] = after[k] - before[k]
    for k in ["rapl_energy_uj", "thermal_millic", "cpu_freq_khz"]:
        b = before.get(k, {})
        a = after.get(k, {})
        out[k] = {p: a[p] - b[p] for p in b if p in a}
    return out


def route_workload(rounds):
    acc = 0
    pts = hn.POINTS
    for _ in range(rounds):
        for a in pts:
            for b in pts:
                acc += hn.symplectic(a, b)
    return acc


def rule110_workload(rounds):
    state = [
        1 if i in {1, 2, 3, 6, 7, 11, 18, 27, 28, 31, 36} else 0 for i in range(40)
    ]
    table = {
        (1, 1, 1): 0,
        (1, 1, 0): 1,
        (1, 0, 1): 1,
        (1, 0, 0): 0,
        (0, 1, 1): 1,
        (0, 1, 0): 1,
        (0, 0, 1): 1,
        (0, 0, 0): 0,
    }
    acc = 0
    for _ in range(rounds):
        state = [
            table[(state[(i - 1) % 40], state[i], state[(i + 1) % 40])]
            for i in range(40)
        ]
        acc += sum(state)
    return acc


def cache_conflict_workload(rounds):
    arr = bytearray(2 * 1024 * 1024)
    acc = 0
    stride = 4096
    for _ in range(rounds):
        for i in range(0, len(arr), stride):
            arr[i] = (arr[i] + 1) & 0xFF
            acc += arr[i]
    return acc


def measure(name, fn, *args):
    before = snapshot()
    acc = fn(*args)
    after = snapshot()
    return {"name": name, "accumulator": acc, "delta": delta(before, after)}


def perf_available():
    if shutil.which("perf") is None:
        return {"available": False, "reason": "perf command not found"}
    code = "x=0\nfor i in range(500000): x += (i*i) % 3\nprint(x)\n"
    try:
        proc = subprocess.run(
            [
                "perf",
                "stat",
                "-x,",
                "-e",
                "task-clock,cycles,instructions,cache-references,cache-misses",
                sys.executable,
                "-c",
                code,
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=8,
            check=False,
        )
    except Exception as exc:
        return {"available": False, "reason": repr(exc)}
    return {
        "available": proc.returncode == 0,
        "returncode": proc.returncode,
        "stdout_tail": proc.stdout.strip().splitlines()[-3:],
        "stderr": proc.stderr.strip().splitlines()[:20],
    }


def summarize_channels(rows):
    sample = snapshot()
    channels = {
        "wall_time": True,
        "process_time": True,
        "resource_usage": True,
        "proc_stat": sample["proc_stat_total_jiffies"] is not None,
        "rapl_energy": bool(sample["rapl_energy_uj"]),
        "thermal": bool(sample["thermal_millic"]),
        "cpu_frequency": bool(sample["cpu_freq_khz"]),
        "perf_counters": None,
    }
    sensitivities = {}
    for row in rows:
        d = row["delta"]
        sensitivities[row["name"]] = {
            "wall_ms": d.get("wall_ns", 0) / 1e6,
            "process_ms": d.get("process_ns", 0) / 1e6,
            "rapl_channels": len(d.get("rapl_energy_uj", {})),
            "thermal_channels": len(d.get("thermal_millic", {})),
            "freq_channels": len(d.get("cpu_freq_khz", {})),
        }
    return channels, sensitivities


def write_markdown(payload):
    lines = []
    lines.append("# Holonet No-Extra-Sensor Side-Channel Report\n\n")
    lines.append(
        "This report lists what this machine can observe about route-coded workloads without adding lab sensors.\n\n"
    )
    lines.append("## Available Channels\n\n")
    for k, v in payload["channels"].items():
        lines.append(f"- {k}: {v}\n")
    lines.append("\n## Workload Sensitivities\n\n")
    for name, row in payload["sensitivities"].items():
        lines.append(
            f"- {name}: wall {row['wall_ms']:.3f} ms, process {row['process_ms']:.3f} ms, RAPL {row['rapl_channels']}, thermal {row['thermal_channels']}, freq {row['freq_channels']}.\n"
        )
    lines.append("\n## Boundary\n\n")
    lines.append(payload["boundary"] + "\n")
    (DOCS / "holonet_sidechannel_report.md").write_text(
        "".join(lines), encoding="utf-8"
    )


def main():
    DATA.mkdir(exist_ok=True)
    DOCS.mkdir(exist_ok=True)
    rows = [
        measure("idle_sleep", lambda s: (time.sleep(s), 0)[1], 0.15),
        measure("route_low", route_workload, 300),
        measure("route_high", route_workload, 3000),
        measure("rule110", rule110_workload, 20000),
        measure("cache_conflict", cache_conflict_workload, 160),
    ]
    perf = perf_available()
    channels, sensitivities = summarize_channels(rows)
    channels["perf_counters"] = perf["available"]
    payload = {
        "channels": channels,
        "sensitivities": sensitivities,
        "rows": rows,
        "perf": perf,
        "boundary": (
            "These are host self-observables, not quantum measurements. They can demonstrate that "
            "route-coded VM workloads create measurable classical shadows and can drive a coupler; "
            "they do not certify photon/electron state without a physical substrate and detector."
        ),
    }
    (DATA / "holonet_sidechannel_suite.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )
    write_markdown(payload)

    print("HOLONET SIDE-CHANNEL SUITE")
    print("--------------------------")
    print("available channels:")
    for k, v in channels.items():
        print(f"  {k}: {v}")
    print("workloads:")
    for name, row in sensitivities.items():
        print(
            f"  {name}: wall={row['wall_ms']:.3f}ms process={row['process_ms']:.3f}ms "
            f"rapl={row['rapl_channels']} thermal={row['thermal_channels']} freq={row['freq_channels']}"
        )
    print(f"perf: {perf.get('available')} {perf.get('reason', '')}")
    print("boundary: " + payload["boundary"])
    print("wrote data/holonet_sidechannel_suite.json")
    print("wrote docs/holonet_sidechannel_report.md")


if __name__ == "__main__":
    main()
