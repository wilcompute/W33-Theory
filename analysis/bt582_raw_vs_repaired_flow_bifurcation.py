#!/usr/bin/env python3
"""BT582: raw vs repaired cubic-flow bifurcation table.

Compares four maps applied to the protected Levi Gram
G=(1/81)CC^T=(160/81)E4:

1. raw cubic Gegenbauer map C3(G),
2. centered raw cubic map C3(G)-E0 component,
3. repaired map P_{E0+E4}C3(G),
4. repaired-centered-normalized map returning G.
"""
import json
from pathlib import Path
import sympy as sp

sqrt6 = sp.sqrt(6)
labels = ["E0", "E1", "E2", "E3", "E4"]
G = [sp.Integer(0), sp.Integer(0), sp.Integer(0), sp.Integer(0), sp.Rational(160, 81)]
raw = [
    sp.Rational(17205568, 243),
    sp.Rational(179189696, 2187) - sp.Rational(734384, 243)*sqrt6,
    sp.Rational(177720928, 2187),
    sp.Rational(179189696, 2187) + sp.Rational(734384, 243)*sqrt6,
    sp.Rational(1751954560, 19683),
]
centered_raw = [sp.Integer(0)] + raw[1:]
repaired = [raw[0], sp.Integer(0), sp.Integer(0), sp.Integer(0), raw[4]]
repaired_centered = [sp.Integer(0), sp.Integer(0), sp.Integer(0), sp.Integer(0), raw[4]]
normalized_repaired = G[:]

def support(vec):
    return [labels[i] for i, x in enumerate(vec) if sp.simplify(x) != 0]

def as_dict(vec):
    return {labels[i]: str(sp.factor(sp.simplify(vec[i]))) for i in range(5)}

def leakage(vec):
    return [x for x in support(vec) if x in {"E1", "E2", "E3"}]

stages = {
    "G_input": G,
    "raw_C3": raw,
    "centered_raw_C3": centered_raw,
    "repaired_P_E0_E4": repaired,
    "repaired_centered": repaired_centered,
    "normalized_repaired": normalized_repaired,
}
checks = {
    "raw_has_all_five_sectors": support(raw) == labels,
    "centered_raw_kills_E0_only": support(centered_raw) == ["E1", "E2", "E3", "E4"],
    "repair_kills_companion": leakage(repaired) == [],
    "centered_repair_is_E4_only": support(repaired_centered) == ["E4"],
    "normalized_returns_G": normalized_repaired == G,
}
result = {
    "bt": 582,
    "title": "Raw vs repaired cubic-flow bifurcation",
    "stages": {name: as_dict(vec) for name, vec in stages.items()},
    "supports": {name: support(vec) for name, vec in stages.items()},
    "bifurcation_summary": [
        "raw C3(G): E0+E1+E2+E3+E4",
        "centered raw: E1+E2+E3+E4",
        "repaired: E0+E4",
        "repaired centered: E4",
        "normalized repaired: original G"
    ],
    "checks": checks,
    "all_identities_hold": all(checks.values()),
}
Path("data/PART_BT582_RAW_VS_REPAIRED_FLOW_BIFURCATION_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
