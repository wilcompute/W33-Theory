# Part CCCCCXCIV — Tomotope Six-Kernel Label Match

This part turns the `k^6` monodromy-kernel statement from Part CCCCCXCIII into a concrete label-matching ledger.

The tomotope cover law gave:

```text
|Mon(Q_k)| = 192^2 * k^6.
```

So the free toroidal phase kernel has rank six at the order-accounting level.  Here we record a canonical six-slot matching between the recurring six-packets already present in the program.

---

## 1. Six-slot carrier

Use a fixed abstract kernel basis:

```text
K = {k1, k2, k3, k4, k5, k6}.
```

All later labels are attached to this same six-slot carrier.

---

## 2. Label families matched to the six slots

We use the following six-element label families:

```text
A2 roots:                 {alpha1, alpha2, alpha3, alpha4, alpha5, alpha6}
tetrahedral bivectors:    {B01, B02, B03, B12, B13, B23}
W(E6) singleton orbits:   {s1, s2, s3, s4, s5, s6}
pointed-shell remainders: {r1, r2, r3, r4, r5, r6}
```

The content of this part is not a unique geometric embedding claim.  It is the exact finite statement that each family is placed in bijection with the same six kernel slots.

---

## 3. Kernel dictionary schema

The executable dictionary constraint is:

```text
slot -> (A2 root, bivector, singleton, remainder)
```

with each coordinate projection a permutation/bijection of the corresponding six-label family.

Equivalently, each family gives one coordinate chart on the same rank-six kernel.

---

## 4. Consistency identities

The exact checks are:

```text
|K| = 6,
|A2| = |Biv| = |S| = |R| = 6,
all four slot-projections are bijections,
|Mon(Q_k)| / 192^2 = k^6.
```

So the label ledger is consistent with the algebraic six-phase mechanism from Part CCCCCXCIII.

---

## 5. Synthesis

This gives a machine-checkable bridge:

```text
k^6 toroidal monodromy kernel
   <-> six abstract slots
   <-> six A2 roots
   <-> six tetrahedral bivectors
   <-> six W(E6) singletons
   <-> six pointed-shell remainders.
```

The statement is intentionally conservative: it locks the shared six-slot combinatorics exactly, while leaving geometric realization freedom for subsequent parts.
