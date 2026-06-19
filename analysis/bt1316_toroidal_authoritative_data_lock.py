#!/usr/bin/env python3
"""BT1316 - Authoritative data lock for the Csaszar/Szilassi toroidal pair.

This verifier exists because an older theorem note had duplicated the
Csaszar V/F row onto Szilassi. The raw realization table, CCCCXXI bridge,
and triad HTML all use the corrected dual values:

  Csaszar:  V,E,F = 7,21,14
  Szilassi: V,E,F = 14,21,7

The executable boundary is simple: E=21 is shared, while V and F are swapped.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "data" / "bt1316_toroidal_authoritative_data_lock.json"


def _load_module(name: str, relpath: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relpath)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module at {relpath}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _raw_counts() -> dict[str, Any]:
    bt803 = _load_module("bt803", "analysis/bt803_seven_realizations_census.py")
    rows = bt803.parse_dataset(ROOT / "data" / "Toroidal-Polyhedra-Realizations.txt")
    families: dict[str, list[dict[str, int]]] = {"Csaszar": [], "Szilassi": []}
    for row in rows:
        faces = row["faces"]
        edges = bt803.edges_of(faces)
        families[row["kind"]].append(
            {
                "version": row["version"],
                "vertices": len(row["vertices"]),
                "edges": len(edges),
                "faces": len(faces),
                "euler_characteristic": len(row["vertices"]) - len(edges) + len(faces),
            }
        )
    return {
        "total_realizations": len(rows),
        "family_counts": {key: len(value) for key, value in families.items()},
        "families": families,
    }


def _bridge_counts() -> dict[str, Any]:
    ccccxxi = _load_module(
        "ccccxxi", "exploration/PART_CCCCXXI_TOROIDAL_FANO_BRIDGE.py"
    )
    results = ccccxxi.build_results()
    return {
        "verified": bool(results["verified"]),
        "checks_passed": int(results["checks_passed"]),
        "checks_total": int(results["checks_total"]),
        "csaszar": results["csaszar_polyhedron"],
        "szilassi": results["szilassi_polyhedron"],
        "duality": results["duality"],
    }


def build_lock() -> dict[str, Any]:
    raw = _raw_counts()
    bridge = _bridge_counts()

    dxxxii = (ROOT / "W33_Part_DXXXII_Csaszar_Szilassi_Genus_Unification.md").read_text(
        encoding="utf-8"
    )
    triad_html = (ROOT / "visualizations" / "w33-toroidal-triad.html").read_text(
        encoding="utf-8"
    )
    index_html = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

    authoritative_values = {
        "csaszar": {"vertices": 7, "edges": 21, "faces": 14, "genus": 1},
        "szilassi": {"vertices": 14, "edges": 21, "faces": 7, "genus": 1},
        "shared_invariant": "edges=21",
        "duality": "(V,F) swap, E preserved",
    }

    raw_all_match = all(
        row["vertices"] == authoritative_values["csaszar"]["vertices"]
        and row["edges"] == authoritative_values["csaszar"]["edges"]
        and row["faces"] == authoritative_values["csaszar"]["faces"]
        and row["euler_characteristic"] == 0
        for row in raw["families"]["Csaszar"]
    ) and all(
        row["vertices"] == authoritative_values["szilassi"]["vertices"]
        and row["edges"] == authoritative_values["szilassi"]["edges"]
        and row["faces"] == authoritative_values["szilassi"]["faces"]
        and row["euler_characteristic"] == 0
        for row in raw["families"]["Szilassi"]
    )

    checks = {
        "raw_has_five_plus_two_realizations": raw["family_counts"]
        == {
            "Csaszar": 5,
            "Szilassi": 2,
        },
        "raw_all_rows_match_authoritative_values": raw_all_match,
        "ccccxxi_bridge_verified": bridge["verified"]
        and bridge["checks_passed"] == bridge["checks_total"] == 48,
        "bridge_csaszar_matches_authoritative_values": (
            bridge["csaszar"]["vertices"],
            bridge["csaszar"]["edges"],
            bridge["csaszar"]["faces"],
        )
        == (7, 21, 14),
        "bridge_szilassi_matches_authoritative_values": (
            bridge["szilassi"]["vertices"],
            bridge["szilassi"]["edges"],
            bridge["szilassi"]["faces"],
        )
        == (14, 21, 7),
        "dxxxii_table_corrected": "| Vertices V | 7 | 14 | 4 |" in dxxxii
        and "| Faces F | 14 | 7 | 4 |" in dxxxii
        and "Correction boundary" in dxxxii,
        "triad_html_uses_correct_dual_values": (
            "<td>7</td><td>21</td><td>14</td>" in triad_html
            and "Szilassi</td><td>14</td><td>21</td><td>7</td>" in triad_html
        ),
        "docs_index_exposes_symmetry_stratification": (
            "Cs&aacute;sz&aacute;r/Szilassi toroidal symmetry stratification"
            in index_html
            and "<code>5</code> Cs&aacute;sz&aacute;r and <code>2</code> Szilassi"
            in index_html
        ),
    }

    return {
        "theorem": "BT1316 toroidal authoritative data lock",
        "verified": all(checks.values()),
        "authoritative_values": authoritative_values,
        "raw": raw,
        "ccccxxi_bridge": bridge,
        "checks": checks,
        "boundary": (
            "The verified toroidal duality preserves E=21 and swaps V/F. "
            "Any prose table listing Szilassi as V=7,F=14 is stale."
        ),
    }


def write_results(path: Path = OUT_PATH) -> Path:
    payload = build_lock()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    payload = build_lock()
    out = write_results()
    print(f"BT1316 verified={payload['verified']} wrote {out}")
    if not payload["verified"]:
        failed = [name for name, ok in payload["checks"].items() if not ok]
        raise SystemExit(f"BT1316 failed checks: {failed}")


if __name__ == "__main__":
    main()
