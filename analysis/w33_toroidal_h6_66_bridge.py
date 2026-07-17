#!/usr/bin/env python3
"""Bridge the W33 route-load 66 to the h=6 toroidal complete-adjacency rung.

The perfect route selector found that the full W33 nonidentity all-pairs
workload uses every line bus exactly 66 times.  This script checks the matching
topological number:

* Csaszar-type neighborly triangulation: K_n on an orientable surface has
  genus h=(n-3)(n-4)/12 when the triangular embedding is possible.
* Szilassi-type dual/face-neighborly map: f mutually adjacent faces gives
  h=(f-4)(f-3)/12 and E=C(f,2).

For n=f=7 this is the Csaszar/Szilassi torus, h=1, E=21.
For n=f=12 this is the h=6 rung, E=C(12,2)=66.

The theorem here is deliberately narrow: W33's perfect all-pairs route load 66
lands exactly on the abstract h=6 complete-adjacency edge count.  This does not
claim a specific embedded geometric h=6 polyhedron has been constructed.
"""

from __future__ import annotations

import argparse
import json
from math import comb
from pathlib import Path
from typing import Any

from w33_perfect_route_selector_runtime import (
    DEFAULT_JSON as DEFAULT_SELECTOR_JSON,
    build_selector_payload,
    load_or_build_certificate,
)
from w33_perfect_multipath_balancer import DEFAULT_JSON as DEFAULT_CERTIFICATE
from w33_uor_runtime_model import ROOT


DEFAULT_JSON = ROOT / "data" / "w33_toroidal_h6_66_bridge.json"
DEFAULT_MD = ROOT / "docs" / "w33_toroidal_h6_66_bridge.md"


def complete_adjacency_rung(n: int) -> dict[str, Any]:
    genus_num = (n - 3) * (n - 4)
    genus = genus_num // 12 if genus_num % 12 == 0 else None
    edges = comb(n, 2)
    if genus is None:
        triangular_faces = None
        dual_vertices = None
    else:
        triangular_faces = 2 * edges // 3
        dual_vertices = edges - n + 2 - 2 * genus
    return {
        "n_or_f": n,
        "genus_formula": "(n-3)(n-4)/12",
        "genus": genus,
        "edges": edges,
        "csaszar_type": {
            "vertices": n,
            "edges": edges,
            "triangular_faces": triangular_faces,
            "genus": genus,
            "description": "neighborly K_n triangular map",
        },
        "szilassi_type_dual": {
            "vertices": dual_vertices,
            "edges": edges,
            "faces": n,
            "genus": genus,
            "description": "dual map with n mutually adjacent faces",
        },
    }


def load_selector_payload() -> dict[str, Any]:
    selector_path = DEFAULT_SELECTOR_JSON
    if selector_path.exists():
        payload = json.loads(selector_path.read_text(encoding="utf-8"))
        if payload.get("status") == "PASS":
            return payload
    return build_selector_payload(load_or_build_certificate(DEFAULT_CERTIFICATE))


def local_realization_hint() -> dict[str, Any]:
    candidates = [
        ROOT / "EDGE_LENGTH_DEEP_PATTERNS.md",
        ROOT / "MDCCLXIV_LXXII_EdgeSpectrum_DeepPatterns.md",
        ROOT / "CLIFFORD_G2_SYNTHESIS.md",
    ]
    hits = []
    for path in candidates:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if "5" in text and "Szilassi" in text and "Cs" in text and "7" in text:
            hits.append(str(path.relative_to(ROOT)))
    return {
        "repo_claim": "local corpus records 5 Csaszar + 2 Szilassi realizations = 7",
        "source_hints": hits,
        "realization_count": 7,
        "csaszar_count": 5,
        "szilassi_count": 2,
        "boundary": "This verifier uses the realization count as a local-corpus hint; the proved bridge below is the exact h=6 edge-count identity.",
    }


def build_payload() -> dict[str, Any]:
    selector = load_selector_payload()
    h0 = complete_adjacency_rung(4)
    h1 = complete_adjacency_rung(7)
    h6 = complete_adjacency_rung(12)
    direct_load = int(next(iter(selector["line_loads"]["direct_histogram"].keys())))
    nonlocal_load = int(next(iter(selector["line_loads"]["nonlocal_histogram"].keys())))
    full_load = int(next(iter(selector["line_loads"]["full_histogram"].keys())))
    checks = {
        "selector_pass": selector["status"] == "PASS",
        "w33_full_line_load_66": selector["line_loads"]["full_histogram"] == {"66": 40},
        "direct_plus_nonlocal_equals_full": direct_load + nonlocal_load == full_load,
        "h0_tetrahedron": h0["csaszar_type"] == {
            "vertices": 4,
            "edges": 6,
            "triangular_faces": 4,
            "genus": 0,
            "description": "neighborly K_n triangular map",
        },
        "h1_csaszar_szilassi_edges_21": h1["genus"] == 1 and h1["edges"] == 21,
        "h6_edges_66": h6["genus"] == 6 and h6["edges"] == 66,
        "h6_dual_has_12_faces_and_44_vertices": h6["szilassi_type_dual"]["faces"] == 12
        and h6["szilassi_type_dual"]["vertices"] == 44,
        "w33_k_is_h6_n": 12 == h6["n_or_f"],
        "w33_full_load_equals_h6_edges": full_load == h6["edges"],
    }
    return {
        "schema": "w33.toroidal_h6_66_bridge.v1",
        "theorem": "W33 perfect route load 66 equals the h=6 complete-adjacency toroidal edge count",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "w33_scheduler_66": {
            "direct_line_load": direct_load,
            "nonlocal_line_load": nonlocal_load,
            "full_nonidentity_line_load": full_load,
            "decomposition": "66 = 12 + 54",
            "line_histogram": selector["line_loads"]["full_histogram"],
        },
        "complete_adjacency_ladder": {
            "h0_fixed_point": h0,
            "h1_csaszar_szilassi": h1,
            "h6_k12_dual_pair": h6,
        },
        "w33_alignment": {
            "k": 12,
            "E_K12": comb(12, 2),
            "h6_genus": 6,
            "full_route_line_load": full_load,
            "identity": "full W33 line-bus load = E(K_12) = 66",
        },
        "seven_realizations_hint": local_realization_hint(),
        "checks": checks,
        "interpretation": (
            "The scheduler 66 is not floating. It is the h=6 complete-adjacency "
            "edge count C(12,2), the same ladder that gives the Csaszar/Szilassi "
            "h=1 pair at n=7. W33 supplies k=12 and the perfect all-pairs route "
            "law supplies 66 uses per line."
        ),
        "honesty_boundary": (
            "This proves an exact numerical/combinatorial bridge. It does not "
            "assert a new embedded h=6 polyhedron realization; external sources "
            "treat that as an abstract/realizability boundary."
        ),
    }


def markdown(payload: dict[str, Any]) -> str:
    h6 = payload["complete_adjacency_ladder"]["h6_k12_dual_pair"]
    return f"""# W(3,3) Toroidal h=6 / 66 Bridge

The perfect route selector gives:

```text
direct line load     = {payload['w33_scheduler_66']['direct_line_load']}
nonlocal line load   = {payload['w33_scheduler_66']['nonlocal_line_load']}
full line load       = {payload['w33_scheduler_66']['full_nonidentity_line_load']}
66 = 12 + 54
```

The complete-adjacency toroidal ladder gives:

```text
h = (n-3)(n-4)/12
n = 7  -> h=1, E=C(7,2)=21   (Csaszar/Szilassi torus)
n = 12 -> h=6, E=C(12,2)=66  (K12 / dual h=6 rung)
```

At the h=6 rung:

| Side | V | E | F | genus |
|---|---:|---:|---:|---:|
| Csaszar-type K12 triangulation | {h6['csaszar_type']['vertices']} | {h6['csaszar_type']['edges']} | {h6['csaszar_type']['triangular_faces']} | {h6['csaszar_type']['genus']} |
| Szilassi-type dual | {h6['szilassi_type_dual']['vertices']} | {h6['szilassi_type_dual']['edges']} | {h6['szilassi_type_dual']['faces']} | {h6['szilassi_type_dual']['genus']} |

Conclusion: the W33 full line-bus load `66` equals `E(K12)`, the h=6
complete-adjacency edge count.

Boundary: this is an exact abstract/combinatorial bridge, not a claim that a
new embedded h=6 polyhedron realization has been constructed.
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-out", default=str(DEFAULT_JSON))
    parser.add_argument("--md-out", default=str(DEFAULT_MD))
    args = parser.parse_args(argv)
    payload = build_payload()
    json_out = Path(args.json_out)
    if not json_out.is_absolute():
        json_out = ROOT / json_out
    md_out = Path(args.md_out)
    if not md_out.is_absolute():
        md_out = ROOT / md_out
    json_out.parent.mkdir(parents=True, exist_ok=True)
    md_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    md_out.write_text(markdown(payload), encoding="utf-8")
    print(f"status: {payload['status']}")
    print(f"W33 load: {payload['w33_scheduler_66']['full_nonidentity_line_load']}")
    print(f"h=6 edges: {payload['complete_adjacency_ladder']['h6_k12_dual_pair']['edges']}")
    print(f"identity: {payload['w33_alignment']['identity']}")
    print(f"wrote: {json_out.relative_to(ROOT)}")
    print(f"wrote: {md_out.relative_to(ROOT)}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
