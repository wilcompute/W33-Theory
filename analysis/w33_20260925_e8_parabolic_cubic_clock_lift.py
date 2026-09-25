#!/usr/bin/env python3
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_20260925_e8_parabolic_cubic_clock_lift.json"

SC = ROOT / "artifacts/e8_structure_constants_w33_discrete.json"
META = ROOT / "extracted_v13/W33-Theory-master/artifacts/e8_root_metadata_table.json"
CANON = ROOT / "extracted_v13/W33-Theory-master/artifacts/canonical_su3_gauge_and_cubic.json"

SIGNATURE = {-3:2,-2:27,-1:54,0:74,1:54,2:27,3:2}

def source_bracket(table, a, b):
    if a == b:
        return []
    s = 1 if a < b else -1
    return [(k, s*c) for k,c in table.get((min(a,b), max(a,b)), [])]

def nested_coeff(table, a, b, c, allowed_top):
    out = []
    for mid, x in source_bracket(table, a, b):
        for top, y in source_bracket(table, mid, c):
            if top in allowed_top:
                out.append((top, x*y))
    return out
def main():
    sc = json.loads(SC.read_text())
    meta = json.loads(META.read_text())
    canon = json.loads(CANON.read_text())

    roots = [tuple(map(int, r)) for r in sc["basis"]["roots"]]
    assert len(roots) == 240
    byroot = {tuple(r["root_orbit"]): r for r in meta["rows"]}
    assert set(roots) == set(byroot)

    candidates = []
    for j in range(8):
        h = Counter(r[j] for r in roots)
        if all(h[k] == v for k,v in SIGNATURE.items()):
            candidates.append(j)
    assert candidates == [6]
    node = candidates[0]

    hist = Counter(r[node] for r in roots)
    assert dict(sorted(hist.items())) == SIGNATURE
    lie_dims = {str(k): hist[k] + (8 if k == 0 else 0) for k in range(-3,4)}
    assert [lie_dims[str(k)] for k in range(-3,4)] == [2,27,54,82,54,27,2]

    # The already-frozen CE2 grading is exactly this integer grading modulo three.
    archived_pairs = Counter((r[node] % 3, byroot[r]["grade"]) for r in roots)
    assert archived_pairs == Counter({(0,"g0"):78,(1,"g1"):81,(2,"g2"):81})
    split = {
        "g0": Counter(r[node] for r in roots if byroot[r]["grade"] == "g0"),
        "g1": Counter(r[node] for r in roots if byroot[r]["grade"] == "g1"),
        "g2": Counter(r[node] for r in roots if byroot[r]["grade"] == "g2"),
    }
    assert split["g0"] == Counter({0:74,-3:2,3:2})
    assert split["g1"] == Counter({1:54,-2:27})
    assert split["g2"] == Counter({-1:54,2:27})

    # The 54 first-order roots are literally 27 histories times the two
    # unselected external-qutrit labels.  The remaining label is grade +2.
    plus1 = [8+i for i,r in enumerate(roots) if r[node] == 1]
    plus2 = [8+i for i,r in enumerate(roots) if r[node] == 2]
    plus3 = [8+i for i,r in enumerate(roots) if r[node] == 3]
    idxmeta = {8+i: byroot[r] for i,r in enumerate(roots)}
    assert len(plus1) == 54 and len(plus2) == 27 and len(plus3) == 2
    assert Counter(idxmeta[i]["i3"] for i in plus1) == Counter({0:27,1:27})
    assert Counter(idxmeta[i]["i3"] for i in plus2) == Counter({2:27})
    assert {idxmeta[i]["i27"] for i in plus1 if idxmeta[i]["i3"] == 0} == set(range(27))
    assert {idxmeta[i]["i27"] for i in plus1 if idxmeta[i]["i3"] == 1} == set(range(27))
    assert {idxmeta[i]["i27"] for i in plus2} == set(range(27))
    table = {}
    for key, terms in sc["brackets"].items():
        a,b = map(int, key.split(","))
        table[(a,b)] = [(int(k), int(c)) for k,c in terms]

    # Every committed Chevalley structure constant respects the integer lift.
    degree = [0]*8 + [r[node] for r in roots]
    checked_terms = 0
    for (a,b), terms in table.items():
        for k,c in terms:
            checked_terms += 1
            assert degree[k] == degree[a] + degree[b]
    assert checked_terms == 8347

    # First brackets: g_1 x g_1 -> g_2 is onto, with uniform multiplicity ten.
    pair_outputs = Counter()
    for ia,a in enumerate(plus1):
        for b in plus1[ia+1:]:
            for k,c in source_bracket(table, a, b):
                if k in plus2:
                    pair_outputs[k] += 1
    assert len(pair_outputs) == 27
    assert Counter(pair_outputs.values()) == Counter({10:27})
    assert sum(pair_outputs.values()) == 270

    # Second brackets: g_1 x g_2 -> g_3 is onto both clock directions.
    top_outputs = Counter()
    for a in plus1:
        for b in plus2:
            for k,c in source_bracket(table, a, b):
                if k in plus3:
                    top_outputs[k] += 1
    assert len(top_outputs) == 2
    assert sorted(top_outputs.values()) == [27,27]

    # All nested nonzero triples land on exactly the 45 canonical E6 cubic triads.
    triad_mult = Counter()
    ext_mult = Counter()
    nested_top_mult = Counter()
    for ia,a in enumerate(plus1):
        for b in plus1[ia+1:]:
            for mid,c1 in source_bracket(table, a, b):
                if mid not in plus2:
                    continue
                for c in plus1:
                    for top,c2 in source_bracket(table, mid, c):
                        if top not in plus3:
                            continue
                        tri = tuple(sorted((
                            idxmeta[a]["i27"], idxmeta[b]["i27"], idxmeta[c]["i27"]
                        )))
                        ext = tuple(sorted((
                            idxmeta[a]["i3"], idxmeta[b]["i3"], idxmeta[c]["i3"]
                        )))
                        triad_mult[tri] += 1
                        ext_mult[ext] += 1
                        nested_top_mult[top] += 1

    canonical_triads = {tuple(sorted(map(int,t))) for t in canon["triads"]}
    assert set(triad_mult) == canonical_triads
    assert len(canonical_triads) == 45
    assert Counter(triad_mult.values()) == Counter({12:45})
    assert ext_mult == Counter({(0,0,1):270,(0,1,1):270})
    assert sorted(nested_top_mult.values()) == [270,270]

    # Fix the repository's canonical ordering i<j<k.  The nested bracket
    # coefficient is exactly the signed E6 cubic coefficient, up to the
    # external antisymmetric orientation sign.
    dsign = {
        tuple(sorted(map(int,x["triple"]))): int(x["sign"])
        for x in canon["solution"]["d_triples"]
    }
    assert set(dsign) == canonical_triads
    g1label = {(idxmeta[a]["i27"], idxmeta[a]["i3"]): a for a in plus1}
    sign_checks = Counter()
    pattern_specs = [
        ((0,1,0), plus3[1], -1),
        ((0,1,1), plus3[0], -1),
        ((1,0,0), plus3[1], +1),
        ((1,0,1), plus3[0], +1),
    ]
    for tri in sorted(canonical_triads):
        i,j,k = tri
        for pat, expected_top, expected_ratio in pattern_specs:
            a,b,c = [g1label[(q,t)] for q,t in zip((i,j,k),pat)]
            rows = nested_coeff(table, a, b, c, set(plus3))
            assert len(rows) == 1
            top, coeff = rows[0]
            assert top == expected_top
            ratio = coeff * dsign[tri]
            assert ratio == expected_ratio
            sign_checks[(pat, top, ratio)] += 1
    assert set(sign_checks.values()) == {45}

    out = {
      "schema":"w33.20260925.e8_parabolic_cubic_clock_lift.v1",
      "status":"PASS_CE2_Z3_IS_MOD3_SHADOW_OF_EXACT_E8_THREE_STEP_CUBIC_CLOCK_GRADING",
      "grading":{
        "source_simple_root_coordinate":node,
        "integer_root_histogram":{str(k):hist[k] for k in range(-3,4)},
        "integer_lie_dimensions":lie_dims,
        "mod3_dimensions":{"g0":86,"g1":81,"g2":81},
        "mod3_split":{
          "g0":"82_integer_grade0 + 2_grade+3 + 2_grade-3 = 86",
          "g1":"54_grade+1 + 27_grade-2 = 81",
          "g2":"54_grade-1 + 27_grade+2 = 81",
        },
        "all_committed_structure_constant_terms_respect_integer_grade":True,
        "structure_constant_terms_checked":checked_terms,
      },
      "selected_now_decomposition":{
        "grade_plus1_dimension":54,
        "formula":"54 = 27 histories x 2 remaining external-qutrit labels",
        "grade_plus1_external_labels":{"0":27,"1":27},
        "grade_plus2_dimension":27,
        "grade_plus2_external_label":{"2":27},
        "grade_plus3_dimension":2,
        "reading":"choosing external label 2 as the selected ray refines 3 -> 2 + 1",
      },
      "bracket_growth":{
        "g1_dimension":54,
        "g2_dimension":27,
        "g3_dimension":2,
        "positive_nilradical_dimension":83,
        "nonzero_unordered_g1_g1_pairs":270,
        "g2_output_multiplicity_each":10,
        "nonzero_g1_g2_pairs":54,
        "g3_output_multiplicity_each":27,
        "growth_vector":[54,81,83],
        "surjective_g1g1_to_g2":True,
        "surjective_g1g2_to_g3":True,
      },
      "cubic_clock":{
        "canonical_E6_triads":45,
        "nested_nonzero_channels":sum(triad_mult.values()),
        "each_E6_triad_nested_multiplicity":12,
        "external_patterns":{
          "001":ext_mult[(0,0,1)],
          "011":ext_mult[(0,1,1)],
        },
        "each_top_clock_direction_nested_multiplicity":270,
        "nested_support_equals_canonical_45_E6_cubic_triads":True,
        "coefficient_identity":[
          "[[e_(i,0),e_(j,1)],e_(k,0)] = -d_ijk * T0",
          "[[e_(i,0),e_(j,1)],e_(k,1)] = -d_ijk * T1",
          "[[e_(i,1),e_(j,0)],e_(k,0)] = +d_ijk * T0",
          "[[e_(i,1),e_(j,0)],e_(k,1)] = +d_ijk * T1",
        ],
        "coefficient_identity_checked_on_all_45_triads":True,
      },
      "theorem":(
        "The repository's frozen E6+A2 order-three grading is not merely adjacent "
        "to the 54+27+2 temporal grading: it is exactly its reduction modulo three "
        "on the same Chevalley E8 basis. Choosing one external-qutrit ray refines "
        "the 81-dimensional matter grade into 54 first-order roots and 27 second-order "
        "roots, while two external-A2 roots become the top grade. The executable "
        "Chevalley bracket then has growth 54 -> 81 -> 83, and its nonzero nested "
        "triple support is exactly the 45 signed E6 cubic triads. In the canonical "
        "triad ordering the nested coefficients equal the signed cubic coefficient "
        "times the external orientation sign."
      ),
      "boundary":(
        "This is an exact finite Lie-algebra theorem on the committed E8 basis. "
        "Calling the top two-dimensional layer physical elapsed time remains an "
        "interpretation. No Hamiltonian, vacuum-selection mechanism, CPTP arrow, "
        "energy scale, or laboratory clock calibration is derived here."
      ),
      "parents":[
        "artifacts/e8_structure_constants_w33_discrete.json",
        "extracted_v13/W33-Theory-master/artifacts/e8_root_metadata_table.json",
        "extracted_v13/W33-Theory-master/artifacts/canonical_su3_gauge_and_cubic.json",
        "data/w33_e6_cubic_diagonal_phase_weld.json",
      ],
    }
    OUT.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":out["status"],
      "integer_dimensions":lie_dims,
      "growth":out["bracket_growth"]["growth_vector"],
      "cubic_triads":out["cubic_clock"]["canonical_E6_triads"],
    },indent=2))

if __name__ == "__main__":
    main()
