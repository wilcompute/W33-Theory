#!/usr/bin/env python3
"""Reproducible, read-only inventory gate for the oscillator measurement front.

This script inventories visible device interfaces and repository traces.  It
never opens a serial/USB/VISA endpoint and never sends an instrument command.
An identified instrument, a measured trace, and an independent calibration
must all be supplied before the status can advance beyond the access blocker.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/w33_measurement_access_audit.json"
WINDOWS_SERIAL_QUERY = (
    "Get-CimInstance Win32_SerialPort | "
    "Select-Object DeviceID,Name | ConvertTo-Json -Compress"
)


def visible_nodes(pattern: str):
    return sorted(str(path) for path in Path("/").glob(pattern.lstrip("/")))


def repository_candidates():
    tokens = ("oscillator", "trace", "calibration")
    answer = []
    for directory in (ROOT / "analysis", ROOT / "data"):
        for path in directory.glob("*.json"):
            if any(token in path.name.lower() for token in tokens):
                answer.append(str(path.relative_to(ROOT)).replace(os.sep, "/"))
    return sorted(answer)


def powershell_path():
    found = shutil.which("powershell.exe")
    if found:
        return found
    fallback = Path(
        "/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe"
    )
    return str(fallback) if fallback.exists() else None


def windows_serial_inventory():
    executable = powershell_path()
    if executable is None:
        return {
            "attempted": False,
            "executable": None,
            "command": WINDOWS_SERIAL_QUERY,
            "returncode": None,
            "stderr": "PowerShell executable not visible from this environment",
            "ports": [],
        }
    try:
        completed = subprocess.run(
            [
                executable,
                "-NoLogo",
                "-NoProfile",
                "-NonInteractive",
                "-Command",
                WINDOWS_SERIAL_QUERY,
            ],
            capture_output=True,
            check=False,
            timeout=20,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return {
            "attempted": True,
            "executable": executable,
            "command": WINDOWS_SERIAL_QUERY,
            "returncode": None,
            "stderr": str(error),
            "ports": [],
        }

    stdout = completed.stdout.decode("utf-8", errors="replace").strip()
    stderr = completed.stderr.decode("utf-8", errors="replace").strip()
    ports = []
    parse_error = None
    if stdout:
        try:
            parsed = json.loads(stdout)
            if isinstance(parsed, dict):
                parsed = [parsed]
            ports = [
                {"port": row.get("DeviceID"), "name": row.get("Name")}
                for row in parsed
                if isinstance(row, dict)
            ]
        except json.JSONDecodeError as error:
            parse_error = str(error)
    return {
        "attempted": True,
        "executable": executable,
        "command": WINDOWS_SERIAL_QUERY,
        "returncode": completed.returncode,
        "stderr": stderr,
        "stdout_parse_error": parse_error,
        "ports": ports,
    }


def selected_path(value: str | None):
    if value is None:
        return None
    path = Path(value)
    if not path.is_absolute():
        path = ROOT / path
    return {
        "supplied": value,
        "resolved": str(path.resolve()),
        "exists": path.exists(),
        "is_file": path.is_file(),
    }


def audit(
    instrument: str | None = None,
    measured_trace: str | None = None,
    independent_calibration: str | None = None,
    checked_utc: str | None = None,
):
    linux_serial = visible_nodes("/dev/serial/by-id/*")
    linux_usb = visible_nodes("/dev/bus/usb/*/*")
    linux_usbtmc = visible_nodes("/dev/usbtmc*")
    linux_hidraw = visible_nodes("/dev/hidraw*")
    windows = windows_serial_inventory()

    trace = selected_path(measured_trace)
    calibration = selected_path(independent_calibration)
    ready = bool(
        instrument
        and trace
        and trace["is_file"]
        and calibration
        and calibration["is_file"]
    )

    synthetic_path = ROOT / "analysis/w33_oscillator_calibration_test.json"
    synthetic = json.loads(synthetic_path.read_text())
    assert synthetic["data_origin"] == (
        "synthetic seeded Gaussian fixture, not hardware measurements"
    )
    assert synthetic["mass_stiffness_scale_not_identifiable_without_external_calibration"]

    timestamp = checked_utc or datetime.now(timezone.utc).isoformat()
    return {
        "schema": "w33.measurement_access_audit.v2",
        "status": (
            "READY_FOR_READONLY_TRACE_INGEST"
            if ready
            else "AWAITING_IDENTIFIED_INSTRUMENT_AND_CALIBRATION"
        ),
        "checked_utc": timestamp,
        "host_context": {
            "platform": platform.platform(),
            "python": platform.python_version(),
            "wsl_interop_visible": bool(os.environ.get("WSL_INTEROP")),
        },
        "repository_json_candidates": repository_candidates(),
        "interface_inventory": {
            "linux_serial_by_id": linux_serial,
            "linux_usb_bus_nodes": linux_usb,
            "linux_usbtmc_nodes": linux_usbtmc,
            "linux_hidraw_nodes": linux_hidraw,
            "windows_serial": windows,
            "visa": {
                "enumerated": False,
                "reason": "No configured VISA backend/resource name was supplied; no bus query was attempted.",
            },
            "network_instruments": {
                "enumerated": False,
                "reason": "No hostname, IP address, mDNS service, or instrument protocol was supplied.",
            },
        },
        "selection": {
            "identified_instrument": instrument,
            "measured_trace": trace,
            "independent_calibration": calibration,
        },
        "synthetic_fixture_firewall": {
            "path": str(synthetic_path.relative_to(ROOT)).replace(os.sep, "/"),
            "data_origin": synthetic["data_origin"],
            "may_be_used_as_measurement": False,
            "mass_stiffness_scale_identified": False,
        },
        "readiness_predicate": (
            "identified instrument AND existing measured-trace file AND existing "
            "independent-calibration file"
        ),
        "actions": (
            "Read-only filesystem and serial-interface inventory. No endpoint was opened "
            "and no command was sent to a device."
        ),
        "scope": (
            "Absence from these visible interfaces is not proof that no laboratory hardware "
            "or data exists elsewhere. USBTMC/HID nodes are listed if exposed; VISA and "
            "network discovery remain unqueried until an explicit resource is identified."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--instrument")
    parser.add_argument("--measured-trace")
    parser.add_argument("--independent-calibration")
    parser.add_argument("--write", action="store_true")
    arguments = parser.parse_args()
    result = audit(
        instrument=arguments.instrument,
        measured_trace=arguments.measured_trace,
        independent_calibration=arguments.independent_calibration,
    )
    if arguments.write:
        OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
