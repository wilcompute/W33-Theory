# Pass 10945 — Choi/Fourier three-channel temporal weld

This pass turns the nine-history temporal picture into an exact repository
intertwiner rather than another count match.  The operator-compatible Fourier
sector has basis `S1(t,r,i)`, with `t,r,i in F3`.  Its evaluation formula
factors into an H27 Schrodinger matrix coefficient and the external-clock
character:

```text
S1(t,r,i)(h,p) = rho_omega(h)[i,r] * omega^(t p).
```

Therefore

```text
S1 = Coeff(V_omega) tensor Reg(C3_external),   27 = 9 * 3.
```

The nine coefficient directions are explicitly intertwined with the nine
qutrit matrix units `E_ir=|i><r|` by the exact Weyl transform
 ```text
E_ir = (1/3) sum_a omega^(-a i) Z^a X^(i-r).
```

All nine identities are checked over `Q(omega)`.  This supplies the missing
algebraic bridge from H27/Weyl coordinates to the nine operator/Choi histories:
the history indices are literally the row and column indices of a qutrit
operator, while the external `C3` factor is a separate clock-phase label.

## Three quotient channels

Inverse Fourier transform in the external character localizes S1 at phase p:

```text
L_(p,r,i) = (1/3) sum_t omega^(-tp) S1(t,r,i).
```

For each of the three 27-coordinate external phase slices `C_p`, exact
Gaussian elimination over `Q(omega)` gives

```text
dim(S1 intersect C_p) = 9,
dim((S1+C_p)/S1) = 18.
```
The three intersections are disjoint and sum to all of S1.  Any pair of phase
slices contributes quotient dimension 36, and all three contribute 54.  Hence

```text
27 = 9 + 9 + 9,
54 = 18 + 18 + 18.
```

The previously proved parabolic `36+18` split is now resolved: the positive
slice P is two external phases and the opposite grade-minus-two slice Q is the
third.  The asymmetry was a parabolic grouping of a more symmetric three-phase
decomposition.

## What the diagonal weld actually releases

The pure center and pure external cubic backgrounds each have quotient rank 36.
Their span has rank 54 and their intersection has dimension 18:

```text
54 = 36 + 36 - 18.
```

More sharply, each pure 36-dimensional weld projects surjectively onto every
single 18-dimensional phase channel and onto every pair of channels.  Therefore
its missing 18 dimensions are not a missing clock phase; they are one
cross-phase linear relation.  Either diagonal center-plus-external or
center-minus-external background has quotient rank 54 and removes that relation.
This replaces the loose statement "diagonal correlation adds more directions"
with an exact mechanism: diagonalization frees the third independent phase
channel while pure backgrounds remain graph subspaces across the three
18-dimensional outputs.

## Boundary

Everything above is exact finite linear algebra over the Eisenstein field and
an exact Weyl/matrix-unit transform.  The word "Choi" refers to the operator
basis `|i><r|`; no claim is made that the three 18-dimensional quotient
channels are spacetime dimensions, particle multiplets, or thermodynamic
future/past sectors.

The numerical resemblance of 9+18 to other finite causal decompositions in the
repository is deliberately not promoted.  An objectwise intertwiner must exist
before those geometries can be identified.

Producer:
`analysis/w33_pass10945_choi_fourier_three_channel_weld.py`

Certificate:
`data/w33_pass10945_choi_fourier_three_channel_weld.json`

Regression:
`tests/test_w33_pass10945_choi_fourier_three_channel_weld.py`
