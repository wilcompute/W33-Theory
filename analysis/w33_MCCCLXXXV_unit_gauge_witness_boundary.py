#!/usr/bin/env python3
"""MCCCLXXXV: unit-gauge witness boundary.

The untracked legacy MCCCLXXXIV note contains useful arithmetic, but its
headline is too strong: unit-scaled SI mantissas are not dimensionless
predictions.  This verifier reconciles that legacy five-witness hint with the
stricter committed MCCCLXXXIV packet and makes the boundary itself executable.
"""

from __future__ import annotations

from collections import Counter
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
STRICT_MODULE_PATH = ROOT / "analysis" / "w33_MCCCLXXXIV_measured_derived_constants_substrate.py"


def load_strict_module():
    spec = importlib.util.spec_from_file_location(
        "w33_MCCCLXXXIV_measured_derived_constants_substrate",
        STRICT_MODULE_PATH,
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


LEGACY_HINTS = [
    {
        "legacy_name": "G (Newton, measured)",
        "strict_name": "Newtonian constant G",
        "expected_mantissa": 667430,
        "legacy_form": "r*F_5*p_11*(Phi_12*p_10 + (q!)^2)",
    },
    {
        "legacy_name": "g_0 (standard gravity)",
        "strict_name": "standard gravity g0",
        "expected_mantissa": 980665,
        "legacy_form": "F_5*Phi_6*(Phi_12*(q^q*Phi_3+2^F_5) + q!*Phi_4)",
    },
    {
        "legacy_name": "1 atm (standard atmosphere)",
        "strict_name": "standard atmosphere",
        "expected_mantissa": 101325,
        "legacy_form": "q*F_5^2*Phi_6*(2^Phi_6 + F_5*Phi_3)",
    },
    {
        "legacy_name": "m_p (proton mass, keV)",
        "strict_name": "proton mass energy equivalent",
        "expected_mantissa": 938272,
        "legacy_form": "2^F_5*(Phi_4^2 + q^2)*(mu^4 + Phi_3)",
    },
    {
        "legacy_name": "F (Faraday)",
        "strict_name": "Faraday constant",
        "expected_mantissa": 9648533,
        "legacy_form": "p_11*(mu*alpha_int-1)*(mu*alpha_int+q*Phi_6)",
    },
]


def generate_payload() -> dict:
    strict = load_strict_module().generate_payload()
    strict_by_name = {item["name"]: item for item in strict["witnesses"]}
    class_counts = Counter(item["class"] for item in strict["witnesses"])

    reconciled = []
    for hint in LEGACY_HINTS:
        strict_item = strict_by_name[hint["strict_name"]]
        reconciled.append(
            {
                **hint,
                "strict_computed": strict_item["computed"],
                "strict_class": strict_item["class"],
                "strict_status": strict_item["status"],
                "match": strict_item["computed"] == hint["expected_mantissa"],
                "promoted_as_dimensionless_prediction": False,
            }
        )

    strict_names = set(strict_by_name)
    legacy_strict_names = {hint["strict_name"] for hint in LEGACY_HINTS}
    strict_extra_names = sorted(strict_names - legacy_strict_names)

    unit_gauge_orbit = {
        "strict_witness_count": len(strict["witnesses"]),
        "legacy_hint_count": len(LEGACY_HINTS),
        "legacy_overlap_count": len(reconciled),
        "strict_extra_names": strict_extra_names,
        "classification_counts": dict(sorted(class_counts.items())),
        "unit_scaled_decimal_witnesses": True,
        "dimensionless_prediction_layer": False,
        "unsafe_legacy_universal_headline_promoted": False,
        "boundary_statement": (
            "The arithmetic is promoted only as a finite unit-gauge witness "
            "orbit.  A dimensionful SI mantissa becomes a physical prediction "
            "only after an independent dimensionless ratio or scale map fixes "
            "the unit gauge."
        ),
    }

    checks = {
        "strict_packet_all_verified": strict["all_verified"] is True,
        "legacy_hints_all_match_strict_packet": all(item["match"] for item in reconciled),
        "legacy_hint_count_is_five": len(LEGACY_HINTS) == 5,
        "strict_packet_count_is_six": len(strict["witnesses"]) == 6,
        "strict_adds_only_molar_gas_constant": strict_extra_names == ["molar gas constant"],
        "classification_counts_are_balanced_two_two_two": class_counts
        == Counter(
            {
                "CODATA measured rounded mantissa": 2,
                "conventional exact": 2,
                "SI-derived exact rounded mantissa": 2,
            }
        ),
        "measured_entries_are_rounded_not_exact": all(
            strict_by_name[name]["class"] == "CODATA measured rounded mantissa"
            for name in ["Newtonian constant G", "proton mass energy equivalent"]
        ),
        "conventional_entries_are_exact": all(
            strict_by_name[name]["class"] == "conventional exact"
            for name in ["standard gravity g0", "standard atmosphere"]
        ),
        "derived_entries_are_exact_but_rounded_display": all(
            strict_by_name[name]["class"] == "SI-derived exact rounded mantissa"
            for name in ["Faraday constant", "molar gas constant"]
        ),
        "molar_gas_lock_uses_alpha_effective_volume": strict["checks"]["gas_factor_b"]
        and strict["checks"]["leff_alpha"],
        "dimensionful_witnesses_not_promoted_as_dimensionless_predictions": (
            unit_gauge_orbit["unit_scaled_decimal_witnesses"]
            and not unit_gauge_orbit["dimensionless_prediction_layer"]
            and not unit_gauge_orbit["unsafe_legacy_universal_headline_promoted"]
        ),
        "every_legacy_hint_is_demoted_to_unit_gauge_witness": all(
            item["promoted_as_dimensionless_prediction"] is False for item in reconciled
        ),
    }

    return {
        "theorem": "MCCCLXXXV_UNIT_GAUGE_WITNESS_BOUNDARY",
        "claim": (
            "The five legacy measured-constant hints are exactly recovered by "
            "the stricter six-witness MCCCLXXXIV packet, but only as a "
            "unit-gauge orbit.  The molar gas constant is the extra strict "
            "closure, and no dimensionful mantissa is promoted as an "
            "independent dimensionless prediction."
        ),
        "legacy_hint_source": (
            "The local untracked legacy MCCCLXXXIV script is treated as a hint "
            "table, not as tracked doctrine, because its universal headline "
            "overstates what dimensionful SI mantissas can prove."
        ),
        "unit_gauge_orbit": unit_gauge_orbit,
        "legacy_reconciliation": reconciled,
        "checks": checks,
        "verified": sum(value is True for value in checks.values()),
        "total_checks": len(checks),
        "all_verified": all(value is True for value in checks.values()),
    }


def main() -> None:
    payload = generate_payload()
    out = Path("data") / "w33_MCCCLXXXV_unit_gauge_witness_boundary.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("MCCCLXXXV: UNIT-GAUGE WITNESS BOUNDARY")
    print(f"verified: {payload['verified']}/{payload['total_checks']}")
    for item in payload["legacy_reconciliation"]:
        print(
            f"  {item['legacy_name']} -> {item['strict_name']}: "
            f"{item['strict_computed']} match={item['match']} class={item['strict_class']}"
        )
    print(f"  strict extra: {payload['unit_gauge_orbit']['strict_extra_names']}")
    if not payload["all_verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
