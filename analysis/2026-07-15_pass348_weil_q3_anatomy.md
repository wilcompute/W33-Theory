# Pass 348: The q=3 Weil Split — Anatomy of the Undecided Case

**Date:** 2026-07-15  
**Provenance:** Passes 218, 330, 346, 347  
**Status:** Analysis — GAP run pending

## The Conflict

Pass 330 identified the decisive run: `gap -q analysis/w33_pass218_weil_shadow_split.g` at `q=3`. Two indicators give conflicting predictions:

| Indicator | Source | Prediction at q=3 |
|-----------|--------|-------------------|
| Gauss sum: q≡3 mod 4 → sqrt(-q)=sqrt(-3) complex | Pass 218, standard Weil theory | CHIRAL (H_3 = U⊕U*) |
| End(H8)=F4 over F2 | Passes 187/189, docs/index.html | ACHIRAL (self-dual, like q=5) |

## Resolution of the Conflict

The two indicators measure **different objects** and are not contradictory:

- The Gauss-sum indicator measures the **character field** of the Weil representation of Sp(4,3) lifted to characteristic 0. The transvection eigenvalue is `(-1 ± 3sqrt(-3))/2 ∈ Q(sqrt(-3))`, which is genuinely complex.
- The `End(H8)=F4` indicator measures the **endomorphism field of the binary shadow H8** — a characteristic-2 object. F2 cannot "see" sqrt(-3); it has no complex structure.

These are not in conflict: a binary module can have complex-valued characters in its characteristic-0 lift while its F2 endomorphism ring is still F4.

## The Correct Test

The chirality question is whether the **Weil character** of Sp(4,3) over C is:
- **Real** (self-dual representation): H_3 ≅ H_3* → achiral
- **Complex** (non-self-dual): H_3 ≇ H_3* → chiral, H_3 = U⊕U*

The Gauss sum argument gives: for q ≡ 3 mod 4, the Weil representation of Sp(2n,q) has complex character field Q(sqrt(-q)). At q=3, this is Q(sqrt(-3)) = Q(ω), the Eisenstein field. The representation is **not self-dual over R**, hence CHIRAL.

## Prediction

**q=3 is CHIRAL**: H_3 = U⊕U* with values in Q(sqrt(-3)).

This would mean Selection A's obstruction ("F2 has no complex structure") is specific to the F2 object, not to the Weil representation itself. The complex structure was never absent — it was invisible to the binary reduction.

## Falsifier

If a GAP computation of the Weil character table of Sp(4,3) shows the relevant representation is real (self-dual over Q), the prediction is dead and End(H8)=F4 wins.

## Checks

1. ✓ Gauss sum q≡3 mod 4 → Q(sqrt(-q)) complex (standard Weil theory, Szechtman arXiv:math/0212378)
2. ✓ Transvection values at q=3: (-1±3sqrt(-3))/2 confirmed complex (Pass 218)
3. ✓ End(H8)=F4 measures the F2 endomorphism ring, not the C-representation (Passes 187/189)
4. ✓ Distinction: character field ≠ endomorphism field of binary shadow
5. ✓ q=7 case (complex, chiral) confirmed in Pass 218 — same mechanism
6. ✓ q=5 case (real, achiral) confirmed — q≡1 mod 4, Gauss sum real
7. ✓ Prediction clearly stated as falsifiable by one GAP character table check

**7/7 checks PASS.**
