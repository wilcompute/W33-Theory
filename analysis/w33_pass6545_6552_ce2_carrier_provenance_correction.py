#!/usr/bin/env python3
"""Passes 6545--6552: CE2 carrier/provenance correction.

This verifier does NOT re-prove the CE2 equations from a vanished producer.
It certifies what is actually present in the repository and prevents a category
error introduced by later synthetic "anchor-22 W33 orbit" scripts.

Certified repository facts:
  * committed_artifacts/ce2_sparse_local_solutions.json contains 5832 authentic
    sparse local rows on a 27 x 3 carrier/fiber label set;
  * 5184 rows are one-term |1/54| repairs and 648 rows are two-term |1/108|
    repairs, matching the two-family decomposition documented by the global
    cocycle module;
  * the carrier is the E6 minuscule 27-set, coordinatized by the committed
    affine-Heisenberg model; it is NOT the 40-point W(3,3) point set;
  * the committed Schlaefli isomorphism is also 27-point and sends carrier
    label 22 to L_45 (phase 0, half-root type);
  * the corrected anchor script contains only three imported witnesses and
    explicitly does not construct an automorphism orbit;
  * the compact artifact names artifacts/ce2_rational_local_solutions.json as
    its source.  That source and the named producer
    tools/solve_sparse_ce2_all_triples.py are not prerequisites of this
    verifier; their absence in the current checkout is a provenance boundary.

Accordingly this packet certifies the authentic 27x3 object and rejects a
40-point anchor-orbit closure unless an explicit equivariant transport is
provided.  It deliberately does not claim independent global CE2 closure.
"""
from __future__ import annotations

import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOL = ROOT / "committed_artifacts" / "ce2_sparse_local_solutions.json"
HEIS = ROOT / "artifacts" / "e6_cubic_affine_heisenberg_model.json"
SCH = ROOT / "artifacts" / "balanced_orbit_schlafli_isomorphism.json"
ANCHOR = ROOT / "scripts" / "w33_ce2_anchor22_closure.py"
GLOBAL = ROOT / "scripts" / "ce2_global_cocycle.py"
OUT = ROOT / "data" / "PART_W33_PASS6545_6552_CE2_CARRIER_PROVENANCE_CORRECTION.json"


def parse_terms(row):
    vals = []
    for side in ("U", "V"):
        for idx, q in row.get(side, []):
            vals.append((side, int(idx), Fraction(str(q))))
    return vals


def main():
    data = json.loads(SOL.read_text(encoding="utf-8"))
    assert data.get("status") == "ok"
    assert int(data.get("n_entries")) == 5832
    entries = data.get("entries")
    assert isinstance(entries, list) and len(entries) == 5832

    keys = set()
    family = Counter()
    fiber_labels = Counter()
    carrier_labels = Counter()
    for row in entries:
        k = str(row["k"])
        assert k not in keys
        keys.add(k)
        triple = [tuple(map(int, str(p).split(","))) for p in k.split(":")]
        assert len(triple) == 3
        for i, f in triple:
            assert 0 <= i < 27
            assert 0 <= f < 3
            carrier_labels[i] += 1
            fiber_labels[f] += 1
        terms = parse_terms(row)
        mags = [abs(q) for _, _, q in terms]
        if len(terms) == 1 and mags == [Fraction(1, 54)]:
            family["simple_one_term_1/54"] += 1
        elif len(terms) == 2 and all(q == Fraction(1, 108) for q in mags):
            family["fiber_two_term_1/108"] += 1
        else:
            family["other"] += 1

    assert family == Counter({
        "simple_one_term_1/54": 5184,
        "fiber_two_term_1/108": 648,
    })
    assert set(carrier_labels) == set(range(27))
    assert set(fiber_labels) == {0, 1, 2}

    heis = json.loads(HEIS.read_text(encoding="utf-8"))
    hmap = heis.get("e6id_to_heisenberg")
    assert isinstance(hmap, dict) and len(hmap) == 27
    hvecs = set()
    for i in range(27):
        p = hmap[str(i)]
        u = p["u"]
        z = p["z"]
        hvecs.add((int(u[0]) % 3, int(u[1]) % 3, int(z) % 3))
    assert len(hvecs) == 27

    sch = json.loads(SCH.read_text(encoding="utf-8"))
    fmap = sch.get("mapping_full")
    assert isinstance(fmap, dict) and len(fmap) == 27
    assert sch.get("isomorphism_verified") is True
    a22 = fmap["22"]
    assert a22["line"] == ["L", 4, 5]
    assert int(a22["phase"]) == 0
    assert a22["root_type"] == "half"

    anchor_src = ANCHOR.read_text(encoding="utf-8")
    assert "OPEN_BEYOND_THREE_IMPORTED_WITNESSES" in anchor_src
    assert "full_orbit_enumerated':False" in anchor_src
    assert "automorphism_action_constructed':False" in anchor_src
    assert "hard-coded rule on labels 1..39" in anchor_src

    global_src = GLOBAL.read_text(encoding="utf-8")
    assert "5184 / 5832" in global_src
    assert "648 / 5832" in global_src
    assert "_heisenberg_vec_maps" in global_src
    assert "committed_artifacts" in global_src

    missing_source = not (ROOT / str(data.get("source", ""))).exists()
    named_producer = ROOT / "tools" / "solve_sparse_ce2_all_triples.py"
    missing_named_producer = not named_producer.exists()

    result = {
        "passes": "6545-6552",
        "status": "PASS_PROVENANCE_CORRECTION__GLOBAL_CLOSURE_NOT_REPROVED",
        "authentic_committed_object": {
            "rows": len(entries),
            "carrier_labels": 27,
            "fiber_labels": 3,
            "family_counts": dict(family),
            "source_named_by_compact_artifact": data.get("source"),
        },
        "carrier_typing": {
            "graded_E8_sector": "(E6+sl3) + (27x3) + (27*x3*)",
            "ce2_local_label_set": "27 carrier labels x 3 fibers",
            "affine_heisenberg_points": len(hvecs),
            "schlafli_points": len(fmap),
            "anchor_22_schlafli_label": "L45",
            "anchor_22_phase": 0,
            "anchor_22_root_type": "half",
            "not_the_same_as": "40 W(3,3) projective points",
        },
        "synthetic_anchor_lane": {
            "verified_imported_witnesses": 3,
            "full_orbit_enumerated": False,
            "automorphism_action_constructed": False,
            "forty_point_transport_status": "ILL_TYPED_WITHOUT_EXPLICIT_27_TO_40_EQUIVARIANT_MAP",
        },
        "provenance_boundary": {
            "named_source_present_in_current_checkout": not missing_source,
            "named_producer_present_in_current_checkout": not missing_named_producer,
            "independent_all_5832_formula_replay_certified_by_this_packet": False,
            "global_predictor_uses_committed_artifact_as_authoritative_data": True,
        },
        "theorem_boundary": "authentic 27x3 CE2 local object certified; global formula compression remains separate replay obligation",
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
