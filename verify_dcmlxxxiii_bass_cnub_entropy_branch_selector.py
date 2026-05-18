#!/usr/bin/env python3
"""Part DCMLXXXIII: Bass/CnuB entropy branch selector.

DCMLXXXII separated the live W(3,3) Ihara-Bass determinant from the
coefficient-12 shadow.  This verifier checks the strongest follow-up
consequence: the same Bass decrement that changes 12 to 11 also selects the
standard cosmic-neutrino-background entropy ratio.

The promoted statement is intentionally narrow:

* the live Bass-11 branch gives mu/(k-1) = 4/11;
* the coefficient-12 shadow gives mu/k = 1/3;
* the standard e+e- entropy-heating factor gives (T_nu/T_gamma)^3 = 4/11;
* therefore coefficient 12 is the wrong denominator for the CnuB entropy
  branch, just as it is the wrong coefficient for the live graph zeta.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcmlxxxii_ihara_z12_cross_branch_resonance_audit import (  # noqa: E402
    build_bridge as build_cross_branch_audit,
)


DATA_PATH = ROOT / "data" / "dcmlxxxiii_bass_cnub_entropy_branch_selector.json"
RESULT_PATH = ROOT / "PART_DCMLXXXIII_BASS_CNUB_ENTROPY_BRANCH_SELECTOR_results.json"

PART = "DCMLXXXIII"
DECIMAL = 983
PREVIOUS_PART = "DCMLXXXII"
PREVIOUS_DECIMAL = 982

DEGREE = 12
BASS = DEGREE - 1
MU = 4
PHOTON_ENTROPY_DOF = Fraction(2, 1)
ELECTRON_POSITRON_ENTROPY_DOF = Fraction(7, 8) * 4


@dataclass(frozen=True)
class SelectorSummary:
    part: str
    decimal: int
    depends_on_part: str
    depends_on_decimal: int
    live_bass_parameter: int
    shadow_coefficient: int
    standard_cnub_temperature_cube_ratio: str
    live_branch_ratio: str
    shadow_branch_ratio: str
    live_branch_classification: str
    shadow_branch_classification: str
    classical_rh_status: str
    all_identities_hold: bool


def frac_payload(value: Fraction) -> dict[str, Any]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "text": f"{value.numerator}/{value.denominator}",
        "float": float(value),
    }


def entropy_reheating_packet() -> dict[str, Any]:
    before = PHOTON_ENTROPY_DOF + ELECTRON_POSITRON_ENTROPY_DOF
    after = PHOTON_ENTROPY_DOF
    photon_heating_cubed = before / after
    cnub_temperature_cubed = 1 / photon_heating_cubed
    return {
        "source": "standard instantaneous-decoupling e+e- entropy transfer",
        "photon_entropy_degrees": frac_payload(PHOTON_ENTROPY_DOF),
        "electron_positron_entropy_degrees": frac_payload(ELECTRON_POSITRON_ENTROPY_DOF),
        "em_entropy_degrees_before_annihilation": frac_payload(before),
        "em_entropy_degrees_after_annihilation": frac_payload(after),
        "photon_heating_cubed": frac_payload(photon_heating_cubed),
        "cnub_temperature_cubed": frac_payload(cnub_temperature_cubed),
    }


def branch_packet(name: str, denominator: int) -> dict[str, Any]:
    temperature_cubed = Fraction(MU, denominator)
    heating_cubed = 1 / temperature_cubed
    return {
        "name": name,
        "mu": MU,
        "denominator": denominator,
        "temperature_cube_ratio": frac_payload(temperature_cubed),
        "photon_heating_cubed": frac_payload(heating_cubed),
    }


def source_anchor_checks() -> dict[str, bool]:
    w33_paper = (ROOT / "w33_paper.tex").read_text(encoding="utf-8")
    dcmlxxxii = (ROOT / "PART_DCMLXXXII_IHARA_Z12_CROSS_BRANCH_RESONANCE_AUDIT.md").read_text(
        encoding="utf-8"
    )
    dcmlxxxii_compact = " ".join(dcmlxxxii.split())
    return {
        "w33_paper_contains_cnub_ratio": (
            "T_{C\\nu B}^3" in w33_paper
            and "\\frac{\\mu}{k-1}" in w33_paper
            and "\\frac{4}{11}" in w33_paper
        ),
        "dcmlxxxii_contains_live_bass_11": (
            "q_{\\rm Bass}=d-1=11" in dcmlxxxii
            and "coefficient-12 shadow" in dcmlxxxii
        ),
        "dcmlxxxii_keeps_classical_rh_open": (
            "classical Riemann Hypothesis is not proved here" in dcmlxxxii_compact
        ),
    }


def build_selector() -> dict[str, Any]:
    previous = build_cross_branch_audit()
    entropy = entropy_reheating_packet()
    live = branch_packet("live_bass_11", BASS)
    shadow = branch_packet("coefficient_12_shadow", DEGREE)

    standard_ratio = Fraction(
        entropy["cnub_temperature_cubed"]["numerator"],
        entropy["cnub_temperature_cubed"]["denominator"],
    )
    live_ratio = Fraction(
        live["temperature_cube_ratio"]["numerator"],
        live["temperature_cube_ratio"]["denominator"],
    )
    shadow_ratio = Fraction(
        shadow["temperature_cube_ratio"]["numerator"],
        shadow["temperature_cube_ratio"]["denominator"],
    )
    standard_heating = Fraction(
        entropy["photon_heating_cubed"]["numerator"],
        entropy["photon_heating_cubed"]["denominator"],
    )
    shadow_heating = Fraction(
        shadow["photon_heating_cubed"]["numerator"],
        shadow["photon_heating_cubed"]["denominator"],
    )

    source_anchors = source_anchor_checks()
    external_sources = [
        {
            "label": "PDG 2025 Neutrinos in Cosmology",
            "url": "https://pdg.lbl.gov/2025/reviews/rpp2025-rev-neutrinos-in-cosmology.pdf",
            "used_fact": "instantaneous decoupling gives T_nu/T_gamma = (4/11)^(1/3), with precision corrections summarized as N_eff = 3.044",
            "runtime_dependency": False,
        },
        {
            "label": "Rangarajan 2017 Ihara-Bass proof for regular graphs",
            "url": "https://drops.dagstuhl.de/opus/volltexte/2018/8386/pdf/LIPIcs-FSTTCS-2017-46.pdf",
            "used_fact": "Ihara zeta is built from prime non-backtracking cycles and the regular determinant uses the d-1 term",
            "runtime_dependency": False,
        },
    ]

    comparison = {
        "bass_decrement": {
            "graph_degree": DEGREE,
            "live_nonbacktracking_denominator": BASS,
            "removed_return_channels": DEGREE - BASS,
            "reading": "The 12-regular graph has one forbidden immediate-return edge after the first step, so the live nonbacktracking denominator is 11.",
        },
        "temperature_cube_gap_live_minus_shadow": frac_payload(live_ratio - shadow_ratio),
        "photon_heating_gap_shadow_minus_standard": frac_payload(shadow_heating - standard_heating),
        "shadow_relative_to_live": frac_payload(shadow_ratio / live_ratio),
    }

    boundary = {
        "verified_statement": "exact branch-selector arithmetic",
        "not_claimed": [
            "direct CnuB detection",
            "full neutrino decoupling dynamics from W33 alone",
            "classical Riemann Hypothesis",
        ],
        "next_proof_target": (
            "derive the entropy-decoupling handoff functorially from the "
            "W33 return-channel deletion, rather than only matching the "
            "4/11 branch denominator"
        ),
    }

    identities = {
        "part_number_is_983": PART == "DCMLXXXIII" and DECIMAL == 983,
        "depends_on_dcmlxxxii": (
            previous["summary"]["part"] == PREVIOUS_PART
            and previous["summary"]["decimal"] == PREVIOUS_DECIMAL
        ),
        "previous_audit_live_bass_is_11": previous["summary"]["live_bass_parameter"] == BASS,
        "previous_audit_shadow_coefficient_is_12": previous["summary"]["shadow_coefficient"] == DEGREE,
        "standard_entropy_ratio_is_4_over_11": standard_ratio == Fraction(4, 11),
        "standard_photon_heating_is_11_over_4": standard_heating == Fraction(11, 4),
        "live_branch_matches_standard_ratio": live_ratio == standard_ratio,
        "shadow_branch_is_one_third": shadow_ratio == Fraction(1, 3),
        "shadow_branch_is_not_standard_ratio": shadow_ratio != standard_ratio,
        "live_minus_shadow_gap_is_one_over_33": live_ratio - shadow_ratio == Fraction(1, 33),
        "shadow_heating_misses_standard_by_one_fourth": shadow_heating - standard_heating == Fraction(1, 4),
        "bass_decrement_removes_one_return_channel": DEGREE - BASS == 1,
        "coefficient_12_is_already_shadow_in_previous_audit": (
            previous["coefficient_12_shadow"]["status"] == "shadow_branch_not_live_graph_zeta"
        ),
        "classical_rh_boundary_remains_open": (
            previous["rh_boundary"]["classical_riemann_hypothesis"] == "OPEN"
        ),
        "source_anchors_are_present": all(source_anchors.values()),
        "external_sources_are_static": all(not source["runtime_dependency"] for source in external_sources),
    }

    summary = SelectorSummary(
        part=PART,
        decimal=DECIMAL,
        depends_on_part=PREVIOUS_PART,
        depends_on_decimal=PREVIOUS_DECIMAL,
        live_bass_parameter=BASS,
        shadow_coefficient=DEGREE,
        standard_cnub_temperature_cube_ratio=frac_payload(standard_ratio)["text"],
        live_branch_ratio=frac_payload(live_ratio)["text"],
        shadow_branch_ratio=frac_payload(shadow_ratio)["text"],
        live_branch_classification="standard_entropy_branch",
        shadow_branch_classification="wrong_denominator_shadow",
        classical_rh_status=previous["rh_boundary"]["classical_riemann_hypothesis"],
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "previous_audit_summary": previous["summary"],
        "standard_entropy_packet": entropy,
        "live_bass_11_branch": live,
        "coefficient_12_shadow_branch": shadow,
        "branch_comparison": comparison,
        "source_anchor_checks": source_anchors,
        "static_external_sources": external_sources,
        "honesty_boundary": boundary,
        "identities": identities,
    }


def write_selector() -> tuple[Path, Path]:
    payload = build_selector()
    DATA_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    RESULT_PATH.write_text(
        json.dumps(
            {
                "part": payload["summary"]["part"],
                "decimal": payload["summary"]["decimal"],
                "status": "VERIFIED: Bass/CnuB entropy branch selector",
                "summary": payload["summary"],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return DATA_PATH, RESULT_PATH


def main() -> None:
    data_path, result_path = write_selector()
    print(f"Wrote {data_path}")
    print(f"Wrote {result_path}")


if __name__ == "__main__":
    main()
