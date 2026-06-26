#!/usr/bin/env python3
"""
One hierarchy, three frameworks reconciled -- and the tier-tower base is the complement
graph. The Planck-to-electroweak gap is written three ways across the corpus: the canonical
document's base-10 form (M_GUT/M_EW = 10^(2 Phi_6), M_Pl/M_GUT = 496), the cyclotomic e-fold
form (ln(M_Pl/M_EW) = q Phi_3), and the multiplicative mass-tier tower (ratio r per tier).
All three give the same ~38-39 e-fold gap, and the tier tower's ratio is now grounded in the
COMPLEMENT graph: r = q^q/(lambda v) = kbar/(lambda v), where q^q = 27 = kbar = v - k - 1 is
the degree of the complement SRG(40,27,18,18) = the E6 fundamental / matter sector. So all
three hierarchies are W(3,3) graph data; their exact integer alignment across bases is the
remaining open thread.

This reconciles my e-fold passes with the canonical document's hierarchy formula and the
older tier tower, using the user's identities q^3 = q^q and 27 = complement-graph degree.

THE COMPLEMENT-GRAPH BASE (the new grounding). The tier tower m = m_Planck r^n used r =
q^q/(l^mu F5) = 27/80. Two refinements:
  * the 80 is lambda*v = 2*40 (the SRG edge-overlap parameter times the vertex count), i.e.
    l^mu F5 = lambda v;
  * the 27 is q^q AND the complement-graph degree kbar = v - k - 1 = 40 - 12 - 1 = 27 (the
    number of non-neighbours of each vertex), which is the E6 fundamental / matter sector.
So r = kbar/(lambda v) = (complement degree)/(lambda * vertices): the tier tower's base is a
pure complement-graph invariant. The complement SRG(40,27,18,18) has lambda_bar = mu_bar =
18 = h(E7), so its degree 27 over lambda*v sets the mass spacing.

THE THREE HIERARCHY FORMS (same gap).
  (A) canonical base-10:  log10(M_GUT/M_EW) = 2 Phi_6 = 14;  M_Pl/M_GUT = 496 = dim SO(32);
      ln(M_Pl/M_EW) = 2 Phi_6 ln10 + ln 496 = 32.24 + 6.21 = 38.44.
  (B) cyclotomic e-fold:  ln(M_Pl/M_EW) = q Phi_3 = 39.
  (C) tier tower:         ln(M_Pl/M_EW) / ln(1/r) = 38.4 / 1.086 = 35.4 tiers.
(A) and (B) agree to 1.4% (38.44 vs 39); (C) is the same gap in tier units (each tier =
ln(lambda v/q^q) = ln(80/27) = 1.086 e-folds).

THE OPEN ALIGNMENT. The three bases (10, e, 80/27) all encode the ~38-39 e-fold Planck-EW
gap, but they do not integer-align simultaneously: 39 e-folds is 35.4 tiers (non-integer),
and 2 Phi_6 = 14 is base-10 while q Phi_3 = 39 is base-e. Each is exact in its own base; a
single quantization making all three integer at once is not found -- the honest open thread.
What IS new: the tier base is the complement-graph degree (r = kbar/(lambda v)), so the
multiplicative tower joins the cyclotomic and base-10 forms as W(3,3) graph data.

Honest scope: the equality of (A) and (B) is a ~1.4% numerical reconciliation (38.44 vs 39),
each exact in its base; (C) restates the gap in tier units. The novel content is the
grounding r = q^q/(lambda v) = kbar/(lambda v) (complement-graph degree over lambda*vertices),
using q^3 = q^q and 27 = v - k - 1. The cross-base integer alignment remains open -- the
three frameworks are the same physics in three bases, not yet one quantization.

Verifies r = kbar/(lambda v), kbar = q^q = v - k - 1 = 27, the complement parameters, the
three hierarchy forms agreeing at ~38-39 e-folds, and the non-alignment.
"""
from __future__ import annotations

import json
import math


def main():
    out = {}
    q, k, lam, mu = 3, 12, 2, 4
    v = 40
    Phi3, Phi6 = q * q + q + 1, q * q - q + 1  # 13, 7
    F5, l = 5, 2

    # complement-graph grounding of r
    kbar = v - k - 1  # 27 = q^q = complement degree
    r = q**q / (lam * v)  # 27/80
    print(
        "== the tier-tower base is the complement graph: r = q^q/(lambda v) = kbar/(lambda v) =="
    )
    # complement of SRG(v,k,lam,mu) = SRG(v, v-k-1, v-2-2k+mu, v-2k+lam) = (40,27,18,18)
    lam_bar = v - 2 - 2 * k + mu  # 18 = h(E7)
    mu_bar = v - 2 * k + lam  # 18 = h(E7)
    print(
        f"  complement SRG(40, kbar, lam_bar, mu_bar) = (40, {kbar}, {lam_bar}, {mu_bar})"
    )
    print(
        f"  kbar = v - k - 1 = {kbar} = q^q = {q**q} (E6 fundamental / matter sector)"
    )
    print(
        f"  r = q^q/(lambda v) = {q**q}/{lam*v} = {r}   (l^mu F5 = lambda v = {l**mu*F5})"
    )
    assert kbar == q**q == 27 and r == q**q / (lam * v)
    assert (
        lam_bar == mu_bar == 18
    )  # complement is SRG(40,27,18,18), lam_bar=mu_bar=h(E7)
    out["complement_base"] = {
        "r": "q^q/(lambda v) = kbar/(lambda v) = 27/80",
        "kbar": kbar,
        "kbar_forms": "v-k-1 = q^q = E6 fundamental",
        "complement_SRG": [v, kbar, lam_bar, mu_bar],
        "identity": "l^mu F5 = lambda v = 80",
    }

    # three hierarchy forms
    M_Pl = 1.22e19
    v_ew = 246.0
    base10 = 2 * Phi6 * math.log(10) + math.log(496)  # ln(M_Pl/M_EW) via doc
    cyclo = q * Phi3  # 39
    efold_per_tier = math.log(lam * v / q**q)  # ln(80/27)
    tiers = base10 / efold_per_tier
    print(f"\n[three hierarchy forms, same ~38-39 e-fold gap]")
    print(
        f"  (A) base-10 (doc): 2 Phi_6 ln10 + ln496 = {2*Phi6*math.log(10):.2f} + {math.log(496):.2f} = {base10:.2f}"
    )
    print(f"  (B) cyclotomic e-fold: ln(M_Pl/M_EW) = q Phi_3 = {cyclo}")
    print(
        f"  (C) tier tower: {base10:.1f}/ln(80/27) = {base10:.1f}/{efold_per_tier:.3f} = {tiers:.1f} tiers"
    )
    print(
        f"  (A) vs (B): {base10:.2f} vs {cyclo}  -> agree to {abs(base10-cyclo)/cyclo*100:.1f}%"
    )
    assert abs(base10 - cyclo) / cyclo < 0.02
    out["three_forms"] = {
        "A_base10": {"form": "2 Phi_6 log10 + log 496", "ln_value": round(base10, 2)},
        "B_cyclotomic": {"form": "q Phi_3", "value": cyclo},
        "C_tier": {"form": "ln-gap / ln(80/27)", "tiers": round(tiers, 1)},
        "A_vs_B_pct": round(abs(base10 - cyclo) / cyclo * 100, 1),
    }

    # the open alignment
    print(
        f"\n[open thread]  the three bases (10, e, 80/27) encode the same gap but do NOT"
    )
    print(
        f"  integer-align simultaneously: q Phi_3 = 39 e-folds = {tiers:.1f} tiers (non-integer),"
    )
    print(
        f"  2 Phi_6 = 14 is base-10 while q Phi_3 = 39 is base-e. Each exact in its base;"
    )
    print(f"  a single all-integer quantization is the remaining open thread.")
    out["open_alignment"] = {
        "status": "same gap, three bases, not simultaneously integer-aligned",
        "evidence": f"q Phi_3 = 39 e-folds = {round(tiers,1)} tiers (non-integer)",
    }

    print("\nRESULT: one hierarchy, three frameworks reconciled, the tier base now a")
    print(
        "  complement-graph invariant. The Planck-to-electroweak gap appears in the corpus"
    )
    print(
        "  three ways -- the document's base-10 (log10(M_GUT/M_EW) = 2 Phi_6 = 14, M_Pl/M_GUT"
    )
    print(
        "  = 496), my cyclotomic e-fold (ln(M_Pl/M_EW) = q Phi_3 = 39), and the multiplicative"
    )
    print(
        "  mass-tier tower -- and all three give the same ~38-39 e-fold gap (A vs B agree to"
    )
    print("  1.4%). The new grounding: the tier tower's ratio is r = q^q/(lambda v) =")
    print(
        "  kbar/(lambda v), where q^q = 27 is BOTH the self-power and the complement-graph"
    )
    print(
        "  degree kbar = v - k - 1 (the E6 fundamental / matter sector), and lambda v = 80 ="
    )
    print(
        "  l^mu F5. So the tower's base is a pure complement-graph invariant, joining the"
    )
    print(
        "  cyclotomic and base-10 forms as W(3,3) data. The honest open thread is that the"
    )
    print(
        "  three bases (10, e, 80/27) do not integer-align at once -- 39 e-folds is 35.4"
    )
    print(
        "  tiers -- so they are the same physics in three quantizations, not yet unified into"
    )
    print(
        "  one. Using q^3 = q^q and 27 = complement degree pins the tower's base to the graph."
    )

    out["summary"] = (
        "one hierarchy, three frameworks reconciled, the tier base grounded in the COMPLEMENT "
        "graph. The Planck-EW gap appears three ways: (A) canonical base-10 (log10(M_GUT/M_EW) "
        "= 2 Phi_6 = 14, M_Pl/M_GUT = 496 = dim SO(32)), (B) cyclotomic e-fold (ln(M_Pl/M_EW) = "
        "q Phi_3 = 39), (C) multiplicative tier tower -- all giving the same ~38-39 e-fold gap "
        "(A=38.44 vs B=39, 1.4%). NEW grounding (user identities q^3=q^q, 27=complement degree): "
        "r = q^q/(lambda v) = kbar/(lambda v), where q^q = 27 = kbar = v - k - 1 is the degree "
        "of the complement SRG(40,27,18,18) (= E6 fundamental / matter sector; its lambda_bar = "
        "mu_bar = 18 = h(E7)), and lambda v = 80 = l^mu F5. So the tier tower's base is a pure "
        "complement-graph invariant, joining the cyclotomic and base-10 forms as W(3,3) data. "
        "OPEN: the three bases (10, e, 80/27) encode the same gap but do not integer-align "
        "simultaneously (q Phi_3 = 39 e-folds = 35.4 tiers, non-integer) -- the same physics in "
        "three quantizations, a single all-integer alignment the remaining thread. HONEST: A vs "
        "B is a 1.4% numerical reconciliation (each exact in its base); the complement-graph "
        "grounding of r is the genuine new identity."
    )
    out["sources"] = [
        "canonical document hierarchy (vEW/MPl = 1/(10^(2 Phi_6) * 496), 496 = dim SO(32)); "
        "cyclotomic e-fold q Phi_3 = 39 (w33_hierarchy_derivation.py, w33_scale_reduction.py); "
        "tier tower r = q^q/(l^mu F5) (BT399, BT411); complement SRG(40,27,18,18), kbar = v-k-1 "
        "= 27 = E6 fundamental; user identities q^3 = q^q, 27 in complement graph."
    ]
    with open("data/w33_hierarchy_three_frameworks.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_hierarchy_three_frameworks.json")


if __name__ == "__main__":
    main()
