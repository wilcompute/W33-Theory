"""W(3,3) SU(d) DIMENSION THEOREM at substrate-meaningful d.

The dimension of the unitary group SU(d), namely d^2 - 1, evaluated at
the SUBSTRATE-MEANINGFUL d values {q, q^2, q^q, v, q^{q+1}} produces
clean substrate-primitive factorisations.  All five identifications
verify.

CENTRAL TABLE.
==============

  d     d-meaning                       dim SU(d) = d^2 - 1   substrate form
  ---   ------------------------------- -------------------   -----------------------------
  3     single qutrit                    8                    2^q
  9     past x future = self-entangled  80                    2 v
        qutrit  (= 9 history cells)
  27    q^q = cubic surface lines /    728                    2^q * Phi_6 * Phi_3
        E_6 fundamental rep
  40    v = W(3,3) vertices            1599                   q * Phi_3 * 41
        (Ogg prime!)
  81    q^{q+1} = H_1 = matter sector  6560                   2^{q+2} * Csaszar_count * 41
        (Ogg prime again!)

CONNECTION TO REGULAR 4-POLYTOPES.
==================================

By the regular 4-polytope substrate package (commit 4065af41):

  8-cell + 16-cell f-vector sum  = 2 * 80 = 160 = mu * v
  8-cell f-vector sum            = 80 = 2 v = dim SU(9)
                                = dim SU(self-entangled qutrit unitary)

The 8-cell / 16-cell dual pair has f-vector sums EACH equal to
2v = dim SU(9), which is the unitary group of the 9-dimensional past x
future qutrit space.  And |W(D_4)| = 192 = f * 2^q acts on this dual
pair.

PHOTONIC UNIVERSAL COMPUTATION READING.
=======================================

In photonic universal QC the parameter count for arbitrary SU(d)
control is d^2 - 1.  Reading our table:

  Single qutrit (3 modes):
      parameter count = 8 = 2^q = tomotope cells
  Self-entangled qutrit (9 modes = past x future):
      parameter count = 80 = 2 v
      = number of independent beam-splitter angles + phase shifts
        needed for universal SU(9) control on the time-bin self-
        entangled qutrit (Part MCCIII single-photon implementation).
  E_6 fundamental (27 modes = q^q cubic surface lines):
      parameter count = 728 = 2^q * Phi_6 * Phi_3
  Full W(3,3) carrier (40 modes = v):
      parameter count = 1599 = q * Phi_3 * 41 (Ogg prime)
  Matter sector (81 modes = H_1):
      parameter count = 6560 = 2^{q+2} * Csaszar_count * 41 (Ogg prime)

So at every substrate-meaningful Hilbert-space dimension the
universal-control parameter count is in substrate-primitive form, and
the Monster/Ogg prime 41 appears at d in {v, H_1}.

OGG PRIME 41 = f + (q^2 + 2^q).

The Ogg prime 41 = q^2 + 2^q + f = 17 + 24 = Twin Pell sum #2 + f
(commit edd05c2f).  It appears as a factor in BOTH dim SU(v) AND
dim SU(H_1), tying the Monster supersingular prime structure to the
photonic-control parameter count of full and matter-sector substrate
computation.

CHAIN OF BLOCH DIMENSIONS.

  d=3  -> d=9:   ratio 80/8  = 10 = Phi_4
  d=9  -> d=27:  ratio 728/80 = 9.1 = 91/10 = Phi_3*Phi_6/Phi_4
  d=27 -> d=40:  ratio 1599/728 not clean
  d=40 -> d=81:  ratio 6560/1599 not clean
  d=81 / d=9:    ratio 82 = 2 * 41 (Ogg prime)
  d=81 / d=3:    ratio 820 = 20*41 = m_4 * 41

The cleanest ratios:
  dim SU(self-entangled) / dim SU(single) = Phi_4
  dim SU(matter sector) / dim SU(self-entangled) = 82 = 2 * 41 (Ogg)

NEW SUBSTRATE FORM:
  dim SU(self-entangled qutrit on photon) = 2 v
  dim SU(matter sector) = 2 v * 82 = 2v * 2 * 41 = 4v * Ogg_41.
"""
from __future__ import annotations

import json
from pathlib import Path


# Substrate constants
Q = 3
QP1 = 4
MU = QP1
K_CODEC = Q * QP1
P_IH = K_CODEC - 1
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
F = 24
G_NEG = 15
V = 40
EDGES = 240
H1 = Q ** QP1
CSASZAR_COUNT = Q + 2
OGG_41 = 41


def su_dim_rows() -> list[dict]:
    return [
        {
            "d": Q,
            "d_substrate": "q (single qutrit)",
            "dim_su": Q * Q - 1,
            "expected_substrate": 2 ** Q,
            "substrate_form": "2^q (tomotope cells)",
            "match": (Q * Q - 1) == 2 ** Q,
        },
        {
            "d": Q * Q,
            "d_substrate": "q^2 (self-entangled qutrit = 9 history cells)",
            "dim_su": Q * Q * Q * Q - 1,
            "expected_substrate": 2 * V,
            "substrate_form": "2 v",
            "match": (Q ** 4 - 1) == 2 * V,
        },
        {
            "d": Q ** Q,
            "d_substrate": "q^q (cubic-surface lines / E_6 fund rep)",
            "dim_su": (Q ** Q) ** 2 - 1,
            "expected_substrate": (2 ** Q) * PHI6 * PHI3,
            "substrate_form": "2^q * Phi_6 * Phi_3",
            "match": ((Q ** Q) ** 2 - 1) == (2 ** Q) * PHI6 * PHI3,
        },
        {
            "d": V,
            "d_substrate": "v (W(3,3) vertex count)",
            "dim_su": V * V - 1,
            "expected_substrate": Q * PHI3 * OGG_41,
            "substrate_form": "q * Phi_3 * 41  (41 = Ogg prime)",
            "match": (V * V - 1) == Q * PHI3 * OGG_41,
        },
        {
            "d": H1,
            "d_substrate": "q^{q+1} = H_1 (matter sector)",
            "dim_su": H1 * H1 - 1,
            "expected_substrate": (2 ** (Q + 2)) * CSASZAR_COUNT * OGG_41,
            "substrate_form": "2^{q+2} * Csaszar_count * 41 (Ogg prime)",
            "match": (H1 * H1 - 1) == (2 ** (Q + 2)) * CSASZAR_COUNT * OGG_41,
        },
    ]


def ogg_41_identification() -> dict:
    """41 = q^2 + 2^q + f (Twin Pell sum #2 + f)."""
    return {
        "value": OGG_41,
        "substrate_form": "q^2 + 2^q + f = 17 + 24",
        "alternative": "Twin Pell sum #2 + f",
        "is_ogg_prime": True,
        "monster_factor": "41 in {2,3,5,7,11,13,17,19,23,29,31,41,47,59,71}",
        "appearances": ["dim SU(v) = 1599 = q*Phi_3*41",
                        "dim SU(H_1) = 6560 = 2^{q+2}*Csaszar*41"],
        "verify": OGG_41 == Q * Q + 2 ** Q + F,
    }


def photonic_universal_control_table() -> list[dict]:
    rows = []
    for r in su_dim_rows():
        rows.append({
            "Hilbert_dim_d": r["d"],
            "physical_realisation_modes": r["d_substrate"],
            "universal_control_parameters": r["dim_su"],
            "parameter_substrate_form": r["substrate_form"],
        })
    return rows


def polytope_link() -> dict:
    return {
        "8_cell_or_16_cell_fvec_sum": 80,
        "self_entangled_SU_dim": 80,
        "match": True,
        "interpretation": (
            "The 8-cell {4,3,3} and 16-cell {3,3,4} dual pair (commit "
            "4065af41) each have f-vector sum 80, exactly equal to "
            "dim SU(9) -- the unitary group of the self-entangled qutrit "
            "Hilbert space.  And |W(D_4)| = 192 = f * 2^q acts on this "
            "dual pair (Klein closure, commit 2a533251).  So the 8/16-cell "
            "dual pair carries the substrate's self-entangled-qutrit "
            "control structure simultaneously at the polytope level and "
            "the photonic-computation level."
        ),
    }


def build_payload() -> dict:
    rows = su_dim_rows()
    return {
        "header": {
            "substrate_constants": {
                "q": Q, "v": V, "k": K_CODEC, "f": F, "H_1": H1,
                "Phi_3": PHI3, "Phi_4": PHI4, "Phi_6": PHI6,
                "Csaszar_count": CSASZAR_COUNT, "Ogg_41": OGG_41,
            },
        },
        "SU_d_substrate_rows": rows,
        "all_match": all(r["match"] for r in rows),
        "ogg_41": ogg_41_identification(),
        "photonic_universal_control": photonic_universal_control_table(),
        "polytope_link": polytope_link(),
        "theorem": (
            "W(3,3) SU(d) Substrate Theorem.  For each substrate-meaningful "
            "Hilbert-space dimension d in {q, q^2, q^q, v, q^{q+1}}, the "
            "unitary group dimension dim SU(d) = d^2 - 1 has a clean "
            "substrate-primitive factorisation.  In photonic universal "
            "computation language: the number of beam-splitter + phase-"
            "shifter parameters needed for universal SU(d) control is "
            "(in order) 2^q, 2v, 2^q*Phi_6*Phi_3, q*Phi_3*41, "
            "2^{q+2}*Csaszar*41 -- with the Monster/Ogg supersingular "
            "prime 41 = q^2 + 2^q + f appearing in BOTH dim SU(v) and "
            "dim SU(H_1).  The self-entangled qutrit (past x future = 9 "
            "modes) has SU dimension 80 = 2v exactly matching the 8-cell "
            "/ 16-cell f-vector sum (commit 4065af41).  This realises the "
            "user's single-photon temporal-triangle picture (Part MCCIII) "
            "at the universal-control-parameter level."
        ),
        "honesty_boundary": (
            "dim SU(d) = d^2 - 1 is standard.  The substrate-primitive "
            "factorisations are exact arithmetic.  The 'photonic control "
            "parameter count' interpretation is the standard "
            "Reck/Clements decomposition language for linear-optics "
            "unitaries.  No new physical observable is derived; the new "
            "content is the unified substrate-primitive reading of the "
            "control parameter counts at the substrate's distinguished "
            "Hilbert-space dimensions."
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_SU_d_dimensions_substrate.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    print("=" * 80)
    print("W(3,3) SU(d) DIMENSIONS AT SUBSTRATE-MEANINGFUL d")
    print("=" * 80)
    print(f"\n{'d':>4s}  {'meaning':<46s}  {'dim SU(d)':>10s}  substrate form")
    print('  ' + '-' * 76)
    for r in payload["SU_d_substrate_rows"]:
        ok = "OK" if r["match"] else "FAIL"
        print(f"  {r['d']:>3d}  {r['d_substrate']:<45s}  {r['dim_su']:>9d}  [{ok}]  {r['substrate_form']}")

    o = payload["ogg_41"]
    print(f"\nOgg prime 41 = {o['substrate_form']}: verified {o['verify']}")
    print(f"  Appears in dim SU(v) and dim SU(H_1)")

    p = payload["polytope_link"]
    print(f"\nPolytope link:")
    print(f"  8-cell / 16-cell f-vector sum = 80 = 2v = dim SU(9) = self-entangled qutrit unitary dim")

    print(f"\nAll five SU(d) substrate forms verify: {payload['all_match']}")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
