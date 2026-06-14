#!/usr/bin/env python3
"""
BT988 — Load explicit CP2_9/K3_16 facets into the edgewise R3 path.

The repo already contains executable facet generators in
`exploration/w33_explicit_curved_4d_complexes.py`:
  - CP2_9 from Kuhnel's 9-vertex orbit description;
  - K3_16 from the Casella-Kuhnel/Sage permutation-orbit construction.

BT988 imports those actual facets and attaches the edgewise/Freudenthal-Kuhn
replacement tower.  It records the exact level-0 explicit chain data and the
exact level-1 edgewise vertex/top-simplex counts:

  vertices(level 1) = f0 + f1     (old vertices plus all edge midpoints),
  top 4-simplices(level r) = f4 * 16^r.

Boundary: this file does not invent the missing 4-simplex local edgewise facet
template.  Exact lower-dimensional level-r incidence matrices require that
local template; BT988 locks the explicit seed facets and the correct edgewise
count layer.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_explicit_curved_4d_complexes import cp2_facets, k3_facets, complex_profile  # noqa: E402


def packet(name: str, facets: tuple[tuple[int, ...], ...]) -> dict:
    profile = complex_profile(name, facets)
    f0, f1, f2, f3, f4 = profile.f_vector
    return {
        "name": name,
        "explicit_facets_loaded": True,
        "facet_count": len(facets),
        "sample_facets": [list(x) for x in facets[:5]],
        "f_vector": list(profile.f_vector),
        "betti_numbers": list(profile.betti_numbers),
        "euler_characteristic": profile.euler_characteristic,
        "edgewise_level1_vertices": f0 + f1,
        "edgewise_top_multiplier_per_step": 16,
        "edgewise_top_4simplices_by_level": [f4 * (16 ** r) for r in range(7)],
        "barycentric_top_4simplices_by_level": [f4 * (120 ** r) for r in range(7)],
    }


def main() -> None:
    out = {
        "theorem": "BT988 explicit CP2_9/K3_16 facets loaded into edgewise R3 path",
        "source_module": "exploration/w33_explicit_curved_4d_complexes.py",
        "seeds": [packet("CP2_9", cp2_facets()), packet("K3_16", k3_facets())],
        "boundary": "Explicit seed facets are loaded. Full edgewise lower-incidence matrices still require the local 4-simplex edgewise facet template; no incidence data is fabricated.",
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/bt988_explicit_cp2_k3_edgewise_facets.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
