#!/usr/bin/env python3
"""Run the seven readable Passes 2917--2923 verifier programs."""
from __future__ import annotations
import argparse
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "2917": ROOT / "analysis" / "bt2917_rank7_frame_engine_truth.py",
    "2918": ROOT / "analysis" / "bt2918_m36_first_order_census.py",
    "2919": ROOT / "analysis" / "bt2919_middle_class_antiunitary_chirality.py",
    "2920a": ROOT / "analysis" / "bt2920_adaptive_observer_information_budget.py",
    "2920b": ROOT / "analysis" / "bt2920_noise_aware_adaptive_observer.py",
    "2922": ROOT / "analysis" / "bt2922_classical_line_stabilizer_suborbits.py",
    "2923": ROOT / "analysis" / "bt2923_diameter19_element_classification.py",
}

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--front", action="append", choices=tuple(SOURCES))
    args = parser.parse_args()
    requested = set(args.front or SOURCES)
    for number, path in SOURCES.items():
        if number not in requested:
            continue
        if not path.is_file():
            raise FileNotFoundError(path)
        print(f"=== {number}: {path.relative_to(ROOT)} ===", flush=True)
        runpy.run_path(str(path), run_name="__main__")

if __name__ == "__main__":
    main()
