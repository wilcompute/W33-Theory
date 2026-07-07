#!/usr/bin/env python3
"""BT1812: Sixth Ring claim firewall.

BT1806 opened a useful physics-facing Sixth Ring, but some labels such as EXACT
mix two different notions: exact internal substrate arithmetic and external
physics identification. This firewall keeps the work valuable by splitting every
BT1806-style claim into public tiers.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

OUT = Path("data/PART_BT1812_SIXTH_RING_CLAIM_FIREWALL_results.json")

TIERS = {
    "T0_EXECUTABLE": "machine-checked or directly executable finite W33 result",
    "T1_ARITHMETIC": "exact arithmetic identity in the chosen parameter table",
    "T2_PHENOMENOLOGY": "comparison to external measured values; not a derivation",
    "T3_SPECULATIVE_IDENTIFICATION": "physics identification requiring an independent derivation or experiment",
    "T4_QUARANTINE": "keep as a research note only until a verifier or source audit exists",
}

CLAIMS = [
    {
        "file": "analysis/w33_yukawa_sector.py",
        "claim": "q = 3 and the W33 parameter table identities",
        "old_label": "EXACT",
        "tier": "T1_ARITHMETIC",
        "public_language": "exact substrate arithmetic, not by itself a Standard Model derivation",
    },
    {
        "file": "analysis/w33_yukawa_sector.py",
        "claim": "CKM rank / Yukawa matrix rank equals q=3",
        "old_label": "EXACT",
        "tier": "T3_SPECULATIVE_IDENTIFICATION",
        "public_language": "candidate identification of W33 triality with three generations",
        "demotion_reason": "The arithmetic q=3 is exact; identifying it with CKM/Yukawa rank is a physics bridge.",
    },
    {
        "file": "analysis/w33_yukawa_sector.py",
        "claim": "mt/mW, Vus, top Yukawa order estimates",
        "old_label": "APPROXIMATE",
        "tier": "T2_PHENOMENOLOGY",
        "public_language": "phenomenological numerology/fit target; compare but do not call derived",
    },
    {
        "file": "analysis/w33_yukawa_sector.py",
        "claim": "bottom, tau, Vub, weak-angle estimates",
        "old_label": "SPECULATIVE",
        "tier": "T3_SPECULATIVE_IDENTIFICATION",
        "public_language": "research-direction only until RG/scale-setting mechanism is supplied",
    },
    {
        "file": "analysis/w33_neutrino_mass_ratios.py",
        "claim": "N_nu = q = 3",
        "old_label": "EXACT",
        "tier": "T3_SPECULATIVE_IDENTIFICATION",
        "public_language": "exact q=3 substrate count; neutrino-family identification is speculative",
        "demotion_reason": "The measured number of light neutrinos is external physics, not an automatic theorem of W33.",
    },
    {
        "file": "analysis/w33_neutrino_mass_ratios.py",
        "claim": "normal hierarchy selector",
        "old_label": "EXACT",
        "tier": "T2_PHENOMENOLOGY",
        "public_language": "testable phenomenological selector, not yet a mass-matrix derivation",
        "demotion_reason": "Needs an explicit neutrino mass operator and uncertainty/source audit.",
    },
    {
        "file": "analysis/w33_neutrino_mass_ratios.py",
        "claim": "Dirac/Majorana statement from p-adic monodromy",
        "old_label": "SPECULATIVE",
        "tier": "T4_QUARANTINE",
        "public_language": "do not present publicly without a lepton-number mechanism and source audit",
    },
    {
        "file": "analysis/w33_cosmological_constant.py",
        "claim": "CF = 1/10 and uncovered fraction = 4/40",
        "old_label": "EXACT",
        "tier": "T0_EXECUTABLE",
        "public_language": "exact contextuality-tax/substrate result",
    },
    {
        "file": "analysis/w33_cosmological_constant.py",
        "claim": "w_DE = -1 from diagonal Hodge structure",
        "old_label": "EXACT",
        "tier": "T3_SPECULATIVE_IDENTIFICATION",
        "public_language": "candidate physics identification; exact only after a verified Hodge-to-FRW derivation",
        "demotion_reason": "The Hodge arithmetic and the cosmological equation-of-state identification are different claims.",
    },
    {
        "file": "analysis/w33_cosmological_constant.py",
        "claim": "rho_vac/rho_Pl ~ CF^4 and Lambda_W scale",
        "old_label": "SPECULATIVE",
        "tier": "T4_QUARANTINE",
        "public_language": "research scratchpad; currently off by the known cosmological-constant hierarchy without a suppression mechanism",
    },
]


def theorem_summary():
    tier_counts = Counter(c["tier"] for c in CLAIMS)
    old_label_counts = Counter(c["old_label"] for c in CLAIMS)
    demotions = [c for c in CLAIMS if c.get("demotion_reason")]
    assert set(tier_counts) <= set(TIERS)
    assert all("public_language" in c for c in CLAIMS)
    assert len(demotions) >= 4
    return {
        "theorem": "BT1812 Sixth Ring Claim Firewall",
        "tier_definitions": TIERS,
        "claim_count": len(CLAIMS),
        "old_label_counts": dict(old_label_counts),
        "tier_counts": dict(tier_counts),
        "demoted_claim_count": len(demotions),
        "claims": CLAIMS,
        "public_rule": "Only T0/T1 may be stated as exact. T2 may be stated as comparison/phenomenology. T3/T4 must be explicitly labelled speculative or quarantined.",
        "checks": {
            "every_claim_has_tier": True,
            "every_claim_has_public_language": True,
            "physics_identifications_demoted_from_exact_where_needed": True,
        },
        "honest_scope": "This is a claim-tier firewall, not a refutation of the research direction. It preserves exact Holonet results while preventing public overclaiming."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
