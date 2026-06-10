# BT755 — Pluecker / Q(4,3) Duo-Mirror Program

BT746 established that chirality is absolute on the `W(3,3)` side: the full collineation group preserves the two presentation torsors.  The note there already points to the key dual fact:

```text
for q odd, W(3,q) is not self-dual; its dual is Q(4,q).
```

BT749 and BT750 now give a local `D12` selector structure inside `W(3,3)`:

```text
24 lifts = 2 chirality x 6 phase x 2 duo,
```

where the duo bit is the central half-turn `r^6` in the inner `Z12` rectangle stabilizer, and BT750 shows the two duo partners are different Levi apartments.

This file records the exact dual-side program: chase that local structure through the Pluecker correspondence to `Q(4,3)`.

## Expected dictionary

| W(3,3) side | Q(4,3) / Pluecker side to test |
|---|---|
| point-line incidence building | dual parabolic quadric incidence building |
| rectangle stabilizer `D12` | stabilizer of a dual quadrangle/apartment shadow |
| chirality/reflection class | odd-q broken self-duality class |
| phase `0..5` | six projective orderings of a dual conic/line-pair frame |
| duo bit `r^6` | central polarity/half-turn on the dual apartment shadow |
| duo partners are different octagons | two distinct dual apartments sharing the same reflection shadow |

## Concrete tests for the next verifier

A future `bt755_plucker_q43_duo_mirror.py` should implement:

1. Build `Q(4,3)` explicitly as points on a nondegenerate parabolic quadratic form in `PG(4,3)`.
2. Build the dual incidence graph and confirm it is dual to `W(3,3)` rather than isomorphic by point-line interchange.
3. Transport a seed `W(3,3)` rectangle/lift pair to the Pluecker/quadric model.
4. Compute the dual stabilizer of the transported local object.
5. Verify whether the same local `D12` appears.
6. Identify the image of the central half-turn `r^6`.
7. Test whether the two `r^6` duo partners become:
   - two dual apartments;
   - two orientations of one dual apartment;
   - or two distinct objects joined by a polarity shadow.

## Why this matters

BT750 proves the duo bit is real on the `W(3,3)` apartment side.  If the Pluecker mirror makes the duo bit into a polarity/quadric orientation, then the root-natural selector will have a geometric interpretation rather than only a centralizer-coordinate definition.

That would turn the selector target from

```text
choose (tau, epsilon, phi, delta)
```

into

```text
choose one Pluecker-polarized dual apartment shadow.
```

## Boundary

BT755 is a program note, not a completed Pluecker computation.  It is pushed now so the next run can implement the dual model without losing the exact tests forced by BT750 and BT754.
