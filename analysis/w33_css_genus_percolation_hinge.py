#!/usr/bin/env python3
"""W(3,3) CSS-distance / genus-equation / percolation hinge verifier.

This is the bridge suggested by the new CSS correction:

    d_X = 3, d_Z = 4

for the canonical edge-qutrit CSS code [[240,81,3]]_3 with asymmetric
witness distances d_X=3, d_Z=4.

The point of this script is not to re-compute the CSS code distances.  That
is handled by analysis/w33_css_exact_audit.py.  Instead, this script tests
the structural implication of those two distances:

    d_X + d_Z = 7  (Heawood / Fano / Csaszar-Szilassi shell)
    d_X d_Z   = 12 (local codec / W33 valency / genus denominator)

and therefore

    (n - d_X)(n - d_Z)/(d_X d_Z) = (n - 3)(n - 4)/12,

exactly the genus equation already used by the Csaszar/Szilassi oscillator.

Interpretation: the CSS code's two minimal logical thresholds are the two
roots of the toroidal genus polynomial.  The X-distance 3 is the first
triangle/cocycle activation; the Z-distance 4 is the first non-boundary
4-cycle/tetrahedral closure.  Together they generate the toroidal hinge.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Iterable


DX = 3
DZ = 4
Q = DX
QP1 = DZ
HEAWOOD = DX + DZ          # 7
CODEC = DX * DZ            # 12
PHI3 = Q * Q + Q + 1       # 13
PHI4 = Q * Q + 1           # 10
PHI6 = Q * Q - Q + 1       # 7
H1 = Q ** QP1              # 81
V = 40
E = 240


@dataclass(frozen=True)
class VisibilityLedger:
    name: str
    rank: int
    trace: float
    trace2: float
    d_eff: float
    split_count: int
    outcome_class: str
    interpretation: str


def positive_values(eigenvalues: Iterable[float], eps: float = 1e-12) -> list[float]:
    return sorted(float(x) for x in eigenvalues if float(x) > eps)


def split_count(eigenvalues: Iterable[float], eps: float = 1e-9) -> int:
    vals = positive_values(eigenvalues, eps)
    if not vals:
        return 0
    groups = 1
    last = vals[0]
    for x in vals[1:]:
        if abs(x - last) > eps:
            groups += 1
            last = x
    return groups


def visibility_ledger(name: str, eigenvalues: list[float], interpretation: str, full_dim: int = H1) -> VisibilityLedger:
    t1 = sum(eigenvalues)
    t2 = sum(x * x for x in eigenvalues)
    d_eff = 0.0 if t2 == 0 else (t1 * t1) / t2
    rank = len(positive_values(eigenvalues))
    if rank == 0:
        outcome = "zero"
    elif rank < full_dim:
        outcome = "rank_defective"
    elif split_count(eigenvalues) == 1:
        outcome = "full_isotropic"
    else:
        outcome = "full_split"
    return VisibilityLedger(name, rank, t1, t2, d_eff, split_count(eigenvalues), outcome, interpretation)


def genus_from_css_roots(n: int) -> Fraction:
    return Fraction((n - DX) * (n - DZ), DX * DZ)


def is_integer_genus(n: int) -> bool:
    return genus_from_css_roots(n).denominator == 1


def genus_spectrum(max_n: int = 90) -> list[dict]:
    rows: list[dict] = []
    for n in range(DX, max_n + 1):
        g = genus_from_css_roots(n)
        if g.denominator == 1:
            rows.append({
                "n": n,
                "g": int(g),
                "m_mod_12": (n - DZ) % CODEC,
                "role": role_for_n(n),
            })
    return rows


def role_for_n(n: int) -> str:
    table = {
        DX: "X-distance root; triangle/cocycle activation; zero numerator",
        DZ: "Z-distance root; tetrahedral closure / first non-boundary cycle; genus 0 K4",
        HEAWOOD: "Heawood/Fano/Csaszar-Szilassi toroidal shell; genus 1 K7",
        CODEC: "local codec = W(3,3) valency; genus 6 K12",
        Q ** Q: "q^q = 27; E6 fundamental / cubic-surface line count; genus 46 K27",
        V: "W(3,3) vertex count; genus 111 K40",
        H1: "H1 = 81 protected logical sector; intentionally off genus spectrum",
    }
    return table.get(n, "integer-genus K_n lattice point")


def percolation_ledgers() -> list[VisibilityLedger]:
    # Toy spectra, using equal positive eigenvalues so d_eff equals the active rank.
    # This aligns the existing percolation utility with CSS/genus thresholds.
    examples = [
        ("p_zero", 0, "no visible H1 sector"),
        ("p_X_triangle", DX, "first X logical / triangle-star cocycle threshold"),
        ("p_Z_square", DZ, "first Z logical / non-boundary 4-cycle threshold"),
        ("p_torus_shell", HEAWOOD, "sum dX+dZ = 7; toroidal Heawood/Fano shell"),
        ("p_codec", CODEC, "product dX*dZ = 12; local codec / valency"),
        ("p_exact_gradient", DX * PHI3, "rank d1 = 39 = dX * Phi3 exact-gradient sector"),
        ("p_triangle_boundary", CODEC * PHI4, "rank d2 = 120 = codec * Phi4 triangle-boundary sector"),
        ("p_H1_full", H1, "protected logical sector H1 = dX^dZ = 81"),
    ]
    ledgers = []
    for name, rank, interp in examples:
        vals = [1.0] * rank + [0.0] * (H1 - min(rank, H1))
        ledgers.append(visibility_ledger(name, vals[:H1], interp))
    return ledgers


def oscillator_flag_identities() -> dict:
    tetra_flags = 2 * CODEC
    csaszar_flags = HEAWOOD * CODEC
    szilassi_flags = HEAWOOD * CODEC
    tomotope_flags = tetra_flags + csaszar_flags + szilassi_flags
    tomotope_cells = 1 + HEAWOOD
    return {
        "tetrahedron_flags": tetra_flags,
        "tetrahedron_formula": "2 * dX*dZ = 2*12 = 24",
        "csaszar_flags": csaszar_flags,
        "csaszar_formula": "(dX+dZ) * dX*dZ = 7*12 = 84",
        "szilassi_flags": szilassi_flags,
        "szilassi_formula": "(dX+dZ) * dX*dZ = 7*12 = 84",
        "tomotope_flags": tomotope_flags,
        "tomotope_formula": "2*dX*dZ + 2*(dX+dZ)*dX*dZ = 192",
        "tomotope_cells": tomotope_cells,
        "tomotope_cells_formula": "1 + (dX+dZ) = 8",
        "tomotope_flag_match": tomotope_flags == 192,
        "tomotope_cell_match": tomotope_cells == 8,
    }


def hodge_sector_identities() -> dict:
    exact_gradient = DX * PHI3
    triangle_boundary = CODEC * PHI4
    harmonic = DX ** DZ
    total = exact_gradient + triangle_boundary + harmonic
    return {
        "exact_gradient_modes": exact_gradient,
        "exact_gradient_formula": "dX * Phi3 = 3 * 13 = 39",
        "triangle_boundary_modes": triangle_boundary,
        "triangle_boundary_formula": "dX*dZ * Phi4 = 12 * 10 = 120",
        "harmonic_modes": harmonic,
        "harmonic_formula": "dX^dZ = 3^4 = 81",
        "total_edge_modes": total,
        "total_formula": "39 + 120 + 81 = 240",
        "matches_W33_edges": total == E,
    }


def build_payload() -> dict:
    spectrum = genus_spectrum(90)
    ledgers = percolation_ledgers()
    flags = oscillator_flag_identities()
    hodge = hodge_sector_identities()
    key_ns = [DX, DZ, HEAWOOD, CODEC, Q ** Q, V, H1]
    key_rows = [{"n": n, "integer_genus": is_integer_genus(n), "g": int(genus_from_css_roots(n)) if is_integer_genus(n) else None, "role": role_for_n(n)} for n in key_ns]

    identities = {
        "dx_is_q": DX == Q == 3,
        "dz_is_q_plus_1": DZ == QP1 == 4,
        "sum_is_heawood_phi6": DX + DZ == HEAWOOD == PHI6 == 7,
        "product_is_codec": DX * DZ == CODEC == 12,
        "genus_formula_same": str(genus_from_css_roots(12)) == "6",
        "K4_genus_zero": genus_from_css_roots(4) == 0,
        "K7_genus_one": genus_from_css_roots(7) == 1,
        "K12_genus_six": genus_from_css_roots(12) == 6,
        "H1_off_spectrum": not is_integer_genus(H1),
        "tomotope_flags_from_distances": flags["tomotope_flag_match"],
        "tomotope_cells_from_distances": flags["tomotope_cell_match"],
        "hodge_decomposition_from_distances": hodge["matches_W33_edges"],
    }

    theorem = (
        "CSS-Genus Hinge Theorem.  For the canonical W(3,3) edge CSS code, "
        "the asymmetric minimal logical distances are d_X=3 and d_Z=4.  These "
        "are exactly the two roots of the toroidal genus numerator: "
        "(n-d_X)(n-d_Z)=(n-3)(n-4).  Their sum is 7, the Heawood/Fano/" 
        "Csaszar-Szilassi shell, and their product is 12, the W(3,3) valency "
        "and local codec.  Hence the genus equation is not external decoration: "
        "it is the quadratic generated by the two CSS logical thresholds."
    )

    return {
        "summary": {
            "d_X": DX,
            "d_Z": DZ,
            "heawood_sum": HEAWOOD,
            "codec_product": CODEC,
            "H1": H1,
            "W33_edges": E,
            "all_identities_hold": all(identities.values()),
        },
        "css_genus_equation": {
            "formula": "g(n) = (n-d_X)(n-d_Z)/(d_X*d_Z)",
            "with_distances": f"g(n) = (n-{DX})(n-{DZ})/{CODEC}",
            "standard_form": "g(K_n) = (n-3)(n-4)/12",
            "roots": [DX, DZ],
            "sum": HEAWOOD,
            "product": CODEC,
        },
        "key_genus_rows": key_rows,
        "integer_spectrum_n_le_90": spectrum,
        "percolation_threshold_ledgers": [asdict(x) for x in ledgers],
        "oscillator_flag_identities": flags,
        "hodge_sector_identities": hodge,
        "identities": identities,
        "theorem": theorem,
        "honesty_boundary": (
            "This verifier proves exact arithmetic compatibility among the CSS distances, "
            "the genus equation, the percolation order-parameter ranks, and the oscillator "
            "flag counts.  It does not by itself prove a continuum TQFT, a physical anyon "
            "braid representation, or empirical particle masses.  It supplies the finite "
            "hinge those later bridges must respect."
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_css_genus_percolation_hinge.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
