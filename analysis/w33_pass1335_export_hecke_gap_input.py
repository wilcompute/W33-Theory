#!/usr/bin/env python3
"""Export the already-certified Pass-1330 Hecke tensor as GAP data.

This file performs no new mathematics.  It is a deterministic serialization
bridge so the Pass-1335 Ext calculation is owned and executed by GAP.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis" / "w33_pass1330_1334_modular_triality_cycle_atlas.py"
MAPS = ROOT / "data" / "w33_pass1330_modular_quotient_maps.json"
OUT = ROOT / "data" / "w33_pass1335_hecke_ext_input.g"


def load_pass1330():
    spec = importlib.util.spec_from_file_location("pass1330_for_pass1335", SOURCE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main() -> None:
    module = load_pass1330()
    maps = json.loads(MAPS.read_text())
    scalar_characters = maps["records"]["5"]["scalar_characters"]
    tensor = module.P.tolist()
    text = (
        "# Generated deterministically by w33_pass1335_export_hecke_gap_input.py\n"
        f'P1335TensorSha256 := "{module.TENSOR_SHA}";;\n'
        f"P1335 := {tensor!r};;\n"
        f"CH1335 := {scalar_characters!r};;\n"
    )
    OUT.write_text(text)
    print(OUT.relative_to(ROOT), len(text.encode()), module.TENSOR_SHA)


if __name__ == "__main__":
    main()
