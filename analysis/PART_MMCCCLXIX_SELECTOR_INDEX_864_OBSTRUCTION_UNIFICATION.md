# Part MMCCCLXIX: Selector Index 864 Obstruction Unification

## Claim

The selector obstruction integer `864` is not a loose coincidence. It is the
same exact finite number in three independent selector layers:

- negative-polar selector index:
  `|O^-(6,2)| / |A5| = 51840 / 60 = 864`;
- signed local affine shell:
  `2*|AGL(2,3)| = 2*3^2*(3^2-1)*(3^2-3) = 864`;
- golden-selector flatness obstruction:
  `864 = 2^(mu+1)*q^3 = 32*27` ordered failed quadrangles.

The total ordered quadrangle carrier is `12960 = 15*864 = v*k*q^3`, and the
unique failure core is `108 = 864/2^q = mu*q^3`.

## Reading

The raw Clifford selector is an `A5` torsor of order `60`. The W33 spread
selector lives at the negative-polar `W(E6)` scale of order `51840`. The missing
selector index is therefore `864`.

Independently, the golden selector fails on exactly `864` ordered nonlocal
quadrangles, and the signed `AGL(2,3)` local search shell also has exactly
`864` candidates. The obstruction size is therefore the coset-size required to
move from the raw `A5` torsor to the negative-polar selector scale.

## Boundary

This part proves equality of exact counts and their substrate decomposition. It
does not yet construct a canonical bijection from failed ordered quadrangles to
`O^-(6,2)/A5` cosets or to signed `AGL(2,3)` candidates.

The next selector target is explicit: build a canonical transport map whose
fibers send the `108` unique golden failures, with their `8` orientations, onto
the `864` cosets of the raw `A5` torsor inside the negative-polar selector
symmetry.

## Verification

Run:

```bash
python3 analysis/w33_selector_index_864_obstruction_unification.py
```

Expected result: `12/12` checks verified.
