#!/usr/bin/env python3
"""Run named focused theorem-test slices.

The repository is large enough that broad pytest collection can be slow on
Windows/WSL-mounted trees.  This helper runs curated file lists for the bridge
areas that are commonly touched during architecture work.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SUITES: dict[str, list[str]] = {
    "photonic-qec": [
        "tests/test_dccxiv_holonomy_signed_triad_a2_projection_bridge.py",
        "tests/test_dccxv_photonic_fusion_syndrome_qec_bridge.py",
        "tests/test_cyclic_cayley_obstruction_ccccxxx.py",
        "tests/test_qec_ouroboros_stabilizer_loop_ccccxvii.py",
        "tests/test_fusion_control_scheduler_splice_ccccxxvi.py",
        "tests/test_photonic_harmonic_tqc_bus_ccccxviii.py",
    ],
    "dcc-weld": [
        "tests/test_dccx_holonomy_selector_carrier_weld_bridge.py",
        "tests/test_dccxi_holonomy_weld_associator_support_bridge.py",
        "tests/test_dccxiv_holonomy_signed_triad_a2_projection_bridge.py",
        "tests/test_dccxv_photonic_fusion_syndrome_qec_bridge.py",
    ],
    "tomotope-klitzing": [
        "tests/test_w33_tomotope_klitzing_partial_operation_commutation.py",
        "tests/test_w33_tomotope_klitzing_six_table_lock.py",
        "tests/test_tomotope_cover_convergence_ledger_cccccxc.py",
    ],
    "sector-split": [
        "tests/test_clifford_percolation_hole_oscillator_ccccclxxxi.py",
        "tests/test_e6_a2_root_refinement_ccccclxxxviii.py",
        "tests/test_tomotope_two_192_mechanisms_cccccxcII.py",
        "tests/test_we6_orbit_phase_shell_ccccclxxxvii.py",
    ],
}

ALIASES = {
    "architecture": ["photonic-qec", "dcc-weld", "tomotope-klitzing", "sector-split"],
}


def expand_suites(names: list[str]) -> list[str]:
    selected: list[str] = []
    for name in names:
        if name in ALIASES:
            selected.extend(expand_suites(ALIASES[name]))
            continue
        if name not in SUITES:
            known = sorted([*SUITES, *ALIASES])
            raise SystemExit(f"Unknown suite {name!r}. Known suites: {', '.join(known)}")
        selected.extend(SUITES[name])

    deduped: list[str] = []
    seen: set[str] = set()
    for path in selected:
        if path not in seen:
            seen.add(path)
            deduped.append(path)
    return deduped


def build_pytest_command(paths: list[str], extra_pytest_args: list[str]) -> list[str]:
    return [
        sys.executable,
        "-m",
        "pytest",
        "--noconftest",
        "-q",
        *paths,
        *extra_pytest_args,
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "suite",
        nargs="*",
        default=["photonic-qec"],
        help=(
            "Suite(s) to run. Known suites: "
            + ", ".join(sorted([*SUITES, *ALIASES]))
            + ". Default: photonic-qec."
        ),
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List suite names and test files without running pytest.",
    )
    args, extra_pytest_args = parser.parse_known_args(argv)
    if extra_pytest_args and extra_pytest_args[0] == "--":
        extra_pytest_args = extra_pytest_args[1:]

    if args.list:
        for name in sorted(SUITES):
            print(f"{name}:")
            for path in SUITES[name]:
                print(f"  {path}")
        for name in sorted(ALIASES):
            print(f"{name}: {', '.join(ALIASES[name])}")
        return 0

    paths = expand_suites(args.suite)
    missing = [path for path in paths if not (ROOT / path).exists()]
    if missing:
        raise SystemExit("Missing test files:\n" + "\n".join(f"  {path}" for path in missing))

    command = build_pytest_command(paths, extra_pytest_args)
    print("Running:", " ".join(command), flush=True)
    return subprocess.call(command, cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
