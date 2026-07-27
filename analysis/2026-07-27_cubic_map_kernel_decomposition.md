# Step 4 — Cubic-Map Kernel: Irreducible Decomposition of the 2195-dim Kernel

**Date:** 2026-07-27  
**Map:** The cubic-support map `φ: V^{⊗3} → W` where  
- Domain: some 2240-dimensional space (cubic forms on the point carrier)  
- Codomain: 45-dimensional space  
- Kernel dimension: 2195  
- Proven Steinberg summand: `3·81 = 243` dimensions  

## Corrected spectral basis for the decomposition

With `spec(D) = 11¹ ⊕ 1²⁴ ⊕ (−5)¹⁵`, the symmetric tensor powers of the
point carrier (as an `Sp(4,3)`-module) are:

```
Sym²(40) decomposes according to the plethysm of the SRG(40,12,2,4) module.
Sym³(40) = the 2240-dim space (if correct dimension) must include
           the trivial module, the Steinberg module St, and other irreducibles.
```

The 2195-dim kernel `K = ker(φ)` is an `Sp(4,3)`-submodule of the cubic space.

## The proven 3·81 Steinberg summand

The Steinberg module for `Sp(4,3)` has dimension `3^4 = 81` (= q^{dim/2} for
Sp(2n, q) with n=2, q=3). The kernel contains `3` copies of it:

```
K ⊇ St^{⊕3},   dim(St^{⊕3}) = 243
```

Remaining kernel dimension after removing Steinberg: `2195 − 243 = 1952`.

## Search for the next bridge module

### Via the signed 27-label module

The E₆ Weyl group acts on 27 labels (the 27 lines of a cubic surface).
If the W(3,3) geometry admits an E₆-equivariant map to this 27-label set,
then the `27`-dimensional module may appear in the kernel decomposition.

Test: Does `2195 − 243 = 1952` contain a `27`-dimensional summand?  
`1952 / 27 = 72.3...` — not integral, so pure 27-copies unlikely.  
But `1952 = 27·k + r` for various small k: check `1952 − 27 = 1925`,
`1925 / 25 = 77` — suggests `1952 = 27 + 25·77 = 27 + 1925`. Inconclusive.

### Via exterior powers

`∧²(40) = 780-dim`, `∧³(40) = 9880-dim` — these are too large for the
1952-dim residual unless heavily projected.

The relevant exterior power to check is `∧²(24)` (from the 24-dim eigenspace):
`∧²(24) = 276-dim`. Does 1952 contain 276-dim summands? `1952 / 276 = 7.07...`.
Not obviously integral, but 7 copies of 276 = 1932, leaving 20-dim residual.

### Via the frame-kernel intertwiner

The "frame" in W(3,3) is the collection of maximal totally isotropic subspaces
(spreads). These give intertwiners between the point carrier and line carrier.
The line carrier of W(3,3) has 130 lines; the collinearity graph of lines is
known. Projecting the cubic kernel through a frame-kernel intertwiner may
isolate a `45`-dim codomain complement.

## Decomposition algorithm (for GAP/Sage)

```python
# Pseudocode for Sage/GAP decomposition
# 1. Construct the 2240-dim Sp(4,3)-module as a submodule of Sym^3(V)
# 2. Compute the 2195-dim kernel K of phi
# 3. Use meataxe / Schur functor to find irreducible summands of K:
#    CompositionFactors(K)  in GAP's MeatAxe
# 4. Identify each factor via its dimension and character
# 5. Check if 3*81 (Steinberg) accounts for 243 dims
# 6. Identify the next largest summand and cross-reference with:
#    - signed 27-label module (E6 type)
#    - exterior power ∧²(24) of the 24-dim eigenspace
#    - standard 40-dim module itself
```

## Connection to (1 + 24 + 15) selection rules

The corrected eigenspace decomposition predicts that the cubic-map kernel,
when projected onto each eigenspace of D, has a specific rank profile:

- Projection onto `P_11·K` (1-dim eigenspace): at most 1-dim contribution
- Projection onto `P_1·K` (24-dim eigenspace): likely the dominant summand
- Projection onto `P_{-5}·K` (15-dim eigenspace): Steinberg is expected here
  since the 15-dim eigenspace of the SRG(40,12,2,4) corresponds to the
  "conic" or "hyperbolic" module in the symplectic geometry.

## Status

- [x] Kernel dimension 2195 and Steinberg summand 3·81 recorded
- [x] Signed 27-label and exterior power candidates analyzed
- [ ] GAP MeatAxe decomposition of K (requires full module construction)
- [ ] Cross-reference with 432-orbit stabilizer types (Step 3)
- [ ] Identify the next viable bridge module beyond Steinberg
