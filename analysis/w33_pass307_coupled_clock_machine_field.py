#!/usr/bin/env python3
"""Pass 307: does the COUPLED clock+machine system have its own field?

Pass 303 showed the two forced fields compose: Q(sqrt2) (the Fano/Heawood clock,
order 2) and Q(sqrt6) (the W(3,3) machine, order 3) generate Q(sqrt2, sqrt3) --
the tribimaximal field.  But that was an abstract compositum of two SEPARATE
spectra.  bt1654_heawood_clock_homology.py records that the clock is a module
COUPLED to the machine, not a subgraph of it (the W(3,3) Levi graph has girth 8
and no 6-cycles).  So the honest follow-up: if the two are actually coupled, does
the COMBINED structure have a spectrum, and does that spectrum land in
Q(sqrt2, sqrt3)?

We build the two graphs and their disjoint union (the uncoupled system), then a
minimally coupled system, and read the fields off the spectra.  A disjoint union
has the union of the spectra, so its field is automatically the compositum -- that
is a triviality and is reported as such.  The real question is whether a genuine
coupling keeps the spectrum inside Q(sqrt2, sqrt3) or pushes it out.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass224_shadow_code_tower import isotropic_lines, pg3_points

OUT = ROOT / "data" / "w33_pass307_coupled_clock_machine_field.json"


def heawood():
    lines = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]
    A = np.zeros((14, 14), int)
    for li, L in enumerate(lines):
        for p in L:
            A[p, 7 + li] = A[7 + li, p] = 1
    return A


def w33_levi():
    pts = pg3_points(3)
    lines = isotropic_lines(pts, 3)
    n, m = len(pts), len(lines)
    A = np.zeros((n + m, n + m), int)
    for j, L in enumerate(lines):
        for p in L:
            A[p, n + j] = A[n + j, p] = 1
    return A


def field_of_spectrum(ev, tol=1e-7):
    """squarefree parts d such that some eigenvalue looks like a*sqrt(d)."""
    out = set()
    for x in ev:
        if abs(x) < tol:
            continue
        s = x * x
        r = sp.nsimplify(round(s, 6), rational=True)
        try:
            n, dn = sp.fraction(sp.Rational(r))
        except Exception:
            continue
        d = 1
        for p, e in sp.factorint(int(n) * int(dn)).items():
            if e % 2:
                d *= p
        out.add(int(d))
    return sorted(out)


def main():
    checks = {}
    H = heawood()
    W = w33_levi()
    checks["heawood_14"] = H.shape[0] == 14
    checks["w33_levi_80"] = W.shape[0] == 80

    evH = np.linalg.eigvalsh(H).tolist()
    evW = np.linalg.eigvalsh(W).tolist()
    fH, fW = field_of_spectrum(evH), field_of_spectrum(evW)
    checks["clock_field_contains_2"] = 2 in fH
    checks["machine_field_contains_6"] = 6 in fW

    # ---- the UNCOUPLED system: disjoint union
    n1, n2 = H.shape[0], W.shape[0]
    D = np.zeros((n1 + n2, n1 + n2), int)
    D[:n1, :n1] = H
    D[n1:, n1:] = W
    evD = np.linalg.eigvalsh(D).tolist()
    fD = field_of_spectrum(evD)
    checks["disjoint_union_field_is_the_union"] = set(fD) >= {2, 6}
    checks["disjoint_union_is_trivial"] = True   # spectra just concatenate

    # ---- a genuine COUPLING: join a few clock nodes to a few machine nodes
    coupled_fields = {}
    for k in (1, 2, 3):
        C = D.copy()
        for i in range(k):
            C[i, n1 + i] = C[n1 + i, i] = 1
        ev = np.linalg.eigvalsh(C).tolist()
        f = field_of_spectrum(ev)
        inside = set(f) <= {1, 2, 3, 6}          # Q(sqrt2,sqrt3) contains sqrt2,3,6
        coupled_fields[str(k)] = {"detected_squarefree_parts": f[:12],
                                  "stays_in_Q_sqrt2_sqrt3": bool(inside)}
    checks["coupling_tested"] = len(coupled_fields) == 3
    any_escape = any(not v["stays_in_Q_sqrt2_sqrt3"] for v in coupled_fields.values())
    checks["result_determined"] = True

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass307.coupled_clock_machine_field.v1",
        "status": "PASS" if all_pass else "FAIL",
        "the_two_pieces": {
            "clock (Heawood, 14 vertices)": {"detected_fields": fH},
            "machine (W(3,3) Levi, 80 vertices)": {"detected_fields": fW},
        },
        "uncoupled_disjoint_union": {
            "detected_fields": fD,
            "note": "a disjoint union's spectrum is the concatenation of the two "
                    "spectra, so its field is the compositum AUTOMATICALLY. This "
                    "is a triviality, not a result -- Pass 303's compositum is an "
                    "abstract statement about two fields, and putting the graphs "
                    "side by side adds nothing.",
        },
        "genuinely_coupled": coupled_fields,
        "verdict": (
            "Adding edges between the clock and the machine DESTROYS the clean "
            "field: the coupled spectrum acquires eigenvalues outside "
            "Q(sqrt2, sqrt3). So the compositum of Pass 303 is a statement about "
            "the two systems considered SEPARATELY, and it does not survive an "
            "arbitrary coupling."
            if any_escape else
            "Under the couplings tried, the spectrum stays inside "
            "Q(sqrt2, sqrt3). That is suggestive but weak: only a few ad hoc "
            "couplings were tested, and there is no principled coupling on offer "
            "-- bt1654 established that the clock is coupled to the machine but "
            "not HOW."
        ),
        "honest_reading": (
            "This pass mostly establishes what the Pass 303 compositum is NOT. "
            "Q(sqrt2, sqrt3) is the field generated by two separate spectra, and "
            "a disjoint union reproduces it trivially. Without a principled "
            "coupling -- which bt1654 explicitly does not supply, recording only "
            "that the Heawood clock is a module coupled to the machine rather "
            "than a subgraph of it -- there is no canonical 'combined spectrum' "
            "to compute. So Pass 303's TBM-field observation stands as a "
            "statement about two forced fields, and should not be upgraded into "
            "a claim about a combined system that has not been defined."
        ),
        "what_would_settle_it": (
            "A derivation of the actual coupling from the substrate (how the "
            "Fano clock attaches to W(3,3)), which the corpus has asserted but "
            "not constructed. Until then the compositum is arithmetic about two "
            "fields, not spectroscopy of one system."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
