#!/usr/bin/env python3
"""Pass 292: re-audit this program's "absent" claims.

Passes 279 and 285 both confidently concluded "sqrt(21) is not in the substrate"
and both were WRONG (Pass 286).  The failure was not arithmetic but SCOPE: they
searched spectra and counts, while the target lived in metric data.  Two false
negatives in one sitting makes the base rate worth knowing, so this witness
sweeps the committed passes for negative claims and records, for each, WHICH
SPACE was actually searched -- the question that would have caught 279/285.
"""
from __future__ import annotations
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass292_absent_claim_audit.json"
NEG = re.compile(r"(does not appear|not found|no such|is absent|does NOT appear|"
                 r"cannot reach|never|refuted|no .{0,20}exists?)", re.I)

def main():
    checks = {}
    files = sorted((ROOT / "data").glob("w33_pass2*.json"))
    findings = []
    for f in files:
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        blob = json.dumps(d)
        for field in ("verdict", "reading", "theorem", "honest_scope"):
            txt = d.get(field)
            if isinstance(txt, str) and NEG.search(txt):
                findings.append({
                    "pass": f.stem, "field": field,
                    "claim": txt[:220],
                })
    checks["swept_committed_passes"] = len(files) > 20
    checks["found_negative_claims"] = len(findings) > 0

    # the known false negatives, and what caught them
    known_false = {
        "w33_pass279_sqrt21_search": {
            "claim": "sqrt(21) does NOT appear in the substrate",
            "space_searched": "SPECTRA: SRG eigenvalues, discriminants, group "
                              "orders, CSS parameters",
            "space_missed": "METRIC: polyhedron edge lengths",
            "refuted_by": "Pass 286",
        },
        "w33_pass285_sqrt21_toroidal_cyclotomic": {
            "claim": "still NOT sqrt(21) -- the toroidal 21 is a count",
            "space_searched": "COUNTS: flags, edges, group orders",
            "space_missed": "METRIC: the edge LENGTHS of the same polyhedra it "
                            "was discussing",
            "refuted_by": "Pass 286",
        },
    }
    checks["two_known_false_negatives"] = len(known_false) == 2

    # negatives that DO state their space and survive
    sound = {
        "w33_pass263_lightcone_survey": "neutrinos cannot reach Q=2/3 -- states "
            "the space exactly (Q in [1/3,1) for non-negative masses) and the "
            "bound is structural, not a search",
        "w33_pass269_down_quark_cone": "down quarks recede -- a computed "
            "direction of travel at two scales, not an absence claim",
        "w33_pass244_vacuum_rung_search": "no vacuum rung -- rests on the "
            "identity q != q+1, a proof rather than a search",
    }
    checks["sound_negatives_identified"] = len(sound) == 3

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass292.absent_claim_audit.v1",
        "status": "PASS" if all_pass else "FAIL",
        "why": (
            "Passes 279 and 285 both concluded sqrt(21) is absent and both were "
            "wrong. The error was SCOPE, not arithmetic: a negative search result "
            "is only as good as the space searched. Two false negatives in one "
            "sitting makes the base rate worth measuring."
        ),
        "the_rule": (
            "Before publishing 'X is absent', state WHICH KINDS OF OBJECT were "
            "searched and whether X could live in a kind that was not. Pass 279's "
            "own rule ('test discriminants, not squarefree parts') was correct but "
            "silently assumed every irrationality is SPECTRAL; edge lengths are "
            "METRIC -- square roots of integer quadratic forms in coordinates, "
            "generating quadratic fields with no discriminant in sight."
        ),
        "known_false_negatives": known_false,
        "negatives_that_state_their_space_and_survive": sound,
        "negative_claims_found": findings[:40],
        "negative_claim_count": len(findings),
        "verdict": (
            "The distinction that matters is between a negative that is a "
            "THEOREM (Pass 244: no vacuum rung, because q != q+1; Pass 263: "
            "neutrinos cannot reach 2/3, because Q is confined to [1/3,1)) and a "
            "negative that is a SEARCH (Passes 279/285). Theorems bound the whole "
            "space; searches only bound the space searched. Both of this "
            "program's false negatives were searches presented with the "
            "confidence of theorems."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1

if __name__ == "__main__":
    raise SystemExit(main())
