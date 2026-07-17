#!/usr/bin/env python3
"""One-button Holonet VM demo launcher."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = ROOT / ".venv" / "bin" / "python"
PYTHON = str(PY if PY.exists() else Path(sys.executable))
DATA = ROOT / "data"
DOCS = ROOT / "docs"


COMMANDS = [
    ("vm_interface", [PYTHON, "analysis/holonet_vm_interface_demo.py"]),
    ("physical_stub", [PYTHON, "analysis/holonet_physical_substrate_stub.py"]),
    ("sidechannels", [PYTHON, "analysis/holonet_sidechannel_suite.py"]),
    (
        "wrapped_rule110_active_ticks",
        [
            PYTHON,
            "analysis/holonet_wrap.py",
            "--optimize",
            "active-ticks",
            "--out",
            "data/holonet_wrap_rule110_demo.json",
            "--",
            PYTHON,
            "-c",
            "s='0111011000100000001000000001100100010000'; print(sum(c=='1' for c in s)); print(s)",
        ],
    ),
    (
        "wrapped_rule110_clock_slots",
        [
            PYTHON,
            "analysis/holonet_wrap.py",
            "--optimize",
            "clock-slots",
            "--out",
            "data/holonet_wrap_rule110_demo_clock_slots.json",
            "--",
            PYTHON,
            "-c",
            "s='0111011000100000001000000001100100010000'; print(sum(c=='1' for c in s)); print(s)",
        ],
    ),
]


def run_one(name, cmd):
    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    path = DATA / f"holonet_demo_launcher_{name}.txt"
    path.write_text(proc.stdout, encoding="utf-8")
    return {
        "name": name,
        "cmd": cmd,
        "returncode": proc.returncode,
        "transcript": str(path.relative_to(ROOT)),
        "tail": proc.stdout.strip().splitlines()[-12:],
    }


def write_markdown(rows, ok):
    lines = ["# Holonet VM Demo Launcher Report\n\n"]
    lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}\n\n")
    lines.append(f"Overall: {'PASS' if ok else 'FAIL'}\n\n")
    lines.append("## Open These\n\n")
    lines.append("- `docs/holonet_vm_live_demo.html`\n")
    lines.append("- `docs/holonet_physical_substrate_stub.svg`\n")
    lines.append("- `docs/holonet_sidechannel_report.md`\n")
    lines.append("- `docs/holonet_vm_demo_and_interface_frontier.md`\n\n")
    lines.append(
        "The launcher now runs the same wrapped Rule-110 control envelope twice: once with `--optimize active-ticks` and once with `--optimize clock-slots`, so the demo shows the active-work schedule and elapsed-frame-clock schedule as separate policies.\n\n"
    )
    lines.append("## Command Tails\n\n")
    for row in rows:
        lines.append(
            f"### {row['name']} ({'PASS' if row['returncode'] == 0 else 'FAIL'})\n\n"
        )
        lines.append("```text\n" + "\n".join(row["tail"]) + "\n```\n\n")
    (DOCS / "holonet_vm_demo_launcher_report.md").write_text(
        "".join(lines), encoding="utf-8"
    )


def main():
    DATA.mkdir(exist_ok=True)
    DOCS.mkdir(exist_ok=True)
    rows = [run_one(name, cmd) for name, cmd in COMMANDS]
    ok = all(r["returncode"] == 0 for r in rows)
    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "python": PYTHON,
        "ok": ok,
        "rows": rows,
        "open": [
            "docs/holonet_vm_live_demo.html",
            "docs/holonet_physical_substrate_stub.svg",
            "docs/holonet_sidechannel_report.md",
            "docs/holonet_vm_demo_and_interface_frontier.md",
        ],
    }
    (DATA / "holonet_vm_demo_launcher.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    write_markdown(rows, ok)
    print("HOLONET VM DEMO LAUNCHER")
    print("------------------------")
    for row in rows:
        print(f"[{'PASS' if row['returncode'] == 0 else 'FAIL'}] {row['name']}")
        for line in row["tail"][-4:]:
            print(f"  {line}")
    print("\nopen docs/holonet_vm_live_demo.html")
    print("wrote data/holonet_vm_demo_launcher.json")
    print("wrote docs/holonet_vm_demo_launcher_report.md")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
