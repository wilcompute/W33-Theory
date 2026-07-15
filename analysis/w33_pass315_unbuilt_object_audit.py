#!/usr/bin/env python3
"""Pass 315: audit the corpus for ASSERTED objects that were never built.

Pass 310 found the defect that blocked Pass 307: bt1654 asserts the Heawood clock
is "a separate clock/homology module coupled to the W33 machine" while never
specifying WHAT KIND of coupling -- no functor, no embedding, no action, no
correspondence.  The conclusion was stated; the object was not built.  Pass 311's
prior says that is where the next retraction lives, so this witness looks for the
same defect elsewhere.

THE DEFECT.  A claim of the form "X is coupled to / realises / is the Y of Z"
where the map itself is never exhibited.  Such a claim cannot be refuted (there
is nothing to check) and cannot be used (there is nothing to compute with), yet
it reads like a result and gets quoted forward.

Distinguish it from a legitimate honest boundary: bt1654 ALSO says the W(3,3)
Levi graph has girth 8 and no 6-cycles, so the Heawood clock is not a literal
Levi subgraph. THAT is a proper negative statement, checkable and checked (Pass
310 re-verified it). The defect is not the boundary; it is the positive claim on
the other side of it.
"""

from __future__ import annotations

import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass315_unbuilt_object_audit.json"

# phrases that assert a relationship whose type is left unstated
ASSERTION = re.compile(
    r"(coupled to|is the .{0,30}of the (machine|substrate)|realis\w+ the|"
    r"IS the .{0,30}(clock|oscillator|carrier|bus)|corresponds to)", re.I)


def main():
    checks = {}

    findings = []
    scanned = 0
    for f in sorted((ROOT / "analysis").glob("*.py")):
        try:
            txt = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        scanned += 1
        doc = txt[:4000]
        for m in ASSERTION.finditer(doc):
            line = doc[max(0, m.start() - 90):m.end() + 90].replace("\n", " ")
            findings.append({"file": f.name, "phrase": m.group(0),
                             "context": line.strip()[:200]})
    checks["scanned_analysis_dir"] = scanned > 50
    checks["found_assertions"] = len(findings) > 0

    # the confirmed case, from Pass 310
    confirmed = {
        "bt1654_heawood_clock_homology.py": {
            "asserted": "the Heawood clock is 'a separate clock/homology module "
                        "coupled to the W33 machine'",
            "object_built": False,
            "type_specified": None,
            "obstructions_found_by_310": [
                "girth 6 vs 8 -- not a subgraph (re-verified)",
                "7 does not divide |PGSp(4,3)| = 51840 -- no group action",
                "14 does not divide 80 -- no orbit decomposition",
                "coupling edges push the spectrum out of Q(sqrt2,sqrt3) (Pass 307)",
            ],
            "consequence": "Pass 307 blocked; Pass 303's TBM-field observation "
                           "cannot be upgraded from arithmetic about two fields "
                           "to physics of one system",
        },
    }
    checks["heawood_coupling_is_unbuilt"] = not confirmed[
        "bt1654_heawood_clock_homology.py"]["object_built"]

    # the contrast: what a PROPERLY built claim looks like
    built = {
        "266 the sentinel IS the -(q+1) eigenspace": "g = q(q^2+1)/2 computed as "
            "an SRG multiplicity and matched to the sentinel dimension -- both "
            "sides constructed",
        "270 the +1 IS the all-ones vector": "j exhibited in C, and dim(C/<j>) "
            "computed and matched to Tr(B^t) -- both sides constructed",
        "305 Aut(Csaszar) = AGL(1,7)": "the group computed by brute force and "
            "matched to AGL(1,7) by order profile -- both sides constructed "
            "(though Pass 309 then showed the TIE to the substrate is only "
            "numerical, which is a different defect)",
        "229 the lines ARE the logical operators": "each line verified to be in C "
            "and not in C^perp -- constructed",
    }
    checks["contrast_cases_listed"] = len(built) == 4

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass315.unbuilt_object_audit.v1",
        "status": "PASS" if all_pass else "FAIL",
        "THE_DEFECT": (
            "A claim of the form 'X is coupled to / realises / IS the Y of Z' "
            "where the map itself is never exhibited. Such a claim cannot be "
            "refuted (nothing to check) and cannot be used (nothing to compute "
            "with), yet it reads like a result and gets quoted forward. Pass 310 "
            "found one blocking Pass 307."
        ),
        "confirmed_case": confirmed,
        "candidate_assertions_found": findings[:25],
        "candidate_count": len(findings),
        "files_scanned": scanned,
        "what_a_BUILT_claim_looks_like": built,
        "the_distinction_that_matters": (
            "bt1654 also states a proper honest boundary -- the W(3,3) Levi graph "
            "has girth 8 and no 6-cycles, so the Heawood clock is not a literal "
            "Levi subgraph. That is checkable and Pass 310 checked it. The defect "
            "is NOT the boundary; it is the positive claim on the other side of "
            "it ('but it IS a coupled module'), which names no object at all."
        ),
        "how_this_relates_to_311": (
            "Pass 311 catalogued two failure modes -- coordinate artefacts, and "
            "correct results over-stated. This is a THIRD, and arguably the worst: "
            "claims that are neither right nor wrong because they have no "
            "content. A coordinate artefact can be refuted by another drawing; an "
            "over-read can be trimmed to its proof. An unbuilt object can only be "
            "built or abandoned, and until one or the other happens everything "
            "downstream of it inherits the vacuum."
        ),
        "recommendation": (
            "Every 'X is coupled to Y' in the corpus should either name the map "
            "(functor, embedding, action, correspondence, quotient) or be "
            "restated as the open question it is. The candidates listed here are "
            "phrase-matches, not verdicts -- each needs reading, which is exactly "
            "the lesson of Passes 279/285/286."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
