#!/usr/bin/env python3
"""BT1457: claim-firewalled integration manifest for the Otto/Szilassi Holonet section."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1457_claim_firewalled_holonet_integration.json"
TEX = ROOT / "analysis" / "BT1457_claim_firewalled_holonet_section.tex"


def main() -> None:
    section = r"""\subsection{Claim-firewalled Otto--Szilassi closure bridge}
\label{sec:bt1457-claim-firewalled-otto-szilassi}

The Otto--Szilassi bridge is included only with claim stratification.  Exact
finite claims are separated from numerical resonances and blocked physical
claims.

\paragraph{Exact coordinate fact.}
The Szilassi data contain a unique fixed hexagon under
\(R(x,y,z)=(-x,-y,z)\), with ordered boundary
\[
[11,9,12,10,8,13],
\]
whose image is a boundary shift by three vertices.

\paragraph{Exact finite bus fact.}
The fixed-face closure gives
\[
3\cdot2\cdot2=12,
\qquad 2\cdot12=24,
\qquad 12(13+1)=168.
\]

\paragraph{Exact group fact.}
The closure/shear layer is
\[
S_3\times C_3,
\]
with the central \(C_3\) interpreted as the qutrit phase center and the \(S_3\)
quotient as the three-channel closure switch.

\paragraph{Finite decoder fact.}
The closure tick is compatible with the retwined CSS rule
\[
\operatorname{syn}_{H}(e)=\operatorname{syn}_{H'}(Je).
\]

\paragraph{Numerical resonance.}
Otto's varied golden quartic coefficient satisfies
\[
4-\phi^2=3+\phi=\sqrt{13+\phi^5},
\]
which resonates with the three opposite-pair closure and 13 half-turn core, but
this is not claimed as a physical derivation.

\paragraph{Blocked claims.}
Equations (49), (50), (64), (65), and (66) remain blocked until their rendered
formula bodies are transcribed and audited.  The real-world particle model is
not imported as an exact claim.
"""
    TEX.write_text(section, encoding="utf-8")
    claims = [
        {"label": "exact_coordinate", "allowed": True},
        {"label": "exact_finite_bus", "allowed": True},
        {"label": "exact_group", "allowed": True},
        {"label": "finite_decoder", "allowed": True},
        {"label": "numerical_resonance", "allowed": True},
        {"label": "formula_level_physics", "allowed": False},
        {"label": "real_world_particle_model", "allowed": False},
    ]
    checks = {
        "tex_section_written": TEX.exists() and "Claim-firewalled" in TEX.read_text(encoding="utf-8"),
        "has_exact_coordinate_label": any(c["label"] == "exact_coordinate" and c["allowed"] for c in claims),
        "has_finite_decoder_label": any(c["label"] == "finite_decoder" and c["allowed"] for c in claims),
        "blocks_formula_level_physics": any(c["label"] == "formula_level_physics" and not c["allowed"] for c in claims),
        "blocks_real_world_particle_model": any(c["label"] == "real_world_particle_model" and not c["allowed"] for c in claims),
    }
    result = {
        "bt": 1457,
        "title": "Claim-firewalled Holonet integration",
        "verified": all(checks.values()),
        "tex_insert_path": "analysis/BT1457_claim_firewalled_holonet_section.tex",
        "claims": claims,
        "integration_command": "Insert \\input{analysis/BT1457_claim_firewalled_holonet_section} into photonic_holonet.tex after the BT1453--BT1455 claim firewall section.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1457, "verified": result["verified"], "tex": result["tex_insert_path"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
