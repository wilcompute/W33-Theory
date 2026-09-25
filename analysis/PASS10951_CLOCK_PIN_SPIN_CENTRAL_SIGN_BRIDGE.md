# Pass 10951 — the clock Pin/Spin central-sign bridge

Producer: `analysis/w33_pass10951_clock_pin_spin_central_sign_bridge.py`

Certificate: `data/w33_pass10951_clock_pin_spin_central_sign_bridge.json`

Regression: `tests/test_w33_pass10951_clock_pin_spin_central_sign_bridge.py`

## Exact theorem

Pass 10948 found two oriented gauges of the tetracode in which one clock tick is the negacyclic shift. Pass 10946 already identifies the monomial clock group with `GL(2,3)`. Exhaustive matching now shows that the two gauges have unique linear lifts

```text
g- = [[0,1],[1,1]],     g+ = -g- = [[0,2],[2,2]].
```

They project to the same 4-cycle of the four projective clock rays and have minimal polynomials

```text
g- : x^2-x-1,      g+ : x^2+x-1.
```

Both have determinant `-1` and exact order eight.
Their power ladder is

```text
g^2 = [[1,1],[1,2]] in Q8,
g^4 = -I,
g^8 = I.
```

Thus the projective clock closes after four ticks, while its central spin lift closes only after eight. Four ticks are invisible on the four rays but are not the identity on the signed tetracode: they are the global sign `-I`.

## Two different C2 data

This pass separates two index-two structures that must not be conflated.

1. The determinant character
   `det : GL(2,3) -> F3^x ~= C2`
   has kernel `SL(2,3)`. On the four clock rays it is exactly even versus odd permutation parity. By the earlier Hesse null-cone certificate it is also the finite orthogonal spinor norm.

2. The central element `z=-I` has determinant (+1), acts trivially on the four projective rays, and acts as a global minus sign on the tetracode.

The clock lift (g) is determinant-odd, but (g^4=z) is determinant-even. The Pin-component bit and the central spin sign are therefore independent data.
## Explicit Spin(3) model

The determinant-one subgroup has order 24 and contains the quaternion subgroup

```text
Q8 = {elements of orders 1,2,4}.
```

The verifier finds generators (a,b,c) with (a,bin Q_8), (c^3=1), and conjugation by (c) cycling the three quaternion axes. It then constructs, by simultaneous word walk, an explicit isomorphism

```text
SL(2,3)  ->  2T subset Spin(3),
a -> i,   b=g^2 -> j,   c -> -(1+i+j+k)/2.
```

All (24^2) products are checked. Under this map

```text
-I  ->  -1 quaternion.
```

So the fourth clock tick is exactly the central (2\pi) spin rotation in the binary-tetrahedral Spin(3) model.

This also nails an important group-theory boundary: (GL(2,3)) is the **plus** Schur cover (2^+S_4), not the binary octahedral **minus** cover (2^-S_4). The latter is a different order-48 group.
## Weld to the clock Albert spinor

Pass 10950 independently proves, on the executable (E_8) basis, that the Euclidean Albert clock form contains (mathrm{Spin}(9)), that its Peirce 16 is the spinor module, and that the repository's matter parity is the (2\pi) central rotation of (mathrm{Spin}(9)).

The standard inclusion (mathrm{Spin}(3)subsetmathrm{Spin}(9)) sends the central element (-1) to the same central (-1). Therefore the new exact chain is

```text
four clock ticks
   = -I in SL(2,3)
   = -1 in 2T subset Spin(3)
   -> -1 in Spin(9)
   = matter parity on the Pass-10950 Peirce 16.
```

This identifies the **central character**, not the entire order-eight tick action on matter. No matrix intertwiner from the determinant-minus-one clock lift (g) to the Albert spinor is claimed.

## External cross-check and boundary

Standard finite-group literature records the two Schur covers of (S_4) as (2^+S_4\cong GL(2,3)) and the binary octahedral (2^-S_4). It also records (SL(2,3)\cong2T). The executable certificate does not rely on these identifications; it reconstructs the relevant structure directly.

This is a finite group and central-character theorem. It does **not** construct physical time evolution, a continuum Pin bundle, a chirality selector, or the action of each clock tick on a physical fermion field.
