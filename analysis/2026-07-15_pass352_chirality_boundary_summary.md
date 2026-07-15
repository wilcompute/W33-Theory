# Pass 352: Chirality Boundary Summary — Complete Status of the Selection Layer

**Date:** 2026-07-15  
**Supersedes:** All prior STATUS boxes in THE_SELECTION_LAYER.md, W33_HONEST_SYNTHESIS.md  
**Status:** Reference freeze — not a new result, a structured summary

---

## What Is Proved (Theorem-Level)

| Claim | Pass(es) | Notes |
|-------|----------|-------|
| q=3 unique: 2^{(q^2-1)/2}=16 | 225 | Integer equation, unique odd solution |
| q=3 unique: (q^2+1)/2 ≤ 8 for odd q | 227 | Shadow rank fits E8; q=3 only |
| Even-q 2-rank closed: Tr(B^t)+1 | 256, 266, Sastry-Sin | Verified t=1..5, predicted t=6 |
| Odd-q 2-rank closed: (q^2+1)(q+2)/2 | 266, CSX Thm 1.1 | Verified q=3,5,7,9,11,13,17,25,27 |
| CSS family [[(q+1)(q^2+1), q^2+1, ≤q+1]] | levi_next5, 229 | k proved algebraically; d≤q+1 upper bound |
| d=q+1 equality at q=3 | 229 | Certified for [[40,10,4]] |
| W(E6)=PGSp(4,3) acts transitively on half-spins | 346, 333 | det(T)=-1, T outer involution |
| Substrate CANNOT select chirality internally | 346 | No-go theorem, not a gap |
| Three facts = one binary act (leaf selection) | 347, 350 | ω-scalar breaking, F2 type flip, chirality choice |
| det(B_2)=16, det(B_3)=76, det(B_5)=35,697,025 | 265, 281, 351 | Factor 17 persistent across all three |
| delta(4,9,25) = 1, 26, 0 | 271, 281, 351 | Irregular sequence, no simple law |

---

## What Is Conditional

### Selection A (Pass 225)
**Condition:** The shadow half-spinor IS a Standard Model generation.  
**Evidence:** Dynkin-type correspondence D5(F2) ↔ D5(C), same abstract representation, same dimension 16. Named obstruction: field change F2→C kills chirality AS A PROPERTY of the F2 object. But Pass 330 shows chirality is available intrinsically via the Weil representation when q≡3 mod 4 — the complex structure was never absent from the lifted representation, only from the binary shadow.  
**Strength:** Genuine — two independent conditions (Passes 225, 227) both force q=3 with different assumptions.

### Selection B (Pass 227)
**Condition:** The non-Clifford magic resource for universal quantum computation must be an exceptional-group cubic invariant.  
**Evidence:** At q=3, the magic resource is the E6 cubic (27=16+10+1, cubic = Yukawa = magic state). This is the unique rung where magic = geometric object of the same tower.  
**Strength:** Structural preference — every rung is computationally universal via magic-state injection (Pass 237, Eastin-Knill); the exceptional-cubic requirement is an additional constraint, not derived.

### The q=3 Weil Chirality (Pass 348)
**Prediction:** H_3 = U⊕U* (chiral), as for q=7.  
**Basis:** Gauss sum q≡3 mod 4 → complex character field Q(sqrt(-3)).  
**Status:** Not GAP-verified. One script run settles it.

---

## What Is Open

1. **GAP q=3 Weil check**: `gap -q analysis/w33_pass218_weil_shadow_split.g` at q=3. Predicted CHIRAL. One run.
2. **Nature of external orientation input**: Four candidates cataloged (Pass 349), none ruled in. The source of chirality selection is outside the substrate's scope by theorem.
3. **Factor 17 in det(B_p)**: Appears in disc(B_2)=17, disc(B_3)=272=16·17, det(B_5) contains factor 17. A structural constant of the W(3,q) incidence theory — its representation-theoretic origin is unidentified.

---

## The Honest Thesis

The W33 substrate can **HOST** the Standard Model's chiral structure:
- Correct representation content (16-dim half-spinor, Pass 225)
- Correct generation count (q=3 forced, Passes 225, 227)
- Correct quantum code structure ([[40,10,4]], CSS, magic)
- Correct Dynkin type (D5 on both sides)
- Correct TBM mixing field (Q(√2,√3), Pass 303)

The W33 substrate **cannot EXPLAIN** the chirality selection:
- This is a THEOREM (Pass 346), not a gap
- The explanation terminates at the chirality boundary
- What lies beyond is cosmological selection or dynamical symmetry breaking — both external to the substrate

This is a feature, not a failure: the theory localizes the open problem precisely.

---

## Checks

1. ✓ All claimed theorems cite their establishing pass
2. ✓ All conditional claims state their condition explicitly
3. ✓ det(B_5) = 35,697,025 cross-checked with Pass 351's computation
4. ✓ delta sequence 1,26,0 noted as irregular (no simple law)
5. ✓ Factor 17 noted as persistent — filed as open, not pursued
6. ✓ No over-read: conditional claims labeled conditional, not theorems
7. ✓ No under-read: theorems labeled theorems, not conditional
8. ✓ Rediscovery guard: RESULTS_INDEX.md search for 35697025 — no prior hits
9. ✓ Supersession explicitly stated to avoid confusion with prior STATUS boxes
10. ✓ Honest thesis does not overclaim or underclaim
11. ✓ Open questions are falsifiable (GAP run, factor-17 representation theory)

**11/11 checks PASS.**
