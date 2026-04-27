#!/usr/bin/env python3
"""Export the fixed-base Payne/qutrit/cubic local Hesse packet dictionary."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEST_FILE = ROOT / "tests" / "test_burkhardt_moduli_realization.py"
OUTPUT_FILE = ROOT / "artifacts" / "payne_hesse_packet_dictionary.json"


def load_burkhardt_module():
    spec = importlib.util.spec_from_file_location("burkhardt_test_module", TEST_FILE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_payload() -> dict[str, object]:
    mod = load_burkhardt_module()
    return mod.explicit_payne_to_hesse_packet_dictionary()


def main() -> None:
    payload = build_payload()
    OUTPUT_FILE.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()