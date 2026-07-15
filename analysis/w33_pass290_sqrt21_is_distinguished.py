#!/usr/bin/env python3
"""Pass 290: sqrt(21) is the UNIQUE field shared by both Szilassi realizations.

Pass 286 retracted Passes 279/285 and established that sqrt(21) really does live
in the substrate -- in the edge lengths of both Szilassi realizations.  The
obvious follow-up: is it distinguished, or just one of many irrational edge
lengths in a pile?  This witness settles it with a full quadratic-field census.

For each of the SEVEN realizations (5 Csaszar + 2 Szilassi) we factor every one
of the 21 edge lengths into the squarefree d with the length in Q(sqrt d), and
tabulate which fields appear where.

RESULT.  36 distinct quadratic fields appear across the seven realizations, and

    sqrt(21) is the ONLY field present in BOTH Szilassi realizations.

Every other field occurs in at most one Szilassi.  And sqrt(21) occurs in NONE of
the five Csaszar realizations.  So it is not one of twenty: it is the unique
metric invariant of the Szilassi pole.

THE OSCILLATOR ASYMMETRY.  `w33_genus_ladder_clock.py` already frames Csaszar
and Szilassi as the two poles of a clock oscillator, with the self-dual
tetrahedron (K4 vertices AND K4 faces -- both maximal adjacencies, genus 0) as
the middle, and Csaszar/Szilassi as the genus-1 vertex-complete / face-complete
dual pair.  Combinatorially the two poles are dual and interchangeable.  But
METRICALLY they are not: sqrt(21) sits in both Szilassi realizations and neither
appears in any Csaszar one.  The duality that holds at the level of incidence is
BROKEN at the level of the realization's metric, and sqrt(21) is what breaks it.
"""
from __future__ import annotations
import json
from collections import Counter, defaultdict
from pathlib import Path
import sys
import sympy as sp
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from analysis.w33_pass286_sqrt21_found_retraction import (
    CSASZAR, CSASZAR_FACES, SZILASSI, SZILASSI_FACES, edge_lengths)
OUT = ROOT / "data" / "w33_pass290_sqrt21_is_distinguished.json"

def field_of(L):
    r = sp.radsimp(sp.nsimplify(L))
    if r.is_rational: return 1
    sq = sp.nsimplify(sp.expand(r ** 2))
    if not sq.is_rational: return None
    n, dn = sp.fraction(sp.Rational(sq))
    out = 1
    for p, e in sp.factorint(n * dn).items():
        if e % 2: out *= p
    return int(out)

def main():
    checks = {}
    where = defaultdict(list); per = {}
    for fam, tab, faces in (("Csaszar", CSASZAR, CSASZAR_FACES),
                            ("Szilassi", SZILASSI, SZILASSI_FACES)):
        for ver, V in tab.items():
            L = edge_lengths(V, faces)
            fs = [field_of(x) for x in L]
            c = Counter(fs)
            fields = sorted(k for k in c if k not in (None, 1))
            key = f"{fam}v{ver}"
            per[key] = {"edges": len(L), "fields": fields,
                        "rational_edges": c.get(1, 0),
                        "nested_biquadratic": sum(1 for f in fs if f is None)}
            for f in fields: where[f].append(key)
            checks[f"{key}_has_21_edges"] = len(L) == 21

    both_sz = sorted(d for d, w in where.items()
                     if {"Szilassiv1", "Szilassiv2"} <= set(w))
    only_sz = sorted(d for d, w in where.items() if all("Szilassi" in x for x in w))
    in_csaszar = sorted(d for d, w in where.items() if any("Csaszar" in x for x in w))

    checks["census_covers_7_realizations"] = len(per) == 7
    checks["sqrt21_in_both_szilassi"] = 21 in both_sz
    checks["sqrt21_is_the_ONLY_field_in_both_szilassi"] = both_sz == [21]
    checks["sqrt21_in_no_csaszar"] = 21 not in in_csaszar
    checks["many_fields_total"] = len(where) > 25

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass290.sqrt21_is_distinguished.v1",
        "status": "PASS" if all_pass else "FAIL",
        "headline": (
            f"Across the seven realizations {len(where)} distinct quadratic "
            "fields appear in the edge lengths, and sqrt(21) is the ONLY field "
            "present in BOTH Szilassi realizations. Every other field occurs in "
            "at most one Szilassi, and sqrt(21) occurs in NONE of the five "
            "Csaszar realizations. It is the unique metric invariant of the "
            "Szilassi pole -- not one of twenty."
        ),
        "per_realization": per,
        "field_occurrences": {str(d): where[d] for d in sorted(where)},
        "fields_in_both_szilassi": both_sz,
        "fields_only_in_szilassi": only_sz,
        "total_distinct_fields": len(where),
        "oscillator_asymmetry": (
            "w33_genus_ladder_clock.py frames Csaszar and Szilassi as the two "
            "poles of a clock oscillator whose genus-0 middle is the SELF-DUAL "
            "tetrahedron -- the unique polyhedron with BOTH maximal adjacencies "
            "(K4 vertices and K4 faces), which the two toroidal poles split "
            "between them at genus 1 (Csaszar: every vertex pair adjacent = K7; "
            "Szilassi: every face pair shares an edge). Combinatorially the poles "
            "are dual and interchangeable. METRICALLY THEY ARE NOT: sqrt(21) is "
            "in both Szilassi realizations and in no Csaszar one. The duality "
            "that holds at the level of incidence is BROKEN at the level of the "
            "realization's metric, and sqrt(21) is exactly what breaks it."
        ),
        "why_this_matters": (
            "eps* = (5 - sqrt 21)/2, the FN parameter on the Koide light cone "
            "(Pass 274), lives in Q(sqrt 21). That field is now not merely "
            "PRESENT in the substrate's metric data (Pass 286) but DISTINGUISHED "
            "within it: the single field common to both realizations of the "
            "face-complete toroidal pole. Whether the Koide occurrence and the "
            "Szilassi occurrence are related remains open -- but the "
            "coincidence is now much sharper than 'the integer 21 appears a lot'."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1

if __name__ == "__main__":
    raise SystemExit(main())
