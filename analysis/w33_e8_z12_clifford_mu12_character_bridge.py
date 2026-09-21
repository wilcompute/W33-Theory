#!/usr/bin/env python3
"""Explicit cyclotomic character from the E8 Qpsi Z12 grading to Clifford mu_12.

Pass 7081-7096 left an honesty boundary: the E8 Z12 root-space grading and the
independent qutrit-Clifford scalar phase group mu_12 had the same order, but no
explicit character/intertwiner had been supplied.

The newer Qpsi theorem closes the character half exactly.  The E8 grading is
Qpsi modulo 12, so choose a primitive twelfth root zeta_12 and define

    chi([q]) = zeta_12^q.

This is a faithful isomorphism Z/12 -> mu_12.  Its phase multiplicities on the
248-dimensional E8 adjoint are exactly the frozen Z12 sector dimensions, and
every certified E6 cubic has total Qpsi zero, so the product of its three
cyclotomic characters is exactly one.

Pass 2799 independently proves that the scalar phase group of the n-qutrit
Clifford group is mu_12 for every n.  Therefore the two cyclic groups now have
an explicit generator-preserving character bridge.

Boundary: this is NOT yet a representation intertwiner between E8 root spaces
and a photonic/qutrit Hilbert space.  Clifford scalar phases act uniformly on a
given Hilbert space, while chi labels E8 charge sectors relatively.  A carrier
map that makes those actions conjugate is still required for physical
identification.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_e8_z12_clifford_mu12_character_bridge.json"

def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

def main(write=True):
    qpsi = json.loads((ROOT / "data/w33_qpsi_mod12_unification.json").read_text())
    phase = json.loads(
        (ROOT / "data/PART_W33_PASS2797_2799_MAGIC_ORBITS_AND_MONOTONE.json").read_text()
    )
    bridge = load(
        ROOT / "analysis/w33_qpsi_matter_parity_e8_d8_bridge.py",
        "w33_mu12_qpsi_source",
    )

    assert qpsi["status"] == "PASS_SINGLE_INTEGER_QPSI_UNIFIES_E8_Z2_Z3_Z4_Z6_Z12"
    assert phase["pass_2799"]["field_identities_hold"] is True
    assert phase["pass_2799"]["conclusion"].startswith("phase group = mu_12 for all n")

    # Symbolic character chi: residue r -> zeta_12^r.
    exponents = list(range(12))
    assert len(set(exponents)) == 12
    for a in exponents:
        for b in exponents:
            assert ((a + b) % 12) == ((a % 12) + (b % 12)) % 12

    # Reconstruct the Qpsi adjoint histogram directly from the source-locked
    # root channels and add the eight neutral Cartans.
    hist = Counter()
    for h in bridge.ROOT_QPSI.values():
        hist.update(h)
    hist[0] += 8
    assert sum(hist.values()) == 248

    phase_mult = [0] * 12
    for q, n in hist.items():
        phase_mult[q % 12] += n
    expected = qpsi["residue_dimensions"]["mod12_common_refinement"]
    assert phase_mult == expected
    assert phase_mult == [54,48,30,16,3,0,0,0,3,16,30,48]

    # Exact E6 cubic selection: all 45 certified cubic charge triples sum to 0,
    # hence chi(q1) chi(q2) chi(q3) = zeta_12^(q1+q2+q3) = 1.
    cubic_counts = Counter()
    total_cubics = 0
    for pat, meta in bridge.CUBIC_PATTERNS.items():
        assert sum(pat) == 0
        exponent = sum(pat) % 12
        assert exponent == 0
        cubic_counts[tuple(pat)] = meta["count"]
        total_cubics += meta["count"]
    assert total_cubics == 45
    assert cubic_counts == Counter({(-2,1,1):40, (-2,-2,4):5})

    # Subgroup reductions commute with the character.
    subgroup = {}
    for n in (2,3,4,6,12):
        subgroup[str(n)] = {
            "charge_reduction": f"Qpsi mod {n}",
            "phase_power": 12 // n,
            "generator_exponent_in_mu12": 12 // n,
            "generator_order": n,
        }
        # zeta_12^(12/n) has exact order n.
        e = 12 // n
        assert min(k for k in range(1, 13) if (e * k) % 12 == 0) == n

    out = {
        "schema": "w33.e8_z12_clifford_mu12_character_bridge.v1",
        "status": "PASS_EXPLICIT_FAITHFUL_Z12_TO_MU12_CHARACTER_BRIDGE",
        "character": {
            "domain": "E8 Qpsi grading group Z/12Z",
            "codomain": "qutrit-Clifford scalar phase group mu_12",
            "definition": "chi([q]) = zeta_12^q",
            "chosen_generator": "chi([1]) = zeta_12",
            "faithful": True,
            "surjective": True,
            "isomorphism": True,
        },
        "E8_phase_multiplicities_exponents_0_to_11": phase_mult,
        "Qpsi_histogram": {str(q): n for q, n in sorted(hist.items())},
        "cubic_phase_selection": {
            "patterns": [
                {"Qpsi": list(pat), "count": count, "character_product": "1"}
                for pat, count in sorted(cubic_counts.items())
            ],
            "total_cubics": total_cubics,
            "all_character_products_trivial": True,
        },
        "subgroup_character_ladder": subgroup,
        "clifford_phase_owner": {
            "source": "data/PART_W33_PASS2797_2799_MAGIC_ORBITS_AND_MONOTONE.json",
            "theorem": phase["pass_2799"]["conclusion"],
            "zeta12_field_identities_hold": phase["pass_2799"]["field_identities_hold"],
        },
        "what_is_closed": (
            "The order-12 equality is no longer only cardinality: a concrete faithful "
            "generator-preserving cyclotomic character identifies the E8 discrete grading "
            "group with the exact Clifford scalar phase group, and E6 cubic charge "
            "conservation becomes scalar-phase conservation under that character."
        ),
        "remaining_intertwiner_boundary": (
            "No Hilbert-space/root-space carrier intertwiner is claimed. Clifford mu_12 "
            "is a global scalar center on each qutrit Hilbert space, whereas the E8 action "
            "has different eigenphases on different charge sectors. A physical identification "
            "still needs an explicit carrier map U with matching relative action, not merely "
            "the cyclic-group character proved here."
        ),
        "checks": {
            "twelve_distinct_character_values_symbolically": True,
            "adjoint_phase_multiplicities_match_Z12": True,
            "all_45_E6_cubics_have_trivial_character_product": True,
            "Z2_Z3_Z4_Z6_subgroups_embed_in_mu12": True,
            "clifford_scalar_phase_group_is_mu12_all_n": True,
            "representation_intertwiner_not_claimed": True,
        },
    }
    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    return out

if __name__ == "__main__":
    main(True)
