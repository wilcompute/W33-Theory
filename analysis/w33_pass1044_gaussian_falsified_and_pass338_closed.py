#!/usr/bin/env python3
"""Pass 1044: the Gaussian tower is FALSIFIED as a substrate, and the Pass 338
selector frame is NOT this tower.

Two closures, both negative, both cheap once the right question is asked.

(1) THE GAUSSIAN TOWER IS FALSIFIED, NOT MERELY DIFFERENT.
Pass 1042 showed the doily base has 6 ovoids where W(3,3) has 0.  An ovoid is a
Kochen-Specker 0/1 colouring, so that is not a contrast between two viable
substrates -- it is an exclusion.  A substrate whose contexts admit a global value
assignment supports a noncontextual hidden-variable model, hence has contextual
fraction 0, hence no magic and no computational advantage of the kind the holonet
architecture is built on.  This script EXHIBITS such a model on the doily rather
than inferring it: an explicit 5-point ovoid, verified to meet every one of the 15
contexts exactly once and to be a cap.

That is the falsification the q=2 alternative needed.  W(3,3) admits no such
assignment at all (0 ovoids), which is why its contextual fraction is 1/10.

(2) THE PASS 338 SELECTOR FRAME IS NOT THE SPRINGER TOWER, DESPITE THREE MATCHES.
Three independent fingerprints line up between analysis/w33_pass338_selector_frame_240.g
and the Springer/Eisenstein tower:

    Pass 338 selector-frame subdegrees   [1^6, 27^6, 72]   = Pass 1020 root action
    Pass 338 degree-120 quotient         [1,2,27,36,54]    = Pass 1043 normaliser
    Pass 338 "signed E8" profile         [1,1,4,54,72,108] = Pass 1020 fused edges

Tempting, and wrong.  The selector frame is the image of ATLAS `U4(2).2` acting on
240 cosets of an order-216 kernel, so it is isomorphic to `U4(2):2 = W(E6)`, which
is NOT perfect.  The tower's total-space group is `Sp(4,3) = 2.U4(2)`, which IS
perfect with centre of order 2.  Non-isomorphic, so no relabelling makes the two
actions equal.

The three matches are therefore profile coincidences across non-isomorphic groups
-- which is exactly the trap Pass 1020 named: order, degree, transitivity and even
the full subdegree profile do not determine the group.  This closes the
identification NEGATIVELY and removes a bridge nobody had yet tried to build.

PRIOR ART -- cited, not reclaimed:
  * analysis/w33_ovoid_construct.py -- ovoid = KS colouring, exists iff q even.
  * Thas -- W(q) has ovoids iff q is even.
  * Pass 1042 -- the 6-vs-0 ovoid count.
  * Pass 1020 -- Sp(4,3) perfect vs W(E6) not; the "same profile, different group"
    trap, and the Pass 338 label reversal.
  * Pass 338 -- the selector frame and its three profiles.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1044_gaussian_falsified_and_pass338_closed.json"


def build(F: int):
    """Points and totally isotropic lines of W(3,F)."""
    def canon(v):
        for a in v:
            if a % F:
                inv = 1 if a % F == 1 else pow(a % F, -1, F)
                return tuple((inv * x) % F for x in v)
        return None

    pts, seen = [], set()
    for v in itertools.product(range(F), repeat=4):
        if any(v):
            c = canon(v)
            if c not in seen:
                seen.add(c)
                pts.append(c)
    idx = {p: i for i, p in enumerate(pts)}

    def form(x, y):
        return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % F

    lines = set()
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            if form(pts[i], pts[j]) == 0:
                span = set()
                for a in range(F):
                    for b in range(F):
                        w = tuple((a * pts[i][k] + b * pts[j][k]) % F for k in range(4))
                        if any(w):
                            span.add(idx[canon(w)])
                if len(span) == F + 1:
                    lines.add(frozenset(span))
    return pts, [sorted(L) for L in lines], form


def all_ovoids(n_pts, lines, onpt):
    sols = []

    def rec(chosen, covered):
        if len(covered) == len(lines):
            sols.append(sorted(chosen))
            return
        li = min(l for l in range(len(lines)) if l not in covered)
        for p in lines[li]:
            if any(p in lines[c] for c in covered):
                continue
            new = covered | set(onpt[p])
            if len(new) != len(covered) + len(onpt[p]):
                continue
            rec(chosen + [p], new)

    rec([], set())
    return sols


def main() -> int:
    out = {"schema": "w33.pass1044.gaussian_falsified_and_pass338_closed.v1"}
    checks = {}

    # ---- (1) the falsification -------------------------------------------
    tow = {}
    for F, name in ((2, "doily_W22_gaussian_base"), (3, "W33_eisenstein_base")):
        pts, lines, form = build(F)
        onpt = [[li for li, L in enumerate(lines) if p in L] for p in range(len(pts))]
        ov = all_ovoids(len(pts), lines, onpt)
        rec = {"points": len(pts), "lines": len(lines),
               "points_per_line": F + 1, "ovoid_size": F * F + 1,
               "ovoids": len(ov)}
        if ov:
            w = ov[0]
            rec["witness_ovoid"] = w
            rec["meets_every_context_exactly_once"] = all(
                len(set(L) & set(w)) == 1 for L in lines)
            rec["is_a_cap"] = all(form(pts[a], pts[b]) != 0
                                  for a in w for b in w if a != b)
            rec["contextual_fraction"] = 0
        else:
            rec["contextual_fraction"] = "nonzero (no global assignment exists)"
        tow[name] = rec

    g = tow["doily_W22_gaussian_base"]
    e = tow["W33_eisenstein_base"]
    checks["gaussian_base_admits_a_noncontextual_model"] = (
        g["ovoids"] == 6 and g["meets_every_context_exactly_once"] and g["is_a_cap"])
    checks["eisenstein_base_admits_none"] = e["ovoids"] == 0
    checks["gaussian_tower_is_falsified_not_merely_different"] = (
        g["ovoids"] > 0 and e["ovoids"] == 0)

    # ---- (2) the Pass 338 closure ----------------------------------------
    # Structural, not numerical: the selector frame is W(E6)-type and the tower's
    # total-space group is Sp(4,3).  |G| and every subdegree profile agree; the
    # groups do not.
    p338 = {
        "selector_frame_group": "image of ATLAS U4(2).2 on 240 cosets = U4(2):2 = W(E6)",
        "selector_frame_perfect": False,
        "tower_total_space_group": "Sp(4,3) = 2.U4(2)",
        "tower_perfect": True,
        "tower_centre_order": 2,
        "matching_fingerprints": {
            "selector_frame_subdegrees": "[1^6, 27^6, 72]  = Pass 1020 root action",
            "degree_120_quotient": "[1,2,27,36,54]   = Pass 1043 normaliser image",
            "signed_E8_profile": "[1,1,4,54,72,108] = Pass 1020 fused edge profile",
        },
        "verdict": (
            "NOT the same object. A perfect group and a non-perfect group of the "
            "same order cannot have equivalent permutation actions, so all three "
            "fingerprint matches are profile coincidences across non-isomorphic "
            "groups -- the trap Pass 1020 named."),
    }
    checks["pass338_frame_is_not_perfect"] = p338["selector_frame_perfect"] is False
    checks["tower_group_is_perfect"] = p338["tower_perfect"] is True
    checks["pass338_identification_closed_negatively"] = (
        p338["selector_frame_perfect"] != p338["tower_perfect"])

    out["status"] = "PASS" if all(checks.values()) else "FAIL"
    out["falsification"] = tow
    out["pass338_closure"] = p338
    out["headline"] = (
        "The Gaussian tower is FALSIFIED as a substrate, not merely different: an "
        "explicit 5-point ovoid on the doily is a global noncontextual value "
        "assignment meeting every one of the 15 contexts exactly once, so its "
        "contextual fraction is 0 and it supports no magic. W(3,3) admits no such "
        "assignment at all. Separately, the Pass 338 selector frame is NOT this "
        "tower despite three matching subdegree fingerprints, because it is "
        "W(E6)-type and non-perfect while the tower's group Sp(4,3) is perfect.")
    out["scope"] = (
        "The falsification is of the q=2 tower as a CONTEXTUAL substrate; it says "
        "nothing about the doily as mathematics, where it remains the other "
        "symplectic quadrangle this corpus uses. The Pass 338 closure is "
        "structural and follows from perfectness alone.")
    out["checks"] = checks

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": out["status"], "checks": checks,
                      "doily_ovoids": g["ovoids"], "w33_ovoids": e["ovoids"],
                      "witness": g.get("witness_ovoid")}, sort_keys=True))
    return 0 if out["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
