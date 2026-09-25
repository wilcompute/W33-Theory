# Pass 10956 — the Albert Peirce 16 contains the same Spin(8) half-spin transposition

Producer: `analysis/w33_pass10956_albert_spin8_halfspin_normalizer.py`

Certificate: `data/w33_pass10956_albert_spin8_halfspin_normalizer.json`

Regression: `tests/test_w33_pass10956_albert_spin8_halfspin_normalizer.py`

## 1. Spin(8) is constructed inside the executable Spin(9)

Pass 10950 certified a compact 36-dimensional spin(9) stabilizer of a primitive Albert idempotent and its absolutely irreducible action on the Peirce 16.

Fix the explicit spatial Peirce-0 direction

```text
s0 = e_g2 - e_g3.
```

Solving (D s0=0) inside the 36 certified generators gives an exact 28-dimensional Lie algebra. This is the expected spin(8) stabilizer of one spatial axis.
## 2. The Peirce 16 splits objectwise as 8_s + 8_c

Restrict the executable 16x16 Spin(9) matrices to that 28-dimensional stabilizer. The exact commutant has dimension two.

Removing the scalar identity from the commutant gives a rational matrix whose square is one quarter of the identity. After exact rescaling, this produces an involution

```text
Chi^2 = I16,
Tr Chi = 0,
Spec Chi = (+1)^8 + (-1)^8.
```

The two projector images each have dimension eight. Each restricted 8D module has scalar commutant, and the cross-intertwiner space between them has dimension zero.

Therefore the executable branching is

```text
16 -> 8_s + 8_c
```

with two inequivalent irreducible Spin(8) half-spin modules.
## 3. A finite Spin(9) half-turn exchanges the two 8s

Choose a second spatial Peirce-0 vector (z) orthogonal to (s0), and form the certified derivation

```text
Drot = [L_s0,L_z] in spin(9).
```

Its vector action is a single rotation plane. Exponentiating to a pi rotation produces an element (U_pi) that sends the chosen spatial axis to its negative. Hence it normalizes the same **unoriented** Spin(8) stabilizer.

On the Peirce 16 the executable gives

```text
U_pi Chi U_pi^-1 = -Chi
```

to (6.2e-15), and the two 8D projector images are exchanged to (3.1e-15).

So the half-spin transposition is realized on the actual Albert spinor carrier, not merely on a D4 weight diagram.
## 4. Its square is the existing matter-parity sign

The same half-turn obeys

```text
U_pi^2 = -I16
U_pi^4 = I16
```

within numerical errors below (1.3e-14).

Pass 10950 independently proved that (-I) on this Peirce 16 is the (2pi) Spin(9) rotation and equals the repository's matter-parity Peirce symmetry. Thus

```text
Spin(8) half-spin exchange
   --square-->
2pi Spin(9) central sign
   =
matter parity on the Albert 16.
```

This is now an objectwise matrix statement on the same executable carrier.
## 5. Relation to the finite clock theorem

Pass 10955 proved that the determinant-minus-one half of the finite clock/tetracode GL(2,3) fixes the D4 vector weight class and exchanges the two D4 half-spin sheets. Pass 10956 constructs the **same outer transposition type** inside the actual Albert Spin(9) representation:

```text
finite D4 weight carrier: 8_s <-> 8_c
Albert Peirce carrier:     8_s <-> 8_c.
```

Both fix the vector representation class.

But the full elements are not yet identified. The finite clock generator has order eight, while the Spin(9) normalizer half-turn has order four and squares directly to the central spin sign. No homomorphism sending the complete GL(2,3) clock action into Spin(9) has been constructed.

That mismatch is useful: it prevents us from silently equating the algebraic clock tick with a physical spin rotation.
## 6. External representation check and boundary

Standard spin representation theory says an odd-dimensional Spin group has one irreducible spin module, while the corresponding even-dimensional Spin group has two half-spin modules. D4 triality further distinguishes the vector and two half-spin 8-dimensional representation classes. The executable Albert calculation realizes exactly this expected 16-to-8+8 restriction.

## Boundary

This is an executable Albert/Spin branching and normalizer theorem. It does not identify the two 8s with observed fermion handedness, derive Standard-Model chirality, or establish the full order-eight clock as a Spin(9) dynamical operator. The next required step is an actual finite-subgroup or weight-normalizer intertwiner, not another count match.
