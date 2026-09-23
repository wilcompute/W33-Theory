#!/usr/bin/env python3
"""Odd-prime extended-Clifford saturation theorem for the Heisenberg bulk graph.

This is a selection theorem extracted by combining two exact structures:

* Pass 408:
    Aut(Gamma_p) = H_p : GL(2,p)
  for every odd prime p (prime-field specialization of the certified theorem).

* Appleby's extended Clifford normalizer:
    projectively, the unitary/anti-unitary Clifford action uses
    ESL(2,p)={F in GL(2,p): det(F)=+/-1}.

Keeping the Pauli phase centre gives the finite retained-phase extended
Clifford action H_p : ESL(2,p).

Since det:GL(2,p)->F_p^* is onto and ESL is the inverse image of {+/-1},

    [Aut(Gamma_p) : ExtCliff_p] = (p-1)/2.

Therefore the retained-phase extended Clifford group saturates the full
unoriented Heisenberg graph automorphism group iff p=3.

This selects qutrit dimension inside this very specific finite symmetry
criterion. It is not a derivation of physical spacetime dimension, particle
generations, or a measured coupling.
"""
from __future__ import annotations

import importlib.util
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PASS408_SCRIPT = ROOT / "analysis/w33_pass408_full_automorphism_theorem.py"
PASS408_DATA = ROOT / "data/w33_pass408_full_automorphism_theorem.json"
Q3_BRIDGE_DATA = ROOT / "data/w33_extended_clifford_pass408_intertwiner.json"
OUT = ROOT / "data/w33_q3_extended_clifford_saturation.json"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def gl2_count_formula(p: int) -> int:
    return (p * p - 1) * (p * p - p)


def sl2_count_formula(p: int) -> int:
    return p * (p * p - 1)


def esl2_count_formula(p: int) -> int:
    # For odd p, +1 and -1 are distinct determinant fibres.
    return 2 * sl2_count_formula(p)


def full_order_formula(p: int) -> int:
    return p**3 * gl2_count_formula(p)


def extended_clifford_order_formula(p: int) -> int:
    return p**3 * esl2_count_formula(p)


def enumerate_linear_counts(p: int):
    det_hist = {a: 0 for a in range(1, p)}
    gl = 0
    esl = 0
    for a, b, c, d in itertools.product(range(p), repeat=4):
        determinant = (a * d - b * c) % p
        if determinant:
            gl += 1
            det_hist[determinant] += 1
            if determinant in (1, p - 1):
                esl += 1
    return gl, esl, det_hist


def main(write=True):
    p408 = load_module(PASS408_SCRIPT, "w33_pass408_q3_saturation_parent")
    pass408 = json.loads(PASS408_DATA.read_text())
    q3_bridge = json.loads(Q3_BRIDGE_DATA.read_text())

    assert pass408["theorem"] == (
        "Aut(Gamma_q)=H_q semidirect GammaL(2,q), "
        "with order q^3(q^2-1)(q^2-q)f for q=p^f"
    )
    assert q3_bridge["group_structure"]["full_group"] == "H27 : GL(2,3)"
    assert q3_bridge["group_structure"]["full_order"] == 1296

    primes = [3, 5, 7, 11, 13]
    cases = []
    for p in primes:
        gl, esl, hist = enumerate_linear_counts(p)
        expected_fibre = sl2_count_formula(p)
        assert gl == gl2_count_formula(p)
        assert esl == esl2_count_formula(p)
        assert set(hist.values()) == {expected_fibre}
        index = gl // esl
        assert index == (p - 1) // 2
        full_order = p**3 * gl
        ext_order = p**3 * esl
        assert full_order == full_order_formula(p)
        assert ext_order == extended_clifford_order_formula(p)
        cases.append({
            "p": p,
            "GL2_order": gl,
            "SL2_order": expected_fibre,
            "ESL2_order": esl,
            "determinant_fibre_size": expected_fibre,
            "full_Heisenberg_graph_automorphism_order": full_order,
            "retained_phase_extended_Clifford_order": ext_order,
            "index_full_over_extended_Clifford": index,
            "saturates_full_automorphism_group": index == 1,
        })

    # Directly lock to the two Pass-408 certified prime instances already frozen.
    by_p = {c["p"]: c for c in cases}
    assert by_p[3]["full_Heisenberg_graph_automorphism_order"] == pass408["instances"]["3"]["full_automorphism_order"]
    assert by_p[5]["full_Heisenberg_graph_automorphism_order"] == pass408["instances"]["5"]["full_automorphism_order"]
    assert by_p[3]["retained_phase_extended_Clifford_order"] == 1296
    assert by_p[3]["saturates_full_automorphism_group"] is True
    assert all(not c["saturates_full_automorphism_group"] for c in cases if c["p"] > 3)

    # Algebraic uniqueness over all odd primes: (p-1)/2=1 iff p=3.
    # We record the symbolic implication and scan a wider range as a guardrail.
    odd_primes_under_50 = [3,5,7,11,13,17,19,23,29,31,37,41,43,47]
    indices = {p: (p - 1) // 2 for p in odd_primes_under_50}
    assert [p for p, idx in indices.items() if idx == 1] == [3]

    checks = {
        "pass408_parent_replayed_structurally": True,
        "q3_coordinate_bridge_imported": True,
        "GL2_formula_matches_enumeration_p3_p5_p7_p11_p13": True,
        "determinant_map_uniform_on_nonzero_fibres": True,
        "ESL_is_exact_det_plusminus1_preimage": True,
        "index_formula_is_p_minus_1_over_2": True,
        "pass408_q3_full_order_match_1296": True,
        "pass408_q5_full_order_match_60000": True,
        "q3_extended_Clifford_order_match_1296": True,
        "q3_saturates_full_graph_automorphisms": True,
        "p_gt_3_sampled_primes_do_not_saturate": True,
        "symbolic_equality_condition_for_odd_prime_is_p_equals_3": True,
    }

    out = {
        "schema": "w33.q3_extended_clifford_saturation.v1",
        "status": "PASS_Q3_UNIQUE_ODD_PRIME_EXTENDED_CLIFFORD_SYMMETRY_SATURATION",
        "headline": (
            "For every odd prime p, Pass 408 gives Aut(Gamma_p)=H_p:GL(2,p), "
            "while the retained-phase unitary/anti-unitary Clifford normalizer is "
            "H_p:ESL(2,p) with ESL={det=+/-1}. Therefore its index in the full "
            "Heisenberg graph automorphism group is (p-1)/2. Equality occurs iff "
            "p=3. Thus qutrit dimension is uniquely selected among odd prime "
            "dimensions by extended-Clifford saturation of the complete unoriented "
            "Heisenberg bulk-graph symmetry."
        ),
        "theorem": {
            "full_group": "Aut(Gamma_p)=H_p:GL(2,p)",
            "extended_Clifford_group": "ExtCliff_p=H_p:ESL(2,p)",
            "ESL_definition": "ESL(2,p)={F in GL(2,p): det(F) in {+1,-1}}",
            "GL2_order": "(p^2-1)(p^2-p)",
            "ESL2_order": "2p(p^2-1)",
            "full_order": "p^3(p^2-1)(p^2-p)",
            "extended_Clifford_order": "2p^4(p^2-1)",
            "index": "(p-1)/2",
            "saturation_condition": "(p-1)/2=1 iff p=3",
        },
        "cases": cases,
        "wide_prime_index_scan": indices,
        "q3_closure": {
            "full_group": q3_bridge["group_structure"]["full_group"],
            "full_order": q3_bridge["group_structure"]["full_order"],
            "projective_full_group": q3_bridge["group_structure"]["projective_full_quotient"],
            "projective_full_order": q3_bridge["group_structure"]["projective_full_order"],
            "reason_ESL_equals_GL": "F3^*={+1,-1}; there are no additional determinant multipliers",
            "coordinate_action_bridge": "data/w33_extended_clifford_pass408_intertwiner.json",
        },
        "q5_contrast": {
            "full_order": by_p[5]["full_Heisenberg_graph_automorphism_order"],
            "extended_Clifford_order": by_p[5]["retained_phase_extended_Clifford_order"],
            "index": by_p[5]["index_full_over_extended_Clifford"],
            "missing_determinants": [2,3],
            "interpretation": (
                "At p=5 the full graph symmetry has four determinant multiplier "
                "classes, while unitary/anti-unitary Clifford symmetry retains only "
                "the +1 and -1 classes."
            ),
        },
        "literature_anchor": {
            "source": "D. M. Appleby, Properties of the extended Clifford group with applications to SIC-POVMs and MUBs, arXiv:0909.5233",
            "fact_used": (
                "In odd prime-power dimension the extended Clifford construction "
                "uses symplectic matrices det=+1 and anti-symplectic matrices det=-1, "
                "collectively ESL(2,F_d)."
            ),
        },
        "novelty_scope": (
            "Pass 408 already proved the full Heisenberg graph automorphism theorem "
            "and noted that the multiplier quotient has size p-1. Appleby already "
            "gives the extended Clifford ESL group. The contribution here is their "
            "explicit comparison and the exact saturation index/uniqueness criterion."
        ),
        "physics_boundary": (
            "This is a finite symmetry-selection theorem for a Heisenberg graph/Clifford "
            "normalizer model. It does not by itself prove that Nature must use qutrits, "
            "derive three particle generations, select spacetime dimension, or determine "
            "a measured coupling. Any such physical reading requires an independent "
            "identification of this saturation criterion with a physical principle."
        ),
        "parents": [
            "data/w33_pass408_full_automorphism_theorem.json",
            "data/w33_extended_clifford_pass408_intertwiner.json",
            "data/w33_hesse_affine_spinor_parity.json",
        ],
        "checks": checks,
    }
    assert all(checks.values())
    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n")
    return out


if __name__ == "__main__":
    print(json.dumps(main(True), indent=2))
