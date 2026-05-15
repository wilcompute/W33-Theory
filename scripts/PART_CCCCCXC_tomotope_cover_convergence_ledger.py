#!/usr/bin/env python3
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUT_PATH = DATA_DIR / "cccccxc_tomotope_cover_convergence_ledger.json"

TOMOTOPE_SUMMARY_PATH = DATA_DIR / "tomotope_cover_bridge_summary.json"
TOMOTOPE_AC_PATH = DATA_DIR / "w33_tomotope_ac_bridge_summary.json"
DISCRETE_CONT_PATH = DATA_DIR / "PART_CCCCCXLV_discrete_continuum_bridge_results.json"


@dataclass(frozen=True)
class Claim:
    id: str
    status: str
    statement: str
    assumptions: list[str]
    evidence: list[str]


@dataclass(frozen=True)
class CoverConvergenceLedger:
    claims: list[Claim]
    checks: dict[str, bool]
    recommendations: list[str]


def _load(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def build() -> CoverConvergenceLedger:
    t_summary = _load(TOMOTOPE_SUMMARY_PATH)
    ac_summary = _load(TOMOTOPE_AC_PATH)
    dc_summary = _load(DISCRETE_CONT_PATH)

    claims = [
        Claim(
            id="finite_tomotope_cover_tower_exists",
            status="exact_verified",
            statement=(
                "The tomotope Q_k family is a genuine infinite internal cover tower with explicit quotient and monodromy growth laws."
            ),
            assumptions=[],
            evidence=[str(TOMOTOPE_SUMMARY_PATH)],
        ),
        Claim(
            id="internal_tower_does_not_fix_weyl_exponent_alone",
            status="exact_verified",
            statement=(
                "Internal cover multiplicities can change finite coefficients but do not by themselves supply the external 4D Weyl exponent."
            ),
            assumptions=[],
            evidence=[str(DISCRETE_CONT_PATH), str(TOMOTOPE_AC_PATH)],
        ),
        Claim(
            id="cover_tower_continuity_requires_external_or_convergence_lift",
            status="conditional_verified",
            statement=(
                "Continuity-like limits from the discrete cover tower are mathematically viable if coupled to an explicit external 4D factor or a separate graph-to-continuum convergence theorem."
            ),
            assumptions=[
                "explicit external 4D spectral factor OR",
                "independent convergence theorem for the cover family",
            ],
            evidence=[str(TOMOTOPE_SUMMARY_PATH), str(TOMOTOPE_AC_PATH)],
        ),
        Claim(
            id="intrinsic_4d_from_discrete_covers_only",
            status="open_frontier",
            statement=(
                "A theorem that discrete tomotope covers alone force a full 4D Weyl-law continuum without external factorization is not yet established in this repo."
            ),
            assumptions=["new intrinsic convergence theorem beyond current product-factor bridge"],
            evidence=[],
        ),
    ]

    native_scaling = t_summary.get("native_scaling", {})
    ac_verdict = str(ac_summary.get("verdict", ""))
    qk_role = str(dc_summary.get("external_continuum_bridge", {}).get("tomotope_Qk_role", ""))

    checks = {
        "native_scaling_marks_external_4d_needed": native_scaling.get("needs_external_4d_factor") is True,
        "ac_summary_mentions_external_4d_role": "external 4D" in ac_verdict,
        "discrete_continuum_bridge_marks_qk_as_internal_role": "external Weyl exponent" in qk_role,
        "claim_status_partition_is_disciplined": {
            c.status for c in claims
        } == {"exact_verified", "conditional_verified", "open_frontier"},
    }

    recommendations = [
        "Keep root/orbit/packet equalities in exact_verified layer.",
        "Keep cover-to-continuum arguments conditional unless external 4D factor or convergence theorem is explicit.",
        "If pursuing intrinsic continuity from covers only, add a dedicated convergence theorem track and keep it labeled open_frontier until proved.",
    ]

    return CoverConvergenceLedger(claims=claims, checks=checks, recommendations=recommendations)


def write(path: Path = OUT_PATH) -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ledger = build()
    payload = {
        "claims": [asdict(c) for c in ledger.claims],
        "checks": ledger.checks,
        "all_checks_pass": all(ledger.checks.values()),
        "recommendations": ledger.recommendations,
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
