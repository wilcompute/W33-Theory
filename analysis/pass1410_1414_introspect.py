#!/usr/bin/env python3
from __future__ import annotations

import inspect
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

import _selector_five_frontiers_impl as ff
import _mackey_selector_decomposition_impl as mk
from pass1370_1374 import core, modular_radicals


def callable_record(module, name: str):
    obj = getattr(module, name)
    try:
        sig = str(inspect.signature(obj))
    except (TypeError, ValueError):
        sig = None
    return {"name": name, "signature": sig, "module": module.__name__}


def selected(module):
    tokens = (
        "worker", "mackey", "fourier", "apartment", "bridge", "order",
        "radical", "loewy", "matrix", "unit", "build", "selector",
        "projector", "tensor", "modular", "exact", "rank", "sheet",
    )
    out = []
    for name in sorted(dir(module)):
        if name.startswith("__"):
            continue
        if not any(token in name.lower() for token in tokens):
            continue
        if callable(getattr(module, name)):
            out.append(callable_record(module, name))
    return out


payload = {
    "selector_frontiers": selected(ff),
    "mackey": selected(mk),
    "core": selected(core),
    "modular_radicals": selected(modular_radicals),
}
print(json.dumps(payload, indent=2, sort_keys=True))
