#!/usr/bin/env python3
"""
The decisive experiment, made concrete: a single-photon protocol for measuring the
contextual fraction 1/Phi_4 = 1/10 on the 40 W(3,3) rays. It specifies the encoding
(two qutrits in one photon), the 40 measurement contexts (the isotropic lines of
W(3,3) = sets of 4 commuting two-qutrit Weyl operators), the Clifford optical setting
per context, the statistic, and the photon budget -- a recipe an experimentalist can
run.

w33_decisive_experiment.py singled out the contextual fraction as the sharpest
near-term test; this turns "measure 1/10" into a protocol.

ENCODING. A single photon carries two ternary registers -- e.g. path (3 paths) and
orbital angular momentum (OAM in {-1,0,+1}) -- giving the two-qutrit Hilbert space
C^3 (x) C^3 = C^9. The 40 W(3,3) points are the 40 two-qutrit Weyl (Heisenberg-Weyl)
operators X^a Z^b (nonzero (a,b) in F_3^4, modulo global phase: (3^4-1)/2 = 40).

CONTEXTS. Two Weyl operators commute iff their symplectic product vanishes iff the
points are collinear in W(3,3). A measurement context is a maximal commuting set = an
isotropic line = 4 Weyl operators (a 2-dim isotropic subspace, (3^2-1)/2 = 4 points).
There are exactly 40 such lines, 4 per point. Each context is a complete two-qutrit
stabiliser basis (9 joint eigenstates).

SETTINGS. Each context is read out by a Clifford (Sp(4,3)) optical transformation --
a tritter on each register plus a controlled phase delay (the universality-theorem
elements) -- that maps the context's 4 commuting Weyls to the computational X,Z
generators, followed by photon-number-resolved detection in the 9 output modes. So
the whole experiment is 40 interferometer settings on the same single-photon source.

STATISTIC. From the 40 context distributions, the contextual fraction CF is the
solution of the standard noncontextuality linear program (Abramsky-Brandenburger):
the minimal weight of the empirical model that cannot be reproduced by a global
(noncontextual) value assignment. The substrate prediction is CF = 1/Phi_4 = 1/10
(the spectral/ratio bound of SRG(40,12,2,4); w33_contextuality_simulation.py). A
measured 1/10 confirms three faces of the Eisenstein object at once; any deviation
falsifies it.

BUDGET. 40 settings; per setting, N photons give the 9-outcome distribution to
precision ~1/sqrt(N). To resolve CF = 0.1 to 1% (0.001) needs ~10^6 photons per
setting, ~4x10^7 total -- seconds at MHz single-photon rates. The observable is a
unit fraction, so no absolute calibration is required: only relative count ratios.

Honest scope: a protocol PROPOSAL grounded in the exact W(3,3) incidence geometry
(the 40 contexts are constructed and verified here); the contextual-fraction value
1/10 is the substrate's spectral prediction. Not a completed measurement -- a recipe.

Verifies the 40 points, the 40 contexts (isotropic lines, 4 commuting Weyls each, 4
per point), and the GQ(3,3) incidence the protocol rests on.
"""
from __future__ import annotations

import itertools
import json


def symplectic(u, v):
    """<u,v> = u1 v3 - u3 v1 + u2 v4 - u4 v2 over F_3."""
    return (u[0] * v[2] - u[2] * v[0] + u[1] * v[3] - u[3] * v[1]) % 3


def proj_points():
    reps = []
    for vec in itertools.product(range(3), repeat=4):
        if all(x == 0 for x in vec):
            continue
        for i in range(4):
            if vec[i]:
                inv = pow(vec[i], 1, 3)  # 3 prime: inverse of 1 is 1, of 2 is 2
                inv = pow(vec[i], 3 - 2, 3)
                rep = tuple((inv * x) % 3 for x in vec)
                break
        if rep not in reps:
            reps.append(rep)
    return reps


def main():
    out = {}

    # the 40 points = two-qutrit Weyl operators
    pts = proj_points()
    n = len(pts)
    idx = {p: i for i, p in enumerate(pts)}
    print(
        f"[encoding]  {n} two-qutrit Weyl operators X^a Z^b = W(3,3) points "
        f"((3^4-1)/2)"
    )
    assert n == 40

    # the contexts = isotropic lines (2-dim totally isotropic subspaces)
    lines = set()
    for a, b in itertools.combinations(range(n), 2):
        u, v = pts[a], pts[b]
        if symplectic(u, v) != 0:
            continue
        # the line through u,v = projective points of span{u,v}; collect the 4 points
        span = set()
        for s in range(3):
            for t in range(3):
                if s == 0 and t == 0:
                    continue
                w = tuple((s * u[i] + t * v[i]) % 3 for i in range(4))
                # normalise to representative
                for i in range(4):
                    if w[i]:
                        invc = pow(w[i], 1, 3)
                        invc = pow(w[i], 3 - 2, 3)
                        w = tuple((invc * x) % 3 for x in w)
                        break
                if w in idx:
                    span.add(idx[w])
        if len(span) == 4:
            lines.add(frozenset(span))
    lines = list(lines)
    print(
        f"[contexts]  {len(lines)} isotropic lines (contexts), each {len(lines[0])} "
        f"commuting Weyls"
    )
    assert len(lines) == 40 and all(len(L) == 4 for L in lines)

    # each point on 4 lines (GQ(3,3) incidence)
    on = {i: 0 for i in range(n)}
    for L in lines:
        for p in L:
            on[p] += 1
    lines_per_point = set(on.values())
    print(f"  lines per point = {lines_per_point} (q+1 = 4)")
    assert lines_per_point == {4}
    out["structure"] = {
        "points_weyls": 40,
        "contexts_lines": 40,
        "weyls_per_context": 4,
        "contexts_per_weyl": 4,
    }

    # the protocol spec
    print(f"\n[protocol]")
    print(f"  carrier: 1 photon, 2 qutrits (path (x) OAM = C^9)")
    print(f"  observables: 40 two-qutrit Weyls; contexts: 40 commuting-4 lines")
    print(f"  settings: 40 Clifford (Sp(4,3)) optical settings (tritter+phase),")
    print(f"            PNR detection in 9 modes")
    print(f"  statistic: noncontextuality LP -> contextual fraction CF")
    print(f"  prediction: CF = 1/Phi_4 = 1/10 (spectral bound of SRG(40,12,2,4))")
    print(
        f"  budget: ~10^6 photons/setting, ~4x10^7 total; unit-fraction (no calibration)"
    )
    out["protocol"] = {
        "carrier": "single photon, 2 qutrits (path x OAM = C^9)",
        "settings": 40,
        "detection": "PNR in 9 modes",
        "statistic": "noncontextuality LP (Abramsky-Brandenburger)",
        "prediction": "CF = 1/Phi_4 = 1/10",
        "budget": "~1e6 photons/setting, ~4e7 total; calibration-free unit fraction",
    }
    out["discriminates"] = "q=2 contextuality-free; q=5 -> 1/26; generic SRG -> != 1/10"

    print("\nRESULT: the contextual-fraction experiment is a concrete single-photon")
    print("  protocol. Encode two qutrits in one photon (path (x) OAM, C^9); the 40")
    print(
        "  W(3,3) points are the 40 two-qutrit Weyl operators, and the 40 contexts are"
    )
    print(
        "  the isotropic lines -- 4 commuting Weyls each, 4 lines per Weyl, the GQ(3,3)"
    )
    print(
        "  incidence verified here. Read each context with one Clifford optical setting"
    )
    print(
        "  (tritter + phase delay, the universality-theorem elements) and photon-number"
    )
    print("  detection in 9 modes; 40 settings in all. The noncontextuality linear")
    print(
        "  program over the 40 distributions returns the contextual fraction, predicted"
    )
    print(
        "  to be the unit fraction 1/Phi_4 = 1/10 -- calibration-free, ~4x10^7 photons,"
    )
    print(
        "  seconds at MHz rates. Measuring 1/10 confirms three faces of the Eisenstein"
    )
    print(
        "  object; a deviation falsifies it. The decisive experiment is now a recipe."
    )

    out["summary"] = (
        "concrete single-photon protocol for the contextual fraction 1/10: encode 2 "
        "qutrits in one photon (path x OAM = C^9); the 40 W(3,3) points are the 40 "
        "two-qutrit Weyl operators, the 40 contexts are the isotropic lines (4 commuting "
        "Weyls each, 4 per Weyl -- GQ(3,3) incidence verified). 40 Clifford (Sp(4,3)) "
        "optical settings (tritter+phase) + PNR detection in 9 modes; the "
        "noncontextuality LP over the 40 distributions returns CF = 1/Phi_4 = 1/10 "
        "(spectral bound). Calibration-free unit fraction, ~1e6 photons/setting (~4e7 "
        "total), seconds at MHz rates. Measuring 1/10 confirms three faces; deviation "
        "falsifies. Honest: a verified-geometry protocol proposal, not a completed "
        "measurement."
    )
    out["sources"] = [
        "two-qutrit Weyl operators = W(3,3)=GQ(3,3) points (40); isotropic lines = "
        "commuting contexts; contextual fraction = Abramsky-Brandenburger LP; substrate "
        "CF=1/Phi_4=1/10 (w33_contextuality_simulation.py, "
        "w33_demonstrator_substrate_constants.py); Clifford optics = Sp(4,3) "
        "(universality theorem, bt825); single-photon path/OAM qutrits; "
        "w33_decisive_experiment.py."
    ]
    with open("data/w33_contextuality_protocol.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_contextuality_protocol.json")


if __name__ == "__main__":
    main()
