# From native six-term gauge repair to the 28-point Klein-quadric complement

**Date:** 28 October 2026. This is a cross-track exact algebraic result for the **existing native** `27/135` voltage-cover Maxwell-style construction and the **existing** finite `Q^+(5,2)` / `28_6,56_3` Klein-quadric workbench. It is not a derivation of a physical photon, E8 gauge representation, Lorentzian dynamics, a 5:3 physical constant or a complete theory of everything.

**Source:** `analysis/w33_20261028_f2_klein_native_gauge_bridge.py`; controls in `tests/test_w33_20261028_f2_klein_native_gauge_bridge.py`; frozen `data/w33_20261028_f2_klein_native_gauge_bridge.json`.

## Construction

The native six-commutator flux space is the ordered 6D bivector representation with coordinates `(01,02,03,12,13,23)`. The Klein/Plücker quadratic is

```text
Pf(v) = v01*v23 - v02*v13 + v03*v12.
```

In characteristic zero the six-term repair packet `analysis/2026-10-28_six_term_native_bloch_repair.md` proved **all fifteen** ways of adding two literal native commutator channels to the existing three mixed magnetic channels have rank five and a one-dimensional kernel with integer Pfaffian nonzero. All 15 are complete on every abstract nonzero complex momentum bivector. The selected repair uses channels (0,5) and primitive kernel `(0,1,1,1,0,0)`, with **Pfaffian 1**.

## Exact reduction to finite geometry

Reduce the primitive integer bivector coordinates modulo two. There are 63 nonzero vectors of `Lambda^2 F2^4`; projectively they are the 63 points of `PG(5,2)`. Direct enumeration yields:

```text
Pf(v)=0: 35 points on the Klein quadric Q+(5,2).
Pf(v)=1: 28 points outside Q+(5,2).
```

These are not arbitrary numerological counts: the 28 nondegenerate alternating forms form one orbit under `GL4(2)` (order 20160), with `Sp4(2)` stabilizer of order 720. Thus **20160/720=28**. The existing W33 `28/56/8` workbench also features these 28 finite points and their 8-label combinatorial structure; no canonical map from the selected gauge kernel to one named 8-label pair is asserted without fixing an equivariant identification.

All fifteen channel choices were independently reduced mod2; each five-by-six matrix retains rank five. **Exactly 12** primitive kernels have odd Pfaffian and remain nondecomposable over `F2`; **three** have even Pfaffian and become decomposable. The fifteen pairs collapse to **six distinct nonsingular** and **one singular** projective mod2 point. This arithmetic distinction is obscured if all 15 characteristic-zero completions are treated as identical.

## Complete momentum test over F2

For every one of the 15 nonzero vectors `d in F2^4`, evaluate the actual four-by-six decomposable-momentum wedge map `C(d):u -> d wedge u` and the five-row channel projection `A=[R;P]`.

- For each of the **12 odd-Pfaffian pairs**, `rank_F2(A C(d))=3` for all nonzero d.
- For each of the **three even-Pfaffian pairs**—(0,1), (0,3), (1,3)—rank drops to **2** exactly at `d=0001,1110,1111`.

The optimized pair **(0,5)** survives all characteristic-two momentum directions, so it is a better arithmetic candidate for interfacing to binary stabilizer and syndrome geometry than an integer pair with Pfaffian divisible by two. This does **not** claim a fault-tolerance threshold, that the 40-mode W33 CSS encoding automatically implements this native gauge action, or that experimental photon polarizations are classified by the 28-set.

## Why this bridge matters

The same geometry now supplies a *functional certificate* in two settings:

1. In the native four-period gauge symbol, **decomposable momentum bivectors** are the subspace that can create magnetic gauge/kernel defects. A **nondecomposable** one-dimensional flux-kernel avoids all of them.
2. In finite `PG(5,2)`, decomposable bivectors form the **35-point Klein quadric**, with **28 complementary** nondecomposable bivectors. The kernel of the selected native channel design reduces to one of those 28.

This is a precise shared algebraic mechanism, stronger than seeing the same integer in two independent counting formulas. Nevertheless, it is a **mathematical correspondence**, not a derivation of the electromagnetic field's existence or the physical coupling scale.

## Independent next experimental/theoretical fronts

1. Derive an explicit **equivariant labeling** of the 28 nondecomposable kernels by the 28 unordered pairs of eight Conwell-heptad labels, tracking native H27 actions rather than assigning labels by hand.
2. Determine whether the 12 odd-Pfaffian pairs survive an **encoded binary/ternary CSS photonic circuit** with native commutator measurements and a real noise model.
3. Classify the six distinct finite nonsingular kernels under the **actual automorphism group of the native voltage cover**, checking whether choosing pair (0,5) breaks any physical or discrete symmetry.
4. Test **two-to-five cosine** repairs using the exact global exceptional quadratic sheet and positivity, while retaining the six-term theorem as the verified all-momentum fallback.
5. Investigate whether a dynamical matter determinant selects a **canonical symplectic form/kernel** from the 28 possibilities, or if this is arbitrary symmetry-breaking data.
