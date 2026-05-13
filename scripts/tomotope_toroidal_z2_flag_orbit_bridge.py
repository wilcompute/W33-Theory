#!/usr/bin/env python3
"""Part DCXV: Z2 quotient-to-flag bridge.

Connects DCXIV quotient counts to toroidal flag counts from the dual packet
bridge:

  weighted shell 168 --(Z2 quotient)--> 84

and verifies this 84 equals each single polyhedron flag shell:

  Csaszar flags = 84,
  Szilassi flags = 84.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ORBIT_PATH = ROOT / "data" / "tomotope_toroidal_z2_orbit_quotient_bridge.json"
DUAL_PATH = ROOT / "data" / "tomotope_toroidal_dual_packet_bridge.json"
OUT_PATH = ROOT / "data" / "tomotope_toroidal_z2_flag_orbit_bridge.json"


def _load_orbit_payload() -> dict[str, Any]:
    if ORBIT_PATH.exists():
        return json.loads(ORBIT_PATH.read_text(encoding="utf-8"))
    from scripts.tomotope_toroidal_z2_orbit_quotient_bridge import build_bridge

    return build_bridge()


def _load_dual_payload() -> dict[str, Any]:
    if DUAL_PATH.exists():
        return json.loads(DUAL_PATH.read_text(encoding="utf-8"))
    from scripts.tomotope_toroidal_dual_packet_bridge import build_bridge

    return build_bridge()


@dataclass(frozen=True)
class FlagOrbitSummary:
    weighted_shell_size: int
    z2_weighted_orbit_count: int
    csaszar_flags: int
    szilassi_flags: int
    dual_toroidal_flags: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    orbit = _load_orbit_payload()
    dual = _load_dual_payload()

    weighted = int(orbit["summary"]["weighted_size"])
    quotient = int(orbit["summary"]["weighted_orbit_count"])

    cs_flags = int(dual["polyhedra"]["csaszar"]["flags"])
    sz_flags = int(dual["polyhedra"]["szilassi"]["flags"])
    dual_flags = int(dual["summary"]["dual_toroidal_flag_weight"])

    identities = {
        "upstream_orbit_identities_hold": bool(orbit["summary"]["all_identities_hold"]),
        "weighted_shell_is_168": weighted == 168,
        "quotient_is_84": quotient == 84,
        "csaszar_flags_84": cs_flags == 84,
        "szilassi_flags_84": sz_flags == 84,
        "dual_flags_168": dual_flags == 168,
        "quotient_matches_csaszar_flags": quotient == cs_flags,
        "quotient_matches_szilassi_flags": quotient == sz_flags,
        "quotient_is_half_of_dual_flags": 2 * quotient == dual_flags,
        "weighted_shell_matches_dual_flags": weighted == dual_flags,
    }

    summary = FlagOrbitSummary(
        weighted_shell_size=weighted,
        z2_weighted_orbit_count=quotient,
        csaszar_flags=cs_flags,
        szilassi_flags=sz_flags,
        dual_toroidal_flags=dual_flags,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "identities": identities,
        "notes": (
            "DCXV identifies the Z2 weighted quotient 84 with each individual toroidal "
            "flag shell (Csaszar and Szilassi), while 168 remains the unswapped dual total."
        ),
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
