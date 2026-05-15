# Part DCCXLIII — Nilpotent Logarithm / Action Bridge

## Why this part exists

DCCXL gave the one-step generator, DCCXLI gave its exact resolvent kernel, and DCCXLII extracted the correct nilpotent spectral content. The next natural step is to form the exact finite logarithm of the response operator.

## Exact nilpotent logarithm

Because the generator is nilpotent of index 6, the logarithm truncates exactly:

```text
A(z) = -log(I - zG) = zG + z^2 G^2 / 2 + z^3 G^3 / 3 + z^4 G^4 / 4 + z^5 G^5 / 5.
```

So the closure action kernel is again a finite polynomial, not a formal infinite series.

## Closed-form entries at z = 1

The verifier proves

```text
A(1)_(ij) = 1 / ((j-i) 2^(j-i))   for j > i,
A(1)_(ij) = 0                     otherwise.
```

In particular:

- `A(1)_(0,1) = 1/2`
- `A(1)_(0,2) = 1/8`
- `A(1)_(0,3) = 1/24`
- `A(1)_(0,5) = 1/160`

## Exact action-to-response law

The verifier also proves that for the sampled values of `z`,

```text
exp(A(z)) = (I - zG)^(-1).
```

So the nilpotent logarithm action exponentiates back to the exact closure resolvent.

## Trace and determinant invariants

Because `A(z)` is strictly upper triangular:

- `tr A(z) = 0`
- `det(I - zG) = 1`
- `log det(I - zG) = 0`

So the effective-action layer is nontrivial in its off-diagonal transport content, while its scalar determinant invariant vanishes exactly.

## Meaning

The closure-time chain now has:

- generator,
- semigroup,
- resolvent,
- Jordan/residue spectral content,
- and a finite exact logarithm action.

This is the cleanest nilpotent effective-action layer of the closure chain so far.

## Exact vs conditional

- **Exact:** the closure chain has an exact finite logarithm action kernel `A(z) = -log(I-zG)`.
- **Conditional:** interpreting this as a continuum effective action still requires a scaling limit.

## Executable artifact

- Verifier: `verify_dccxliii_nilpotent_logarithm_action_bridge.py`
- Tests: `tests/test_dccxliii_nilpotent_logarithm_action_bridge.py`
- Data: `data/dccxliii_nilpotent_logarithm_action_bridge.json`
